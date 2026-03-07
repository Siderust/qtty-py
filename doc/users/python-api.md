# Python Api

## Public module surface

```python
from qtty import Quantity, DerivedQuantity, DerivedUnit, Unit, UnitId
```

`Unit` is an alias for `UnitId`.

## Quantity

Construction:

```python
from qtty import Quantity, Unit

q = Quantity(42.0, Unit.Meter)
```

Properties:

- `q.value`
- `q.unit`

Main methods:

- `q.to(unit)`
- `q.to_json()`
- `Quantity.from_json(json_str)`

Supported operators:

- `+`, `-` between compatible quantities
- `*` and `/` with scalars
- `/` with another `Quantity`
- unary `+`, unary `-`, `abs(...)`
- comparisons between compatible quantities

Division behavior:

- compatible dimensions return a `Quantity` ratio in the left operand unit
- different dimensions return a `DerivedQuantity`

## DerivedQuantity

Construction:

```python
from qtty import DerivedQuantity, Unit

speed = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
```

Properties:

- `value`
- `numerator`
- `denominator`

Main methods:

- `symbol()`
- `to(numerator, denominator)`
- `to_json()`
- `DerivedQuantity.from_json(json_str)`

Supported operators:

- `*` and `/` with scalars
- unary `-`

## DerivedUnit

`DerivedUnit` is a lightweight helper for a numerator and denominator pair.

```python
from qtty import DerivedUnit, Unit

unit = DerivedUnit(Unit.Kilometer, Unit.Hour)
print(unit.symbol())
```

## Error model

- incompatible dimensions raise `TypeError`
- division by zero raises `ZeroDivisionError`
- unsupported operators raise `TypeError` or `NotImplementedError`

## Serialization

Pickle works for:

- `Quantity`
- `DerivedQuantity`
- `UnitId`

JSON helpers are provided on `Quantity` and `DerivedQuantity`.
