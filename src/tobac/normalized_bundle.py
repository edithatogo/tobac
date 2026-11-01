"""Read Voiage normalized input bundles without changing their Arrow schema."""

lazy from pathlib import Path

lazy from voiage.contracts.normalized_input import NormalizedInputBundle


def read_normalized_bundle(path: Path, *, expected_digest: str) -> NormalizedInputBundle:
    """Open a single-table Parquet or Arrow IPC bundle and verify its content digest."""
    if path.suffix.lower() == ".parquet":
        bundle = NormalizedInputBundle.read_parquet(path)
    elif path.suffix.lower() in {".arrow", ".ipc"}:
        bundle = NormalizedInputBundle.read_ipc(path)
    else:
        msg = "Expected a .parquet, .arrow or .ipc normalized bundle"
        raise ValueError(msg)
    if bundle.content_digest != expected_digest:
        msg = "Normalized bundle content digest differs from the expected digest"
        raise ValueError(msg)
    return bundle
