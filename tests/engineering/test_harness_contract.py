"""Static contracts are not proof that hosted tools have executed successfully."""
import ast
import json
from pathlib import Path
import re
import tomllib

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ('engineering.yml', 'engineering-deep.yml', 'release-candidate.yml')


@pytest.mark.parametrize('name', WORKFLOWS)
def test_new_workflows_are_pinned_read_only_and_bounded(name):
    data = yaml.load((ROOT / '.github/workflows' / name).read_text(), Loader=yaml.BaseLoader)
    assert 'pull_request_target' not in data['on']
    assert data['permissions'] == {'contents': 'read'}
    assert data['concurrency']['group']
    for job in data['jobs'].values():
        assert 0 < int(job['timeout-minutes']) <= 60
        assert 'continue-on-error' not in job
        for step in job['steps']:
            assert 'continue-on-error' not in step
            if 'uses' in step:
                assert re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+@[0-9a-f]{40}', step['uses'])
                if step['uses'].startswith('actions/checkout@'):
                    assert step['with']['persist-credentials'] == 'false'
            assert 'pull_request.title' not in step.get('run', '')
            assert 'secrets.' not in step.get('run', '')


def test_context_profiles_are_schema_valid_and_bounded():
    schema = json.loads((ROOT / 'engineering/context.schema.json').read_text())
    profiles = list((ROOT / 'engineering/context').glob('*.json'))
    assert len(profiles) >= 3
    for path in profiles:
        cfg = json.loads(path.read_text())
        Draft202012Validator(schema).validate(cfg)
        assert cfg['max_bytes'] <= 100000
        assert cfg['paths'][0] == 'AGENTS.md'
        assert 'docs/WORKSTREAM_SYNC.md' in cfg['paths']
        assert not any(x.startswith('outputs/') for x in cfg['paths'])


def test_conductor_is_upstream_pinned_not_copied():
    metadata = json.loads((ROOT / 'engineering/upstream-pins.json').read_text())
    pin = metadata['conductor']
    assert re.fullmatch('[0-9a-f]{40}', pin['commit'])
    assert pin['url'] == 'https://github.com/gemini-cli-extensions/conductor.git'
    modules = (ROOT / '.gitmodules').read_text()
    assert pin['url'] in modules and 'vendor/conductor' in modules


def test_newest_ecosystem_is_a_separate_canary_not_a_reference_overwrite():
    code = (ROOT / 'noxfile.py').read_text()
    tree = ast.parse(code)
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {'tests', 'quality', 'strict_all', 'reproduce', 'security', 'lock', 'package', 'mutation', 'profile', 'canary'} <= names
    assert 'session.python' not in code
    assert 'source-only' in code
    assert 'require-hashes' in code and '--no-build-isolation' in code
    config = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    assert config['project']['requires-python'] == '>=3.15.1,<3.16'
    assert config['project']['dependencies'] == ['numpy==2.5.4', 'scipy==1.18.1']
    assert "sys.version_info[:3] == (3, 15, 1)" in code
    strict = ast.parse(code)
    strict_session = next(n for n in strict.body if isinstance(n, ast.FunctionDef) and n.name == 'strict_all')
    strict_source = ast.unparse(strict_session)
    assert "'engineering/ruff.toml'" in strict_source
    lint = tomllib.loads((ROOT / 'engineering/ruff.toml').read_text())
    assert lint['target-version'] == 'py315'
    assert 'CPY001' in lint['lint']['ignore']
    for profile in ['basedpyright.json', 'basedpyright-all.json']:
        checker = json.loads((ROOT / 'engineering' / profile).read_text())
        assert checker['pythonVersion'] == '3.15'
    all_checker = json.loads((ROOT / 'engineering/basedpyright-all.json').read_text())
    assert all_checker['extraPaths'] == ['../src', '../scripts']


def test_renovate_does_not_automerge_scientific_changes():
    data = json.loads((ROOT / 'renovate.json').read_text())
    assert data['automerge'] is False
    assert 'helpers:pinGitHubActionDigests' in data['extends']
    assert data['minimumReleaseAge']


def test_release_requires_reviewed_lock_and_is_not_public_publication():
    text = (ROOT / '.github/workflows/release-candidate.yml').read_text()
    assert 'workflow_dispatch' in text and 'engineering/requirements.lock' in text
    assert 'id-token: write' not in text and 'pypa/gh-action-pypi-publish' not in text
    assert 'git push' not in text
