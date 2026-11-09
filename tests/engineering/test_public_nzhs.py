"""Verify exact NZHS source cells without creating independent observations."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import shutil
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]
PACK = Path("evidence/public_data_20261108")
FILES = (
    "nzhs_counts_2024_25.csv",
    "nzhs_prevalence_2024_25.csv",
    "nzhs_vaping_union_ci_2024_25.csv",
    "nzhs_smoking_ci_2024_25.csv",
)
INDICATORS = {
    "daily_smoking": "Daily smokers",
    "daily_vaping": "Daily vaping",
    "current_vaping_at_least_monthly": "Monthly vaping",
    "daily_smoking_or_vaping_or_both": "Daily smoker and/or daily vaper",
}


@pytest.fixture
def audit() -> ModuleType:
    """Load the script's public reconciliation surface without its CLI."""
    spec = importlib.util.spec_from_file_location("public_nzhs", ROOT / "scripts/reconcile_public_nzhs.py")
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames
        return reader.fieldnames, list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_selection(row: dict[str, str]) -> tuple[str, str]:
    """Build synthetic source locations independently of production selection."""
    stratum = row.get("stratum", "all")
    if row.get("unit") == "estimated_people":
        return "Total", "estimated.number"
    if stratum in ("men", "women"):
        return "Total", "male" if stratum == "men" else "female"
    if stratum.startswith("NZDep_quintile_"):
        return "Quintile " + stratum[-1], "total"
    if row.get("stratum_type") == "age":
        return stratum.replace("_plus", "+").replace("_", "-"), "total"
    return {"all": "Total", "Maori": "Māori", "European_Other": "European/Other"}.get(
        stratum, stratum
    ), "total"


@pytest.fixture
def inputs(tmp_path: Path, audit: ModuleType, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """Use a complete synthetic source with deliberate gender and union traps."""
    pack = tmp_path / PACK
    pack.mkdir(parents=True)
    shutil.copyfile(ROOT / PACK / "manifest.json", pack / "manifest.json")
    source_rows: dict[tuple[str, str], dict[str, str]] = {}
    for name in FILES:
        shutil.copyfile(ROOT / PACK / name, pack / name)
        _, rows = read_csv(pack / name)
        for row in rows:
            group, field = source_selection(row)
            indicator = INDICATORS[row["indicator"]]
            source = source_rows.setdefault((indicator, group), dict.fromkeys(audit.NZHS_COLUMNS, ""))
            source.update(population="adults", year="2024", group=group, **{"short.description": indicator})
            source[field] = row["value"]
            step = Decimal(1000) if field == "estimated.number" else Decimal("0.1")
            source.setdefault(field + ".low.CI", "")
            source.setdefault(field + ".high.CI", "")
            if not source[field + ".low.CI"]:
                source[field + ".low.CI"] = str(Decimal(row["value"]) - step)
                source[field + ".high.CI"] = str(Decimal(row["value"]) + step)
            if "ci95_lower" in row:
                source[field + ".low.CI"] = row["ci95_lower"]
                source[field + ".high.CI"] = row["ci95_upper"]
            flag = (
                "flag_for_publishing"
                if field in ("total", "estimated.number")
                else field + "_flag_for_publishing"
            )
            if row.get("caution_rse_over_30_percent") == "true":
                source[flag] = "e"
    trap = dict.fromkeys(audit.NZHS_COLUMNS, "")
    trap.update(
        population="adults",
        year="2024",
        group="Total",
        total="1.4",
        **{"short.description": "Daily smoker and daily vaper", "total.low.CI": "1", "total.high.CI": "2"},
    )
    original = tmp_path / "synthetic-nzhs.csv"
    write_csv(original, list(audit.NZHS_COLUMNS), [trap, *[source_rows[key] for key in sorted(source_rows)]])
    monkeypatch.setattr(audit, "QUALIFIED_SOURCE_SHA256", hashlib.sha256(original.read_bytes()).hexdigest())
    return tmp_path, original


def repin_pack(root: Path, name: str) -> None:
    manifest_path = root / PACK / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest["files"]:
        if item["path"] == name:
            item["sha256"] = hashlib.sha256((root / PACK / name).read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


def mutate_source(
    inputs: tuple[Path, Path], audit: ModuleType, monkeypatch: pytest.MonkeyPatch, field: str, value: str
) -> None:
    _, source = inputs
    fields, rows = read_csv(source)
    selected = next(
        row for row in rows if row["short.description"] == "Daily vaping" and row["group"] == "Total"
    )
    selected[field] = value
    write_csv(source, fields, rows)
    monkeypatch.setattr(audit, "QUALIFIED_SOURCE_SHA256", hashlib.sha256(source.read_bytes()).hexdigest())


def test_all_rows_map_to_source_cells_and_preserve_dependence(
    audit: ModuleType, inputs: tuple[Path, Path]
) -> None:
    root, source = inputs
    rows, report = audit.reconcile(source, root=root)
    assert len(rows) == 89
    assert report["verification"] == {
        "point_estimates": 89,
        "confidence_interval_pairs": 69,
        "explicit_caution_flags": 54,
        "unreported_caution_flags": 15,
        "summary_rows_without_caution_field": 20,
        "unique_source_cells": 73,
        "unique_source_records": 67,
        "source_records": 68,
    }
    assert report["empirical_admission"] is False
    assert report["independent_observations_added"] == 0
    assert {row["dependence_group"] for row in rows} == {"NZHS_2024_25_shared_survey"}
    _, source_rows = read_csv(source)
    for row in rows:
        assert source_rows[int(row["source_record_ordinal"]) - 1][row["source_field"]] == row["source_value"]


def test_union_is_not_dual_use_and_gender_uses_sex_field(
    audit: ModuleType, inputs: tuple[Path, Path]
) -> None:
    root, source = inputs
    rows, _ = audit.reconcile(source, root=root)
    union = next(
        row
        for row in rows
        if row["indicator"] == "daily_smoking_or_vaping_or_both" and row["stratum"] == "all"
    )
    assert union["source_indicator"] == "Daily smoker and/or daily vaper"
    assert Decimal(union["source_value"]) == Decimal("17.1")
    male = next(row for row in rows if row["indicator"] == "daily_vaping" and row["stratum"] == "men")
    assert male["source_field"] == "male"
    assert male["source_ci95_lower"]
    assert male["ci_check"] == "source_annotation_only"


def test_decimal_equality_is_exact_without_precision_tolerance(
    audit: ModuleType, inputs: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root, source = inputs
    mutate_source(inputs, audit, monkeypatch, "male", "13")
    audit.reconcile(source, root=root)
    mutate_source(inputs, audit, monkeypatch, "male", "13.000000001")
    with pytest.raises(ValueError, match="point estimate"):
        audit.reconcile(source, root=root)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("total.low.CI", "10.6"),
        ("flag_for_publishing", "e"),
        ("flag_for_publishing", "S"),
        ("flag_for_publishing", "unknown"),
        ("total", "NaN"),
    ],
)
def test_bad_source_values_or_flags_fail_before_output(
    audit: ModuleType, inputs: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch, field: str, value: str
) -> None:
    root, source = inputs
    mutate_source(inputs, audit, monkeypatch, field, value)
    output = root / "result"
    with pytest.raises(ValueError, match=r"confidence interval|caution|Suppressed|Unknown source|Nonfinite"):
        audit.write_reconciliation(source, output, root=root)
    assert not output.exists()


def test_unreviewed_source_hash_drift_is_rejected(audit: ModuleType, inputs: tuple[Path, Path]) -> None:
    root, source = inputs
    source.write_bytes(source.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="hash mismatch"):
        audit.reconcile(source, root=root)


def test_pack_hash_drift_is_rejected(audit: ModuleType, inputs: tuple[Path, Path]) -> None:
    root, source = inputs
    path = root / PACK / FILES[0]
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="hash mismatch"):
        audit.reconcile(source, root=root)


