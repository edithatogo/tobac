"""Numerical reproduction must reject altered identities, shapes, nonfinite values and results."""

import hashlib
import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def checker(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return importlib.import_module("check_scientific_reproduction")


def test_reference_is_the_entire_accepted_native_csv_closure(checker) -> None:
    refs = checker.reference_tables()
    assert len(refs) == 8
    assert sum(len(tables) for tables in refs.values()) == 82


@pytest.mark.parametrize("column", ["year", "observation_id", "path_id", "state_id", "case"])
def test_numeric_identifiers_are_exact(checker, column) -> None:
    with pytest.raises(ValueError, match="identity"):
        checker.compare_cell("1", "1.0", column, relative=False)


def test_existing_numerical_tolerances_and_nonfinite_guard(checker) -> None:
    assert checker.compare_cell("1", "1.000000000001", "value", relative=False) < 1e-10
    with pytest.raises(ValueError, match="numerical"):
        checker.compare_cell("1", "1.01", "value", relative=False)
    with pytest.raises(ValueError, match="Nonfinite"):
        checker.compare_cell("nan", "nan", "value", relative=True)
    with pytest.raises(ValueError, match="text"):
        checker.compare_cell("unknown", "known", "scope", relative=False)


def test_missing_rows_and_changed_columns_fail(checker, tmp_path) -> None:
    out = tmp_path / "table.csv"
    out.write_text("year,value\n2024,1\n", encoding="utf-8")
    assert checker.compare_table("year,value\n2024,1\n", out, relative=False)["rows"] == 1
    with pytest.raises(ValueError, match="row count"):
        checker.compare_table("year,value\n2024,1\n2025,2\n", out, relative=False)
    with pytest.raises(ValueError, match="schema"):
        checker.compare_table("year,other\n2024,1\n", out, relative=False)


def test_scaled_reference_policy_does_not_relax_publication_limit(checker) -> None:
    left, right = "1302.2446720089888", "1302.2446720092391"
    assert checker.compare_cell(left, right, "gross_value_nzd", relative=True) < 1e-9
    with pytest.raises(ValueError, match="numerical"):
        checker.compare_cell(left, right, "gross_value_nzd", relative=False)
    with pytest.raises(ValueError, match="numerical"):
        checker.compare_cell("1302", "1302.001", "gross_value_nzd", relative=True)


@pytest.fixture
def synthesis_view(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return importlib.import_module("prepare_synthesis_replay")


def test_synthesis_view_preserves_raw_outputs_and_hashes(synthesis_view, tmp_path) -> None:

    (tmp_path / "configs").mkdir()
    config = tmp_path / "configs/input.json"
    config.write_bytes(b"{}")
    replay = tmp_path / "raw"
    (replay / "m2").mkdir(parents=True)
    (replay / "release_calibration").mkdir()
    table = replay / "m2/summary.csv"
    table.write_bytes(b"value\n1\n")
    manifest = {
        "inputs": {r"configs\input.json": hashlib.sha256(config.read_bytes()).hexdigest()},
        "outputs": {"summary.csv": hashlib.sha256(table.read_bytes()).hexdigest()},
    }
    path = replay / "m2/manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    original = path.read_bytes()
    out = tmp_path / "view"
    report = synthesis_view.prepare(tmp_path, replay, out)
    assert report["raw_outputs_unchanged"]
    assert path.read_bytes() == original
    assert (out / "m2/summary.csv").read_bytes() == table.read_bytes()
    assert set(json.loads((out / "m2/manifest.json").read_text())["inputs"]) == {"configs/input.json"}
    with pytest.raises(FileExistsError):
        synthesis_view.prepare(tmp_path, replay, out)


@pytest.mark.parametrize(
    "name", [r"..\input.json", r"C:\input.json", r"\\host\share\input.json", r"a\D:input.json"]
)
def test_synthesis_view_rejects_escaping_references(synthesis_view, tmp_path, name) -> None:
    with pytest.raises(ValueError, match=r"forbidden|Noncanonical"):
        synthesis_view.canonical_inputs(tmp_path, {name: "0" * 64})


def test_synthesis_view_rejects_hash_changes_and_aliases(synthesis_view, tmp_path) -> None:

    (tmp_path / "a").mkdir()
    path = tmp_path / "a/input"
    path.write_bytes(b"value")
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="hash mismatch"):
        synthesis_view.canonical_inputs(tmp_path, {r"a\input": "0" * 64})
    with pytest.raises(ValueError, match="Duplicate"):
        synthesis_view.canonical_inputs(tmp_path, {r"a\input": value, "a/input": value})
