"""Bounded MOH native-verification protocol and consumer parity checks."""

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def module():
    spec = importlib.util.spec_from_file_location(
        "qualify_moh_workbook", ROOT / "scripts/qualify_moh_workbook.py"
    )
    assert spec
    assert spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def native_fixture():
    bindings = json.loads((ROOT / "integration/archive/source-bindings.json").read_text())
    source = next(s for s in bindings["sources"] if s["archive_id"] == "tobac-7ee48855a1ed1c4b")
    return {"register_sha256": bindings["register_sha256"], "sources": [source]}


def test_missing_capture_time_does_not_fail_fixity_or_become_verification_time() -> None:
    capture = module().checked_capture(native_fixture(), ROOT)
    assert capture["captured_at"] is None
    assert capture["status"] == "source_workbook_values_matched"


@pytest.mark.parametrize("field", ["sha256", "warc_sha256", "uri", "status"])
def test_wrong_native_identity_or_unverified_status_fails_closed(field) -> None:
    result = native_fixture()
    capture = next(
        c for c in result["sources"][0]["captures"] if c["status"] == "source_workbook_values_matched"
    )
    capture[field] = "wrong"
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Expected\ one\ native\ workbook\ capture"
            r"|"
            r"Native\ workbook\ or\ WARC\ qualification\ mismatch"
            r")"
        ),
    ):
        module().checked_capture(result, ROOT)


def test_duplicate_source_cannot_hide_conflicting_capture() -> None:
    result = native_fixture()
    result["sources"].append(copy.deepcopy(result["sources"][0]))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Native\ source/register\ identity\ mismatch)"),
    ):
        module().checked_capture(result, ROOT)


def test_exact_parity_and_periods_use_current_consumer_bytes() -> None:
    import csv  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from decimal import Decimal  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    with (ROOT / "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    expected = [[int(r["year"]), float(Decimal(r["value"]))] for r in rows]
    result = module().compare_rows(rows, expected)
    assert len(result) == 16
    assert result[0] == {
        "year": 2010,
        "value_tonnes": "2293",
        "period_start": "2010-01-01",
        "period_end": "2011-01-01",
    }


@pytest.mark.parametrize("mutation", ["value", "missing", "duplicate", "year", "unit", "source", "period"])
def test_transcription_or_scope_drift_is_rejected(mutation) -> None:
    import csv  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    with (ROOT / "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    expected = [[int(r["year"]), float(r["value"])] for r in rows]
    if mutation == "value":
        rows[0]["value"] = "2294"
    elif mutation == "missing":
        rows.pop()
    elif mutation == "duplicate":
        rows.append(copy.deepcopy(rows[0]))
    elif mutation == "year":
        rows[0]["year"] = "2009"
    elif mutation == "unit":
        rows[0]["unit"] = "cigarette_equivalents/year"
    elif mutation == "source":
        rows[0]["source_id"] = "different-citation"
    else:
        rows[0]["period_end"] = "2010-12-31"
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Consumer\ value,\ source,\ unit\ or\ period\ mismatch"
            r"|"
            r"Missing,\ duplicated\ or\ reordered\ consumer\ years"
            r")"
        ),
    ):
        module().compare_rows(rows, expected)


def test_pathway_spec_does_not_invent_calibration_or_duty_free_coverage() -> None:
    spec = json.loads((ROOT / "integration/archive/moh-observation-specification.json").read_text())
    assert spec["measurement_model"]["parameter_values"] is None
    assert spec["scope"]["duty_free_included"] is None
    assert spec["conversion"]["total_mass_divided_by_0_7_is_valid"] is False
    assert spec["scientific_qualification"] is False
    assert spec["automatically_conditions_live_model"] is False
