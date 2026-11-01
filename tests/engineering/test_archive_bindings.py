"""Guard archive links without altering scientific input or source identities."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "integration/archive"


def test_all_bibliography_aliases_have_archive_identity() -> None:
    register = json.loads((ARCHIVE / "source-register.json").read_text(encoding="utf-8"))
    expected = set()
    for path, digest in register["collection_sha256"].items():
        source = ROOT / path
        assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
        expected.update((path, ref["id"]) for ref in json.loads(source.read_text(encoding="utf-8")))
    actual = [
        (ref["collection"], ref["source_id"])
        for source in register["sources"]
        for ref in source["references"]
    ]
    assert len(actual) == len(set(actual))
    assert set(actual) == expected


def test_input_hashes_rows_and_archive_targets() -> None:
    import csv  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    manifest = json.loads((ARCHIVE / "consumer-inputs.json").read_text(encoding="utf-8"))
    register = json.loads((ARCHIVE / "source-register.json").read_text(encoding="utf-8"))
    identities = {row["archive_id"] for row in register["sources"]}
    expected = {p.relative_to(ROOT).as_posix() for p in ROOT.glob("data/**/*.csv")}
    expected |= {p.relative_to(ROOT).as_posix() for p in ROOT.glob("evidence/prior_work/**/*.csv")}
    assert {row["path"] for row in manifest["inputs"]} == expected
    for row in manifest["inputs"]:
        path = ROOT / row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        with path.open(newline="", encoding="utf-8") as stream:
            assert len(list(csv.DictReader(stream))) == row["rows"]
        for ref in row["source_references"]:
            assert ref["archive_id"] in identities or ref["status"] == "unresolved_or_internal_reference"
    for row in manifest["supporting_files"]:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]


def test_bindings_match_register_and_do_not_upgrade_evidence() -> None:
    register = json.loads((ARCHIVE / "source-register.json").read_text(encoding="utf-8"))
    receipt = json.loads((ARCHIVE / "source-bindings.json").read_text(encoding="utf-8"))
    assert (
        receipt["register_sha256"]
        == hashlib.sha256((ARCHIVE / "source-register.json").read_bytes()).hexdigest()
    )
    assert {r["archive_id"] for r in receipt["sources"]} == {r["archive_id"] for r in register["sources"]}
    assert all(not r["redistribution_authorized"] for r in receipt["sources"])
    statuses = {c["status"] for r in receipt["sources"] for c in r["captures"]}
    assert "challenge_not_source" in statuses
    assert "retrieval_failed" in statuses
    assert "metadata_only" in statuses
    assert "source_html_identity_observed" in statuses
    assert "source_workbook_values_matched" in statuses


def test_original_workbook_reconciliation_is_bound_to_consumer_input() -> None:
    receipt = json.loads((ARCHIVE / "workbook-reconciliation.json").read_text(encoding="utf-8"))
    source = ROOT / receipt["consumer_path"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == receipt["consumer_sha256"]
    assert receipt["matched_rows"] == 16
    assert receipt["status"] == "all_16_values_match_exactly"
    bindings = json.loads((ARCHIVE / "source-bindings.json").read_text(encoding="utf-8"))
    assert any(
        c.get("sha256") == receipt["source_sha256"] and c["status"] == "source_workbook_values_matched"
        for r in bindings["sources"]
        for c in r["captures"]
    )


def test_native_export_preserves_binding_scope_and_producer_pin() -> None:
    bindings_path = ARCHIVE / "source-bindings.json"
    bindings = json.loads(bindings_path.read_bytes())
    refs = json.loads((ARCHIVE / "native-source-refs.json").read_bytes())
    pin = json.loads((ARCHIVE / "native-registration-interface.json").read_bytes())
    assert refs["source_bindings_sha256"] == hashlib.sha256(bindings_path.read_bytes()).hexdigest()
    assert refs["wheel_sha256"] == pin["wheel_sha256"]
    assert refs["producer_revision"] == pin["producer_revision"]
    assert refs["source_register_sha256"] == bindings["register_sha256"]
    assert refs["capture_receipt_sha256"] == bindings["capture_receipt_sha256"]
    expected = sorted(bindings["sources"], key=lambda item: item["archive_id"])
    for row, native in zip(expected, refs["native_source_refs"], strict=True):
        assert row["archive_id"] == native["archive_id"]
        assert row["references"] == native["consumer_aliases"]
        assert row["redistribution_authorized"] == native["redistribution_authorized"]
        for cap, actual in zip(row["captures"], native["captures"], strict=True):
            assert {key: actual[key] for key in cap} == cap
            registration = actual["native_registration"]
            if cap["status"] in {"source_workbook_values_matched", "source_html_identity_observed"}:
                assert registration["object_id"] == "sha256:" + cap["sha256"]
                assert registration["observation_id"] == row["archive_id"]
            else:
                assert registration is None
            assert actual["bytes_verified"] == ("sha256" in cap)
    assert refs["native_lineage_qualified"] is False
    assert refs["scientific_qualification"] is False
