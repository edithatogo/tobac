"""Concurrent M3 command integration, not an M3 scientific re-estimation."""

import ast
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_m3_session_retains_shared_fail_stop_evidence_contract(monkeypatch) -> None:
    path = ROOT / "tests/incorporation/test_evidence_execution.py"
    spec = importlib.util.spec_from_file_location("evidence_contract_reuse", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Reuse the same labelled Nox command double and its fail-before-setup check.
    module.test_nox_paths_run_evidence_gate_first_and_stop_on_failure(monkeypatch, "research_m3")


def test_shared_reproduction_includes_m3_without_replacing_existing_models() -> None:
    source = ast.parse((ROOT / "noxfile.py").read_text())
    function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "reproduce")
    loops = [n for n in function.body if isinstance(n, ast.For)]
    assert ast.literal_eval(loops[0].iter) == [
        ("tobac.run", "m1"),
        ("tobac.m2", "m2"),
        ("tobac.research.runner", "m3"),
    ]
    assert ast.literal_eval(loops[1].iter) == ["release_calibration", "empirical_longitudinal"]
    sessions = [n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "research_m3"]
    assert len(sessions) == 1
    calls = [ast.unparse(n) for n in sessions[0].body]
    assert any("'tests/m3', 'tests/test_workstream_integration.py'" in c for c in calls)
    assert any("'tobac.research.runner'" in c for c in calls)
    assert any("'scripts/verify.py', 'outputs/replay_m3'" in c for c in calls)
