"""Derived unit, pickle, and integration tests for the Unit enum API."""

import pickle
import pytest
from qtty import DerivedQuantity, DerivedUnit, Quantity, Unit


class TestUnitEnumUsage:
    """Unit enum is the only supported surface (no strings)."""

    def test_requires_unit_enum(self):
        quantity = Quantity(100.0, Unit.Meter)
        assert quantity.unit == Unit.Meter

        with pytest.raises(TypeError):
            Quantity(1.0, "m")  # type: ignore[arg-type]


class TestDerivedUnits:
    """Derived unit functionality."""

    def test_create_derived_quantity(self):
        velocity = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        assert velocity.value == 10.0
        assert velocity.numerator == Unit.Meter
        assert velocity.denominator == Unit.Second

    def test_derived_from_division(self):
        distance = Quantity(100.0, Unit.Meter)
        time = Quantity(10.0, Unit.Second)

        velocity = distance / time
        assert isinstance(velocity, DerivedQuantity)
        assert velocity.value == 10.0
        assert velocity.numerator == Unit.Meter
        assert velocity.denominator == Unit.Second

    def test_dimensionless_division_same_dimension(self):
        distance = Quantity(100.0, Unit.Meter)
        reference = Quantity(50.0, Unit.Meter)

        ratio = distance / reference
        assert isinstance(ratio, Quantity)
        assert ratio.value == 2.0
        assert ratio.unit == Unit.Meter

    def test_derived_unit_symbol(self):
        velocity = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        assert velocity.symbol() == "m/s"

        speed = DerivedQuantity(100.0, Unit.Kilometer, Unit.Hour)
        assert speed.symbol() == "km/h"

    def test_derived_unit_conversion(self):
        v1 = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        v2 = v1.to(Unit.Kilometer, Unit.Hour)

        assert abs(v2.value - 36.0) < 1e-9
        assert v2.numerator == Unit.Kilometer
        assert v2.denominator == Unit.Hour

    def test_incompatible_derived_conversion(self):
        velocity = DerivedQuantity(10.0, Unit.Meter, Unit.Second)

        with pytest.raises(TypeError, match="incompatible dimensions"):
            velocity.to(Unit.Kilogram, Unit.Gram)

    def test_derived_scalar_multiplication(self):
        v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        v2 = v * 2.0
        assert v2.value == 20.0
        assert v2.numerator == Unit.Meter
        assert v2.denominator == Unit.Second

        v3 = 3.0 * v
        assert v3.value == 30.0

    def test_derived_scalar_division(self):
        v = DerivedQuantity(20.0, Unit.Meter, Unit.Second)
        v2 = v / 2.0
        assert v2.value == 10.0
        assert v2.numerator == Unit.Meter
        assert v2.denominator == Unit.Second

    def test_derived_negation(self):
        v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        v_neg = -v
        assert v_neg.value == -10.0
        assert v_neg.numerator == Unit.Meter
        assert v_neg.denominator == Unit.Second

    def test_derived_str_repr(self):
        v = DerivedQuantity(10.0, Unit.Meter, Unit.Second)
        assert str(v) == "10 m/s"
        assert "DerivedQuantity" in repr(v)


class TestPickleSupport:
    """Pickle serialization and deserialization."""

    def test_pickle_quantity(self):
        q = Quantity(100.0, Unit.Meter)

        pickled = pickle.dumps(q)
        restored = pickle.loads(pickled)

        assert restored.value == q.value
        assert restored.unit == q.unit

    def test_pickle_derived_quantity(self):
        velocity = DerivedQuantity(25.0, Unit.Meter, Unit.Second)

        pickled = pickle.dumps(velocity)
        restored = pickle.loads(pickled)

        assert restored.value == 25.0
        assert restored.numerator == Unit.Meter
        assert restored.denominator == Unit.Second

    def test_pickle_preserves_operations(self):
        q1 = Quantity(100.0, Unit.Meter)
        pickled = pickle.dumps(q1)
        q2 = pickle.loads(pickled)

        q3 = q2 + Quantity(50.0, Unit.Meter)
        assert q3.value == 150.0

        km = q2.to(Unit.Kilometer)
        assert abs(km.value - 0.1) < 1e-12

    def test_pickle_different_protocols(self):
        q = Quantity(42.0, Unit.Second)

        for protocol in range(2, pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(q, protocol=protocol)
            restored = pickle.loads(pickled)
            assert restored.value == 42.0
            assert restored.unit == Unit.Second


class TestDerivedUnitClass:
    """DerivedUnit helper class."""

    def test_create_derived_unit(self):
        unit = DerivedUnit(Unit.Meter, Unit.Second)
        assert unit.numerator == Unit.Meter
        assert unit.denominator == Unit.Second

    def test_derived_unit_symbols(self):
        unit = DerivedUnit(Unit.Meter, Unit.Second)
        assert unit.numerator == Unit.Meter
        assert unit.denominator == Unit.Second

    def test_derived_unit_str(self):
        unit = DerivedUnit(Unit.Meter, Unit.Second)
        assert str(unit) == "m/s"


class TestIntegrationWorkflows:
    """Integration tests combining derived quantities and pickling."""

    def test_velocity_calculation_workflow(self):
        distance = Quantity(150.0, Unit.Kilometer)
        time = Quantity(2.0, Unit.Hour)

        velocity = distance / time
        assert isinstance(velocity, DerivedQuantity)
        assert velocity.value == 75.0
        assert velocity.symbol() == "km/h"

        velocity_ms = velocity.to(Unit.Meter, Unit.Second)
        assert abs(velocity_ms.value - 20.833333) < 1e-4

    def test_complex_unit_mixing(self):
        m1 = Quantity(100.0, Unit.Meter)
        m2 = Quantity(50.0, Unit.Meter)

        total = m1 + m2
        assert total.value == 150.0

        s = Quantity(10.0, Unit.Second)
        velocity = total / s

        assert isinstance(velocity, DerivedQuantity)
        assert velocity.value == 15.0

    def test_pickle_workflow(self):
        distance = Quantity(100.0, Unit.Meter)
        time = Quantity(10.0, Unit.Second)
        velocity = distance / time

        pickled = pickle.dumps(velocity)
        restored = pickle.loads(pickled)
        assert restored.value == 10.0
        assert restored.numerator == Unit.Meter
        assert restored.denominator == Unit.Second

        doubled = restored * 2.0
        assert doubled.value == 20.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
