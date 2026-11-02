"""Run scientific entry points, verify their source comparisons and query their native receipts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import io
import json
import os
import re
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, cast
lazy from collections.abc import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_moh_lineage as moh
import qualify_shine_table as shine
import runner_provenance as runners
from scientific_receipts import persist_execution, verify_execution
from source_handoff import checked, read
lazy from extract_moh_lineage import NativeStore

PHYO_YEARS = range(2012, 2024)
TABLE_WIDTH = 5
ROOT = runners.ROOT
ARCHIVE = ROOT / "integration/archive"
RETAIL = "configs/m2_retail.json"
SUPPLY = "data/empirical_intake_20261024/nz_historical_legal_supply.csv"
TONNES = "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv"
PHYO = "tobac-297be26fc11cb7b3"
MOH = "tobac-7ee48855a1ed1c4b"
SHINE = "tobac-a892a52bb0ce2147"
# Each contract selects a normal entry point, its effective config and the source-bearing input.
RUNS = {
    "m1": ("src/tobac/run.py", "configs/regulatory.json", (), None),
    "m2_retail": ("src/tobac/m2.py", RETAIL, ("--grid-check",), SHINE),
    "m2": ("scripts/run_m2_publication.py", "configs/m2_publication.json", (), SHINE),
    "m2_publication": (
        "scripts/run_m2_publication.py",
        "configs/m2_publication.json",
        ("--grid-check",),
        SHINE,
    ),
    "m2_robustness": ("scripts/run_m2_robustness.py", "configs/m2_robustness.json", (), SHINE),
    "m3": ("src/tobac/research/runner.py", "configs/m3_research.json", (), SHINE),
    "longitudinal": (
        "scripts/run_empirical_longitudinal.py",
        "configs/empirical_longitudinal_v2.9.0/model.json",
        (),
        PHYO,
    ),
    "release_calibration": (
        "scripts/run_release_calibration.py",
        "configs/calibration_v2.8.0/model.json",
        (),
        MOH,
    ),
}
SOURCE_HASHES = {
    PHYO: "d215537ac34d501668da42cf5f1573c2443b81e184976b018d1840d3faea6a3e",
    MOH: "3a55a6469097ebc3fb27a6143db7749e5b885761ada76b197053dfe76f36e883",
    SHINE: shine.SOURCE_SHA256,
}


def compare_phyo(original: bytes, table: bytes) -> int:
    """Verify years, legal supply, consumption bounds, signed gaps and percentages."""
    parser = shine.TableParser()
    parser.feed(original.decode())
    rows = list(csv.DictReader(io.StringIO(table.decode())))
    if (
        parser.sections != 1
        or parser.tables != 1
        or len(parser.rows) != len(PHYO_YEARS)
        or len(rows) != len(PHYO_YEARS)
    ):
        msg = "Missing or incomplete Phyo Table 2"
        raise ValueError(msg)
    for year, (cells, row) in enumerate(zip(parser.rows, rows, strict=True), start=2012):
        values = [
            re.findall(r"-?\d+(?:\.\d+)?", s.replace(" ", "").replace("\N{MINUS SIGN}", "-")) for s in cells
        ]
        if len(values) != TABLE_WIDTH or [len(x) for x in values] != [1, 3, 1, 3, 3]:
            msg = "Unexpected Table 2 columns or interval"
            raise ValueError(msg)
        observed = [values[0][0], values[2][0], values[1][0], values[1][1], values[3][0], values[4][0]]
        keys = (
            "year",
            "legal_sales_cigarette_equivalent",
            "reported_upper_smoker_bound_consumption",
            "reported_lower_smoker_bound_consumption",
            "reported_signed_gap",
            "reported_upper_scenario_gap_percent",
        )
        if (
            int(row["year"]) != year
            or row["source_id"] != "parallel-S08"
            or row["source_locator"] != "Table 2"
            or any(Decimal(v) != Decimal(row[k]) for k, v in zip(keys, observed, strict=True))
        ):
            msg = f"Phyo Table 2 differs in {year}"
            raise ValueError(msg)
    return len(rows)


def affected_results(runs: dict[str, dict[str, Any]], changed: str) -> dict[str, list[str]]:
    """Conservative rerun set. Equal output bytes do not merge separate executions."""
    return {
        name: sorted(run["outputs"])
        for name, run in runs.items()
        if changed in run["inputs"]
        or changed in run["originals"]
        or changed in run["originals"].values()
        or changed in run["inputs"].values()
        or changed in run.get("underlying_groups", [])
    }


def verify_original(source: str, original: bytes) -> dict[str, Any]:
    """Re-extract the exact original for the signed-off scientific role."""
    if hashlib.sha256(original).hexdigest() != SOURCE_HASHES[source]:
        msg = "Wrong original for the selected scientific comparison"
        raise ValueError(msg)
    if source == PHYO:
        return {
            "input": SUPPLY,
            "verified_years": compare_phyo(original, checked(ROOT, SUPPLY).read_bytes()),
            "role": "published national Table 2; shared NZHS and MOH returns with fixed uplift",
        }
    if source == SHINE:
        extracted = shine.extract_table(original)
        shine.consumer_comparison(shine.consumer_snapshots(ROOT), extracted)
        return {
            "input": RETAIL,
            "source_beta": extracted["source_beta"],
            "role": "transported model parameter; historical edition equivalence unknown",
        }
    rows = moh.extract_and_compare(original, checked(ROOT, TONNES).read_bytes(), "Sheet1")
    return {
        "input": TONNES,
        "verified_years": len(rows),
        "role": "reported tonnes; independent value comparison with the retained transcription",
    }


def manifest_io(folder: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Normalize both maintained runner manifest shapes and check the whole output inventory."""
    path = folder / "manifest.json"
    if path.exists():
        manifest = read(path)
        inputs, outputs = manifest["inputs"], dict(manifest["outputs"])
    else:
        path = folder / "run_manifest.json"
        manifest = read(path)
        inputs = {r["path"]: r["sha256"] for r in manifest["sources"]}
        outputs = {r["path"]: r["sha256"] for r in manifest["files"]}
    outputs[path.name] = runners.digest(path)
    actual = {p.relative_to(folder).as_posix(): runners.digest(p) for p in folder.rglob("*") if p.is_file()}
    if actual != outputs:
        msg = "Output inventory differs from the completed runner manifest"
        raise ValueError(msg)
    return inputs, outputs


