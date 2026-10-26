"""Restore losslessly packed M3 outputs; standard library, bounded and fail-closed."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import lzma
import tarfile
from pathlib import Path, PurePosixPath

MAX_BYTES = 5_000_000


# Named bounds preserve the existing scientific/data contract.
MIN_OBSERVATIONS = 2


def safe_members(raw: bytes) -> dict[str, bytes]:
    """Verify packed artifact names and hashes before extracting any member."""
    if len(raw) > MAX_BYTES:
        msg = "Unpacked archive exceeds the bounded result contract"
        raise ValueError(msg)
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        for member in archive:
            path = PurePosixPath(member.name)
            if (
                not member.isfile()
                or path.is_absolute()
                or len(path.parts) != MIN_OBSERVATIONS
                or path.parts[0] not in {"full", "refined"}
                or ".." in path.parts
                or path.suffix not in {".csv", ".json"}
                or member.name in files
                or member.size < 0
                or member.size > MAX_BYTES
            ):
                msg = "Unsafe or duplicate archive member"
                raise ValueError(msg)
            source = archive.extractfile(member)
            if source is None:
                msg = "Missing member bytes"
                raise ValueError(msg)
            files[member.name] = source.read(MAX_BYTES + 1)
            if len(files[member.name]) != member.size:
                msg = "Truncated member"
                raise ValueError(msg)
    if sum(map(len, files.values())) > MAX_BYTES:
        msg = "Expanded output exceeds limit"
        raise ValueError(msg)
    return files


def unpack(source: Path, destination: Path) -> int:
    """Extract verified M3 artifacts into a new destination without overwriting files."""
    source, destination = Path(source), Path(destination)
    if destination.exists():
        msg = "Use a new output directory"
        raise FileExistsError(msg)
    manifest = json.loads((source / "manifest.json").read_text())
    if manifest["schema"] != "tobac.m3.saved-runs.v1":
        msg = "Unknown archive schema"
        raise ValueError(msg)
    pieces: list[bytes] = []
    for part in manifest["parts"]:
        name = part["name"]
        if name not in {"part-001", "part-002", "part-003"}:
            msg = "Invalid part path"
            raise ValueError(msg)
        data = (source / name).read_bytes()
        if len(data) != part["size"] or hashlib.sha256(data).hexdigest() != part["sha256"]:
            msg = "Archive part mismatch"
            raise ValueError(msg)
        pieces.append(data)
    packed = b"".join(pieces)
    if (
        len(packed) > MAX_BYTES
        or len(packed) != manifest["archive_bytes"]
        or hashlib.sha256(packed).hexdigest() != manifest["archive_sha256"]
    ):
        msg = "Complete archive mismatch"
        raise ValueError(msg)
    decoder = lzma.LZMADecompressor(memlimit=128 * 1024 * 1024)
    raw = decoder.decompress(packed, max_length=MAX_BYTES + 1)
    if not decoder.eof or decoder.unused_data:
        msg = "Oversized or trailing archive stream"
        raise ValueError(msg)
    files = safe_members(raw)
    if len(files) != manifest["file_count"]:
        msg = "Archive file-count mismatch"
        raise ValueError(msg)
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    return len(files)


def main() -> None:
    """Parse command-line options, execute the selected operation and report its result."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--archive", default="results/milestone3/archive")
    args = parser.parse_args()
    print(  # noqa: T201  # CLI emits the requested structured result on stdout.
        json.dumps(
            {
                "restored_files": unpack(Path(args.archive), Path(args.out)),
                "scope": "saved conditional outputs, not new observed evidence",
            }
        )
    )


if __name__ == "__main__":
    main()
