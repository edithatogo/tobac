"""Native dependency snapshots must retain all pinned packages without inventing edges."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def module():
    spec = importlib.util.spec_from_file_location(
        "dependency_snapshot", ROOT / "scripts/dependency_snapshot.py"
    )
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_exact_resolved_pins_and_purl_encoding(tmp_path) -> None:
    path = tmp_path / "example.lock"
    path.write_text("numpy==2.5.4 \\\n    --hash=sha256:abc\nvoiage==2.2.0+local\n")
    result = module().packages(path)
    assert result["numpy"]["package_url"] == "pkg:pypi/numpy@2.5.4"
    assert result["voiage"]["package_url"] == "pkg:pypi/voiage@2.2.0%2Blocal"
    assert all("dependencies" not in item for item in result.values())


@pytest.mark.parametrize("text", ["numpy>=2", "numpy", "numpy==2\nnumpy==3\n"])
def test_ambiguous_or_unpinned_lock_is_rejected(tmp_path, text) -> None:
    path = tmp_path / "bad.lock"
    path.write_text(text)
    with pytest.raises(
        ValueError,
        match=(r"^(?:Ambiguous\ duplicate\ lock\ package|Require\ exact\ resolved\ lock\ versions)"),
    ):
        module().packages(path)


def test_all_four_verified_profiles_are_present_and_no_runtime_is_downgraded() -> None:
    import subprocess  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()  # noqa: S607 -- Fixed developer tool resolved on the qualified runner PATH.
    data = module().snapshot(head, "refs/heads/main", "synthetic-test")
    assert len(data["manifests"]) == 4
    assert data["metadata"]["python"] == "3.15.1"
    all_packages = {name for manifest in data["manifests"].values() for name in manifest["resolved"]}
    assert {
        "numpy",
        "scipy",
        "jax",
        "msgspec",
        "pyarrow",
        "patito",
        "polars",
        "pytest-gremlins",
    } <= all_packages


def test_invalid_source_identity_fails_closed() -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:Require\ Python\ 3\.15\.1\ and\ exact\ source/job\ identity)"),
    ):
        module().snapshot("short", "refs/heads/main", "test")


def test_installed_relationships_apply_markers_and_validate_constraints() -> None:
    packages = {"alpha": "1.0", "beta": "2.0", "gamma": "3.0"}
    requirements = {
        "alpha": ["beta>=2", "gamma; python_version < '3'", "gamma; extra == 'fast'"],
        "beta": [],
        "gamma": [],
    }
    assert module().installed_relationships(packages, requirements) == {
        "alpha": ["beta"],
        "beta": [],
        "gamma": [],
    }


@pytest.mark.parametrize(
    ("packages", "requirements"),
    [
        ({"alpha": "1.0"}, {"alpha": ["beta>=2"]}),
        ({"alpha": "1.0", "beta": "1.0"}, {"alpha": ["beta>=2"], "beta": []}),
        ({"Alpha": "1.0", "alpha": "1.0"}, {}),
        ({"alpha": "1.0"}, {"unknown": ["alpha"]}),
        ({"alpha": "1.0", "beta": "2.0"}, {"alpha": ["beta[fast]>=2"], "beta": []}),
        ({"alpha": "1.0", "beta": "2.0"}, {"alpha": ["beta @ https://example.org/beta.whl"], "beta": []}),
    ],
)
def test_installed_relationships_reject_inconsistent_inputs(packages, requirements) -> None:
    with pytest.raises(ValueError, match=r"Ambiguous|Unknown|missing or incompatible|Direct references"):
        module().installed_relationships(packages, requirements)


def test_installed_inventory_is_bound_to_applicable_lock_entries(tmp_path) -> None:
    path = tmp_path / "lock.txt"
    path.write_text("alpha==1.0\nbeta==2.0 ; python_version < '3'\n")
    module().verify_installed_inventory(path, {"Alpha": "1.0"})
    for wrong in ({}, {"alpha": "2.0"}, {"alpha": "1.0", "unexpected": "1.0"}):
        with pytest.raises(ValueError, match="Installed inventory"):
            module().verify_installed_inventory(path, wrong)


def test_relationships_reject_missing_metadata_owner() -> None:
    with pytest.raises(ValueError, match="metadata"):
        module().installed_relationships({"alpha": "1.0", "beta": "2.0"}, {"alpha": ["beta>=2"]})


def test_metadata_record_hash_detects_changes_and_missing_digest() -> None:
    import base64  # noqa: PLC0415
    import hashlib  # noqa: PLC0415

    data = b"Metadata-Version: 2.4\nName: example\nVersion: 1.0\n\n"
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
    module().verify_metadata_digest(data, "sha256", digest)
    for payload, algorithm, value in (
        (data + b"x", "sha256", digest),
        (data, "md5", digest),
        (data, "sha256", ""),
    ):
        with pytest.raises(ValueError, match="metadata"):
            module().verify_metadata_digest(payload, algorithm, value)
