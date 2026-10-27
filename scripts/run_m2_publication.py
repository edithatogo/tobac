"""Run the dated conditional publication analysis without empirical conditioning."""

from __future__ import annotations

import argparse
import csv
import json
import platform
from copy import deepcopy
from itertools import product
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, cast

import jsonschema
import numpy as np
from qualify_m2_pathway import checkout_identity
from qualify_m2_synthesis import csv_rows, supply_summary
from source_handoff import checked, digest, read, same_hash

from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
from tobac.information import evaluate
from tobac.regulation import ACTIONS, grouped_labels, load_config
from tobac.retail_case import build_retail_states, retail_channels, retail_components, retail_studies
from tobac.value_sensitivity import (
    ATOL,
    VALUE_UNIT,
    Consequences,
    ValueWeights,
    box_optima,
    crime_thresholds,
    optimal_indices,
)

if TYPE_CHECKING:
    from tobac._typing import Config, Report, StateArrays

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = "configs/m2_publication.json"
SCHEMA = "engineering/schemas/m2-publication.schema.json"


class _Validator(Protocol):
    def validate(self, instance: object) -> None: ...


def write_table(path: Path, rows: list[Report]) -> None:
    """Write stable LF tables; retain an explicit header for absent switch points."""
    columns = list(dict.fromkeys(k for row in rows for k in row))
    if not columns:
        columns = ["case", "resource_weight", "crime_weight", "cooptimal_actions"]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validated_documents(
    index: list[dict[str, str]], sources: list[dict[str, str]], extracts: list[dict[str, str]]
) -> dict[str, str]:
    """Check source/extraction identities, shared-data groups and no-adoption flags."""
    documents = {r["source_id"]: r["document_id"] for r in index}
    if (
        len(documents) != len(index)
        or len(sources) != len(index)
        or len(set(documents.values())) != len(index)
        or {r["source_id"] for r in sources} != set(documents)
    ):
        msg = "Unique matching source/document records required"
        raise ValueError(msg)
    if len({r["extraction_id"] for r in extracts}) != len(extracts):
        msg = "Unique extraction IDs required"
        raise ValueError(msg)
    for row in extracts:
        if documents.get(row["source_id"]) != row["document_id"]:
            msg = "Extraction source/document mismatch"
            raise ValueError(msg)
        if row["target_input_adopted"] != "false":
            msg = "No automatic public-extract adoption is permitted"
            raise ValueError(msg)
    if any(r["target_likelihood_adopted"] != "false" for r in sources):
        msg = "No automatic source likelihood adoption is permitted"
        raise ValueError(msg)
    for row in sources:
        group = next(r["underlying_data_group"] for r in index if r["source_id"] == row["source_id"])
        if row["underlying_data_group"] != group:
            msg = "Source/document underlying-data group mismatch"
            raise ValueError(msg)
    return documents


def source_audit(root: Path, directory: str) -> tuple[Report, list[Report]]:
    """Check catalogue eligibility without asserting possession of raw originals."""
    manifest = read(checked(root, f"{directory}/manifest.json"))
    required = {f"{directory}/{name}.csv" for name in ("source_index", "source_table", "extraction_table")}
    if not required <= manifest["sha256"].keys():
        msg = "All source tables require manifest hash bindings"
        raise ValueError(msg)
    for name, sha in manifest["sha256"].items():
        same_hash(root, name, sha)
    index = csv_rows(checked(root, f"{directory}/source_index.csv"))
    sources = csv_rows(checked(root, f"{directory}/source_table.csv"))
    extracts = csv_rows(checked(root, f"{directory}/extraction_table.csv"))
    documents = validated_documents(index, sources, extracts)
    uses = [
        {
            "source_id": r["source_id"],
            "document_id": documents[r["source_id"]],
            "underlying_data_group": r["underlying_data_group"],
            "model_use": "context_only_not_a_target_likelihood",
            "limitation": r.get("limitation", "See source table"),
        }
        for r in sources
    ]
    return {
        "documents": len(index),
        "extracts": len(extracts),
        "conditioned": False,
        "scope": "Metadata fixity/eligibility only;not fresh raw-object verification or target calibration",
    }, uses


