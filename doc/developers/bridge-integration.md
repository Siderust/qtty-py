# Bridge Integration

The public Rust bridge lets an independently compiled PyO3 extension exchange quantities with the installed `qtty` package without relying on PyO3 class identity across shared libraries.

## Supported baseline

- qtty/qtty-ffi source tag: `v0.8.6`
- PyO3: `0.29.x`
- qtty-py library outputs: `cdylib` and `rlib`

`qtty 0.8.6` is published on crates.io. `qtty-ffi` stopped being published separately after 0.8.2, so qtty-py pins the immutable qtty repository tag to obtain the matching 0.8.6 FFI API. No Git submodule is required.

## Why the boundary uses primitives

Every PyO3 extension registers its own Python class objects. Compiling `PyQuantity` or the PyO3-enabled `UnitId` into two extensions does not make their Python type identities equal. A downstream extension must therefore never return its locally compiled `PyQuantity` and assume it is the installed `qtty.Quantity`.

The bridge calls private bridge functions in the installed `qtty._qtty` extension. The canonical extension constructs and extracts its own classes, while only an `f64` and the stable `u32` `UnitId` discriminant cross the extension boundary. Raw IDs are validated with `UnitId::from_u32`; unknown IDs raise `ValueError`.

## Cargo setup

```toml
[lib]
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.29", features = ["extension-module"] }
qtty-py = { git = "https://github.com/Siderust/qtty-py.git" }
```

For a checkout next to the consuming crate, replace the Git dependency with `qtty-py = { path = "../qtty-py" }`.

qtty-py enables `pyo3/extension-module` from `pyproject.toml` only for maturin builds. This keeps the `rlib` consumable and lets the final downstream extension select that PyO3 feature without breaking qtty-py's Rust test binaries.

## Copy-pastable example

```rust
use pyo3::prelude::*;
use qtty_py::bridge::{quantity_from_python, to_py_quantity, ToQuantity};
use qtty_py::UnitId;

struct Distance {
    value: f64,
    unit: UnitId,
}

impl ToQuantity for Distance {
    fn value(&self) -> f64 { self.value }
    fn unit(&self) -> UnitId { self.unit }
}

#[pyfunction]
fn altitude(py: Python<'_>) -> PyResult<Py<PyAny>> {
    let distance = Distance { value: 408.0, unit: UnitId::Kilometer };
    to_py_quantity(py, &distance)
}

#[pyfunction]
fn inspect(value: &Bound<'_, PyAny>) -> PyResult<(f64, u32)> {
    let parts = quantity_from_python(value)?;
    Ok((parts.value, parts.unit as u32))
}

#[pymodule]
fn my_extension(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(altitude, m)?)?;
    m.add_function(wrap_pyfunction!(inspect, m)?)?;
    Ok(())
}
```

`altitude()` returns the actual installed `qtty.Quantity`; `type(altitude()) is qtty.Quantity` is true. `inspect()` accepts that canonical object and returns stable primitive parts after extraction by qtty itself.

## Public API

- `QuantityParts`: validated Rust carrier with `value: f64` and `unit: UnitId`
- `quantity_to_python`: construct a canonical quantity from `f64 + UnitId`
- `quantity_to_python_raw`: validate a raw discriminant and construct a canonical quantity
- `quantity_from_python`: extract a canonical quantity into `QuantityParts`
- `ToQuantity` / `to_py_quantity`: ergonomic Rust conversion into the canonical Python type

The old `bridge::PyQuantity` re-export was removed because returning it from another extension was precisely the unsafe integration pattern this contract replaces.
