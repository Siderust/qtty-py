#!/usr/bin/env python3
"""Advanced demo for qtty-py (derived units, conversions, pickle)."""

import pickle

from qtty import DerivedQuantity, DerivedUnit, Quantity, Unit


def demo_derived_units():
    print("=== Derived units ===")
    distance = Quantity(150.0, Unit.Kilometer)
    time = Quantity(2.0, Unit.Hour)

    velocity = distance / time
    print(f"distance: {distance}")
    print(f"time:     {time}")
    print(f"velocity: {velocity} ({velocity.symbol()})")

    velocity_ms = velocity.to(Unit.Meter, Unit.Second)
    print(f"velocity in m/s: {velocity_ms}\n")


def demo_explicit_creation():
    print("=== Explicit construction ===")
    speed = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
    print(f"DerivedQuantity(...): {speed}")

    unit = DerivedUnit(Unit.Kilometer, Unit.Hour)
    converted = speed.to(unit.numerator, unit.denominator)
    print(f"Using DerivedUnit helper ({unit}): {converted}\n")


def demo_pickle_support():
    print("=== Pickle support ===")
    q = Quantity(42.0, Unit.Kilogram)
    restored_q = pickle.loads(pickle.dumps(q))
    print(f"Quantity round-trip: {restored_q} (unit: {restored_q.unit})")

    v = DerivedQuantity(25.0, Unit.Meter, Unit.Second)
    restored_v = pickle.loads(pickle.dumps(v))
    print(f"DerivedQuantity round-trip: {restored_v} ({restored_v.symbol()})\n")


def demo_dimension_protection():
    print("=== Dimension protection ===")
    try:
        Quantity(1.0, Unit.Meter) + Quantity(1.0, Unit.Second)
    except TypeError as exc:
        print(f"Caught expected error: {exc}\n")


if __name__ == "__main__":
    demo_derived_units()
    demo_explicit_creation()
    demo_pickle_support()
    demo_dimension_protection()
    print("All demos completed.")
