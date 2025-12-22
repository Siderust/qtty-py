#!/usr/bin/env python3
"""Quick start example for qtty-py (Unit enum API)."""

from qtty import DerivedQuantity, Quantity, Unit

print("=== qtty-py Quick Start (Unit enum only) ===\n")

# 1. Creating quantities
print("1) Creating quantities:")
distance = Quantity(1000.0, Unit.Meter)
time = Quantity(9.58, Unit.Second)
print(f"   distance = {distance}")
print(f"   time     = {time}\n")

# 2. Converting units
print("2) Converting units:")
distance_km = distance.to(Unit.Kilometer)
print(f"   {distance} = {distance_km}\n")

# 3. Arithmetic (dimension checked)
print("3) Arithmetic:")
a = Quantity(50.0, Unit.Meter)
b = Quantity(30.0, Unit.Meter)
print(f"   {a} + {b} = {a + b}")
print(f"   {a} - {b} = {a - b}")
print(f"   {a} × 2   = {a * 2.0}")
print(f"   {a} ÷ 2   = {a / 2.0}\n")

# 4. Derived quantities (rates)
print("4) Derived quantities:")
velocity = distance / time  # DerivedQuantity
print(f"   distance / time = {velocity} ({velocity.symbol()})")
velocity_kmh = velocity.to(Unit.Kilometer, Unit.Hour)
print(f"   in km/h: {velocity_kmh}\n")

# 5. Mixed-unit arithmetic
print("5) Mixed-unit arithmetic:")
meters = Quantity(1.0, Unit.Meter)
kilometers = Quantity(1.0, Unit.Kilometer)
print(f"   {meters} + {kilometers} = {meters + kilometers}\n")

# 6. Comparisons
print("6) Comparisons:")
small = Quantity(5.0, Unit.Meter)
large = Quantity(10.0, Unit.Meter)
print(f"   {small} < {large}: {small < large}")
print(f"   {large} > {small}: {large > small}")
print(f"   {small} == {small}: {small == small}\n")

# 7. Astronomical units
print("7) Astronomical units:")
au = Quantity(1.0, Unit.AstronomicalUnit)
meters_in_au = au.to(Unit.Meter)
print(f"   1 AU = {meters_in_au.value:.2e} meters")
ly = Quantity(1.0, Unit.LightYear)
meters_in_ly = ly.to(Unit.Meter)
print(f"   1 light-year = {meters_in_ly.value:.2e} meters\n")

# 8. Angle conversions
print("8) Angle conversions:")
degrees = Quantity(180.0, Unit.Degree)
radians = degrees.to(Unit.Radian)
print(f"   180° = {radians.value:.6f} radians\n")

# 9. Type-safe units (no strings)
print("9) Type-safe units:")
print(f"   Unit.Meter: {Unit.Meter}")
print(f"   Unit.Kilometer: {Unit.Kilometer}")
print("   IDE autocomplete covers all units. Typos are impossible.\n")

# 10. Error handling
print("10) Dimension checking:")
try:
    _ = Quantity(10.0, Unit.Meter) + Quantity(5.0, Unit.Second)
except TypeError as exc:
    print(f"   ✓ Caught error: {exc}\n")

print("=== Quick Start Complete ===")
