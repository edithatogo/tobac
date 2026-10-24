"""CLI/source-integrity and held-out-comparison checks."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[2]


def test_release_calibration_runner_exists():
    assert (ROOT/'scripts/run_release_calibration.py').is_file()


def load_runner():
    spec=importlib.util.spec_from_file_location('release_runner',ROOT/'scripts/run_release_calibration.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def test_received_source_equals_accepted_series():
    result=load_runner().reconcile_sources(ROOT)
    assert result['rows']==16 and result['new_independent_observations']==0
    assert result['workbook_independently_read'] is False
    assert result['status']=='matched_all_rows'


def test_backtest_never_trains_on_target_and_counts_match():
    mod=load_runner()
    import numpy as np
    from tobac_supply.release_calibration import ReleaseGrid
    years=np.arange(2010,2026); values=np.exp(-.05*(years-2010))*2000
    rows=mod.hindcasts(years,values,ReleaseGrid(mu_points=11,sigma_points=9),2015,2022)
    assert len(rows)==33
    assert all(r['train_end_year']==r['test_year']-1 for r in rows)
    assert sum(r['stage']=='reserved_diagnostic_2023_2025' for r in rows)==9
    assert all(r['observed_tonnes']>0 for r in rows)
    assert all(r['lower_95']<r['median']<r['upper_95'] for r in rows)


def test_cli_builds_complete_quantitative_outputs_and_rejects_reuse(tmp_path):
    target=tmp_path/'run'
    cmd=[sys.executable,str(ROOT/'scripts/run_release_calibration.py'),'--out',str(target),'--quick','--skip-figures','--draws','64']
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    manifest=json.loads((target/'run_manifest.json').read_text())
    assert manifest['status']=='partial_empirical_reported_release_calibration'
    assert manifest['funding_recommendation'] is False and manifest['quick_mode'] is True
    assert len(manifest['files'])>=10
    assert (target/'forecast_summary.csv').is_file()
    second=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    assert second.returncode!=0 and 'fresh' in second.stderr.lower()


def test_interval_score_penalises_misses():
    score=load_runner().interval_score
    assert score(5,0,10,.05)==10
    assert score(-1,0,10,.05)==50
    assert score(11,0,10,.05)==50
