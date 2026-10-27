"""Export input-verified resolved locks through GitHub's supported snapshot schema."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lock_receipt import PROFILES, verify

ROOT = Path(__file__).resolve().parents[1]


def packages(path: Path) -> dict[str, Any]:
    """Retain exact resolved PURLs; do not infer dependency edges or directness."""
    result: dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip().removesuffix("\\").strip()
        if not line or line.startswith(("#", "--hash=")):
            continue
        requirement = Requirement(line)
        specs = list(requirement.specifier)
        if len(specs) != 1 or specs[0].operator != "==" or "*" in specs[0].version or requirement.url:
            msg = "Require exact resolved lock versions"
            raise ValueError(msg)
        name = canonicalize_name(requirement.name)
        if name in result:
            msg = "Ambiguous duplicate lock package"
            raise ValueError(msg)
        result[name] = {"package_url": f"pkg:pypi/{quote(name, safe='')}@{quote(specs[0].version, safe='')}"}
    if not result:
        msg = "No resolved lock packages"
        raise ValueError(msg)
    return result


def snapshot(sha: str, ref: str, job: str) -> dict[str, Any]:
    """Verify each generated lock before describing the exact committed inputs."""
    if (
        sys.version_info[:3] != (3, 15, 1)
        or not re.fullmatch(r"[0-9a-f]{40}", sha)
        or not ref.startswith("refs/heads/")
        or not job
    ):
        msg = "Require Python 3.15.1 and exact source/job identity"
        raise ValueError(msg)
    git = shutil.which("git")
    if git is None:
        msg = "Git is required to verify committed snapshot inputs"
        raise RuntimeError(msg)
    head = subprocess.check_output(  # noqa: S603  # Fixed local Git read, no shell.
        [git, "-C", str(ROOT), "rev-parse", "HEAD"], text=True, timeout=15
    ).strip()
    if sha != head:
        msg = "Snapshot source must match the checked-out commit"
        raise ValueError(msg)
    manifests: dict[str, Any] = {}
    for profile, (_, name) in PROFILES.items():
        path = ROOT / "engineering" / name
        verify(ROOT, path, profile)
        location = path.relative_to(ROOT).as_posix()
        committed = subprocess.check_output(  # noqa: S603  # Fixed local Git object read.
            [git, "-C", str(ROOT), "show", f"{sha}:{location}"], timeout=15
        )
        if hashlib.sha256(committed).hexdigest() != hashlib.sha256(path.read_bytes()).hexdigest():
            msg = "Resolved lock differs from the committed snapshot source"
            raise ValueError(msg)
        manifests[location] = {
            "name": location,
            "file": {"source_location": location},
            "metadata": {
                "lock_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "scope": "resolved profile inventory; no unobserved dependency edges",
            },
            "resolved": packages(path),
        }
    return {
        "version": 0,
        "sha": sha,
        "ref": ref,
        "job": {"id": job, "correlator": "tobac-resolved-python315-locks"},
        "detector": {
            "name": "tobac-verified-locks",
            "version": "1.0.0",
            "url": "https://github.com/edithatogo/tobac",
        },
        "scanned": datetime.now(UTC).isoformat(),
        "metadata": {"python": "3.15.1", "service_runtime_bypass": False},
        "manifests": manifests,
    }


def main() -> None:
    """Generate a fresh payload; API publication is an explicit separate CLI step."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sha",
        default=os.environ.get("GITHUB_SHA"),
        required="GITHUB_SHA" not in os.environ,
    )
    parser.add_argument(
        "--ref",
        default=os.environ.get("GITHUB_REF"),
        required="GITHUB_REF" not in os.environ,
    )
    parser.add_argument(
        "--job",
        default=os.environ.get("GITHUB_RUN_ID"),
        required="GITHUB_RUN_ID" not in os.environ,
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = snapshot(args.sha, args.ref, args.job)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
