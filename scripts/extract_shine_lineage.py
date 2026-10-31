"""Extract the retained SHINE Table 2 original with installed native records.

This is the second source-backed consumer operation: it consumes an HTML original
and several consumer metadata parents through the frozen producer's CAS and strict
records. Its fixed mode is **exploratory**. Native source registration, complete
manifest closure, source-edition equivalence and scientific applicability remain
open. The output is a published model input, not a new empirical observation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_moh_lineage as support
import qualify_shine_table as comparison

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = Path(__file__).resolve()
COMPARISON_IMPLEMENTATION = Path(comparison.__file__).resolve()


def digest(path: Path) -> str:
    """Hash the exact implementation bytes recorded in the transformation parameters."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_transformation(  # noqa: PLR0913  # Keep the explicit native fields visible in one record.
    *,
    attempt: str,
    revision: str,
    started: str,
    input_ids: list[str],
    environment_id: str,
    software_bill_id: str,
    binding: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    """Build the exploratory multi-parent transformation record before execution."""
    return {
        "schema_version": "archive-govt-nz.transformation/v1",
        "record_id": attempt,
        "observed_at": started,
        "state": "failed",
        "evidence": [],
        "name": "tobac.shine-retail-table2-extract-and-compare",
        "version": "1",
        "implementation_revision": revision,
        "input_object_ids": input_ids,
        "output_object_ids": [],
        "parameters": {
            "lineage_mode": "exploratory",
            "source_id": comparison.SOURCE_ID,
            "doi": comparison.DOI,
            "source_uri": binding["source_uri"],
            "archive_id": binding["archive_id"],
            "locator_section": "T2",
            "locator_transition": comparison.TRANSITION,
            "selection": (
                "Retail outlet-restriction cessation row only; other Table 2 rows and article prose omitted"
            ),
            "conversions": "None; published beta parameters retained without unit conversion",
            "dependency_assumptions": (
                "Published model input, not observed effectiveness; earlier reference capture "
                "is a different SHA-256, so no same-edition equivalence is assumed"
            ),
            "original_captured_at": binding["original_captured_at"],
            "source_warc_sha256_not_verified_this_run": binding["source_warc_sha256"],
            "same_source_version_assumed": False,
            "implementation_sha256": digest(IMPLEMENTATION),
            "comparison_implementation_sha256": digest(COMPARISON_IMPLEMENTATION),
            "command": sys.argv,
            "shared_data_identity": "SHINE_RETAIL_TABLE2_published_model_input",
            "unit": "beta parameters (dimensionless); percentages as published",
            "environment_details_object_id": environment_id,
            "root": str(root),
        },
        "environment_sbom_id": software_bill_id,
        "started_at": started,
        "ended_at": started,
        "information_loss": (
            "Table 2 retail cessation row, locator and published uncertainty retained; "
            "surrounding table rows, article prose and formatting observed but not stored"
        ),
        "deterministic": True,
    }


def installed_environment(lock_sha: str, pin: dict[str, Any]) -> dict[str, Any]:
    """Describe the actual interpreter, producer artifact and installed distributions."""
    return {
        "python": sys.version,
        "producer_revision": pin["producer_revision"],
        "producer_wheel_sha256": pin["wheel_sha256"],
        "lock_sha256": lock_sha,
        "distributions": sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions()),
    }


