# Repository Layout

This repository contains the Python binding layer and its tests:

## Python bindings

- `src/`: PyO3 module implementation
- `python/qtty/`: Python package exports
- `tests/`: Python-facing behavior tests
- `tests/fixtures/bridge_consumer/`: independently compiled bridge consumer
- `examples/`: Python examples

The Rust dependency baseline comes from the pinned qtty `v0.8.6` Git tag because the matching `qtty-ffi` crate is not published separately.

## Documentation layout

- `doc/users/`: user-facing guides and API references
- `doc/developers/`: contributor and integration documentation
- `doc/architecture/`: system structure and component boundaries
