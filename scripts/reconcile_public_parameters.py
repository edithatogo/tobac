"""Reconcile existing candidate aliases; never admit or condition observations."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

MARKER = re.compile(r"<!-- TOBAC_PARAMETER_CANDIDATES_V1 -->\s*```json\s*(.*?)\s*```", re.DOTALL)
UNCERTAINTY_ALIASES = {
    ("not_reported", "not_extracted"),
    ("not_applicable", "not_sampling_uncertainty"),
    ("not_applicable", "scenario_not_distribution"),
    ("binomial_counts_available", "counts_available_no_ci_assigned"),
    ("confidence_interval_95", "reported_two_sided_95CI"),
}
PERCENT_TO_FRACTION = 0.01
SOURCE_ALIASES = {("PHARMAC_DISCOUNT", "PHARMAC_PFPA_DISCOUNT")}


def _unique(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result = {row[key]: row for row in records}
    if len(result) != len(records):
        msg = f"Duplicate {key}"
        raise ValueError(msg)
    return result


def _check_counts(new: dict[str, Any], old: dict[str, Any]) -> None:
    if (new["numerator"], new["denominator"]) != (old["numerator"], old["denominator"]):
        msg = "Alias count representation conflict"
        raise ValueError(msg)


def reconcile(
    registry: dict[str, Any], embedded: dict[str, Any], aliases: list[dict[str, str]]
) -> dict[str, Any]:
    """Account for both editions completely without adding their overlapping counts."""
    candidate = _unique(registry["parameters"], "parameter_id")
    older = _unique([dict(zip(embedded["columns"], row, strict=True)) for row in embedded["records"]], "id")
    _unique(aliases, "candidate_id")
    _unique(aliases, "embedded_id")
    if (
        embedded["empirical_admission"]
        or embedded["active_model_parameters_changed"]
        or any(
            row["admission_status"] != "candidate_only"
            or row["runtime_configuration_changed"]
            or row["distribution"] is not None
            for row in candidate.values()
        )
    ):
        msg = "Candidate-only boundary violated"
        raise ValueError(msg)
    matched: list[dict[str, Any]] = []
    for row in aliases:
        new, old = candidate[row["candidate_id"]], older[row["embedded_id"]]
        source_pair = (new["source_id"], old["source_id"])
        if (row["candidate_source"], row["embedded_source"]) != source_pair or (
            source_pair[0] != source_pair[1] and source_pair not in SOURCE_ALIASES
        ):
            msg = "Alias source identity mismatch"
            raise ValueError(msg)
        if (row["candidate_unit"], row["embedded_unit"]) != (new["unit"], old["unit"]):
            msg = "Alias unit identity mismatch"
            raise ValueError(msg)
        factor = float(row["candidate_to_embedded_multiplier"])
        if (
            not math.isfinite(factor)
            or factor not in (1.0, 0.01)
            or (
                factor == PERCENT_TO_FRACTION
                and (new["unit"], old["unit"]) != ("percentage_points", "risk_difference")
            )
        ):
            msg = "Unsupported alias conversion"
            raise ValueError(msg)
        _check_counts(new, old)
        for field in ("value", "lower", "upper"):
            a, b = new[field], old[field]
            if (a is None) != (b is None) or (
                a is not None and not math.isclose(a * factor, b, rel_tol=0, abs_tol=1e-12)
            ):
                msg = "Alias values or intervals conflict"
                raise ValueError(msg)
        if (
            row["admission"] != "candidate_only"
            or new["admission_status"] != "candidate_only"
            or new["runtime_configuration_changed"]
            or new["distribution"] is not None
        ):
            msg = "Candidate-only boundary violated"
            raise ValueError(msg)
        if (new["interval_type"], old["uncertainty"]) not in UNCERTAINTY_ALIASES:
            msg = "Unreviewed uncertainty-type alias"
            raise ValueError(msg)
        matched.append(
            {
                "candidate_id": row["candidate_id"],
                "embedded_id": row["embedded_id"],
                "numeric_match": True,
                "independent_observations_added": 0,
                "candidate_uncertainty": new["interval_type"],
                "embedded_uncertainty": old["uncertainty"],
                "source_scope_review_required": True,
                "runtime_target": new["model_target"],
            }
        )
    return {
        "candidate_count": len(candidate),
        "embedded_count": len(older),
        "aliases": matched,
        "unmatched_candidate_ids": sorted(set(candidate) - {r["candidate_id"] for r in aliases}),
        "unmatched_embedded_ids": sorted(set(older) - {r["embedded_id"] for r in aliases}),
        "independent_observations_added": 0,
        "empirical_admission": False,
        "runtime_configuration_changed": False,
    }


def verify_hashes(root: Path, expected: dict[str, str]) -> None:
    """Reject missing or changed source editions before reconciliation output."""
    for name, digest in expected.items():
        path = (root / name).resolve()
        if (
            not path.is_relative_to(root.resolve())
            or not path.is_file()
            or hashlib.sha256(path.read_bytes()).hexdigest() != digest
        ):
            msg = f"Missing or stale source edition: {name}"
            raise ValueError(msg)


def run(root: Path, expected: dict[str, str]) -> dict[str, Any]:
    """Bind the existing registry, embedded edition and alias table by exact bytes."""
    names = [
        "evidence/parameter_candidates_20261109/registry.json",
        "conductor/tracks/dynamic_frontier_20261108/design.md",
        "evidence/parameter_candidates_20261109/alias_crosswalk.csv",
    ]
    if set(expected) != set(names):
        msg = "Bind all three canonical source editions"
        raise ValueError(msg)
    verify_hashes(root, expected)
    registry = json.loads((root / names[0]).read_text(encoding="utf-8"))
    found = MARKER.search((root / names[1]).read_text(encoding="utf-8"))
    if found is None:
        msg = "Embedded catalogue absent"
        raise ValueError(msg)
    with (root / names[2]).open(newline="", encoding="utf-8") as stream:
        aliases = list(csv.DictReader(stream))
    return {"source_sha256": expected, "result": reconcile(registry, json.loads(found.group(1)), aliases)}


class _DoiMetadata(HTMLParser):
    """Read article metadata, never a DOI merely cited in a bibliography."""

    def __init__(self) -> None:
        super().__init__()
        self.dois: set[str] = set()
        self.in_article_doi = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "article-id" and attributes.get("pub-id-type") == "doi":
            self.in_article_doi = True
        if tag == "meta" and attributes.get("name") == "citation_doi":
            value = attributes.get("content")
            if value:
                self.dois.add(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "article-id":
            self.in_article_doi = False

    def handle_data(self, data: str) -> None:
        if self.in_article_doi and data.strip():
            self.dois.add(data.strip())


def _article_dois(original: str) -> set[str]:
    parser = _DoiMetadata()
    parser.feed(original)
    return parser.dois


def check_extracts(root: Path, originals: Path, extracts: dict[str, Any]) -> dict[str, Any]:
    """Compare a manually located source extraction to its existing candidate entry.

    Hash/identity readback binds the edition; numerical agreement is not a second
    independent extraction, causal transport, archive admission or a fitted input.
    """
    registry = json.loads((root / "evidence/parameter_candidates_20261109/registry.json").read_text())
    parameters = _unique(registry["parameters"], "parameter_id")
    records = extracts["records"]
    _unique(records, "parameter_id")
    checked: list[str] = []
    for row in records:
        verify_hashes(originals, {row["original_file"]: row["original_sha256"]})
        original = (originals / row["original_file"]).read_text(encoding="utf-8")
        candidate = parameters[row["parameter_id"]]
        source = next(item for item in registry["sources"] if item["source_id"] == candidate["source_id"])
        if source["doi"] != row["doi"] or _article_dois(original) != {row["doi"]}:
            msg = "Source DOI identity mismatch"
            raise ValueError(msg)
        for field in (
            "source_id",
            "value",
            "lower",
            "upper",
            "unit",
            "interval_type",
            "dependency_group",
            "admission_status",
        ):
            if row[field] != candidate[field]:
                msg = f"Source extraction conflict: {row['parameter_id']} {field}"
                raise ValueError(msg)
        target = row["code_interface"]
        if target is not None and not (root / target).is_file():
            msg = "Missing code interface"
            raise ValueError(msg)
        checked.append(row["parameter_id"])
    return {"source_matched_candidate_ids": checked, "empirical_admission": False}


def main() -> None:
    """Create a new reconciliation receipt, preserving earlier outputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bindings", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--extracts", type=Path)
    parser.add_argument("--originals", type=Path)
    args = parser.parse_args()
    if (args.extracts is None) != (args.originals is None):
        parser.error("Supply both --extracts and --originals")
    result = run(Path(__file__).resolve().parents[1], json.loads(args.bindings.read_text(encoding="utf-8")))
    if args.extracts is not None:
        result["source_check"] = check_extracts(
            Path(__file__).resolve().parents[1],
            args.originals,
            json.loads(args.extracts.read_text(encoding="utf-8")),
        )
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
