# Qtty Ffi

`qtty-ffi` is the stable interoperability layer shared by C consumers and `qtty-py`.

## Responsibilities

- define ABI-stable `UnitId`, `DimensionId`, and quantity structs
- convert between compatible units
- expose generated unit metadata
- provide a flat representation suitable for FFI

## Dependency source

qtty-py uses `qtty-ffi` from the qtty repository's immutable `v0.8.6` tag. Although `qtty` 0.8.6 is on crates.io, the separately published `qtty-ffi` line ends at 0.8.2.

## Build pipeline

Upstream `qtty-ffi/build.rs`:

- parses the stable discriminant catalog and qtty unit definitions
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
