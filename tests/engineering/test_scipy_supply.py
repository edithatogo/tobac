"""Distribution-library migration checks; the independent oracle stays test-only."""

import inspect

import numpy as np
import pytest
from scipy.linalg import solve_triangular

from tobac.supply import release_loglikelihood


def oracle(observed, expected, covariance):
    chol = np.linalg.cholesky(covariance)
    z = solve_triangular(chol, (observed - expected).T, lower=True)
    return -0.5 * (len(observed) * np.log(2 * np.pi) + 2 * np.log(np.diag(chol)).sum() + (z * z).sum(axis=0))


def test_maintained_distribution_is_the_executed_backend() -> None:
    # The existing formula already passes parity; this guards actual replacement.
    assert "multivariate_normal.logpdf" in inspect.getsource(release_loglikelihood)


@pytest.mark.parametrize("dimensions", [1, 2, 5, 12])
@pytest.mark.parametrize("states", [1, 3, 31])
def test_matches_independent_cholesky_oracle(dimensions, states) -> None:
    rng = np.random.default_rng(89 + dimensions + states)
    for _ in range(20):
        a = rng.normal(size=(dimensions, dimensions))
        cov = a @ a.T + np.eye(dimensions) * 0.03
        y = rng.uniform(0, 100, size=dimensions)
        mu = rng.uniform(0, 100, size=(states, dimensions))
        result = release_loglikelihood(y, mu, cov)
        assert result.shape == (states,)
        np.testing.assert_allclose(result, oracle(y, mu, cov), rtol=2e-13, atol=2e-10)


def test_small_but_positive_variance_not_silently_degenerate() -> None:
    cov = np.diag([1e-14, 2.0])
    y = np.array([1.0, 2.0])
    mu = np.array([[1.0, 2.0], [1.0000001, 2.0]])
    np.testing.assert_allclose(release_loglikelihood(y, mu, cov), oracle(y, mu, cov), rtol=1e-13)


@pytest.mark.parametrize(
    "cov", [[[1, 1], [1, 1]], [[1, 2], [2, 1]], [[1, 0], [0.1, 1]], [[np.nan, 0], [0, 1]]]
)
def test_covariance_fail_closed(cov) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Finite\ matching\ nonnegative\ releases\ and\ symmetric\ covariance\ req"
            r"uired"
            r"|"
            r"Positive\ definite\ reporting\-error\ covariance\ required"
            r")"
        ),
    ):
        release_loglikelihood([1, 2], [[1, 2]], cov)


def test_density_above_one_is_legal_and_negative_observation_is_not() -> None:
    assert release_loglikelihood([1], [[1]], [[1e-6]])[0] > 0
    with pytest.raises(
        ValueError,
        match=(r"^(?:Finite\ matching\ nonnegative\ releases\ and\ symmetric\ covariance\ required)"),
    ):
        release_loglikelihood([-1], [[1]], [[1]])


@pytest.mark.parametrize(
    "args", [(-1.0, 0.0, 0.0), (10.0, 1.1, 0.0), (10.0, 0.0, -1.0), (10.0, 0.5, 6.0), (np.nan, 0.0, 0.0)]
)
def test_domain_validation_remains_before_the_library_call(args) -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

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
        expected_releases(*args)


def test_negative_releases_are_not_clipped() -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    with pytest.raises(ValueError, match="negative"):
        expected_releases(10.0, 0.0, 0.0, stock_change=-20.0)


@pytest.mark.parametrize(
    "field",
    [
        "total",
        "illicit_share",
        "lawful_unrecorded",
        "stock_change",
        "outbound",
        "wastage",
        "reporting_multiplier",
    ],
)
@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
def test_each_accounting_channel_rejects_nonfinite(field, bad) -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    inputs = {
        "total": 100.0,
        "illicit_share": 0.2,
        "lawful_unrecorded": 5.0,
        "stock_change": 0.0,
        "outbound": 0.0,
        "wastage": 0.0,
        "reporting_multiplier": 1.0,
    }
    inputs[field] = bad
    with pytest.raises(
        ValueError,
        match=(r"^(?:Invalid\ physical\ supply/accounting\ inputs)"),
    ):
        expected_releases(**inputs)


