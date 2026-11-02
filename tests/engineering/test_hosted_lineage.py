"""Hosted evidence must authenticate real native acceptance before a workload starts."""

from __future__ import annotations

import json
import shutil
lazy from pathlib import Path

import pytest

from scripts import hosted_lineage as hosted


def copied_root(tmp_path: Path) -> Path:
    """Copy only public inputs and signed evidence into an isolated checkout shape."""
    root = tmp_path / "checkout"
    capsule = hosted.authenticate(hosted.ROOT)
    names = set(capsule["pins"]) | {
        hosted.CAPSULE,
        hosted.CAPSULE + ".sig",
        hosted.SIGNERS,
        "scripts/hosted_lineage.py",
    }
    for pattern in ("configs/**/*", "data/**/*", "evidence/**/*", "src/**/*.py", "scripts/run_*.py"):
        names.update(
            p.relative_to(hosted.ROOT).as_posix()
            for p in hosted.ROOT.glob(pattern)
            if p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store"
        )
    for run in capsule["runners"].values():
        names.update(run["executed_input_objects"])
    for name in names:
        destination = root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(hosted.ROOT / name, destination)
    return root


def test_actual_signed_native_acceptance_and_all_inputs() -> None:
    """All eight native closures qualify without exposing their original payload bytes."""
    capsule = hosted.authenticate(hosted.ROOT)
    result = hosted.verify_inputs(hosted.ROOT, capsule, [])
    assert result["success"]
    assert len(result["runners"]) == 8
    assert sum(r["verified_outputs"] for r in result["runners"].values()) == 140
    assert capsule["native_readback"]["success"] is True


@pytest.mark.parametrize(
    "case", ["missing", "signature", "payload", "source", "inventory", "runtime", "authority"]
)
def test_rejection_precedes_hosted_workload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, case: str
) -> None:
    """Missing, stale or tampered material cannot claim workload execution."""
    root = copied_root(tmp_path)
    if case == "missing":
        (root / hosted.CAPSULE).unlink()
    elif case == "signature":
        (root / (hosted.CAPSULE + ".sig")).write_bytes(b"substituted signature")
    elif case == "payload":
        (root / hosted.CAPSULE).write_bytes(b"{}")
    elif case == "source":
        capsule = hosted.authenticate(root)
        name = next(iter(capsule["runners"]["m1"]["executed_input_objects"]))
        (root / name).write_bytes(b"changed scientific input")
    elif case == "inventory":
        (root / "data/unreviewed.csv").write_bytes(b"new source")
    elif case == "runtime":
        monkeypatch.setattr(hosted, "runtime_profile", lambda: {"python_sha256": "substituted"})
    else:
        (root / hosted.SIGNERS).write_bytes(b"different authority")
    monkeypatch.setattr(hosted.sys, "prefix", str(root / ".venv"))
    marker = root / "workload-started"

    def workload() -> None:
        hosted.verify(root, ["m1"])
        marker.write_bytes(b"started")

    reasons = {
        "missing": "Missing hosted lineage input",
        "signature": "signature rejected",
        "payload": "signature rejected",
        "source": "stale scientific input",
        "inventory": "Scientific inventory",
        "runtime": "runtime differs",
        "authority": "signing authority",
    }
    with pytest.raises((ValueError, FileNotFoundError), match=reasons[case]):
        workload()
    assert not marker.exists()


@pytest.mark.parametrize("field", ["artifacts", "originals", "executed_input_objects", "manifest"])
def test_valid_object_substitution_is_not_accepted(field: str) -> None:
    """A separately valid native object cannot replace the independently accepted identity."""
    capsule = hosted.authenticate(hosted.ROOT)
    capsule["runners"]["m1"][field] = capsule["runners"]["m2"][field]
    with pytest.raises(ValueError, match="substituted accepted native"):
        hosted.verify_inputs(hosted.ROOT, capsule, ["m1"])


def test_wrong_runner_manifest_selection(tmp_path: Path) -> None:
    """A manifest digest must agree with the explicit accepted runner selection."""
    capsule = hosted.authenticate(hosted.ROOT)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"unaccepted": True}), encoding="utf-8")
    with pytest.raises(ValueError, match="requested accepted runner"):
        hosted.verify_inputs(hosted.ROOT, capsule, ["m1"], manifest)


def test_failed_native_readback_cannot_qualify() -> None:
    """A signed declaration still requires successful native verification evidence."""
    capsule = hosted.authenticate(hosted.ROOT)
    capsule["native_readback"]["success"] = False
    with pytest.raises(ValueError, match="successful native byte verification"):
        hosted.verify_inputs(hosted.ROOT, capsule, ["m1"])


def test_alternate_executable_cannot_report_its_own_success(tmp_path: Path) -> None:
    """A valid script is rejected by executable identity before it can emit JSON."""
    executable = tmp_path / "python"
    executable.write_bytes(b"#!/bin/sh\nprintf '{\"success\":true}\\n'\n")
    with pytest.raises(ValueError, match="qualified executable bytes"):
        hosted.authenticate_interpreter(hosted.ROOT, executable)


def test_runtime_profile_substitution_is_rejected(tmp_path: Path) -> None:
    """An independently well-formed profile cannot replace the qualified runtime."""
    root = copied_root(tmp_path)
    (root / hosted.PROFILES).write_text(json.dumps({"profiles": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="profiles differ from acceptance"):
        hosted.authenticate(root)
