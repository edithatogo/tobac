"""Source handoff admission checks; synthetic metadata is never empirical proof."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('source_handoff', ROOT / 'scripts/source_handoff.py')


def module():
    assert SPEC and SPEC.loader
    result = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(result)
    return result


def test_current_inputs_remain_blocked_and_shared_returns_are_detected():
    report = module().build_report(ROOT)
    assert report['automatically_conditions_live_model'] is False
    assert report['scientific_qualification'] is False
    assert report['status'] == 'blocked'
    assert len(report['observations']) == 28
    rows = {r['observation_id']: r for r in report['observations']}
    supply = rows['historical-2012']
    releases = rows['releases-2012']
    assert set(supply['data_ids']) & set(releases['data_ids'])
    assert 'shared_underlying_data_requires_joint_likelihood' in releases['gaps']
    assert 'role_not_observation' in supply['gaps']
    assert 'capture_bytes_not_verified' in releases['gaps']
    assert all(not row['metadata_compatible'] for row in rows.values())


@pytest.fixture
def synthetic(tmp_path):
    """A fully declared one-row fixture for testing software compatibility only."""
    import shutil
    for name in ('source-register.json', 'source-bindings.json', 'consumer-inputs.json'):
        target = tmp_path / 'integration/archive' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / 'integration/archive' / name, target)
    manifest = json.loads((ROOT / 'integration/archive/observation-handoff.json').read_text())
    manifest['observations'] = [copy.deepcopy(manifest['observations'][0])]
    obs = manifest['observations'][0]
    manifest['target_scope_status'] = 'declared'
    manifest['target_scope']['unit'] = 'tonnes/year'
    obs.update(source_scope=dict(manifest['target_scope'], unit='tonnes/year', start=obs['period_start'], end=obs['period_end']), products=manifest['target_products'],
               likelihood_model='synthetic-joint-normal', covariance_model='synthetic-SPD',
               transport_model='synthetic matched population; no inference about NZ')
    inventories = json.loads((tmp_path / 'integration/archive/consumer-inputs.json').read_text())
    register = json.loads((tmp_path / 'integration/archive/source-register.json').read_text())
    for path in register['collection_sha256']:
        dst = tmp_path / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, dst)
    for item in inventories['inputs'] + inventories['supporting_files']:
        dst = tmp_path / item['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / item['path'], dst)
    bindings = json.loads((tmp_path / 'integration/archive/source-bindings.json').read_text())
    archive_id = next(s['archive_id'] for s in register['sources']
                      if any(r['source_id'] == obs['source_id'] for r in s['references']))
    payload = b'synthetic source, not an actual workbook'
    sha = hashlib.sha256(payload).hexdigest()
    capture = next(s for s in bindings['sources'] if s['archive_id'] == archive_id)['captures'][0]
    capture.update(status='source_workbook_values_matched', sha256=sha, captured_at='2026-10-26T00:00:00Z')
    capture['warc_sha256'] = hashlib.sha256(b'synthetic warc').hexdigest()
    capture['byte_count'] = len(payload)
    objects = tmp_path / 'objects'
    objects.mkdir()
    (objects / sha).write_bytes(payload)
    (objects / capture['warc_sha256']).write_bytes(b'synthetic warc')
    (tmp_path / 'integration/archive/source-bindings.json').write_text(json.dumps(bindings))
    return tmp_path, manifest, objects


def test_complete_synthetic_declarations_are_only_metadata_compatible(synthetic):
    root, proposal, objects = synthetic
    report = module().build_report(root, proposal, objects)
    assert report['status'] == 'metadata_compatible'
    assert report['scientific_qualification'] is False
    assert report['automatically_conditions_live_model'] is False


@pytest.mark.parametrize('role', ['forecast', 'posterior', 'assumption', 'summary'])
def test_derived_roles_cannot_become_observations(synthetic, role):
    root, proposal, objects = synthetic
    proposal['observations'][0]['role'] = role
    assert 'role_not_observation' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


def test_citation_alias_does_not_create_independent_data(synthetic):
    root, proposal, objects = synthetic
    duplicate = copy.deepcopy(proposal['observations'][0])
    duplicate['observation_id'] = 'another-citation'
    proposal['observations'].append(duplicate)
    report = module().build_report(root, proposal, objects)
    assert all('shared_underlying_data_requires_joint_likelihood' in r['gaps'] for r in report['observations'])


def test_already_conditioned_data_is_rejected(synthetic):
    root, proposal, objects = synthetic
    ids = module().build_report(root, proposal, objects)['observations'][0]['data_ids']
    proposal['used_data_ids'] = ids
    assert 'underlying_data_already_conditioned' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


@pytest.mark.parametrize('field', ['likelihood_model', 'covariance_model', 'transport_model', 'products', 'source_scope'])
def test_missing_scientific_declarations_are_not_inferred(synthetic, field):
    root, proposal, objects = synthetic
    proposal['observations'][0][field] = None
    assert not module().build_report(root, proposal, objects)['observations'][0]['metadata_compatible']


def test_period_mismatch_not_waived_by_transport_note(synthetic):
    root, proposal, objects = synthetic
    proposal['observations'][0]['period_start'] = '2009-01-01'
    assert 'observation_period_mismatch' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


@pytest.mark.parametrize('file', ['consumer-inputs.json', 'source-register.json'])
def test_source_or_input_drift_fails_closed(synthetic, file):
    root, proposal, objects = synthetic
    item = root / 'integration/archive' / file
    data = json.loads(item.read_text())
    if file == 'consumer-inputs.json':
        (root / data['inputs'][0]['path']).write_text('changed')
    else:
        (root / next(iter(data['collection_sha256']))).write_text('[]')
    with pytest.raises(ValueError, match='hash mismatch'):
        module().build_report(root, proposal, objects)


def test_capture_tampering_is_not_verified(synthetic):
    root, proposal, objects = synthetic
    for file in objects.iterdir():
        file.write_bytes(b'tampered')
    assert 'capture_bytes_not_verified' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


def test_metadata_capture_cannot_substitute_for_original(synthetic):
    root, proposal, objects = synthetic
    path = root / 'integration/archive/source-bindings.json'
    data = json.loads(path.read_text())
    for source in data['sources']:
        for capture in source['captures']:
            capture['status'] = 'metadata_only'
    path.write_text(json.dumps(data))
    assert 'original_source_capture_missing' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


def test_path_escape_and_unknown_keys_are_rejected(synthetic):
    root, proposal, objects = synthetic
    proposal['observations'][0]['path'] = '../outside.csv'
    with pytest.raises(ValueError):
        module().build_report(root, proposal, objects)
    proposal['unexpected_approval'] = True
    with pytest.raises(ValueError):
        module().build_report(root, proposal, objects)


def test_overlap_with_longer_previously_conditioned_window_is_rejected(synthetic):
    root, proposal, objects = synthetic
    proposal['used_data_ids'] = ['NZ_MOH_tobacco_returns:2009-07-01/2010-07-01']
    assert 'underlying_data_already_conditioned' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


def test_legacy_used_data_ids_require_explicit_reconciliation(synthetic):
    root, proposal, objects = synthetic
    proposal['used_data_ids'] = ['MOH:2010']
    with pytest.raises(ValueError, match='reconcile legacy IDs'):
        module().build_report(root, proposal, objects)


def test_citation_aliases_resolve_to_one_original_identity():
    aliases, _, _ = module().archive_index(ROOT)
    assert aliases[('evidence/longitudinal/references.csl.json', 'parallel-S08')] == aliases[('evidence/references.csl.json', 'phyo2025')]


def test_dependency_alias_cannot_be_marked_independent_with_a_prose_note(synthetic):
    root, proposal, objects = synthetic
    second = copy.deepcopy(proposal['observations'][0])
    second.update(observation_id='prose-asserted-independent', covariance_model='independent of first')
    proposal['observations'].append(second)
    report = module().build_report(root, proposal, objects)
    assert all('shared_underlying_data_requires_joint_likelihood' in r['gaps'] for r in report['observations'])


def test_unit_conversion_cannot_be_inferred_from_transport_prose(synthetic):
    root, proposal, objects = synthetic
    proposal['target_scope']['unit'] = 'cigarette_equivalents/year'
    assert 'unit_conversion_requires_separate_qualification' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


def test_unselected_target_scope_stays_a_gap(synthetic):
    root, proposal, objects = synthetic
    proposal['target_scope_status'] = 'proposed'
    assert 'target_scope_unqualified' in module().build_report(root, proposal, objects)['observations'][0]['gaps']


def test_used_periods_must_be_canonical_iso_dates(synthetic):
    root, proposal, objects = synthetic
    proposal['used_data_ids'] = ['NZ_MOH_tobacco_returns:20100101/20110101']
    with pytest.raises(ValueError):
        module().build_report(root, proposal, objects)
