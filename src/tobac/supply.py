"""A unit-neutral accounting bridge, NOT a fitted NZ supply/consumption model.

Inputs must share one time, geography, population and physical unit. Enforce that
in an EvidencePacket scope. Release forecasts never become new observations.
Lawful unrecorded consumption is an ABSOLUTE amount in the same unit, not a share.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import Covariance, multivariate_normal


def expected_releases(total, illicit_share, lawful_unrecorded, stock_change=0.,
                      outbound=0., wastage=0., reporting_multiplier=1.) -> np.ndarray:
    """Expected measured releases = (recorded consumption + stock + flows) * bias.

    Positive stock_change means inventory accumulation. Outbound is lawful supply
    leaving the target consumption geography; lawful inputs not in releases belong
    in lawful_unrecorded. Do not count visitors/duty-free in both adjustments.
    Signed stock changes are allowed; negative implied releases are rejected.
    """
    t, i, u, stock, out, waste, bias = np.broadcast_arrays(
        *[np.asarray(x, dtype=float) for x in
          (total, illicit_share, lawful_unrecorded, stock_change, outbound, wastage, reporting_multiplier)])
    if (not all(np.isfinite(x).all() for x in (t,i,u,stock,out,waste,bias))
            or (t < 0).any() or (i < 0).any() or (i > 1).any() or (u < 0).any()
            or (out < 0).any() or (waste < 0).any() or (bias <= 0).any()):
        raise ValueError('Invalid physical supply/accounting inputs')
    recorded = t * (1-i) - u
    releases = recorded + stock + out + waste
    if (recorded < 0).any() or (releases < 0).any():
        raise ValueError('Implied recorded consumption or releases are negative; do not clip')
    return releases * bias


def release_loglikelihood(observed, expected, covariance) -> np.ndarray:
    """Gaussian reporting-error likelihood with explicit inter-period covariance.

    Rows of expected are hypotheses; columns are jointly observed releases.
    This is a declared error approximation, not precision inferred from sales.
    """
    y = np.asarray(observed, float)
    mu = np.asarray(expected, float)
    cov = np.asarray(covariance, float)
    if (y.ndim != 1 or not len(y) or mu.ndim != 2 or mu.shape[1] != len(y) or not len(mu)
            or cov.shape != (len(y),len(y)) or not all(np.isfinite(a).all() for a in (y,mu,cov))
            or (y < 0).any() or (mu < 0).any() or not np.allclose(cov,cov.T,atol=1e-12,rtol=0)):
        raise ValueError('Finite matching nonnegative releases and symmetric covariance required')
    try:
        chol = np.linalg.cholesky(cov)
    except np.linalg.LinAlgError as exc:
        raise ValueError('Positive definite reporting-error covariance required') from exc
    # Preserve the original positive-definite contract, including very small
    # positive eigenvalues; do not apply SciPy's default pseudo-inverse cutoff.
    distribution_covariance = Covariance.from_cholesky(chol)
    return np.atleast_1d(multivariate_normal.logpdf(
        y - mu, mean=np.zeros(len(y)), cov=distribution_covariance,
    ))
