"""Tests for the public Python API surface of qtty.

Verifies that the package exposes at least:
  - unit identifiers (Unit / UnitId enum)
  - a quantity object (Quantity)
  - conversion operations
  - Python exceptions for errors (no crashes or raw status codes)
  - derived quantities and units
  - string/display conventions
"""

import math
import pickle
import pytest

import qtty
from qtty import DerivedQuantity, DerivedUnit, Quantity, Unit, UnitId


# ── Module-level exports ─────────────────────────────────────────────────────


class TestModuleExports:
    """Verify the public surface of the qtty package."""

    def test_all_exports_present(self):
        for name in ("Quantity", "DerivedQuantity", "DerivedUnit", "Unit", "UnitId", "__version__"):
            assert hasattr(qtty, name), f"qtty.{name} missing"

    def test_version_is_string(self):
        assert isinstance(qtty.__version__, str)
        assert qtty.__version__ == "0.1.0"

    def test_unit_is_alias_for_unitid(self):
        assert Unit is UnitId

    def test_import_from_submodule(self):
        """Can import from qtty._qtty directly."""
        from qtty._qtty import Quantity as Q2
        assert Q2 is Quantity


# ── UnitId enum ──────────────────────────────────────────────────────────────


class TestUnitEnum:
    """UnitId exposes all five dimensions and common units."""

    @pytest.mark.parametrize("unit", [
        Unit.Meter, Unit.Kilometer, Unit.Millimeter, Unit.AstronomicalUnit,
        Unit.LightYear, Unit.Parsec, Unit.Inch, Unit.Foot, Unit.Mile,
    ])
    def test_length_units_exist(self, unit):
        assert unit is not None

    @pytest.mark.parametrize("unit", [
        Unit.Second, Unit.Minute, Unit.Hour, Unit.Day, Unit.Year,
        Unit.Millisecond, Unit.Nanosecond, Unit.JulianYear,
    ])
    def test_time_units_exist(self, unit):
        assert unit is not None

    @pytest.mark.parametrize("unit", [
        Unit.Radian, Unit.Degree, Unit.Arcminute, Unit.Arcsecond,
        Unit.Gradian, Unit.Turn, Unit.HourAngle,
    ])
    def test_angle_units_exist(self, unit):
        assert unit is not None

    @pytest.mark.parametrize("unit", [
        Unit.Gram, Unit.Kilogram, Unit.Milligram, Unit.Pound,
        Unit.Ounce, Unit.Tonne, Unit.SolarMass,
    ])
    def test_mass_units_exist(self, unit):
        assert unit is not None

    @pytest.mark.parametrize("unit", [
        Unit.Watt, Unit.Kilowatt, Unit.Megawatt,
        Unit.HorsepowerMetric, Unit.SolarLuminosity,
    ])
    def test_power_units_exist(self, unit):
        assert unit is not None

    def test_unit_equality(self):
        assert Unit.Meter == Unit.Meter
        assert Unit.Meter != Unit.Kilometer

    def test_unit_is_hashable(self):
        s = {Unit.Meter, Unit.Kilometer, Unit.Meter}
        assert len(s) == 2

    def test_unit_repr(self):
        r = repr(Unit.Meter)
        assert "Meter" in r

    def test_no_string_construction(self):
        """Units cannot be constructed from strings — typo-proof."""
        with pytest.raises(TypeError):
            Quantity(1.0, "Meter")  # type: ignore[arg-type]

    def test_unit_pickle(self):
        for u in (Unit.Meter, Unit.Second, Unit.Degree, Unit.Kilogram, Unit.Watt):
            restored = pickle.loads(pickle.dumps(u))
            assert restored == u


# ── Quantity object ──────────────────────────────────────────────────────────


class TestQuantityCreation:
    """Quantity(value, unit) construction."""

    def test_basic(self):
        q = Quantity(42.0, Unit.Meter)
        assert q.value == 42.0
        assert q.unit == Unit.Meter

    def test_negative_value(self):
        q = Quantity(-5.0, Unit.Second)
        assert q.value == -5.0

    def test_zero(self):
        q = Quantity(0.0, Unit.Kilogram)
        assert q.value == 0.0

    def test_large_value(self):
        q = Quantity(1e30, Unit.Meter)
        assert q.value == 1e30

    def test_integer_coercion(self):
        q = Quantity(7, Unit.Meter)
        assert q.value == 7.0


