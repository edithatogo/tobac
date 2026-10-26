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
    manifest = json.loads((ROOT / 'integration/prior_work_manifest.json').read_text())
    assert result['status'] == 'pass'
    assert result['files'] == 19
    assert result['files'] == len(manifest['files'])
    # The 298-row total is a golden number that is also restated in the receipts and
    # docs; asserting it against the verifier's own recount of the ACTUAL files (not
    # the manifest's rows fields) breaks a coordinated file+manifest drift: changing
    # both files and manifest in lockstep still has to match this literal.
    expected_rows = sum(f.get('rows', 0) for f in manifest['files'] if f['path'].endswith('.csv'))
    assert result['csv_rows'] == expected_rows == 298
    assert result['bibliography_records'] == 28
    assert result['bibliography_records'] == len(manifest['source_ids'])
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


@pytest.mark.parametrize('change,message', [
    (lambda d: d.update(automatically_conditions_live_model=True),
     'overstated incorporation scope'),
    (lambda d: d.update(new_raw_assays=1), None),
    (lambda d: d.update(supplier_quotes_received_by_this_import=1), None),
    (lambda d: d.update(bibliographic_validation_performed=True),
     'overstated incorporation scope'),
    (lambda d: d.update(schema='other'), 'overstated incorporation scope'),
    (lambda d: d.update(files=[]), 'Missing file inventory'),
    (lambda d: d['files'].append(d['files'][0].copy()), 'Duplicate file inventory entry'),
    (lambda d: d['files'][0].update(role=''), 'role, transformation or hash'),
    (lambda d: d['files'][0].update(path='../../escape'), 'Path outside declared snapshot'),
    (lambda d: d['files'][0].update(archive_path='tobac/../../escape'), 'Path outside declared snapshot'),
    (lambda d: d['files'][0].update(sha256='invalid'), 'role, transformation or hash'),
    (lambda d: d['files'][0].update(transformation='reestimated'), 'role, transformation or hash'),
    (lambda d: d.update(unmatched_source_tokens=[]), None),
])
def test_malformed_or_overclaiming_manifest_fails(snapshot, change, message):
    edit_manifest(snapshot, change)
    if message is None:
        with pytest.raises(ValueError): load().verify(snapshot)
    else:
        with pytest.raises(ValueError, match=message): load().verify(snapshot)


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
