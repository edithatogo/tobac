"""Stage the declared consumer estate for an owner-held, private recovery generation."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "integration/archive"


def read(path: Path) -> dict[str, Any]:
    """Read one committed declaration."""
    return json.loads(path.read_bytes())


def digest(path: Path) -> str:
    """Hash locally retained contents."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def files_for_project() -> list[str]:
    """Select committed code, model/evidence inputs and referenced context from the accepted records."""
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())  # noqa: S607 -- Fixed local Git read.
    names = {
        n
        for n in tracked
        if n.startswith(
            ("src/", "scripts/", "engineering/", "configs/", "data/", "evidence/", "integration/archive/")
        )
    }
    names.update(
        {
            "LICENSE",
            "NOTICE",
            "README.md",
            "pyproject.toml",
            "requirements.lock",
            ".python-version",
            "noxfile.py",
            "integration/baseline.json",
        }
    )
    rows = read(ARCHIVE / "p4-dataset-migration_20261031.json")["migrated"]
    for row in rows:
        if digest(ROOT / row["path"]) != row["sha256"]:
            msg = f"Dataset inventory drift: {row['path']}"
            raise ValueError(msg)
        names.add(row["path"])
    for result in read(ARCHIVE / "scientific-lineage-checkpoint_python3152_20261106.json")[
        "runner_results"
    ].values():
        for name, key in result["executed_input_objects"].items():
            if "sha256:" + digest(ROOT / name) != key:
                msg = f"Scientific input drift: {name}"
                raise ValueError(msg)
            names.add(name)
    if not names <= tracked:
        msg = "Declared project inputs must be tracked"
        raise ValueError(msg)
    return sorted(names)


def copy_file(source: Path, target: Path, expected: str | None = None) -> None:
    """Refuse symlink substitution and validate known historical digests."""
    if source.is_symlink() or not source.is_file() or (expected and digest(source) != expected):
        msg = f"Missing or changed declared file: {source.name}"
        raise ValueError(msg)
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as incoming, target.open("xb") as output:
        shutil.copyfileobj(incoming, output)


def capture_files(root: Path, out: Path) -> dict[str, int]:
    """Use the four pinned generations, including retrieval failures, to select originals and WARCs."""
    pins = set(read(ARCHIVE / "source-bindings.json")["capture_receipt_sha256"])
    seen: set[str] = set()
    bodies: dict[str, str] = {}
    warcs: dict[str, str] = {}
    failures = 0
    for path in sorted(root.glob("*/capture.json")):
        sha = digest(path)
        if sha not in pins:
            continue
        if sha in seen:
            msg = "Duplicate historical capture generation"
            raise ValueError(msg)
        seen.add(sha)
        copy_file(path, out / path.relative_to(root), sha)
        for item in read(path)["targets"]:
            if item["status"] == "failed":
                failures += 1
                continue
            body = item["sha256"]
            bodies[f"cas/sha256/{body[:2]}/{body}"] = body
            warc = item["warc"]
            prefix = "build/tobac/"
            if not warc["path"].startswith(prefix):
                msg = "Unexpected capture path"
                raise ValueError(msg)
            name = warc["path"][len(prefix) :]
            if not (root / name).resolve().is_relative_to(root.resolve()):
                msg = "WARC escapes declared capture tree"
                raise ValueError(msg)
            warcs[name] = warc["sha256"]
    if seen != pins:
        msg = "Missing historical capture generation"
        raise ValueError(msg)
    for name, sha in (bodies | warcs).items():
        copy_file(root / name, out / name, sha)
    return {
        "capture_generations": len(seen),
        "capture_bodies": len(bodies),
        "warcs": len(warcs),
        "failed_targets": failures,
    }


def copy_tree(source: Path, target: Path) -> None:
    """Copy only regular files and preserve empty CAS directories."""
    target.mkdir(parents=True)
    for path in sorted(source.rglob("*")):
        destination = target / path.relative_to(source)
        if path.is_dir() and not path.is_symlink():
            destination.mkdir(exist_ok=True)
        else:
            copy_file(path, destination)


def main() -> None:
    """Supply the accepted private bindings explicitly and use a new staging root."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("out", "captures", "registrations", "attempts", "moh", "shine"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    names = files_for_project()
    subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *names], cwd=ROOT, check=True)  # noqa: S603,S607 -- Reviewed paths and fixed read-only operation.
    for name in names:
        copy_file(ROOT / name, args.out / "project" / name)
    counts = capture_files(args.captures, args.out / "captures")
    copy_tree(args.registrations, args.out / "registrations")
    accepted = read(ARCHIVE / "scientific-lineage-checkpoint_python3152_20261106.json")["runner_results"]
    for name, run in accepted.items():
        attempt = args.attempts / name
        terminal = read(attempt / "terminal")
        if (
            terminal["state"] != "succeeded"
            or terminal["attempt_id"] != run["attempt_id"]
            or terminal["result"]["manifest"] != run["manifest"]
        ):
            msg = f"Wrong native attempt: {name}"
            raise ValueError(msg)
        copy_tree(attempt, args.out / "attempts" / name)
    for name, original in (("moh", args.moh), ("shine", args.shine)):
        target = args.out / "extractions" / name
        copy_tree(original / "cas", target / "cas")
        for entry in ("receipt.json", "transformation.json", "validation.json"):
            copy_file(original / entry, target / entry)
    copy_tree(args.moh / "capture-evidence", args.out / "extractions/moh/capture-evidence")
    register = read(ARCHIVE / "source-register.json")["sources"]
    summary = {
        "schema": "tobac.recovery-declaration.v1",
        "project_files": len(names),
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),  # noqa: S607 -- Fixed revision query.
        **counts,
        "source_identities": len(register),
        "accepted_attempts": len(accepted),
        "accepted_outputs": sum(v["output_files"] for v in accepted.values()),
        "p4_inventory": len(read(ARCHIVE / "p4-dataset-migration_20261031.json")["migrated"]),
        "restriction": "Private owner-held offline copy; retain source-specific rights.",
    }
    (args.out / "declaration.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
