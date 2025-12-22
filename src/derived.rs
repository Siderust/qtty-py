//! Derived unit support for compound quantities, backed by `qtty-ffi`.

use pyo3::prelude::*;
use qtty_ffi::{QttyDerivedQuantity, UnitId};

/// A derived unit represented as numerator/denominator.
///
/// Examples:
/// - Velocity: Meter/Second (m/s)
/// - Frequency: Radian/Second (rad/s)
#[pyclass(name = "DerivedUnit", module = "qtty")]
#[derive(Clone, Debug)]
pub struct PyDerivedUnit {
    pub numerator: UnitId,
    pub denominator: UnitId,
}

#[pymethods]
impl PyDerivedUnit {
    #[new]
    fn new(numerator: UnitId, denominator: UnitId) -> PyResult<Self> {
        Ok(Self { numerator, denominator })
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
        format!(
            "DerivedUnit({:?}, {:?})",
            self.numerator, self.denominator
        )
    }

    fn __str__(&self) -> String {
        self.symbol()
    }
}

/// A quantity with a derived unit.
///
/// This represents compound quantities like velocity (m/s) or frequency (rad/s).
/// Wraps QttyDerivedQuantity from qtty-ffi for safe, reusable operations.
#[pyclass(name = "DerivedQuantity", module = "qtty")]
#[derive(Clone)]
pub struct PyDerivedQuantity {
    pub value: f64,
    pub numerator: UnitId,
    pub denominator: UnitId,
}

impl PyDerivedQuantity {
    /// Creates a PyDerivedQuantity from a QttyDerivedQuantity.
    fn from_ffi(inner: QttyDerivedQuantity) -> Self {
        Self {
            value: inner.value,
            numerator: inner.numerator,
            denominator: inner.denominator,
        }
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
        Ok(Self { value, numerator, denominator })
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
        self.to_ffi().symbol()
    }

    /// Converts to another derived unit with compatible dimensions.
    ///
    /// Example: convert m/s to km/h
    fn to(&self, numerator: UnitId, denominator: UnitId) -> PyResult<Self> {
        self.to_ffi()
            .convert_to(numerator, denominator)
            .map(Self::from_ffi)
            .ok_or_else(|| {
                pyo3::exceptions::PyTypeError::new_err(format!(
                    "Cannot convert {:?}/{:?} to {:?}/{:?}: incompatible dimensions",
                    self.numerator, self.denominator, numerator, denominator
                ))
            })
    }

    /// Multiplies the derived quantity by a scalar.
    fn __mul__(&self, scalar: f64) -> Self {
        Self::from_ffi(self.to_ffi().mul_scalar(scalar))
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
        Ok(Self::from_ffi(self.to_ffi().div_scalar(scalar)))
    }

    /// Negates the derived quantity.
    fn __neg__(&self) -> Self {
        Self::from_ffi(self.to_ffi().neg())
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

    // Pickling support intentionally omitted: returning the raw `UnitId` from
    // `qtty-ffi` keeps the Python API simple. If pickling is required, we can
    // add a `__reduce__` that constructs the appropriate Python tuple.
}
