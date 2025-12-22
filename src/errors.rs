//! Error handling utilities for Python bindings.

use pyo3::exceptions::*;
use pyo3::prelude::*;
use qtty_ffi::UnitId;

/// Creates a dimension incompatibility error with detailed message.
pub fn map_dimension_error(unit_a: UnitId, unit_b: UnitId) -> PyErr {
    PyTypeError::new_err(format!(
        "Cannot operate on {:?} and {:?} (incompatible dimensions)",
        unit_a, unit_b
    ))
}