# ── Conversion operations ───────────────────────────────────────────────────


class TestConversion:
    """Quantity.to(unit) delegates to Rust conversion engine."""

    def test_meters_to_kilometers(self):
        q = Quantity(5000.0, Unit.Meter).to(Unit.Kilometer)
        assert abs(q.value - 5.0) < 1e-12
        assert q.unit == Unit.Kilometer

    def test_hours_to_seconds(self):
        q = Quantity(2.0, Unit.Hour).to(Unit.Second)
        assert abs(q.value - 7200.0) < 1e-9

    def test_degrees_to_radians(self):
        q = Quantity(360.0, Unit.Degree).to(Unit.Radian)
        assert abs(q.value - 2 * math.pi) < 1e-12

    def test_kilograms_to_pounds(self):
        q = Quantity(1.0, Unit.Kilogram).to(Unit.Pound)
        assert abs(q.value - (1000.0 / 453.59237)) < 1e-6

    def test_watts_to_kilowatts(self):
        q = Quantity(2500.0, Unit.Watt).to(Unit.Kilowatt)
        assert abs(q.value - 2.5) < 1e-12

    def test_roundtrip(self):
        original = Quantity(123.456, Unit.Meter)
        back = original.to(Unit.Kilometer).to(Unit.Meter)
        assert abs(back.value - original.value) < 1e-9

    def test_same_unit_conversion(self):
        q = Quantity(42.0, Unit.Meter)
        q2 = q.to(Unit.Meter)
        assert abs(q2.value - 42.0) < 1e-12

    def test_astronomical_unit_to_meters(self):
        au = Quantity(1.0, Unit.AstronomicalUnit).to(Unit.Meter)
        assert abs(au.value - 149597870700.0) < 1.0

    def test_parsec_to_lightyear(self):
        pc = Quantity(1.0, Unit.Parsec).to(Unit.LightYear)
        # 1 parsec ≈ 3.2616 light-years
        assert abs(pc.value - 3.2616) < 0.001


# ── Error handling (Python exceptions, not crashes) ──────────────────────────


class TestErrorHandling:
    """Verify all failures appear as Python exceptions."""

    def test_incompatible_conversion_raises_type_error(self):
        with pytest.raises(TypeError, match="incompatible dimensions"):
            Quantity(1.0, Unit.Meter).to(Unit.Second)

    def test_incompatible_addition_raises_type_error(self):
        with pytest.raises(TypeError, match="incompatible dimensions"):
            Quantity(1.0, Unit.Meter) + Quantity(1.0, Unit.Kilogram)

    def test_incompatible_subtraction_raises_type_error(self):
        with pytest.raises(TypeError):
            Quantity(1.0, Unit.Second) - Quantity(1.0, Unit.Degree)

    def test_incompatible_comparison_raises_type_error(self):
        with pytest.raises(TypeError):
            Quantity(1.0, Unit.Meter) < Quantity(1.0, Unit.Second)

    def test_division_by_zero_scalar(self):
        with pytest.raises(ZeroDivisionError):
            Quantity(10.0, Unit.Meter) / 0.0

    def test_division_by_zero_quantity(self):
        with pytest.raises(ZeroDivisionError):
            Quantity(10.0, Unit.Meter) / Quantity(0.0, Unit.Meter)

    def test_multiply_two_quantities_raises(self):
        """Multiplying two quantities is not (yet) supported."""
        with pytest.raises(TypeError):
            Quantity(1.0, Unit.Meter) * Quantity(2.0, Unit.Meter)

    def test_floor_division_not_implemented(self):
        with pytest.raises(Exception):  # NotImplementedError or TypeError
            Quantity(10.0, Unit.Meter) // 2.0

    def test_modulo_not_implemented(self):
        with pytest.raises(Exception):
            Quantity(10.0, Unit.Meter) % 2.0

    def test_derived_conversion_dimension_mismatch(self):
        v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        with pytest.raises(TypeError, match="incompatible dimensions"):
            v.to(Unit.Kilogram, Unit.Gram)

    def test_derived_division_by_zero(self):
        v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        with pytest.raises(ZeroDivisionError):
            v / 0.0


# ── Arithmetic ───────────────────────────────────────────────────────────────


