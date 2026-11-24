"""Installed-consumer check for the inspection-conditioned Voiage handoff."""

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, replace
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path
from typing import Literal

import pyarrow as pa
import voiage
from voiage.experimental.censored_evsi import censored_sequential_evsi
from voiage.experimental.credal import credal_decisions
from voiage.experimental.paired_draws import paired_draw_bundle

import tobac
from tobac.evidence import Scope
from tobac.partial_identification import Interval
from tobac.strategic_inspection import (
    InspectionDecisionDraw,
    InspectionObservations,
    prepare_inspection_paired_draws,
    run_inspection_scenario,
)

Channel = Literal["border_seizure", "retail_inspection"]
CHANNELS: tuple[Channel, ...] = ("border_seizure", "retail_inspection")
SCOPE = Scope("NZ", "synthetic continuing consumers", "2026-01-01", "2026-12-31", "baseline share")


def digest(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def ratio(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def synthetic_value(draw: InspectionDecisionDraw) -> tuple[float, float]:
    switching = draw.switching
    assert switching is not None
    return float(8 * switching - 3), 0.0


def model(
    executable: Path,
    channel: Channel,
    detection_lower: Fraction,
    second_switching: Fraction,
    *,
    wrong_context: bool = False,
) -> list[InspectionDecisionDraw]:
    fiscal_template = json.loads((Path(__file__).parent / "fixtures/fiscal-nz-synthetic.json").read_bytes())
    scenario_id = f"synthetic-{channel}"
    calibration = digest(b"Synthetic qualification maps the game share to switching in this scope.")
    observations = InspectionObservations(
        SCOPE,
        "synthetic product",
        Interval(0.5, 0.5),
        Interval(0.25, 0.375),
        Interval(1, 1),
        Interval(1, 1),
        channel=channel,
        scenario_id=scenario_id,
        calibration_sha256=calibration,
    )
    states = (("draw-a", Fraction(1, 4)), ("draw-b", second_switching))
    draw_set_digest = digest(
        json.dumps(
            [scenario_id, str(detection_lower), [(name, str(switching)) for name, switching in states]]
        ).encode()
    )
    draws = []
    for draw_id, switching in states:
        fiscal = {
            **fiscal_template,
            "key": {
                **fiscal_template["key"],
                "scenario_id": scenario_id,
                "draw_id": draw_id,
                "replication_id": "rep-" + draw_id,
            },
            "draw_set_digest": draw_set_digest,
        }
        request = {
            "schema_version": "tobac-inspection/0.1",
            "scope": {
                "channel": channel,
                "scenario_id": scenario_id,
                "product": observations.product,
                "observations": asdict(SCOPE),
                "switching_measure": "evasion_among_continuing_consumers",
                "calibration_sha256": calibration,
            },
            "inspector_valuation": {
                "currency": "NZD",
                "price_year": 2026,
                "resource_basis": "public_expenditure",
            },
            "fiscal_packet": fiscal,
            "undetected_harm": ratio(Fraction(64)),
            "evasion_gain": ratio(Fraction(1)),
            "detected_loss": ratio(Fraction(3)),
            "detection": {"lower": ratio(detection_lower), "upper": ratio(Fraction(1))},
        }
        expected = observations
        if wrong_context:
            other = "retail_inspection" if channel == "border_seizure" else "border_seizure"
            expected = replace(observations, channel=other)
        result = run_inspection_scenario(executable, json.dumps(request).encode(), expected)
        assert result.evasion_support == (Fraction(1, 4), Fraction(1, 4) / detection_lower)
        draws.append(InspectionDecisionDraw(result, Fraction(1, 2), (1 - switching) / 2, 0.5))
    return draws


def evaluate(draws: list[InspectionDecisionDraw]) -> tuple[Fraction, list[str]]:
    handoff = prepare_inspection_paired_draws(draws, synthetic_value, value_unit="synthetic utility")
    assert [key["replication_id"] for key in handoff.fiscal_keys] == ["rep-draw-a", "rep-draw-b"]
    bundle = paired_draw_bundle(
        pa.Table.from_pylist(handoff.rows),
        dataset_id=handoff.dataset_id,
        strategy_ids=handoff.strategy_ids,
        weight_field="weight",
    )
    assay = {
        "action_id": "synthetic-assay",
        "limit": 0.0,
        "cutpoints": [],
        "outcome_ids": ["unavailable", "below-limit", "measured"],
        "states": [
            {"draw_id": "draw-b", "mean": 0.0, "standard_deviation": 1.0, "detection_probability": 0.0},
            {"draw_id": "draw-a", "mean": 0.0, "standard_deviation": 1.0, "detection_probability": 1.0},
        ],
    }
    result = censored_sequential_evsi(
        bundle,
        stages=[[assay]],
        perspective=handoff.perspective,
        subgroup_id=handoff.subgroup_id,
        max_branches=100,
    )
    assert result.status == "complete"
    assert result.draw_ids == ("draw-a", "draw-b")
    assert result.strategy_ids == handoff.strategy_ids
    assert (result.perspective, result.subgroup_id) == (handoff.perspective, handoff.subgroup_id)
    assert result.evsi is not None

    # This synthetic credal comparison varies the second draw's probability.
    # With two states each strategy's expected value is affine in that probability.
    parameter = "draw-b-weight"
    priors = pa.Table.from_pylist([{"parameter_id": parameter, "lower": 0.25, "upper": 0.75}])
    affine_values = []
    for strategy_id in handoff.strategy_ids:
        value_a, value_b = (
            float(row["net_benefit"]) for row in handoff.rows if row["strategy_id"] == strategy_id
        )
        affine_values.append(
            {
                "strategy_id": strategy_id,
                "parameter_id": parameter,
                "intercept": value_a,
                "coefficient": value_b - value_a,
            }
        )
    decision = credal_decisions(priors, pa.Table.from_pylist(affine_values), max_bases=10)
    assert decision["status"] == "feasible"
    undominated = decision["interval_undominated"]
    assert isinstance(undominated, list)
    return result.evsi, undominated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    args = parser.parse_args()
    assert sys.version_info[:3] == (3, 15, 2)
    assert version("voiage") == "3.1.0"
    for module in (tobac, voiage):
        assert Path(module.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    for channel in CHANNELS:
        try:
            model(args.executable, channel, Fraction(1, 2), Fraction(1, 2), wrong_context=True)
        except ValueError as error:
            assert "differs from the declared M2a context" in str(error)
        else:
            raise AssertionError("Mismatched channel was accepted")

        high_model = model(args.executable, channel, Fraction(1, 2), Fraction(1, 2))
        high, undominated = evaluate(high_model)
        middle, _ = evaluate(model(args.executable, channel, Fraction(1, 2), Fraction(3, 8)))
        assert (min(high, middle), max(high, middle)) == (0, Fraction(1, 2))
        fiscal = high_model[0].scenario.receipt["fiscal"]
        assert isinstance(fiscal, dict)
        assert undominated == [fiscal["key"]["strategy_id"], fiscal["comparator_strategy_id"]]
        try:
            evaluate(model(args.executable, channel, Fraction(2, 3), Fraction(1, 2)))
        except ValueError as error:
            assert "outside the matched observations and native switching support" in str(error)
        else:
            raise AssertionError("Draw outside the new native support was accepted")
        narrowed, undominated = evaluate(model(args.executable, channel, Fraction(2, 3), Fraction(3, 8)))
        assert narrowed == 0
        assert undominated == [fiscal["comparator_strategy_id"]]
        print(f"{channel} admitted finite-model EVSI range [0, {high}], narrowed range [0, {narrowed}]")
        print(f"{channel} only the comparator is interval-undominated after narrowing")


if __name__ == "__main__":
    main()
