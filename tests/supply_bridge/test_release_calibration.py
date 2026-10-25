"""Independent numerical and boundary checks for the release-only calibration."""
from pathlib import Path

import numpy as np
import pytest
from scipy.special import logsumexp
from scipy.stats import norm


def module():
    from tobac_supply import release_calibration
    return release_calibration


YEARS = np.arange(2010, 2026)
VALUES = np.array([2293, 2102, 2046, 1905, 1857, 1788, 1768, 1687,
                   1618, 1492, 1429, 1426, 1249, 1052, 968, 755.])


def test_receipt_normalises_only_valid_grouping():
    m = module()
    text = 'Series Label,Year,Tonnes\nTotal tobacco sold tonnes (excl. cigars/cigarillos),2024,968\nTotal tobacco sold tonnes (excl. cigars/cigarillos),2025,1,755\n'
    assert m.parse_release_export(text, [2024,2025]) == [
        {'year':2024,'tonnes':968}, {'year':2025,'tonnes':1755}]


@pytest.mark.parametrize('values', ['2,29', '2,293,0', '-10', 'nan', '0', '7.55', '"755"'])
def test_receipt_rejects_bad_grouping(values):
    with pytest.raises(ValueError):
        module().parse_release_export('Total tobacco sold tonnes (excl. cigars/cigarillos),2025,'+values, [2025])


def test_receipt_rejects_missing_duplicate_and_unknown_series():
    m = module(); row='Total tobacco sold tonnes (excl. cigars/cigarillos),2025,755'
    for text,years in [(row,[2024,2025]), (row+'\n'+row,[2025]), ('Other,2025,755',[2025])]:
        with pytest.raises(ValueError): m.parse_release_export(text,years)


def trapezoid_gaussian_mass(nodes, mean, sd):
    """1-D Gaussian mass per quadrature node, halving both outer intervals."""
    spacing = nodes[1] - nodes[0]
    weights = np.full(nodes.size, spacing)
    weights[0] *= 0.5
    weights[-1] *= 0.5
    return weights * np.exp(-0.5 * ((nodes - mean) / sd) ** 2)


def test_prior_grid_equals_independent_trapezoid_product():
    m = module()
    grid = m.ReleaseGrid(mu_points=5, sigma_points=4)
    mu_nodes = np.linspace(grid.mu_min, grid.mu_max, grid.mu_points)
    sigma_nodes = np.linspace(grid.sigma_min, grid.sigma_max, grid.sigma_points)
    expected = np.outer(
        trapezoid_gaussian_mass(mu_nodes, grid.mu_prior_mean, grid.mu_prior_sd),
        trapezoid_gaussian_mass(sigma_nodes, 0.0, grid.sigma_prior_scale))
    expected /= expected.sum()
    mu, sigma, prior = m.make_grid(grid)
    np.testing.assert_allclose(mu.reshape(5, 4), np.broadcast_to(mu_nodes[:, None], (5, 4)),
                               rtol=0, atol=0)
    np.testing.assert_allclose(sigma.reshape(5, 4), np.broadcast_to(sigma_nodes[None, :], (5, 4)),
                               rtol=0, atol=0)
    np.testing.assert_allclose(prior.reshape(5, 4), expected, rtol=1e-12, atol=0)
    assert prior.sum() == pytest.approx(1.0, rel=0, abs=1e-12)
    for i, j in [(2, 1), (1, 2), (0, 0), (0, 3), (4, 0), (4, 3)]:
        assert prior.reshape(5, 4)[i, j] == pytest.approx(expected[i, j], rel=1e-12, abs=0)


def test_prior_grid_edge_halving_is_material():
    m = module()
    grid = m.ReleaseGrid(mu_points=5, sigma_points=4)
    values = m.make_grid(grid)[2].reshape(5, 4)
    sigma_nodes = np.linspace(grid.sigma_min, grid.sigma_max, grid.sigma_points)
    mu_nodes = np.linspace(grid.mu_min, grid.mu_max, grid.mu_points)
    unhalved = np.outer(np.exp(-0.5 * (mu_nodes / grid.mu_prior_sd) ** 2),
                        np.exp(-0.5 * (sigma_nodes / grid.sigma_prior_scale) ** 2))
    unhalved /= unhalved.sum()
    assert np.max(np.abs(values / unhalved - 1)) > 1e-3


