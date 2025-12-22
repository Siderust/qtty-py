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
use quantity::PyQuantity;
pub use qtty_ffi::UnitId;

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
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
