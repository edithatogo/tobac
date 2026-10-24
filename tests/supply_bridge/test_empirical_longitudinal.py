"""Independent numerical, source and identification tests."""
import importlib.util
import math
from dataclasses import replace
import numpy as np
import pytest
from scipy.stats import multivariate_normal

@pytest.fixture
def module():
    spec=importlib.util.find_spec('tobac_supply.empirical_longitudinal')
    assert spec is not None, 'empirical longitudinal implementation is missing'
    from tobac_supply import empirical_longitudinal
    return empirical_longitudinal


def test_interval_reconstruction_is_explicit(module):
    r=module.reconstruct_interval(80.,125.,1.25)
    assert r['median_proxy']==pytest.approx(80.)
    assert r['log_se']==pytest.approx(math.log(125/80)/3.919927969080108)
    assert r['is_published_point_estimate'] is False

@pytest.mark.parametrize('a,b,u',[(0,1,1),(2,1,1),(1,1,1),(1,2,0),(1,np.inf,1),(True,2,1)])
def test_bad_interval(module,a,b,u):
    with pytest.raises(ValueError): module.reconstruct_interval(a,b,u)


def test_gaussian_conditioning_matches_direct_matrix(module):
    times=np.array([0.,1.,2.]);obs=np.array([-.1,-.2,-.1]);se=np.array([.1,.1,.2])
    spec=module.TemporalSpec(process_grid=(.05,),intensity_cv=0,alignment_cv=0)
    fit=module.fit_temporal(times,obs,se,spec)
    result=module.posterior_components(fit,[0.,1.,2.,3.])
    K=module.prior_kernel(np.arange(4.),times,.05,spec)
    S=module.prior_kernel(times,times,.05,spec)+np.diag(se**2)
    expected=K@np.linalg.solve(S,obs)
    np.testing.assert_allclose(result['means'][0],expected,atol=1e-12)
    expected_cov=module.prior_kernel(np.arange(4.),np.arange(4.),.05,spec)-K@np.linalg.solve(S,K.T)
    np.testing.assert_allclose(result['covariances'][0],expected_cov,atol=1e-12)
    assert fit.log_evidence==pytest.approx(multivariate_normal.logpdf(obs,cov=S))


def test_grid_weights_and_finite_log_evidence(module):
    f=module.fit_temporal([2013,2014,2016],[-.2,-.15,-.3],[.04,.05,.08])
    assert np.isfinite(f.log_evidence)
    assert f.weights.sum()==pytest.approx(1.)
    assert (f.weights>=0).all()


def test_deterministic_sampling_preserves_joint_paths(module):
    f=module.fit_temporal([0,1,2],[-.2,-.2,-.1],[.05]*3)
    a=module.sample_temporal(f,[2,3,4],5000,4)
    b=module.sample_temporal(f,[2,3,4],5000,4)
    np.testing.assert_array_equal(a,b)
    assert np.corrcoef(a[:,1],a[:,2])[0,1]>.4


def test_forecast_uncertainty_increases(module):
    f=module.fit_temporal([0,1,2],[-.2,-.1,-.1],[.05]*3)
    c=module.posterior_components(f,[2,3,5])
    assert np.all(c['covariances'][:,2,2]>c['covariances'][:,0,0])


def test_summary_predictive_vs_latent(module):
    f=module.fit_temporal([0,1,2],[-.2,-.1,-.1],[.05]*3)
    a=module.summarise_temporal(f,[3],observation_se=0)[0]
    b=module.summarise_temporal(f,[3],observation_se=.5)[0]
    assert b['upper_95_log']-b['lower_95_log']>a['upper_95_log']-a['lower_95_log']


def test_shared_bias_does_not_average_away(module):
    paths=np.zeros((5000,4));ref=np.array([100.]*4)
    d=module.map_discrepancy(paths,ref,ref,1.23,.3,seed=42)
    np.testing.assert_allclose(d['survey_proxy'][:,0],d['survey_proxy'][:,3])
    assert np.std(np.log(d['uplift']))==pytest.approx(.3,rel=.05)
    assert d['calibrated_illicit_volume'] is False


def test_negative_discrepancy_is_not_clamped(module):
    d=module.map_discrepancy(np.full((4,2),math.log(.5)),[100.,100.],[100.,100.],1.,0.)
    assert (d['signed_gap']==-50.).all()


