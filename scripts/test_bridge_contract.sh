#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${BRIDGE_VENV_DIR:-$ROOT_DIR/.venv-bridge}"

if ! "$PYTHON_BIN" -m venv "$VENV_DIR"; then
  if ! command -v uv >/dev/null 2>&1; then
    echo "Python venv support is unavailable and uv is not installed" >&2
    exit 1
  fi
  rm -rf "$VENV_DIR"
  uv venv --seed --python "$PYTHON_BIN" "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install pytest maturin
python -m pip install --force-reinstall "$ROOT_DIR"
python -m pip install --force-reinstall "$ROOT_DIR/tests/fixtures/bridge_consumer"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
cd "$tmp_dir"
python -m pytest --rootdir "$ROOT_DIR" "$ROOT_DIR/tests/test_bridge_contract.py"
