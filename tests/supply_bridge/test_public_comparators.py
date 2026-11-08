"""Identity, scope and numerical consistency of the candidate public tables."""

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "evidence/public_data_20261108"
MANIFEST = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))


def rows(name):
    with (PACK / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@pytest.mark.parametrize("entry", MANIFEST["files"], ids=lambda entry: entry["path"])
def test_declared_table_bytes_shape_and_nonadmission(entry):
    path = PACK / entry["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    records = rows(entry["path"])
    assert len(records) == entry["rows"]
    assert list(records[0]) == entry["columns"]
    assert all(
        None not in record and all(value is not None for value in record.values()) for record in records
    )
    assert entry["empirical_admission"] is False
    assert entry["role"] in {"external_comparator", "descriptive_context"}


def test_complete_periods_and_finite_numbers_in_abs_tables():
    periods = ["Dec-16"] + [f"{q}-{year}" for year in range(17, 26) for q in ("Mar", "Jun", "Sep", "Dec")]
    for entry in MANIFEST["files"]:
        if not entry["path"].startswith("abs_"):
            continue
        records = rows(entry["path"])
        expected = [str(year) for year in range(2018, 2026)] if entry["rows"] == 8 else periods
        assert [row["period_as_published"] for row in records] == expected
        numbers = np.array([[float(row[column]) for column in entry["columns"][1:]] for row in records])
        assert np.isfinite(numbers).all()


@pytest.mark.parametrize(
    "name", ["abs_nicotine_kg_quarterly.csv", "abs_expenditure_aud_million_quarterly.csv"]
)
def test_component_totals_preserve_published_rounding(name):
    records = rows(name)
    columns = list(records[0])[1:]
    numbers = np.array([[float(row[column]) for column in columns] for row in records])
    # Five independently rounded displayed cells allow up to 2.5 of the unit.
    assert np.all(np.abs(numbers[:, 0] - numbers[:, 1:].sum(axis=1)) <= 2.5)
    assert np.all(numbers >= 0)
    if name == "abs_nicotine_kg_quarterly.csv":
        assert numbers[-1, 0] == 8030
        assert numbers[-1, 1:].sum() == 8031  # Deliberately not silently balanced.


def test_sensitivity_scenarios_ordered_and_distinct_from_intervals():
    for record in rows("abs_expenditure_scenarios_quarterly.csv"):
        values = list(record.values())
        assert float(values[1]) <= float(values[2]) <= float(values[3])
    source = MANIFEST["sources"][0]
    assert "not confidence" in source["uncertainty"]


def test_nz_marginals_remain_scoped_and_missing_uncertainty_explicit():
    records = rows("nzhs_prevalence_2024_25.csv")
    assert len({(row["stratum_type"], row["stratum"]) for row in records}) == 9
    assert len({(row["stratum_type"], row["stratum"], row["indicator"]) for row in records}) == 18
    for row in records:
        assert 0 <= float(row["value"]) <= 100
        assert row["geography"] == "NZ_national"
        assert row["age_scope"] == "15_plus"
        assert row["unit"] == "percent"
        assert row["uncertainty"] == "not_provided_in_summary_text"
    nz_source = MANIFEST["sources"][1]
    assert nz_source["original_sha256"] is None
    assert nz_source["empirical_admission"] is False


def test_sources_and_pack_are_not_claimed_as_independent_admitted_data():
    assert len({source["dependence_group"] for source in MANIFEST["sources"]}) == 2
    assert all(source["empirical_admission"] is False for source in MANIFEST["sources"])
    assert MANIFEST["native_lineage_qualification"] == "pending"
    assert sum(entry["rows"] for entry in MANIFEST["files"]) == 282


def test_published_intervals_and_caution_flags_are_preserved():
    records = rows("nzhs_smoking_ci_2024_25.csv") + rows("nzhs_vaping_union_ci_2024_25.csv")
    assert len(records) == 69
    for row in records:
        assert 0 <= float(row["ci95_lower"]) <= float(row["value"]) <= float(row["ci95_upper"]) <= 100
        assert row["unit"] == "percent"
    cautions = [row for row in records if row["caution_rse_over_30_percent"] == "true"]
    assert len(cautions) == 2
    assert {row["stratum"] for row in cautions} == {"75_plus"}


def test_overlapping_published_values_agree_without_becoming_new_observations():
    def key(row):
        return row["stratum_type"], row["stratum"], row["indicator"]

    official = {key(row): float(row["value"]) for row in rows("nzhs_prevalence_2024_25.csv")}
    compared = set()
    for row in rows("nzhs_smoking_ci_2024_25.csv") + rows("nzhs_vaping_union_ci_2024_25.csv"):
        if key(row) in official:
            assert float(row["value"]) == official[key(row)]
            compared.add(key(row))
    assert len(compared) == 16  # The PHCC vaping table does not include gender rows.
    assert all(
        source["dependence_group"] == "NZHS_2024_25_shared_survey" for source in MANIFEST["sources"][1:]
    )


def test_union_is_not_mislabelled_as_dual_use_or_transition_evidence():
    groups = {}
    for row in rows("nzhs_vaping_union_ci_2024_25.csv"):
        groups.setdefault((row["stratum_type"], row["stratum"]), {})[row["indicator"]] = float(row["value"])
    for values in groups.values():
        assert values["daily_vaping"] <= values["current_vaping_at_least_monthly"]
        assert values["daily_vaping"] <= values["daily_smoking_or_vaping_or_both"]
    assert groups["all_adults", "all"]["daily_smoking_or_vaping_or_both"] == 17.1
