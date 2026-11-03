"""Numerical reproduction must reject altered identities, shapes, nonfinite values and results."""

import importlib
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
