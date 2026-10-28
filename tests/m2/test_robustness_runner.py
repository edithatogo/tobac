"""Check protocol validation, original parity and executable challenge outputs."""

import json
from pathlib import Path

import jsonschema
import numpy as np
import pytest

ROOT = Path(__file__).parents[2]


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import run_m2_robustness  # noqa: PLC0415 -- CLI boundary.

    return run_m2_robustness


def test_unchanged_design_membership_and_likelihoods(runner) -> None:
    from tobac.regulation import load_config  # noqa: PLC0415 -- Reference parity.
    from tobac.retail_case import build_retail_states, retail_channels, retail_studies  # noqa: PLC0415

    states, prior, config = build_retail_states(load_config(ROOT / "configs/regulatory.json"), quit_points=1)
    channels = retail_channels(states, config)
    original = retail_studies(channels)
    neutral = runner.challenge_reports(channels, prior, {})
    assert neutral.keys() == original.keys()
    assert all(np.allclose(neutral[k], original[k], rtol=0, atol=1e-14) for k in original)
    coupled = runner.challenge_reports(channels, prior, {"report_dependence": 0.8})
    assert np.array_equal(coupled["none"], original["none"])
    assert np.array_equal(coupled["criminal_harm_study"], original["criminal_harm_study"])


def test_source_bound_small_challenge_run_and_new_directory(runner, tmp_path) -> None:
    spec = json.loads((ROOT / "configs/m2_robustness.json").read_text())
    spec.update(
        quit_points=1,
        crime_weights=[0, 1],
        resource_weights=[0, 1],
        challenges=[
            {"id": "baseline"},
            {"id": "half_information", "information_retained": 0.5},
            {"id": "combined_stress", "report_dependence": 0.8, "information_retained": 0.5, "coupling": 0.8},
        ],
    )
    report = runner.run(ROOT, tmp_path / "new", specification=spec)
    assert report["row_counts"]["decisions"] == 60
    assert report["row_counts"]["study_value"] == 360
    assert report["row_counts"]["grouped_evppi"] == 420
    assert report["summary"][0]["changed_policy_sets"] == 0
    assert report["summary"][1]["changed_policy_sets"] == 0
    assert report["conditioned"] is False
    with pytest.raises(FileExistsError, match="new output"):
        runner.run(ROOT, tmp_path / "new", specification=spec)


def test_invalid_and_duplicate_challenge_specs_rejected(runner) -> None:
    spec = json.loads((ROOT / "configs/m2_robustness.json").read_text())
    spec["challenges"] = [{"id": "baseline"}, {"id": "baseline"}]
    with pytest.raises(ValueError, match="Unique"):
        runner.validate_spec(ROOT, spec)
    spec["challenges"] = [{"id": "baseline", "coupling": 0}]
    with pytest.raises(ValueError, match="unchanged"):
        runner.validate_spec(ROOT, spec)
    spec["challenges"] = [{"id": "baseline"}]
    spec["crime_weights"] = [1, 0]
    with pytest.raises(ValueError, match="increasing"):
        runner.validate_spec(ROOT, spec)
    spec["crime_weights"] = [0, 1]
    spec["challenges"].append({"id": "invented", "target_effect": 0.1})
    with pytest.raises(jsonschema.ValidationError, match="Additional properties"):
        runner.validate_spec(ROOT, spec)


def test_challenge_regret_requires_the_actual_baseline_profile(runner) -> None:
    from tobac.regulation import load_config  # noqa: PLC0415 -- Fixed finite reference setup.

    spec = json.loads((ROOT / "configs/m2_robustness.json").read_text())
    spec.update(quit_points=1, crime_weights=[0, 1], resource_weights=[0, 1])
    retail = json.loads((ROOT / "configs/m2_retail.json").read_text())
    publication = json.loads((ROOT / "configs/m2_publication.json").read_text())
    with pytest.raises(ValueError, match="Complete baseline"):
        runner.case_rows(
            (load_config(ROOT / "configs/regulatory.json"), retail, spec),
            retail["cases"][0],
            {"id": "other"},
            {},
            publication,
        )
