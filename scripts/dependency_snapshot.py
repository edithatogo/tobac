"""Export input-verified resolved locks through GitHub's supported snapshot schema."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
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


def verify_metadata_digest(data: bytes, algorithm: str, digest: str) -> None:
    """Compare installed metadata bytes with their RECORD digest, not wheel provenance."""
    actual = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")
    if algorithm != "sha256" or not digest or not hmac.compare_digest(actual, digest):
        msg = "Installed metadata RECORD digest missing or mismatched"
        raise ValueError(msg)


def verify_installed_inventory(path: Path, versions: dict[str, str]) -> None:
    """Match an installed environment against applicable exact lock entries."""
    expected: dict[str, str] = {}
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
        if requirement.marker is not None and not requirement.marker.evaluate({"extra": ""}):
            continue
        if name in expected:
            msg = "Ambiguous applicable lock package"
            raise ValueError(msg)
        expected[name] = specs[0].version
    actual = {canonicalize_name(name): version for name, version in versions.items()}
    if not expected or len(actual) != len(versions) or actual != expected:
        msg = "Installed inventory does not match applicable locked packages"
        raise ValueError(msg)


def installed_relationships(
    versions: dict[str, str], requirements: dict[str, list[str]]
) -> dict[str, list[str]]:
    """Check no-extra relationships in the current environment, without submitting them."""
    normalized = {canonicalize_name(name): version for name, version in versions.items()}
    if len(normalized) != len(versions):
        msg = "Ambiguous installed distribution names"
        raise ValueError(msg)
    normalized_requirements = {canonicalize_name(name): values for name, values in requirements.items()}
    if (
        len(normalized_requirements) != len(requirements)
        or not normalized_requirements.keys() <= normalized.keys()
    ):
        msg = "Unknown or ambiguous requirement owner"
        raise ValueError(msg)
    if normalized_requirements.keys() != normalized.keys():
        msg = "Missing installed package metadata owner"
        raise ValueError(msg)
    result: dict[str, list[str]] = {}
    for name in normalized:
        dependencies: set[str] = set()
        for raw in normalized_requirements.get(name, []):
            requirement = Requirement(raw)
            if requirement.marker is not None and not requirement.marker.evaluate({"extra": ""}):
                continue
            if requirement.url or requirement.extras:
                msg = "Direct references and requested extras require separate qualification"
                raise ValueError(msg)
            target = canonicalize_name(requirement.name)
            if target not in normalized or not requirement.specifier.contains(
                normalized[target], prereleases=True
            ):
                msg = "Installed dependency missing or incompatible"
                raise ValueError(msg)
            dependencies.add(target)
        result[name] = sorted(dependencies)
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
