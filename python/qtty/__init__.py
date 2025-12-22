"""
qtty: Fast Physical Units for Python

This package provides Python bindings for the qtty Rust library,
enabling fast, type-safe physical quantity operations.
Units are exposed through the Rust `UnitId` enum for typo-proof usage.
"""

# Import from the Rust extension module
from qtty._qtty import Quantity, DerivedQuantity, DerivedUnit, __version__
from qtty._qtty import UnitId as Unit
from qtty._qtty import UnitId  # Also make it available at qtty.UnitId for pickle

__all__ = ["Quantity", "DerivedQuantity", "DerivedUnit", "Unit", "UnitId", "__version__"]
