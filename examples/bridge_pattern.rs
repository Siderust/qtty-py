//! # Bridge Pattern Example - DOCUMENTATION ONLY
//!
//! This file demonstrates how to use qtty-py's bridge API in your own Rust project.
//! It cannot be compiled as part of qtty-py itself, but shows you the exact pattern to follow.
//!
//! See BRIDGE_GUIDE.md for complete setup instructions and working examples.
//!
//! ## The Pattern
//!
//! 1. Define your own quantity types in your project
//! 2. Implement `qtty_py::bridge::ToQuantity` on them
//! 3. Use `.to_py_quantity()` in your PyO3 getters
//!
//! ## Code Example
//!
//! In your project's Cargo.toml:
//! ```toml
//! [dependencies]
//! pyo3 = { version = "0.22", features = ["extension-module"] }
//! qtty-py = { path = "../qtty-py" }
//! qtty-ffi = { version = "0.2" }
//! ```
//!
//! In your Rust code:
//! ```ignore
//! use pyo3::prelude::*;
//! use qtty_ffi::UnitId;
//! use qtty_py::bridge::ToQuantity;
//! use qtty_py::PyQuantity;
//!
//! #[derive(Clone)]
//! pub struct CustomDistance {
//!     value: f64,
//!     unit: UnitId,
//! }
//!
//! impl ToQuantity for CustomDistance {
//!     fn value(&self) -> f64 { self.value }
//!     fn unit(&self) -> UnitId { self.unit }
//! }
//!
//! #[pyclass]
//! pub struct Satellite {
//!     name: String,
//!     altitude: CustomDistance,
//! }
//!
//! #[pymethods]
//! impl Satellite {
//!     #[new]
//!     fn new(name: String, altitude_value: f64, altitude_unit: UnitId) -> Self {
//!         Self {
//!             name,
//!             altitude: CustomDistance { value: altitude_value, unit: altitude_unit },
//!         }
//!     }
//!
//!     #[getter]
//!     fn altitude(&self) -> PyQuantity {
//!         self.altitude.to_py_quantity()  // Magic happens here!
//!     }
//! }
//!
//! #[pymodule]
//! fn my_project(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
//!     m.add_class::<Satellite>()?;
//!     Ok(())
//! }
//! ```
//!
//! ## Usage in Python
//!
//! ```python
//! from qtty import Unit
//! from my_project import Satellite
//!
//! sat = Satellite("ISS", 408000, Unit.Meter)
//! altitude = sat.altitude
//!
//! # altitude is now a qtty PyQuantity, so you can:
//! print(f"Altitude: {altitude.value} {altitude.unit}")  # 408000 Meter
//! 
//! altitude_km = altitude.to(Unit.Kilometer)
//! print(f"In km: {altitude_km.value}")  # 408.0
//! 
//! doubled = altitude_km * 2
//! print(f"Doubled: {doubled.value} {doubled.unit}")  # 816.0 Kilometer
//! ```
//!
