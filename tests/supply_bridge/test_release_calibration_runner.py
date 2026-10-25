"""CLI/source-integrity, config-agreement and held-out-comparison checks."""
from dataclasses import asdict, replace
from pathlib import Path
import importlib.util
import json
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'configs/calibration_v2.8.0/model.json'
DRAWS = '64'


def config():
    return json.loads(CONFIG.read_text())


def quick_grid(cfg):
    """The grid the quick CLI mode actually fits (51 mu cells, 25 sigma cells)."""
    return replace(module_grid(cfg), mu_points=51, sigma_points=25)


def module_grid(cfg):
    from tobac_supply.release_calibration import ReleaseGrid
    return ReleaseGrid(**cfg['grid'])


def test_release_calibration_runner_exists():
    assert (ROOT/'scripts/run_release_calibration.py').is_file()


def load_runner():
    spec=importlib.util.spec_from_file_location('release_runner',ROOT/'scripts/run_release_calibration.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def run_cli(target):
    cmd=[sys.executable,str(ROOT/'scripts/run_release_calibration.py'),'--out',str(target),
         '--quick','--skip-figures','--draws',DRAWS]
    return subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)


@pytest.fixture(scope='module')
def cli_output(tmp_path_factory):
    target=tmp_path_factory.mktemp('release_run')/'run'
    result=run_cli(target)
    assert result.returncode==0,result.stderr
    return target


def test_received_source_equals_accepted_series():
    result=load_runner().reconcile_sources(ROOT,config())
    assert result['rows']==16 and result['new_independent_observations']==0
    assert result['workbook_independently_read'] is False
    assert result['status']=='matched_all_rows'


def test_source_reconciliation_echoes_config_scope():
    cfg=config(); result=load_runner().reconcile_sources(ROOT,cfg)
    assert result['exclusions']==cfg['exclusions']
    assert result['unresolved']==cfg['unresolved']
    assert result['source_run_id']=='d26e9dec-6327-41f7-a08e-ff95cb3fee3a'


def test_backtest_never_trains_on_target_and_counts_match():
    mod=load_runner()
    years=np.arange(2010,2026); values=np.exp(-.05*(years-2010))*2000
    rows=mod.hindcasts(years,values,module_grid(config()),2015,2022)
    assert len(rows)==33
    assert all(r['train_end_year']==r['test_year']-1 for r in rows)
    assert sum(r['stage']=='reserved_diagnostic_2023_2025' for r in rows)==9
    assert all(r['observed_tonnes']>0 for r in rows)
    assert all(r['lower_95']<r['median']<r['upper_95'] for r in rows)


def test_cli_builds_complete_quantitative_outputs_and_rejects_reuse(tmp_path):
    target=tmp_path/'run'
    result=run_cli(target)
    assert result.returncode==0,result.stderr
    manifest=json.loads((target/'run_manifest.json').read_text())
    assert manifest['status']=='partial_empirical_reported_release_calibration'
    assert manifest['funding_recommendation'] is False and manifest['quick_mode'] is True
    assert len(manifest['files'])>=10
    assert (target/'forecast_summary.csv').is_file()
    second=run_cli(target)
    assert second.returncode!=0 and 'fresh' in second.stderr.lower()
    assert str(target) in second.stderr


def test_stage_labels_follow_the_split_arguments():
    mod=load_runner()
    years=np.arange(2010,2026); values=np.exp(-.05*(years-2010))*2000
    rows=mod.hindcasts(years,values,module_grid(config()),2016,2021)
    assert {r['stage'] for r in rows}=={'exploratory_selection_2016_2021',
                                        'reserved_diagnostic_2022_2025'}
    assert all(r['train_end_year']<r['test_year'] for r in rows)


def test_empty_window_mapping_is_honoured():
    mod=load_runner()
    years=np.arange(2010,2026); values=np.exp(-.05*(years-2010))*2000
    assert mod.hindcasts(years,values,module_grid(config()),2015,2022,windows={})==[]


def test_forecast_summary_matches_independent_fit(cli_output):
    cfg=config(); frame=pd.read_csv(cli_output/'forecast_summary.csv')
    assert sorted(frame.horizon.unique().tolist())==[1,2,3,4,5]
    assert sorted(frame.year.unique().tolist())==[2026,2027,2028,2029,2030]
    assert (frame.year==2025+frame.horizon).all()
    assert (frame.lower_95<frame['median']).all()
    assert (frame['median']<frame.upper_95).all()
    assert not frame[['mean','lower_95','lower_80','median','upper_80','upper_95']].isna().any().any()
    series=pd.read_csv(ROOT/cfg['source_table'])
    years=series.year.to_numpy(dtype=int); values=series.value.to_numpy(dtype=float)
    from tobac_supply.release_calibration import fit_release_process, forecast_summary
    expected={r['horizon']:r for r in forecast_summary(
        fit_release_process(years,values,window=4,grid=quick_grid(cfg)),
        cfg['forecast_horizons'])}
    chosen=frame[frame.model=='recent_4_changes']
    for horizon in (1,3,5):
        row=chosen[chosen.horizon==horizon].iloc[0]
        assert row['median']==pytest.approx(expected[horizon]['median'],rel=1e-9)
        assert row['lower_95']==pytest.approx(expected[horizon]['lower_95'],rel=1e-9)
        assert row['upper_95']==pytest.approx(expected[horizon]['upper_95'],rel=1e-9)


