from pathlib import Path
import importlib.util
import json
import numpy as np
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('empirical_runner',ROOT/'scripts/run_empirical_longitudinal.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)


def test_period_alignment_changes_only_denominator():
    t=runner.source_table()
    a=runner.assembled_inputs(t,'calendar_replication')
    b=runner.assembled_inputs(t,'nominal_survey_year')
    np.testing.assert_array_equal(a.reconstruction_median,b.reconstruction_median)
    assert len(b)==11 and b.year.tolist()==list(range(2013,2024))
    assert b.matched_annual_release.iloc[-1]>a.matched_annual_release.iloc[-1]
    assert (b.log_reported_ratio<=0).all()


def test_original_negative_source_gaps_preserved():
    t=runner.source_table()
    assert t[t.year==2023].reported_signed_gap.iloc[0]<0
    assert t[t.year==2021].reported_signed_gap.iloc[0]<0


def test_published_upper_bound_not_default_mean():
    t=runner.source_table();a=runner.assembled_inputs(t)
    upper=runner.assembled_inputs(t,centre='published_upper_stress')
    assert (a.reconstruction_median<upper.reconstruction_median).all()
    assert not a.published_central_estimate.any()


def test_period_alignment_explicit_pandemic_sensitivity():
    assert runner.period(2021,'documented_collection_sensitivity')==('2020-09-01','2021-09-01')
    assert runner.period(2022,'documented_collection_sensitivity')==('2021-07-01','2022-08-01')
    with pytest.raises(ValueError):runner.period(2023,'unknown')
    with pytest.raises(ValueError):runner.assembled_inputs(runner.source_table(),centre='invented')


def test_run_refuses_existing_files(tmp_path):
    (tmp_path/'anything').write_text('do not overwrite')
    with pytest.raises(ValueError,match='empty'):runner.run(tmp_path,quick=True)


def test_pipeline_and_no_current_observation_invention(tmp_path):
    manifest=runner.run(tmp_path/'result',quick=True)
    folder=tmp_path/'result'
    scope=json.loads((folder/'fit_scope.json').read_text())
    assert manifest['funding_recommendation'] is False
    assert manifest['latest_paired_observation_year']==2023
    assert scope['current_joint_nz_posterior'] is False
    assert scope['current_assay_panel_fitted'] is False
    assert len(pd.read_csv(folder/'aligned_observations.csv'))==33
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


def test_source_input_rejects_missing_or_duplicate_year(tmp_path):
    t=runner.source_table();target=tmp_path/'data/empirical_intake_20261024'
    target.mkdir(parents=True)
    t.iloc[:-1].to_csv(target/'nz_historical_legal_supply.csv',index=False)
    with pytest.raises(ValueError,match='complete'):runner.source_table(tmp_path)


def test_source_input_rejects_unit_substitution(tmp_path):
    t=runner.source_table();t['unit']='tonnes/year';target=tmp_path/'data/empirical_intake_20261024'
    target.mkdir(parents=True);t.to_csv(target/'nz_historical_legal_supply.csv',index=False)
    with pytest.raises(ValueError,match='tonne'):runner.source_table(tmp_path)
