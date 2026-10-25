"""Temporal numerical and provenance contracts, not empirical-validation claims."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import math
import numpy as np
import pytest


def mod():
    assert importlib.util.find_spec('tobac_supply.longitudinal') is not None, 'Temporal module missing'
    from tobac_supply import longitudinal
    return longitudinal


def rec(v, available):
    return dict(series_id='NZHS_smoking',period_start='2021-07-01',period_end='2022-08-01',
                available_on=available,source_id='official',value=v,unit='percent')


def test_vintage_selection_respects_as_of_and_does_not_double_count():
    rows=[rec(8.0,'2022-11-17'),rec(8.6,'2023-12-14')]
    assert mod().choose_vintage(rows,'2023-01-01')[0]['value']==8
    assert mod().choose_vintage(rows,'2026-10-24')[0]['value']==8.6
    assert mod().choose_vintage(rows,'2020-01-01')==[]
    assert len(rows)==2


def test_ambiguous_same_vintage_rejected():
    with pytest.raises(ValueError,match='Conflicting'):
        mod().choose_vintage([rec(8,'2023-01-01'),rec(9,'2023-01-01')],'2026-01-01')


def test_vintage_duplicate_exact_is_not_extra_evidence():
    a=rec(8,'2023-01-01')
    assert len(mod().choose_vintage([a,deepcopy(a)],'2026-01-01'))==1


def test_date_validation():
    with pytest.raises(ValueError):mod().choose_vintage([rec(8,'not-date')],'2026-01-01')
    bad=rec(8,'2023-01-01');bad['period_end']=bad['period_start']
    with pytest.raises(ValueError):mod().choose_vintage([bad],'2026-01-01')


def test_period_mix_rejected():
    a=rec(8,'2023-01-01');b=rec(8,'2024-01-01');b['unit']='tonnes'
    with pytest.raises(ValueError,match='unit'):mod().choose_vintage([a,b],'2026-01-01')


@pytest.mark.parametrize('field,value',[
    ('series_id',None),('series_id',float('nan')),('series_id',''),('series_id','   '),
    ('unit',None),('unit',float('nan')),('unit',''),('unit','  '),
])
def test_missing_identity_rejected_before_string_coercion(field,value):
    # str(None)/str(nan) would become the truthy labels 'None'/'nan' and merge
    # unrelated series, so identity is validated before conversion.
    bad=rec(8,'2023-01-01');bad[field]=value
    with pytest.raises(ValueError,match=field):mod().choose_vintage([bad],'2026-01-01')


def test_identity_surrounding_whitespace_is_normalised_not_a_new_series():
    a=rec(8,'2023-01-01');b=rec(8.5,'2024-01-01')
    b['period_start']='2022-08-01';b['period_end']='2023-07-01'
    b['series_id']=' '+b['series_id']+' '
    assert len(mod().choose_vintage([a,b],'2026-01-01'))==2
    b['unit']=' tonnes '
    with pytest.raises(ValueError,match='Incompatible unit'):
        mod().choose_vintage([a,b],'2026-01-01')



def test_calendar_correlation_uses_elapsed_days():
    c=mod().continuous_correlation([0,1,7,14],7)
    assert c[0,2]==pytest.approx(.5)
    assert c[0,3]==pytest.approx(.25)
    assert np.linalg.eigvalsh(c).min()>0


def test_equal_spacing_matches_discrete_ar1():
    n=6;rho=.5
    expected=n*n/(n+2*sum((n-k)*rho**k for k in range(1,n)))
    assert mod().effective_sample_size(range(n),1)==pytest.approx(expected)


def test_wider_spacing_increases_effective_n_for_same_stationary_mean():
    assert mod().effective_sample_size([0,30,60,90,120,150],7)>mod().effective_sample_size(range(6),7)


def test_zero_half_life_preserves_same_day_dependence():
    c=mod().continuous_correlation([0,0,1],0)
    assert c[0,1]==1 and c[0,2]==0


def test_common_error_floor_is_not_removed_by_more_days():
    c=mod().log_observation_covariance(np.arange(100)*30,.25,.15,.5,7)
    v=mod().contrast_log_se(c,np.ones(100)/100)**2
    assert v>math.log1p(.5**2)


def test_stable_common_calibration_cancels_in_log_change():
    t=[0,30]
    a=mod().log_observation_covariance(t,.25,.15,0,7)
    b=mod().log_observation_covariance(t,.25,.15,.5,7)
    assert mod().contrast_log_se(a,[-1,1])==pytest.approx(mod().contrast_log_se(b,[-1,1]))


@pytest.mark.parametrize('days,half', [([],7),([0,float('nan')],7),([0,1],-1),([0,True],7)])
def test_invalid_dates_and_half_life(days,half):
    with pytest.raises(ValueError):mod().continuous_correlation(days,half)


@pytest.mark.parametrize('cv',[float('nan'),-1,True])
def test_invalid_cv(cv):
    with pytest.raises(ValueError):mod().log_observation_covariance([0,1],cv,.1,.3,7)


def test_bad_covariance_rejected():
    for a in [np.array([[1,2],[2,1]]),np.array([[1,0],[1,1]]),np.array([[np.nan]])]:
        with pytest.raises(ValueError):mod().contrast_log_se(a,np.ones(a.shape[0]))
    with pytest.raises(ValueError):mod().contrast_log_se(np.eye(2),[1])


def test_annual_overlap_respects_leap_year():
    result=mod().aggregate_uniform_years({2023:365,2024:366},'2023-07-01','2024-07-01')
    assert result['value']==366
    assert result['status']=='uniform_within_year_allocation_assumption'
    assert result['covered_days']==366


def test_missing_annual_supply_raises_not_zero_filled():
    with pytest.raises(ValueError,match='Missing'):mod().aggregate_uniform_years({2023:365},'2023-07-01','2024-07-01')
    with pytest.raises(ValueError):mod().aggregate_uniform_years({2023:-1},'2023-01-01','2024-01-01')
    with pytest.raises(ValueError):mod().aggregate_uniform_years({2023:1},'2024-01-01','2023-01-01')


def test_loglinear_hindcast_predicts_exponential_and_no_future_fit():
    y=np.arange(2010,2018);v=100*np.exp(-.1*(y-2010))
    rows=mod().rolling_origin_forecasts(y,v,min_train=4)
    assert len(rows)==4
    for r in rows: assert r['predicted']==pytest.approx(r['observed'])
    v[-1]*=2
    changed=mod().rolling_origin_forecasts(y,v,min_train=4)
    assert changed[-1]['predicted']==pytest.approx(rows[-1]['predicted'])
    assert all(r['train_end']<r['test_year'] for r in rows)


def test_last_observation_reference_and_window():
    rows=mod().rolling_origin_forecasts([2010,2012,2015,2016],[20,18,16,15],min_train=2,method='last')
    assert [r['predicted'] for r in rows]==[18,16]
    assert len(mod().rolling_origin_forecasts(range(10),np.arange(10)+1,window=3,min_train=4))==6


def test_window_counts_training_rows_not_calendar_years():
    years=[2000,2001,2010,2011,2012,2013];vals=[50,51,52,53,54,55]
    rows=mod().rolling_origin_forecasts(years,vals,min_train=4,window=3)
    assert [(r['train_n'],r['train_start'],r['train_end']) for r in rows]==[
        (3,2001.,2011.),(3,2010.,2012.)]
    # Three rows spanning ten calendar years, so window is not a year width.
    assert rows[0]['train_end']-rows[0]['train_start']==10.


def test_error_field_is_predicted_minus_observed_not_residual():
    over=mod().rolling_origin_forecasts([2020,2021,2022],[10.,20.,15.],
                                        min_train=2,method='last')
    assert over[0]['predicted']==20. and over[0]['observed']==15.
    assert over[0]['error']==pytest.approx(5.)      # over-prediction is positive
    under=mod().rolling_origin_forecasts([2020,2021,2022],[10.,20.,28.],
                                         min_train=2,method='last')
    assert under[0]['error']==pytest.approx(-8.)    # under-prediction is negative
    for row in over+under:
        assert row['error']==pytest.approx(row['predicted']-row['observed'])


@pytest.mark.parametrize('min_train',[3,4,9])
def test_too_few_observations_raises_not_empty_hindcast(min_train):
    with pytest.raises(ValueError,match='requires at least'):
        mod().rolling_origin_forecasts([2000,2001,2002],[10,11,12],min_train=min_train)



@pytest.mark.parametrize('years,vals,kwargs', [([1,1,2],[1,2,3],{}),([1,2,3],[1,0,3],{}),([1,2],[1],{}),([1,2,3],[1,2,3],{'method':'magic'}),([1,2,3],[1,2,3],{'min_train':True}),([1,2,3],[1,2,3],{'window':1})])
def test_invalid_hindcast(years,vals,kwargs):
    with pytest.raises(ValueError):mod().rolling_origin_forecasts(years,vals,**kwargs)


def test_time_bridge_reproduces_declared_reference_width_and_grows():
    m=mod();ref=m.time_bridge(583,3.23,3.23,.35,.15,.5)
    oldvar=math.log1p(.35**2)+math.log1p(.15**2)
    assert ref['log_variance']==pytest.approx(oldvar)
    assert ref['mean']==583
    assert m.time_bridge(583,6,3.23,.35,.15,.5)['log_variance']>ref['log_variance']
    assert m.time_bridge(583,0,3.23,.35,.15,.5)['log_variance']==pytest.approx(math.log1p(.15**2))
    assert ref['status']=='time_indexed_planning_distribution_not_fitted'


def test_bridge_decline_is_only_declared_scenario():
    assert mod().time_bridge(100,2,3,.35,.15,.5,mean_log_slope=-.05)['mean']==pytest.approx(100*math.exp(-.1))


def test_bridge_component_split_is_pinned_field_by_field():
    m=mod();ref=m.time_bridge(100.,1.,3.,.35,.15,.5)
    variance_ref=math.log1p(.35**2)
    assert ref['process_variance_per_year']==pytest.approx(.5*variance_ref/3)
    assert ref['slope_variance']==pytest.approx(.5*variance_ref/9)
    assert ref['common_log_variance']==pytest.approx(
        ref['process_variance_per_year']*1+ref['slope_variance']*1)
    # A swapped split is a different declaration and must change both components.
    swapped=m.time_bridge(100.,1.,3.,.35,.15,.25)
    assert swapped['process_variance_per_year']==pytest.approx(.75*variance_ref/3)
    assert swapped['slope_variance']==pytest.approx(.25*variance_ref/9)
    assert abs(.25*variance_ref/3-swapped['process_variance_per_year'])>1e-12
    assert abs(.75*variance_ref/9-swapped['slope_variance'])>1e-12
    assert swapped['process_variance_per_year']!=ref['process_variance_per_year']
    assert swapped['slope_variance']!=ref['slope_variance']


def test_bridge_zero_drift_fraction_removes_slope_and_one_removes_process():
    m=mod();variance_ref=math.log1p(.35**2)
    no_slope=m.time_bridge(100.,2.,3.,.35,.15,0.)
    assert no_slope['slope_variance']==0.
    assert no_slope['process_variance_per_year']==pytest.approx(variance_ref/3)
    no_process=m.time_bridge(100.,2.,3.,.35,.15,1.)
    assert no_process['process_variance_per_year']==0.
    assert no_process['slope_variance']==pytest.approx(variance_ref/9)


def test_bridge_two_horizons_reproduces_hand_computed_variance():
    m=mod();horizon=3.
    ref=m.time_bridge(100.,2*horizon,horizon,.35,.15,.5)
    common=(ref['process_variance_per_year']*2*horizon
            +ref['slope_variance']*(2*horizon)**2)
    assert ref['common_log_variance']==pytest.approx(common)
    variance_ref=math.log1p(.35**2)
    # Hand computation: q=0.5*v/3 and s2=0.5*v/9 give 3*v at t=6.
    assert ref['common_log_variance']==pytest.approx(3*variance_ref)
    assert ref['log_variance']==pytest.approx(
        3*variance_ref+math.log1p(.15**2))



@pytest.mark.parametrize('args',[(0,1,3,.35,.15,.5),(1,-1,3,.35,.15,.5),(1,1,0,.35,.15,.5),(1,1,3,.35,.15,2)])
def test_invalid_bridge(args):
    with pytest.raises(ValueError):mod().time_bridge(*args)
