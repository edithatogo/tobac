"""Verify preserved prior-work bytes and roles, not scientific validity or model fit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "evidence/prior_work/v2.9.0/"
MANIFEST = "integration/prior_work_manifest.json"
SUBSET = "subset_by_source_ID_exact_record_objects_reformatted"
SUBSET_CANONICAL_DOI = "subset_by_source_ID_exact_record_objects_reformatted_canonical_doi"
TRANSFORMS = {"none", "CRLF_to_LF_only", SUBSET, SUBSET_CANONICAL_DOI}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(text: str):
    return json.loads(text, object_pairs_hook=unique_pairs)


def relative_path(value: str, prefix: str) -> PurePosixPath:
    if not isinstance(value, str) or "\\" in value:
        raise ValueError("Invalid relative path")
    path = PurePosixPath(value)
    if not value.startswith(prefix) or path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise ValueError("Path outside declared snapshot")
    return path


def checked_file(root: Path, name: str) -> Path:
    path = root
    for part in PurePosixPath(name).parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f"Forbidden symlink: {name}")
    if not path.is_file():
        raise ValueError(f"Missing file: {name}")
    return path


def verify(root: Path = ROOT, archive: Path | None = None) -> dict:
    root = Path(root).resolve()
    manifest = read_json(checked_file(root, MANIFEST).read_text(encoding="utf-8"))
    if (
        manifest.get("schema") != "tobac.prior-work-incorporation.v1"
        or manifest.get("automatically_conditions_live_model") is not False
        or manifest.get("bibliographic_validation_performed") is not False
        or type(manifest.get("new_raw_assays")) is not int
        or manifest["new_raw_assays"] != 0
        or type(manifest.get("supplier_quotes_received_by_this_import")) is not int
        or manifest["supplier_quotes_received_by_this_import"] != 0
    ):
        raise ValueError("Invalid schema or overstated incorporation scope")
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Missing file inventory")
    seen = set()
    rows_total = 0
    tokens = set()
    references = None
    for item in entries:
        name = relative_path(item["path"], PREFIX).as_posix()
        relative_path(item["archive_path"], "tobac/")
        if name in seen:
            raise ValueError("Duplicate file inventory entry")
        seen.add(name)
        if (
            not isinstance(item.get("role"), str)
            or not item["role"].strip()
            or item.get("transformation") not in TRANSFORMS
            or any(not re.fullmatch("[0-9a-f]{64}", item.get(k, "")) for k in ("sha256", "archive_sha256"))
        ):
            raise ValueError("Missing/invalid role, transformation or hash")
        data = checked_file(root, name).read_bytes()
        if sha(data) != item["sha256"]:
            raise ValueError(f"Content hash mismatch: {name}")
        if name.endswith(".csv"):
            reader = csv.DictReader(io.StringIO(data.decode("utf-8")))
            records = list(reader)
            if (
                not reader.fieldnames
                or len(set(reader.fieldnames)) != len(reader.fieldnames)
                or any(None in r or any(v is None for v in r.values()) for r in records)
            ):
                raise ValueError(f"Malformed CSV: {name}")
            if type(item.get("rows")) is not int or len(records) != item["rows"]:
                raise ValueError(f"CSV row count mismatch: {name}")
            rows_total += len(records)
            for row in records:
                for key in ("source_id", "source_ids", "legal_context_source_ids"):
                    tokens.update(t.strip() for t in re.split("[;|]", row.get(key, "")) if t.strip())
                for key in ("current_raw_observation", "admissible_as_current_nz_raw_assay"):
                    if key in row and row[key].lower() != "false":
                        raise ValueError("Historical evidence presented as current raw observation")
        elif name.endswith("/references.csl.json"):
            references = read_json(data.decode("utf-8"))
            if not isinstance(references, list) or len(references) != item.get("records"):
                raise ValueError("Bibliography record count mismatch")
    actual = {
        p.relative_to(root).as_posix() for p in (root / PREFIX).rglob("*") if p.is_file() or p.is_symlink()
    }
    if actual != seen:
        raise ValueError("Unregistered or missing snapshot files")
    if references is None:
        raise ValueError("Missing inherited bibliography")
    ids = [r["id"] for r in references]
    if len(set(ids)) != len(ids) or sorted(ids) != manifest["source_ids"]:
        raise ValueError("Bibliography identities differ")
    if sorted(tokens - set(ids)) != manifest["unmatched_source_tokens"]:
        raise ValueError("Undeclared source tokens or lost reference linkage")
    if not set(ids) <= tokens:
        raise ValueError("Bibliography contains unrelated source identities")
    archive_checked = False
    if archive is not None:
        if sha(Path(archive).read_bytes()) != manifest["archive"]["sha256"]:
            raise ValueError("Archive hash does not match declared predecessor")
        with zipfile.ZipFile(archive) as source:
            for item in entries:
                raw = source.read(item["archive_path"])
                if sha(raw) != item["archive_sha256"]:
                    raise ValueError("Source member hash differs")
                copied = checked_file(root, item["path"]).read_bytes()
                if item["transformation"] in {SUBSET, SUBSET_CANONICAL_DOI}:
                    original = read_json(raw.decode("utf-8"))
                    selected = {r["id"]: r for r in original}
                    expected = [selected[i] for i in sorted(ids)]
                    if item["transformation"] == SUBSET_CANONICAL_DOI:
                        # Only the DOI may differ, and only by case: CSL validation requires the
                        # canonical lower-case form, which is the same identifier (DOIs are
                        # case-insensitive). Every other field must still equal the archive.
                        if any(r.get("DOI") and r["DOI"] != r["DOI"].lower() for r in references):
                            raise ValueError("Stored DOI is not canonical")
                        expected = [dict(r, DOI=r["DOI"].lower()) if r.get("DOI") else r for r in expected]
                    if references != expected:
                        raise ValueError("Inherited reference records changed")
                else:
                    expected = raw if item["transformation"] == "none" else raw.replace(b"\r\n", b"\n")
                    if expected != copied:
                        raise ValueError("Source bytes changed beyond declared newline conversion")
        archive_checked = True
    return {
        "status": "pass",
        "files": len(entries),
        "csv_rows": rows_total,
        "bibliography_records": len(ids),
        "source_archive_checked": archive_checked,
        "automatically_conditions_live_model": False,
        "scope": "preservation_and_internal_linkage_not_scientific_validation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.root, args.archive), indent=2))


if __name__ == "__main__":
    main()