@pytest.mark.parametrize(
    "field", ["total", "illicit_share", "lawful_unrecorded", "outbound", "wastage", "reporting_multiplier"]
)
def test_each_unsigned_accounting_channel_rejects_negative(field) -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    inputs = {
        "total": 100.0,
        "illicit_share": 0.2,
        "lawful_unrecorded": 5.0,
        "stock_change": 0.0,
        "outbound": 0.0,
        "wastage": 0.0,
        "reporting_multiplier": 1.0,
    }
    inputs[field] = -0.01
    with pytest.raises(
        ValueError,
        match=(r"^(?:Invalid\ physical\ supply/accounting\ inputs)"),
    ):
        expected_releases(**inputs)


def test_zero_and_full_illicit_accounting_endpoints_are_legal() -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    np.testing.assert_array_equal(expected_releases([0.0, 100.0], [0.0, 1.0], 0.0), [0.0, 0.0])
    np.testing.assert_array_equal(expected_releases([10.0, 20.0], 0.0, [10.0, 20.0]), [0.0, 0.0])
    assert expected_releases(10.0, 0.0, 0.0, stock_change=-10.0) == 0.0
    with pytest.raises(
        ValueError,
        match=(r"^(?:Invalid\ physical\ supply/accounting\ inputs)"),
    ):
        expected_releases(10.0, 0.0, 0.0, reporting_multiplier=0.0)


@pytest.mark.parametrize(
    ("observed", "expected", "covariance"),
    [
        ([], [[]], []),
        ([1.0], [], [[1.0]]),
        ([[1.0]], [[1.0]], [[1.0]]),
        ([1.0], [1.0], [[1.0]]),
        ([1.0, 2.0], [[1.0]], [[1.0]]),
        ([1.0], [[1.0]], [1.0]),
        ([1.0], [[1.0]], [[1.0, 0.0], [0.0, 1.0]]),
        ([1.0], [[np.nan]], [[1.0]]),
        ([np.inf], [[1.0]], [[1.0]]),
        ([1.0], [[-1.0]], [[1.0]]),
        ([1.0, 2.0], [[1.0, 2.0]], [[1.0, 0.2], [0.2000001, 1.0]]),
    ],
)
def test_reporting_shape_domain_and_strict_symmetry(observed, expected, covariance) -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:Finite\ matching\ nonnegative\ releases\ and\ symmetric\ covariance\ required)"),
    ):
        release_loglikelihood(observed, expected, covariance)


def test_zero_observations_and_hypotheses_are_legal() -> None:
    observed = np.array([0.0, 1.0])
    expected = np.array([[0.0, 0.0], [1.0, 1.0]])
    covariance = np.array([[1.0, 0.2], [0.2, 1.0]])
    np.testing.assert_allclose(
        release_loglikelihood(observed, expected, covariance),
        oracle(observed, expected, covariance),
        rtol=1e-13,
    )


@pytest.mark.parametrize(
    ("total", "share", "expected"), [(0.0, 0.0, 0.0), (0.5, 0.0, 0.5), (1.0, 1.0, 0.0), (1.0, 0.5, 0.5)]
)
def test_physical_zero_and_fractional_boundaries_are_not_shifted(total, share, expected) -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    assert expected_releases(total, share, 0.0) == expected


def test_each_signed_accounting_channel_and_reporting_multiplier() -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    # Independent lawful ledger: 100*.8 - 7 + 2 + 3 + 4 = 82; report at 1.2.
    assert expected_releases(
        100.0, 0.2, 7.0, stock_change=2.0, outbound=3.0, wastage=4.0, reporting_multiplier=1.2
    ) == pytest.approx(98.4)
    assert expected_releases(
        100.0, 0.2, 7.0, stock_change=-2.0, outbound=3.0, wastage=4.0, reporting_multiplier=0.8
    ) == pytest.approx(62.4)


@pytest.mark.parametrize(("total", "unrecorded", "stock"), [(0.5, 0.7, 0.0), (0.5, 0.0, -0.7)])
def test_fractional_negative_consumption_or_releases_are_rejected(total, unrecorded, stock) -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    with pytest.raises(ValueError, match="negative"):
        expected_releases(total, 0.0, unrecorded, stock_change=stock)


@pytest.mark.parametrize(
    ("total", "share", "unrecorded", "stock"),
    [(-0.5, 1.0, 0.0, 0.0), (0.0, 1.5, 0.0, 0.0), (0.5, 0.0, 0.7, 1.0)],
)
def test_each_domain_guard_is_independent_of_later_accounting_guards(total, share, unrecorded, stock) -> None:
    from tobac.supply import expected_releases  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

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
        expected_releases(total, share, unrecorded, stock_change=stock)