def execute(
    source: Path,
    out: Path,
    environment_lock: Path,
    wheel: Path | None = None,
    sbom: Path | None = None,
) -> dict[str, Any]:
    """Execute one new private exploratory attempt; earlier attempts stay immutable."""
    if out.exists() or out.is_symlink():
        msg = "Choose a new attempt directory; earlier receipts are immutable"
        raise FileExistsError(msg)
    if not out.resolve().is_relative_to(ROOT / "outputs"):
        msg = "Keep original bytes and native attempts in consumer-owned private outputs"
        raise ValueError(msg)
    if sys.version_info[:3] != (3, 15, 1) or not Path(sys.prefix).resolve().is_relative_to(ROOT):
        msg = "Select a repo-local Python 3.15.1 environment"
        raise RuntimeError(msg)
    if wheel is None:
        msg = "Supply the reviewed producer wheel"
        raise ValueError(msg)
    native, factory, pin = support.producer(wheel)
    lock_sha = support.qualification.digest(environment_lock)
    sbom_bytes = support.environment_sbom(sbom)
    source_raw = support.verified_bytes(source, comparison.SOURCE_SHA256)
    snapshots = comparison.consumer_snapshots(ROOT)
    binding = comparison.binding_metadata(snapshots)
    out.mkdir(parents=True)
    store = factory(out / "cas")
    source_object = store.put_bytes(source_raw)
    consumer_objects = {name: store.put_bytes(raw) for name, raw in sorted(snapshots.items())}
    software_bill = store.put_bytes(sbom_bytes)
    environment = store.put_bytes(support.encoded(installed_environment(lock_sha, pin)))
    started = support.now()
    attempt = "tobac-shine-" + uuid4().hex
    revision = subprocess.check_output(  # noqa: S603 -- Fixed local Git read; no shell or source-provided argv.
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],  # noqa: S607 -- Fixed developer tool.
        text=True,
        timeout=15,
    ).strip()
    inputs = [source_object, *consumer_objects.values()]
    transformation = build_transformation(
        attempt=attempt,
        revision=revision,
        started=started,
        input_ids=[r.object_id for r in inputs],
        environment_id=environment.object_id,
        software_bill_id=software_bill.object_id,
        binding=binding,
        root=ROOT,
    )
    try:
        extracted = comparison.extract_table(store.verify(source_object.object_id).path.read_bytes())
        comparison_result = comparison.consumer_comparison(snapshots, extracted)
        output = store.put_bytes(
            support.encoded(
                {
                    "source_id": comparison.SOURCE_ID,
                    "unit": "beta parameters (dimensionless)",
                    **extracted,
                    **comparison_result,
                }
            )
        )
        support.verify_objects(store, [*inputs, environment, software_bill, output])
        transformation.update(state="succeeded", ended_at=support.now(), output_object_ids=[output.object_id])
    except Exception:
        transformation["ended_at"] = support.now()
        support.persist(transformation, out / "failed-transformation.json", native, store)
        raise
    transformation_id = support.persist(transformation, out / "transformation.json", native, store)
    validation = {
        "schema_version": "archive-govt-nz.validation/v1",
        "record_id": attempt + "-validation",
        "observed_at": support.now(),
        "state": "passed",
        "evidence": [],
        "validator_name": "tobac.shine-table2-locator-and-consumer-parity",
        "validator_version": "1",
        "subject_ids": [r.object_id for r in [*inputs, environment, software_bill, output]],
        "checks": [
            "SHINE Table 2 retail cessation row and locator",
            "beta(23.4, 97.2) matches the consumer configuration and prior reference",
            "source SHA-256 matches the retained original",
            "native CAS actual bytes",
            "strict native record readback",
            "same-source-edition equivalence is not assumed",
        ],
        "findings": [],
        "started_at": started,
        "ended_at": support.now(),
    }
    validation_id = support.persist(validation, out / "validation.json", native, store)
    result = {
        "schema": "tobac.shine-native-extraction.v1",
        "execution_mode": "exploratory",
        "attempt_id": attempt,
        "producer_revision": pin["producer_revision"],
        "producer_wheel_sha256": pin["wheel_sha256"],
        "implementation_revision": revision,
        "implementation_sha256": digest(IMPLEMENTATION),
        "comparison_implementation_sha256": digest(COMPARISON_IMPLEMENTATION),
        "source_sha256": source_object.sha256,
        "source_byte_count": len(source_raw),
        "original_captured_at": comparison_result["original_captured_at"],
        "source_capture_time_verified": False,
        "locator": extracted["locator"],
        "source_beta": extracted["source_beta"],
        "metadata_sha256": comparison_result["metadata_sha256"],
        "extracted_object_id": output.object_id,
        "transformation_object_id": transformation_id,
        "validation_object_id": validation_id,
        "environment_object_id": environment.object_id,
        "environment_sbom_object_id": software_bill.object_id,
        "native_object_count": store.verified_inventory().object_count,
        "native_lineage_qualified": False,
        "scientific_qualification": False,
        "independent_empirical_observation": False,
        "automatically_conditions_live_model": False,
        "remaining_producer_gates": pin["remaining_producer_gates"],
        "scope": (
            "Actual SHINE Table 2 extraction/native CAS/records; manifest and runner closure remain open"
        ),
    }
    with (out / "receipt.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + "\n")
    return result


def main() -> None:
    """Require explicit local sources/artifacts and a new private output location."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--environment-lock", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--environment-sbom", required=True, type=Path)
    args = parser.parse_args()
    execute(args.source, args.out, args.environment_lock, args.wheel, args.environment_sbom)
    sys.stdout.write(
        "Extracted the SHINE Table 2 row with native records; full lineage remains unqualified\n"
    )


if __name__ == "__main__":
    main()
