//! Python Quantity class implementation (UnitId-first API).
//!
//! Relies on safe `qtty-ffi` helpers instead of custom parsing logic.

use pyo3::exceptions::{PyTypeError, PyZeroDivisionError};
use pyo3::prelude::*;
use qtty_ffi::{QttyQuantity, UnitId};

use crate::derived::PyDerivedQuantity;
use crate::errors::map_dimension_error;

/// A physical quantity with a value and unit.
///
/// Quantities support arithmetic operations with automatic dimension checking.
/// Units are represented using the UnitId enum from Rust.
///
/// Examples:
/// >>> from qtty import Quantity, Unit
/// >>> q = Quantity(100.0, Unit.Meter)
/// >>> q.value
/// 100.0
/// >>> q.unit
/// Unit.Meter
/// >>> km = q.to(Unit.Kilometer)
/// >>> km.value
/// 0.1
#[pyclass(name = "Quantity", module = "qtty")]
#[derive(Clone)]
pub struct PyQuantity {
    inner: QttyQuantity,
}

#[pymethods]
impl PyQuantity {
    /// Creates a new Quantity with the given value and unit.
    ///
    /// Args:
    ///     value: The numeric value of the quantity
    ///     unit: The unit (UnitId enum value)
    ///
    /// Returns:
    ///     A new Quantity instance
    ///
    /// Examples:
    /// >>> from qtty import Quantity, Unit
    /// >>> q = Quantity(100.0, Unit.Meter)
    /// >>> q.value
    /// 100.0
    #[new]
    fn new(value: f64, unit: UnitId) -> PyResult<Self> {
        Ok(Self {
            inner: QttyQuantity::new(value, unit),
        })
    }

    /// The numeric value of the quantity.
    #[getter]
    fn value(&self) -> f64 {
        self.inner.value
    }

    /// The unit of the quantity.
    #[getter]
    fn unit(&self) -> UnitId {
        self.inner.unit
    }

    /// Converts this quantity to another unit of the same dimension.
    ///
    /// Args:
    ///     unit: The target unit (UnitId enum value)
    ///
    /// Returns:
    ///     A new Quantity with the converted value and unit
    ///
    /// Raises:
    ///     TypeError: If the units have incompatible dimensions
    ///
    /// Examples:
    /// >>> from qtty import Quantity, Unit
    /// >>> m = Quantity(1000.0, Unit.Meter)
    /// >>> km = m.to(Unit.Kilometer)
    /// >>> km.value
    /// 1.0
    fn to(&self, unit: UnitId) -> PyResult<Self> {
        self.inner
            .convert_to(unit)
            .map(|inner| Self { inner })
            .ok_or_else(|| map_dimension_error(self.inner.unit, unit))
    }

    /// Returns the absolute value of the quantity.
    ///
    /// Examples:
    /// >>> from qtty import Quantity, Unit
    /// >>> q = Quantity(-10.0, Unit.Meter)
    /// >>> abs(q).value
    /// 10.0
    fn __abs__(&self) -> Self {
        Self {
            inner: QttyQuantity::new(self.value().abs(), self.inner.unit),
        }
    }

    /// Adds two quantities with compatible dimensions.
    ///
    /// The result has the same unit as the left operand.
    ///
    /// Raises:
    ///     TypeError: If the dimensions are incompatible
    fn __add__(&self, other: &PyQuantity) -> PyResult<Self> {
        self.inner
            .add(&other.inner)
            .map(|inner| Self { inner })
            .ok_or_else(|| map_dimension_error(self.inner.unit, other.inner.unit))
    }

    /// Subtracts two quantities with compatible dimensions.
    ///
    /// The result has the same unit as the left operand.
    ///
    /// Raises:
    ///     TypeError: If the dimensions are incompatible
    fn __sub__(&self, other: &PyQuantity) -> PyResult<Self> {
        self.inner
            .sub(&other.inner)
            .map(|inner| Self { inner })
            .ok_or_else(|| map_dimension_error(self.inner.unit, other.inner.unit))
    }

