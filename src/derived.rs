//! Derived unit support for compound quantities, backed by `qtty-ffi`.

use pyo3::prelude::*;
use qtty_ffi::{QttyDerivedQuantity, UnitId};

/// A derived unit represented as numerator/denominator.
///
/// Examples:
/// - Velocity: Meter/Second (m/s)
/// - Frequency: Radian/Second (rad/s)
#[pyclass(name = "DerivedUnit", module = "qtty", from_py_object)]
#[derive(Clone, Debug)]
pub struct PyDerivedUnit {
    pub numerator: UnitId,
    pub denominator: UnitId,
}

#[pymethods]
impl PyDerivedUnit {
    #[new]
    fn new(numerator: UnitId, denominator: UnitId) -> PyResult<Self> {
        Ok(Self {
            numerator,
            denominator,
        })
    }

    /// Returns the numerator unit.
    #[getter]
    fn numerator(&self) -> UnitId {
        self.numerator
    }

    /// Returns the denominator unit.
    #[getter]
    fn denominator(&self) -> UnitId {
        self.denominator
    }

    /// Returns the symbol (e.g., "m/s").
    fn symbol(&self) -> String {
        format!("{}/{}", self.numerator.symbol(), self.denominator.symbol())
    }

    fn __repr__(&self) -> String {
        format!("DerivedUnit({:?}, {:?})", self.numerator, self.denominator)
    }

    fn __str__(&self) -> String {
        self.symbol()
    }
}

/// A quantity with a derived unit.
///
/// This represents compound quantities like velocity (m/s) or frequency (rad/s).
/// Wraps QttyDerivedQuantity from qtty-ffi for safe, reusable operations.
#[pyclass(name = "DerivedQuantity", module = "qtty", from_py_object)]
#[derive(Clone)]
pub struct PyDerivedQuantity {
    pub value: f64,
    pub numerator: UnitId,
    pub denominator: UnitId,
}

impl PyDerivedQuantity {
    /// Creates a PyDerivedQuantity from a QttyDerivedQuantity.
    fn from_ffi(inner: QttyDerivedQuantity) -> Option<Self> {
        Some(Self {
            value: inner.value,
            numerator: inner.numerator_id()?,
            denominator: inner.denominator_id()?,
        })
    }

    /// Converts to a QttyDerivedQuantity for FFI operations.
    fn to_ffi(&self) -> QttyDerivedQuantity {
        QttyDerivedQuantity::new(self.value, self.numerator, self.denominator)
    }
}

#[pymethods]
impl PyDerivedQuantity {
    #[new]
    fn new(value: f64, numerator: UnitId, denominator: UnitId) -> PyResult<Self> {
        Ok(Self {
            value,
            numerator,
            denominator,
        })
    }

    /// The numeric value of the derived quantity.
    #[getter]
    fn value(&self) -> f64 {
        self.value
    }

    /// The numerator unit.
    #[getter]
    fn numerator(&self) -> UnitId {
        self.numerator
    }

    /// The denominator unit.
    #[getter]
    fn denominator(&self) -> UnitId {
        self.denominator
    }

    /// The unit symbol (e.g., "m/s").
    fn symbol(&self) -> String {
        format!("{}/{}", self.numerator.symbol(), self.denominator.symbol())
    }

    /// Converts to another derived unit with compatible dimensions.
    ///
    /// Example: convert m/s to km/h
    fn to(&self, numerator: UnitId, denominator: UnitId) -> PyResult<Self> {
        self.to_ffi()
            .convert_to(numerator, denominator)
            .and_then(Self::from_ffi)
            .ok_or_else(|| {
                pyo3::exceptions::PyTypeError::new_err(format!(
                    "Cannot convert {:?}/{:?} to {:?}/{:?}: incompatible dimensions",
                    self.numerator, self.denominator, numerator, denominator
                ))
            })
    }

    /// Multiplies the derived quantity by a scalar.
    fn __mul__(&self, scalar: f64) -> Self {
        Self {
            value: self.value * scalar,
            numerator: self.numerator,
            denominator: self.denominator,
        }
    }

    /// Right multiplication.
    fn __rmul__(&self, scalar: f64) -> Self {
        self.__mul__(scalar)
    }

    /// Divides the derived quantity by a scalar.
    fn __truediv__(&self, scalar: f64) -> PyResult<Self> {
        if scalar == 0.0 {
            return Err(pyo3::exceptions::PyZeroDivisionError::new_err(
                "Division by zero",
            ));
        }
        Ok(Self {
            value: self.value / scalar,
            numerator: self.numerator,
            denominator: self.denominator,
        })
    }

    /// Negates the derived quantity.
    fn __neg__(&self) -> Self {
        Self {
            value: -self.value,
            numerator: self.numerator,
            denominator: self.denominator,
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "DerivedQuantity({}, {:?}, {:?})",
            self.value, self.numerator, self.denominator
        )
    }

    fn __str__(&self) -> String {
        format!("{} {}", self.value, self.symbol())
    }

    /// Pickle support: return (class, args) for unpickling.
    fn __reduce__(&self, py: Python<'_>) -> PyResult<(Py<PyAny>, (f64, UnitId, UnitId))> {
        let cls = py.get_type::<Self>().into_any().unbind();
        Ok((cls, (self.value, self.numerator, self.denominator)))
    }

    /// Serializes this derived quantity to a JSON string.
    ///
    /// The format is: `{"value": <float>, "numerator": <uint>, "denominator": <uint>}`
    ///
    /// Examples:
    /// >>> v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
    /// >>> v.to_json()
    /// '{"value":10.0,"numerator":10011,"denominator":20008}'
    fn to_json(&self) -> PyResult<String> {
        serde_json::to_string(&self.to_ffi()).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!("Serialization error: {e}"))
        })
    }

    /// Deserializes a DerivedQuantity from a JSON string.
    ///
    /// Accepts: `{"value": <float>, "numerator": <uint>, "denominator": <uint>}`
    ///
    /// Raises:
    ///     ValueError: If the JSON is malformed or unit IDs are invalid
    #[staticmethod]
    fn from_json(json: &str) -> PyResult<Self> {
        let inner: QttyDerivedQuantity = serde_json::from_str(json).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!("Deserialization error: {e}"))
        })?;
        Self::from_ffi(inner).ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err(
                "Deserialization error: invalid numerator or denominator unit ID",
            )
        })
    }
}
