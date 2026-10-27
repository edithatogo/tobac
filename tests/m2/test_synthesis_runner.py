"""Exercise real source reconciliation and fail-closed report provenance."""

import csv
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def bind_replay(replay):
    names = ("validation.json", "summary.csv", "grouped_evppi.csv", "study_value.csv")
    outputs = {n: hashlib.sha256((replay / "m2" / n).read_bytes()).hexdigest() for n in names}
    (replay / "m2/manifest.json").write_text(json.dumps({"inputs": {}, "outputs": outputs}))
    name = "rolling_predictive_checks.csv"
    sha = hashlib.sha256((replay / "release_calibration" / name).read_bytes()).hexdigest()
    (replay / "release_calibration/run_manifest.json").write_text(
        json.dumps({"files": [{"path": name, "sha256": sha}]})
    )


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import qualify_m2_synthesis  # noqa: PLC0415 -- Standalone entry-point boundary.

    return qualify_m2_synthesis


@pytest.fixture
def replay(tmp_path):
    config = json.loads((ROOT / "configs/m2_retail.json").read_text())
    scenarios = [(c["id"], w) for c in config["cases"] for w in config["crime_weights"]]
    write_csv(
        tmp_path / "m2/summary.csv",
        [{"case": c, "crime_weight": w, "value_unit": "synthetic units"} for c, w in scenarios],
    )
    write_csv(
        tmp_path / "m2/grouped_evppi.csv",
        [{"case": c, "crime_weight": w, "group": "market", "evppi": 0.05} for c, w in scenarios],
    )
    write_csv(
        tmp_path / "m2/study_value.csv",
        [
            {"case": c, "crime_weight": w, "design": d, "evsi": value}
            for c, w in scenarios
            for d, value in (("none", 0), ("matched", 0.1))
        ],
    )
    (tmp_path / "m2/validation.json").write_text(json.dumps({"passed": True, "designs": 2}))
    write_csv(
        tmp_path / "release_calibration/rolling_predictive_checks.csv",
        [
            {
                "train_end_year": 2023,
                "test_year": 2024,
                "stage": "reserved_diagnostic_2024_2025",
                "covered_95": True,
                "vintage": "synthetic_retrospective",
            }
        ],
    )
    bind_replay(tmp_path)
    return tmp_path


def test_source_bound_report_preserves_conflicts_without_fitting(runner, replay) -> None:
    report = runner.build_report(ROOT, replay)
    assert not report["conditioned"]
    assert not report["target_empirically_identified"]
    assert report["supply"]["factory_made_known_sticks"] == "736488410.000"
    assert report["supply"]["factory_made_with_one_RS_interpretation_sticks"] == [
        "736564810.000",
        "737252410.000",
    ]
    assert report["supply"]["ryo_known_tonnes"] == "109.60010"
    assert report["supply"]["ryo_if_BAT_2025_year_confirmed_tonnes"] == "215.00010"
    assert report["supply"]["national_upper_bound"] is None
    assert report["supply"]["national_cigarette_equivalents"] is None
    assert report["conditional_voi"]["gross_cost_ceiling_ranges"]["matched"] == [0.1, 0.1]
    assert report["bounds"][0]["quitting"] == {"lower": 0, "upper": 1}


def test_edited_reference_output_is_rejected(runner, replay) -> None:
    (replay / "m2/study_value.csv").write_text("edited")
    with pytest.raises(ValueError, match="hash mismatch"):
        runner.build_report(ROOT, replay)


def test_partial_scenario_table_is_not_a_robust_envelope(runner, replay) -> None:
    path = replay / "m2/study_value.csv"
    rows = runner.csv_rows(path)
    write_csv(path, rows[:-1])
    bind_replay(replay)
    with pytest.raises(ValueError, match="Complete unique"):
        runner.build_report(ROOT, replay)


def test_failed_numerical_validation_cannot_supply_cost_ceiling(runner, replay) -> None:
    (replay / "m2/validation.json").write_text(json.dumps({"passed": False}))
    bind_replay(replay)
    with pytest.raises(ValueError, match="invariants must pass"):
        runner.build_report(ROOT, replay)


def test_future_leakage_is_rejected_even_in_a_rehashed_fixture(runner, replay) -> None:
    path = replay / "release_calibration/rolling_predictive_checks.csv"
    rows = runner.csv_rows(path)
    rows[0]["train_end_year"] = "2024"
    write_csv(path, rows)
    bind_replay(replay)
    with pytest.raises(ValueError, match="future test observation"):
        runner.build_report(ROOT, replay)


def test_command_refuses_to_overwrite(runner, replay, monkeypatch) -> None:
    out = replay / "synthesis.json"
    monkeypatch.setattr("sys.argv", ["synthesis", "--replay", str(replay), "--out", str(out)])
    runner.main()
    before = out.read_bytes()
    with pytest.raises(FileExistsError):
        runner.main()
    assert out.read_bytes() == before


def test_duplicate_designs_do_not_supply_an_envelope(runner, replay) -> None:
    path = replay / "m2/study_value.csv"
    rows = runner.csv_rows(path)
    write_csv(path, [*rows, rows[0]])
    bind_replay(replay)
    with pytest.raises(ValueError, match="Complete unique"):
        runner.build_report(ROOT, replay)


def test_missing_reserved_diagnostic_is_not_field_validation(runner, replay) -> None:
    path = replay / "release_calibration/rolling_predictive_checks.csv"
    rows = runner.csv_rows(path)
    rows[0]["stage"] = "exploratory_selection"
    write_csv(path, rows)
    bind_replay(replay)
    with pytest.raises(ValueError, match="reserved diagnostics"):
        runner.build_report(ROOT, replay)


def test_nonfinite_values_are_not_cost_ceilings(runner, replay) -> None:
    path = replay / "m2/study_value.csv"
    rows = runner.csv_rows(path)
    rows[0]["evsi"] = "NaN"
    write_csv(path, rows)
    bind_replay(replay)
    with pytest.raises(ValueError, match="Finite study"):
        runner.build_report(ROOT, replay)