def registration(
    source: str | None, native_store: Path, wheel: Path, store: NativeStore
) -> tuple[dict[str, Any], dict[str, str], dict[str, Any]]:
    """Verify the exact scientific original and its native registration before execution."""
    export_path = ARCHIVE / "native-source-refs.json"
    export = json.loads(
        runners.verified_bytes(
            export_path, "f75582e8362b39d08bc69ef7196131667bb756e39df285189ca478c2a5bd9ed3"
        )
    )
    registered = {}
    originals: dict[str, str] = {}
    comparison = {}
    if source:
        row = next(r for r in export["native_source_refs"] if r["archive_id"] == source)
        refs = [
            c["native_registration"]
            for c in row["captures"]
            if c.get("sha256") == SOURCE_HASHES[source] and c["native_registration"]
        ]
        if len(refs) != 1:
            msg = "A unique native registration for the exact source edition is required"
            raise ValueError(msg)
        registered = {source: refs}
        runners.readback_sources(registered, native_store, wheel, "transformation-interface.json")
        originals[source] = refs[0]["object_id"]
        comparison = verify_original(source, store.verify(refs[0]["object_id"]).path.read_bytes())
    return registered, originals, comparison


def collect_inputs(
    folder: Path, expected: dict[str, str], store: NativeStore, code: dict[str, str]
) -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    """Reconcile actual reads, the runner manifest, and the independently pinned inputs."""
    declared, outputs = manifest_io(folder / "outputs")
    observed = read(folder / "reads.json")
    inputs: dict[str, str] = {}
    for path in sorted(observed.keys() | declared.keys()):
        raw = checked(ROOT, path).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if expected.get(path, code.get(path)) != sha or any(
            m[path] != sha for m in (declared, observed) if path in m
        ):
            msg = f"Unpinned or changed scientific input: {path}"
            raise ValueError(msg)
        inputs[path] = store.put_bytes(raw).object_id
    if not set(expected) <= inputs.keys():
        msg = "Executed input inventory differs from reviewed inventory"
        raise ValueError(msg)
    return inputs, outputs, observed, declared


