# Development

## Prerequisites

- Rust toolchain with `cargo`
- Python 3.8+
- `maturin`
- `pytest`

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install maturin pytest
maturin develop
```

## Common commands

```bash
pytest -v
cargo test
cargo fmt
cargo clippy --all-targets --all-features
```

To rebuild the extension after Rust changes:

```bash
maturin develop
```

## Repository layout

- `src/`: PyO3 bindings for `qtty-py`
- `python/qtty/`: Python package shim
- `tests/`: Python integration tests
- `examples/`: runnable Python examples
- `qtty/`: vendored Rust workspace
- `doc/`: centralized project documentation

## Documentation policy

- Long-form docs live under `doc/`.
- Package `README.md` files are kept minimal when required by packaging metadata.
- New docs should use lowercase file names and be placed in one of:
  - `doc/architecture/`
  - `doc/developers/`
  - `doc/users/`
