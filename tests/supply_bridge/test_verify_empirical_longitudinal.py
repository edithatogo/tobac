"""The verifier must fail closed; a manifest that lists fewer files is not a pass."""
from pathlib import Path
import importlib.util
import json
import shutil

import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('empirical_runner',ROOT/'scripts/run_empirical_longitudinal.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
vspec=importlib.util.spec_from_file_location(
    'empirical_verify',ROOT/'scripts/verify_empirical_longitudinal.py')
verifier=importlib.util.module_from_spec(vspec);vspec.loader.exec_module(verifier)


@pytest.fixture
def run_dir(tmp_path):
    runner.run(tmp_path/'result',quick=True)
    return tmp_path/'result'


def test_verifier_passes_a_complete_run(run_dir):
    result=verifier.verify(run_dir)
    assert result['status']=='pass',result['errors']
    assert result['errors']==[]

def test_missing_manifest_fails_without_raising(tmp_path):
    result=verifier.verify(tmp_path)
    assert result['status']=='fail'
    assert any('run manifest' in error for error in result['errors'])

def test_deleted_artefact_fails_even_if_manifest_is_pruned(run_dir):
    manifest=json.loads((run_dir/'run_manifest.json').read_text())
    (run_dir/'fit_sensitivity.csv').unlink()
    manifest['files']=[item for item in manifest['files']
                       if item['path']!='fit_sensitivity.csv']
    (run_dir/'run_manifest.json').write_text(json.dumps(manifest))
    result=verifier.verify(run_dir)
    assert result['status']=='fail'
    assert any('fit_sensitivity.csv' in error for error in result['errors'])

def test_tampered_artefact_fails(run_dir):
    target=run_dir/'latent_ratio_summary.csv'
    target.write_text(target.read_text().replace('historical','tampered',1))
    result=verifier.verify(run_dir)
    assert result['status']=='fail'
    assert any('Hash mismatch' in error for error in result['errors'])

def test_missing_provenance_fails(run_dir):
    manifest=json.loads((run_dir/'run_manifest.json').read_text())
    manifest.pop('commit',None);manifest.pop('command',None)
    (run_dir/'run_manifest.json').write_text(json.dumps(manifest))
    result=verifier.verify(run_dir)
    assert result['status']=='fail'
    assert sum('provenance' in error for error in result['errors'])==2

def test_path_escape_fails(run_dir,tmp_path):
    manifest=json.loads((run_dir/'run_manifest.json').read_text())
    outside=tmp_path/'outside.txt';outside.write_text('outside')
    manifest['files'].append({'path':'../outside.txt',
                              'sha256':verifier.hashlib.sha256(b'outside').hexdigest()})
    (run_dir/'run_manifest.json').write_text(json.dumps(manifest))
    result=verifier.verify(run_dir)
    assert result['status']=='fail'
    assert any('Invalid path' in error for error in result['errors'])

def test_relabelled_illicit_interpretation_fails(run_dir):
    target=run_dir/'signed_discrepancy_sensitivity.csv'
    text=target.read_text().replace('NOT_illicit_consumption','illicit_consumption')
    target.write_text(text)
    result=verifier.verify(run_dir)
    assert result['status']=='fail'
    assert any('illicit' in error for error in result['errors'])

def test_primary_alignment_mismatch_fails(run_dir):
    scope=json.loads((run_dir/'fit_scope.json').read_text())
    scope['primary_alignment']='calendar_replication'
    (run_dir/'fit_scope.json').write_text(json.dumps(scope))
    result=verifier.verify(run_dir)
    assert result['status']=='fail'
    assert any('alignment' in error for error in result['errors'])
