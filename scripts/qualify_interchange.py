"""Measure the bounded native evidence transport; never calibrate observations."""
from __future__ import annotations

import argparse
import gc
import hashlib
import importlib
import json
import platform
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from typing import Any, cast

import numpy as np

from tobac._core import DecisionProblem, exact_evpi
from tobac.evidence import Belief, EvidencePacket, Scope, condition
from tobac.interchange import from_arrow, from_polars, read_metadata, to_arrow, to_polars, write_ipc
from tobac.research.voiage_adapter import installed_evpi
from tobac.supply import release_loglikelihood
from tobac_supply.consumption_ledger import SupplyBasis

pa = importlib.import_module("pyarrow")
ROOT = Path(__file__).resolve().parents[1]


def qualify(destination: Path) -> None:
    """Retain actual identities, logical/physical hashes and buffer measurements."""
    if sys.version_info[:3] != (3, 15, 1):
        msg = "Select the qualified repo-local Python 3.15.1"
        raise RuntimeError(msg)
    destination.mkdir(parents=True, exist_ok=False)
    basis = SupplyBasis(source_ids=("synthetic:source",), observation_years=(2024,))
    scope = Scope(basis.geography, "synthetic adults", "2024-01-01", "2024-12-31", basis.unit)
    covariance = np.array([[2., .5], [.5, 1.]])
    packet = EvidencePacket(
        "synthetic:joint", ("synthetic:data",), basis.source_ids, ("state:a", "state:b"),
        release_loglikelihood([3., 4.], [[2., 4.], [4., 5.]], covariance), scope, scope,
        "synthetic Gaussian with supplied off-diagonal covariance",
    )
    table = cast("Any", to_arrow(packet, captured_at=datetime(2026, 10, 26, tzinfo=UTC), supply_basis=basis,
                     covariance=covariance, observation_ids=("o1", "o2"),
                     covariance_unit="cigarette_equivalents^2", producer_revision="synthetic-fixture-v1"))
    chunks = pa.concat_tables([table.slice(0, 1), table.slice(1, 1)])
    logical_digest = read_metadata(table)["digest"]
    if logical_digest != read_metadata(chunks)["digest"]:
        msg = "Chunking changed logical content"
        raise AssertionError(msg)
    allocated_before = pa.total_allocated_bytes()
    stream = pa.RecordBatchReader.from_stream(table).read_all()
    view = to_polars(stream)
    allocated_after = pa.total_allocated_bytes()
    source_buffer = table.column(1).chunk(0).buffers()[1].address
    view_buffer = cast("Any", view.frame).to_arrow().column(1).chunk(0).buffers()[1].address
    if source_buffer != view_buffer:
        msg = "Float64 buffer was copied"
        raise AssertionError(msg)
    for name, value in (("contiguous.arrow", table), ("chunked.arrow", chunks)):
        write_ipc(destination / name, value)
    prior = Belief(DecisionProblem(np.array([[0., 4.], [3., 0.]]),
                           ("a", "b"), "score", np.array([.75, .25])), packet.state_ids, scope)
    original = condition(prior, packet)
    restored = from_arrow(table)
    np.testing.assert_array_equal(restored.log_likelihood, packet.log_likelihood)
    del table, chunks, stream
    gc.collect()
    recovered = from_polars(view)
    np.testing.assert_array_equal(recovered.log_likelihood, packet.log_likelihood)
    restored_belief = condition(prior, recovered)
    np.testing.assert_array_equal(original.problem.prior_weights, restored_belief.problem.prior_weights)
    actual = installed_evpi(restored_belief.problem)
    np.testing.assert_allclose(actual["value"], exact_evpi(original.problem), rtol=1e-12, atol=1e-12)
    receipt = {
        "schema": "tobac.interchange-qualification.v1", "status": "passed",
        "python": sys.version, "platform": platform.platform(),
        "versions": {name: version(name) for name in ("pyarrow", "polars", "patito", "msgspec", "voiage")},
        "source_sha256": hashlib.sha256((ROOT / "src/tobac/interchange.py").read_bytes()).hexdigest(),
        "scope": asdict(scope), "logical_sha256_v1": logical_digest,
        "ipc_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in destination.glob("*.arrow")},
        "float64_view": {"source_address": source_buffer, "view_address": view_buffer,
                         "arrow_pool_before": allocated_before, "arrow_pool_after": allocated_after,
                         "survives_source_gc": True, "length": 2, "offset": 0},
        "producer": actual,
        "limits": "Synthetic fixture only. Export/reconstruction copy. "
                  "No string, whole-table or process-wide "
                  "zero-allocation claim; Arrow pool counters exclude other allocators. "
                  "Digests are not signatures. "
                  "No empirical or Voiage 3 qualification.",
    }
    (destination / "receipt.json").write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")


def main() -> None:
    """Execute the explicitly selected qualification."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    qualify(parser.parse_args().out)


if __name__ == "__main__":
    main()