def run_one(name: str, dest: Path, native_store: Path, wheel: Path) -> None:
    """Reserve an attempt, compare its original, execute, and bind all output bytes."""
    from lineage_preflight import verify  # noqa: PLC0415 -- Execution gate; read-only historical queries stay independent.

    attempts = os.environ.get("TOBAC_LINEAGE_ATTEMPTS")
    if not attempts:
        msg = "Missing TOBAC_LINEAGE_ATTEMPTS for qualified scientific execution"
        raise ValueError(msg)
    verify(Path(attempts), wheel, [name])
    native, factory, pin = moh.producer(wheel, ARCHIVE / "transformation-interface.json")
    api = importlib.import_module("archive_govt_nz.transformation_attempt")
    script, config, args, source = RUNS[name]
    source_store = cast("Callable[..., NativeStore]", factory)(native_store, create=False)
    contract = read(ARCHIVE / "scientific-runner-inputs.json")
    expected = {p: contract["sha256"][p] for p in contract["runners"][name]}
    for path, value in expected.items():
        if runners.digest(checked(ROOT, path)) != value:
            msg = f"Input differs from reviewed repository bytes: {path}"
            raise ValueError(msg)
    registered, originals, comparison = registration(source, native_store, wheel, source_store)
    material = runners.execution_material(name, ROOT / config, ROOT / script, registered, list(args))
    expected_env = read(ARCHIVE / "runner-material.json")["environment"]
    if material["environment"] != expected_env:
        msg = "Scientific runner environment differs from the reviewed environment"
        raise ValueError(msg)
    attempt = api.TransformationAttempt(dest, {**material, "producer_revision": pin["producer_revision"]})
    started = moh.now()
    try:
        result = runners.execute_runner_with_provenance(
            name,
            ROOT / config,
            dest / "outputs",
            ROOT / script,
            list(args),
            observed_inputs=dest / "reads.json",
        )
        require_success(result)
        inputs, outputs, observed, declared = collect_inputs(dest, expected, attempt.store, contract["code"])
        native_outputs = {
            p: attempt.store.put_bytes(checked(dest / "outputs", p).read_bytes()).object_id for p in outputs
        }
        record = {
            "runner": name,
            "model_revision": contract["revision"],
            "started": started,
            "attempt_id": attempt.attempt_id,
            "material": material,
            "inputs": inputs,
            "originals": originals,
            "source_comparison": comparison,
            "outputs": native_outputs,
            "observed_reads": sorted(observed),
            "manifest_inputs": sorted(declared),
            "scientific_qualification": False,
        }
        if source:
            verify_link(
                source,
                source_store.verify(originals[source]).path.read_bytes(),
                attempt.store.verify(inputs[comparison["input"]]).path.read_bytes(),
            )
            for ref in registered[source]:
                for k in ("object_id", "manifest_object_id", "registration_object_id"):
                    attempt.store.put_bytes(source_store.verify(ref[k]).path.read_bytes())
        pointers = persist_execution(record, native, attempt.store)
    except BaseException:
        attempt.finish("interrupted" if sys.exc_info()[0] is KeyboardInterrupt else "failed", {})
        raise
    attempt.finish("succeeded", pointers)


def require_success(result: dict[str, Any]) -> None:
    """Keep a failed child from acquiring successful native records."""
    if result["status"] != "completed":
        raise RuntimeError(result["error"])


def verify_link(source: str, raw: bytes, data: bytes) -> None:
    """Repeat the scientific comparison using exclusively the bytes in the attempt."""
    if source == PHYO:
        compare_phyo(raw, data)
    elif source == MOH:
        moh.extract_and_compare(raw, data, "Sheet1")
    elif [float(v) for v in shine.extract_table(raw)["source_beta"]] != json.loads(data)["source_beta"]:
        msg = "SHINE source parameters differ from the executed retail configuration"
        raise ValueError(msg)


def underlying_groups(source: str, data: bytes) -> list[str]:
    """Resolve published dependency labels without adding a likelihood or conflating editions."""
    if source not in {MOH, PHYO}:
        return []
    pin = read(ARCHIVE / "scientific-runner-inputs.json")["shared_evidence_contract"]
    contract = json.loads(runners.verified_bytes(checked(ROOT, pin["path"]), pin["sha256"]))
    column = "dependency_group" if source == MOH else "source_dependency"
    labels = {row[column] for row in csv.DictReader(io.StringIO(data.decode()))}
    return sorted({group for label in labels for group in contract["dependency_mappings"][label]})


