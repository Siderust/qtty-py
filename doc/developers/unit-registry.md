# Unit Registry

The FFI unit catalog is defined in [`qtty/qtty-ffi/units.csv`](../../qtty/qtty-ffi/units.csv).

## Csv schema

```text
discriminant,dimension,name,symbol,ratio
```

## Rules

- `discriminant` is ABI-stable and must never change after release.
- `dimension` must match a known `DimensionId`.
- `name` becomes the Rust and generated ABI identifier.
- `symbol` is the display symbol.
- `ratio` is the scale relative to the canonical unit for the dimension.

## Build impact

Changes to `units.csv` regenerate:

- the `UnitId` enum
- unit lookup tables
- the runtime conversion registry
- the generated C header

## Canonical units

- Length: meter
- Time: second
- Angle: radian
- Mass: gram
- Power: watt

## Related documents

- [qtty-ffi.md](../architecture/qtty-ffi.md)
- [repository-layout.md](../architecture/repository-layout.md)
