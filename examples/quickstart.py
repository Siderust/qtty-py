#!/usr/bin/env python3
"""Quick start example for qtty-py (Unit enum API)."""

from qtty import DerivedQuantity, Quantity, Unit

print("=== qtty-py Quick Start ===\n")

# 1. Creating quantities — two equivalent forms
print("1) Creating quantities:")
distance = 1000.0 * Unit.Meter          # arithmetic expression syntax
time     = Quantity(9.58, Unit.Second)   # explicit constructor
print(f"   distance = {distance}")
print(f"   time     = {time}")
print(f"   (9.58 * Unit.Second == Quantity(9.58, Unit.Second): "
      f"{9.58 * Unit.Second == Quantity(9.58, Unit.Second)})\n")

# 2. Converting units
print("2) Converting units:")
distance_km = distance.to(Unit.Kilometer)
print(f"   {distance} = {distance_km}\n")

# 3. Arithmetic (dimension checked)
print("3) Arithmetic:")
a = 50.0 * Unit.Meter
b = 30.0 * Unit.Meter
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
meters     = 1.0 * Unit.Meter
kilometers = 1.0 * Unit.Kilometer
print(f"   {meters} + {kilometers} = {meters + kilometers}\n")

# 6. Comparisons
print("6) Comparisons:")
small = 5.0  * Unit.Meter
large = 10.0 * Unit.Meter
print(f"   {small} < {large}: {small < large}")
print(f"   {large} > {small}: {large > small}")
print(f"   {small} == {small}: {small == small}\n")

# 7. Astronomical units
print("7) Astronomical units:")
au = 1.0 * Unit.AstronomicalUnit
ly = 1.0 * Unit.LightYear
print(f"   1 AU = {au.to(Unit.Meter).value:.2e} meters")
print(f"   1 light-year = {ly.to(Unit.Meter).value:.2e} meters\n")

# 8. Angle conversions
print("8) Angle conversions:")
degrees = 180.0 * Unit.Degree
radians = degrees.to(Unit.Radian)
print(f"   180° = {radians.value:.6f} radians\n")

# 9. JSON serialization
print("9) JSON serialization:")
q = 42.195 * Unit.Kilometer
j = q.to_json()
q2 = Quantity.from_json(j)
print(f"   to_json:   {j}")
print(f"   from_json: {q2} (equal: {q == q2})\n")

# 10. Type-safe units (no strings)
print("10) Type-safe units:")
print(f"   Unit.Meter: {Unit.Meter}")
print(f"   Unit.Kilometer: {Unit.Kilometer}")
print("   IDE autocomplete covers all units. Typos are impossible.\n")

# 11. Error handling
print("11) Dimension checking:")
try:
    _ = 10.0 * Unit.Meter + 5.0 * Unit.Second
except TypeError as exc:
    print(f"   ✓ Caught error: {exc}\n")

print("=== Quick Start Complete ===")
