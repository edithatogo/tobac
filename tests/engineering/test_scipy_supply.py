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


@pytest.mark.parametrize('field', ['total', 'illicit_share', 'lawful_unrecorded',
                                   'stock_change', 'outbound', 'wastage', 'reporting_multiplier'])
@pytest.mark.parametrize('bad', [np.nan, np.inf, -np.inf])
def test_each_accounting_channel_rejects_nonfinite(field, bad):
    from tobac.supply import expected_releases
    inputs = dict(total=100., illicit_share=.2, lawful_unrecorded=5., stock_change=0.,
                  outbound=0., wastage=0., reporting_multiplier=1.)
    inputs[field] = bad
    with pytest.raises(ValueError):
        expected_releases(**inputs)


@pytest.mark.parametrize('field', ['total', 'illicit_share', 'lawful_unrecorded',
                                   'outbound', 'wastage', 'reporting_multiplier'])
def test_each_unsigned_accounting_channel_rejects_negative(field):
    from tobac.supply import expected_releases
    inputs = dict(total=100., illicit_share=.2, lawful_unrecorded=5., stock_change=0.,
                  outbound=0., wastage=0., reporting_multiplier=1.)
    inputs[field] = -.01
    with pytest.raises(ValueError):
        expected_releases(**inputs)


def test_zero_and_full_illicit_accounting_endpoints_are_legal():
    from tobac.supply import expected_releases
    np.testing.assert_array_equal(expected_releases([0., 100.], [0., 1.], 0.), [0., 0.])
    np.testing.assert_array_equal(expected_releases([10., 20.], 0., [10., 20.]), [0., 0.])
    assert expected_releases(10., 0., 0., stock_change=-10.) == 0.
    with pytest.raises(ValueError):
        expected_releases(10., 0., 0., reporting_multiplier=0.)


@pytest.mark.parametrize('observed,expected,covariance', [
    ([], [[]], []), ([1.], [], [[1.]]), ([[1.]], [[1.]], [[1.]]),
    ([1.], [1.], [[1.]]), ([1., 2.], [[1.]], [[1.]]),
    ([1.], [[1.]], [1.]), ([1.], [[1.]], [[1., 0.], [0., 1.]]),
    ([1.], [[np.nan]], [[1.]]), ([np.inf], [[1.]], [[1.]]),
    ([1.], [[-1.]], [[1.]]), ([1., 2.], [[1., 2.]], [[1., .2], [.2000001, 1.]]),
])
def test_reporting_shape_domain_and_strict_symmetry(observed, expected, covariance):
    with pytest.raises(ValueError):
        release_loglikelihood(observed, expected, covariance)


def test_zero_observations_and_hypotheses_are_legal():
    observed = np.array([0., 1.])
    expected = np.array([[0., 0.], [1., 1.]])
    covariance = np.array([[1., .2], [.2, 1.]])
    np.testing.assert_allclose(release_loglikelihood(observed, expected, covariance),
                               oracle(observed, expected, covariance), rtol=1e-13)


@pytest.mark.parametrize('total,share,expected', [(0.,0.,0.),(.5,0.,.5),(1.,1.,0.),(1.,.5,.5)])
def test_physical_zero_and_fractional_boundaries_are_not_shifted(total, share, expected):
    from tobac.supply import expected_releases
    assert expected_releases(total,share,0.) == expected


def test_each_signed_accounting_channel_and_reporting_multiplier():
    from tobac.supply import expected_releases
    # Independent lawful ledger: 100*.8 - 7 + 2 + 3 + 4 = 82; report at 1.2.
    assert expected_releases(100.,.2,7.,stock_change=2.,outbound=3.,wastage=4.,reporting_multiplier=1.2) == pytest.approx(98.4)
    assert expected_releases(100.,.2,7.,stock_change=-2.,outbound=3.,wastage=4.,reporting_multiplier=.8) == pytest.approx(62.4)


@pytest.mark.parametrize('total,unrecorded,stock',[(.5,.7,0.),(.5,0.,-.7)])
def test_fractional_negative_consumption_or_releases_are_rejected(total,unrecorded,stock):
    from tobac.supply import expected_releases
    with pytest.raises(ValueError,match='negative'):
        expected_releases(total,0.,unrecorded,stock_change=stock)


@pytest.mark.parametrize('total,share,unrecorded,stock', [(-.5,1.,0.,0.),(0.,1.5,0.,0.),(.5,0.,.7,1.)])
def test_each_domain_guard_is_independent_of_later_accounting_guards(total,share,unrecorded,stock):
    from tobac.supply import expected_releases
    with pytest.raises(ValueError):
        expected_releases(total,share,unrecorded,stock_change=stock)