def test_prior_and_posterior_match_independent_likelihood():
    m = module(); grid = m.ReleaseGrid(mu_points=11, sigma_points=9)
    post = m.fit_release_process(YEARS, VALUES, window=4, grid=grid)
    mu,sigma,prior = m.make_grid(grid)
    obs = np.diff(np.log(VALUES))[-4:]
    logw = np.log(prior) + norm.logpdf(obs[:,None],loc=mu,scale=sigma).sum(axis=0)
    expected = np.exp(logw-logsumexp(logw))
    np.testing.assert_allclose(post.weights,expected,rtol=1e-11,atol=1e-14)
    assert abs(post.weights.sum()-1)<1e-12
    assert post.n_changes==4 and post.first_change_year==2022
    assert post.last_year==2025 and post.last_value==755


def test_unit_rescaling_does_not_change_log_transition():
    m = module(); a=m.fit_release_process(YEARS,VALUES); b=m.fit_release_process(YEARS,VALUES*1000)
    np.testing.assert_allclose(a.weights,b.weights,rtol=1e-10,atol=1e-13)
    sa=m.forecast_summary(a,[1])[0]; sb=m.forecast_summary(b,[1])[0]
    assert sb['median']==pytest.approx(sa['median']*1000)


def test_no_lookahead_when_through_year_set():
    m=module(); changed=VALUES.copy(); changed[-3:]*=3
    a=m.fit_release_process(YEARS,VALUES,through_year=2022)
    b=m.fit_release_process(YEARS,changed,through_year=2022)
    np.testing.assert_array_equal(a.weights,b.weights)
    assert a.last_year==2022


@pytest.mark.parametrize('years,values', [([2020,2022,2023],[1,2,3]),([2020,2020,2021],[1,2,3]),([2020,2021,2022],[1,0,3]),([2020,2021,2022],[1,float('nan'),3]),([2020.5,2021,2022],[1,2,3]),([2020,2021],[1,2]),([2020,2021,2022],[1,2]),([True,2021,2022],[1,2,3])])
def test_bad_series_rejected(years,values):
    with pytest.raises(ValueError): module().fit_release_process(years,values)


@pytest.mark.parametrize('kw',[{'mu_points':2},{'sigma_points':True},{'sigma_min':0},{'mu_min':1},{'mu_prior_sd':0},{'sigma_prior_scale':float('nan')}])
def test_bad_grids_rejected(kw):
    with pytest.raises(ValueError): module().make_grid(module().ReleaseGrid(**kw))


@pytest.mark.parametrize('kw',[{'window':1},{'window':True},{'through_year':2011},{'through_year':2022.5}])
def test_bad_fit_configuration(kw):
    with pytest.raises(ValueError): module().fit_release_process(YEARS,VALUES,**kw)


def test_summary_matches_single_lognormal_case():
    m=module(); p=m.ReleasePosterior(np.array([-.1]),np.array([.2]),np.array([1.]),2025,755.,2022,4,4)
    s=m.forecast_summary(p,[1,3])
    for row,h in zip(s,[1,3]):
        assert row['mean']==pytest.approx(755*np.exp(-.1*h+.5*.2**2*h))
        assert row['median']==pytest.approx(755*np.exp(-.1*h))
        assert row['lower_95']==pytest.approx(755*np.exp(-.1*h+norm.ppf(.025)*.2*np.sqrt(h)))
        assert row['upper_95']==pytest.approx(755*np.exp(-.1*h+norm.ppf(.975)*.2*np.sqrt(h)))
        assert row['year']==2025+h
    assert m.log_predictive_density(p,700.)==pytest.approx(norm.logpdf(np.log(700/755),-.1,.2)-np.log(700))


def test_positive_finite_joint_paths_reproducible():
    m=module(); p=m.fit_release_process(YEARS,VALUES,window=4)
    a=m.sample_release_paths(p,5,5000,991); b=m.sample_release_paths(p,5,5000,991)
    np.testing.assert_array_equal(a['values'],b['values'])
    assert a['values'].shape==(5000,5)
    assert np.isfinite(a['values']).all() and (a['values']>0).all()
    np.testing.assert_array_equal(a['years'],np.arange(2026,2031))
    assert np.corrcoef(np.log(a['values']).T)[0,4]>.25
    expected=m.forecast_summary(p,[1])[0]['mean']
    assert a['values'][:,0].mean()==pytest.approx(expected,rel=.02)
    assert a['mu'].shape==(5000,) and a['sigma'].shape==(5000,)


