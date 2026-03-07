# Rust Workspace

This repository vendors the `qtty` Rust workspace under [`qtty/`](../../qtty/).

## Crates

- `qtty`: end-user facade crate
- `qtty-core`: quantity type system and units
- `qtty-derive`: `#[derive(Unit)]` proc macro
- `qtty-ffi`: C and Python facing flat ABI

## Current workspace version

The Rust crates in `qtty/` are on workspace version `0.4.0`.

## When to use which crate

- Use `qtty` for normal Rust application code.
- Use `qtty-core` when you need lower-level primitives or custom unit work.
- Use `qtty-derive` when defining new unit marker types.
- Use `qtty-ffi` when integrating with C, Python bindings, or foreign-language bridges.

## Related documents

- [repository-layout.md](../architecture/repository-layout.md)
- [qtty-ffi.md](../architecture/qtty-ffi.md)
- [development.md](../developers/development.md)
