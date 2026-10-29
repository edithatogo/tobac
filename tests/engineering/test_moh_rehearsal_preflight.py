"""Independent controls for the bounded MOH rehearsal inventory guard."""

import copy
import importlib.util
from pathlib import Path

import pytest


def check():
    path = Path(__file__).resolve().parents[2] / "scripts/check_moh_rehearsal.py"
    spec = importlib.util.spec_from_file_location("moh_rehearsal_check", path)
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_rehearsal_manifest


def examples():
    ids = ["sha256:" + f"{n:064x}" for n in range(1, 10)]
    inventory = {
        "inventory_sha256": "a" * 64,
        "objects": [{"object_id": oid, "byte_count": i} for i, oid in enumerate(ids)],
    }
    manifest = {
        "sha256_root": "a" * 64,
        "records_count": 9,
        "records": [{"record_id": oid, "sha256": oid[7:], "size_bytes": i} for i, oid in enumerate(ids)],
    }
    return manifest, inventory, ids


def test_valid_nine_object_rehearsal() -> None:
    manifest, inventory, ids = examples()
    check()(manifest, inventory, ids)


@pytest.mark.parametrize("case", ["empty", "wrong_root", "duplicate", "missing", "extra", "size", "ids"])
def test_rejects_incomplete_or_inconsistent_manifest(case) -> None:
    manifest, inventory, ids = examples()
    manifest, inventory, ids = copy.deepcopy((manifest, inventory, ids))
    if case == "empty":
        manifest["records"] = []
        manifest["records_count"] = 0
    elif case == "wrong_root":
        manifest["sha256_root"] = "0" * 64
    elif case == "duplicate":
        manifest["records"][-1] = manifest["records"][0]
    elif case == "missing":
        inventory["objects"].pop()
    elif case == "extra":
        manifest["records"].append(manifest["records"][0])
        manifest["records_count"] = 10
    elif case == "size":
        manifest["records"][0]["size_bytes"] += 1
    else:
        ids[-1] = ids[0]
    with pytest.raises(ValueError, match="Rehearsal"):
        check()(manifest, inventory, ids)
