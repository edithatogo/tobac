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
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "evidence/prior_work/v2.9.0/"
MANIFEST = "integration/prior_work_manifest.json"
SUBSET = "subset_by_source_ID_exact_record_objects_reformatted"
SUBSET_CANONICAL_DOI = "subset_by_source_ID_exact_record_objects_reformatted_canonical_doi"
LOCAL_DOCUMENTS = {
    "evidence/prior_work/v2.9.0/requests/LONGITUDINAL_DATA_ADDENDUM_v2.7.0.md": (
        "95b92297b51f251873a18adcf2e0c2bd25d13a042e2713f1dcef9b77cbfd2e1d"
    ),
    "evidence/prior_work/v2.9.0/requests/empirical_20261024/R05_ASSAY_PERFORMANCE_ADDENDUM_v2.6.0.md": (
        "92ebf7c34c4e59cff318e124c185475b4822f215654f058a573779ebf2f68e9c"
    ),
}
TRANSFORMS = {"none", "CRLF_to_LF_only", SUBSET, SUBSET_CANONICAL_DOI}


def sha(data: bytes) -> str:
    """Return the SHA-256 digest of the supplied source bytes."""
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys while preserving their decoded values."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            msg = f"Duplicate JSON key: {key}"
            raise ValueError(msg)
        result[key] = value
    return result


def read_json(text: str) -> Any:  # noqa: ANN401  # Raw JSON may have any root shape; callers validate the required schema.
    """Decode JSON while rejecting duplicate object keys."""
    return json.loads(text, object_pairs_hook=unique_pairs)


def relative_path(value: str, prefix: str) -> PurePosixPath:
    """Validate a canonical relative path within the declared archive prefix."""
    if not isinstance(cast("object", value), str) or "\\" in value:
        msg = "Invalid relative path"
        raise ValueError(msg)
    path = PurePosixPath(value)
    if not value.startswith(prefix) or path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        msg = "Path outside declared snapshot"
        raise ValueError(msg)
    return path


def checked_file(root: Path, name: str) -> Path:
    """Resolve a required repository file while rejecting symlink traversal."""
    path = root
    for part in PurePosixPath(name).parts:
        path /= part
        if path.is_symlink():
            msg = f"Forbidden symlink: {name}"
            raise ValueError(msg)
    if not path.is_file():
        msg = f"Missing file: {name}"
        raise ValueError(msg)
    return path


