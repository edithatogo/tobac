"""Distribution-library migration checks; the independent oracle stays test-only."""
import inspect
import numpy as np
import pytest
from scipy.linalg import solve_triangular
from tobac.supply import release_loglikelihood


def oracle(observed, expected, covariance):
    chol = np.linalg.cholesky(covariance)
    z = solve_triangular(chol, (observed-expected).T, lower=True)
    return -.5*(len(observed)*np.log(2*np.pi)+2*np.log(np.diag(chol)).sum()+(z*z).sum(axis=0))


def test_maintained_distribution_is_the_executed_backend():
    # The existing formula already passes parity; this guards actual replacement.
    assert 'multivariate_normal.logpdf' in inspect.getsource(release_loglikelihood)


@pytest.mark.parametrize('dimensions', [1,2,5,12])
@pytest.mark.parametrize('states', [1,3,31])
def test_matches_independent_cholesky_oracle(dimensions, states):
    rng=np.random.default_rng(89+dimensions+states)
    for _ in range(20):
        a=rng.normal(size=(dimensions,dimensions))
        cov=a@a.T + np.eye(dimensions)*.03
        y=rng.uniform(0,100,size=dimensions)
        mu=rng.uniform(0,100,size=(states,dimensions))
        result=release_loglikelihood(y,mu,cov)
        assert result.shape==(states,)
        np.testing.assert_allclose(result,oracle(y,mu,cov),rtol=2e-13,atol=2e-10)


def test_small_but_positive_variance_not_silently_degenerate():
    cov=np.diag([1e-14,2.])
    y=np.array([1.,2.]);mu=np.array([[1.,2.],[1.0000001,2.]])
    np.testing.assert_allclose(release_loglikelihood(y,mu,cov),oracle(y,mu,cov),rtol=1e-13)


@pytest.mark.parametrize('cov', [[[1,1],[1,1]], [[1,2],[2,1]], [[1,0],[.1,1]], [[np.nan,0],[0,1]]])
def test_covariance_fail_closed(cov):
    with pytest.raises(ValueError):release_loglikelihood([1,2],[[1,2]],cov)


def test_density_above_one_is_legal_and_negative_observation_is_not():
    assert release_loglikelihood([1],[[1]],[[1e-6]])[0]>0
    with pytest.raises(ValueError):release_loglikelihood([-1],[[1]],[[1]])


@pytest.mark.parametrize('args', [(-1., 0., 0.), (10., 1.1, 0.), (10., 0., -1.),
                                   (10., .5, 6.), (np.nan, 0., 0.)])
def test_domain_validation_remains_before_the_library_call(args):
    from tobac.supply import expected_releases
    with pytest.raises(ValueError):
        expected_releases(*args)


def test_negative_releases_are_not_clipped():
    from tobac.supply import expected_releases
    with pytest.raises(ValueError, match='negative'):
        expected_releases(10., 0., 0., stock_change=-20.)
