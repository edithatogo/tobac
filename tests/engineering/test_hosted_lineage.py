"""Hosted evidence must authenticate real native acceptance before a workload starts."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
lazy from pathlib import Path

import pytest

from scripts import hosted_lineage as hosted
from scripts import lineage_preflight as native


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


def test_new_capsule_pins_are_algorithm_qualified() -> None:
    """Identify generated content hashes explicitly in the signed format."""
    capsule = hosted.authenticate(hosted.ROOT)
    assert capsule["schema"] == "tobac.signed-native-lineage/v2"
    assert all(value.startswith("sha256:") for value in capsule["pins"].values())


@pytest.mark.parametrize("schema", ["tobac.signed-native-lineage/v3", None, {}])
def test_unknown_or_malformed_schema_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, schema: object
) -> None:
    """Unsupported versions and malformed fields fail at the schema boundary."""
    root = copied_root(tmp_path)
    capsule = json.loads((root / hosted.CAPSULE).read_bytes())
    capsule["schema"] = schema
    (root / hosted.CAPSULE).write_text(json.dumps(capsule))
    monkeypatch.setattr(hosted, "verify_signature", lambda *_args: None)
    with pytest.raises(ValueError, match="Unknown native evidence schema"):
        hosted.authenticate(root)


@pytest.mark.parametrize("schema", ["tobac.signed-native-lineage/v1", "tobac.signed-native-lineage/v2"])
def test_supported_pin_formats_enforce_the_same_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, schema: str
) -> None:
    """Exercise both representations after the separate signature boundary."""
    root = copied_root(tmp_path)
    capsule = json.loads((root / hosted.CAPSULE).read_bytes())
    raw = {name: value.removeprefix("sha256:") for name, value in capsule["pins"].items()}
    capsule["schema"] = schema
    capsule["pins"] = {
        name: "sha256:" + value if schema.endswith("/v2") else value for name, value in raw.items()
    }
    (root / hosted.CAPSULE).write_text(json.dumps(capsule))
    monkeypatch.setattr(hosted, "verify_signature", lambda *_args: None)
    assert hosted.authenticate(root)["schema"] == schema
    (root / "noxfile.py").write_bytes(b"changed workload definition")
    with pytest.raises(ValueError, match="Stale native acceptance pin"):
        hosted.authenticate(root)


@pytest.mark.parametrize("prefix", ["", "sha512:", "SHA256:", None])
def test_v2_rejects_unqualified_or_substituted_pin_algorithms(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, prefix: str | None
) -> None:
    """A versioned receipt requires its declared SHA-256 representation."""
    root = copied_root(tmp_path)
    capsule = json.loads((root / hosted.CAPSULE).read_bytes())
    capsule["schema"] = "tobac.signed-native-lineage/v2"
    capsule["pins"] = {
        "noxfile.py": prefix + hosted.digest(root / "noxfile.py") if prefix is not None else None
    }
    (root / hosted.CAPSULE).write_text(json.dumps(capsule))
    monkeypatch.setattr(hosted, "verify_signature", lambda *_args: None)
    with pytest.raises(ValueError, match="algorithm-qualified"):
        hosted.authenticate(root)


@pytest.mark.parametrize(
    "case",
    [
        "missing",
        "signature",
        "payload",
        "source",
        "methods_source",
        "methods_benchmark",
        "inventory",
        "runtime",
        "authority",
        "stage",
        "stage_context",
        "dag",
    ],
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
    elif case in {"stage", "stage_context", "dag", "methods_source", "methods_benchmark"}:
        path = {
            "stage": "scripts/run_m1_stage.py",
            "stage_context": "scripts/verify_context_stage.py",
            "dag": "workflow/Snakefile",
            "methods_source": "src/tobac/credal.py",
            "methods_benchmark": "scripts/bf2_benchmark.py",
        }[case]
        (root / path).write_bytes(b"changed admitted source")
    elif case == "inventory":
        (root / "data/unreviewed.csv").write_bytes(b"new source")
    elif case == "runtime":
        monkeypatch.setattr(hosted, "runtime_profile", lambda: {"python_sha256": "substituted"})
    else:
        (root / hosted.SIGNERS).write_bytes(b"different authority")
    if case != "runtime":
        selected_profile = next(
            p
            for p in hosted.qualified_profiles(hosted.ROOT)
            if p["system"] == hosted.platform.system() and p["machine"] == hosted.platform.machine()
        )
        monkeypatch.setattr(hosted, "runtime_profile", lambda: selected_profile)
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
        "methods_source": "Stale native acceptance pin",
        "methods_benchmark": "Stale native acceptance pin",
        "inventory": "Scientific inventory",
        "runtime": "runtime differs",
        "authority": "signing authority",
        "stage": "Stale native acceptance pin",
        "stage_context": "Stale native acceptance pin",
        "dag": "Stale native acceptance pin",
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


@pytest.mark.skipif(
    not os.environ.get("TOBAC_LINEAGE_PYTHON"),
    reason="requires the explicitly selected qualified verifier interpreter",
)
def test_configured_verifier_executes_actual_signed_input_check() -> None:
    """Exercise the selected verifier independently of the test environment's Python."""
    result = subprocess.run(  # noqa: S603 -- Explicit qualified interpreter and fixed verifier entry point.
        [os.environ["TOBAC_LINEAGE_PYTHON"], "-I", "-S", str(hosted.ROOT / "scripts/hosted_lineage.py")],
        cwd=hosted.ROOT,
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode()
    receipt = json.loads(result.stdout)
    assert receipt["success"] is True
    assert len(receipt["runners"]) == 8
    assert sum(r["verified_outputs"] for r in receipt["runners"].values()) == 140


def test_methods_acceptance_binds_reviewed_source() -> None:
    """Check exact source identities for the newly admitted finite methods."""
    record = json.loads((hosted.ROOT / native.METHODS_ACCEPTANCE).read_bytes())
    assert record["inventory_sha256"] == native.INVENTORY_SHA
    for path, expected in record["source_sha256"].items():
        assert hosted.digest(hosted.ROOT / path) == expected


def test_native_gate_rejects_changed_methods_source(tmp_path: Path) -> None:
    """Reject a content change even when scientific inventory membership agrees."""
    root = copied_root(tmp_path)
    native.checked_pins(root)
    (root / "src/tobac/credal.py").write_bytes(b"substituted finite model")
    with pytest.raises(ValueError, match="differ from the pinned source"):
        native.checked_pins(root)
