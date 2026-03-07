# Qtty Ffi

`qtty-ffi` is the stable interoperability layer shared by C consumers and `qtty-py`.

## Responsibilities

- define ABI-stable `UnitId`, `DimensionId`, and quantity structs
- convert between compatible units
- expose generated unit metadata
- provide a flat representation suitable for FFI

## Data source

The unit catalog is driven by `qtty/qtty-ffi/units.csv`.

## Build pipeline

`qtty/qtty-ffi/build.rs`:

- parses `units.csv`
- generates Rust source fragments for unit ids and lookup tables
- updates `include/qtty_ffi.h` through `cbindgen`

## Runtime layers

- `types.rs`: ABI types and generated enum integration
- `registry.rs`: unit metadata lookup and conversion logic
- `ffi.rs`: exported C ABI
- `helpers.rs` / `macros.rs`: Rust-side ergonomic conversions

## Why `qtty-py` depends on it

`qtty-py` uses `qtty-ffi` as the runtime authority for:

- unit identity
- compatibility checks
- conversions
- derived quantity helpers
