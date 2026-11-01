"""Extract the pinned MOH workbook with installed native CAS and strict records.

This consumer operation does not qualify native source registration, manifest
closure, original capture dates, scientific applicability or independent recovery.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import importlib.metadata
import io
import json
import subprocess
import sys
import zipfile
from abc import abstractmethod
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Protocol, cast
from uuid import uuid4
lazy from collections.abc import Callable

from packaging.utils import canonicalize_name

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qualify_moh_workbook as qualification
from source_handoff import unique

ROOT = Path(__file__).resolve().parents[1]
INTERFACE = ROOT / "integration/archive/native-producer-interface.json"
HEADER = ("Year", "Total tobacco sold tonnes (excl. cigars/cigarillos)")
YEARS = tuple(range(2010, 2026))
MAX_INPUT_BYTES = 16 * 1024 * 1024


class NativeObject(Protocol):
    """Selected public native CAS receipt fields, without duplicating its implementation."""

    object_id: str
    sha256: str
    path: Path


class NativeInventory(Protocol):
    """Selected public inventory field."""

    object_count: int


class NativeStore(Protocol):
    """Existing producer operations used by this consumer."""

    @abstractmethod
    def put_bytes(self, content: bytes) -> NativeObject:
        """Store actual bytes through the producer."""
        raise NotImplementedError

    @abstractmethod
    def verify(self, object_id: str) -> NativeObject:
        """Verify actual stored bytes through the producer."""
        raise NotImplementedError

    @abstractmethod
    def verified_inventory(self) -> NativeInventory:
        """Read the producer's verified object count."""
        raise NotImplementedError


class NativeRecords(Protocol):
    """Existing strict native record operations."""

    @abstractmethod
    def canonical_record_bytes(self, record: dict[str, Any]) -> bytes:
        """Validate and canonicalize a strict native record."""
        raise NotImplementedError

    @abstractmethod
    def validate_archive_record(self, record: dict[str, Any]) -> None:
        """Revalidate a persisted native record."""
        raise NotImplementedError


def verified_bytes(path: Path, expected: str | None = None) -> bytes:
    """Take one bounded immutable snapshot; parse exactly these verified bytes."""
    if path.is_symlink():
        msg = "Symlink input is forbidden"
        raise ValueError(msg)
    with path.open("rb") as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES or (expected and hashlib.sha256(raw).hexdigest() != expected):
        msg = "Input bytes exceed their bound or differ from the pinned source"
        raise ValueError(msg)
    return raw


def extract_rows(table: list[tuple[object, ...]], sheet: str) -> list[dict[str, Any]]:
    """Retain all sixteen values and exact cells; reject coercion and wrong tables."""
    if sheet != "Sheet1" or len(table) != len(YEARS) + 1 or tuple(table[0]) != HEADER:
        msg = "Unexpected workbook sheet, header or row coverage"
        raise ValueError(msg)
    result: list[dict[str, Any]] = []
    for number, row in enumerate(table[1:], start=2):
        if len(row) != len(HEADER) or type(row[0]) is not int or row[0] != YEARS[number - 2]:
            msg = "Unexpected workbook year, order or columns"
            raise ValueError(msg)
        value = row[1]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            msg = "Non-numeric workbook value; coercion is forbidden"
            raise TypeError(msg)
        decimal = Decimal(str(value))
        if not decimal.is_finite() or decimal < 0:
            msg = "Non-finite or negative workbook value"
            raise ValueError(msg)
        result.append(
            {
                "year": row[0],
                "value_tonnes": str(decimal),
                "sheet": sheet,
                "year_cell": f"A{number}",
                "value_cell": f"B{number}",
            }
        )
    return result


def producer(
    wheel: Path, interface: Path = INTERFACE
) -> tuple[NativeRecords, Callable[[Path], NativeStore], dict[str, Any]]:
    """Verify the actual installed wheel and selected native implementation bytes."""
    pin = qualification.read(interface)
    wheel_bytes = verified_bytes(wheel)
    if hashlib.sha256(wheel_bytes).hexdigest() != pin["wheel_sha256"]:
        msg = "Producer wheel differs from the reviewed interface"
        raise ValueError(msg)
    distribution = importlib.metadata.distribution(pin["distribution"])
    direct = json.loads(distribution.read_text("direct_url.json") or "{}")
    if distribution.version != pin["version"] or direct.get("dir_info", {}).get("editable"):
        msg = "Require the selected installed producer wheel, never an editable source"
        raise ValueError(msg)
    with zipfile.ZipFile(io.BytesIO(wheel_bytes)) as archive:
        for name in archive.namelist():
            if not name.startswith("archive_govt_nz/") or name.endswith("/"):
                continue
            installed = Path(str(distribution.locate_file(name)))
            if (
                installed.is_symlink()
                or not installed.resolve().is_relative_to(Path(sys.prefix).resolve())
                or installed.read_bytes() != archive.read(name)
            ):
                msg = "Installed producer bytes differ from the pinned wheel"
                raise ValueError(msg)
    modules: dict[str, Any] = {}
    for name, expected in pin["module_sha256"].items():
        module = importlib.import_module(name)
        if module.__file__ is None or qualification.digest(Path(module.__file__)) != expected:
            msg = "Imported native interface differs from the frozen producer"
            raise ValueError(msg)
        modules[name] = module
    return (
        cast("NativeRecords", modules["archive_govt_nz.records"]),
        cast("Callable[[Path], NativeStore]", modules["archive_govt_nz.object_store"].ContentAddressedStore),
        pin,
    )


