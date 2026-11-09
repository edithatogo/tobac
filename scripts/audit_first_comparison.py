"""Reconcile a bounded evidence review with actual source and handoff checks.

Review labels are claims to inspect, never observation-admission authority. This
audit reuses the maintained source handoff and NZHS extractor. It constructs no
EvidencePacket, likelihood, posterior or scientific acceptance certificate.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from audit_empirical_coverage import nzhs_candidates  # noqa: E402
from reconcile_empirical_candidates import source  # noqa: E402
from source_handoff import build_report, checked, digest, read, same_hash  # noqa: E402

REVIEW_COLUMNS = (
    "record_id",
    "source_id",
    "doi_or_source_url",
    "source_location",
    "comparison_role",
    "review_scope",
    "disposition",
    "dependency_group",
    "matched_target_data_available",
    "scientific_blockers",
    "archive_blockers",
    "existing_receipt",
)
DISPOSITIONS = {
    "candidate_for_joint_model_review",
    "context_only",
    "calibration_sensitivity_only",
    "excluded_independent_validation",
    "blocked_likelihood",
    "excluded_scope",
}
ROLES = {
    "baseline_observation",
    "wastewater_measurement",
    "measurement_calibration",
    "independent_validation",
    "policy_response",
    "contextual_comparator",
}
COMPARISON_ROLES = ("baseline_observation", "wastewater_measurement", "independent_validation")
MINIMUM_PRIOR_LABELS = 3


def list_values(value: str) -> list[str]:
    """Parse explicit review lists without treating repeated entries as evidence."""
    if not value:
        return []
    values = [part.strip() for part in value.split(";")]
    if any(not part for part in values) or len(values) != len(set(values)):
        msg = "Duplicate review list entry or empty list member"
        raise ValueError(msg)
    return values


def pinned_file(path: Path, sha256: str) -> Path:
    """Use the existing external-source path and byte-integrity contract."""
    resolved, _ = source({"root": str(path.parent.absolute()), "file": path.name, "sha256": sha256})
    return resolved


def review_claims(row: dict[str, Any]) -> None:
    """Reject malformed or admission-like claims before resolving source evidence."""
    if set(row) != set(REVIEW_COLUMNS) or any(not isinstance(v, str) for v in row.values()):
        msg = "Malformed review CSV row"
        raise ValueError(msg)
    if any(not row[key].strip() for key in REVIEW_COLUMNS if not key.endswith("blockers")):
        msg = "Required review field is empty"
        raise ValueError(msg)
    if row["disposition"] not in DISPOSITIONS:
        msg = "Unknown review disposition; reviews cannot declare admission"
        raise ValueError(msg)
    if row["comparison_role"] not in ROLES:
        msg = "Unknown comparison role"
        raise ValueError(msg)
    if row["matched_target_data_available"] not in {"yes", "no", "unverified"}:
        msg = "Unknown matched-target review claim"
        raise ValueError(msg)
    for key in ("dependency_group", "scientific_blockers", "archive_blockers", "existing_receipt"):
        row[key] = list_values(row[key])
    if row["disposition"] == "blocked_likelihood" and not row["scientific_blockers"]:
        msg = "Blocked likelihood must name the scientific blocker"
        raise ValueError(msg)


def load_review(path: Path, sha256: str, root: Path) -> list[dict[str, Any]]:
    """Validate source-review claims and bind cited local receipts to actual bytes."""
    path = pinned_file(path, sha256)
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or []) != REVIEW_COLUMNS:
            msg = "Unexpected first-comparison review CSV columns"
            raise ValueError(msg)
        records: list[dict[str, Any]] = list(reader)
    if not records:
        msg = "The first-comparison review must contain records"
        raise ValueError(msg)
    identities: set[str] = set()
    for row in records:
        review_claims(row)
        if row["record_id"] in identities:
            msg = "Duplicate review record identity"
            raise ValueError(msg)
        identities.add(row["record_id"])
        row["receipt_sha256"] = {name: digest(checked(root, name)) for name in row["existing_receipt"]}
    same_hash(path.parent, path.name, sha256)
    return records


def reconcile_record(
    row: dict[str, Any], observations: list[dict[str, Any]], registered: set[str]
) -> dict[str, Any]:
    """Attach executed handoff evidence without promoting the reviewer's claims."""
    selected = [item for item in observations if item["source_id"] == row["source_id"]]
    gaps = sorted({gap for item in selected for gap in item["gaps"]})
    if not selected:
        gaps.append("no_proposed_observation" if row["source_id"] in registered else "source_not_registered")
    return {
        "record_id": row["record_id"],
        "source_id": row["source_id"],
        "source_url": row["doi_or_source_url"],
        "source_location": row["source_location"],
        "review_scope": row["review_scope"],
        "comparison_role": row["comparison_role"],
        "review_disposition": row["disposition"],
        "reviewed_matched_target_claim": row["matched_target_data_available"],
        "review_scientific_blockers": row["scientific_blockers"],
        "review_archive_blockers": row["archive_blockers"],
        "receipt_sha256": row["receipt_sha256"],
        "dependency_groups": row["dependency_group"],
        "handoff_dependency_groups": sorted(
            {group for item in selected for group in item["dependency_groups"]}
        ),
        "registered_source": row["source_id"] in registered,
        "proposed_observation_rows": len(selected),
        "capture_bytes_verified_rows": sum(
            not {"original_source_capture_missing", "capture_bytes_not_verified"}.intersection(item["gaps"])
            for item in selected
        ),
        "metadata_compatible_rows": sum(item["metadata_compatible"] for item in selected),
        "handoff_gaps": gaps,
    }


