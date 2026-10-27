"""Security disposition gates must reject expired exceptions and unsupported closure."""

import importlib.util
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def checker():
    spec = importlib.util.spec_from_file_location(
        "security_findings", ROOT / "scripts/check_security_findings.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def finding(**changes):
    result = {
        "id": "SYNTHETIC-1",
        "owner": "fixture",
        "component": "fixture",
        "severity": "high",
        "rationale": "test fixture",
        "status": "open",
        "artifacts": [],
    }
    result.update(changes)
    return result


def test_open_findings_are_visible_failures() -> None:
    with pytest.raises(ValueError, match="Unresolved"):
        checker().validate([finding()], date(2026, 10, 26))


def test_expired_exception_cannot_hide_a_finding() -> None:
    with pytest.raises(ValueError, match="Expired"):
        checker().validate([finding(status="exception", expires="2026-10-25")], date(2026, 10, 26))


def test_closure_requires_fix_verification_artifacts() -> None:
    with pytest.raises(ValueError, match="verification"):
        checker().validate([finding(status="fixed")], date(2026, 10, 26))


def test_duplicate_ids_are_rejected() -> None:
    item = finding(status="exception", expires="2026-11-01")
    with pytest.raises(ValueError, match="Duplicate"):
        checker().validate([item, item], date(2026, 10, 26))


def test_fixed_finding_requires_matching_artifact_bytes(tmp_path) -> None:
    import hashlib  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    proof = tmp_path / "proof.json"
    proof.write_text('{"fixture":true}')
    row = finding(
        status="fixed",
        verification="synthetic test",
        artifacts=[{"path": "proof.json", "sha256": hashlib.sha256(proof.read_bytes()).hexdigest()}],
    )
    checker().validate([row], date(2026, 10, 26), tmp_path)
    proof.write_text("changed")
    with pytest.raises(ValueError, match="artifact"):
        checker().validate([row], date(2026, 10, 26), tmp_path)
