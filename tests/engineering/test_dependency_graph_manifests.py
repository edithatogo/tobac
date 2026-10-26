"""Guard the native graph fetcher's manifest boundary and canonical pin source."""
from pathlib import Path
import re
import tomllib
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

import pytest

ROOT = Path(__file__).resolve().parents[2]


def discover(path, visited=None):
    """Model the documented upstream txt/in include restriction, without executing pip."""
    visited = set() if visited is None else visited
    path = path.resolve()
    if path in visited:
        return visited
    assert path.is_relative_to(ROOT), 'manifest include must remain inside checkout'
    visited.add(path)
    for line in path.read_text().splitlines():
        if line.startswith(('-r ', '-c ')):
            child = line.split(maxsplit=1)[1]
            assert re.fullmatch(r'.*\.(txt|in)', child), f'graph cannot discover include {child}'
            discover(path.parent / child, visited)
    return visited


@pytest.mark.parametrize('manifest', ['requirements.in', 'audit.in', 'voiage.in'])
def test_graph_discovers_every_profile_input(manifest):
    files = discover(ROOT / 'engineering' / manifest)
    assert ROOT / 'engineering/reference-requirements.txt' in files
    assert all(p.is_file() for p in files)


def test_legacy_entrypoint_points_to_one_canonical_pin_source():
    lines = [line for line in (ROOT / 'requirements.lock').read_text().splitlines()
             if line and not line.startswith('#')]
    assert lines == ['-r engineering/reference-requirements.txt']
    assert (ROOT / '.python-version').read_text().strip() == '3.15.1'


def test_canonical_pins_are_unique_and_satisfy_declared_runtime_dependencies():
    pins = {}
    for line in (ROOT / 'engineering/reference-requirements.txt').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        requirement = Requirement(line)
        name = canonicalize_name(requirement.name)
        assert name not in pins, 'ambiguous duplicate reference pin'
        specifier, = requirement.specifier
        assert specifier.operator == '==' and '*' not in specifier.version
        pins[name] = specifier.version
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']
    declared = project['dependencies'] + [dep for group in project['optional-dependencies'].values() for dep in group]
    for text in declared:
        requirement = Requirement(text)
        assert pins[canonicalize_name(requirement.name)] in requirement.specifier


@pytest.mark.parametrize('manifest', ['voiage.in', 'ecosystem.in'])
def test_polars_profile_pin_matches_canonical_requirement(manifest):
    """An optional profile must not silently restore an older Polars runtime."""
    def polars_pin(path):
        requirements = [Requirement(line) for line in path.read_text().splitlines()
                        if line and not line.startswith(('#', '-'))]
        return [str(item.specifier) for item in requirements
                if canonicalize_name(item.name) == 'polars']
    canonical = polars_pin(ROOT / 'engineering/reference-requirements.txt')
    assert len(canonical) == 1
    assert polars_pin(ROOT / 'engineering' / manifest) == canonical
