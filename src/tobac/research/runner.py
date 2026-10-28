"""Reproducible M3 research-design experiment using the unchanged M2 models."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
from typing import TYPE_CHECKING, cast

import numpy as np
import scipy

from tobac._core import exact_evpi, exact_partial_information
from tobac.evidence import Belief, EvidencePacket, Scope, condition, state_identifiers
from tobac.information import joint_likelihood
from tobac.regulation import grouped_labels, load_config
from tobac.retail_case import build_retail_states, retail_channels, retail_problem

from .implementation import adoption_kernel, decomposition, discounted_uptake, implementation_values
from .portfolio import Costs, Source, portfolio_value
from .robust import envelope
from .staged import staged_portfolio
from .structure import structure_value
from .voiage_adapter import partition_problem, uniform_equivalent

if TYPE_CHECKING:
    from tobac._typing import FloatArray, Report

DESIGNS = {
    "none": [],
    "calibration_only": ["calibration"],
    "supply": ["legal_supply"],
    "panel": ["anabasine", "nicotine"],
    "panel_supply": ["anabasine", "nicotine", "legal_supply"],
    "calibration_panel_supply": ["calibration", "anabasine", "nicotine", "legal_supply"],
    "improved_panel_supply": ["anabasine_improved", "nicotine", "legal_supply"],
    "total_causal": ["policy_comparison"],
    "matched_causal": ["policy_comparison", "policy_lawful_comparison"],
    "linked": ["anabasine", "nicotine", "legal_supply", "policy_comparison", "policy_lawful_comparison"],
    "criminal_harm": ["criminal_harm_research"],
    "causal_and_harm": ["policy_comparison", "criminal_harm_research"],
}


# Named bounds preserve the existing scientific/data contract.
INVARIANT_ATOL = 1e-11
REFERENCE_HIGH_PROBABILITY = 0.5


def write_csv(path: Path, rows: list[Report]) -> None:
    """Write a report table with a stable union of its declared columns."""
    if not rows:
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            {
                k: json.dumps(v, sort_keys=True) if isinstance(v, (dict, list, tuple)) else v
                for k, v in r.items()
            }
            for r in rows
        )


def run(config_path: str | Path, out: str | Path, *, quick: bool = False) -> Report:  # noqa: C901, PLR0912, PLR0915  # Keep ordered model validation and report assembly in one visible operation.; Keep explicit fail-closed validation branches together.; Keep the declared numerical/report sequence visible and ordered.
    """Run the declared analysis and write provenance-bound outputs."""
    root = Path.cwd().resolve()
    path = Path(config_path).resolve()
    cfg = json.loads(path.read_text(encoding="utf-8"))
    if cfg["schema"] != "tobac.research-m3.v1":
        msg = "Unknown M3 schema"
        raise ValueError(msg)
    base = load_config(root / cfg["base_config"])
    retail_path = root / cfg["retail_config"]
    rc = json.loads(retail_path.read_text(encoding="utf-8"))
    cases = rc["cases"]
    if quick:
        cases = [c for c in cases if c["id"] == "source_shape_partial_replacement"]
    priors = [0.5] if quick else cfg["prior_high_illicit_probabilities"]
    weights = [1.0] if quick else cfg["normative_crime_weights"]
    if any(not 0 < p < 1 for p in priors):
        msg = "Prior-scenario probabilities must be interior"
        raise ValueError(msg)
    dest = Path(out)
    if dest.exists() and any(dest.iterdir()):
        msg = "Use a new result directory"
        raise FileExistsError(msg)
    dest.mkdir(parents=True, exist_ok=True)
    rows: list[Report] = []
    partials: list[Report] = []
    increments: list[Report] = []
    impl: list[Report] = []
    cells: list[Report] = []
    stages: list[Report] = []
    stage_branches: list[Report] = []
    d0: list[Report] = []
    checks: list[bool] = []
    ref = None
    scope = Scope(
        "M2 synthetic representative catchment",
        "M2 declared exposure denominator",
        "2025-01-01",
        "2025-12-31",
        "cigarette_equivalents/1000/day",
    )
    for case in cases:
        s, p, c = build_retail_states(
            base,
            quit_points=cfg["quit_points"],
            transport=case["transport"],
            null_weight=case["null_weight"],
            source_beta=rc["source_beta"],
        )
        ids = state_identifiers(s)
        channels = retail_channels(s, c)
        assets = {
            key: (
                ("lab_setup",)
                if key in ("anabasine", "anabasine_improved", "nicotine")
                else ("causal_protocol",)
                if key.startswith("policy_")
                else ()
            )
            for key in cfg["direct_costs"]
        }
        sources = {
            key: Source(
                key,
                channels[key],
                ("future:" + ("anabasine" if key == "anabasine_improved" else key),),
                ids,
                assets[key],
            )
            for key in cfg["direct_costs"]
        }
        for high_probability in priors:
            # Explicit sensitivity, not a fitted posterior or a viewpoint probability.
            high = s["illicit"] == np.max(s["illicit"])
            wp = p * np.where(high, 2 * high_probability, 2 * (1 - high_probability))
            wp /= wp.sum()
            for cw in weights:
                pr = retail_problem(s, wp, c, cw, lawful_replacement=case["lawful_replacement"])
                b = Belief(pr, ids, scope)
                costs = Costs(pr.value_unit, cfg["direct_costs"], cfg["shared_costs"])
                scenario = f"{case['id']}|P_high_illicit={high_probability:g}"
                tag = {
                    "scenario": scenario,
                    "case": case["id"],
                    "prior_high_illicit": high_probability,
                    "crime_weight": cw,
                }
                evpi = exact_evpi(pr)
                trans = uniform_equivalent(pr)
                error = abs(float(np.mean(np.max(trans, axis=1)) - np.max(np.mean(trans, axis=0))) - evpi)
                checks.append(error < INVARIANT_ATOL)
                results: dict[str, Report] = {}
                for design, keys in DESIGNS.items():
                    r = portfolio_value(b, [sources[k] for k in keys], costs)
                    rows.append(
                        dict(
                            tag,
                            design=design,
                            evsi=r["evsi"],
                            cost=r["cost"],
                            enbs=r["enbs"],
                            evpi=evpi,
                            probability_action_changes=r["probability_action_changes"],
                            min_effective_states=r["minimum_effective_states"],
                            value_unit=pr.value_unit,
                        )
                    )
                    results[design] = r
                    checks.extend(
                        [
                            r["evsi"] >= -INVARIANT_ATOL,
                            r["evsi"] <= evpi + 1e-11,
                            r["posterior_martingale_max_error"] < INVARIANT_ATOL,
                        ]
                    )
                for group in [
                    "market",
                    "behaviour",
                    "criminal_harm",
                    "implementation",
                    "measurement",
                    "baseline_reachable",
                ]:
                    labels = grouped_labels(s, c, group)
                    g = partition_problem(pr, labels)
                    v = exact_evpi(g)
                    checks.append(abs(v - exact_partial_information(pr, labels)) < INVARIANT_ATOL)
                    partials.append(dict(tag, group=group, evppi=v, value_unit=pr.value_unit))
                for more, less in [
                    ("calibration_panel_supply", "panel_supply"),
                    ("improved_panel_supply", "panel_supply"),
                    ("linked", "matched_causal"),
                ]:
                    delta = results[more]["evsi"] - results[less]["evsi"]
                    dc = results[more]["cost"] - results[less]["cost"]
                    increments.append(
                        dict(
                            tag,
                            added_to=less,
                            combined=more,
                            incremental_evsi=delta,
                            incremental_cost=dc,
                            incremental_enbs=delta - dc,
                            value_unit=pr.value_unit,
                        )
                    )
                    checks.append(delta >= -INVARIANT_ATOL)
                if (
                    case["id"] == "source_shape_partial_replacement"
                    and high_probability == REFERENCE_HIGH_PROBABILITY
                    and cw == 1
                ):
                    ref = (s, p, c, pr, b, channels, sources, costs)
    if ref is None:
        msg = "Required reference scenario absent"
        raise ValueError(msg)
    s, p, c, pr, b, _ch, sources, costs = ref
    # Explicit model-probability sensitivity only. Never use these weights to pool the robustness scenarios.
    model0 = retail_problem(s, p, c, 1.0, lawful_replacement=0.0)
    model1 = retail_problem(s, p, c, 1.0, lawful_replacement=1.0)
    structural: list[Report] = []
    for w in cfg["structure_probability_grid"]:
        r = structure_value({"no_lawful_replacement": model0, "full_lawful_replacement": model1}, [w, 1 - w])
        structural.append(dict(probability_first_model=w, **r))
        checks.extend(
            [r["structure_only"] >= -INVARIANT_ATOL, r["remaining_parameter_value"] >= -INVARIANT_ATOL]
        )
    # Possible baseline supply outcomes, not actual NZ D0. New analysis uses posterior Belief and
    # rejects the old data IDs.
    old = sources["legal_supply"]
    q = old.likelihood @ cast("FloatArray", pr.prior_weights)
    for y, mass in enumerate(q):
        if mass <= 0:
            continue
        with np.errstate(divide="ignore"):
            logl = np.log(old.likelihood[y])
        packet = EvidencePacket(
            f"synthetic-D0-{y}",
            old.data_ids,
            ("synthetic_report_fixture",),
            b.state_ids,
            logl,
            scope,
            scope,
            "possible supply-report category; not field data",
        )
        post = condition(b, packet)
        rr = portfolio_value(post, [sources["anabasine"], sources["nicotine"]], costs)
        d0.append(
            {
                "possible_supply_outcome": y,
                "prior_predictive_probability": float(mass),
                "conditional_panel_evsi": rr["evsi"],
                "remaining_evpi": rr["evpi"],
                "status": "possible D0 fixture, not an assimilated NZ observation",
            }
        )
    expected_extra = sum(x["prior_predictive_probability"] * x["conditional_panel_evsi"] for x in d0)
    combined = portfolio_value(b, [sources[k] for k in DESIGNS["panel_supply"]], costs)
    first = portfolio_value(b, [old], costs)
    checks.append(abs(expected_extra - (combined["evsi"] - first["evsi"])) < INVARIANT_ATOL)
    # Implementation fractions are scenario-weighted parts of the same valued horizon, not extra
    # years/population.
    for profile, trajectory in cfg["uptake_profiles"].items():
        fraction = discounted_uptake(trajectory, cfg["time_weights"])
        kernel = adoption_kernel(
            pr, fraction, reference_action=pr.action_names.index(cfg["implementation_reference_action"])
        )
        effective = implementation_values(pr, kernel)
        cells.append(dict(profile=profile, effective_uptake=fraction, **decomposition(pr, kernel)))
        eb = Belief(effective, b.state_ids, b.scope, b.used_data_ids, b.receipts)
        for design in ["panel_supply", "calibration_panel_supply", "matched_causal", "linked"]:
            r = portfolio_value(eb, [sources[k] for k in DESIGNS[design]], costs)
            impl.append(
                {
                    "profile": profile,
                    "effective_uptake": fraction,
                    "design": design,
                    "evsi": r["evsi"],
                    "cost": r["cost"],
                    "enbs": r["enbs"],
                    "value_unit": pr.value_unit,
                }
            )
    # A pilot comprises the panel+baseline supply; follow-up is a matched causal comparison. Costs use
    # shared assets.
    pilot_sources = [sources[k] for k in DESIGNS["panel_supply"]]
    next_sources = [sources[k] for k in DESIGNS["matched_causal"]]
    _ = joint_likelihood(*(x.likelihood for x in pilot_sources))
    _ = joint_likelihood(*(x.likelihood for x in next_sources))
    ca = costs.price(pilot_sources)
    _ = costs.price(pilot_sources + next_sources) - ca
    for timing in cfg["stage_timings"]:
        for multiplier in cfg["stage_followup_cost_multipliers"]:
            r = staged_portfolio(
                b,
                pilot_sources,
                next_sources,
                costs,
                followup_cost_multiplier=multiplier,
                pilot_remaining=timing["pilot_remaining"],
                followup_remaining=timing["followup_remaining"],
            )
            tag = {"timing": timing["name"], "followup_cost_multiplier": multiplier}
            stages.append(dict(tag, **{k: v for k, v in r.items() if k != "branches"}))
            stage_branches.extend(dict(tag, **branch) for branch in r["branches"])
            checks.extend(
                [
                    r["adaptive_enbs"] >= max(r["pilot_only_enbs"], r["fixed_both_enbs"]) - 1e-11,
                    r["best_with_no_study"] >= 0,
                ]
            )
    envelopes: list[Report] = []
    for cw in weights:
        envelopes.extend(
            dict(crime_weight=cw, **x) for x in envelope([r for r in rows if r["crime_weight"] == cw])
        )
    tables = {
        "study_portfolios.csv": rows,
        "grouped_evppi.csv": partials,
        "conditional_increments.csv": increments,
        "robust_envelopes.csv": envelopes,
        "structure_only_curve.csv": structural,
        "d0_conditional_values.csv": d0,
        "implementation_values.csv": impl,
        "implementation_four_cells.csv": cells,
        "staged_designs.csv": stages,
        "stage_branches.csv": stage_branches,
    }
    for name, data in tables.items():
        write_csv(dest / name, data)
    validation = {
        "all_invariants_passed": bool(all(checks)),
        "invariant_count": len(checks),
        "scenario_decisions": len(rows) // len(DESIGNS),
        "designs": len(DESIGNS),
        "reference_states": len(p),
        "prior_structure_scenario_probabilities": "not supplied or averaged",
        "external_libraries_executed": False,
        "value_scope": cfg["cost_scope"],
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "finite_model_scope": cfg["status"],
    }
    (dest / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    inputs = {
        f.relative_to(root).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
        for f in (root / "src/tobac").rglob("*.py")
    }
    for f in (path, root / cfg["base_config"], retail_path):
        inputs[f.relative_to(root).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    outputs = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in dest.iterdir() if f.is_file()}
    (dest / "manifest.json").write_text(
        json.dumps({"schema": "tobac.run.v1", "inputs": inputs, "outputs": outputs}, indent=2) + "\n",
        encoding="utf-8",
    )
    if not all(checks):
        msg = "M3 exact invariants failed"
        raise ArithmeticError(msg)
    return validation


def main() -> None:
    """Parse command-line options, execute the selected operation and report its result."""
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/m3_research.json")
    p.add_argument("--out", required=True)
    p.add_argument("--quick", action="store_true")
    args = p.parse_args()
    print(json.dumps(run(args.config, args.out, quick=args.quick), indent=2))  # noqa: T201  # CLI emits the requested structured result on stdout.


if __name__ == "__main__":
    main()
