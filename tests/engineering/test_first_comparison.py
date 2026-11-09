"""First-comparison review must retain source gaps and dependent evidence."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]


def test_published_first_comparison_audit_binds_review_and_implementation() -> None:
    """The retained audit must describe the actual reviewed source and code edition."""
    track = ROOT / "conductor/tracks/nz_au_empirical_20261106"
    report = json.loads((track / "first-comparison-audit-20261109.json").read_text())
    assert (
        report["review_sha256"]
        == hashlib.sha256((track / "first-comparison-dispositions-20261109.csv").read_bytes()).hexdigest()
    )
    assert (
        report["audit_source_sha256"]
        == hashlib.sha256((ROOT / "scripts/audit_first_comparison.py").read_bytes()).hexdigest()
    )
    for record in report["records"]:
        for name, digest in record["receipt_sha256"].items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    assert report["comparison_readiness"]["status"] == "blocked"
    assert report["scientific_qualification"] is False
    assert report["automatically_conditions_live_model"] is False


FIELDS = (
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


@pytest.fixture
def audit() -> ModuleType:
    """Load the maintained audit without invoking its command line."""
    spec = importlib.util.spec_from_file_location(
        "first_comparison_audit", ROOT / "scripts/audit_first_comparison.py"
    )
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_review(path: Path, rows: list[dict[str, str]]) -> str:
    """Write explicitly invented review claims, which cannot confer admission."""
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def rows() -> list[dict[str, str]]:
    """Claim matching for two known dependent sources to test rejection."""
    shared = {
        "doi_or_source_url": "https://example.invalid/synthetic-test-only",
        "source_location": "Synthetic fixture; not a review of the named source",
        "review_scope": "synthetic_fixture_only",
        "disposition": "blocked_likelihood",
        "dependency_group": "MOH_returns",
        "matched_target_data_available": "yes",
        "scientific_blockers": "period_bridge_missing",
        "archive_blockers": "",
        "existing_receipt": "integration/archive/observation-handoff-report.json",
    }
    return [
        {
            **shared,
            "record_id": "fixture_release",
            "source_id": "long-nz-tobacco-tonnes-2025",
            "comparison_role": "baseline_observation",
        },
        {
            **shared,
            "record_id": "fixture_summary",
            "source_id": "parallel-S08",
            "comparison_role": "independent_validation",
        },
    ]


def test_review_claims_do_not_clear_real_handoff_gaps(
    tmp_path: Path, audit: ModuleType, rows: list[dict[str, str]]
) -> None:
    review = tmp_path / "review.csv"
    result = audit.audit_review(review, write_review(review, rows))
    assert result["handoff"]["status"] == "blocked"
    assert result["handoff"]["rows"] == 28
    release = result["records"][0]
    assert release["reviewed_matched_target_claim"] == "yes"
    assert release["proposed_observation_rows"] == 16
    assert release["metadata_compatible_rows"] == 0
    assert "capture_bytes_not_verified" in release["handoff_gaps"]
    assert result["comparison_readiness"]["status"] == "blocked"
    assert "missing_review_role:wastewater_measurement" in result["comparison_readiness"]["gaps"]
    assert result["scientific_qualification"] is False
    assert result["automatically_conditions_live_model"] is False


def test_shared_review_sources_cannot_be_independent_validation(
    tmp_path: Path, audit: ModuleType, rows: list[dict[str, str]]
) -> None:
    review = tmp_path / "review.csv"
    result = audit.audit_review(review, write_review(review, rows))
    assert {
        "dependency_group": "MOH_returns",
        "record_ids": ["fixture_release", "fixture_summary"],
    } in result["shared_source_groups"]
    validation = result["records"][1]
    assert validation["overlaps_baseline_or_wastewater"] == ["fixture_release"]
    assert (
        "no_single_metadata_and_review_candidate:independent_validation"
        in result["comparison_readiness"]["gaps"]
    )


def test_review_group_labels_cannot_erase_known_handoff_dependence(
    tmp_path: Path, audit: ModuleType, rows: list[dict[str, str]]
) -> None:
    rows[0]["dependency_group"] = "asserted_independent_a"
    rows[1]["dependency_group"] = "asserted_independent_b"
    review = tmp_path / "review.csv"
    result = audit.audit_review(review, write_review(review, rows))
    assert {
        "dependency_group": "NZ_MOH_tobacco_returns",
        "record_ids": ["fixture_release", "fixture_summary"],
    } in result["shared_source_groups"]
    assert result["records"][1]["overlaps_baseline_or_wastewater"] == ["fixture_release"]


@pytest.mark.parametrize(
    "case",
    [
        ("disposition", "admitted", "Unknown review disposition"),
        ("matched_target_data_available", "true", "Unknown matched-target review claim"),
        ("comparison_role", "ready_likelihood", "Unknown comparison role"),
        ("scientific_blockers", "", "Blocked likelihood must name"),
        ("dependency_group", "MOH_returns;MOH_returns", "Duplicate review list entry"),
        ("existing_receipt", "../outside.json", "Noncanonical repository path"),
    ],
)
def test_malformed_or_approval_like_review_values_fail(
    tmp_path: Path,
    audit: ModuleType,
    rows: list[dict[str, str]],
    case: tuple[str, str, str],
) -> None:
    field, value, message = case
    rows[0][field] = value
    review = tmp_path / "review.csv"
    sha = write_review(review, rows)
    with pytest.raises(ValueError, match=message):
        audit.audit_review(review, sha)


def test_changed_review_duplicate_identity_and_unknown_columns_fail(
    tmp_path: Path, audit: ModuleType, rows: list[dict[str, str]]
) -> None:
    review = tmp_path / "review.csv"
    sha = write_review(review, rows)
    review.write_text(review.read_text().replace("fixture_release", "changed"))
    with pytest.raises(ValueError, match="Input hash mismatch"):
        audit.audit_review(review, sha)
    rows[1]["record_id"] = rows[0]["record_id"]
    with pytest.raises(ValueError, match="Duplicate review record"):
        audit.audit_review(review, write_review(review, rows))
    review.write_text("record_id,admitted\nsynthetic,true\n")
    with pytest.raises(ValueError, match="review CSV columns"):
        audit.audit_review(review, hashlib.sha256(review.read_bytes()).hexdigest())


def test_unregistered_source_remains_explicit(
    tmp_path: Path, audit: ModuleType, rows: list[dict[str, str]]
) -> None:
    rows[0]["source_id"] = "synthetic-unregistered-source"
    review = tmp_path / "review.csv"
    result = audit.audit_review(review, write_review(review, rows))
    record = result["records"][0]
    assert record["registered_source"] is False
    assert record["proposed_observation_rows"] == 0
    assert record["handoff_gaps"] == ["source_not_registered"]


def survey_fixture(path: Path, *, flag_latest: bool) -> str:
    """Generate source-shaped synthetic marginals with five survey labels."""
    import audit_empirical_coverage as coverage  # noqa: PLC0415

    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=coverage.NZHS_COLUMNS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for indicator in coverage.NZHS_INDICATORS:
            for year in range(2020, 2025):
                row = dict.fromkeys(coverage.NZHS_COLUMNS, "")
                row.update(
                    {
                        "population": "adults",
                        "group": "Total",
                        "short.description": indicator,
                        "year": str(year),
                        "total": "2",
                        "total.low.CI": "1",
                        "total.high.CI": "3",
                        "flag_for_publishing": "S" if flag_latest and year == 2024 else "",
                    }
                )
                writer.writerow(row)
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize(("flag_latest", "latest"), [(False, 2024), (True, 2023)])
def test_survey_label_support_preserves_flags_and_is_not_a_consumption_holdout(
    tmp_path: Path,
    audit: ModuleType,
    rows: list[dict[str, str]],
    *,
    flag_latest: bool,
    latest: int,
) -> None:
    review, survey = tmp_path / "review.csv", tmp_path / "survey.csv"
    result = audit.audit_review(
        review,
        write_review(review, rows),
        nzhs_csv=survey,
        nzhs_sha256=survey_fixture(survey, flag_latest=flag_latest),
    )
    source = result["nzhs_source_diagnostics"]
    assert source["candidate_records"] == 40
    assert source["source_sha256"] == hashlib.sha256(survey.read_bytes()).hexdigest()
    assert all(s["candidate_latest_label"] == latest for s in source["label_support"])
    assert all(s["three_prior_labels_available"] for s in source["label_support"])
    assert source["matched_consumption_holdout_qualified"] is False
    assert source["matching_registered_payload_captures"] == 0
    assert source["source_alias"] == "nz-key-results-2024-25"
    assert result["comparison_readiness"]["status"] == "blocked"


def metadata_fixture(role: str, name: str) -> dict[str, object]:
    """Synthetic post-handoff records test quantifiers, never actual admission."""
    return {
        "record_id": name,
        "comparison_role": role,
        "metadata_compatible_rows": 1,
        "review_disposition": "candidate_for_joint_model_review",
        "reviewed_matched_target_claim": "yes",
        "review_scientific_blockers": [],
        "review_archive_blockers": [],
        "overlaps_baseline_or_wastewater": [],
    }


def test_role_cannot_mix_metadata_and_review_witnesses(audit: ModuleType) -> None:
    first = metadata_fixture("baseline_observation", "metadata-only")
    first["review_scientific_blockers"] = ["unknown_scope"]
    second = metadata_fixture("baseline_observation", "claim-only")
    second["metadata_compatible_rows"] = 0
    result = audit.readiness([first, second])
    assert result["metadata_review_candidates_by_role"]["baseline_observation"] == []
    assert "no_single_metadata_and_review_candidate:baseline_observation" in result["gaps"]


@pytest.mark.parametrize("disposition", ["context_only", "excluded_independent_validation", "excluded_scope"])
def test_excluded_or_context_record_cannot_supply_a_role(audit: ModuleType, disposition: str) -> None:
    row = metadata_fixture("baseline_observation", "excluded")
    row["review_disposition"] = disposition
    assert audit.metadata_review_candidate(row) is False


def test_independent_alternative_not_blocked_by_excluded_dependent_record(audit: ModuleType) -> None:
    records = [metadata_fixture(role, role) for role in audit.COMPARISON_ROLES]
    excluded = metadata_fixture("independent_validation", "dependent-excluded")
    excluded["review_disposition"] = "excluded_independent_validation"
    excluded["overlaps_baseline_or_wastewater"] = ["baseline_observation"]
    result = audit.readiness([*records, excluded])
    assert result["status"] == "requires_joint_model_validation"
    assert result["gaps"] == []
    assert result["metadata_review_candidates_by_role"]["independent_validation"] == [
        "independent_validation"
    ]
    assert result["joint_likelihood_evaluated"] is False


def test_cli_refuses_existing_output(
    tmp_path: Path, audit: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "existing.json"
    output.write_text("original evidence")
    monkeypatch.setattr(
        "sys.argv",
        ["audit", "--review", "missing.csv", "--review-sha256", "0" * 64, "--out", str(output)],
    )
    with pytest.raises(SystemExit, match="2"):
        audit.main()
    assert output.read_text() == "original evidence"
