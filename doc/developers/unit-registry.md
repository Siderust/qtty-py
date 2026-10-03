# Unit Registry

The FFI unit catalog belongs to the upstream qtty 0.8.6 source. qtty-py consumes it through `qtty-ffi`; it does not keep a local duplicate.

## Csv schema

```text
discriminant,ffi_name
```

## Rules

- `discriminant` is ABI-stable and must never change after release.
- `ffi_name` maps the stable value to the upstream qtty unit type.
- Dimensions, symbols, and conversion ratios come from qtty's unit definitions.

## Build impact

Upstream catalog changes regenerate:

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
