"""The advisory lane must not downgrade unresolved imports or syntax errors."""

import importlib.util
import json
from pathlib import Path

import pytest


def test_observed_checker_failure_codes_are_fatal() -> None:
    path = Path(__file__).resolve().parents[2] / "scripts" / "advisory_types.py"
    spec = importlib.util.spec_from_file_location("advisory_types", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    codes = ["unresolved-import", "missing-import", "invalid-syntax", "parse-error"]
    assert module.fatal_codes([*codes, "invalid-assignment"]) == codes


def load_advisory():
    path = Path(__file__).resolve().parents[2] / "scripts" / "advisory_types.py"
    spec = importlib.util.spec_from_file_location("advisory_test_subject", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ty_report(*, code="invalid-assignment", severity="error", line=5):
    return {
        "version": "2.1.0",
        "runs": [
            {
                "results": [
                    {
                        "ruleId": code,
                        "level": severity,
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {"uri": "src/tobac/supply.py"},
                                    "region": {"startLine": line},
                                }
                            }
                        ],
                    }
                ]
            }
        ],
    }


def pyrefly_report(*, code="bad-assignment", severity="error", line=5):
    return {"errors": [{"path": "src/tobac/supply.py", "line": line, "name": code, "severity": severity}]}


def test_checker_reports_preserve_overlap_and_unique_findings() -> None:

    m = load_advisory()
    ty = m.parse_report("ty", json.dumps(ty_report()).encode(), 1)
    pyrefly = m.parse_report("pyrefly", json.dumps(pyrefly_report()).encode(), 1)
    comparison = m.compare({"ty": ty, "pyrefly": pyrefly})
    assert comparison["overlap_locations"] == 1
    assert comparison["tools"]["ty"]["overlap_count"] == 1
    assert comparison["tools"]["pyrefly"]["unique_count"] == 0
    other = m.parse_report("pyrefly", json.dumps(pyrefly_report(line=6)).encode(), 1)
    assert m.compare({"ty": ty, "pyrefly": other})["tools"]["ty"]["unique_count"] == 1


def test_report_failures_and_warning_exit_semantics() -> None:

    m = load_advisory()
    raw = json.dumps(ty_report()).encode()
    with pytest.raises(ValueError, match="crashed"):
        m.parse_report("ty", raw, 2)
    with pytest.raises(ValueError, match="contradicts"):
        m.parse_report("ty", raw, 0)
    with pytest.raises(json.JSONDecodeError):
        m.parse_report("ty", b"{", 1)
    warning = json.dumps(ty_report(severity="warning")).encode()
    assert m.parse_report("ty", warning, 0)[0]["severity"] == "warning"
    with pytest.raises(ValueError, match="contradicts"):
        m.parse_report("ty", warning, 1)
    with pytest.raises(ValueError, match="outside"):
        m.parse_report(
            "pyrefly",
            json.dumps(
                {"errors": [{"path": "../../outside.py", "line": 1, "name": "x", "severity": "error"}]}
            ).encode(),
            1,
        )


def test_crash_and_timeout_write_original_execution_evidence(tmp_path, monkeypatch) -> None:
    import subprocess  # noqa: PLC0415 -- Exercise the subprocess failure boundary.
    import sys  # noqa: PLC0415 -- Use the selected interpreter as the known executable.

    m = load_advisory()
    cmd = [sys.executable, "--version"]

    def crashed(*_args, **_kwargs):
        return subprocess.CompletedProcess(cmd, 7, stdout=b"partial", stderr=b"error bytes")

    monkeypatch.setattr(m.subprocess, "run", crashed)
    recorded = m.execute_checker("ty", cmd, tmp_path, {})
    assert recorded["exit_code"] == 7
    assert (tmp_path / "ty.json").read_bytes() == b"partial"
    assert json.loads((tmp_path / "ty-execution.json").read_text())["exit_code"] == 7
    with pytest.raises(ValueError, match="crashed"):
        m.parse_report("ty", b"partial", recorded["exit_code"])

    def timed_out(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd, 1, output=b"incomplete", stderr=b"timeout")

    monkeypatch.setattr(m.subprocess, "run", timed_out)
    with pytest.raises(TimeoutError, match="timed out"):
        m.execute_checker("ty", cmd, tmp_path, {})
    assert (tmp_path / "ty.json").read_bytes() == b"incomplete"
    assert json.loads((tmp_path / "ty-execution.json").read_text())["timed_out"] is True
