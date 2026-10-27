"""Execute bounded installed-library contracts; optional tools never qualify empirical data."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import platform
import resource
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from tobac._core import DecisionProblem, exact_evpi
from tobac.backend import evpi


def qualify(out: Path) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0915  # Keep the bounded native acceptance sequence visible.
    """Exercise weighted/tie/permutation cases and actual Arrow buffer lifetimes."""
    if sys.version_info[:3] != (3, 15, 1):
        msg = "Python 3.15.1 required"
        raise RuntimeError(msg)
    if out.exists():
        msg = "Preserve previous qualification receipts"
        raise FileExistsError(msg)
    jax = importlib.import_module("jax")
    jax.config.update("jax_enable_x64", True)  # noqa: FBT003  # Public JAX API.
    arrow = importlib.import_module("pyarrow")
    polars = importlib.import_module("polars")
    patito = importlib.import_module("patito")
    msgspec = importlib.import_module("msgspec")
    checks: list[dict[str, Any]] = []
    for weights in ([0.5, 0.5], [0.9, 0.1], [1.0, 0.0], [1e-8, 1 - 1e-8]):
        for offset in (0.0, 1e10):
            values = np.array([[0.0, 4.0], [3.0, 0.0]]) + offset
            p = DecisionProblem(values, ("a", "b"), "score", np.array(weights))
            expected = exact_evpi(p)
            actual = evpi(p, backend="jax")
            np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-12)
            permuted = DecisionProblem(values[::-1], ("a", "b"), "score", np.array(weights)[::-1])
            np.testing.assert_allclose(evpi(permuted, backend="jax"), expected, rtol=1e-12, atol=1e-12)
            checks.append(
                {
                    "weights": weights,
                    "offset": offset,
                    "reference": expected,
                    "jax": actual,
                }
            )
    table = arrow.table({"state_id": ["s1", "s2"], "value": [1.0, 2.0]})
    before = table.column("value").chunk(0).buffers()[1].address
    frame = polars.from_arrow(table, rechunk=False)
    retained = frame.to_arrow()
    after = retained.column("value").chunk(0).buffers()[1].address
    if before != after:
        msg = "Arrow/Polars float buffer was copied on this qualified path"
        raise AssertionError(msg)
    del table, frame
    if retained.column("value").to_pylist() != [1.0, 2.0]:
        msg = "Buffer lifetime or state ordering changed"
        raise AssertionError(msg)
    chunks = arrow.chunked_array([[1.0], [2.0]])
    chunked = arrow.table({"value": chunks})
    logical = polars.from_arrow(chunked, rechunk=False)["value"].to_list()
    if logical != [1.0, 2.0]:
        msg = "Chunked logical values changed"
        raise AssertionError(msg)

    class Boundary(patito.Model):
        state_id: str
        value: float

    Boundary.validate(polars.DataFrame({"state_id": ["s1"], "value": [1.0]}))
    rejected = False
    try:
        Boundary.validate(polars.DataFrame({"state_id": ["s1"], "value": ["1"]}))
    except ValueError, TypeError:
        rejected = True
    if not rejected:
        msg = "Patito boundary silently coerced strings"
        raise AssertionError(msg)
    codec = msgspec.json.Decoder(type=dict[str, float], strict=True)
    if codec.decode(b'{"value":1.0}') != {"value": 1.0}:
        msg = "Strict codec changed numbers"
        raise AssertionError(msg)
    for invalid in (b'{"value":"1"}', b'{"value":null}', b'{"value":NaN}'):
        try:
            codec.decode(invalid)
        except msgspec.DecodeError:
            continue
        msg = "Strict codec accepted an invalid numeric value"
        raise AssertionError(msg)
    timings: list[dict[str, Any]] = []
    for size in (4096, 262144):
        values = np.random.default_rng(0).normal(size=(size, 4))
        p = DecisionProblem(values, ("a", "b", "c", "d"), "score")
        start = time.perf_counter()
        array = jax.device_put(values)
        array.block_until_ready()
        transfer = time.perf_counter() - start
        # Public JAX lowering gives a separate compile measurement for the
        # expected-value matmul operand; it is not the whole Voiage endpoint.
        kernel = jax.jit(jax.numpy.matmul)
        weights_array = jax.device_put(p.prior_weights)
        start = time.perf_counter()
        compiled = kernel.lower(weights_array, array).compile()
        compile_seconds = time.perf_counter() - start
        start = time.perf_counter()
        expected_values = compiled(weights_array, array).block_until_ready()
        kernel_seconds = time.perf_counter() - start
        np.testing.assert_allclose(
            np.asarray(expected_values),
            np.asarray(p.prior_weights) @ values,
            rtol=1e-12,
            atol=1e-12,
        )
        start = time.perf_counter()
        value = evpi(p, backend="jax")
        cold = time.perf_counter() - start
        reference = exact_evpi(p)
        np.testing.assert_allclose(value, reference, rtol=1e-12, atol=1e-12)
        samples = {}
        for backend in ("numpy", "jax"):
            start = time.perf_counter()
            for _ in range(10):
                evpi(p, backend=backend)
            samples[backend] = (time.perf_counter() - start) / 10
        timings.append(
            {
                "states": size,
                "actions": 4,
                "host_to_device_seconds": transfer,
                "cold_producer_seconds": cold,
                "operand_compile_seconds": compile_seconds,
                "operand_warm_seconds": kernel_seconds,
                "warm_seconds": samples,
                "compile_boundary": (
                    "producer combines primitive compilation and execution; not separately measured"
                ),
            }
        )
    result = {
        "schema": "tobac.ecosystem-probe.v1",
        "status": "passed",
        "python": sys.version,
        "machine": platform.machine(),
        "platform": platform.platform(),
        "devices": [str(d) for d in jax.devices()],
        "jax_x64": jax.config.x64_enabled,
        "checks": checks,
        "versions": {
            n: importlib.metadata.version(n)
            for n in (
                "numpy",
                "scipy",
                "voiage",
                "jax",
                "jaxlib",
                "polars",
                "pyarrow",
                "patito",
                "msgspec",
            )
        },
        "arrow": {
            "float_buffer_shared": before == after,
            "lifetime_verified": True,
            "logical_chunk_content_sha256": hashlib.sha256(json.dumps(logical).encode()).hexdigest(),
            "scope": (
                "tested float64 column path only; string columns may copy; metadata contract not adopted"
            ),
        },
        "timings": timings,
        "peak_rss_process_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "performance_policy": (
            "retain NumPy default; no surrogate or optimisation without demonstrated benefit"
        ),
        "scientific_qualification": False,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    return result


def main() -> None:
    """Write a new native execution generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    qualify(args.out)
    sys.stdout.write("Native JAX/interchange qualification passed\n")


if __name__ == "__main__":
    main()
