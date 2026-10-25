from pathlib import Path
import importlib.util
import json
import numpy as np
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('empirical_runner',ROOT/'scripts/run_empirical_longitudinal.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
CONFIG=ROOT/'configs/empirical_longitudinal_v2.9.0/model.json'


def test_period_alignment_changes_only_denominator():
    t=runner.source_table()
    a=runner.assembled_inputs(t,alignment='calendar_replication',centre='geometric_interval_midpoint')
    b=runner.assembled_inputs(t,alignment='nominal_survey_year',centre='geometric_interval_midpoint')
    shared=a[a.year.isin(b.year)].reset_index(drop=True)
    np.testing.assert_array_equal(shared.reconstruction_median,b.reconstruction_median)
    assert len(b)==11 and b.year.tolist()==list(range(2013,2024))
    assert b.matched_annual_release.iloc[-1]>a[a.year==2023].matched_annual_release.iloc[0]
    assert (b.log_reported_ratio<=0).all()


def test_calendar_replication_keeps_2012_but_2011_opening_windows_cannot():
    t=runner.source_table()
    calendar=runner.assembled_inputs(t,alignment='calendar_replication',centre='geometric_interval_midpoint')
    nominal=runner.assembled_inputs(t,alignment='nominal_survey_year',centre='geometric_interval_midpoint')
    assert calendar.year.tolist()==list(range(2012,2024))
    assert nominal.year.tolist()==list(range(2013,2024))
    documented=runner.assembled_inputs(t,alignment='documented_collection_sensitivity',
                                       centre='geometric_interval_midpoint')
    assert documented.year.tolist()==list(range(2013,2024))


def test_period_origin_labels_the_actual_pairing_start():
    assert runner.period_origin(2021,'documented_collection_sensitivity')=='documented_window'
    assert runner.period_origin(2019,'documented_collection_sensitivity')=='nominal_july_june_fallback'
    assert runner.period_origin(2019,'calendar_replication')=='calendar_year'
    assert runner.period_origin(2019,'nominal_survey_year')=='nominal_july_june_fallback'
    frame=runner.assembled_inputs(runner.source_table(),
                                  alignment='documented_collection_sensitivity',
                                  centre='geometric_interval_midpoint')
    assert set(frame.period_origin)=={'documented_window','nominal_july_june_fallback'}


def test_original_negative_source_gaps_preserved():
    t=runner.source_table()
    assert t[t.year==2023].reported_signed_gap.iloc[0]<0
    assert t[t.year==2021].reported_signed_gap.iloc[0]<0


def test_published_upper_bound_not_default_mean():
    t=runner.source_table()
    a=runner.assembled_inputs(t,alignment='nominal_survey_year',centre='geometric_interval_midpoint')
    upper=runner.assembled_inputs(t,alignment='nominal_survey_year',centre='published_upper_stress')
    assert (a.reconstruction_median<upper.reconstruction_median).all()
    assert not a.published_central_estimate.any()


def test_period_alignment_explicit_pandemic_sensitivity():
    # Half-open [start, end): Sep 2020-Aug 2021 and Jul 2021-Jul 2022.
    assert runner.period(2021,'documented_collection_sensitivity')==('2020-09-01','2021-09-01')
    assert runner.period(2022,'documented_collection_sensitivity')==('2021-07-01','2022-08-01')
    with pytest.raises(ValueError):runner.period(2023,'unknown')
    with pytest.raises(ValueError):
        runner.assembled_inputs(runner.source_table(),alignment='nominal_survey_year',centre='invented')
    with pytest.raises(ValueError):
        runner.assembled_inputs(runner.source_table(),alignment='invented',
                                centre='geometric_interval_midpoint')


def test_assembled_inputs_requires_both_selectors():
    t=runner.source_table()
    with pytest.raises(TypeError):
        runner.assembled_inputs(t)  # type: ignore[call-arg]


def test_run_refuses_existing_files(tmp_path):
    (tmp_path/'anything').write_text('do not overwrite')
    with pytest.raises(ValueError,match='empty'):runner.run(tmp_path,quick=True)


def test_pipeline_and_no_current_observation_invention(tmp_path):
    manifest=runner.run(tmp_path/'result',quick=True)
    folder=tmp_path/'result'
    scope=json.loads((folder/'fit_scope.json').read_text())
    cfg=json.loads(CONFIG.read_text())
    assert manifest['funding_recommendation'] is False
    assert manifest['latest_paired_observation_year']==2023
    assert scope['current_joint_nz_posterior'] is False
    assert scope['current_assay_panel_fitted'] is False
    assert scope['primary_alignment']==cfg['primary_alignment']
    assert manifest['version']==cfg['version']
    aligned=pd.read_csv(folder/'aligned_observations.csv')
    assert len(aligned)>0
    assert len(aligned[aligned.alignment==cfg['primary_alignment']])==11
    assert len(list((folder/'figures').glob('*.svg')))==5
    checks=pd.read_csv(folder/'rolling_hindcasts.csv')
    assert (checks.train_end<checks.test_year).all()
    audit=json.loads((folder/'source_audit.json').read_text())
    assert audit['source_2014_lower_count_arithmetic']['difference']!=0
    assert audit['raw_paired_nz_assays_added']==0
    assert len(pd.read_csv(folder/'fit_sensitivity.csv'))==15
    assert len(pd.read_csv(folder/'signed_discrepancy_sensitivity.csv'))==15*11
    for item in manifest['files']:
        assert runner.digest(folder/item['path'])==item['sha256']
    # The base discrepancy scenario must exist and carry finite values.
    base=f"uplift_{float(cfg['source_uplift']):g}_shared_{float(cfg['base_shared_uplift_log_sd']):g}"
    rows=pd.read_csv(folder/'signed_discrepancy_sensitivity.csv')
    base_rows=rows[rows.scenario==base]
    assert len(base_rows)==11 and base_rows.signed_gap_median.notna().all()


def test_accounting_arms_apply_the_declared_fractions_exactly(tmp_path):
    manifest=runner.run(tmp_path/'result',quick=True)
    folder=tmp_path/'result'
    cfg=json.loads(CONFIG.read_text())
    ledgers=pd.read_csv(folder/'lawful_stock_ledgers.csv')
    for fraction in cfg['unrecorded_lawful_fractions_of_releases']:
        if not fraction: continue
        name=f'unrecorded{fraction*100:g}pct'
        rows=ledgers[ledgers.scenario==name]
        np.testing.assert_allclose(rows.lawful_unrecorded,float(fraction)*rows.release,rtol=1e-12)
        assert (rows.lawful_unrecorded>0).all()
    for visitor in cfg['net_visitor_fraction_sensitivity']:
        if not visitor: continue
        name=f'visitor_{"minus" if visitor<0 else "plus"}{abs(visitor)*100:g}pct'
        rows=ledgers[ledgers.scenario==name]
        np.testing.assert_allclose(rows.net_visitors,float(visitor)*rows.release,rtol=1e-12)
    for days in cfg['stock_days']:
        if not days: continue
        rows=ledgers[ledgers.scenario==f'stock{days:g}']
        expected=runner.stock_scenario(rows.release.to_numpy(float),float(days))
        np.testing.assert_allclose(rows.opening_stock,expected[:-1],rtol=1e-12)
        np.testing.assert_allclose(rows.closing_stock,expected[1:],rtol=1e-12)
    # Changing the unrecorded assumption must move the reported discrepancy.
    rows=pd.read_csv(folder/'signed_discrepancy_sensitivity.csv')
    small=rows[rows.scenario=='unrecorded2pct'].set_index('year').signed_gap_median
    large=rows[rows.scenario=='unrecorded5pct'].set_index('year').signed_gap_median
    assert len(small)==len(large)==11
    assert not np.allclose(small.to_numpy(),large.to_numpy())


def test_hindcast_count_and_training_end_are_pinned(tmp_path):
    runner.run(tmp_path/'result',quick=True)
    folder=tmp_path/'result'
    cfg=json.loads(CONFIG.read_text())
    checks=pd.read_csv(folder/'rolling_hindcasts.csv')
    years=list(range(cfg['hindcast_start_year'],2024))
    assert len(checks)==len(years)*3
    assert sorted(checks.test_year.unique().tolist())==years
    assert checks.train_end.max()==2022
    assert (checks.train_end<checks.test_year).all()
    assert set(checks.alignment)==set(runner.ALIGNMENTS)


def test_primary_alignment_is_propagated_to_every_derived_arm(monkeypatch,tmp_path):
    cfg=json.loads(CONFIG.read_text())
    recorded=[]
    original=runner.assembled_inputs
    def wrapper(table,**kwargs):
        recorded.append((kwargs['alignment'],kwargs['centre']))
        return original(table,**kwargs)
    monkeypatch.setattr(runner,'assembled_inputs',wrapper)
    runner.run(tmp_path/'result',quick=True)
    assert len(recorded)==6, recorded
    frames,stresses=recorded[:3],recorded[3:]
    # The three comparison frames keep their own alignment but the declared centre.
    assert {alignment for alignment,_ in frames}==set(runner.ALIGNMENTS)
    assert {centre for _,centre in frames}=={cfg['primary_centre']}
    # The centre-stress variants must use the declared primary alignment, not a
    # hardcoded nominal one.
    assert {alignment for alignment,_ in stresses}=={cfg['primary_alignment']}
    assert {centre for _,centre in stresses}=={
        'arithmetic_interval_midpoint','published_upper_stress','published_lower_stress'}


def test_config_validation_rejects_silent_scientific_inputs():
    cfg=json.loads(CONFIG.read_text())
    runner.validate_config(cfg)
    bad=dict(cfg,unrecorded_lawful_fractions_of_releases=[0.0,1.0])
    with pytest.raises(ValueError,match='strictly below'):runner.validate_config(bad)
    bad=dict(cfg,stock_days=[30,30])
    with pytest.raises(ValueError,match='duplicate'):runner.validate_config(bad)
    bad=dict(cfg,base_shared_uplift_log_sd=0.3)
    with pytest.raises(ValueError,match='base_shared_uplift_log_sd'):runner.validate_config(bad)
    bad=dict(cfg,source_uplift=1.15)
    with pytest.raises(ValueError,match='source_uplift'):runner.validate_config(bad)
    bad=dict(cfg,primary_alignment='invented')
    with pytest.raises(ValueError,match='primary_alignment'):runner.validate_config(bad)
    bad=dict(cfg,primary_centre='invented')
    with pytest.raises(ValueError,match='primary_centre'):runner.validate_config(bad)
    bad=dict(cfg,forecast_to=2024.0)
    with pytest.raises(ValueError,match='forecast_to'):runner.validate_config(bad)
    bad=dict(cfg,source_annual_days=360)
    with pytest.raises(ValueError,match='source_annual_days'):runner.validate_config(bad)
    missing=dict(cfg);missing.pop('base_shared_uplift_log_sd')
    with pytest.raises(ValueError,match='missing required keys'):runner.validate_config(missing)


def test_horizon_must_extend_past_the_last_observation():
    cfg=json.loads(CONFIG.read_text())
    runner.validate_horizon(cfg,2023)
    for forecast_to in (2023,2020,-1):
        with pytest.raises(ValueError,match='forecast_to'):
            runner.validate_horizon(dict(cfg,forecast_to=forecast_to),2023)
    with pytest.raises(ValueError,match='hindcast_start_year'):
        runner.validate_horizon(dict(cfg,hindcast_start_year=2024),2023)


def test_scenario_arms_reconcile_declared_values():
    cfg=json.loads(CONFIG.read_text())
    arms=runner.scenario_arms(cfg)
    assert len(arms)==7
    assert len({arm[0] for arm in arms})==7
    with pytest.raises(ValueError,match='duplicate'):
        runner.scenario_arms(dict(cfg,stock_days=[30,30]))
    with pytest.raises(ValueError,match='strictly below'):
        runner.scenario_arms(dict(cfg,unrecorded_lawful_fractions_of_releases=[1.2]))


def test_source_input_rejects_missing_or_duplicate_year(tmp_path):
    t=runner.source_table();target=tmp_path/'data/empirical_intake_20261024'
    target.mkdir(parents=True)
    t.iloc[:-1].to_csv(target/'nz_historical_legal_supply.csv',index=False)
    with pytest.raises(ValueError,match='complete'):runner.source_table(tmp_path)


def test_source_input_rejects_unit_substitution(tmp_path):
    t=runner.source_table();t['unit']='tonnes/year';target=tmp_path/'data/empirical_intake_20261024'
    target.mkdir(parents=True);t.to_csv(target/'nz_historical_legal_supply.csv',index=False)
    with pytest.raises(ValueError,match='tonne'):runner.source_table(tmp_path)
