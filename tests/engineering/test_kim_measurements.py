"""Check source-bound parsing, censored arithmetic and the empirical refusal."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "evidence/kim_measurements_20261109"


@pytest.fixture
def comparison() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "kim_measurements", ROOT / "scripts/compare_kim_measurements.py"
    )
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthetic_table(table: str, rows: list[tuple[str, list[str]]], *, values_above: bool = False) -> str:
    """Use new fixed-width text, reversed plant order and deliberately wrapped cells."""
    lines = [f"Table {table}.", " " * 40 + "".join(f"{day:^14}" for day in ["WED", "SUN"] * 6)]
    for site, cells in rows:
        tops, bottoms = [], []
        for cell in cells:
            first, separator, last = cell.partition(" ± ")
            tops.append(first + " ±" if separator else cell)
            bottoms.append(last if separator else "")
        if values_above:
            lines.extend(
                (
                    " " * 40 + "".join(f"{part:^14}" for part in tops),
                    f"{site:<40}" + "".join(f"{part:^14}" for part in bottoms),
                )
            )
        else:
            lines.extend(
                (
                    f"{site:<40}" + "".join(f"{part:^14}" for part in tops),
                    " " * 40 + "".join(f"{part:^14}" for part in bottoms),
                )
            )
    return "\n".join(lines)


@pytest.fixture
def layout(comparison: ModuleType) -> str:
    """Preserve reviewed shapes using entirely synthetic dates and assay values."""
    pages = [""] * 53
    rows = []
    for site in comparison.SITES:
        cells = [f"{10 + column % 2:02}/{column // 2 + 5:02}/23" for column in range(12)]
        if site == "Whangārei":
            cells[-2:] = ["-", "-"]
        rows.append((site, cells))
    pages[7] = synthetic_table("S3", rows)
    for analyte, (page, table) in {**comparison.TABLES, "TOTAL": (46, "S23")}.items():
        rows = []
        for site_index, site in enumerate(comparison.SITES):
            cells = []
            for column in range(12):
                cell = f"{site_index * 100 + column + 1} ± 2"
                if analyte == "ANBA" and site_index * 12 + column >= 25:
                    cell = "< LoQ"
                if site == "Whangārei" and column >= 10:
                    cell = ""
                cells.append(cell)
            rows.append((site, cells))
        pages[page - 1] = synthetic_table(table, list(reversed(rows)), values_above=table == "S23")
    return "\f".join(pages) + "\f"


def test_wrapped_cells_join_by_plant_and_keep_censored_slots(comparison: ModuleType, layout: str) -> None:
    dates = comparison.occasions(layout)
    rows, totals = comparison.measurement_rows(layout, dates)
    assert len(rows) == 576
    assert len(totals) == 144
    selected = next(
        row
        for row in rows
        if row["analyte"] == "COT"
        and row["plant_as_published"] == "Hamilton"
        and row["nominal_weekday"] == "SUN"
        and row["month_as_published"] == "October"
    )
    assert selected["mean_as_published"] == "412"
    assert selected["duplicate_sd_as_published"] == "2"
    assert totals[selected["slot_id"]]["mean_as_published"] == "412"
    assert sum(row["status"] == "between_lod_and_loq" for row in rows) == 117
    assert all(
        not row["mean_as_published"] and not row["duplicate_sd_as_published"]
        for row in rows
        if row["status"] != "quantified"
    )
    scenarios = comparison.calibration_rows(rows)
    assert len(scenarios) == 432
    assert sum(bool(row["load_divided_by_factor"]) for row in scenarios) == 75
    assert all(
        not row["load_divided_by_factor"] and not row["rounding_only_upper"]
        for row in scenarios
        if row["status"] != "quantified"
    )


@pytest.mark.parametrize("bad", ["< LoD", "0 ± 2", "4 ± -1", "4 ± NaN", "4 2", "< LoQ 0", "1 ± 2 ± 3"])
def test_unknown_or_malformed_measurement_is_not_repaired(comparison: ModuleType, bad: str) -> None:
    with pytest.raises(ValueError, match="Unrecognised measurement"):
        comparison.measurement_cell(bad)


def test_changed_date_missingness_and_plant_identity_fail(comparison: ModuleType, layout: str) -> None:
    with pytest.raises(ValueError, match="outside its source month"):
        comparison.occasions(layout.replace("10/05/23", "10/04/23", 1))
    with pytest.raises(ValueError, match="Missing or duplicate plant"):
        comparison.occasions(layout.replace("Auckland Central", "Auckland North", 1))
    dates = comparison.occasions(layout)
    # A present load at an absent Whangārei occasion must not become a new sample.
    target = next(row for row in dates if row["status"] == "missing_occasion")
    target["status"] = "dated_occasion"
    with pytest.raises(ValueError, match="missingness disagrees"):
        comparison.measurement_rows(layout, dates)


def test_duplicate_date_does_not_inflate_occasions(comparison: ModuleType, layout: str) -> None:
    with pytest.raises(ValueError, match="Occasion identities"):
        comparison.occasions(layout.replace("11/05/23", "10/05/23", 1))


def test_two_replicates_require_endpoints_not_merely_correlation_envelope(comparison: ModuleType) -> None:
    assert comparison.spread_check("10.00", "10.00", "27.00")["sd_compatibility"] == "paired_endpoint"
    assert comparison.spread_check("10.00", "10.00", "13.50")["sd_compatibility"] == "broader_envelope_only"
    result = comparison.spread_check("18", "59", "325")
    assert result["sd_compatibility"] == "outside_broader_envelope"
    assert result["sd_envelope_upper"] == "105.3"


def test_nicotine_reconstruction_retains_signed_disagreement(comparison: ModuleType) -> None:
    measurements = [
        {"slot_id": "sample", "analyte": "COT", "mean_as_published": "100", "duplicate_sd_as_published": "1"},
        {
            "slot_id": "sample",
            "analyte": "COT-OH",
            "mean_as_published": "200",
            "duplicate_sd_as_published": "2",
        },
    ]
    total = {
        "occasion_id": "sample",
        "status": "quantified",
        "cell_as_published": "403 ± 4",
        "mean_as_published": "403",
        "duplicate_sd_as_published": "4",
    }
    row = comparison.nicotine_diagnostics(measurements, {"sample": total})[0]
    assert row["reported_total_mean"] == "403"
    assert row["reconstructed_mean"] == "405"
    assert row["reported_minus_reconstructed"] == "-2"
    assert row["mean_rounding_tolerance"] == "1.85"
    assert row["mean_compatible_with_rounding"] == "false"


def test_calibration_units_cancel_thousands_without_pooling(comparison: ModuleType) -> None:
    rows = comparison.calibration_rows(
        [
            {
                "analyte": "ANBA",
                "slot_id": "sample",
                "occasion_id": "sample",
                "status": "quantified",
                "mean_as_published": "1.13",
            }
        ]
    )
    by_scenario = {row["scenario"]: row for row in rows}
    assert float(by_scenario["bade2020_reported"]["load_divided_by_factor"]) == 1
    assert float(by_scenario["zheng2023_reported"]["load_divided_by_factor"]) == pytest.approx(1.13 / 0.91)
    assert float(by_scenario["weng2026_conditional_dose"]["load_divided_by_factor"]) == pytest.approx(
        1.13 / 0.64944
    )
    assert float(by_scenario["bade2020_reported"]["rounding_only_lower"]) == pytest.approx(1.125 / 1.13)


def test_original_hash_rejected_before_converter_or_output(
    comparison: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "changed.pdf"
    source.write_bytes(b"unqualified edition")
    monkeypatch.setattr(comparison.shutil, "which", lambda _: pytest.fail("converter must not run"))
    with pytest.raises(ValueError, match="hash mismatch"):
        comparison.run(source, tmp_path / "comparison")
    assert not (tmp_path / "comparison").exists()


def test_converter_output_requires_qualified_layout(
    comparison: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source, executable = tmp_path / "source.pdf", tmp_path / "converter"
    source.write_bytes(b"synthetic source")
    executable.write_bytes(b"synthetic executable identity")
    monkeypatch.setattr(comparison, "PDF_SHA256", hashlib.sha256(source.read_bytes()).hexdigest())
    monkeypatch.setattr(comparison.shutil, "which", lambda _: str(executable))
    responses = iter(
        [
            SimpleNamespace(stdout=b"", stderr=b"pdftotext version synthetic\n"),
            SimpleNamespace(stdout=b"changed layout", stderr=b""),
        ]
    )
    monkeypatch.setattr(comparison.subprocess, "run", lambda *_args, **_kwargs: next(responses))
    with pytest.raises(ValueError, match="qualified layout"):
        comparison.layout_from_pdf(source)


def test_immutable_output_and_changed_review_gate(
    comparison: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, layout: str
) -> None:
    destination = tmp_path / "existing"
    destination.mkdir()
    with pytest.raises(ValueError, match="overwrite"):
        comparison.run(tmp_path / "missing.pdf", destination)
    monkeypatch.setattr(comparison, "read", lambda _: {"scientific_qualification": True})
    dates = comparison.occasions(layout)
    measurements, totals = comparison.measurement_rows(layout, dates)
    with pytest.raises(ValueError, match="review status changed"):
        comparison.comparison_report(
            dates, measurements, comparison.nicotine_diagnostics(measurements, totals), {}
        )


def test_published_pack_preserves_observations_and_explicit_no_score() -> None:
    report = json.loads((PACK / "comparison.json").read_text(encoding="utf-8"))
    assert report["source_support"]["dated_occasions"] == 142
    assert report["source_support"]["nominal_weekday_disagreements"] == 7
    assert report["nicotine_diagnostics"]["means_compatible_with_rounding"] == 136
    assert report["nicotine_diagnostics"]["means_outside_rounding"] == 6
    assert report["nicotine_diagnostics"]["sd_compatibility"] == {
        "paired_endpoint": 137,
        "broader_envelope_only": 2,
        "outside_broader_envelope": 3,
    }
    assert report["empirical_admission"] is False
    assert report["native_lineage_qualification"] is False
    assert report["automatically_conditions_live_model"] is False
    assert report["first_comparison"]["paired_predictive_score"] is None
    assert report["first_comparison"]["empirical_voi"] is None
    for name, binding in report["outputs"].items():
        path = PACK / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == binding["sha256"]
        with path.open(encoding="utf-8", newline="") as handle:
            assert len(list(csv.DictReader(handle))) == binding["rows"]
    with (PACK / "measurements.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if row["status"] != "quantified":
            assert not row["mean_as_published"]
            assert not row["duplicate_sd_as_published"]
    assert len({row["occasion_id"] for row in rows if row["occasion_id"]}) == 142
