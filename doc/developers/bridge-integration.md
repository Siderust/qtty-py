# Bridge Integration

Use the `qtty-py` bridge when another Rust crate already has its own quantity wrapper and you want to expose it to Python as a `qtty.Quantity`.

## Public bridge api

The bridge module exports:

- `qtty_py::bridge::ToQuantity`
- `qtty_py::bridge::PyQuantity`
- `qtty_py::bridge::to_py_quantity`

## Minimal example

```rust
use pyo3::prelude::*;
use qtty_ffi::UnitId;
use qtty_py::bridge::{PyQuantity, ToQuantity};

pub struct Distance {
    value: f64,
    unit: UnitId,
}

impl ToQuantity for Distance {
    fn value(&self) -> f64 { self.value }
    fn unit(&self) -> UnitId { self.unit }
}

#[pyclass]
pub struct Satellite {
    altitude: Distance,
}

#[pymethods]
impl Satellite {
    #[getter]
    fn altitude(&self) -> PyQuantity {
        self.altitude.to_py_quantity()
    }
}
```

## Cargo setup

```toml
[dependencies]
pyo3 = { version = "0.28.2", features = ["extension-module"] }
qtty-py = { path = "../qtty-py" }
qtty-ffi = { path = "../qtty/qtty-ffi" }
```

## Notes

- The public `PyQuantity` re-export lives under `qtty_py::bridge`, not at the crate root.
- The bridge copies `value` and `UnitId` into `PyQuantity`; it is not a borrowed Python view.
- `UnitId` must come from `qtty-ffi`.
