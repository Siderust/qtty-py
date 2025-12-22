# qtty-py: Fast Physical Units for Python

[![PyPI](https://img.shields.io/pypi/v/qtty.svg)](https://pypi.org/project/qtty/)
[![Python Version](https://img.shields.io/pypi/pyversions/qtty.svg)](https://pypi.org/project/qtty/)
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](https://github.com/Siderust/qtty/blob/main/LICENSE)

Python bindings for the [qtty](https://github.com/Siderust/qtty) Rust library. qtty-py exposes the Rust `UnitId` enum directly—no string parsing—so IDEs can autocomplete every unit while Rust keeps conversions fast and dimension-safe.

## Highlights

- Type-safe `Unit` enum with 150+ units (length, time, mass, angle, power, astronomy)
- Derived quantities for rates (e.g., m/s, km/h) with conversions between compatible pairs
- Runtime dimension checks on arithmetic and comparisons
- Pickle support for both `Quantity` and `DerivedQuantity`
- Rust-powered performance via `qtty-ffi`
- Friendly, Pythonic API without losing type information

## Installation

```bash
pip install qtty
```

## Usage

### Quantities (Unit enum only)

```python
from qtty import Quantity, Unit

distance = Quantity(1000.0, Unit.Meter)
time = Quantity(9.58, Unit.Second)

print(distance.to(Unit.Kilometer))  # 1.0 Kilometer
print(distance + Quantity(1.0, Unit.Kilometer))  # 2000 Meter
```

### Derived quantities and conversions

```python
from qtty import Quantity, DerivedQuantity, Unit

distance = Quantity(150.0, Unit.Kilometer)
duration = Quantity(2.0, Unit.Hour)

velocity = distance / duration          # DerivedQuantity(75, Kilometer, Hour)
print(velocity.symbol())                # "km/h"
print(velocity.to(Unit.Meter, Unit.Second))  # 20.833333 m/s
```

### Dimension safety

```python
from qtty import Quantity, Unit

meters = Quantity(10.0, Unit.Meter)
seconds = Quantity(5.0, Unit.Second)

try:
    meters + seconds
except TypeError as exc:
    print(f"Protected from mistakes: {exc}")
```

### Pickle support

```python
import pickle
from qtty import Quantity, DerivedQuantity, Unit

q = Quantity(42.0, Unit.Kilogram)
restored = pickle.loads(pickle.dumps(q))
assert restored.value == q.value and restored.unit == q.unit

v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
assert pickle.loads(pickle.dumps(v)).symbol() == "m/s"
```

## Notes and limitations

- Units are provided by the `Unit` enum; string-based parsing has been removed for a typo-proof API.
- Multiplying two `Quantity` values is not implemented yet; divide to create `DerivedQuantity` for rates.
- Expression parsing and numpy/pandas integrations are planned but not yet available.
- The full unit catalog matches [`qtty-ffi`'s registry](https://github.com/Siderust/qtty/blob/main/qtty-ffi/units.csv).

## Development

### Prerequisites

- Rust 1.70+ with `cargo`
- Python 3.8+
- `maturin` for building wheels
- `pytest` for the Python test suite

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install maturin pytest
maturin develop  # builds and installs the extension into the venv
```

### Workflow

```bash
# Rebuild after Rust changes
maturin develop

# Run Python tests
pytest -v

# Run Rust tests
cargo test
```

Optional checks:

```bash
cargo fmt && cargo clippy
pip install black
black tests/
```

### Project structure

```
src/
  lib.rs          # PyO3 module definition and exports
  quantity.rs     # Quantity implementation (UnitId-first)
  derived.rs      # DerivedQuantity and DerivedUnit helpers
  errors.rs       # Python error helpers
python/qtty/__init__.py  # Python-facing imports
examples/quickstart.py   # Minimal walkthrough
examples/derived_demo.py # Derived units, pickle demo
tests/                   # Python tests exercising the public API
```

### Publishing (maintainers)

```bash
maturin build --release
maturin publish
```

### Troubleshooting

- Import errors after code changes: rebuild with `maturin develop`.
- Dimension mismatches: use the `Unit` enum; strings are intentionally rejected.
- Stale artifacts: `cargo clean` and remove `target/` or recreate your virtualenv.

## License

AGPL-3.0 (same as the parent `qtty` crate). See [LICENSE](https://github.com/Siderust/qtty/blob/main/LICENSE).
