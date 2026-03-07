//! Bridge module for converting Rust quantities to Python PyQuantity objects.
//!
//! This module provides utilities for seamlessly converting between Rust quantity types
//! and Python-compatible PyQuantity objects, allowing external Rust projects to use
//! qtty-py as a bridge to Python.
//!
//! # Example Usage
//!
//! In your `Cargo.toml`:
//! ```toml
//! qtty-py = { path = "../qtty-py" }
//! pyo3 = { version = "0.28.2", features = ["extension-module"] }
//! qtty-ffi = { path = "../qtty/qtty-ffi" }
//! ```
//!
//! In your Rust code:
//! ```ignore
//! use pyo3::prelude::*;
//! use qtty_ffi::UnitId;
//! use qtty_py::bridge::{PyQuantity, ToQuantity};
//!
//! #[pyclass]
//! pub struct MyObject {
//!     distance: Distance,
//! }
//!
//! pub struct Distance {
//!     value: f64,
//!     unit: UnitId,
//! }
//!
//! impl ToQuantity for Distance {
//!     fn value(&self) -> f64 { self.value }
//!     fn unit(&self) -> UnitId { self.unit }
//! }
//!
//! #[pymethods]
//! impl MyObject {
//!     #[getter]
//!     fn distance(&self) -> PyQuantity {
//!         self.distance.to_py_quantity()
//!     }
//! }
//! ```

use qtty_ffi::UnitId;

pub use crate::quantity::PyQuantity;

/// Trait for types that can be converted to PyQuantity.
///
/// Implement this trait on your Rust quantity types to expose them through PyO3
/// getters as `qtty.Quantity` instances.
pub trait ToQuantity {
    /// Get the numeric value of this quantity
    fn value(&self) -> f64;

    /// Get the unit of this quantity
    fn unit(&self) -> UnitId;

    /// Convert this quantity to a standalone `PyQuantity`.
    fn to_py_quantity(&self) -> PyQuantity {
        PyQuantity::from_quantity(self.value(), self.unit())
    }
}

/// Helper function to convert any type implementing [`ToQuantity`] into [`PyQuantity`].
pub fn to_py_quantity<T: ToQuantity>(quantity: &T) -> PyQuantity {
    quantity.to_py_quantity()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trait_conversion() {
        struct TestQuantity {
            val: f64,
            u: UnitId,
        }

        impl ToQuantity for TestQuantity {
            fn value(&self) -> f64 {
                self.val
            }
            fn unit(&self) -> UnitId {
                self.u
            }
        }

        let q = TestQuantity {
            val: 42.0,
            u: UnitId::Meter,
        };
        let py_q = q.to_py_quantity();
        assert_eq!(py_q.get_value(), 42.0);
        assert_eq!(py_q.get_unit(), UnitId::Meter);
    }
}