def verify_contract(record: dict[str, Any], name: str) -> None:
    """Reject a swapped runner or substituted input even if a different attempt is internally consistent."""
    contract = read(ARCHIVE / "scientific-runner-inputs.json")
    if name != record["runner"] or record["model_revision"] != contract["revision"]:
        msg = "Unexpected runner or scientific model revision"
        raise ValueError(msg)
    reviewed = contract["runners"][name]
    inputs = record["inputs"]
    if not set(reviewed) <= inputs.keys():
        msg = "Completed attempt omits reviewed inputs"
        raise ValueError(msg)
    for path, key in inputs.items():
        expected = contract["sha256"].get(path) if path in reviewed else contract["code"].get(path)
        if expected is None or key != "sha256:" + expected:
            msg = f"Completed attempt references unreviewed input: {path}"
            raise ValueError(msg)
    source = RUNS[name][3]
    expected_originals = {source: "sha256:" + SOURCE_HASHES[source]} if source else {}
    if record["originals"] != expected_originals:
        msg = "Completed attempt has different scientific originals"
        raise ValueError(msg)


def load_run(
    folder: Path, factory: Callable[..., NativeStore], *, runner: str | None = None
) -> dict[str, Any]:
    """Independently reopen the attempt and every declared input, source and output."""
    terminal = read(folder / "terminal")
    store = factory(folder / "cas", create=False)
    record = read(store.verify(terminal["result"]["receipt"]).path)
    if (
        terminal["state"] != "succeeded"
        or record["attempt_id"] != terminal["attempt_id"]
        or read(folder / "started")["attempt_id"] != terminal["attempt_id"]
    ):
        msg = "Scientific receipt does not belong to a completed attempt"
        raise ValueError(msg)
    verify_contract(record, runner or folder.name)
    verify_execution(record, terminal, store)
    if set(manifest_io(folder / "outputs")[1]) != set(record["outputs"]):
        msg = "Files no longer match the native inventory"
        raise ValueError(msg)
    for field in ("inputs", "originals", "outputs"):
        for key in set(record[field].values()):
            store.verify(key)
    source = RUNS[record["runner"]][3]
    if source:
        raw = store.verify(record["originals"][source]).path.read_bytes()
        observed_input = record["source_comparison"]["input"]
        data = store.verify(record["inputs"][observed_input]).path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != SOURCE_HASHES[source]:
            msg = "Unexpected original version in the completed attempt"
            raise ValueError(msg)
        verify_link(source, raw, data)
        record["underlying_groups"] = underlying_groups(source, data)
    for path, key in record["outputs"].items():
        if runners.digest(checked(folder / "outputs", path)) != key.removeprefix("sha256:"):
            msg = "Material output differs from its native object"
            raise ValueError(msg)
    return record


def main() -> None:
    """Run one profile, or query completed attempts by source or local input."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--store", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", choices=tuple(RUNS))
    group.add_argument("--changed")
    group.add_argument("--trace", nargs=2, metavar=("RUNNER", "OUTPUT"))
    args = parser.parse_args()
    if args.run:
        if not args.store:
            parser.error("--run requires --store")
        run_one(args.run, args.out.resolve() / args.run, args.store, args.wheel)
    else:
        _, factory, _ = moh.producer(args.wheel, ARCHIVE / "transformation-interface.json")
        if args.trace:
            name, path = args.trace
            if name not in RUNS:
                parser.error("Unknown runner")
            run = load_run(args.out / name, factory)
            answer = {
                "runner": name,
                "artifact": path,
                "object": run["outputs"][path],
                "attempt_id": run["attempt_id"],
                "inputs": run["inputs"],
                "originals": run["originals"],
                "underlying_groups": run.get("underlying_groups", []),
                "source_comparison": run["source_comparison"],
            }
        else:
            runs = {name: load_run(args.out / name, factory) for name in RUNS}
            answer = affected_results(runs, args.changed)
        sys.stdout.write(json.dumps(answer, indent=2) + "\n")


if __name__ == "__main__":
    main()
