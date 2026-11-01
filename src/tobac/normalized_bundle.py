"""Read Voiage normalized input bundles without changing their Arrow schema."""

from importlib import import_module
from typing import Protocol, cast
lazy from collections.abc import Mapping
lazy from pathlib import Path


class NormalizedBundle(Protocol):
    """Readable surface of the upstream bundle returned by the consumer."""

    @property
    def content_digest(self) -> str:
        """Digest of the manifest and its tables."""
        ...

    @property
    def tables(self) -> Mapping[str, object]:
        """Arrow tables indexed by manifest table identifier."""
        ...


def read_normalized_bundle(path: Path, *, expected_digest: str) -> NormalizedBundle:
    """Open a single-table Parquet or Arrow IPC bundle and verify its content digest."""
    reader = import_module("voiage.contracts.normalized_input").NormalizedInputBundle
    if path.suffix.lower() == ".parquet":
        bundle = reader.read_parquet(path)
    elif path.suffix.lower() in {".arrow", ".ipc"}:
        bundle = reader.read_ipc(path)
    else:
        msg = "Expected a .parquet, .arrow or .ipc normalized bundle"
        raise ValueError(msg)
    if bundle.content_digest != expected_digest:
        msg = "Normalized bundle content digest differs from the expected digest"
        raise ValueError(msg)
    return cast("NormalizedBundle", bundle)