class TestArithmetic:
    """Arithmetic delegates dimension checking to Rust."""

    def test_add_mixed_units(self):
        result = Quantity(1.0, Unit.Kilometer) + Quantity(500.0, Unit.Meter)
        assert abs(result.value - 1.5) < 1e-9
        assert result.unit == Unit.Kilometer

    def test_sub_mixed_units(self):
        result = Quantity(2.0, Unit.Hour) - Quantity(30.0, Unit.Minute)
        assert abs(result.value - 1.5) < 1e-9
        assert result.unit == Unit.Hour

    def test_scalar_mul_int(self):
        q = Quantity(3.0, Unit.Meter) * 4
        assert abs(q.value - 12.0) < 1e-12

    def test_rmul(self):
        q = 3.0 * Quantity(4.0, Unit.Second)
        assert abs(q.value - 12.0) < 1e-12

    def test_neg(self):
        q = -Quantity(5.0, Unit.Meter)
        assert q.value == -5.0

    def test_pos(self):
        q = +Quantity(-5.0, Unit.Meter)
        assert q.value == -5.0

    def test_abs(self):
        q = abs(Quantity(-7.0, Unit.Meter))
        assert q.value == 7.0

    def test_division_same_dimension_gives_quantity(self):
        ratio = Quantity(100.0, Unit.Meter) / Quantity(50.0, Unit.Meter)
        assert isinstance(ratio, Quantity)
        assert abs(ratio.value - 2.0) < 1e-12

    def test_division_cross_dimension_gives_derived(self):
        v = Quantity(100.0, Unit.Meter) / Quantity(10.0, Unit.Second)
        assert isinstance(v, DerivedQuantity)
        assert abs(v.value - 10.0) < 1e-12
        assert v.numerator == Unit.Meter
        assert v.denominator == Unit.Second


# ── Comparison operators ─────────────────────────────────────────────────────


class TestComparisons:
    """Comparisons work across compatible units."""

    def test_eq_same_unit(self):
        assert Quantity(5.0, Unit.Meter) == Quantity(5.0, Unit.Meter)

    def test_eq_different_units(self):
        assert Quantity(1.0, Unit.Kilometer) == Quantity(1000.0, Unit.Meter)

    def test_ne(self):
        assert Quantity(1.0, Unit.Meter) != Quantity(2.0, Unit.Meter)

    def test_lt(self):
        assert Quantity(1.0, Unit.Meter) < Quantity(1.0, Unit.Kilometer)

    def test_le(self):
        assert Quantity(1000.0, Unit.Meter) <= Quantity(1.0, Unit.Kilometer)
        assert Quantity(999.0, Unit.Meter) <= Quantity(1.0, Unit.Kilometer)

    def test_gt(self):
        assert Quantity(1.0, Unit.Kilometer) > Quantity(999.0, Unit.Meter)

    def test_ge(self):
        assert Quantity(1.0, Unit.Kilometer) >= Quantity(1000.0, Unit.Meter)
        assert Quantity(1.001, Unit.Kilometer) >= Quantity(1000.0, Unit.Meter)

    def test_incompatible_eq_returns_false(self):
        """Equality between incompatible dimensions returns False (no raise)."""
        assert not (Quantity(1.0, Unit.Meter) == Quantity(1.0, Unit.Second))


# ── Display / string conventions ─────────────────────────────────────────────


class TestDisplay:
    """String representations are human-friendly."""

    def test_str_format(self):
        s = str(Quantity(42.5, Unit.Meter))
        assert "42.5" in s
        assert "Meter" in s

    def test_repr_format(self):
        r = repr(Quantity(42.5, Unit.Meter))
        assert "Quantity" in r
        assert "42.5" in r
        assert "Meter" in r

    def test_derived_str(self):
        s = str(DerivedQuantity(10.0, Unit.Meter, Unit.Second))
        assert "m/s" in s

    def test_derived_repr(self):
        r = repr(DerivedQuantity(10.0, Unit.Meter, Unit.Second))
        assert "DerivedQuantity" in r

    def test_derived_unit_str(self):
        assert str(DerivedUnit(Unit.Kilometer, Unit.Hour)) == "km/h"

    def test_derived_symbol(self):
        d = DerivedQuantity(60.0, Unit.Kilometer, Unit.Hour)
        assert d.symbol() == "km/h"