def dependencies(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Expose shared sources, including validation outcomes reused by a baseline."""
    members: dict[str, list[str]] = {}
    for row in records:
        groups = set(row["dependency_groups"]) | set(row["handoff_dependency_groups"])
        for group in groups:
            members.setdefault(group, []).append(row["record_id"])
        row["overlaps_baseline_or_wastewater"] = sorted(
            other["record_id"]
            for other in records
            if other["record_id"] != row["record_id"]
            and other["comparison_role"] in {"baseline_observation", "wastewater_measurement"}
            and groups.intersection(set(other["dependency_groups"]) | set(other["handoff_dependency_groups"]))
        )
    return [
        {"dependency_group": group, "record_ids": sorted(ids)}
        for group, ids in sorted(members.items())
        if len(ids) > 1
    ]


def readiness(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute unresolved comparison requirements; metadata never certifies a joint model."""
    gaps: list[str] = []
    candidates: dict[str, list[str]] = {}
    for role in COMPARISON_ROLES:
        selected = [row for row in records if row["comparison_role"] == role]
        candidates[role] = [row["record_id"] for row in selected if metadata_review_candidate(row)]
        if not selected:
            gaps.append(f"missing_review_role:{role}")
        elif not candidates[role]:
            gaps.append(f"no_single_metadata_and_review_candidate:{role}")
            if not any(row["metadata_compatible_rows"] for row in selected):
                gaps.append(f"no_metadata_compatible_observations:{role}")
            if not any(
                row["reviewed_matched_target_claim"] == "yes" and not row["review_scientific_blockers"]
                for row in selected
            ):
                gaps.append(f"review_reports_no_qualified_matched_target:{role}")
    return {
        "status": "blocked" if gaps else "requires_joint_model_validation",
        "gaps": gaps,
        "metadata_review_candidates_by_role": candidates,
        "scope": "source_and_review_compatibility_not_scientific_admission",
        "joint_likelihood_evaluated": False,
    }


def metadata_review_candidate(row: dict[str, Any]) -> bool:
    """Require one record to satisfy every preliminary gate, never mixed witnesses."""
    return bool(
        row["metadata_compatible_rows"]
        and row["review_disposition"] == "candidate_for_joint_model_review"
        and row["reviewed_matched_target_claim"] == "yes"
        and not row["review_scientific_blockers"]
        and not row["review_archive_blockers"]
        and not (
            row["comparison_role"] == "independent_validation" and row["overlaps_baseline_or_wastewater"]
        )
    )


def nzhs_diagnostics(path: Path, sha256: str) -> dict[str, Any]:
    """Compute source-label support without inventing matched annual consumption."""
    path = pinned_file(path, sha256)
    summary, _ = nzhs_candidates(path, sha256)
    labels: list[dict[str, Any]] = []
    for item in summary["series"]:
        available = item["unflagged_complete_triplets"]
        enough = len(available) > MINIMUM_PRIOR_LABELS
        labels.append(
            {
                "indicator": item["indicator"],
                "unit": item["unit"],
                "unflagged_complete_triplet_labels": available,
                "flagged_labels": item["flagged_for_review"],
                "missing_triplet_labels": item["missing_triplets"],
                "absent_source_labels": item["absent_year_labels"],
                "three_prior_labels_available": enough,
                "candidate_latest_label": max(available) if enough else None,
                "candidate_prior_labels": available[:-1] if enough else [],
            }
        )
    return {
        "source_alias": summary["source_alias"],
        "source_sha256": sha256,
        "source_export_records": summary["source_export_records"],
        "candidate_records": summary["candidate_records"],
        "period_kind": summary["period_kind"],
        "label_support": labels,
        "matched_consumption_holdout_qualified": False,
        "limits": summary["limits"],
    }


def audit_review(
    review: Path,
    review_sha256: str,
    *,
    nzhs_csv: Path | None = None,
    nzhs_sha256: str | None = None,
    objects: Path | None = None,
) -> dict[str, Any]:
    """Execute existing source checks and reconcile a reproducible review snapshot."""
    if (nzhs_csv is None) != (nzhs_sha256 is None):
        msg = "NZHS source path and hash must be supplied together"
        raise ValueError(msg)
    reviewed = load_review(review, review_sha256, ROOT)
    handoff = build_report(ROOT, objects=objects)
    register = read(checked(ROOT, "integration/archive/source-register.json"))
    registered = {ref["source_id"] for item in register["sources"] for ref in item["references"]}
    records = [reconcile_record(row, handoff["observations"], registered) for row in reviewed]
    shared = dependencies(records)
    result: dict[str, Any] = {
        "schema_version": "tobac.first-comparison-review-audit.v1",
        "review_sha256": review_sha256,
        "audit_source_sha256": digest(Path(__file__)),
        "records": records,
        "shared_source_groups": shared,
        "handoff": {
            "status": handoff["status"],
            "rows": len(handoff["observations"]),
            "metadata_compatible_rows": sum(row["metadata_compatible"] for row in handoff["observations"]),
            "proposal_sha256": handoff["proposal_sha256"],
            "binding_sha256": handoff["binding_sha256"],
            "raw_object_staging_supplied": objects is not None,
        },
        "comparison_readiness": readiness(records),
        "scientific_qualification": False,
        "automatically_conditions_live_model": False,
    }
    if nzhs_csv is not None and nzhs_sha256 is not None:
        nzhs = nzhs_diagnostics(nzhs_csv, nzhs_sha256)
        bindings = read(checked(ROOT, "integration/archive/source-bindings.json"))
        nzhs["matching_registered_payload_captures"] = sum(
            capture.get("sha256") == nzhs_sha256
            for item in bindings["sources"]
            if any(ref["source_id"] == nzhs["source_alias"] for ref in item["references"])
            for capture in item["captures"]
        )
        nzhs["registration_boundary"] = (
            "A registered bibliography alias does not register every source edition; "
            "only an exact payload-hash match links this CSV to existing capture metadata. "
            "Capture metadata alone does not establish archive/WARC or scientific admission."
        )
        result["nzhs_source_diagnostics"] = nzhs
    for row in records:
        for name, sha in row["receipt_sha256"].items():
            same_hash(ROOT, name, sha)
    pinned_file(review, review_sha256)
    return result


def main() -> None:
    """Write a new immutable audit edition from explicit byte-bound inputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--review-sha256", required=True)
    parser.add_argument("--nzhs-csv", type=Path)
    parser.add_argument("--nzhs-sha256")
    parser.add_argument("--objects", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists() or args.out.is_symlink():
        parser.error("Refusing to overwrite an existing first-comparison audit")
    if sys.version_info[:3] != (3, 15, 2):
        parser.error("This audit is qualified only on repository Python 3.15.2")
    result = audit_review(
        args.review,
        args.review_sha256,
        nzhs_csv=args.nzhs_csv,
        nzhs_sha256=args.nzhs_sha256,
        objects=args.objects,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + "\n")
    sys.stdout.write(
        f"{result['comparison_readiness']['status']}: {len(result['records'])} reviewed records\n"
    )


if __name__ == "__main__":
    main()
