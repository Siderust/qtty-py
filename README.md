# qtty-py

[![Crates.io](https://img.shields.io/crates/v/qtty.svg)](https://crates.io/crates/qtty)
[![Docs.rs](https://docs.rs/qtty/badge.svg)](https://docs.rs/qtty)
[![CI](https://github.com/Siderust/qtty-py/actions/workflows/ci.yml/badge.svg)](https://github.com/Siderust/qtty-py/actions/workflows/ci.yml)
[![License: AGPL-3.0-only](https://img.shields.io/badge/license-AGPL--3.0--only-blue)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

Fast, type-safe physical quantities for Python, powered by the [qtty](https://github.com/Siderust/qtty) Rust crate through PyO3.

`qtty-py` exposes the Rust unit registry directly through `UnitId`, exported in Python as `Unit`, so unit conversions and dimension checks remain fast and typo-proof.

The Crates.io and docs.rs badges above refer to the underlying `qtty` Rust crate used by these bindings.

## Features

- **Rust-backed quantities** with conversions performed by `qtty`
- **Enum-based units** through `Unit` / `UnitId` instead of string parsing
- **Dimension-safe arithmetic** and conversions between compatible units
- **Derived quantities** such as speed from distance divided by time
- **Pythonic operators** for arithmetic, comparisons, negation, and scalar operations
- **Serialization** with pickle and JSON helpers
- **PyO3 interoperability** for exchanging canonical `qtty.Quantity` objects across independently compiled Rust extensions
- Clear Python exceptions for incompatible dimensions, division by zero, and unsupported operations

## Installation

```bash
pip install qtty
```

## Quick Start

```python
from qtty import Quantity, Unit

distance = Quantity(1000.0, Unit.Meter)
duration = Quantity(2.0, Unit.Minute)

print(distance.to(Unit.Kilometer))
print(distance / duration)
```

The bindings also support concise quantity construction:

```python
from qtty import Unit

distance = 1000.0 * Unit.Meter
duration = 2.0 * Unit.Minute

speed = distance / duration
print(speed)
print(speed.to(Unit.Kilometer, Unit.Hour))
```

## Quantity API

The public module surface is:

```python
from qtty import Quantity, DerivedQuantity, DerivedUnit, Unit, UnitId
```

`Unit` is an alias for `UnitId`.

### Quantity

```python
from qtty import Quantity, Unit

distance = Quantity(1500.0, Unit.Meter)

print(distance.value)
print(distance.unit)
print(distance.to(Unit.Kilometer))
```

Supported operations include:

- `+` and `-` between compatible quantities
- `*` and `/` with scalar values
- `/` with another `Quantity`
- unary `+`, unary `-`, and `abs(...)`
- comparisons between compatible quantities

Dividing quantities with different dimensions produces a `DerivedQuantity`.

### Derived quantities

```python
from qtty import DerivedQuantity, DerivedUnit, Unit

speed = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
print(speed.symbol())
print(speed.to(Unit.Kilometer, Unit.Hour))

unit = DerivedUnit(Unit.Kilometer, Unit.Hour)
print(unit.symbol())
```

Multiplication of two `Quantity` values is currently not implemented in the Python API. Unit lookup is enum-based; string parsing is intentionally not supported.

## Serialization

`Quantity`, `DerivedQuantity`, and `UnitId` support pickle. `Quantity` and `DerivedQuantity` also expose JSON helpers:

```python
from qtty import Quantity, Unit

distance = Quantity(42.0, Unit.Kilometer)

payload = distance.to_json()
restored = Quantity.from_json(payload)
```

## Rust / PyO3 interoperability

`qtty-py` also builds an `rlib` and provides a Rust bridge for independently compiled PyO3 extensions.

The bridge intentionally exchanges primitive values across the extension boundary and asks the installed `qtty` extension to construct or extract its canonical Python classes. This avoids relying on PyO3 class identity across separate shared libraries.

```toml
[dependencies]
pyo3 = { version = "0.29" }
qtty-py = { git = "https://github.com/Siderust/qtty-py.git" }
```

```rust
use pyo3::prelude::*;
use qtty_py::bridge::{to_py_quantity, ToQuantity};
use qtty_py::UnitId;

struct Distance {
    value: f64,
    unit: UnitId,
}

impl ToQuantity for Distance {
    fn value(&self) -> f64 {
        self.value
    }

    fn unit(&self) -> UnitId {
        self.unit
    }
}

#[pyfunction]
fn altitude(py: Python<'_>) -> PyResult<Py<PyAny>> {
    let distance = Distance {
        value: 408.0,
        unit: UnitId::Kilometer,
    };

    to_py_quantity(py, &distance)
}
```

See [Bridge integration](./doc/developers/bridge-integration.md) for the complete interoperability contract and examples.

## Documentation

- [Getting started](./doc/users/getting-started.md)
- [Python API](./doc/users/python-api.md)
- [Bridge integration](./doc/developers/bridge-integration.md)
- [Development](./doc/developers/development.md)
- [Repository layout](./doc/architecture/repository-layout.md)

## Relationship with qtty

`qtty-py` is a thin Python interface over the [qtty](https://github.com/Siderust/qtty) Rust crate. Core unit definitions, conversions, and dimensional logic remain implemented in Rust; the Python layer focuses on idiomatic Python objects, operators, serialization, and interoperability.

- Rust crate: [crates.io/crates/qtty](https://crates.io/crates/qtty)
- Rust API documentation: [docs.rs/qtty](https://docs.rs/qtty)

## Development

Prerequisites:

- Rust toolchain with `cargo`
- Python 3.8+
- Maturin 1.9.4 or newer
- pytest

Local setup:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

python -m pip install --upgrade pip
python -m pip install "maturin>=1.9.4,<2" pytest
maturin develop
```

Common checks:

```bash
pytest -v
cargo test
cargo fmt --check
cargo clippy --all-targets --all-features
```

## License

AGPL-3.0 — see [LICENSE](LICENSE).
