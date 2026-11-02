"""P6.1-P6.4: Qualification enforcement tests."""

import json
lazy from pathlib import Path

from scripts.qualification_check import qualification_check, run_qualification


def make_manifest(tmp_path: Path, *, complete: bool = True, tampered: bool = False) -> Path:
    """Create a test manifest."""
    manifest = {
        "schema_version": "archive-govt-nz.manifest/v1",
        "archive_id": "test-archive",
        "observations": [{"observation_id": "o1"}],
        "objects": [{"object_id": "sha256:a"}],
        "versions": [{"version_id": "v1", "observation_id": "o1"}],
        "receipts": {
            "transformations": [],
            "validations": [],
            "publications": [],
        },
        "context": {},
    }

    if tampered:
        manifest["objects"] = [{"object_id": "sha256:a"}, {"object_id": "sha256:a"}]

    if not complete:
        del manifest["receipts"]

    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2))
    return path


def test_qualified_mode_passes_complete_manifest(tmp_path: Path) -> None:
    """Complete manifest qualifies in qualified mode."""
    manifest = make_manifest(tmp_path, complete=True)
    result = run_qualification(manifest, "qualified")
    assert result["qualified"] is True
    assert result["mode"] == "qualified"
    assert result["native_lineage_qualified"] is False
    assert result["errors"] == []


def test_qualified_mode_fails_incomplete_manifest(tmp_path: Path) -> None:
    """Incomplete manifest fails in qualified mode."""
    manifest = make_manifest(tmp_path, complete=False)
    result = run_qualification(manifest, "qualified")
    assert result["qualified"] is False
    assert "missing_field:receipts" in result["errors"]
    assert result["mode"] == "fail_closed"


def test_qualified_mode_fails_tampered_manifest(tmp_path: Path) -> None:
    """Tampered manifest fails in qualified mode."""
    manifest = make_manifest(tmp_path, tampered=True)
    result = run_qualification(manifest, "qualified")
    assert result["qualified"] is False
    assert any("duplicate_object_id" in e for e in result["errors"])


def test_qualified_mode_fails_missing_manifest(tmp_path: Path) -> None:
    """Missing manifest fails in qualified mode."""
    manifest = tmp_path / "nonexistent.json"
    result = run_qualification(manifest, "qualified")
    assert result["qualified"] is False
    assert "manifest_missing" in result["errors"]


def test_exploratory_mode_unqualified(tmp_path: Path) -> None:
    """Exploratory mode produces visibly unqualified artifact."""
    manifest = make_manifest(tmp_path, complete=True)
    result = run_qualification(manifest, "exploratory")
    assert result["qualified"] is False
    assert result["native_lineage_qualified"] is False
    assert result["mode"] == "exploratory_unqualified"
    assert "Exploratory mode" in result["note"]


def test_legacy_mode_unqualified(tmp_path: Path) -> None:
    """Legacy mode produces visibly unqualified artifact."""
    manifest = make_manifest(tmp_path, complete=True)
    result = run_qualification(manifest, "legacy")
    assert result["qualified"] is False
    assert result["native_lineage_qualified"] is False
    assert result["mode"] == "legacy_unqualified"
    assert "Legacy mode" in result["note"]


def test_no_implicit_mode_fallback(tmp_path: Path) -> None:
    """Qualified mode does not fall back to exploratory."""
    manifest = make_manifest(tmp_path, complete=False)
    result = run_qualification(manifest, "qualified")
    assert result["qualified"] is False
    assert result["mode"] == "fail_closed"
    assert result["execution_mode"] == "qualified"


def test_no_automatic_waivers(tmp_path: Path) -> None:
    """Incomplete manifest cannot be waived to qualified."""
    manifest = make_manifest(tmp_path, complete=False)
    result = run_qualification(manifest, "qualified")
    assert result["qualified"] is False
    assert result["native_lineage_qualified"] is False
    assert result["scientific_qualification"] is False


def test_qualification_check_returns_error_details(tmp_path: Path) -> None:
    """Qualification check returns detailed error information."""
    manifest = make_manifest(tmp_path, complete=False)
    result = qualification_check(manifest)
    assert "errors" in result
    assert len(result["errors"]) > 0
    assert "checked_fields" in result
    assert "object_count" in result
    assert "observation_count" in result
    assert "version_count" in result
    assert "receipt_counts" in result


def test_qualification_check_no_scientific_qualification(tmp_path: Path) -> None:
    """Qualification never claims scientific qualification."""
    manifest = make_manifest(tmp_path, complete=True)
    result = qualification_check(manifest)
    assert result["scientific_qualification"] is False
    assert result["automatically_conditions_live_model"] is False


def test_runner_rejects_unregistered_sources_before_execution(tmp_path: Path, monkeypatch) -> None:
    from scripts import runner_provenance  # noqa: PLC0415 -- Exercise the execution boundary.

    def forbidden(*_args, **_kwargs):
        msg = "Runner must not execute before source validation"
        raise AssertionError(msg)

    monkeypatch.setattr(runner_provenance, "execute_runner_with_provenance", forbidden)
    import pytest  # noqa: PLC0415 -- Local negative control.

    for refs in (None, [], ["unknown"], ["tobac-7ee48855a1ed1c4b"] * 2):
        with pytest.raises(ValueError, match=r"native source|verified native"):
            runner_provenance.execute_runner_lineage(
                "m1",
                tmp_path / "config",
                tmp_path / "out",
                tmp_path / "runner",
                native_refs=refs,
            )


def test_runner_binds_verified_sources(tmp_path: Path, monkeypatch) -> None:
    from scripts import runner_provenance  # noqa: PLC0415 -- Exercise the execution boundary.

    config = tmp_path / "config"
    config.write_text("{}")
    monkeypatch.setattr(
        runner_provenance,
        "execute_runner_with_provenance",
        lambda *_args, **_kwargs: {"status": "completed"},
    )
    monkeypatch.setattr(runner_provenance, "readback_sources", lambda *_args: None)
    source = "tobac-7ee48855a1ed1c4b"
    result = runner_provenance.execute_runner_lineage(
        "m1",
        config,
        tmp_path / "out",
        tmp_path / "runner",
        native_refs=[source],
    )
    assert result["source_registrations"][source][0]["object_id"].startswith("sha256:")
    assert result["native_lineage_qualified"] is False


def test_runner_readback_requires_native_artifacts() -> None:
    import pytest  # noqa: PLC0415 -- Negative control.

    from scripts.runner_provenance import readback_sources  # noqa: PLC0415 -- Optional native boundary.

    with pytest.raises(ValueError, match="Native store and pinned producer wheel"):
        readback_sources({}, None, None)
