"""Generated rectangular accounting supports with an independent corner oracle."""

from __future__ import annotations

import os
from fractions import Fraction
from itertools import product

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tobac.partial_identification import Interval, accounting_bounds

_EXAMPLES = int(os.environ.get("TOBAC_PROPERTY_EXAMPLES", "100"))
if not 1 <= _EXAMPLES <= 1000:
    message = "TOBAC_PROPERTY_EXAMPLES must be between 1 and 1000"
    raise ValueError(message)
_BOUNDED = settings(max_examples=_EXAMPLES, deadline=1000)


def _support(minimum: int, maximum: int) -> st.SearchStrategy[Interval]:
    return st.tuples(st.integers(minimum, maximum), st.integers(minimum, maximum)).map(
        lambda pair: Interval(float(min(pair)), float(max(pair)))
    )


_SUPPORTS = st.fixed_dictionaries(
    {
        "releases": _support(0, 10000),
        "reporting_bias": _support(1, 100),
        "unrecorded": _support(0, 10000),
        "stock": _support(-10000, 10000),
        "outbound": _support(0, 10000),
        "wastage": _support(0, 10000),
    }
)


@_BOUNDED
@given(supports=_SUPPORTS)
def test_accounting_bounds_equal_extrema_of_every_rectangular_corner(
    supports: dict[str, Interval],
) -> None:
    """Enumerating 64 exact rational corners checks signs and attainable bounds."""
    corners = product(
        *[
            (Fraction(supports[name].lower), Fraction(supports[name].upper))
            for name in ("releases", "reporting_bias", "unrecorded", "stock", "outbound", "wastage")
        ]
    )
    possible = [
        releases / bias + unrecorded - stock - outbound - wastage
        for releases, bias, unrecorded, stock, outbound, wastage in corners
    ]
    actual = accounting_bounds(**supports)
    assert actual.lower == pytest.approx(float(min(possible)), rel=1e-12, abs=1e-9)
    assert actual.upper == pytest.approx(float(max(possible)), rel=1e-12, abs=1e-9)


@_BOUNDED
@given(supports=_SUPPORTS, stock_delta=st.integers(-10000, 10000))
def test_stock_translation_retains_the_signed_accounting_discrepancy(
    supports: dict[str, Interval], stock_delta: int
) -> None:
    before = accounting_bounds(**supports)
    stock = supports["stock"]
    supports["stock"] = Interval(stock.lower + stock_delta, stock.upper + stock_delta)
    after = accounting_bounds(**supports)
    assert after.lower == pytest.approx(before.lower - stock_delta, rel=1e-12, abs=1e-9)
    assert after.upper == pytest.approx(before.upper - stock_delta, rel=1e-12, abs=1e-9)


@_BOUNDED
@given(supports=_SUPPORTS, widening=st.integers(0, 10000))
def test_wider_stock_uncertainty_cannot_narrow_the_result(
    supports: dict[str, Interval], widening: int
) -> None:
    before = accounting_bounds(**supports)
    stock = supports["stock"]
    supports["stock"] = Interval(stock.lower - widening, stock.upper + widening)
    after = accounting_bounds(**supports)
    assert after.lower <= before.lower
    assert after.upper >= before.upper


@_BOUNDED
@given(supports=_SUPPORTS, lower=st.integers(-100, 0), upper=st.integers(0, 100))
def test_calibration_support_touching_zero_is_rejected(
    supports: dict[str, Interval], lower: int, upper: int
) -> None:
    supports["reporting_bias"] = Interval(float(lower), float(upper))
    with pytest.raises(ValueError, match="strictly positive calibration required"):
        accounting_bounds(**supports)
