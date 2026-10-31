"""Independent controls for the SHINE native consumer operation.

Synthetic metadata does not qualify the retained original, the producer estate or
scientific applicability.
"""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def module():
    """Load the consumer helper without importing an optional producer package."""
    spec = importlib.util.spec_from_file_location("extract_shine", ROOT / "scripts/extract_shine_lineage.py")
    assert spec
    assert spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def binding_snapshot() -> bytes:
    return json.dumps(
        {
            "sources": [
                {
                    "archive_id": "tobac-a892a52bb0ce2147",
                    "redistribution_authorized": False,
                    "references": [{"source_id": "SHINE_RETAIL_TABLE2"}],
                    "captures": [
                        {
                            "uri": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11672025/",
                            "status": "source_html_identity_observed",
                            "sha256": "9d8fe4fca0e55129ebc9325edb93e2daf539e5328e48cb11e45ff4dfd943217e",
                            "byte_count": 236088,
                            "warc_sha256": "1c5093f75d54f84b801c8ead7522f499ac3f2c2dce259bbab5e6507d693dfd58",
                            "captured_at": None,
                        }
                    ],
                }
            ]
        }
    ).encode()


def synthetic_snapshots() -> dict[str, bytes]:
    return {
        "config": (ROOT / "configs/m2_retail.json").read_bytes(),
        "bindings": binding_snapshot(),
        "prior_check": (ROOT / "evidence/m2/publication_20261028/model_input_check.json").read_bytes(),
    }


def test_retained_binding_identity_is_resolved_without_edition_claims() -> None:
    metadata = module().comparison.binding_metadata(synthetic_snapshots())
    assert metadata["archive_id"] == "tobac-a892a52bb0ce2147"
    assert metadata["source_uri"] == "https://pmc.ncbi.nlm.nih.gov/articles/PMC11672025/"
    assert metadata["original_captured_at"] is None
    assert metadata["redistribution_authorized"] is False


@pytest.mark.parametrize("mutation", ["duplicate", "status", "captured", "rights", "uri"])
def test_ambiguous_or_challenge_binding_metadata_is_rejected(mutation) -> None:
    payload = json.loads(binding_snapshot())
    source = payload["sources"][0]
    if mutation == "duplicate":
        payload["sources"].append(payload["sources"][0])
    elif mutation == "status":
        source["captures"][0]["status"] = "challenge_not_source"
    elif mutation == "captured":
        source["captures"][0]["captured_at"] = "2026-10-29T00:00:00Z"
    elif mutation == "rights":
        source["redistribution_authorized"] = True
    else:
        source["captures"][0]["uri"] = "https://example.invalid/"
    snapshots = {**synthetic_snapshots(), "bindings": json.dumps(payload).encode()}
    with pytest.raises(ValueError, match="SHINE"):
        module().comparison.binding_metadata(snapshots)


def test_consumer_configuration_flags_remain_explicit() -> None:
    result = module().comparison.consumer_comparison(synthetic_snapshots(), {"source_beta": ["23.4", "97.2"]})
    assert result["source_sha256"] == "9d8fe4fca0e55129ebc9325edb93e2daf539e5328e48cb11e45ff4dfd943217e"
    assert result["previous_reference_sha256"] != result["source_sha256"]
    assert result["same_source_version_assumed"] is False
    assert result["native_lineage_qualified"] is False
    assert result["scientific_qualification"] is False
    assert result["independent_empirical_observation"] is False
    assert set(result["metadata_sha256"]) == {"config", "bindings", "prior_check"}


def test_parsed_beta_must_match_the_consumer_configuration() -> None:
    with pytest.raises(ValueError, match="extracted beta"):
        module().comparison.consumer_comparison(synthetic_snapshots(), {"source_beta": ["23.4", "97.3"]})


def test_altered_configuration_or_prior_reference_fails_closed() -> None:
    snapshots = synthetic_snapshots()
    snapshots["config"] = snapshots["config"].replace(b"23.4", b"23.5")
    with pytest.raises(ValueError, match="SHINE"):
        module().comparison.consumer_comparison(snapshots, {"source_beta": ["23.4", "97.2"]})


def test_transformation_record_is_exploratory_multi_parent_and_failed_first() -> None:
    record = module().build_transformation(
        attempt="tobac-shine-test",
        revision="deadbeef",
        started="2026-10-31T00:00:00Z",
        input_ids=["obj-source", "obj-config", "obj-bindings", "obj-prior"],
        environment_id="obj-environment",
        software_bill_id="obj-sbom",
        binding={
            "source_uri": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11672025/",
            "archive_id": "tobac-a892a52bb0ce2147",
            "original_captured_at": None,
            "source_warc_sha256": "1c5093f75d54f84b801c8ead7522f499ac3f2c2dce259bbab5e6507d693dfd58",
        },
        root=ROOT,
    )
    assert record["state"] == "failed"
    assert record["output_object_ids"] == []
    assert record["input_object_ids"] == ["obj-source", "obj-config", "obj-bindings", "obj-prior"]
    assert record["environment_sbom_id"] == "obj-sbom"
    parameters = record["parameters"]
    assert parameters["lineage_mode"] == "exploratory"
    assert parameters["same_source_version_assumed"] is False
    assert parameters["original_captured_at"] is None
    assert parameters["environment_details_object_id"] == "obj-environment"
    assert "beta" in parameters["unit"]


def test_existing_attempt_is_never_overwritten(tmp_path) -> None:
    (tmp_path / "retained").write_text("old attempt")
    with pytest.raises(FileExistsError):
        module().execute(tmp_path / "source", tmp_path, tmp_path / "environment.lock")
    assert (tmp_path / "retained").read_text() == "old attempt"


def test_output_outside_private_namespace_is_rejected(tmp_path) -> None:
    with pytest.raises(ValueError, match="private outputs"):
        module().execute(tmp_path / "source", tmp_path / "new-attempt", tmp_path / "environment.lock")


def test_installed_environment_records_producer_and_lock_identity() -> None:
    described = module().installed_environment(
        "a" * 64, {"producer_revision": "rev", "wheel_sha256": "b" * 64}
    )
    assert described["producer_revision"] == "rev"
    assert described["producer_wheel_sha256"] == "b" * 64
    assert described["lock_sha256"] == "a" * 64
    assert isinstance(described["distributions"], list)
