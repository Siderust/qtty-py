#!/usr/bin/env python3
"""Comprehensive qtty-py examples: all units, features, and idioms.

This file demonstrates every dimension, the arithmetic-expression syntax,
serde (JSON), derived quantities, pickle, comparisons, and error handling.
"""

from qtty import Quantity, DerivedQuantity, DerivedUnit, Unit

# ─── 1. Arithmetic-expression syntax ────────────────────────────────────────
#
# Instead of Quantity(value, Unit.X), multiply a scalar by a unit:
#   9.58 * Unit.Second   ⟺   Quantity(9.58, Unit.Second)
#
# Both forms produce the same Quantity object.

print("═══ 1. Arithmetic-expression syntax ═══\n")

# These two are exactly equivalent:
q1 = Quantity(9.58, Unit.Second)
q2 = 9.58 * Unit.Second
print(f"  Quantity(9.58, Unit.Second) → {q1}")
print(f"  9.58 * Unit.Second         → {q2}")
print(f"  Equal? {q1 == q2}")

# Unit * scalar also works:
q3 = Unit.Meter * 100.0
print(f"  Unit.Meter * 100.0         → {q3}")

# Use it in expressions:
distance = 100.0 * Unit.Meter
time     = 9.58 * Unit.Second
velocity = distance / time
print(f"\n  Usain Bolt's 100 m dash:")
print(f"    distance = {distance}")
print(f"    time     = {time}")
print(f"    velocity = {velocity} ({velocity.symbol()})")
print(f"    in km/h  = {velocity.to(Unit.Kilometer, Unit.Hour)}")
print()


# ─── 2. Length units ────────────────────────────────────────────────────────

print("═══ 2. Length units ═══\n")

print("  SI prefixes:")
nm  = 1.0 * Unit.Nanometer
um  = 1.0 * Unit.Micrometer
mm  = 1.0 * Unit.Millimeter
cm  = 1.0 * Unit.Centimeter
m   = 1.0 * Unit.Meter
km  = 1.0 * Unit.Kilometer
print(f"    1 nm  = {nm.to(Unit.Meter).value:.0e} m")
print(f"    1 µm  = {um.to(Unit.Meter).value:.0e} m")
print(f"    1 mm  = {mm.to(Unit.Meter).value} m")
print(f"    1 cm  = {cm.to(Unit.Meter).value} m")
print(f"    1 km  = {km.to(Unit.Meter).value} m")

print("\n  Imperial:")
inch = 1.0 * Unit.Inch
foot = 1.0 * Unit.Foot
yard = 1.0 * Unit.Yard
mile = 1.0 * Unit.Mile
print(f"    1 inch = {inch.to(Unit.Meter).value} m")
print(f"    1 foot = {foot.to(Unit.Meter).value} m")
print(f"    1 yard = {yard.to(Unit.Meter).value} m")
print(f"    1 mile = {mile.to(Unit.Meter).value} m")

print("\n  Nautical:")
nmi = 1.0 * Unit.NauticalMile
print(f"    1 nmi  = {nmi.to(Unit.Meter).value} m")

print("\n  Astronomical:")
au  = 1.0 * Unit.AstronomicalUnit
ly  = 1.0 * Unit.LightYear
pc  = 1.0 * Unit.Parsec
kpc = 1.0 * Unit.Kiloparsec
mpc = 1.0 * Unit.Megaparsec
print(f"    1 AU        = {au.to(Unit.Meter).value:.4e} m")
print(f"    1 light-year= {ly.to(Unit.Meter).value:.4e} m")
print(f"    1 parsec    = {pc.to(Unit.LightYear).value:.4f} ly")
print(f"    1 kpc       = {kpc.to(Unit.Parsec).value:.0f} pc")
print(f"    1 Mpc       = {mpc.to(Unit.Kiloparsec).value:.0f} kpc")

print("\n  Solar/planetary:")
r_earth = 1.0 * Unit.NominalEarthRadius
r_sun   = 1.0 * Unit.NominalSolarRadius
r_jup   = 1.0 * Unit.NominalJupiterRadius
print(f"    Earth radius   = {r_earth.to(Unit.Kilometer).value:.1f} km")
print(f"    Jupiter radius = {r_jup.to(Unit.Kilometer).value:.1f} km")
print(f"    Solar radius   = {r_sun.to(Unit.Kilometer).value:.1f} km")
print()