def verify(root: Path = ROOT, archive: Path | None = None) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0915  # Keep ordered model validation and report assembly in one visible operation.; Keep explicit fail-closed validation branches together.; Keep the declared numerical/report sequence visible and ordered.
    """Verify retained source and output integrity without claiming scientific qualification."""
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
        msg = "Invalid schema or overstated incorporation scope"
        raise ValueError(msg)
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        msg = "Missing file inventory"
        raise ValueError(msg)
    entries = cast("list[dict[str, Any]]", entries)
    seen: set[str] = set()
    local_documents: list[str] = []
    rows_total = 0
    tokens: set[str] = set()
    references: list[dict[str, Any]] | None = None
    for item in entries:
        name = relative_path(item["path"], PREFIX).as_posix()
        relative_path(item["archive_path"], "tobac/")
        if name in seen:
            msg = "Duplicate file inventory entry"
            raise ValueError(msg)
        seen.add(name)
        if (
            not isinstance(item.get("role"), str)
            or not item["role"].strip()
            or item.get("transformation") not in TRANSFORMS
            or any(not re.fullmatch(r"[0-9a-f]{64}", item.get(k, "")) for k in ("sha256", "archive_sha256"))
        ):
            msg = "Missing/invalid role, transformation or hash"
            raise ValueError(msg)
        if name in LOCAL_DOCUMENTS:
            if item["sha256"] != LOCAL_DOCUMENTS[name]:
                msg = "Local document historical binding changed"
                raise ValueError(msg)
            local_documents.append(name)
            continue
        data = checked_file(root, name).read_bytes()
        if sha(data) != item["sha256"]:
            msg = f"Content hash mismatch: {name}"
            raise ValueError(msg)
        if name.endswith(".csv"):
            reader = csv.DictReader(io.StringIO(data.decode("utf-8")))
            records = list(reader)
            if (
                not reader.fieldnames
                or len(set(reader.fieldnames)) != len(reader.fieldnames)
                or any(None in r or any(v is None for v in r.values()) for r in records)
            ):
                msg = f"Malformed CSV: {name}"
                raise ValueError(msg)
            if type(item.get("rows")) is not int or len(records) != item["rows"]:
                msg = f"CSV row count mismatch: {name}"
                raise ValueError(msg)
            rows_total += len(records)
            for row in records:
                for key in ("source_id", "source_ids", "legal_context_source_ids"):
                    tokens.update(t.strip() for t in re.split(r"[;|]", row.get(key, "")) if t.strip())
                for key in ("current_raw_observation", "admissible_as_current_nz_raw_assay"):
                    if key in row and row[key].lower() != "false":
                        msg = "Historical evidence presented as current raw observation"
                        raise ValueError(msg)
        elif name.endswith("/references.csl.json"):
            references = read_json(data.decode("utf-8"))
            if not isinstance(cast("object", references), list) or len(
                cast("list[dict[str, Any]]", references)
            ) != item.get("records"):
                msg = "Bibliography record count mismatch"
                raise ValueError(msg)
    actual = {
        p.relative_to(root).as_posix() for p in (root / PREFIX).rglob("*") if p.is_file() or p.is_symlink()
    }
    if actual != seen - set(local_documents):
        msg = "Unregistered or missing snapshot files"
        raise ValueError(msg)
    if references is None:
        msg = "Missing inherited bibliography"
        raise ValueError(msg)
    ids = [r["id"] for r in references]
    if len(set(ids)) != len(ids) or sorted(ids) != manifest["source_ids"]:
        msg = "Bibliography identities differ"
        raise ValueError(msg)
    if sorted(tokens - set(ids)) != manifest["unmatched_source_tokens"]:
        msg = "Undeclared source tokens or lost reference linkage"
        raise ValueError(msg)
    if not set(ids) <= tokens:
        msg = "Bibliography contains unrelated source identities"
        raise ValueError(msg)
    archive_checked = False
    if archive is not None:
        if sha(Path(archive).read_bytes()) != manifest["archive"]["sha256"]:
            msg = "Archive hash does not match declared predecessor"
            raise ValueError(msg)
        with zipfile.ZipFile(archive) as source:
            for item in entries:
                raw = source.read(item["archive_path"])
                if sha(raw) != item["archive_sha256"]:
                    msg = "Source member hash differs"
                    raise ValueError(msg)
                if item["path"] in LOCAL_DOCUMENTS:
                    continue
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
                            msg = "Stored DOI is not canonical"
                            raise ValueError(msg)
                        expected = [dict(r, DOI=r["DOI"].lower()) if r.get("DOI") else r for r in expected]
                    if references != expected:
                        msg = "Inherited reference records changed"
                        raise ValueError(msg)
                else:
                    expected = raw if item["transformation"] == "none" else raw.replace(b"\r\n", b"\n")
                    if expected != copied:
                        msg = "Source bytes changed beyond declared newline conversion"
                        raise ValueError(msg)
        archive_checked = True
    return {
        "status": "pass",
        "files": len(entries) - len(local_documents),
        "catalogued_files": len(entries),
        "local_documents_not_verified": local_documents,
        "csv_rows": rows_total,
        "bibliography_records": len(ids),
        "source_archive_checked": archive_checked,
        "automatically_conditions_live_model": False,
        "scope": "public_preservation_and_internal_linkage_local_documents_not_verified",
    }


def main() -> None:
    """Parse command-line options, execute the selected operation and report its result."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.root, args.archive), indent=2))  # noqa: T201  # CLI emits the requested structured result on stdout.


if __name__ == "__main__":
    main()
