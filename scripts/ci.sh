#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
PACKAGE_NAME="qtty"

cd "$ROOT_DIR"

"$PYTHON_BIN" -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install ruff pytest pytest-cov
python -m pip install .
python -m pip install ./tests/fixtures/bridge_consumer

cargo fmt --all -- --check
cargo fmt --manifest-path tests/fixtures/bridge_consumer/Cargo.toml -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets --all-features

python -m ruff format --check python tests examples scripts
python -m ruff check python tests examples scripts

run_pytest() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  (
    cd "$tmp_dir"
    python -m pytest --rootdir "$ROOT_DIR" "$ROOT_DIR/tests" "$@"
  )
  rm -rf "$tmp_dir"
}

rm -f coverage.xml
rm -rf htmlcov

run_pytest
run_pytest \
  --cov="$PACKAGE_NAME" \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=xml:"$ROOT_DIR/coverage.xml" \
  --cov-report=html:"$ROOT_DIR/htmlcov"
