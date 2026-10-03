"""Contract test for a genuinely independent PyO3 extension."""

import pytest

import qtty

consumer = pytest.importorskip(
    "qtty_bridge_consumer",
    reason="independent bridge fixture is built by scripts/test_bridge_contract.py and CI",
)


# Stable qtty-ffi discriminants, deliberately passed as primitive integers.
REPRESENTATIVE_UNITS = [
    (12.5, 10011, qtty.Unit.Meter, qtty.Unit.Kilometer),
    (90.0, 20008, qtty.Unit.Second, qtty.Unit.Minute),
    (3.25, 40013, qtty.Unit.Kilogram, qtty.Unit.Gram),
    (180.0, 31004, qtty.Unit.Degree, qtty.Unit.Radian),
]


@pytest.mark.parametrize(("number", "unit_id", "unit", "compatible_unit"), REPRESENTATIVE_UNITS)
def test_consumer_constructs_canonical_quantity(number, unit_id, unit, compatible_unit):
    value = consumer.make_quantity(number, unit_id)

    assert type(value) is qtty.Quantity
    assert isinstance(value, qtty.Quantity)
    assert value.value == number
    assert value.unit == unit
    # A successful conversion demonstrates that the physical dimension survived.
    assert value.to(compatible_unit).unit == compatible_unit


@pytest.mark.parametrize(("number", "unit_id", "unit", "_compatible_unit"), REPRESENTATIVE_UNITS)
def test_consumer_extracts_and_round_trips_canonical_quantity(
    number, unit_id, unit, _compatible_unit
):
    canonical = qtty.Quantity(number, unit)

    assert consumer.extract_quantity(canonical) == (number, unit_id)
    result = consumer.round_trip(canonical)
    assert type(result) is qtty.Quantity
    assert result.value == number
    assert result.unit == unit


@pytest.mark.parametrize("invalid", [None, object(), 3.5, "not a quantity"])
def test_consumer_rejects_non_quantities(invalid):
    with pytest.raises(TypeError):
        consumer.extract_quantity(invalid)


def test_consumer_rejects_invalid_raw_unit_id():
    with pytest.raises(ValueError, match="invalid qtty unit ID"):
        consumer.make_quantity(1.0, 2**32 - 1)


def test_consumer_rejects_malformed_raw_input():
    with pytest.raises((TypeError, OverflowError)):
        consumer.make_quantity(1.0, "Meter")
