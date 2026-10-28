"""Validate actual Git objects and stage minimal exports using one reviewed policy."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import shutil
import stat
import subprocess
import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
POLICY = "engineering/publication-policy.json"
MAX_DEPTH = 3
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024
PUBLIC_SUFFIXES = {".json", ".csv", ".png", ".svg", ".xml", ".whl"}
DENIED_PARTS = {".git", ".nox", ".venv", "source", "checkout", "context", "private"}


@dataclass(frozen=True)
class Policy:
    """Reviewed inventory and exact fingerprints; not a semantic manuscript detector."""

    public_paths: frozenset[str]
    private_hashes: dict[str, str]
    baseline: str
    gitlinks: dict[str, str]


def git(root: Path, *args: str) -> bytes:
    """Run bounded fixed Git argv without a shell; never print blob contents."""
    return subprocess.check_output(  # noqa: S603 -- Fixed Git binary/argv, no shell.
        [
            shutil.which("git") or "/usr/bin/git",
            "-c",
            "core.fsmonitor=false",
            "-c",
            "core.untrackedCache=false",
            "-C",
            str(root),
            *args,
        ],
        timeout=60,
    )


def safe_name(name: str) -> None:
    """Reject noncanonical paths before reading archive or repository entries."""
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name or str(path) != name:
        msg = "Unsafe publication path"
        raise ValueError(msg)


def load_policy(root: Path = ROOT, revision: str | None = None) -> Policy:
    """Read the reviewed local policy, rejecting duplicate inventory entries."""
    raw = json.loads(
        (root / POLICY).read_bytes() if revision is None else git(root, "show", f"{revision}:{POLICY}")
    )
    paths = cast("list[str]", raw["public_paths"])
    private = cast("dict[str, str]", raw["local_documents"])
    if len(paths) != len(set(paths)) or set(paths) & set(private):
        msg = "Duplicate or conflicting publication classification"
        raise ValueError(msg)
    for name in [*paths, *private]:
        safe_name(name)
    return Policy(frozenset(paths), private, str(raw["legacy_baseline"]), raw.get("gitlinks", {}))


def inspect_bytes(data: bytes, policy: Policy, *, depth: int = 0) -> None:
    """Reject known document copies and inspect bounded nested archives without extraction."""
    if len(data) > MAX_FILE_BYTES or depth > MAX_DEPTH:
        msg = "Publication content exceeds inspection budget"
        raise ValueError(msg)
    if hashlib.sha256(data).hexdigest() in policy.private_hashes.values():
        msg = "Known local document bytes in publication content"
        raise ValueError(msg)
    stream = io.BytesIO(data)
    if zipfile.is_zipfile(stream):
        inspect_zip(stream, policy, depth)
    elif data.startswith(b"\x1f\x8b") or data[257:262] == b"ustar":
        stream.seek(0)
        inspect_tar(stream, policy, depth)


def inspect_zip(stream: io.BytesIO, policy: Policy, depth: int) -> None:
    """Inspect safe ZIP member bytes within declared expansion limits."""
    with zipfile.ZipFile(stream) as archive:
        if sum(m.file_size for m in archive.infolist()) > MAX_ARCHIVE_BYTES:
            msg = "Archive expansion budget exceeded"
            raise ValueError(msg)
        for member in archive.infolist():
            if member.is_dir():
                continue
            safe_name(member.filename)
            if local_document_name(member.filename, policy) or member.file_size > MAX_FILE_BYTES:
                msg = "Disallowed archive member"
                raise ValueError(msg)
            if stat.S_ISLNK(member.external_attr >> 16):
                msg = "Archive symlink rejected"
                raise ValueError(msg)
            inspect_bytes(archive.read(member), policy, depth=depth + 1)


def inspect_tar(stream: io.BytesIO, policy: Policy, depth: int) -> None:
    """Inspect regular tar members without extracting paths onto disk."""
    if stream.getvalue().startswith(b"\x1f\x8b"):
        with gzip.GzipFile(fileobj=stream) as compressed:
            raw = compressed.read(MAX_ARCHIVE_BYTES + 1)
        if len(raw) > MAX_ARCHIVE_BYTES:
            msg = "Archive expansion budget exceeded"
            raise ValueError(msg)
        stream = io.BytesIO(raw)
    with tarfile.open(fileobj=stream, mode="r:") as archive:
        total = 0
        for member in archive:
            safe_name(member.name)
            if member.isdir():
                continue
            total += member.size
            if (
                not member.isfile()
                or local_document_name(member.name, policy)
                or member.size > MAX_FILE_BYTES
                or total > MAX_ARCHIVE_BYTES
            ):
                msg = "Disallowed archive member or expansion budget"
                raise ValueError(msg)
            content = archive.extractfile(member)
            if content is None:
                msg = "Unreadable archive member"
                raise ValueError(msg)
            inspect_bytes(content.read(MAX_FILE_BYTES + 1), policy, depth=depth + 1)


def local_document_name(name: str, policy: Policy) -> bool:
    """Recognize document paths even beneath an archive's versioned package prefix."""
    return any(name == path or name.endswith("/" + path) for path in policy.private_hashes)