def encoded(value: dict[str, Any]) -> bytes:
    """Serialize deterministic content separately from execution timestamps."""
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def validate_inventory(document: dict[str, Any], installed: dict[str, str]) -> None:
    """Reject incomplete, duplicated or stale Python component inventories."""
    components = [c for c in document["components"] if c["type"] == "library"]
    actual = {(canonicalize_name(c["name"]), c["version"]) for c in components}
    expected = {(canonicalize_name(name), version) for name, version in installed.items()}
    if actual != expected or len(components) != len(expected):
        msg = "SBOM does not match the actual installed Python environment"
        raise ValueError(msg)


def environment_sbom(path: Path | None) -> bytes:
    """Use the maintained CycloneDX validator, then compare actual installed components."""
    if path is None:
        msg = "Supply a complete schema-valid CycloneDX 1.6 environment SBOM"
        raise ValueError(msg)
    raw = verified_bytes(path)
    document = cast("dict[str, Any]", json.loads(raw, object_pairs_hook=unique))
    validation = importlib.import_module("cyclonedx.validation.json")
    schema = importlib.import_module("cyclonedx.schema")
    if validation.JsonStrictValidator(schema.SchemaVersion.V1_6).validate_str(raw.decode()) is not None:
        msg = "Environment SBOM fails the CycloneDX 1.6 schema"
        raise ValueError(msg)
    validate_inventory(document, {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()})
    return raw


def now() -> str:
    """Record current execution time, never substitute it for original capture time."""
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def persist(record: dict[str, Any], path: Path, native: NativeRecords, store: NativeStore) -> str:
    """Persist and reopen actual native canonical records and verify their CAS bytes."""
    raw = native.canonical_record_bytes(record)
    with path.open("xb") as stream:
        stream.write(raw)
    native.validate_archive_record(json.loads(path.read_bytes()))
    saved = store.put_bytes(raw)
    if store.verify(saved.object_id).path.read_bytes() != raw:
        msg = "Native record CAS readback differs"
        raise ValueError(msg)
    return str(saved.object_id)


def extract_and_compare(source: bytes, reference: bytes, sheet_name: str) -> list[dict[str, Any]]:
    """Read the actual snapshotted source with a maintained reader and compare legacy values."""
    library = importlib.import_module("openpyxl")
    book = library.load_workbook(io.BytesIO(source), read_only=True, data_only=False)
    try:
        sheet = book[sheet_name]
        rows = extract_rows(list(sheet.values), sheet.title)
    finally:
        book.close()
    qualification.compare_rows(
        list(csv.DictReader(io.StringIO(reference.decode("utf-8"), newline=""))),
        [[r["year"], r["value_tonnes"]] for r in rows],
    )
    return rows


def verify_objects(store: NativeStore, receipts: list[NativeObject]) -> None:
    """Independently hash actual objects after native verification, not supplied IDs alone."""
    for receipt in receipts:
        verified_bytes(store.verify(receipt.object_id).path, receipt.sha256)


def source_inputs(workbook: Path) -> tuple[dict[str, Any], dict[str, Any], list[bytes]]:
    """Bind the exact metadata and data snapshots actually consumed by extraction."""
    specification = verified_bytes(ROOT / qualification.RECONCILIATION)
    reconciliation = cast("dict[str, Any]", json.loads(specification, object_pairs_hook=unique))
    bindings = verified_bytes(ROOT / "integration/archive/source-bindings.json")
    parsed = cast("dict[str, Any]", json.loads(bindings, object_pairs_hook=unique))
    capture = qualification.checked_capture(parsed, ROOT)
    if capture["sha256"] != reconciliation["source_sha256"]:
        msg = "Source metadata changed during preflight"
        raise ValueError(msg)
    reference = qualification.checked(ROOT, reconciliation["consumer_path"])
    return (
        reconciliation,
        capture,
        [
            verified_bytes(workbook, reconciliation["source_sha256"]),
            verified_bytes(reference, reconciliation["consumer_sha256"]),
            specification,
            bindings,
        ],
    )