# ─── 3. Time units ─────────────────────────────────────────────────────────

print("═══ 3. Time units ═══\n")

print("  SI prefixes:")
ns  = 1.0 * Unit.Nanosecond
us  = 1.0 * Unit.Microsecond
ms  = 1.0 * Unit.Millisecond
s   = 1.0 * Unit.Second
print(f"    1 ns  = {ns.to(Unit.Second).value:.0e} s")
print(f"    1 µs  = {us.to(Unit.Second).value:.0e} s")
print(f"    1 ms  = {ms.to(Unit.Second).value} s")

print("\n  Common:")
minute = 1.0 * Unit.Minute
hour   = 1.0 * Unit.Hour
day    = 1.0 * Unit.Day
week   = 1.0 * Unit.Week
print(f"    1 min  = {minute.to(Unit.Second).value:.0f} s")
print(f"    1 hour = {hour.to(Unit.Minute).value:.0f} min")
print(f"    1 day  = {day.to(Unit.Hour).value:.0f} h")
print(f"    1 week = {week.to(Unit.Day).value:.0f} d")

print("\n  Calendar & astronomical:")
yr     = 1.0 * Unit.Year
jy     = 1.0 * Unit.JulianYear
jc     = 1.0 * Unit.JulianCentury
sday   = 1.0 * Unit.SiderealDay
print(f"    1 year             = {yr.to(Unit.Day).value:.2f} d")
print(f"    1 Julian year      = {jy.to(Unit.Day).value:.2f} d")
print(f"    1 Julian century   = {jc.to(Unit.Year).value:.0f} yr")
print(f"    1 sidereal day     = {sday.to(Unit.Hour).value:.6f} h")
print()


# ─── 4. Angle units ────────────────────────────────────────────────────────

print("═══ 4. Angle units ═══\n")

import math

deg  = 180.0 * Unit.Degree
rad  = deg.to(Unit.Radian)
grad = deg.to(Unit.Gradian)
turn = 1.0 * Unit.Turn
print(f"  180° = {rad.value:.6f} rad (π = {math.pi:.6f})")
print(f"  180° = {grad.value:.1f} gradians")
print(f"  1 turn = {turn.to(Unit.Degree).value:.0f}°")

print("\n  Astronomical:")
arcsec = 1.0 * Unit.Arcsecond
arcmin = 1.0 * Unit.Arcminute
mas    = 1.0 * Unit.MilliArcsecond
ha     = 1.0 * Unit.HourAngle
print(f"    1 arcsec        = {arcsec.to(Unit.Degree).value:.6f}°")
print(f"    1 arcmin        = {arcmin.to(Unit.Arcsecond).value:.0f} arcsec")
print(f"    1 HourAngle     = {ha.to(Unit.Degree).value:.1f}°")
print(f"    1 mas           = {mas.to(Unit.Arcsecond).value:.3f} arcsec")
print()


# ─── 5. Mass units ─────────────────────────────────────────────────────────

print("═══ 5. Mass units ═══\n")

print("  SI prefixes:")
mg  = 1.0 * Unit.Milligram
g   = 1.0 * Unit.Gram
kg  = 1.0 * Unit.Kilogram
t   = 1.0 * Unit.Tonne
print(f"    1 mg = {mg.to(Unit.Gram).value} g")
print(f"    1 kg = {kg.to(Unit.Gram).value:.0f} g")
print(f"    1 t  = {t.to(Unit.Kilogram).value:.0f} kg")

print("\n  Imperial:")
oz  = 1.0 * Unit.Ounce
lb  = 1.0 * Unit.Pound
st  = 1.0 * Unit.Stone
print(f"    1 oz    = {oz.to(Unit.Gram).value:.4f} g")
print(f"    1 lb    = {lb.to(Unit.Gram).value:.5f} g")
print(f"    1 stone = {st.to(Unit.Kilogram).value:.5f} kg")

print("\n  Special:")
ct  = 1.0 * Unit.Carat
amu = 1.0 * Unit.AtomicMassUnit
m_sun = 1.0 * Unit.SolarMass
print(f"    1 carat      = {ct.to(Unit.Gram).value} g")
print(f"    1 AMU        = {amu.to(Unit.Gram).value:.6e} g")
print(f"    1 solar mass = {m_sun.to(Unit.Kilogram).value:.4e} kg")
print()