    /// Multiplies the quantity by a scalar.
    ///
    /// Examples:
    /// >>> from qtty import Quantity, Unit
    /// >>> q = Quantity(10.0, Unit.Meter)
    /// >>> (q * 2.5).value
    /// 25.0
    fn __mul__(&self, other: &Bound<'_, PyAny>) -> PyResult<Self> {
        if let Ok(scalar) = other.extract::<f64>() {
            Ok(Self {
                inner: self.inner.mul_scalar(scalar),
            })
        } else {
            Err(PyTypeError::new_err(
                "Quantity can only be multiplied by a scalar (float or int). \
                 Multiplying two quantities is not yet supported; divide to create derived rates.",
            ))
        }
    }

    /// Right multiplication (scalar * quantity).
    fn __rmul__(&self, other: &Bound<'_, PyAny>) -> PyResult<Self> {
        self.__mul__(other)
    }

    /// Divides the quantity by a scalar or another quantity.
    ///
    /// When dividing by a scalar, the unit is preserved.
    /// When dividing by another quantity with compatible dimensions, returns a dimensionless ratio.
    /// When dividing by another quantity with different dimensions, returns a DerivedQuantity.
    ///
    /// Examples:
    /// >>> m = Quantity(100.0, Unit.Meter)
    /// >>> s = Quantity(10.0, Unit.Second)
    /// >>> velocity = m / s  # Returns DerivedQuantity(10.0, Meter, Second)
    ///
    /// Raises:
    ///     ZeroDivisionError: If dividing by zero
    fn __truediv__(&self, other: &Bound<'_, PyAny>) -> PyResult<PyObject> {
        let py = other.py();
        
        // Try to extract as f64 first (scalar division)
        if let Ok(scalar) = other.extract::<f64>() {
            if scalar == 0.0 {
                return Err(PyZeroDivisionError::new_err("Division by zero"));
            }
            let result = Self {
                inner: self.inner.div_scalar(scalar),
            };
            return Ok(result.into_py(py));
        }

        // Try to extract as PyQuantity (quantity division)
        if let Ok(q) = other.extract::<PyQuantity>() {
            // Check if dimensions are compatible using safe method
            if self.inner.compatible(&q.inner) {
                // Same dimension: return dimensionless quantity
                let q_converted = q.to(self.unit())?;
                if q_converted.value() == 0.0 {
                    return Err(PyZeroDivisionError::new_err("Division by zero"));
                }
                let ratio = self.value() / q_converted.value();
                let result = Self {
                    inner: QttyQuantity::new(ratio, self.inner.unit),
                };
                return Ok(result.into_py(py));
            } else {
                // Different dimensions: return DerivedQuantity (e.g., m/s)
                if q.value() == 0.0 {
                    return Err(PyZeroDivisionError::new_err("Division by zero"));
                }
                let derived = PyDerivedQuantity {
                    value: self.value() / q.value(),
                    numerator: self.inner.unit,
                    denominator: q.inner.unit,
                };
                return Ok(derived.into_py(py));
            }
        }
        
        Err(PyTypeError::new_err(
            "Quantity can only be divided by a scalar or another Quantity",
        ))
    }

    /// Floor division (not yet implemented for quantities).
    fn __floordiv__(&self, _other: &Bound<'_, PyAny>) -> PyResult<Self> {
        Err(pyo3::exceptions::PyNotImplementedError::new_err(
            "Floor division is not supported for Quantity",
        ))
    }

    /// Modulo operation (not yet implemented for quantities).
    fn __mod__(&self, _other: &Bound<'_, PyAny>) -> PyResult<Self> {
        Err(pyo3::exceptions::PyNotImplementedError::new_err(
            "Modulo operation is not supported for Quantity",
        ))
    }

    /// Negates the quantity.
    ///
    /// Examples:
    /// >>> q = Quantity(10.0, "Meter")
    /// >>> (-q).value
    /// -10.0
    fn __neg__(&self) -> Self {
        Self {
            inner: self.inner.neg(),
        }
    }