def _empty_tables() -> dict[str, list[Report]]:
    return {
        name: []
        for name in (
            "consequences",
            "decisions",
            "grouped_evppi",
            "study_value",
            "thresholds",
            "robustness",
            "scientific_information",
        )
    }


def _information_rows(
    problem: DecisionProblem, inputs: tuple[StateArrays, Config, StateArrays], key: Report, spec: Report
) -> tuple[list[Report], list[Report]]:
    """Compute group information before report-design values under the same objective."""
    states, config, designs = inputs
    evpi = exact_evpi(problem)
    groups: list[Report] = []
    for group in spec["groups"]:
        value = exact_partial_information(problem, grouped_labels(states, config, group))
        if not -ATOL <= value <= evpi + ATOL:
            msg = "Group information outside EVPI bounds"
            raise ArithmeticError(msg)
        groups.append(dict(key, group=group, evppi=value))
    studies: list[Report] = []
    for name in spec["designs"]:
        result = evaluate(problem, designs[name])
        if not -ATOL <= result["evsi"] <= evpi + ATOL or result["posterior_martingale_max_error"] > ATOL:
            msg = "Conditional study-value invariant failed"
            raise ArithmeticError(msg)
        studies.append(
            dict(key, design=name, evsi=result["evsi"], evpi=evpi, gross_cost_ceiling=result["evsi"])
        )
    return groups, studies


def analyse_case(base: Config, retail: Report, case: Report, spec: Report) -> dict[str, list[Report]]:
    """Cross one declared structural/prior case with separate normative weights."""
    states, prior, config = build_retail_states(
        base,
        quit_points=spec["quit_points"],
        transport=case["transport"],
        null_weight=case["null_weight"],
        source_beta=retail["source_beta"],
    )
    physical = retail_components(states, config, lawful_replacement=case["lawful_replacement"])
    table = Consequences(physical["health_gain"], physical["criminal_harm_change"], physical["resource_cost"])
    means = table.expected(prior)
    designs = retail_studies(retail_channels(states, config))
    if set(spec["designs"]) - designs.keys():
        msg = "Unknown conditional report design"
        raise ValueError(msg)
    rows = _empty_tables()
    reference = table.problem(prior, names=ACTIONS)
    targets = {name: states[name] for name in ("net_cessation", "diversion", "crime")}
    for name in spec["designs"]:
        learning = evaluate(reference, designs[name], targets)["targets"]
        for target, statistics in learning.items():
            rows["scientific_information"].append(
                dict(case=case["id"], design=name, target=target, **statistics)
            )
    for i, action in enumerate(ACTIONS):
        rows["consequences"].append(
            dict(
                case=case["id"],
                action=action,
                **{
                    ("mean_state_illicit_share" if name == "illicit_share" else name): float(
                        prior @ values[:, i]
                    )
                    for name, values in physical.items()
                },
            )
        )
    for crime, resource in product(spec["crime_weights"], spec["resource_weights"]):
        weights = ValueWeights(1, crime, resource)
        problem = table.problem(prior, weights, ACTIONS)
        expected = prior @ problem.values
        key = {"case": case["id"], "crime_weight": crime, "resource_weight": resource}
        rows["decisions"].append(
            dict(
                key,
                cooptimal_actions=";".join(ACTIONS[i] for i in optimal_indices(expected)),
                best_expected_value=float(expected.max()),
                evpi=exact_evpi(problem),
            )
        )
        groups, studies = _information_rows(problem, (states, config, designs), key, spec)
        rows["grouped_evppi"].extend(groups)
        rows["study_value"].extend(studies)
    crime_bounds = (spec["crime_weights"][0], spec["crime_weights"][-1])
    resource_bounds = (spec["resource_weights"][0], spec["resource_weights"][-1])
    robust = box_optima(means, crime_bounds, resource_bounds)
    rows["robustness"].append(
        {
            "case": case["id"],
            "cooptimal_across_continuous_box": ";".join(ACTIONS[i] for i in robust),
            "crime_lower": crime_bounds[0],
            "crime_upper": crime_bounds[1],
            "resource_lower": resource_bounds[0],
            "resource_upper": resource_bounds[1],
        }
    )
    for resource in spec["resource_weights"]:
        for crime in crime_thresholds(means, resource, crime_bounds):
            values = means @ np.array([1, -crime, -resource])
            rows["thresholds"].append(
                {
                    "case": case["id"],
                    "resource_weight": resource,
                    "crime_weight": crime,
                    "cooptimal_actions": ";".join(ACTIONS[i] for i in optimal_indices(values)),
                }
            )
    return rows