@pytest.mark.parametrize(
    "mutation", ["duplicate", "subgroup", "union", "schema", "caution", "scope", "source"]
)
def test_repinned_bad_extract_is_not_accepted(
    audit: ModuleType, inputs: tuple[Path, Path], mutation: str
) -> None:
    root, source = inputs
    name = FILES[2]
    path = root / PACK / name
    fields, rows = read_csv(path)
    if mutation == "duplicate":
        rows[-1] = rows[0].copy()
    elif mutation == "subgroup":
        rows[0]["stratum"] = "unknown"
    elif mutation == "union":
        rows[2]["value"] = "1.4"
    elif mutation == "schema":
        fields.append("unexpected")
    elif mutation == "caution":
        rows[24]["caution_rse_over_30_percent"] = "false"
    elif mutation == "scope":
        rows[0]["geography"] = "AU_national"
    else:
        rows[0]["source_id"] = "unknown"
    write_csv(path, fields, rows)
    repin_pack(root, name)
    with pytest.raises(ValueError, match=r"Duplicate|unreviewed|point estimate|schema|caution"):
        audit.reconcile(source, root=root)


def test_duplicate_source_identity_is_rejected(
    audit: ModuleType, inputs: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root, source = inputs
    fields, rows = read_csv(source)
    rows.append(rows[1].copy())
    write_csv(source, fields, rows)
    monkeypatch.setattr(audit, "QUALIFIED_SOURCE_SHA256", hashlib.sha256(source.read_bytes()).hexdigest())
    with pytest.raises(ValueError, match="Duplicate"):
        audit.reconcile(source, root=root)


def test_outputs_are_deterministic_and_do_not_overwrite(audit: ModuleType, inputs: tuple[Path, Path]) -> None:
    root, source = inputs
    for name in ("first", "second"):
        audit.write_reconciliation(source, root / name, root=root)
    for name in ("nzhs-reconciliation.csv", "nzhs-reconciliation.json"):
        assert (root / "first" / name).read_bytes() == (root / "second" / name).read_bytes()
    with pytest.raises(ValueError, match="overwrite"):
        audit.write_reconciliation(source, root / "first", root=root)