def test_receipts_echo_the_executed_config(cli_output):
    cfg=config()
    selection=json.loads((cli_output/'selection_receipt.json').read_text())
    assert selection['selection_years']==[cfg['hindcast_start'],cfg['selection_end']]
    assert selection['reserved_diagnostic_years']==cfg['reserved_diagnostic_years']
    assert selection['qualification']==cfg['selection_qualification']
    assert selection['all_candidates_retained']==list(load_runner().window_names(cfg['windows']))
    scope=json.loads((cli_output/'fit_scope.json').read_text())
    assert scope['country']==cfg['country']
    assert scope['version']==cfg['version'] and scope['analysis_date']==cfg['analysis_date']
    assert scope['observed_annual_levels']==16 and scope['observation_years']==[2010,2025]
    assert scope['fitted_likelihood']==cfg['likelihood']
    assert scope['unit']==cfg['unit'] and scope['estimand']==cfg['estimand']
    assert scope['grid_prior']==asdict(quick_grid(cfg))
    assert scope['funding_recommendation'] is False
    manifest=json.loads((cli_output/'run_manifest.json').read_text())
    assert manifest['version']==cfg['version'] and manifest['analysis_date']==cfg['analysis_date']
    assert manifest['seed']==cfg['seed'] and manifest['draws_per_model']==int(DRAWS)
    assert manifest['quick_mode'] is True and manifest['figures_generated'] is False
    assert isinstance(manifest['worktree_dirty'],bool)
    assert 'run_release_calibration.py' in manifest['command']
    if manifest['commit'] is not None:
        head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True)
        assert manifest['commit']==head.stdout.strip()
    sources={s['path'] for s in manifest['sources']}
    assert CONFIG.relative_to(ROOT).as_posix() in sources


def test_receipts_follow_an_edited_config(tmp_path):
    """Editing model.json must move the echoed fields, not just the arithmetic."""
    mod=load_runner(); cfg=config()
    root=tmp_path/'repo'
    (root/'configs/calibration_v2.8.0').mkdir(parents=True)
    for name in ('data','scripts','src'):
        (root/name).symlink_to(ROOT/name)
    cfg.update(version='9.9.9',analysis_date='2030-01-01',hindcast_start=2016,
               selection_end=2021,reserved_diagnostic_years=[2022,2023,2024,2025],
               windows=[None,3])
    (root/'configs/calibration_v2.8.0/model.json').write_text(json.dumps(cfg))
    mod.ROOT=root
    out=tmp_path/'out'
    mod.run(out,quick=True,draws=8,skip_figures=True)
    selection=json.loads((out/'selection_receipt.json').read_text())
    assert selection['selection_years']==[2016,2021]
    assert selection['reserved_diagnostic_years']==[2022,2023,2024,2025]
    assert selection['all_candidates_retained']==['all_changes','recent_3_changes']
    scope=json.loads((out/'fit_scope.json').read_text())
    assert scope['version']=='9.9.9' and scope['analysis_date']=='2030-01-01'
    manifest=json.loads((out/'run_manifest.json').read_text())
    assert manifest['version']=='9.9.9' and manifest['analysis_date']=='2030-01-01'
    checks=pd.read_csv(out/'rolling_predictive_checks.csv')
    assert set(checks.stage)=={'exploratory_selection_2016_2021','reserved_diagnostic_2022_2025'}
    assert sorted(checks.test_year.unique().tolist())==list(range(2016,2026))


def test_interval_score_penalises_misses():
    score=load_runner().interval_score
    assert score(5,0,10,.05)==10
    assert score(-1,0,10,.05)==50
    assert score(11,0,10,.05)==50


@pytest.mark.parametrize('alpha',[0,1,-.05,1.5,float('nan')])
def test_interval_score_rejects_alpha_outside_the_open_unit_interval(alpha):
    with pytest.raises(ValueError,match='alpha must be in'):
        load_runner().interval_score(5,0,10,alpha)


def test_absolute_percentage_error_matches_definition():
    error=load_runner().absolute_percentage_error
    assert error(200,250)==25
    assert error(200,150)==25


@pytest.mark.parametrize('observed',[0,-1,float('nan'),float('-inf')])
def test_absolute_percentage_error_requires_positive_observed(observed):
    with pytest.raises(ValueError,match='observed must be > 0'):
        load_runner().absolute_percentage_error(observed,10)


def test_duplicate_window_specs_are_rejected():
    with pytest.raises(ValueError,match='2 windows but 1'):
        load_runner().configured_windows({'windows':[4,4]})
    with pytest.raises(ValueError,match='3 windows but 2'):
        load_runner().configured_windows({'windows':[None,4,4]})