# ─── 6. Power units ────────────────────────────────────────────────────────

print("═══ 6. Power units ═══\n")

mW  = 1.0 * Unit.Milliwatt
W   = 1.0 * Unit.Watt
kW  = 1.0 * Unit.Kilowatt
MW  = 1.0 * Unit.Megawatt
GW  = 1.0 * Unit.Gigawatt
hp  = 1.0 * Unit.HorsepowerMetric
L_sun = 1.0 * Unit.SolarLuminosity
print(f"  1 mW  = {mW.to(Unit.Watt).value} W")
print(f"  1 kW  = {kW.to(Unit.Watt).value:.0f} W")
print(f"  1 MW  = {MW.to(Unit.Kilowatt).value:.0f} kW")
print(f"  1 GW  = {GW.to(Unit.Megawatt).value:.0f} MW")
print(f"  1 HP (metric) = {hp.to(Unit.Watt).value:.5f} W")
print(f"  Solar luminosity = {L_sun.to(Unit.Watt).value:.3e} W")
print()


# ─── 7. Derived quantities (rates) ─────────────────────────────────────────

print("═══ 7. Derived quantities (rates) ═══\n")

# Create from division
dist  = 150.0 * Unit.Kilometer
dur   = 2.0 * Unit.Hour
speed = dist / dur
print(f"  {dist} / {dur} = {speed} ({speed.symbol()})")

# Convert between derived units
speed_ms = speed.to(Unit.Meter, Unit.Second)
print(f"  in m/s: {speed_ms}")

# Explicit construction
angular_velocity = DerivedQuantity(2 * math.pi, Unit.Radian, Unit.Second)
print(f"  Angular velocity: {angular_velocity} ({angular_velocity.symbol()})")
print(f"    in °/s: {angular_velocity.to(Unit.Degree, Unit.Second)}")

# DerivedUnit helper
mps = DerivedUnit(Unit.Meter, Unit.Second)
kmh = DerivedUnit(Unit.Kilometer, Unit.Hour)
print(f"  DerivedUnit helpers: {mps}, {kmh}")

# Scalar operations on derived
doubled = speed * 2.0
halved  = speed / 2.0
negated = -speed
print(f"  {speed} × 2   = {doubled}")
print(f"  {speed} ÷ 2   = {halved}")
print(f"  -{speed} = {negated}")
print()


# ─── 8. Arithmetic ─────────────────────────────────────────────────────────

print("═══ 8. Arithmetic ═══\n")

a = 50.0 * Unit.Meter
b = 30.0 * Unit.Meter
print(f"  {a} + {b}       = {a + b}")
print(f"  {a} - {b}       = {a - b}")
print(f"  {a} × 3         = {a * 3}")
print(f"  3 × {a}         = {3 * a}")
print(f"  {a} ÷ 2         = {a / 2.0}")
print(f"  -{a}            = {-a}")
print(f"  abs({-a})     = {abs(-a)}")

# Mixed-unit addition
m1 = 1.5 * Unit.Kilometer
m2 = 500.0 * Unit.Meter
print(f"\n  {m1} + {m2} = {m1 + m2}  (result in left operand's unit)")

# Division: same dimension → ratio
ratio = (100.0 * Unit.Meter) / (50.0 * Unit.Meter)
print(f"  100 m / 50 m = {ratio}  (same-dimension ratio)")

# Division: cross-dimension → DerivedQuantity
derived = (100.0 * Unit.Meter) / (10.0 * Unit.Second)
print(f"  100 m / 10 s = {derived} ({derived.symbol()})  (cross-dimension)")
print()


# ─── 9. Comparisons ────────────────────────────────────────────────────────

print("═══ 9. Comparisons ═══\n")

x = 1.0 * Unit.Kilometer
y = 999.0 * Unit.Meter
print(f"  {x} == {y}     : {x == y}")
print(f"  {x} > {y}      : {x > y}")
print(f"  {x} >= 1000 m  : {x >= 1000.0 * Unit.Meter}")
print(f"  1 km == 1000 m : {x == 1000.0 * Unit.Meter}")
print()


# ─── 10. JSON serialization ────────────────────────────────────────────────

print("═══ 10. JSON serialization (serde) ═══\n")