def test_identification_not_inferred(module):
    # Positive gaps change with legal accounting while the fitted exposure stays fixed.
    paths=np.zeros((4,2));r=[100.,100.]
    a=module.map_discrepancy(paths,r,r,1.,0.)
    b=module.map_discrepancy(paths,r,[95.,95.],1.,0.)
    np.testing.assert_allclose(a['survey_proxy'],b['survey_proxy'])
    np.testing.assert_allclose(b['signed_gap']-a['signed_gap'],5.)

@pytest.mark.parametrize('t,y,se',[
 ([0,0],[1,1],[.1,.1]),([1,0],[1,1],[.1,.1]),([0],[1],[.1]),
 ([0,1],[1],[.1,.1]),([0,1],[1,1],[.1,0]),([0,1],[1,np.nan],[.1,.1]),
])
def test_bad_observations(module,t,y,se):
    with pytest.raises(ValueError): module.fit_temporal(t,y,se)


def test_duplicate_source_ids_fail(module):
    with pytest.raises(ValueError,match='duplicate'):
        module.fit_temporal([0,1],[0,0],[.1,.1],observation_ids=['same','same'])


def test_invalid_query_and_sample_size(module):
    f=module.fit_temporal([1,2],[0,0],[.1,.1])
    with pytest.raises(ValueError): module.sample_temporal(f,[0],4,1)
    with pytest.raises(ValueError): module.sample_temporal(f,[2],True,1)


def test_prior_sensitivity_is_not_data_duplication(module):
    f=module.fit_temporal([0,1,2],[-.2,-.1,-.1],[.05]*3)
    wider=module.fit_temporal([0,1,2],[-.2,-.1,-.1],[.05]*3,replace(f.spec,intensity_cv=.3))
    assert len(f.observations)==len(wider.observations)==3
    assert module.summarise_temporal(wider,[2])[0]['sd_log']>module.summarise_temporal(f,[2])[0]['sd_log']

@pytest.mark.parametrize('kwargs',[
 {'level_sd':0.},{'slope_sd':-1},{'process_prior_scale':float('nan')},
 {'intensity_cv':-.1},{'alignment_cv':-.1},{'residual_half_life_years':-.1},
 {'process_grid':(.1,.1)},{'process_grid':(.1,-.1)},{'process_grid':()},
])
def test_bad_spec_fails_closed(module,kwargs):
    with pytest.raises(ValueError):module.TemporalSpec(**kwargs)


def test_bad_query_order_and_negative_noise(module):
    f=module.fit_temporal([0,1],[0,0],[.1,.1])
    with pytest.raises(ValueError):module.posterior_components(f,[2,1])
    with pytest.raises(ValueError):module.summarise_temporal(f,[2],observation_se=-1)
    with pytest.raises(ValueError):module.prior_kernel([-1],[0],.1,f.spec)


def test_bad_discrepancy_and_overflow(module):
    with pytest.raises(ValueError):module.map_discrepancy(np.zeros((1,2)),[1],[1],1,0)
    with pytest.raises(ValueError):module.map_discrepancy(np.zeros((1,1)),[1],[-1],1,0)
    with pytest.raises(ValueError):module.map_discrepancy(np.zeros((1,1)),[1],[1],1,-.1)
    with pytest.raises(ValueError):module.map_discrepancy(np.full((1,1),1000.),[1],[1],1,0)


def test_temporal_dependence_uses_elapsed_time(module):
    spec=module.TemporalSpec(alignment_cv=.15,residual_half_life_years=1.)
    c=module.observation_covariance(np.array([0.,1.,3.]),np.ones(3)*.1,spec)
    assert c[0,1]/c[0,2]==pytest.approx(4.)


def test_single_future_density_matches_normal_component(module):
    spec=module.TemporalSpec(process_grid=(.1,),intensity_cv=0,alignment_cv=0)
    f=module.fit_temporal([0,1],[0.,0.],[.1,.1],spec)
    c=module.posterior_components(f,[2])
    value=.15
    expected=multivariate_normal.logpdf([value],mean=c['means'][0],cov=c['covariances'][0]+.2**2)
    assert module.predictive_log_density(f,2,value,.2)==pytest.approx(expected)
