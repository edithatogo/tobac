"""Exercise the optional installed Voiage contract with a synthetic Arrow table."""

lazy from pathlib import Path

import pytest

from tobac.normalized_bundle import read_normalized_bundle


@pytest.mark.parametrize("suffix", [".arrow", ".parquet"])
def test_normalized_bundle_round_trip(tmp_path: Path, suffix: str) -> None:
    contract = pytest.importorskip("voiage.contracts.normalized_input", exc_type=ModuleNotFoundError)
    pa = pytest.importorskip("pyarrow")
    column = pa.chunked_array([[1, 2], [3, None]], type=pa.timestamp("s"))
    table = pa.table({"sample": column})
    manifest = contract.DatasetManifest(
        dataset_id="tobac-test",
        tables=(
            contract.TableManifest(
                table_id="samples", fields=(contract.FieldManifest(field_id="sample", dtype="timestamp[s]"),)
            ),
        ),
        provenance=contract.SourceProvenance(
            provider_id="test", source_uri="fixture://samples", descriptor_digest="a" * 64
        ),
    )
    bundle = contract.NormalizedInputBundle(manifest=manifest, tables={"samples": table})
    path = tmp_path / ("samples" + suffix)
    if suffix == ".arrow":
        bundle.write_ipc(path)
    else:
        bundle.write_parquet(path)
    restored = read_normalized_bundle(path, expected_digest=bundle.content_digest)
    assert restored.content_digest == bundle.content_digest
    assert restored.tables["samples"].equals(table)
    assert restored.tables["samples"]["sample"].num_chunks == 2
    with pytest.raises(ValueError, match="digest"):
        read_normalized_bundle(path, expected_digest="0" * 64)