def execute(
    workbook: Path,
    out: Path,
    environment_lock: Path,
    wheel: Path | None = None,
    sbom: Path | None = None,
) -> dict[str, Any]:
    """Execute one new private attempt; leave source inputs and failed attempts intact."""
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
    native, factory, pin = producer(wheel)
    reconciliation, capture, snapshots = source_inputs(workbook)
    lock_sha = qualification.digest(environment_lock)
    sbom_bytes = environment_sbom(sbom)
    out.mkdir(parents=True)
    store = factory(out / "cas")
    inputs = [store.put_bytes(raw) for raw in snapshots]
    software_bill = store.put_bytes(sbom_bytes)
    environment = store.put_bytes(
        encoded(
            {
                "python": sys.version,
                "producer_revision": pin["producer_revision"],
                "producer_wheel_sha256": pin["wheel_sha256"],
                "lock_sha256": lock_sha,
                "distributions": sorted(
                    (d.metadata["Name"], d.version) for d in importlib.metadata.distributions()
                ),
            }
        )
    )
    started = now()
    attempt = "tobac-moh-" + uuid4().hex
    revision = subprocess.check_output(  # noqa: S603 -- Fixed local Git read; no shell or source-provided argv.
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],  # noqa: S607 -- Fixed developer tool.
        text=True,
        timeout=15,
    ).strip()
    transformation: dict[str, Any] = {
        "schema_version": "archive-govt-nz.transformation/v1",
        "record_id": attempt,
        "observed_at": started,
        "state": "failed",
        "evidence": [],
        "name": "tobac.moh-workbook-extract-and-compare",
        "version": "1",
        "implementation_revision": revision,
        "input_object_ids": [r.object_id for r in inputs],
        "output_object_ids": [],
        "parameters": {
            "lineage_mode": "exploratory",
            "source_id": qualification.SOURCE_ID,
            "archive_id": qualification.ARCHIVE_ID,
            "source_url": reconciliation["source_url"],
            "original_captured_at": capture["captured_at"],
            "source_warc_sha256_not_verified_this_run": capture["warc_sha256"],
            "comparison_only_object_id": inputs[1].object_id,
            "environment_details_object_id": environment.object_id,
            "implementation_sha256": qualification.digest(Path(__file__)),
            "command": sys.argv,
            "shared_data_identity": "NZ_MOH_tobacco_returns",
            "unit": "tonnes/year",
        },
        "environment_sbom_id": software_bill.object_id,
        "started_at": started,
        "ended_at": started,
        "information_loss": "Values/cells retained; workbook formatting omitted; no unit conversion",
        "deterministic": True,
    }
    try:
        rows = extract_and_compare(
            store.verify(inputs[0].object_id).path.read_bytes(),
            store.verify(inputs[1].object_id).path.read_bytes(),
            reconciliation["sheet"],
        )
        output = store.put_bytes(
            encoded({"source_id": qualification.SOURCE_ID, "unit": "tonnes/year", "rows": rows})
        )
        verify_objects(store, [*inputs, environment, software_bill, output])
        transformation.update(state="succeeded", ended_at=now(), output_object_ids=[output.object_id])
    except Exception:
        transformation["ended_at"] = now()
        persist(transformation, out / "failed-transformation.json", native, store)
        raise
    transformation_id = persist(transformation, out / "transformation.json", native, store)
    validation = {
        "schema_version": "archive-govt-nz.validation/v1",
        "record_id": attempt + "-validation",
        "observed_at": now(),
        "state": "passed",
        "evidence": [],
        "validator_name": "tobac.moh-cell-parity-and-native-fixity",
        "validator_version": "1",
        "subject_ids": [r.object_id for r in [*inputs, environment, software_bill, output]],
        "checks": [
            "16 exact year/value pairs",
            "Sheet1 A2:B17 locators",
            "native CAS actual bytes",
            "strict native record readback",
        ],
        "findings": [],
        "started_at": started,
        "ended_at": now(),
    }
    validation_id = persist(validation, out / "validation.json", native, store)
    result = {
        "schema": "tobac.moh-native-extraction.v1",
        "execution_mode": "exploratory",
        "attempt_id": attempt,
        "producer_revision": pin["producer_revision"],
        "producer_wheel_sha256": pin["wheel_sha256"],
        "implementation_revision": revision,
        "implementation_sha256": qualification.digest(Path(__file__)),
        "source_sha256": inputs[0].sha256,
        "consumer_sha256": inputs[1].sha256,
        "original_captured_at": capture["captured_at"],
        "source_capture_time_verified": False,
        "extracted_object_id": output.object_id,
        "transformation_object_id": transformation_id,
        "validation_object_id": validation_id,
        "environment_object_id": environment.object_id,
        "environment_sbom_object_id": software_bill.object_id,
        "matched_rows": rows,
        "native_object_count": store.verified_inventory().object_count,
        "native_lineage_qualified": False,
        "scientific_qualification": False,
        "automatically_conditions_live_model": False,
        "remaining_producer_gates": pin["remaining_producer_gates"],
        "scope": "Actual workbook extraction/native CAS/records; manifest and runner closure remain open",
    }
    with (out / "receipt.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + "\n")
    return result


def main() -> None:
    """Require explicit local sources/artifacts and a new private output location."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--environment-lock", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--environment-sbom", required=True, type=Path)
    args = parser.parse_args()
    execute(args.workbook, args.out, args.environment_lock, args.wheel, args.environment_sbom)
    sys.stdout.write("Extracted 16 unchanged values with native records; full lineage remains unqualified\n")


if __name__ == "__main__":
    main()