def validate_tree(root: Path, revision: str | None = None) -> int:
    """Inspect index or committed object bytes, including staged/worktree divergence."""
    policy = load_policy(root, revision)
    if revision is None and git(root, "show", ":" + POLICY) != (root / POLICY).read_bytes():
        msg = "Staged publication policy differs from working policy"
        raise ValueError(msg)
    protected = load_policy(root)
    if not protected.private_hashes.items() <= policy.private_hashes.items():
        msg = "Outgoing policy lost a local document binding"
        raise ValueError(msg)
    raw = (
        git(root, "ls-files", "--stage", "-z")
        if revision is None
        else git(root, "ls-tree", "-r", "-z", revision)
    )
    names: set[str] = set()
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        header, encoded = entry.split(b"\t", 1)
        mode, middle, last = header.decode().split()
        name = encoded.decode("utf-8")
        safe_name(name)
        oid = middle if revision is None else last
        allowed_link = mode == "160000" and policy.gitlinks.get(name) == oid
        if (
            name not in policy.public_paths
            or name in names
            or (mode not in {"100644", "100755"} and not allowed_link)
        ):
            msg = "Unreviewed path, duplicate entry or mode in publication tree"
            raise ValueError(msg)
        if revision is None and last != "0":
            msg = "Unmerged index rejected"
            raise ValueError(msg)
        if allowed_link:
            names.add(name)
            continue
        size = int(git(root, "cat-file", "-s", oid))
        if size > MAX_FILE_BYTES:
            msg = "Git blob exceeds inspection budget"
            raise ValueError(msg)
        inspect_bytes(git(root, "cat-file", "blob", oid), policy)
        names.add(name)
    if names != set(policy.public_paths):
        msg = "Public tree and reviewed inventory differ"
        raise ValueError(msg)
    return len(names)


def validate_outgoing(root: Path, tips: list[str]) -> None:
    """Check every newly authored commit, allowing only the declared legacy baseline."""
    policy = load_policy(root)
    for tip in tips:
        # This also refuses unrelated history and unavailable/truncated baselines.
        git(root, "merge-base", "--is-ancestor", policy.baseline, tip)
        for revision in git(root, "rev-list", tip, "^" + policy.baseline).decode().splitlines():
            validate_tree(root, revision)
        validate_tree(root, tip)


def read_export_file(source: Path, path: Path) -> bytes:
    """Recheck containment and bound reads, including files growing during inspection."""
    cursor = path
    while cursor != source:
        if cursor.is_symlink():
            msg = "Symlink in export source"
            raise ValueError(msg)
        cursor = cursor.parent
    if not path.resolve().is_relative_to(source.resolve()):
        msg = "Export path escaped source"
        raise ValueError(msg)
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        msg = "Export file exceeds inspection budget"
        raise ValueError(msg)
    return data


def stage_exports(root: Path, source: Path, destination: Path) -> int:
    """Export only inspected numerical/qualification files; never upload a replay checkout."""
    policy = load_policy(root)
    if source.is_symlink() or not source.is_dir() or destination.exists():
        msg = "Export requires a real source directory and new destination"
        raise ValueError(msg)
    if destination.resolve().is_relative_to(source.resolve()):
        msg = "Export destination must be outside source"
        raise ValueError(msg)
    selected: list[tuple[Path, str]] = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if path.is_symlink():
            msg = "Symlink in export source"
            raise ValueError(msg)
        if not path.is_file() or any(
            p in DENIED_PARTS or p.startswith(".venv") or "context" in p.lower() for p in relative.parts
        ):
            continue
        if path.suffix not in PUBLIC_SUFFIXES and not path.name.endswith(".tar.gz"):
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            msg = "Export file exceeds inspection budget"
            raise ValueError(msg)
        inspect_bytes(read_export_file(source, path), policy)
        selected.append((path, relative.as_posix()))
    destination.mkdir(parents=True)
    try:
        for path, name in selected:
            data = read_export_file(source, path)
            inspect_bytes(data, policy)
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    except Exception:
        shutil.rmtree(destination)
        raise
    return len(selected)


def scan_export(root: Path, destination: Path) -> None:
    """Scan generated export bytes too, never emitting scanner matches in CI logs."""
    try:
        result = subprocess.run(  # noqa: S603 -- Checksum-pinned binary and explicit argv, no shell.
            [
                str(root / ".security-tools/gitleaks"),
                "dir",
                str(destination),
                "--redact",
                "--no-banner",
                "--ignore-gitleaks-allow",
                "--max-archive-depth",
                "3",
                "--config",
                str(root / "engineering/gitleaks.toml"),
                "--gitleaks-ignore-path",
                "/dev/null",
            ],
            capture_output=True,
            check=False,
            timeout=1800,
        )
    except Exception:
        shutil.rmtree(destination)
        raise
    if result.returncode:
        shutil.rmtree(destination)
        msg = "Export secret scanner failed; inspect locally with redacted output"
        raise ValueError(msg)


def main() -> None:
    """Expose fail-closed Git and export entry points without printing inspected bytes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["index", "outgoing", "export"])
    parser.add_argument("--tip", action="append", default=[])
    parser.add_argument("--source", type=Path)
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    if args.mode == "index":
        validate_tree(ROOT)
    elif args.mode == "outgoing":
        validate_outgoing(ROOT, args.tip or ["HEAD"])
    elif args.source is None or args.destination is None:
        parser.error("Export requires source and destination")
    else:
        stage_exports(ROOT, args.source, args.destination)
        scan_export(ROOT, args.destination)


if __name__ == "__main__":
    main()
