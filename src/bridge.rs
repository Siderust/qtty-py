//! Cross-extension-safe interoperability with the installed `qtty` package.
//!
//! A PyO3 class is local to the extension module which registers it. Two
//! independently compiled extensions therefore cannot exchange their own
//! copies of `PyQuantity` or `UnitId` as though those Python types were
//! identical. This bridge imports the installed `qtty._qtty` module and asks
//! that canonical extension to construct or extract its classes. Only `f64`
//! and the stable `u32` [`UnitId`] discriminant cross the module boundary.
//!
//! # Downstream extension
//!
//! ```ignore
//! use pyo3::prelude::*;
//! use qtty_py::bridge::{quantity_from_python, to_py_quantity, ToQuantity};
//! use qtty_py::UnitId;
//!
//! struct Distance {
//!     value: f64,
//!     unit: UnitId,
//! }
//!
//! impl ToQuantity for Distance {
//!     fn value(&self) -> f64 { self.value }
//!     fn unit(&self) -> UnitId { self.unit }
//! }
//!
//! #[pyfunction]
//! fn distance(py: Python<'_>) -> PyResult<Py<PyAny>> {
//!     to_py_quantity(py, &Distance { value: 12.5, unit: UnitId::Meter })
//! }
//!
//! #[pyfunction]
//! fn inspect(value: &Bound<'_, PyAny>) -> PyResult<(f64, u32)> {
//!     let parts = quantity_from_python(value)?;
//!     Ok((parts.value, parts.unit as u32))
//! }
//! ```

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use qtty_ffi::UnitId;

const EXTENSION_MODULE: &str = "qtty._qtty";
const FROM_PARTS: &str = "_bridge_quantity_from_parts";
const TO_PARTS: &str = "_bridge_quantity_to_parts";

/// Stable Rust representation of a canonical Python `qtty.Quantity`.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct QuantityParts {
    /// Numeric quantity value.
    pub value: f64,
    /// Validated stable unit identifier.
    pub unit: UnitId,
}

/// Construct the actual `qtty.Quantity` class owned by the installed package.
pub fn quantity_to_python(py: Python<'_>, value: f64, unit: UnitId) -> PyResult<Py<PyAny>> {
    quantity_to_python_raw(py, value, unit as u32)
}

/// Construct a canonical quantity from a raw stable unit discriminant.
///
/// This entry point is useful at FFI boundaries which already carry a `u32`.
/// Unknown discriminants produce `ValueError`; they never fall back to a unit.
pub fn quantity_to_python_raw(py: Python<'_>, value: f64, unit_id: u32) -> PyResult<Py<PyAny>> {
    if UnitId::from_u32(unit_id).is_none() {
        return Err(PyValueError::new_err(format!(
            "invalid qtty unit ID: {unit_id}"
        )));
    }

    PyModule::import(py, EXTENSION_MODULE)?
        .getattr(FROM_PARTS)?
        .call1((value, unit_id))
        .map(Bound::unbind)
}

/// Extract primitive parts from the installed package's `qtty.Quantity`.
///
/// Type checking and extraction happen inside the canonical extension which
/// owns the Python class. An object of any other type produces `TypeError`.
pub fn quantity_from_python(value: &Bound<'_, PyAny>) -> PyResult<QuantityParts> {
    let (number, raw_unit): (f64, u32) = PyModule::import(value.py(), EXTENSION_MODULE)?
        .getattr(TO_PARTS)?
        .call1((value,))?
        .extract()?;
    let unit = UnitId::from_u32(raw_unit).ok_or_else(|| {
        PyValueError::new_err(format!(
            "canonical qtty extension returned invalid unit ID: {raw_unit}"
        ))
    })?;
    Ok(QuantityParts {
        value: number,
        unit,
    })
}

/// Trait for Rust values which can become a canonical Python `qtty.Quantity`.
pub trait ToQuantity {
    /// Numeric quantity value.
    fn value(&self) -> f64;

    /// Validated qtty unit.
    fn unit(&self) -> UnitId;

    /// Ask the installed qtty extension to create its own `Quantity` object.
    fn to_py_quantity(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        quantity_to_python(py, self.value(), self.unit())
    }
}

/// Convert a Rust value into the installed package's canonical quantity type.
pub fn to_py_quantity<T: ToQuantity>(py: Python<'_>, quantity: &T) -> PyResult<Py<PyAny>> {
    quantity.to_py_quantity(py)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn quantity_parts_preserve_stable_unit() {
        let parts = QuantityParts {
            value: 42.0,
            unit: UnitId::Meter,
        };
        assert_eq!(parts.value, 42.0);
        assert_eq!(parts.unit, UnitId::Meter);
    }

    #[test]
    fn rejects_invalid_raw_unit_before_importing_python() {
        Python::attach(|py| {
            let error = quantity_to_python_raw(py, 1.0, u32::MAX).unwrap_err();
            assert!(error.is_instance_of::<PyValueError>(py));
        });
    }
}
