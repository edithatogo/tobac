"""Inventory existing evidence, or record actual library execution with its limited scope.

An inventory pass is not CSL/provider validation, independent evidence or a model update.
The existing Sourceright and voiage interfaces remain the only external execution routes.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_prior_work import checked_file, read_json
from verify_prior_work import verify as verify_prior_work

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLLECTIONS = (
    "evidence/references.csl.json",
    "evidence/m2/references.csl.json",
    "evidence/longitudinal/references.csl.json",
    "evidence/prior_work/v2.9.0/references.csl.json",
)


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def bibliography_record(root: Path, name: str) -> dict:
    path = checked_file(root, name)
    data = path.read_bytes()
    records = read_json(data.decode("utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError(f"Nonempty bibliography list required: {name}")
    ids = [r.get("id") if isinstance(r, dict) else None for r in records]
    if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
        raise ValueError(f"Missing or duplicate project citation identity: {name}")
    return {
        "path": name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "records": len(records),
        "source_ids": ids,
        "role": (
            "preserved_reference_only"
            if name.startswith("evidence/prior_work/")
            else "active_bibliography_not_observations"
        ),
    }


def inventory(root: Path = ROOT) -> dict:
    """Reuse byte/role verification and inventory every evidence/*.csl.json collection.

    Literal IDs are namespaced by file. Repeated IDs are reported, not merged or
    counted as independent studies. This is not a replacement CSL schema validator.
    """
    root = Path(root).resolve()
    preserved = verify_prior_work(root)
    for name in REQUIRED_COLLECTIONS:
        checked_file(root, name)
    names = []
    for directory, folders, files in os.walk(root / "evidence", followlinks=False):
        for name in folders + files:
            if (Path(directory) / name).is_symlink():
                raise ValueError("Forbidden symlink in evidence inventory")
        names.extend(
            (Path(directory) / name).relative_to(root).as_posix()
            for name in files
            if name.endswith(".csl.json")
        )
    collections = [bibliography_record(root, name) for name in sorted(names)]
    locations = defaultdict(list)
    for collection in collections:
        for identity in collection["source_ids"]:
            locations[identity].append(collection["path"])
    return {
        "tool": "internal_evidence_inventory",
        "success": True,
        "preservation": preserved,
        "collections": collections,
        "collection_count": len(collections),
        "record_occurrences": sum(c["records"] for c in collections),
        "distinct_literal_ids": len(locations),
        "repeated_literal_ids": {k: v for k, v in sorted(locations.items()) if len(v) > 1},
        "external_tool_executed": False,
        "bibliographic_validation_performed": False,
        "scientific_applicability_validated": False,
        "live_model_conditioned": False,
        "new_raw_assays": 0,
        "supplier_quotes_received": 0,
        "scope": "preserved_bytes_and_bibliography_inventory_not_independent_observations",
    }


def qualify_sourceright(root: Path = ROOT, *, all_csl: bool = False) -> dict:
    """Run the genuine CLI for every selected collection, retaining all failure results."""
    root = Path(root).resolve()
    before = inventory(root) if all_csl else None
    selected = (
        before["collections"] if before else [bibliography_record(root, "evidence/references.csl.json")]
    )
    receipt = {
        "tool": "sourceright",
        "success": False,
        "results": [],
        "scope_selection": "all_evidence_collections" if all_csl else "single_legacy_collection",
        "external_tool_executed": False,
        "scientific_applicability_validated": False,
        "live_model_conditioned": False,
        "scope": "CSL CLI exit-status validation, not provider-backed claim or numerical verification",
    }
    if before is not None:
        receipt["inventory"] = before
    exe = shutil.which("sourceright")
    if not exe:
        receipt["error"] = "sourceright not installed"
        return receipt
    receipt["executable_sha256"] = digest(Path(exe))
    for collection in selected:
        command = [exe, "validate-csl", "--json", str(root / collection["path"])]
        result = dict(collection, command=command, success=False)
        try:
            run = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=120)
            receipt["external_tool_executed"] = True
            result.update(
                exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr, success=run.returncode == 0
            )
        except subprocess.TimeoutExpired:
            receipt["external_tool_executed"] = True
            result["error"] = "timeout"
        except OSError as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"
        receipt["results"].append(result)
    try:
        after = (
            inventory(root)["collections"]
            if all_csl
            else [bibliography_record(root, "evidence/references.csl.json")]
        )
        receipt["inputs_unchanged"] = after == selected
        receipt["executable_unchanged"] = digest(Path(exe)) == receipt["executable_sha256"]
    except (ValueError, OSError) as exc:
        receipt["inputs_unchanged"] = False
        receipt["postcheck_error"] = str(exc)
    receipt["success"] = (
        bool(receipt["results"])
        and all(r["success"] for r in receipt["results"])
        and receipt["inputs_unchanged"]
        and receipt.get("executable_unchanged", False)
    )
    return receipt


def qualify_voiage() -> dict:
    """Retain the existing 51-case equal-weight EVPI probe; M3 owns broader adapters."""
    import numpy as np
    from voiage.analysis import DecisionAnalysis
    from voiage.schema import ValueArray

    rng = np.random.default_rng(20261024)
    errors = []
    for i in range(51):
        values = np.array([[0.0, 2.0], [2.0, 0.0]]) if i == 0 else rng.normal(size=(37, 4))
        got = float(DecisionAnalysis(ValueArray.from_numpy(values)).evpi())
        expected = float(values.max(axis=1).mean() - values.mean(axis=0).max())
        if not np.isfinite(got) or not np.isfinite(expected):
            raise ValueError("Nonfinite voiage result cannot qualify parity")
        errors.append(abs(got - expected))
    return {
        "tool": "voiage",
        "version": importlib.metadata.version("voiage"),
        "cases": 51,
        "max_absolute_error": max(errors),
        "success": max(errors) < 1e-9,
        "external_tool_executed": True,
        "scope": "equal-weight EVPI only; not EVPPI/EVSI or empirical validation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["inventory", "voiage", "sourceright"], required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--all-csl", action="store_true")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.all_csl and args.mode != "sourceright":
        parser.error("--all-csl applies only to Sourceright")
    if args.out.exists() or args.out.is_symlink():
        parser.error("Refusing to overwrite a previous execution receipt")
    try:
        if args.mode == "inventory":
            receipt = inventory(args.root)
        elif args.mode == "sourceright":
            receipt = qualify_sourceright(args.root, all_csl=args.all_csl)
        else:
            receipt = qualify_voiage()
    except Exception as exc:
        receipt = {"tool": args.mode, "success": False, "error": repr(exc)}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    print(json.dumps(receipt, indent=2, allow_nan=False))
    raise SystemExit(0 if receipt["success"] else 2)


if __name__ == "__main__":
    main()
