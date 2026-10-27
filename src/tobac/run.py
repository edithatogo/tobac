"""Reproduce the regulatory uncertainty milestone without modifying old outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy

from tobac._core import exact_evpi, exact_partial_information
lazy from tobac._typing import Report

from .information import evaluate, same_data_robustness, scalar_oracle
from .regulation import (
    ACTIONS,
    build_states,
    grouped_labels,
    load_config,
    make_problem,
    policy_components,
    studies,
    study_channels,
)

# Named bounds preserve the existing scientific/data contract.
REFERENCE_OTHER_NICOTINE_MG = 150.0
INVARIANT_ATOL = 1e-10
INVARIANT_ATOL_1e_12 = 1e-12


def write_csv(path: Path, rows: list[Report]) -> None:
    """Write a report table with a stable union of its declared columns."""
    if not rows:
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def run(config_path: str | Path, out: str | Path, quick: bool = False) -> Report:  # noqa: C901, FBT001, FBT002, PLR0915  # Keep ordered model validation and report assembly in one visible operation.; Preserve the established public positional flag convention.; Keep the declared numerical/report sequence visible and ordered.
    """Run the declared analysis and write provenance-bound outputs."""
    c = load_config(config_path)
    out = Path(out)
    root = Path.cwd().resolve()
    config_relative = Path(config_path).resolve().relative_to(root)
    confidence = c["scientific_event"]["confidence"]
    if out.exists() and any(out.iterdir()):
        msg = "Use a new empty output directory"
        raise FileExistsError(msg)
    out.mkdir(parents=True, exist_ok=True)
    s, p0 = build_states(c)
    d = policy_components(s, c)
    channels = study_channels(s, c)
    designs = studies(channels)
    event = (d["illicit"][:, 1] - d["illicit"][:, 0]) / s["tobacco"] >= c["scientific_event"][
        "minimum_absolute_growth_fraction"
    ]
    current_event = (
        s["tobacco"] * s["illicit"] >= REFERENCE_OTHER_NICOTINE_MG
    )  # explicitly illustrative scientific magnitude
    groups = [
        "market",
        "behaviour",
        "criminal_harm",
        "health_consequences",
        "implementation",
        "measurement",
        "baseline_reachable",
    ]
    targets = {
        "current_illicit_share": s["illicit"],
        "current_illicit_volume": s["tobacco"] * s["illicit"],
        "current_total_tobacco": s["tobacco"],
        "future_diversion": s["diversion"],
        "criminal_externality": s["crime"],
    }
    cases = [(name, params, 0.0) for name, params in c["prior_scenarios"].items()]
    if not quick:
        cases += [(name, {}, a) for name, a in c["dependence_scenarios"].items() if a]
    else:
        cases = cases[:1]
    summaries: list[Report] = []
    partials: list[Report] = []
    infos: list[Report] = []
    science: list[Report] = []
    ledgers: list[Report] = []
    prices: list[Report] = []
    incremental: list[Report] = []
    checks: list[bool] = []
    by_reference: dict[str, Report] = {}
    for name, prior_args, association in cases:
        _, p = build_states(c, prior_args, association)
        for weight in [1.0] if quick else c["crime_weights"]:
            pr = make_problem(s, p, c, weight)
            a0 = int(np.argmax(p @ pr.values))
            ep = exact_evpi(pr)
            base = {"prior": name, "crime_weight": weight}
            summaries.append(
                dict(
                    base,
                    prior_action=ACTIONS[a0],
                    evpi=ep,
                    **{a: float(p @ pr.values[:, j]) for j, a in enumerate(ACTIONS)},
                )
            )
            ledgers.extend(
                (
                    dict(base, action=a, **{k: float(p @ v[:, j]) for k, v in d.items()})
                    for j, a in enumerate(ACTIONS)
                )
            )
            pv: dict[str, float] = {}
            for group in groups:
                pv[group] = exact_partial_information(pr, grouped_labels(s, c, group))
                partials.append(
                    dict(
                        base,
                        parameter_group=group,
                        evppi=pv[group],
                        scope="exact EVPPI for declared finite variables, not estimated continuous EVPPI",
                    )
                )
            scores: dict[str, float] = {}
            for design, likelihood_matrix in designs.items():
                r = evaluate(
                    pr,
                    likelihood_matrix,
                    targets if weight == 1 else None,
                    event=event,
                    confidence=confidence,
                )
                scores[design] = r["evsi"]
                infos.append(
                    dict(
                        base,
                        design=design,
                        **{k: v for k, v in r.items() if k not in ("targets", "method", "value_unit")},
                    )
                )
                if weight == 1:
                    rc = evaluate(pr, likelihood_matrix, event=current_event, confidence=confidence)
                    science.extend(
                        (dict(base, design=design, target=target, **v) for target, v in r["targets"].items())
                    )
                    science.extend(
                        (
                            dict(
                                base,
                                design=design,
                                target="current_illicit_volume_ge_150",
                                resolution_probability=rc["resolution_probability"],
                                prior_event_probability=rc["prior_event_probability"],
                                event_brier_risk=rc["event_brier_risk"],
                            ),
                            dict(
                                base,
                                design=design,
                                target="policy_causes_material_absolute_illicit_growth",
                                resolution_probability=r["resolution_probability"],
                                prior_event_probability=r["prior_event_probability"],
                                event_brier_risk=r["event_brier_risk"],
                            ),
                        )
                    )
                if name == "balanced" and weight == 1:
                    by_reference[design] = r
                    for scale in c["monetary_scales_nzd_per_unit"]:
                        prices.extend(
                            {
                                "design": design,
                                "assumed_nzd_per_normalised_unit": scale,
                                "gross_value_nzd": r["evsi"] * scale,
                                "assumed_study_cost_nzd": cost,
                                "enbs_nzd": r["evsi"] * scale - cost,
                                "scope": (
                                    "normative monetary scale and hypothetical price; not NZ benefit "
                                    "estimate or quote"
                                ),
                            }
                            for cost in c["conditional_study_cost_grid_nzd"]
                        )
                checks.extend(
                    (
                        r["evsi"] >= -INVARIANT_ATOL and r["evsi"] <= ep + 1e-10,
                        r["posterior_martingale_max_error"] < INVARIANT_ATOL,
                    )
                )
            incremental.extend(
                (
                    dict(
                        base,
                        existing_information=first,
                        combined_information=second,
                        incremental_evsi=scores[second] - scores[first],
                        scope=(
                            "prospective marginal information; for observed baseline data "
                            "condition prior once first"
                        ),
                    )
                    for first, second in [
                        ("panel", "panel_supply"),
                        ("supply", "panel_supply"),
                        ("panel_supply", "better_quantification_supply"),
                        ("panel_supply", "calibration_panel_supply"),
                        ("causal_policy_study", "causal_and_harm"),
                    ]
                )
            )
            checks.append(scores["panel_supply"] <= pv["baseline_reachable"] + 1e-10)
    # Common-data robustness, not a comparison of different simulated datasets.
    pr = make_problem(s, p0, c)
    priors = [build_states(c, {"diversion": q})[1] for q in (0.2, 0.5, 0.8)]
    robust: list[Report] = []
    robust.extend(
        (
            dict(
                design=design,
                **same_data_robustness(
                    pr.values, priors, p0, likelihood_matrix, event, confidence=confidence
                ),
            )
            for design, likelihood_matrix in designs.items()
        )
    )
    oracle = scalar_oracle(pr, designs["panel_supply"])
    vector = evaluate(pr, designs["panel_supply"])["evsi"]
    checks.append(abs(oracle - vector) < INVARIANT_ATOL_1e_12)
    # Independent Monte Carlo over *exact outcome* probabilities: integration check.
    likelihood_matrix = designs["panel_supply"]
    j = likelihood_matrix * p0
    prob = j.sum(1)
    post = j / prob[:, None]
    a0 = np.argmax(p0 @ pr.values)
    g = np.max(post @ (pr.values - pr.values[:, a0, None]), axis=1)
    draws = np.random.default_rng(20261024).choice(len(prob), size=50000, p=prob)
    mc = g[draws]
    se = mc.std(ddof=1) / np.sqrt(len(mc))
    checks.append(abs(mc.mean() - vector) < 5 * se + 1e-12)
    outputs = {
        "decision_summary.csv": summaries,
        "grouped_evppi.csv": partials,
        "study_value.csv": infos,
        "scientific_learning.csv": science,
        "same_data_robustness.csv": robust,
        "consequence_ledgers.csv": ledgers,
        "conditional_price_frontier.csv": prices,
        "incremental_information.csv": incremental,
    }
    for f, rows in outputs.items():
        write_csv(out / f, rows)
    validation = {
        "passed": bool(all(checks)),
        "checks": len(checks),
        "states": len(p0),
        "cases": len(cases),
        "designs": len(designs),
        "exact_oracle_error": abs(oracle - vector),
        "mc_check_estimate": float(mc.mean()),
        "mc_check_se": float(se),
        "exact_reference_evsi": vector,
        "method": "exact finite prior and coarsened outcomes; MC used only as independent check",
        "scope": "conditional research; not current NZ posterior or policy recommendation",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    (out / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    # Hash the executed package, including installed-wheel invocations. Map it
    # to project source paths so the verifier checks source/install parity.
    package = Path(__file__).resolve().parent
    inputs = {
        (Path("src/tobac") / p.relative_to(package)).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in package.rglob("*.py")
    }
    inputs[config_relative.as_posix()] = hashlib.sha256(Path(config_path).read_bytes()).hexdigest()
    hashes = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file()
    }
    (out / "manifest.json").write_text(
        json.dumps({"schema": "tobac.run.v1", "inputs": inputs, "outputs": hashes}, indent=2) + "\n",
        encoding="utf-8",
    )
    if not all(checks):
        msg = "A numerical invariant failed; inspect outputs"
        raise ArithmeticError(msg)
    return validation


def main() -> None:
    """Parse command-line options, execute the selected operation and report its result."""
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/regulatory.json")
    p.add_argument("--out", required=True)
    p.add_argument("--quick", action="store_true")
    a = p.parse_args()
    print(json.dumps(run(a.config, a.out, a.quick), indent=2))  # noqa: T201  # CLI emits the requested structured result on stdout.


if __name__ == "__main__":
    main()
