"""Real snapshot checks plus labelled tool doubles; no empirical or external qualification."""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Never

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/qualify_integrations.py"


def load():
    spec = importlib.util.spec_from_file_location("integration_qualification", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(tmp_path):
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "evidence", root / "evidence")
    (root / "integration").mkdir()
    shutil.copyfile(
        ROOT / "integration/prior_work_manifest.json", root / "integration/prior_work_manifest.json"
    )
    return root


def test_inventory_cli_checks_actual_preserved_bytes_without_external_tools(tmp_path) -> None:
    out = tmp_path / "inventory.json"
    result = subprocess.run(  # noqa: S603 -- Fixed test/qualification argv and local fixture paths; no shell.
        [sys.executable, str(SCRIPT), "--mode", "inventory", "--root", str(ROOT), "--out", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    receipt = json.loads(out.read_text())
    assert receipt["success"] is True
    assert receipt["preservation"]["files"] == 17
    assert receipt["preservation"]["csv_rows"] == 298
    assert receipt["collection_count"] >= 4
    assert receipt["record_occurrences"] >= 43
    assert receipt["external_tool_executed"] is False
    assert receipt["live_model_conditioned"] is False
    assert receipt["scientific_applicability_validated"] is False


def test_all_collections_are_inventory_occurrences_not_independent_observations() -> None:
    report = load().inventory(ROOT)
    assert report["record_occurrences"] > report["distinct_literal_ids"]
    assert "parallel-S08" in report["repeated_literal_ids"]
    assert {c["role"] for c in report["collections"]} == {
        "active_bibliography_not_observations",
        "preserved_reference_only",
    }


@pytest.mark.parametrize(
    "name",
    [
        "evidence/references.csl.json",
        "evidence/m2/references.csl.json",
        "evidence/longitudinal/references.csl.json",
        "evidence/prior_work/v2.9.0/references.csl.json",
    ],
)
def test_missing_required_collection_fails(tmp_path, name) -> None:
    root = snapshot(tmp_path)
    (root / name).unlink()
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Missing\ file:\ evidence/longitudinal/references\.csl\.json"
            r"|"
            r"Missing\ file:\ evidence/m2/references\.csl\.json"
            r"|"
            r"Missing\ file:\ evidence/prior_work/v2\.9\.0/references\.csl\.json"
            r"|"
            r"Missing\ file:\ evidence/references\.csl\.json"
            r")"
        ),
    ):
        load().inventory(root)


@pytest.mark.parametrize(
    "name",
    [
        "evidence/references.csl.json",
        "evidence/m2/references.csl.json",
        "evidence/longitudinal/references.csl.json",
        "evidence/prior_work/v2.9.0/references.csl.json",
    ],
)
def test_stored_dois_are_canonical(name) -> None:
    """Sourceright rejects non-canonical DOIs; check locally without the external binary."""
    text = (ROOT / name).read_text(encoding="utf-8")
    try:
        records = json.loads(text)
    except json.JSONDecodeError:
        records = [json.loads(likelihood) for likelihood in text.splitlines() if likelihood.strip()]
    assert records
    assert not [r["DOI"] for r in records if r.get("DOI") and r["DOI"] != r["DOI"].lower()]


def test_changed_preserved_parameters_fail_before_any_tool(tmp_path, monkeypatch) -> None:
    root = snapshot(tmp_path)
    next((root / "evidence/prior_work").rglob("parameter_estimates*.csv")).write_text("changed")
    mod = load()
    calls = []
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: calls.append(a))  # noqa: ARG005 -- Mirror the replaced callable signature in the execution double.
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Content\ hash\ mismatch:\ evidence/prior_work/v2\.9\.0/data/longitudinal"
            r"_20261024/parameter_estimates_v2\.7\.0\.csv"
            r")"
        ),
    ):
        mod.qualify_sourceright(root, all_csl=True)
    assert not calls


def test_additional_bibliography_is_discovered_not_ignored(tmp_path) -> None:
    root = snapshot(tmp_path)
    before = load().inventory(root)
    path = root / "evidence/future_fixture/references.csl.json"
    path.parent.mkdir()
    path.write_text('[{"id":"future-fixture","type":"article-journal"}]')
    report = load().inventory(root)
    assert report["collection_count"] == before["collection_count"] + 1
    assert report["record_occurrences"] == before["record_occurrences"] + 1
    assert "evidence/future_fixture/references.csl.json" in [r["path"] for r in report["collections"]]


