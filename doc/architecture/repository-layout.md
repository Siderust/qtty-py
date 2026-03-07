# Repository Layout

This repository contains two layers:

## Python bindings

- `src/`: PyO3 module implementation
- `python/qtty/`: Python package exports
- `tests/`: Python-facing behavior tests
- `examples/`: Python examples

## Vendored Rust workspace

- `qtty/qtty`: facade crate
- `qtty/qtty-core`: core unit system
- `qtty/qtty-derive`: derive macro
- `qtty/qtty-ffi`: FFI layer used by `qtty-py`

## Documentation layout

- `doc/users/`: user-facing guides and API references
- `doc/developers/`: contributor and integration documentation
- `doc/architecture/`: system structure and component boundaries
