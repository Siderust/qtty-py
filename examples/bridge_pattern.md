# Bridge Pattern Example

This document reproduces the documentation-only example from `examples/bridge_pattern.rs`.
It demonstrates how to expose your project-specific quantity types to Python using the `qtty-py` bridge API.

> Note: this is documentation and an integration pattern — it's not compiled as part of `qtty-py`.

## The Pattern

1. Define your own quantity types in your project.
2. Implement `qtty_py::bridge::ToQuantity` on them.
3. Use `.to_py_quantity()` in your PyO3 getters to return a `PyQuantity` to Python.

## Cargo.toml (dependencies)

```toml
[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
qtty-py = { path = "../qtty-py" }
qtty-ffi = { version = "0.2" }
```

## Rust integration example

```rust
use pyo3::prelude::*;
use qtty_ffi::UnitId;
use qtty_py::bridge::ToQuantity;
use qtty_py::PyQuantity;

#[derive(Clone)]
pub struct CustomDistance {
    value: f64,
    unit: UnitId,
}

impl ToQuantity for CustomDistance {
    fn value(&self) -> f64 { self.value }
    fn unit(&self) -> UnitId { self.unit }
}

#[pyclass]
pub struct Satellite {
    name: String,
    altitude: CustomDistance,
}

#[pymethods]
impl Satellite {
    #[new]
    fn new(name: String, altitude_value: f64, altitude_unit: UnitId) -> Self {
        Self {
            name,
            altitude: CustomDistance { value: altitude_value, unit: altitude_unit },
        }
    }

    #[getter]
    fn altitude(&self) -> PyQuantity {
        self.altitude.to_py_quantity()  // returns a qtty PyQuantity for Python
    }
}

#[pymodule]
fn my_project(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Satellite>()?;
    Ok(())
}
```

## Usage from Python

```python
from qtty import Unit
from my_project import Satellite

sat = Satellite("ISS", 408000, Unit.Meter)
altitude = sat.altitude

# `altitude` is a qtty PyQuantity in Python
print(f"Altitude: {altitude.value} {altitude.unit}")  # 408000 Meter

altitude_km = altitude.to(Unit.Kilometer)
print(f"In km: {altitude_km.value}")  # 408.0

doubled = altitude_km * 2
print(f"Doubled: {doubled.value} {doubled.unit}")  # 816.0 Kilometer
```

## See also

- BRIDGE_GUIDE.md — additional setup and integration notes.
- BRIDGE_QUICK_REFERENCE.md — quick reference for the bridge API.

---

This file was generated from `examples/bridge_pattern.rs` to provide a Markdown reference for documentation or README inclusion.
