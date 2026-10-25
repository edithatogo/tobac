"""Fail-closed checks for the release-calibration integrity verifier."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = ['forecast_summary.csv', 'predictive_scores.csv', 'rolling_predictive_checks.csv',
            'posterior_parameter_summary.csv', 'source_reconciliation.json', 'fit_scope.json']


def load_verifier():
    spec = importlib.util.spec_from_file_location(
        'release_verifier', ROOT/'scripts/verify_release_calibration.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def edit_manifest(run, mutate):
    path = run/'run_manifest.json'
    manifest = json.loads(path.read_text())
    mutate(manifest)
    path.write_text(json.dumps(manifest, indent=2))


@pytest.fixture(scope='module')
def calibration_run(tmp_path_factory):
    """One real CLI run; every test copies it before mutating."""
    target = tmp_path_factory.mktemp('verify_run')/'run'
    cmd = [sys.executable, str(ROOT/'scripts/run_release_calibration.py'), '--out',
           str(target), '--skip-figures', '--quick', '--draws', '32']
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return target


@pytest.fixture
def run_copy(calibration_run, tmp_path):
    copy = tmp_path/'run'
    shutil.copytree(calibration_run, copy)
    return copy


def test_complete_run_passes(calibration_run):
    result = load_verifier().verify(calibration_run)
    assert result['status'] == 'pass', result['errors']
    assert result['errors'] == []
    assert result['required_artifacts'] == len(REQUIRED)


def test_required_artifact_missing_from_disk_and_manifest_names_the_artifact(run_copy):
    (run_copy/'rolling_predictive_checks.csv').unlink()
    edit_manifest(run_copy, lambda m: m.__setitem__(
        'files', [f for f in m['files'] if f['path'] != 'rolling_predictive_checks.csv']))
    result = load_verifier().verify(run_copy)
    assert result['status'] == 'fail'
    assert any('rolling_predictive_checks.csv' in e for e in result['errors'])


def test_tampered_artifact_reports_hash_mismatch(run_copy):
    target = run_copy/'forecast_summary.csv'
    target.write_text(target.read_text() + 'tampered\n')
    result = load_verifier().verify(run_copy)
    assert result['status'] == 'fail'
    assert any('Hash mismatch' in e and 'forecast_summary.csv' in e for e in result['errors'])


def test_manifest_without_provenance_fails(run_copy):
    def drop(manifest):
        del manifest['commit']
        del manifest['command']
    edit_manifest(run_copy, drop)
    result = load_verifier().verify(run_copy)
    assert result['status'] == 'fail'
    assert any("'commit'" in e for e in result['errors'])
    assert any("'command'" in e for e in result['errors'])


def test_manifest_path_escaping_the_root_fails(run_copy):
    (run_copy.parent/'escape.csv').write_text('outside\n')
    edit_manifest(run_copy, lambda m: m['files'].append(
        {'path': '../escape.csv', 'sha256': '0'*64}))
    result = load_verifier().verify(run_copy)
    assert result['status'] == 'fail'
    assert any('../escape.csv' in e for e in result['errors'])


def test_missing_manifest_fails_instead_of_raising(tmp_path):
    empty = tmp_path/'no_manifest'
    empty.mkdir()
    result = load_verifier().verify(empty)
    assert result['status'] == 'fail'
    assert result['errors'] and 'run_manifest.json' in result['errors'][0]


def test_fit_scope_funding_flag_is_checked(run_copy):
    path = run_copy/'fit_scope.json'
    scope = json.loads(path.read_text())
    scope['funding_recommendation'] = True
    path.write_text(json.dumps(scope, indent=2))
    result = load_verifier().verify(run_copy)
    assert result['status'] == 'fail'
    assert any('fit_scope' in e and 'funding' in e for e in result['errors'])