def test_higher_horizons_include_shared_drift_uncertainty():
    m=module(); p=m.ReleasePosterior(np.array([-.2,.1]),np.array([.01,.01]),np.array([.5,.5]),2025,755.,2022,4,4)
    paths=m.sample_release_paths(p,2,30000,72)
    changes=np.column_stack([np.log(paths['values'][:,0]/755),np.log(paths['values'][:,1]/paths['values'][:,0])])
    assert np.corrcoef(changes.T)[0,1]>.95


@pytest.mark.parametrize('h',[0,-1,1.5,True,51])
def test_invalid_horizon(h):
    m=module(); p=m.fit_release_process(YEARS,VALUES)
    with pytest.raises(ValueError): m.forecast_summary(p,[h])


@pytest.mark.parametrize('draws',[0,-1,1.5,True])
def test_invalid_path_draws(draws):
    m=module(); p=m.fit_release_process(YEARS,VALUES)
    with pytest.raises(ValueError): m.sample_release_paths(p,2,draws,9)


def test_forecast_invalid_probability_value_and_posterior():
    m=module(); p=m.fit_release_process(YEARS,VALUES)
    for val in [0,-1,np.nan,np.inf]:
        with pytest.raises(ValueError): m.log_predictive_density(p,val)
    for weight in [np.array([-1.]),np.array([2.]),np.array([np.nan])]:
        with pytest.raises(ValueError): m.ReleasePosterior(np.array([0.]),np.array([.1]),weight,2025,755.,2022,4,4)


def hand_built_posterior(mu, sigma, weights):
    m = module()
    return m.ReleasePosterior(np.asarray(mu, float), np.asarray(sigma, float),
                              np.asarray(weights, float), 2025, 755., 2022, 4, 4)


def test_boundary_mass_is_exact_on_hand_built_posteriors():
    m = module()
    all_edge = hand_built_posterior([-1., -1., 1., 1.], [.1, .2, .1, .2], [.1, .2, .3, .4])
    assert m.boundary_mass(all_edge) == 1.0
    interior_only = hand_built_posterior([-1., 0., 1.], [.1, .2, .3], [0., 1., 0.])
    assert m.boundary_mass(interior_only) == 0.0
    mixed = hand_built_posterior([-1., 0., 1.], [.1, .2, .3], [.25, .5, .25])
    assert m.boundary_mass(mixed) == 0.5
    corner_only = hand_built_posterior([-1., 0., 1.], [.1, .2, .3], [0., 0., 1.])
    assert m.boundary_mass(corner_only) == 1.0


def test_predictive_intervals_ordered_and_fitted_boundary_mass_small():
    m=module(); p=m.fit_release_process(YEARS,VALUES,window=4)
    for s in m.forecast_summary(p,[1,2,5]):
        assert 0<s['lower_95']<s['lower_80']<s['median']<s['upper_80']<s['upper_95']
    assert m.boundary_mass(p) < 0.05


@pytest.mark.parametrize('grid', [0, 0.0, [], {}, '', False, ()])
def test_non_grid_objects_are_not_replaced_by_the_default_grid(grid):
    with pytest.raises(ValueError, match='ReleaseGrid'):
        module().fit_release_process(YEARS, VALUES, grid=grid)



def test_source_agrees_with_supplied_completion():
    m=module(); root=Path(__file__).resolve().parents[2]
    raw=(root/'data/calibration_20261024/raw/tobacco_returns_completion.txt').read_text()
    rows=m.parse_release_export(raw,list(range(2010,2026)))
    assert [r['tonnes'] for r in rows]==VALUES.tolist()


def test_remaining_input_contract_edges():
    m=module()
    for values in [[True,2,3],[],None]:
        with pytest.raises(ValueError): m.fit_release_process([2020,2021,2022],values)
    for expected in [[],[2025,2025]]:
        with pytest.raises(ValueError): m.parse_release_export('',expected)
    with pytest.raises(ValueError): m.parse_release_export(None,[2025])
    with pytest.raises(ValueError): m.make_grid({})
    with pytest.raises(ValueError): m.ReleasePosterior(np.array([0.,1.]),np.array([.1]),np.array([1.]),2025,755.,2022,4,4)
    with pytest.raises(ValueError): m.ReleasePosterior(np.array([0.]),np.array([.1]),np.array([1.]),2025,755.,2021,4,4)
