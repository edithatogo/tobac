"""Independent domain cases; synthetic tables do not qualify preserved originals."""

import hashlib
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALUES = (2293, 2102, 2046, 1905, 1857, 1788, 1768, 1687, 1618, 1492, 1429, 1426, 1249, 1052, 968, 755)
HEADER = ("Year", "Total tobacco sold tonnes (excl. cigars/cigarillos)")


def module():
    """Load the consumer helper without importing an optional producer package."""
    spec = importlib.util.spec_from_file_location("extract_moh", ROOT / "scripts/extract_moh_lineage.py")
    assert spec
    assert spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def table():
    """Independent frozen value oracle, distinct from the parser implementation."""
    return [HEADER, *zip(range(2010, 2026), VALUES, strict=True)]


def test_all_values_and_cell_locators_are_retained_without_mutating_input() -> None:
    data = table()
    before = list(data)
    rows = module().extract_rows(data, "Sheet1")
    assert [int(row["value_tonnes"]) for row in rows] == list(VALUES)
    assert [row["year"] for row in rows] == list(range(2010, 2026))
    assert rows[0]["year_cell"] == "A2"
    assert rows[0]["value_cell"] == "B2"
    assert rows[-1]["value_cell"] == "B17"
    assert all(row["sheet"] == "Sheet1" for row in rows)
    assert data == before


@pytest.mark.parametrize(
    "mutation",
    ["header", "missing", "extra", "order", "year_type", "negative", "nan", "inf", "columns"],
)
def test_wrong_table_and_unsafe_numeric_coercion_are_rejected(mutation) -> None:
    data = table()
    if mutation == "header":
        data[0] = ("Year", "Cigarettes")
    elif mutation == "missing":
        data.pop()
    elif mutation == "extra":
        data.append((2026, 500))
    elif mutation == "order":
        data[1], data[2] = data[2], data[1]
    elif mutation == "year_type":
        data[1] = ("2010", 2293)
    elif mutation == "negative":
        data[1] = (2010, -1)
    elif mutation == "nan":
        data[1] = (2010, float("nan"))
    elif mutation == "inf":
        data[1] = (2010, float("inf"))
    else:
        data[1] = (2010, 2293, "unexpected")
    with pytest.raises(ValueError, match="workbook"):
        module().extract_rows(data, "Sheet1")


@pytest.mark.parametrize("value", [True, "2293", None])
def test_numeric_cells_are_not_coerced(value) -> None:
    data = table()
    data[1] = (2010, value)
    with pytest.raises(TypeError, match="workbook"):
        module().extract_rows(data, "Sheet1")


def test_verified_snapshot_is_independent_of_later_file_changes(tmp_path) -> None:
    path = tmp_path / "original"
    path.write_bytes(b"original")
    frozen = module().verified_bytes(path, hashlib.sha256(b"original").hexdigest())
    path.write_bytes(b"<html>challenge</html>")
    assert frozen == b"original"
    with pytest.raises(ValueError, match="Input bytes"):
        module().verified_bytes(path, hashlib.sha256(b"original").hexdigest())


def test_symlink_input_and_output_outside_private_namespace_are_rejected(tmp_path) -> None:
    actual = tmp_path / "original"
    actual.write_bytes(b"original")
    link = tmp_path / "link"
    link.symlink_to(actual)
    with pytest.raises(ValueError, match="Symlink"):
        module().verified_bytes(link)
    with pytest.raises(ValueError, match="private outputs"):
        module().execute(actual, tmp_path / "new-attempt", tmp_path / "lock")


def test_unreviewed_producer_wheel_is_rejected_before_import(tmp_path) -> None:
    path = tmp_path / "unreviewed.whl"
    path.write_bytes(b"unreviewed artifact")
    with pytest.raises(ValueError, match="Producer wheel"):
        module().producer(path)


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "version"])
def test_sbom_must_cover_actual_installed_components_exactly(mutation) -> None:
    document = {"components": [{"type": "library", "name": "archive_govt_nz", "version": "0.1.0"}]}
    module().validate_inventory(document, {"archive-govt-nz": "0.1.0"})
    if mutation == "missing":
        document["components"] = []
    elif mutation == "duplicate":
        document["components"] *= 2
    else:
        document["components"][0]["version"] = "0.0.0"
    with pytest.raises(ValueError, match="actual installed"):
        module().validate_inventory(document, {"archive-govt-nz": "0.1.0"})


def test_wrong_sheet_cannot_be_substituted_for_the_pinned_source() -> None:
    with pytest.raises(ValueError, match="workbook"):
        module().extract_rows(table(), "WrongSheet")


def test_existing_attempt_is_never_overwritten(tmp_path) -> None:
    (tmp_path / "retained").write_text("old attempt")
    with pytest.raises(FileExistsError):
        module().execute(tmp_path / "source.xlsx", tmp_path, tmp_path / "environment.lock")
    assert (tmp_path / "retained").read_text() == "old attempt"
