"""Execute post-primary finite assumption challenges without empirical conditioning."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from typing import TYPE_CHECKING

import jsonschema
import numpy as np
from qualify_m2_pathway import checkout_identity
from run_m2_publication import source_audit, write_table
from source_handoff import digest, read

from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
from tobac.information import evaluate
from tobac.regulation import ACTIONS, grouped_labels, load_config
from tobac.retail_case import build_retail_states, retail_channels, retail_components, retail_studies
from tobac.robustness import binary_prior, dependent_joint, frechet_prior, garble, tie_regret
from tobac.value_sensitivity import ATOL, VALUE_UNIT, Consequences, ValueWeights, optimal_indices

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from tobac._typing import Config, FloatArray, Report, StateArrays

ROOT = Path(__file__).resolve().parents[1]
CONFIG = "configs/m2_robustness.json"
SCHEMA = "engineering/schemas/m2-robustness.schema.json"
COMPONENTS = {
    "panel_supply": ("anabasine", "nicotine", "legal_supply"),
    "better_quantification_supply": ("anabasine_improved", "nicotine", "legal_supply"),
    "calibration_panel_supply": ("calibration", "anabasine", "nicotine", "legal_supply"),
    "causal_matched_total_and_lawful": ("policy_comparison", "policy_lawful_comparison"),
}


def validate_spec(root: Path, specification: Report) -> None:
    """Require explicit bounded challenge supports and one unchanged first baseline."""
    jsonschema.validate(specification, read(root / SCHEMA))
    challenges = specification["challenges"]
    if challenges[0] != {"id": "baseline"} or len({c["id"] for c in challenges}) != len(challenges):
        msg = "Unique challenge IDs and unchanged first baseline required"
        raise ValueError(msg)
    for name in ("crime_weights", "resource_weights"):
        if not (np.diff(specification[name]) > 0).all():
            msg = "Strictly increasing finite normative supports required"
            raise ValueError(msg)


def challenge_reports(channels: StateArrays, prior: FloatArray, challenge: Report) -> StateArrays:
    """Preserve declared design membership while challenging joint errors and information."""
    reports = retail_studies(channels)
    dependence = challenge.get("report_dependence", 0)
    for name, components in COMPONENTS.items():
        reports[name] = dependent_joint(tuple(channels[c] for c in components), dependence)
    return {
        name: garble(channel, prior, challenge.get("information_retained", 1))
        for name, channel in reports.items()
    }


def challenge_inputs(
    base: Config, retail: Report, case: Report, specification: Report, challenge: Report
) -> tuple[StateArrays, FloatArray, Config]:
    """Change declared assumptions on the same finite state identity and supports."""
    states, prior, config = build_retail_states(
        base,
        quit_points=specification["quit_points"],
        transport=case["transport"],
        null_weight=challenge.get("null_weight", case["null_weight"]),
        source_beta=retail["source_beta"],
    )
    for name, probability in challenge.get("high_probabilities", {}).items():
        high = states[name] == states[name].max()
        prior = binary_prior(prior, high, probability)
    if "coupling" in challenge:
        prior = frechet_prior(
            prior,
            states["illicit"] == states["illicit"].max(),
            states["diversion"] == states["diversion"].max(),
            challenge["coupling"],
        )
    return states, prior, config


def profile_key(row: Report) -> tuple[str, float, float]:
    """Return stable scientific identity independent of a challenge identifier."""
    return str(row["case"]), float(row["crime_weight"]), float(row["resource_weight"])


def profile_information(
    problem: DecisionProblem, key: Report, labels: Mapping[str, Sequence[object]], reports: StateArrays
) -> tuple[list[Report], list[Report]]:
    """Compute grouped information before report EVSI under one declared objective."""
    evpi = exact_evpi(problem)
    groups: list[Report] = []
    for group, partition in labels.items():
        value = exact_partial_information(problem, partition)
        if not -ATOL <= value <= evpi + ATOL:
            msg = "Challenge grouped information outside EVPI bounds"
            raise ArithmeticError(msg)
        groups.append(dict(key, group=group, evppi=value))
    studies: list[Report] = []
    for design, channel in reports.items():
        result = evaluate(problem, channel)
        if not -ATOL <= result["evsi"] <= evpi + ATOL or result["posterior_martingale_max_error"] > ATOL:
            msg = "Challenge study information invariant failed"
            raise ArithmeticError(msg)
        studies.append(dict(key, design=design, evsi=result["evsi"], evpi=evpi))
    return groups, studies


def check_garbling(problem: DecisionProblem, studies: list[Report], originals: StateArrays) -> None:
    """Check the decision-value data-processing inequality for fixed-prior garbling."""
    for row in studies:
        original = evaluate(problem, originals[row["design"]])["evsi"]
        if row["evsi"] > original + ATOL:
            msg = "Garbling increased decision value"
            raise ArithmeticError(msg)


def case_rows(
    inputs: tuple[Config, Report, Report],
    case: Report,
    challenge: Report,
    baseline: dict[tuple[str, float, float], Report],
    publication: Report,
) -> dict[str, list[Report]]:
    """Enumerate the same objectives with joint-prior and report assumptions explicit."""
    base, retail, specification = inputs
    groups, designs = publication["groups"], publication["designs"]
    states, prior, config = challenge_inputs(base, retail, case, specification, challenge)
    physical = retail_components(states, config, lawful_replacement=case["lawful_replacement"])
    table = Consequences(physical["health_gain"], physical["criminal_harm_change"], physical["resource_cost"])
    channels = retail_channels(states, config)
    original_reports = retail_studies(channels)
    reports = challenge_reports(channels, prior, challenge)
    reports = {name: reports[name] for name in designs}
    rows: dict[str, list[Report]] = {
        k: [] for k in ("decisions", "grouped_evppi", "study_value", "scientific_information")
    }
    labels = {group: grouped_labels(states, config, group) for group in groups}
    targets = {target: states[target] for target in ("net_cessation", "diversion", "crime")}
    for design in designs:
        information = evaluate(table.problem(prior), reports[design], targets)["targets"]
        for target, statistics in information.items():
            rows["scientific_information"].append(
                dict(challenge=challenge["id"], case=case["id"], design=design, target=target, **statistics)
            )
    for crime in specification["crime_weights"]:
        for resource in specification["resource_weights"]:
            key: Report = {
                "challenge": challenge["id"],
                "case": case["id"],
                "crime_weight": crime,
                "resource_weight": resource,
            }
            problem = table.problem(prior, ValueWeights(1, crime, resource), ACTIONS)
            expected = prior @ problem.values
            optima = optimal_indices(expected)
            reference = baseline.get(profile_key(key))
            previous = (
                optima
                if reference is None
                else tuple(ACTIONS.index(a) for a in str(reference["cooptimal_actions"]).split(";"))
            )
            low, high = tie_regret(expected, previous)
            evpi = exact_evpi(problem)
            row = dict(
                key,
                cooptimal_actions=";".join(ACTIONS[i] for i in optima),
                best_expected_value=float(expected.max()),
                evpi=evpi,
                baseline_regret_min=low,
                baseline_regret_max=high,
            )
            rows["decisions"].append(row)
            if challenge["id"] == "baseline":
                baseline[profile_key(key)] = row
            group_rows, studies = profile_information(problem, key, labels, reports)
            if challenge["id"] == "half_information":
                check_garbling(problem, studies, original_reports)
            rows["grouped_evppi"].extend(group_rows)
            rows["study_value"].extend(studies)
    return rows


def ranked(rows: list[Report], statistic: str, label: str) -> dict[tuple[str, float, float], tuple[str, ...]]:
    """Retain every gross-information co-optimum rather than selecting an arbitrary tie."""
    grouped: dict[tuple[str, float, float], list[Report]] = {}
    for row in rows:
        grouped.setdefault(profile_key(row), []).append(row)
    return {
        key: tuple(sorted(str(items[i][label]) for i in optimal_indices([r[statistic] for r in items])))
        for key, items in grouped.items()
    }


def summaries(tables: dict[str, list[Report]], challenges: list[Report]) -> list[Report]:
    """Compare matched profiles and retain regret over every original policy tie."""
    baseline = {profile_key(r): r for r in tables["decisions"] if r["challenge"] == "baseline"}
    original = {
        (profile_key(r), r["design"]): r for r in tables["study_value"] if r["challenge"] == "baseline"
    }
    reference_rank = ranked(
        [r for r in tables["study_value"] if r["challenge"] == "baseline"], "evsi", "design"
    )
    reference_group = ranked(
        [r for r in tables["grouped_evppi"] if r["challenge"] == "baseline"], "evppi", "group"
    )
    result: list[Report] = []
    for challenge in challenges:
        name = challenge["id"]
        decisions = [r for r in tables["decisions"] if r["challenge"] == name]
        studies = [r for r in tables["study_value"] if r["challenge"] == name]
        ranks = ranked(studies, "evsi", "design")
        group_ranks = ranked([r for r in tables["grouped_evppi"] if r["challenge"] == name], "evppi", "group")
        result.append(
            {
                "challenge": name,
                "compared_profiles": len(decisions),
                "changed_policy_sets": sum(
                    r["cooptimal_actions"] != baseline[profile_key(r)]["cooptimal_actions"] for r in decisions
                ),
                "disjoint_policy_sets": sum(
                    not set(str(r["cooptimal_actions"]).split(";"))
                    & set(str(baseline[profile_key(r)]["cooptimal_actions"]).split(";"))
                    for r in decisions
                ),
                "changed_gross_design_sets": sum(
                    value != reference_rank[key] for key, value in ranks.items()
                ),
                "changed_group_sets": sum(
                    value != reference_group[key] for key, value in group_ranks.items()
                ),
                "maximum_baseline_tie_regret": max(r["baseline_regret_max"] for r in decisions),
                "maximum_absolute_evsi_difference": max(
                    abs(r["evsi"] - original[profile_key(r), r["design"]]["evsi"]) for r in studies
                ),
            }
        )
    return result


def run(root: Path, out: Path, *, specification: Report | None = None) -> Report:
    """Run the declared post-primary challenges into a fresh directory."""
    if out.exists() and any(out.iterdir()):
        msg = "Use a new output directory"
        raise FileExistsError(msg)
    spec = read(root / CONFIG) if specification is None else specification
    validate_spec(root, spec)
    retail = read(root / "configs/m2_retail.json")
    publication = read(root / "configs/m2_publication.json")
    audit, _ = source_audit(root, publication["source_map"])
    base = load_config(root / retail["base_config"])
    tables: dict[str, list[Report]] = {
        k: [] for k in ("decisions", "grouped_evppi", "study_value", "scientific_information")
    }
    baseline: dict[tuple[str, float, float], Report] = {}
    for challenge in spec["challenges"]:
        for case in retail["cases"]:
            for name, rows in case_rows((base, retail, spec), case, challenge, baseline, publication).items():
                tables[name].extend(rows)
    tables["summary"] = summaries(tables, spec["challenges"])
    report: Report = {
        "passed": True,
        "python": platform.python_version(),
        "checkout": checkout_identity(root),
        "specification": spec,
        "value_unit": VALUE_UNIT,
        "conditioned": False,
        "empirically_validated": False,
        "source_audit": audit,
        "row_counts": {name: len(rows) for name, rows in tables.items()},
        "summary": tables["summary"],
        "no_requests_or_submissions": True,
    }
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        write_table(out / f"{name}.csv", rows)
    (out / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    inputs = [
        CONFIG,
        SCHEMA,
        "configs/m2_retail.json",
        "configs/m2_publication.json",
        retail["base_config"],
        "docs/research/M2_READINESS_PROTOCOL.md",
        "scripts/run_m2_robustness.py",
        "scripts/run_m2_publication.py",
        "evidence/m2/public_sources_20261027/manifest.json",
    ]
    hashes = {p.relative_to(root).as_posix(): digest(p) for p in (root / "src/tobac").glob("*.py")}
    hashes.update({name: digest(root / name) for name in inputs})
    manifest = {
        "schema": "tobac.run.v1",
        "inputs": hashes,
        "outputs": {p.name: digest(p) for p in out.iterdir() if p.is_file()},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    """Execute the fixed post-primary protocol; no external actions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(ROOT, args.out), indent=2, allow_nan=False))  # noqa: T201 -- Structured CLI receipt.


if __name__ == "__main__":
    main()