@pytest.mark.parametrize(
    "text", ["{}", "[]", '[{"id":"x"},{"id":"x"}]', '[{"id":"x","id":"y"}]', '[{"id":false}]', "[{}]"]
)
def test_invalid_bibliography_identity_fails(tmp_path, text) -> None:
    root = snapshot(tmp_path)
    (root / "evidence/references.csl.json").write_text(text)
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Duplicate\ JSON\ key:\ id"
            r"|"
            r"Missing\ or\ duplicate\ project\ citation\ identity:\ evidence/reference"
            r"s\.csl\.json"
            r"|"
            r"Nonempty\ bibliography\ list\ required:\ evidence/references\.csl\.json"
            r")"
        ),
    ):
        load().inventory(root)


def test_symlinked_collection_is_not_followed(tmp_path) -> None:
    root = snapshot(tmp_path)
    p = root / "evidence/linked.csl.json"
    try:
        p.symlink_to(root / "evidence/references.csl.json")
    except OSError:
        pytest.skip("Host cannot create symlink fixture")
    with pytest.raises(ValueError, match="symlink"):
        load().inventory(root)


def test_symlinked_collection_directory_is_not_silently_omitted(tmp_path) -> None:
    root = snapshot(tmp_path)
    try:
        (root / "evidence/linked").symlink_to(root / "evidence/m2", target_is_directory=True)
    except OSError:
        pytest.skip("Host cannot create symlink fixture")
    with pytest.raises(ValueError, match="symlink"):
        load().inventory(root)


def tool_double(mod, tmp_path, monkeypatch, codes=None, timeout_index=None):
    """Build a labelled execution double: never used to assert real Sourceright qualification."""
    exe = tmp_path / "not-a-real-sourceright"
    exe.write_text("fixture only")
    calls = []
    monkeypatch.setattr(mod.shutil, "which", lambda name: str(exe))  # noqa: ARG005 -- Mirror the replaced callable signature in the execution double.

    def run(command, **kwargs):
        calls.append(command)
        assert command[1:3] == ["validate-csl", "--json"]
        assert kwargs["timeout"] == 120
        if len(calls) == timeout_index:
            raise subprocess.TimeoutExpired(command, 120)
        code = 0 if codes is None else codes[len(calls) - 1]
        return subprocess.CompletedProcess(command, code, "fixture stdout", "fixture stderr" if code else "")

    monkeypatch.setattr(mod.subprocess, "run", run)
    return calls


def test_external_all_csl_calls_real_command_contract_for_each_collection(tmp_path, monkeypatch) -> None:
    mod = load()
    calls = tool_double(mod, tmp_path, monkeypatch)
    result = mod.qualify_sourceright(ROOT, all_csl=True)
    assert len(calls) == len(mod.inventory(ROOT)["collections"])
    assert result["success"] is True
    assert result["external_tool_executed"] is True
    assert len(result["results"]) == len(calls)
    assert len(result["executable_sha256"]) == 64
    assert all(len(r["sha256"]) == 64 for r in result["results"])
    assert result["scientific_applicability_validated"] is False


def test_failed_collection_does_not_hide_later_checks(tmp_path, monkeypatch) -> None:
    mod = load()
    n = mod.inventory(ROOT)["collection_count"]
    calls = tool_double(mod, tmp_path, monkeypatch, codes=[1] + [0] * (n - 1))
    result = mod.qualify_sourceright(ROOT, all_csl=True)
    assert len(calls) == mod.inventory(ROOT)["collection_count"]
    assert result["success"] is False
    assert result["results"][0]["exit_code"] == 1
    assert result["results"][-1]["success"] is True


def test_timeout_does_not_hide_other_collection_results(tmp_path, monkeypatch) -> None:
    mod = load()
    calls = tool_double(mod, tmp_path, monkeypatch, timeout_index=2)
    result = mod.qualify_sourceright(ROOT, all_csl=True)
    assert len(calls) == mod.inventory(ROOT)["collection_count"]
    assert result["success"] is False
    assert result["results"][1]["error"] == "timeout"


def test_default_external_mode_retains_single_collection_compatibility(tmp_path, monkeypatch) -> None:
    mod = load()
    calls = tool_double(mod, tmp_path, monkeypatch)
    result = mod.qualify_sourceright(ROOT, all_csl=False)
    assert len(calls) == 1
    assert result["results"][0]["path"] == "evidence/references.csl.json"
    assert result["scope_selection"] == "single_legacy_collection"


