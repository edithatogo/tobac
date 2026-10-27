"""Hypothesis contracts; hardened CI requires the dependency before collecting tests."""

import numpy as np
import pytest

pytest.importorskip("hypothesis", reason="Local optional dependency unavailable; engineering CI requires it")
from hypothesis import given, settings
from hypothesis import strategies as st

from tobac._core import DecisionProblem, exact_evpi
from tobac.supply import expected_releases
from tobac_supply.longitudinal import continuous_correlation


@settings(max_examples=100, deadline=None, derandomize=True)
@given(st.lists(st.integers(-10000, 10000), min_size=6, max_size=6))
def test_evpi_is_nonnegative_and_invariant_to_common_value_offset(values) -> None:
    matrix = np.array(values, float).reshape(3, 2)
    a = exact_evpi(DecisionProblem(matrix, ["a", "b"], "fixture_units"))
    b = exact_evpi(DecisionProblem(matrix + 10000, ["a", "b"], "fixture_units"))
    assert a >= 0
    assert a == pytest.approx(b, abs=1e-9)


@settings(max_examples=100, deadline=None, derandomize=True)
@given(
    st.floats(1, 10000, allow_nan=False, allow_infinity=False),
    st.floats(0, 0.5, allow_nan=False, allow_infinity=False),
)
def test_observation_accounting_uses_absolute_unrecorded_amount(total, illicit) -> None:
    unrecorded = total * 0.1
    result = expected_releases(total, illicit, unrecorded)
    assert float(result) == pytest.approx(total * (1 - illicit) - unrecorded)


@settings(max_examples=60, deadline=None, derandomize=True)
@given(st.lists(st.integers(0, 365), min_size=1, max_size=12), st.floats(0.1, 365))
def test_calendar_covariance_is_psd_for_irregular_and_duplicate_days(days, half_life) -> None:
    matrix = continuous_correlation(days, half_life)
    assert np.linalg.eigvalsh(matrix).min() >= -1e-10
    np.testing.assert_allclose(np.diag(matrix), 1.0)