# ── Pickle / serialization ──────────────────────────────────────────────────


class TestPickle:
    """Quantities survive pickle roundtrip."""

    def test_quantity_roundtrip(self):
        q = Quantity(99.9, Unit.Meter)
        q2 = pickle.loads(pickle.dumps(q))
        assert q2.value == q.value
        assert q2.unit == q.unit

    def test_derived_quantity_roundtrip(self):
        d = DerivedQuantity(3.5, Unit.Kilometer, Unit.Hour)
        d2 = pickle.loads(pickle.dumps(d))
        assert d2.value == d.value
        assert d2.numerator == d.numerator
        assert d2.denominator == d.denominator

    def test_unit_roundtrip(self):
        u = Unit.Parsec
        assert pickle.loads(pickle.dumps(u)) == u

    def test_pickle_then_convert(self):
        q = pickle.loads(pickle.dumps(Quantity(1.0, Unit.Kilometer)))
        m = q.to(Unit.Meter)
        assert abs(m.value - 1000.0) < 1e-9


# ── Hash / set / dict usage ─────────────────────────────────────────────────


class TestHashing:
    def test_quantity_in_set(self):
        s = {Quantity(1.0, Unit.Meter), Quantity(1.0, Unit.Meter), Quantity(2.0, Unit.Meter)}
        assert len(s) == 2

    def test_quantity_as_dict_key(self):
        d = {Quantity(1.0, Unit.Meter): "one meter"}
        assert d[Quantity(1.0, Unit.Meter)] == "one meter"


# ── DerivedQuantity operations ───────────────────────────────────────────────


class TestDerivedOperations:
    """DerivedQuantity arithmetic and conversion."""

    def test_convert_velocity(self):
        v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        v2 = v.to(Unit.Kilometer, Unit.Hour)
        assert abs(v2.value - 36.0) < 1e-6

    def test_scalar_mul(self):
        v = DerivedQuantity(5.0, Unit.Meter, Unit.Second)
        assert (v * 3.0).value == 15.0

    def test_scalar_div(self):
        v = DerivedQuantity(15.0, Unit.Meter, Unit.Second)
        assert (v / 3.0).value == 5.0

    def test_neg(self):
        v = DerivedQuantity(5.0, Unit.Meter, Unit.Second)
        assert (-v).value == -5.0

    def test_derived_unit_accessors(self):
        u = DerivedUnit(Unit.Meter, Unit.Second)
        assert u.numerator == Unit.Meter
        assert u.denominator == Unit.Second


# ── Integration: end-to-end workflows ────────────────────────────────────────


class TestEndToEnd:
    """Realistic multi-step workflows that a user would perform."""

    def test_astronomical_distance_conversion(self):
        """Convert between astronomical distance units."""
        d = Quantity(1.0, Unit.Parsec)
        au = d.to(Unit.AstronomicalUnit)
        # 1 pc ≈ 206265 AU
        assert abs(au.value - 206265) < 5

    def test_velocity_workflow(self):
        """Compute and convert a velocity."""
        d = Quantity(42195.0, Unit.Meter)   # marathon distance
        t = Quantity(2.0, Unit.Hour)
        v = d / t
        assert isinstance(v, DerivedQuantity)
        v_kmh = v.to(Unit.Kilometer, Unit.Hour)
        assert abs(v_kmh.value - 21.0975) < 0.001

    def test_mass_unit_chain(self):
        """Chain mass conversions."""
        kg = Quantity(1.0, Unit.Kilogram)
        g = kg.to(Unit.Gram)
        mg = g.to(Unit.Milligram)
        assert abs(mg.value - 1e6) < 1e-3

    def test_mixed_addition_preserves_lhs_unit(self):
        """Adding different-unit quantities returns result in left operand's unit."""
        result = Quantity(1.0, Unit.Kilometer) + Quantity(500.0, Unit.Meter)
        assert result.unit == Unit.Kilometer

    def test_no_c_abi_exposure(self):
        """Python users never see raw C ABI structs, status codes, or pointers."""
        q = Quantity(1.0, Unit.Meter)
        # The object is a proper Python Quantity, not a raw FFI struct
        assert type(q).__name__ == "Quantity"
        assert hasattr(q, "value")
        assert hasattr(q, "unit")
        assert hasattr(q, "to")
