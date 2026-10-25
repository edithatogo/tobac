"""Preservation checks do not certify the original scientific inputs."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load():
    path = ROOT / 'scripts/verify_prior_work.py'
    assert path.is_file(), 'incorporation verifier not yet implemented'
    spec = importlib.util.spec_from_file_location('verify_prior_work', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def snapshot(tmp_path):
    shutil.copytree(ROOT / 'evidence/prior_work', tmp_path / 'evidence/prior_work')
    (tmp_path / 'integration').mkdir()
    shutil.copyfile(ROOT / 'integration/prior_work_manifest.json', tmp_path / 'integration/prior_work_manifest.json')
    return tmp_path


def edit_manifest(root, change):
    path = root / 'integration/prior_work_manifest.json'
    data = json.loads(path.read_text())
    change(data)
    path.write_text(json.dumps(data))


def test_real_preserved_payload():
    result = load().verify(ROOT)
    assert result['status'] == 'pass'
    assert result['files'] == 19
    assert result['bibliography_records'] == 28
    assert result['automatically_conditions_live_model'] is False
    assert result['scope'] == 'preservation_and_internal_linkage_not_scientific_validation'


def test_missing_file_fails(snapshot):
    data = json.loads((snapshot / 'integration/prior_work_manifest.json').read_text())
    (snapshot / data['files'][0]['path']).unlink()
    with pytest.raises(ValueError, match='Missing'): load().verify(snapshot)


def test_changed_bytes_fail(snapshot):
    data = json.loads((snapshot / 'integration/prior_work_manifest.json').read_text())
    with (snapshot / data['files'][0]['path']).open('a') as f: f.write('altered')
    with pytest.raises(ValueError, match='hash'): load().verify(snapshot)


@pytest.mark.parametrize('change', [
    lambda d: d.update(automatically_conditions_live_model=True),
    lambda d: d.update(new_raw_assays=1),
    lambda d: d.update(supplier_quotes_received_by_this_import=1),
    lambda d: d.update(bibliographic_validation_performed=True),
    lambda d: d.update(schema='other'),
    lambda d: d.update(files=[]),
    lambda d: d['files'].append(d['files'][0].copy()),
    lambda d: d['files'][0].update(role=''),
    lambda d: d['files'][0].update(path='../../escape'),
    lambda d: d['files'][0].update(archive_path='tobac/../../escape'),
    lambda d: d['files'][0].update(sha256='invalid'),
    lambda d: d['files'][0].update(transformation='reestimated'),
    lambda d: d.update(unmatched_source_tokens=[]),
])
def test_malformed_or_overclaiming_manifest_fails(snapshot, change):
    edit_manifest(snapshot, change)
    with pytest.raises(ValueError): load().verify(snapshot)


def test_wrong_row_count_fails(snapshot):
    edit_manifest(snapshot, lambda d: d['files'][0].update(rows=999))
    with pytest.raises(ValueError, match='row'): load().verify(snapshot)


def test_unregistered_file_fails(snapshot):
    (snapshot / 'evidence/prior_work/v2.9.0/new-data.csv').write_text('made,up\n1,2\n')
    with pytest.raises(ValueError, match='Unregistered'): load().verify(snapshot)


def test_symlink_fails(snapshot):
    data = json.loads((snapshot / 'integration/prior_work_manifest.json').read_text())
    path = snapshot / data['files'][0]['path']
    original = path.read_bytes(); path.unlink()
    target = snapshot / 'other.csv'; target.write_bytes(original)
    try: path.symlink_to(target)
    except OSError: pytest.skip('symlink creation unavailable')
    with pytest.raises(ValueError, match='symlink'): load().verify(snapshot)


def test_cli_reports_precise_scope():
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/verify_prior_work.py'), '--root', str(ROOT)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['status'] == 'pass'


def test_archive_mismatch_fails(snapshot, tmp_path):
    archive = tmp_path / 'wrong.zip'; archive.write_bytes(b'not the source archive')
    with pytest.raises(ValueError, match='Archive hash'): load().verify(snapshot, archive)
