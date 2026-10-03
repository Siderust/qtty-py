//! Python bindings for qtty physical quantities.
//!
//! This crate provides Python bindings for the qtty Rust library, enabling
//! fast, type-safe physical quantity operations in Python with a UnitId-first API

use pyo3::prelude::*;

pub mod bridge;
mod derived;
mod errors;
mod quantity;

use derived::{PyDerivedQuantity, PyDerivedUnit};
pub use qtty_ffi::UnitId;
use quantity::PyQuantity;

/// Canonical constructor used by [`bridge`] through Python's module boundary.
#[pyfunction]
fn _bridge_quantity_from_parts(value: f64, unit_id: u32) -> PyResult<PyQuantity> {
    let unit = UnitId::from_u32(unit_id).ok_or_else(|| {
        pyo3::exceptions::PyValueError::new_err(format!("invalid qtty unit ID: {unit_id}"))
    })?;
    Ok(PyQuantity::from_quantity(value, unit))
}

/// Canonical extractor: this extension owns `PyQuantity`, so extraction is safe.
#[pyfunction]
fn _bridge_quantity_to_parts(quantity: &PyQuantity) -> (f64, u32) {
    (quantity.get_value(), quantity.get_unit() as u32)
}

/// qtty: Fast Physical Units for Python
///
/// This module provides type-safe physical quantities with runtime dimensional
/// analysis, powered by Rust for high performance.
///
/// Example:
/// >>> from qtty import Quantity, Unit
/// >>> m = Quantity(100.0, Unit.Meter)
/// >>> km = m.to(Unit.Kilometer)
/// >>> print(km)
/// 0.1 Kilometer
#[pymodule]
fn _qtty(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyQuantity>()?;
    m.add_class::<PyDerivedUnit>()?;
    m.add_class::<PyDerivedQuantity>()?;
    m.add_class::<UnitId>()?;
    m.add_function(wrap_pyfunction!(_bridge_quantity_from_parts, m)?)?;
    m.add_function(wrap_pyfunction!(_bridge_quantity_to_parts, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