def figures(out: Path, tables: dict[str, list[Report]]) -> None:
    """Render declared grid choices and one explicitly conditional study-value slice."""
    import matplotlib as mpl  # noqa: PLC0415 -- Plotting is a presentation-only dependency.

    mpl.use("Agg")
    import matplotlib.pyplot as plt  # noqa: PLC0415 -- Select the headless backend first.

    mpl.rcParams["svg.hashsalt"] = "tobac-m2-publication-20261028"
    colours = ("#555555", "#e69f00", "#0072b2", "#009e73")
    cases = list(dict.fromkeys(str(row["case"]) for row in tables["decisions"]))
    fig, axes = plt.subplots(1, len(cases), figsize=(18, 4), sharey=True, squeeze=False)
    axes = axes[0]
    for ax, case in zip(axes, cases, strict=True):
        for row in tables["decisions"]:
            if row["case"] == case:
                name = row["cooptimal_actions"]
                colour = colours[ACTIONS.index(name)] if name in ACTIONS else "#cc79a7"
                ax.scatter(row["crime_weight"], row["resource_weight"], color=colour, marker="s", s=75)
        ax.set(
            title=("Zero additional\nretail cessation" if case == "null_effect" else case.replace("_", "\n")),
            xlabel="Crime weight",
            xlim=(-0.2, 4.2),
            ylim=(-0.2, 4.2),
        )
        ax.grid(alpha=0.2)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    axes[0].set_ylabel("Resource-score weight; health weight = 1")
    for action, colour in zip(ACTIONS, colours, strict=True):
        axes[-1].scatter([], [], color=colour, marker="s", label=action.replace("_", " "))
    axes[-1].scatter([], [], color="#cc79a7", marker="s", label="co-optimal tie")
    axes[-1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), fontsize=7)
    fig.suptitle("Declared value-grid choices: points are scenarios, not preference probabilities")  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.38)
    fig.savefig(out / "decision_grid.png", dpi=180)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    fig.savefig(out / "decision_grid.svg", metadata={"Date": None})  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(11, 6))
    case = "source_shape_partial_replacement"
    designs = list(dict.fromkeys(str(row["design"]) for row in tables["study_value"]))
    for design in designs:
        rows = [
            r
            for r in tables["study_value"]
            if r["case"] == case and r["resource_weight"] == 1 and r["design"] == design
        ]
        ax.plot(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
            [r["crime_weight"] for r in rows], [r["evsi"] for r in rows], "o-", label=design.replace("_", " ")
        )
    ax.set(
        title="Source-shape/partial-replacement scenario; resource weight = 1",
        xlabel="Crime weight (health weight = 1)",
        ylabel="Gross conditional EVSI in normalised decision units",
    )
    ax.grid(alpha=0.2)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.legend(fontsize=8)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    fig.text(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        0.03,
        0.015,
        "Assumed finite priors and report performance; "
        "not NZD, priced studies or an empirical research ranking.",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(out / "study_value_slice.png", dpi=180)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    fig.savefig(out / "study_value_slice.svg", metadata={"Date": None})  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    plt.close(fig)


def validated_inputs(root: Path, spec: Report) -> tuple[Report, Report]:
    """Validate declared value support and inherited source roles before numerical use."""
    validator = cast("_Validator", jsonschema.Draft202012Validator(read(checked(root, SCHEMA))))
    validator.validate(spec)
    for name in ("crime_weights", "resource_weights"):
        values = np.asarray(spec[name], float)
        if not np.isfinite(values).all() or not (np.diff(values) > 0).all():
            msg = "Normative grid must be finite and strictly increasing"
            raise ValueError(msg)
    retail = read(checked(root, spec["retail_config"]))
    cases = retail["cases"]
    if (
        retail["schema"] != "tobac.m2.retail.v1"
        or not cases
        or len({c["id"] for c in cases}) != len(cases)
        or "none" not in spec["designs"]
    ):
        msg = "Unique nonempty retail cases and no-study comparator required"
        raise ValueError(msg)
    source_check = read(checked(root, "evidence/m2/publication_20261028/model_input_check.json"))
    same_hash(root, "evidence/m2/source_review.json", source_check["legacy_ledger_sha256"])
    source = read(checked(root, "evidence/m2/source_review.json"))["sources"][0]
    if retail["source_id"] != source["id"] or retail["source_beta"] != [
        source["finding"]["alpha"],
        source["finding"]["beta"],
    ]:
        msg = "Inherited transported model input differs from its source ledger"
        raise ValueError(msg)
    if (
        [source_check["alpha"], source_check["beta"]] != retail["source_beta"]
        or source_check["source_id"] != retail["source_id"]
        or source_check["independent_empirical_observation"] is not False
    ):
        msg = "Source-model check must preserve role and source values"
        raise ValueError(msg)
    return retail, source_check


def run(root: Path, out: Path, *, specification: Report | None = None, quit_points: int = 4) -> Report:
    """Write one fresh, source-bound conditional analysis with no external action."""
    if out.exists() and any(out.iterdir()):
        msg = "Use a new output directory"
        raise FileExistsError(msg)
    spec = read(checked(root, DEFAULT)) if specification is None else deepcopy(specification)
    retail, source_check = validated_inputs(root, spec)
    spec["quit_points"] = quit_points
    audit, uses = source_audit(root, spec["source_map"])
    base = load_config(checked(root, retail["base_config"]))
    tables = _empty_tables()
    for case in retail["cases"]:
        for name, rows in analyse_case(base, retail, case, spec).items():
            tables[name].extend(rows)
    robust_sets: list[set[str]] = [
        set(str(row["cooptimal_across_continuous_box"]).split(";")) - {""} for row in tables["robustness"]
    ]
    common = set(ACTIONS)
    for robust in robust_sets:
        common.intersection_update(robust)
    report: Report = {
        "passed": True,
        "python": platform.python_version(),
        "checkout": checkout_identity(root),
        "scientific_status": spec["scientific_status"],
        "value_unit": VALUE_UNIT,
        "conditioned": False,
        "empirically_validated": False,
        "ethics_status": (
            "Desk assessment only;formal applicability undetermined;no approval or exemption claimed"
        ),
        "equity_effects_identified": False,
        "decision_rows": len(tables["decisions"]),
        "study_rows": len(tables["study_value"]),
        "threshold_rows": len(tables["thresholds"]),
        "source_audit": audit,
        "transported_model_input": source_check,
        "scientific_information_rows": len(tables["scientific_information"]),
        "supply": supply_summary(root),
        "cooptimal_across_cases_and_continuous_box": sorted(common),
        "specification": spec,
        "no_requests_or_submissions": True,
    }
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        write_table(out / f"{name}.csv", rows)
    write_table(out / "source_use.csv", uses)
    figures(out, tables)
    (out / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    inputs = [
        DEFAULT,
        SCHEMA,
        spec["retail_config"],
        retail["base_config"],
        spec["protocol"],
        spec["ethics_assessment"],
        "evidence/m2/source_review.json",
        "evidence/m2/publication_20261028/model_input_check.json",
        "evidence/m2/publication_20261028/parameter_provenance.csv",
        "integration/m2_publication_20261028/guidance-catalogue.json",
        "integration/m2_publication_20261028/model-source-catalogue.json",
        f"{spec['source_map']}/manifest.json",
        "scripts/run_m2_publication.py",
        "scripts/qualify_m2_synthesis.py",
    ]
    hashes = {str(p.relative_to(root)): digest(p) for p in (root / "src/tobac").glob("*.py")}
    hashes.update({name: digest(checked(root, name)) for name in inputs})
    manifest = {
        "schema": "tobac.run.v1",
        "inputs": hashes,
        "outputs": {p.name: digest(p) for p in out.iterdir() if p.is_file()},
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return report


def resolution_table(
    folder: Path, name: str, columns: tuple[str, ...]
) -> dict[tuple[str, ...], dict[str, str]]:
    """Index a nonempty unique grid-diagnostic table by its scientific keys."""
    rows = csv_rows(folder / f"{name}.csv")
    mapping = {tuple(row[k] for k in columns): row for row in rows}
    if not rows or len(mapping) != len(rows):
        msg = "Complete unique resolution table required"
        raise ValueError(msg)
    return mapping


def information_optima(
    mapping: dict[tuple[str, ...], dict[str, str]], statistic: str, label: str
) -> dict[tuple[str, ...], tuple[str, ...]]:
    """Retain all co-optimal gross-information designs or finite parameter groups."""
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for key, row in mapping.items():
        grouped.setdefault(key[:3], []).append(row)
    return {
        key: tuple(sorted(rows[i][label] for i in optimal_indices([float(r[statistic]) for r in rows])))
        for key, rows in grouped.items()
    }


def resolution_comparison(first: Path, second: Path) -> Report:
    """Compare identical scenario/value supports under two finite cessation grids."""
    reports = [read(folder / "report.json") for folder in (first, second)]
    specs = [{k: v for k, v in r["specification"].items() if k != "quit_points"} for r in reports]
    if specs[0] != specs[1]:
        msg = "Resolution comparison must hold all non-grid inputs fixed"
        raise ValueError(msg)
    for folder in (first, second):
        manifest = read(folder / "manifest.json")
        for name, sha in manifest["outputs"].items():
            if digest(folder / name) != sha:
                msg = "Resolution output hash mismatch"
                raise ValueError(msg)
    result: Report = {
        "quit_points": [r["specification"]["quit_points"] for r in reports],
        "scope": "Finite-resolution diagnostic,not proof of continuous convergence or empirical validity",
    }
    for name, statistic, extra in (
        ("decisions", "evpi", ()),
        ("study_value", "evsi", ("design",)),
        ("grouped_evppi", "evppi", ("group",)),
    ):
        columns = ("case", "crime_weight", "resource_weight", *extra)
        indexed: list[dict[tuple[str, ...], dict[str, str]]] = []
        for folder in (first, second):
            mapping = resolution_table(folder, name, columns)
            indexed.append(mapping)
        if indexed[0].keys() != indexed[1].keys():
            msg = "Resolution tables must have matching scenario keys"
            raise ValueError(msg)
        differences = [
            abs(float(row[statistic]) - float(indexed[1][key][statistic])) for key, row in indexed[0].items()
        ]
        if not np.isfinite(differences).all():
            msg = "Finite resolution differences required"
            raise ValueError(msg)
        result[f"maximum_absolute_{statistic}_difference"] = max(differences)
        if name == "decisions":
            result["changed_cooptimal_sets"] = sum(
                row["cooptimal_actions"] != indexed[1][key]["cooptimal_actions"]
                for key, row in indexed[0].items()
            )
            result["compared_value_profiles"] = len(indexed[0])
        else:
            label = "design" if name == "study_value" else "group"
            optima = [information_optima(index, statistic, label) for index in indexed]
            result[f"changed_{label}_cooptimal_sets"] = sum(
                optima[0][key] != optima[1][key] for key in optima[0]
            )
    return result


def grid_check(root: Path, out: Path) -> Report:
    """Execute two resolution challenges and bind their files into the primary run."""
    paths: dict[int, Path] = {}
    for nodes in (2, 8):
        destination = out / f"grid-{nodes}"
        run(root, destination, quit_points=nodes)
        paths[nodes] = destination
    comparison = {
        "two_to_four": resolution_comparison(paths[2], out),
        "four_to_eight": resolution_comparison(out, paths[8]),
    }
    report = read(out / "report.json")
    report["grid_check"] = comparison
    (out / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    manifest = read(out / "manifest.json")
    manifest["outputs"]["report.json"] = digest(out / "report.json")
    for folder in paths.values():
        manifest["outputs"].update(
            {str(p.relative_to(out)): digest(p) for p in folder.rglob("*") if p.is_file()}
        )
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    """Run the fixed publication protocol with a fresh output directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--grid-check", action="store_true")
    args = parser.parse_args()
    result = run(ROOT, args.out)
    if args.grid_check:
        result = grid_check(ROOT, args.out)
    print(json.dumps(result, indent=2, allow_nan=False))  # noqa: T201 -- Structured CLI receipt.


if __name__ == "__main__":
    main()
