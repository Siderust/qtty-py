"""Basic tests for qtty Python bindings (Unit enum API)."""

import pytest
from qtty import Quantity, Unit


def test_quantity_creation():
    """Test creating a quantity with value and unit."""
    q = Quantity(100.0, Unit.Meter)
    assert q.value == 100.0
    assert q.unit == Unit.Meter


def test_quantity_conversion():
    """Test unit conversion."""
    m = Quantity(1000.0, Unit.Meter)
    km = m.to(Unit.Kilometer)
    assert abs(km.value - 1.0) < 1e-12
    assert km.unit == Unit.Kilometer


def test_quantity_conversion_roundtrip():
    """Test that conversion roundtrips correctly."""
    original = Quantity(100.0, Unit.Meter)
    km = original.to(Unit.Kilometer)
    back = km.to(Unit.Meter)
    assert abs(back.value - original.value) < 1e-12


def test_incompatible_conversion():
    """Test that converting between incompatible dimensions raises TypeError."""
    m = Quantity(100.0, Unit.Meter)
    with pytest.raises(TypeError, match="incompatible dimensions"):
        m.to(Unit.Second)


def test_quantity_addition():
    """Test adding two quantities with the same unit."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(5.0, Unit.Meter)
    c = a + b
    assert abs(c.value - 15.0) < 1e-12
    assert c.unit == Unit.Meter


def test_quantity_addition_different_units():
    """Test adding quantities with different but compatible units."""
    m = Quantity(1.0, Unit.Meter)
    km = Quantity(1.0, Unit.Kilometer)
    result = m + km
    assert abs(result.value - 1001.0) < 1e-9
    assert result.unit == Unit.Meter


def test_incompatible_addition():
    """Test that adding incompatible dimensions raises TypeError."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(5.0, Unit.Second)
    with pytest.raises(TypeError, match="incompatible dimensions"):
        _ = a + b


def test_quantity_subtraction():
    """Test subtracting two quantities."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(3.0, Unit.Meter)
    c = a - b
    assert abs(c.value - 7.0) < 1e-12
    assert c.unit == Unit.Meter


def test_incompatible_subtraction():
    """Test that subtracting incompatible dimensions raises TypeError."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(5.0, Unit.Second)
    with pytest.raises(TypeError, match="incompatible dimensions"):
        _ = a - b


def test_scalar_multiplication():
    """Test multiplying a quantity by a scalar."""
    q = Quantity(10.0, Unit.Meter)
    result = q * 2.5
    assert abs(result.value - 25.0) < 1e-12
    assert result.unit == Unit.Meter


def test_scalar_multiplication_reverse():
    """Test reverse multiplication (scalar * quantity)."""
    q = Quantity(10.0, Unit.Meter)
    result = 2.5 * q
    assert abs(result.value - 25.0) < 1e-12
    assert result.unit == Unit.Meter


def test_scalar_division():
    """Test dividing a quantity by a scalar."""
    q = Quantity(10.0, Unit.Meter)
    result = q / 2.0
    assert abs(result.value - 5.0) < 1e-12
    assert result.unit == Unit.Meter


def test_division_by_zero():
    """Test that division by zero raises ZeroDivisionError."""
    q = Quantity(10.0, Unit.Meter)
    with pytest.raises(ZeroDivisionError):
        _ = q / 0.0


def test_quantity_negation():
    """Test negating a quantity."""
    q = Quantity(10.0, Unit.Meter)
    neg_q = -q
    assert neg_q.value == -10.0
    assert neg_q.unit == Unit.Meter


def test_quantity_positive():
    """Test positive unary operator."""
    q = Quantity(-10.0, Unit.Meter)
    pos_q = +q
    assert pos_q.value == -10.0  # Doesn't change the sign
    assert pos_q.unit == Unit.Meter


def test_quantity_abs():
    """Test absolute value."""
    q = Quantity(-10.0, Unit.Meter)
    abs_q = abs(q)
    assert abs_q.value == 10.0
    assert abs_q.unit == Unit.Meter


def test_quantity_equality():
    """Test equality comparison."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(10.0, Unit.Meter)
    c = Quantity(10000.0, Unit.Millimeter)  # Same value, different unit
    d = Quantity(5.0, Unit.Meter)

    assert a == b
    assert a == c  # Should be equal after conversion
    assert not (a == d)


def test_quantity_inequality():
    """Test inequality comparison."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(5.0, Unit.Meter)

    assert a != b
    assert not (a != a)


def test_quantity_less_than():
    """Test less than comparison."""
    a = Quantity(5.0, Unit.Meter)
    b = Quantity(10.0, Unit.Meter)

    assert a < b
    assert not (b < a)


def test_quantity_less_equal():
    """Test less than or equal comparison."""
    a = Quantity(5.0, Unit.Meter)
    b = Quantity(10.0, Unit.Meter)
    c = Quantity(5.0, Unit.Meter)

    assert a <= b
    assert a <= c
    assert not (b <= a)


def test_quantity_greater_than():
    """Test greater than comparison."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(5.0, Unit.Meter)

    assert a > b
    assert not (b > a)


def test_quantity_greater_equal():
    """Test greater than or equal comparison."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(5.0, Unit.Meter)
    c = Quantity(10.0, Unit.Meter)

    assert a >= b
    assert a >= c
    assert not (b >= a)


def test_incompatible_comparison():
    """Test that comparing incompatible dimensions raises TypeError."""
    a = Quantity(10.0, Unit.Meter)
    b = Quantity(5.0, Unit.Second)

    with pytest.raises(TypeError, match="incompatible dimensions"):
        _ = a < b


def test_quantity_repr():
    """Test string representation."""
    q = Quantity(100.0, Unit.Meter)
    assert repr(q) == "Quantity(100, Meter)"  # Python formats 100.0 as "100"


def test_quantity_str():
    """Test human-readable string."""
    q = Quantity(100.0, Unit.Meter)
    assert str(q) == "100 Meter"  # Python formats 100.0 as "100"


def test_quantity_hash():
    """Test that quantities can be hashed."""
    q1 = Quantity(100.0, Unit.Meter)
    q2 = Quantity(100.0, Unit.Meter)
    q3 = Quantity(200.0, Unit.Meter)

    # Same quantities should have same hash
    assert hash(q1) == hash(q2)
    # Different quantities should (likely) have different hashes
    assert hash(q1) != hash(q3)

    # Should be usable in sets and dicts
    qty_set = {q1, q2, q3}
    assert len(qty_set) == 2  # q1 and q2 are equal


def test_astronomical_units():
    """Test astronomical unit conversions."""
    au = Quantity(1.0, Unit.AstronomicalUnit)
    meters = au.to(Unit.Meter)
    assert abs(meters.value - 149597870700.0) < 1e-3

    ly = Quantity(1.0, Unit.LightYear)
    meters = ly.to(Unit.Meter)
    assert abs(meters.value - 9460730472580800.0) < 1e6


def test_time_units():
    """Test time unit conversions."""
    hours = Quantity(1.0, Unit.Hour)
    minutes = hours.to(Unit.Minute)
    assert abs(minutes.value - 60.0) < 1e-12

    seconds = hours.to(Unit.Second)
    assert abs(seconds.value - 3600.0) < 1e-12


def test_angle_units():
    """Test angle unit conversions."""
    degrees = Quantity(180.0, Unit.Degree)
    radians = degrees.to(Unit.Radian)
    import math

    assert abs(radians.value - math.pi) < 1e-12
