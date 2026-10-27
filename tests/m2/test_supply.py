"""Regression tests for supply."""

import numpy as np
import pytest

from tobac.supply import expected_releases, release_loglikelihood


def test_supply_accounting_not_sales_equals_consumption() -> None:
    # total 100, illicit 20, lawful unrecorded 5: recorded consumption=75.
    assert expected_releases(np.array([100.0]), 0.2, 5.0, 10.0, 2.0, 3.0) == pytest.approx([90.0])


def test_stock_drawdown_and_multiplier() -> None:
    assert expected_releases(np.array([100.0]), 0.2, 5.0, -10.0, 0.0, 0.0, 1.1) == pytest.approx([71.5])


@pytest.mark.parametrize(
    "kwargs",
    [
        {"total": [-1.0]},
        {"illicit_share": 1.1},
        {"lawful_unrecorded": 81.0},
        {"stock_change": -100.0},
        {"reporting_multiplier": 0.0},
        {"outbound": -1.0},
        {"wastage": -1.0},
        {"total": [np.nan]},
    ],
)
def test_invalid_supply_inputs(kwargs) -> None:
    d = {
        "total": np.array([100.0]),
        "illicit_share": 0.2,
        "lawful_unrecorded": 5.0,
        "stock_change": 0.0,
        "outbound": 0.0,
        "wastage": 0.0,
    }
    d.update(kwargs)
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Implied\ recorded\ consumption\ or\ releases\ are\ negative;\ do\ not\ c"
            r"lip"
            r"|"
            r"Invalid\ physical\ supply/accounting\ inputs"
            r")"
        ),
    ):
        expected_releases(**d)


def test_joint_likelihood_shared_error_and_missing_precision() -> None:
    means = np.array([[70.0, 80.0], [90.0, 100.0]])
    covariance = np.array([[4.0, 2.0], [2.0, 4.0]])
    logl = release_loglikelihood([70.0, 80.0], means, covariance)
    assert logl[0] > logl[1]
    with pytest.raises(
        ValueError,
        match=(r"^(?:Positive\ definite\ reporting\-error\ covariance\ required)"),
    ):
        release_loglikelihood([70.0, 80.0], means, [[1.0, 2.0], [2.0, 1.0]])
    with pytest.raises(
        ValueError,
        match=(r"^(?:Positive\ definite\ reporting\-error\ covariance\ required)"),
    ):
        release_loglikelihood([70.0, 80.0], means, [[0.0, 0.0], [0.0, 0.0]])
    with pytest.raises(
        ValueError,
        match=(r"^(?:Finite\ matching\ nonnegative\ releases\ and\ symmetric\ covariance\ required)"),
    ):
        release_loglikelihood([-1.0, 80.0], means, covariance)
