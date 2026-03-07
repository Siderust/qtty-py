# Getting Started

`qtty-py` exposes Rust-backed physical quantities to Python through three public types:

- `Quantity`
- `DerivedQuantity`
- `Unit` / `UnitId`

## Install

```bash
pip install qtty
```

## Basic usage

```python
from qtty import Quantity, Unit

distance = Quantity(1000.0, Unit.Meter)
duration = Quantity(120.0, Unit.Second)

print(distance.to(Unit.Kilometer))
print(distance / duration)
```

You can also use the arithmetic shorthand already implemented by the bindings:

```python
from qtty import Unit

distance = 1000.0 * Unit.Meter
duration = 2.0 * Unit.Minute
```

## What is supported

- Unit-safe conversion between compatible units.
- Arithmetic on compatible `Quantity` values.
- `DerivedQuantity` creation from division such as `distance / time`.
- Pickle support for `Quantity`, `DerivedQuantity`, and `UnitId`.
- JSON helpers through `to_json()` / `from_json()`.

## Current limits

- Multiplying two `Quantity` values is not implemented in the Python API.
- Unit lookup is enum-based only. String parsing is intentionally not supported.

## Next documents

- [python-api.md](./python-api.md)
- [bridge-integration.md](../developers/bridge-integration.md)
- [python-bindings.md](../architecture/python-bindings.md)
