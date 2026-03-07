# Python Bindings

`qtty-py` is a thin PyO3 layer over `qtty-ffi`.

## Main modules

- `src/lib.rs`: registers the Python module and exported classes
- `src/quantity.rs`: `Quantity`
- `src/derived.rs`: `DerivedQuantity` and `DerivedUnit`
- `src/bridge.rs`: Rust-to-Python bridge helpers
- `src/errors.rs`: Python exception mapping

## Binding model

- Units are exposed directly as the Rust `UnitId` enum.
- `Quantity` wraps `qtty_ffi::QttyQuantity`.
- `DerivedQuantity` wraps `qtty_ffi::QttyDerivedQuantity` data at the API boundary.
- Dimension checks and conversions delegate to `qtty-ffi`.

## Public Python surface

- `qtty.Quantity`
- `qtty.DerivedQuantity`
- `qtty.DerivedUnit`
- `qtty.Unit`
- `qtty.UnitId`

## Design choices

- No string-based unit parsing.
- Errors are raised as Python exceptions instead of raw status codes.
- Pickle support is implemented at the Python object level.
