"""Write M2 metadata feasibility and explicit research gaps; no empirical update."""

import argparse
import json
import platform
import shutil
import subprocess
import sys
from abc import abstractmethod
from pathlib import Path
from typing import Any, Protocol, cast

import jsonschema
from source_handoff import checked, digest, read, same_hash

from tobac.evidence import Scope
from tobac.matched import MatchedObservation, audit_pathway

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "engineering/schemas/m2-pathway.schema.json"
DEFAULT = "evidence/m2/matched_pathway_20261027.json"


class _Validator(Protocol):
    @abstractmethod
    def validate(self, instance: object) -> None:
        """Validate against the bound schema using the implementing library."""
        raise NotImplementedError


def build_report(root: Path, manifest: str = DEFAULT) -> dict[str, Any]:
    """Validate source-bound declarations without promoting them to scientific evidence."""
    path = checked(root, manifest)
    case = read(path)
    validator = cast("_Validator", jsonschema.Draft202012Validator(read(checked(root, SCHEMA))))
    validator.validate(case)
    for name, expected in case["input_sha256"].items():
        same_hash(root, name, expected)
    source_ids = [source["id"] for source in case["sources"]]
    if len(set(source_ids)) != len(source_ids):
        msg = "Source IDs must be unique"
        raise ValueError(msg)
    observations: list[MatchedObservation] = []
    for row in case["observations"]:
        if row["source_id"] not in source_ids:
            msg = "Observation references an undeclared source"
            raise ValueError(msg)
        observations.append(
            MatchedObservation(
                row["observation_id"],
                row["cell"],
                row["quantity"],
                None if row["scope"] is None else Scope(**row["scope"]),
                tuple(row["products"]),
                tuple(row["data_ids"]),
                row["role"],
            )
        )
    report = audit_pathway(observations)
    inputs = [manifest, SCHEMA, case["protocol"], "src/tobac/matched.py", "scripts/qualify_m2_pathway.py"]
    return {
        "schema_version": "tobac.m2-pathway-report.v1",
        **report,
        "python": platform.python_version(),
        "input_sha256": {**case["input_sha256"], **{name: digest(checked(root, name)) for name in inputs}},
        "sources": case["sources"],
        "research_gaps": case["research_gaps"],
        "next_action": (
            "Resolve feasible legal contrast and matched field access before fitting or study optimisation"
        ),
    }


def checkout_identity(root: Path) -> dict[str, str]:
    """Read the exact checkout identity without modifying repository state."""
    git = shutil.which("git")
    if git is None:
        msg = "Git is required to bind the audit checkout"
        raise FileNotFoundError(msg)
    result: dict[str, str] = {}
    for name, arguments in (
        ("commit", ["rev-parse", "HEAD"]),
        ("tracked_status", ["status", "--porcelain", "--untracked-files=no"]),
    ):
        completed = subprocess.run(  # noqa: S603 -- Resolved executable and fixed read-only Git argv; no shell.
            [git, *arguments],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        result[name] = completed.stdout.strip()
    return result


def main() -> None:
    """Create a new receipt; scientific blocked status is a valid audit outcome."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    before = checkout_identity(ROOT)
    report = build_report(ROOT, args.manifest)
    if checkout_identity(ROOT) != before:
        msg = "Checkout changed during audit"
        raise ValueError(msg)
    report.update(checkout=before, command=[sys.executable, *sys.argv])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as output:
        output.write(json.dumps(report, indent=2, allow_nan=False, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
