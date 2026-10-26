"""Native dependency snapshots must retain all pinned packages without inventing edges."""
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]


def module():
    spec=importlib.util.spec_from_file_location('dependency_snapshot',ROOT/'scripts/dependency_snapshot.py')
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result


def test_exact_resolved_pins_and_purl_encoding(tmp_path):
    path=tmp_path/'example.lock';path.write_text('numpy==2.5.4 \\\n    --hash=sha256:abc\nvoiage==2.2.0+local\n')
    result=module().packages(path)
    assert result['numpy']['package_url']=='pkg:pypi/numpy@2.5.4'
    assert result['voiage']['package_url']=='pkg:pypi/voiage@2.2.0%2Blocal'
    assert all('dependencies' not in item for item in result.values())


@pytest.mark.parametrize('text',['numpy>=2','numpy','numpy==2\nnumpy==3\n'])
def test_ambiguous_or_unpinned_lock_is_rejected(tmp_path,text):
    path=tmp_path/'bad.lock';path.write_text(text)
    with pytest.raises(ValueError):module().packages(path)


def test_all_four_verified_profiles_are_present_and_no_runtime_is_downgraded():
    import subprocess
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    data=module().snapshot(head,'refs/heads/main','synthetic-test')
    assert len(data['manifests'])==4
    assert data['metadata']['python']=='3.15.1'
    all_packages={name for manifest in data['manifests'].values() for name in manifest['resolved']}
    assert {'numpy','scipy','jax','msgspec','pyarrow','patito','polars','pytest-gremlins'}<=all_packages


def test_invalid_source_identity_fails_closed():
    with pytest.raises(ValueError):module().snapshot('short','refs/heads/main','test')