import json

# Quantity serde
q = 42.195 * Unit.Kilometer
j = q.to_json()
print(f"  to_json:   {j}")
print(f"  (parsed):  {json.loads(j)}")

q_back = Quantity.from_json(j)
print(f"  from_json: {q_back} (eq: {q == q_back})")

# DerivedQuantity serde
v = DerivedQuantity(343.0, Unit.Meter, Unit.Second)  # speed of sound
j2 = v.to_json()
print(f"\n  derived to_json:   {j2}")
v_back = DerivedQuantity.from_json(j2)
print(f"  derived from_json: {v_back} ({v_back.symbol()})")

# JSON interop: construct from external JSON
external = '{"value": 299792458.0, "unit": "Meter"}'
c = Quantity.from_json(external)
print(f"\n  From external JSON: {c}")
print(f"    Speed of light = {c.to(Unit.Kilometer).value:.0f} km")
print()


# ─── 11. Pickle ─────────────────────────────────────────────────────────────

print("═══ 11. Pickle support ═══\n")

import pickle

# Quantity
q = 1.0 * Unit.AstronomicalUnit
data = pickle.dumps(q)
q2 = pickle.loads(data)
print(f"  pickle roundtrip: {q} → bytes → {q2}")
print(f"    equal: {q == q2}")

# DerivedQuantity
v = DerivedQuantity(60.0, Unit.Kilometer, Unit.Hour)
v2 = pickle.loads(pickle.dumps(v))
print(f"  derived pickle:   {v} → {v2}")

# Unit
u = Unit.Parsec
u2 = pickle.loads(pickle.dumps(u))
print(f"  unit pickle:      {u} → {u2} (eq: {u == u2})")
print()


# ─── 12. Error handling ────────────────────────────────────────────────────

print("═══ 12. Error handling ═══\n")

errors = [
    ("Incompatible conversion",
     lambda: (1.0 * Unit.Meter).to(Unit.Second)),
    ("Incompatible addition",
     lambda: (1.0 * Unit.Meter) + (1.0 * Unit.Second)),
    ("Division by zero (scalar)",
     lambda: (1.0 * Unit.Meter) / 0.0),
    ("Division by zero (quantity)",
     lambda: (1.0 * Unit.Meter) / (0.0 * Unit.Meter)),
    ("Invalid JSON",
     lambda: Quantity.from_json("not json")),
    ("String unit rejected",
     lambda: Quantity(1.0, "meter")),  # type: ignore
]

for label, fn in errors:
    try:
        fn()
        print(f"  ✗ {label}: no error raised!")
    except Exception as exc:
        print(f"  ✓ {label}: {type(exc).__name__}: {exc}")
print()


# ─── 13. Real-world workflows ──────────────────────────────────────────────

print("═══ 13. Real-world workflows ═══\n")

# Astronomy: parallax → distance
parallax = 0.7687 * Unit.Arcsecond  # Proxima Centauri parallax
print(f"  Proxima Centauri parallax: {parallax}")
# Distance ≈ 1/parallax in parsecs
distance_pc = (1.0 / parallax.to(Unit.Arcsecond).value) * Unit.Parsec
distance_ly = distance_pc.to(Unit.LightYear)
print(f"    distance ≈ {distance_pc.value:.2f} pc = {distance_ly.value:.2f} ly")

# Physics: speed of light
c = 299_792_458.0 * Unit.Meter
one_sec = 1.0 * Unit.Second
light_speed = c / one_sec
print(f"\n  Speed of light: {light_speed} ({light_speed.symbol()})")
print(f"    = {light_speed.to(Unit.Kilometer, Unit.Hour)} ({DerivedUnit(Unit.Kilometer, Unit.Hour)})")

# Engineering: power output
engine_power = 150.0 * Unit.HorsepowerMetric
print(f"\n  Engine: {engine_power}")
print(f"    = {engine_power.to(Unit.Kilowatt).value:.2f} kW")
print(f"    = {engine_power.to(Unit.Watt).value:.2f} W")

# Chemistry: atomic mass
oxygen_mass = 15.999 * Unit.AtomicMassUnit
print(f"\n  Oxygen atomic mass: {oxygen_mass}")
print(f"    = {oxygen_mass.to(Unit.Gram).value:.4e} g")

print()
print("═══ All examples complete ═══")
