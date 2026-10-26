"""Re-execute the producer's native workbook/WARC checks without changing source objects."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_handoff import checked, digest, read

ROOT = Path(__file__).resolve().parents[1]
INPUTS = "integration/archive/moh-pathway-inputs.json"
RECONCILIATION = "integration/archive/workbook-reconciliation.json"
SOURCE_ID = "long-nz-tobacco-tonnes-2025"
ARCHIVE_ID = "tobac-7ee48855a1ed1c4b"


def checked_capture(native: dict[str, Any], root: Path) -> dict[str, Any]:
    """Accept only a unique native workbook result with the original pinned identities."""
    original = read(checked(root, RECONCILIATION))
    bindings = read(checked(root, "integration/archive/source-bindings.json"))
    sources = [s for s in native["sources"] if s["archive_id"] == ARCHIVE_ID]
    if len(sources) != 1 or native["register_sha256"] != bindings["register_sha256"]:
        msg = "Native source/register identity mismatch"
        raise ValueError(msg)
    captures = [c for c in sources[0]["captures"] if c["uri"] == original["source_url"]]
    if len(captures) != 1:
        msg = "Expected one native workbook capture"
        raise ValueError(msg)
    capture = captures[0]
    if (
        capture["status"] != "source_workbook_values_matched"
        or capture["sha256"] != original["source_sha256"]
        or capture["warc_sha256"] != original["warc_sha256"]
    ):
        msg = "Native workbook or WARC qualification mismatch"
        raise ValueError(msg)
    return capture


def compare_rows(rows: list[dict[str, str]], expected: list[list[Any]]) -> list[dict[str, Any]]:
    """Require complete exact numerical parity, unchanged source/unit and calendar labels."""
    years = list(range(2010, 2026))
    if len(rows) != len(years) or [r["year"] for r in rows] != [str(y) for y in years]:
        msg = "Missing, duplicated or reordered consumer years"
        raise ValueError(msg)
    if [r[0] for r in expected] != years:
        msg = "Producer workbook rows do not match the declared annual series"
        raise ValueError(msg)
    result: list[dict[str, Any]] = []
    for row, (year, value) in zip(rows, expected, strict=True):
        period = (f"{year}-01-01", f"{year + 1}-01-01")
        if (
            row["source_id"] != SOURCE_ID
            or row["unit"] != "tonnes/year"
            or (row["period_start"], row["period_end"]) != period
            or not Decimal(row["value"]).is_finite()
            or Decimal(row["value"]) != Decimal(str(value))
        ):
            msg = "Consumer value, source, unit or period mismatch"
            raise ValueError(msg)
        result.append(
            {"year": year, "value_tonnes": row["value"], "period_start": period[0], "period_end": period[1]}
        )
    return result


def execute(command: list[str]) -> str:
    """Run fixed argument vectors for explicitly selected read-only producer verification."""
    return subprocess.check_output(command, text=True, timeout=120)  # noqa: S603  # Explicit native verifier/Python argv; no shell or source text commands.


def qualify(producer: Path, python: Path, archive: Path, out: Path, objects: Path) -> dict[str, Any]:
    """Reverify native fixity, payload/request identity and workbook values; preserve missing time."""
    descriptor = read(checked(ROOT, INPUTS))
    tool = checked(producer, descriptor["producer_tool"])
    register = checked(producer, descriptor["producer_register"])
    capture_receipt = checked(archive, descriptor["native_capture_receipt"])
    for path, sha in (
        (tool, descriptor["producer_tool_sha256"]),
        (register, descriptor["producer_register_sha256"]),
        (capture_receipt, descriptor["native_capture_receipt_sha256"]),
    ):
        if digest(path) != sha:
            msg = "Producer inputs changed; requalification required"
            raise ValueError(msg)
    environment = json.loads(
        execute(
            [
                str(python),
                "-c",
                (
                    "import sys,json,importlib.metadata as m; "
                    "print(json.dumps({'python':list(sys.version_info[:3]),'packages':"
                    "{p:m.version(p) for p in ['openpyxl','warcio']}}))"
                ),
            ]
        )
    )
    if environment != descriptor["qualified_producer_environment"]:
        msg = "Producer interpreter or libraries differ from the qualified profile"
        raise ValueError(msg)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="moh-native-", dir=out.parent) as temp:
        native_path = Path(temp) / "native.json"
        execute(
            [
                str(python),
                str(tool),
                "--register",
                str(register),
                "--capture",
                str(capture_receipt),
                "--store",
                str(archive / descriptor["native_store"]),
                "--root",
                str(archive),
                "--out",
                str(native_path),
            ]
        )
        native = read(native_path)
        capture = checked_capture(native, ROOT)
        native_sha = digest(native_path)
    original = read(checked(ROOT, RECONCILIATION))
    csv_path = checked(ROOT, original["consumer_path"])
    if digest(csv_path) != original["consumer_sha256"]:
        msg = "Consumer input hash changed"
        raise ValueError(msg)
    source = next(s for s in read(register)["sources"] if s["archive_id"] == ARCHIVE_ID)
    asset = next(a for a in source["assets"] if a["url"] == capture["uri"])
    if asset["consumer_sha256"] != original["consumer_sha256"]:
        msg = "Producer extraction is bound to a different consumer"
        raise ValueError(msg)
    with csv_path.open(newline="", encoding="utf-8") as stream:
        values = compare_rows(list(csv.DictReader(stream)), asset["expected_rows"])
    # Staging is consumer-owned; all canonical producer objects remain untouched.
    target = read(capture_receipt)["targets"][0]
    body = archive / descriptor["native_store"] / "sha256" / capture["sha256"][:2] / capture["sha256"]
    warc = checked(archive, target["warc"]["path"])
    objects.mkdir(parents=True, exist_ok=False)
    for path, sha in ((body, capture["sha256"]), (warc, capture["warc_sha256"])):
        if digest(path) != sha:
            msg = "Source object changed after native verification"
            raise ValueError(msg)
        shutil.copyfile(path, objects / sha)
    return {
        "schema": "tobac.moh-workbook-qualification.v1",
        "verified_at": datetime.now(UTC).isoformat(),
        "status": "native_fixity_and_values_verified",
        "original_capture_timestamp": capture["captured_at"],
        "capture_time_status": "unverified_missing_original_WARC_Date",
        "source_url": capture["uri"],
        "source_sha256": capture["sha256"],
        "warc_sha256": capture["warc_sha256"],
        "consumer_path": original["consumer_path"],
        "consumer_sha256": original["consumer_sha256"],
        "matched_rows": values,
        "producer_tool_sha256": digest(tool),
        "producer_register_sha256": digest(register),
        "native_verifier_output_sha256": native_sha,
        "producer_environment": environment,
        "checks": [
            "CAS fixity",
            "WARC fixity",
            "WARC/CAS payload equality",
            "request URL identity",
            "native openpyxl workbook/header parity",
            "all 16 consumer year/value pairs",
        ],
        "scientific_qualification": False,
        "automatically_conditions_live_model": False,
    }


def main() -> None:
    """Require explicit local producer paths and create a new immutable execution receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--producer-python", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if sys.version_info[:3] != (3, 15, 1):
        msg = "Consumer requires Python 3.15.1"
        raise RuntimeError(msg)
    if args.out.exists() or args.objects.exists():
        msg = "Choose new receipt and object staging paths; preserve earlier executions"
        raise ValueError(msg)
    result = qualify(
        args.producer.resolve(),
        args.producer_python.absolute(),
        args.archive.resolve(),
        args.out,
        args.objects,
    )
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    sys.stdout.write(
        "Verified 16 workbook values and native CAS/WARC identities; scientific qualification open\n"
    )


if __name__ == "__main__":
    main()