def test_missing_library_is_failure_not_inventory_success(monkeypatch) -> None:
    mod = load()
    monkeypatch.setattr(mod.shutil, "which", lambda _: None)
    result = mod.qualify_sourceright(ROOT, all_csl=True)
    assert result["success"] is False
    assert result["external_tool_executed"] is False
    assert result["inventory"]["success"] is True


def test_changes_during_external_check_invalidate_receipt(tmp_path, monkeypatch) -> None:
    root = snapshot(tmp_path)
    mod = load()
    calls = tool_double(mod, tmp_path, monkeypatch)
    original = mod.subprocess.run

    def mutate(command, **kwargs):
        result = original(command, **kwargs)
        if len(calls) == 1:
            with (root / "evidence/references.csl.json").open("a") as f:
                f.write("\n")
        return result

    monkeypatch.setattr(mod.subprocess, "run", mutate)
    result = mod.qualify_sourceright(root, all_csl=True)
    assert result["success"] is False
    assert result["inputs_unchanged"] is False


def test_cli_refuses_receipt_overwrite_before_external_call(tmp_path) -> None:
    out = tmp_path / "receipt.json"
    out.write_text("previous")
    result = subprocess.run(  # noqa: S603 -- Fixed test/qualification argv and local fixture paths; no shell.
        [sys.executable, str(SCRIPT), "--mode", "inventory", "--root", str(ROOT), "--out", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert out.read_text() == "previous"


def test_inventory_success_does_not_fill_in_current_quotes_or_raw_observations() -> None:
    report = load().inventory(ROOT)
    assert report["new_raw_assays"] == 0
    assert report["supplier_quotes_received"] == 0
    assert report["bibliographic_validation_performed"] is False


@pytest.mark.parametrize("name", ["tests", "reproduce", "package", "evidence"])
def test_nox_paths_run_evidence_gate_first_and_stop_on_failure(monkeypatch, name) -> None:
    import types  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    nox = types.ModuleType("nox")
    nox.options = types.SimpleNamespace()
    nox.session = lambda f=None, **kwargs: f if f is not None else (lambda fn: fn)  # noqa: ARG005 -- Mirror the replaced callable signature in the execution double.
    command = types.ModuleType("nox.command")

    class CommandFailed(Exception):  # noqa: N818 -- Mirror Nox CommandFailed by name in the isolated execution double.
        pass

    command.CommandFailed = CommandFailed
    monkeypatch.setitem(sys.modules, "nox", nox)
    monkeypatch.setitem(sys.modules, "nox.command", command)
    spec = importlib.util.spec_from_file_location("nox_integration", ROOT / "noxfile.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    def unexpected_environment(*a, **k) -> Never:  # noqa: ARG001 -- Keep the injected fixture or execution-double call signature.
        raise AssertionError("environment ran before evidence integrity")  # noqa: EM101, TRY003 -- Synthetic failure message in an execution double.

    monkeypatch.setattr(mod, "environment", unexpected_environment)
    calls = []

    class Session:
        def run(self, *args, **kwargs) -> None:  # noqa: ARG002 -- Keep the execution-double method signature.
            calls.append(args)
            if args[:2] == ("python", "-c"):
                return
            raise CommandFailed("fixture inventory failure")  # noqa: EM101, TRY003 -- Synthetic failure message in an execution double.

    with pytest.raises(CommandFailed):
        getattr(mod, name)(Session())
    inventory = [
        call
        for call in calls
        if call[:4] == ("python", "scripts/qualify_integrations.py", "--mode", "inventory")
    ]
    assert inventory[0][-1].startswith(f"outputs/engineering/evidence-{name}-")
    assert inventory[0][-1].endswith(".json")
    if name == "evidence":
        assert calls[0][:2] == ("python", "-c")


def test_scientific_workflows_gate_preservation_and_cover_every_citation_collection() -> None:
    import yaml  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    root_workflow = yaml.load((ROOT / ".github/workflows/ci.yml").read_text(), Loader=yaml.BaseLoader)
    long_workflow = yaml.load(
        (ROOT / ".github/workflows/longitudinal.yml").read_text(), Loader=yaml.BaseLoader
    )
    for workflow, name in [(root_workflow, "numerical"), (long_workflow, "longitudinal")]:
        commands = [s["run"] for s in workflow["jobs"][name]["steps"] if "run" in s]
        inventory_at = next(
            i for i, command in enumerate(commands) if "qualify_integrations.py --mode inventory" in command
        )
        # Interpreter selection may precede inventory; installs and models may not.
        assert inventory_at < next(i for i, command in enumerate(commands) if "-m pip install" in command)
        assert not any(
            marker in command
            for command in commands[:inventory_at]
            for marker in ("-m pytest", "-m tobac.", "scripts/run_")
        )
        assert any("pytest" in c for c in commands)
        assert not any("continue-on-error" in s for s in workflow["jobs"][name]["steps"])
    commands = [s.get("run", "") for s in root_workflow["jobs"]["sourceright"]["steps"]]
    assert sum("--mode sourceright --all-csl" in c for c in commands) == 1
    assert not any("validate-csl --json evidence/m2/" in c for c in commands)


def test_bounded_evidence_context_uses_existing_schema() -> None:
    from jsonschema import Draft202012Validator  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    schema = json.loads((ROOT / "engineering/context.schema.json").read_text())
    profile = json.loads((ROOT / "engineering/context/evidence.json").read_text())
    Draft202012Validator(schema).validate(profile)
    assert "integration/prior_work_manifest.json" in profile["paths"]
    assert "docs/EVIDENCE_INTEGRATION.md" in profile["paths"]
    assert profile["base_commit"] is None
    assert profile["max_bytes"] <= 80000


def voiage_double(mod, monkeypatch, bad=None):
    """Only checks the adapter contract; not an installed voiage qualification."""
    import types  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    import numpy as np  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    package = types.ModuleType("voiage")
    analysis = types.ModuleType("voiage.analysis")
    schema = types.ModuleType("voiage.schema")
    seen = []

    class ValueArray:
        @staticmethod
        def from_numpy(values) -> object:
            return values

    class DecisionAnalysis:
        def __init__(self, values) -> None:
            self.values = values

        def evpi(self):
            seen.append(self.values.copy())
            if len(seen) == 2 and bad is not None:
                return bad
            v = self.values
            return float(np.max(v, axis=1).mean() - np.max(v.mean(axis=0)))

    schema.ValueArray = ValueArray
    analysis.DecisionAnalysis = DecisionAnalysis
    for name, item in [("voiage", package), ("voiage.analysis", analysis), ("voiage.schema", schema)]:
        monkeypatch.setitem(sys.modules, name, item)
    monkeypatch.setattr(mod.importlib.metadata, "version", lambda _: "fixture-not-installed")
    return seen


def test_existing_voiage_equal_weight_probe_retains_51_cases(monkeypatch) -> None:
    mod = load()
    seen = voiage_double(mod, monkeypatch)
    report = mod.qualify_voiage()
    assert len(seen) == 51
    assert report["cases"] == 51
    assert report["max_absolute_error"] == 0
    assert report["success"] is True
    assert report["version"] == "fixture-not-installed"


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_external_evpi_cannot_be_hidden_by_max_error(monkeypatch, bad) -> None:
    mod = load()
    voiage_double(mod, monkeypatch, bad)
    with pytest.raises(ValueError, match="Nonfinite"):
        mod.qualify_voiage()


def test_wrong_external_evpi_fails_parity(monkeypatch) -> None:
    mod = load()
    voiage_double(mod, monkeypatch, 100.0)
    report = mod.qualify_voiage()
    assert report["success"] is False


def test_external_executable_change_invalidates_validation(tmp_path, monkeypatch) -> None:
    mod = load()
    calls = tool_double(mod, tmp_path, monkeypatch)
    original = mod.subprocess.run

    def mutate(command, **kwargs):
        result = original(command, **kwargs)
        if len(calls) == 1:
            Path(command[0]).write_text("changed executable fixture", encoding="utf-8")
        return result

    monkeypatch.setattr(mod.subprocess, "run", mutate)
    result = mod.qualify_sourceright(ROOT, all_csl=True)
    assert result["success"] is False
    assert result["executable_unchanged"] is False


def test_invalid_mode_combination_fails_before_receipt(tmp_path) -> None:
    out = tmp_path / "bad.json"
    result = subprocess.run(  # noqa: S603 -- Fixed test/qualification argv and local fixture paths; no shell.
        [sys.executable, str(SCRIPT), "--mode", "inventory", "--all-csl", "--out", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert not out.exists()