    /// Positive unary operator (returns self).
    fn __pos__(&self) -> Self {
        self.clone()
    }

    /// Equality comparison.
    ///
    /// Two quantities are equal if they have the same dimension and
    /// represent the same value when converted to a common unit.
    fn __eq__(&self, other: &PyQuantity) -> PyResult<bool> {
        if !self.inner.compatible(&other.inner) {
            return Ok(false);
        }

        let other_converted = other.to(self.unit())?;
        Ok((self.value() - other_converted.value()).abs() < 1e-12)
    }

    /// Inequality comparison.
    fn __ne__(&self, other: &PyQuantity) -> PyResult<bool> {
        Ok(!self.__eq__(other)?)
    }

    /// Less than comparison.
    ///
    /// Raises:
    ///     TypeError: If the dimensions are incompatible
    fn __lt__(&self, other: &PyQuantity) -> PyResult<bool> {
        if !self.inner.compatible(&other.inner) {
            return Err(map_dimension_error(self.inner.unit, other.inner.unit));
        }

        let other_converted = other.to(self.unit())?;
        Ok(self.value() < other_converted.value())
    }

    /// Less than or equal comparison.
    fn __le__(&self, other: &PyQuantity) -> PyResult<bool> {
        if !self.inner.compatible(&other.inner) {
            return Err(map_dimension_error(self.inner.unit, other.inner.unit));
        }

        let other_converted = other.to(self.unit())?;
        Ok(self.value() <= other_converted.value())
    }

    /// Greater than comparison.
    fn __gt__(&self, other: &PyQuantity) -> PyResult<bool> {
        if !self.inner.compatible(&other.inner) {
            return Err(map_dimension_error(self.inner.unit, other.inner.unit));
        }

        let other_converted = other.to(self.unit())?;
        Ok(self.value() > other_converted.value())
    }

    /// Greater than or equal comparison.
    fn __ge__(&self, other: &PyQuantity) -> PyResult<bool> {
        if !self.inner.compatible(&other.inner) {
            return Err(map_dimension_error(self.inner.unit, other.inner.unit));
        }

        let other_converted = other.to(self.unit())?;
        Ok(self.value() >= other_converted.value())
    }

    /// Returns a detailed representation of the quantity.
    fn __repr__(&self) -> String {
        format!("Quantity({}, {:?})", self.value(), self.unit())
    }

    /// Returns a human-readable string representation.
    fn __str__(&self) -> String {
        format!("{} {}", self.value(), self.inner.unit.name())
    }

    /// Pickle support: return (class, args) for unpickling.
    fn __reduce__(&self, py: Python) -> PyResult<(PyObject, (f64, UnitId))> {
        let cls = py.get_type_bound::<Self>();
        Ok((cls.into_any().unbind(), (self.value(), self.unit())))
    }

    /// Returns a hash of the quantity (for use in sets and dicts).
    fn __hash__(&self) -> u64 {
        // Simple hash combining value and unit
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};

        let mut hasher = DefaultHasher::new();
        self.value().to_bits().hash(&mut hasher);
        (self.inner.unit as u32).hash(&mut hasher);
        hasher.finish()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quantity_creation() {
        pyo3::prepare_freethreaded_python();

        let q = PyQuantity::new(100.0, UnitId::Meter).unwrap();
        assert_eq!(q.value(), 100.0);
        assert_eq!(q.unit(), UnitId::Meter);
    }

    #[test]
    fn test_quantity_conversion() {
        pyo3::prepare_freethreaded_python();

        let m = PyQuantity::new(1000.0, UnitId::Meter).unwrap();
        let km = m.to(UnitId::Kilometer).unwrap();
        assert!((km.value() - 1.0).abs() < 1e-12);
        assert_eq!(km.unit(), UnitId::Kilometer);
    }

    #[test]
    fn test_incompatible_conversion() {
        pyo3::prepare_freethreaded_python();

        let m = PyQuantity::new(100.0, UnitId::Meter).unwrap();
        let result = m.to(UnitId::Second);
        assert!(result.is_err());
    }
}
