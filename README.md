# qtty-py

Rust-backed physical quantities for Python.

`qtty-py` exposes the `qtty-ffi` unit registry directly through `UnitId`, exported in Python as `Unit`, so conversions and dimension checks stay fast and typo-proof.

## Quick start

```bash
pip install qtty
```

```python
from qtty import Quantity, Unit

distance = Quantity(1000.0, Unit.Meter)
duration = Quantity(120.0, Unit.Second)

print(distance.to(Unit.Kilometer))
print(distance / duration)
```

## Documentation

- [Getting started](./doc/users/getting-started.md)
- [Python API](./doc/users/python-api.md)
- [Bridge integration](./doc/developers/bridge-integration.md)
- [Development](./doc/developers/development.md)
- [Repository layout](./doc/architecture/repository-layout.md)
