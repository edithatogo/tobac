"""Inventory historical publication surfaces without rewriting or deleting anything."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from publication_boundary import ROOT, git, load_policy


def api(endpoint: str) -> Any:  # noqa: ANN401 -- GitHub list and object endpoints differ; callers select fields.
    """Read all returned pages through the authenticated CLI without printing bodies."""
    data = subprocess.check_output(  # noqa: S603 -- Fixed gh read-only API operation, no shell.
        [shutil.which("gh") or "/opt/homebrew/bin/gh", "api", "--paginate", "--slurp", endpoint], timeout=600
    )
    return json.loads(data)


def assess() -> dict[str, Any]:
    """Record metadata coverage honestly; artifact/log contents remain uninspected."""
    policy = load_policy()
    pages = api("repos/edithatogo/tobac/actions/artifacts?per_page=100")
    artifacts = [
        {k: item.get(k) for k in ("id", "name", "expired", "size_in_bytes", "created_at", "workflow_run")}
        for page in pages
        for item in page["artifacts"]
    ]
    repository = api("repos/edithatogo/tobac")[0]
    return {
        "schema": "tobac.publication-exposure-assessment.v1",
        "source_commit": git(ROOT, "rev-parse", "HEAD").decode().strip(),
        "scope": "metadata_inventory_not_content_inspection_or_cleanup_authorization",
        "repository": {
            k: repository.get(k) for k in ("visibility", "has_pages", "forks_count", "security_and_analysis")
        },
        "local_refs": git(ROOT, "for-each-ref", "--format=%(refname) %(objectname)").decode().splitlines(),
        "remote_branches": [
            {"name": item["name"], "sha": item["commit"]["sha"]}
            for page in api("repos/edithatogo/tobac/branches?per_page=100")
            for item in page
        ],
        "remote_tags": [
            {"name": item["name"], "sha": item["commit"]["sha"]}
            for page in api("repos/edithatogo/tobac/tags?per_page=100")
            for item in page
        ],
        "pull_requests": [
            {
                "number": item["number"],
                "state": item["state"],
                "url": item["html_url"],
                "head_sha": item["head"]["sha"],
            }
            for page in api("repos/edithatogo/tobac/pulls?state=all&per_page=100")
            for item in page
        ],
        "releases": [
            {"id": item["id"], "tag": item["tag_name"], "assets": [a["id"] for a in item["assets"]]}
            for page in api("repos/edithatogo/tobac/releases?per_page=100")
            for item in page
        ],
        "local_document_paths": sorted(policy.private_hashes),
        "artifact_reported_total": pages[0]["total_count"],
        "artifacts_enumerated": len(artifacts),
        "artifacts": artifacts,
        "artifact_log_runs_to_review": sorted(
            {a["workflow_run"]["id"] for a in artifacts if a["workflow_run"]}
        ),
        "unresolved": [
            "Artifact metadata is enumerated; archives still need content classification before deletion.",
            "Run logs, caches and PR refs may retain copies; no complete log/cache inspection claimed.",
            "Historical renamed documents need path tracing before an exact rewrite plan.",
            "Downloaded copies cannot be recalled; zero registered forks is not proof of no external copies.",
            "Preserve active worktrees and old-to-new mappings before a separately reviewed rewrite.",
        ],
        "mutations_performed": False,
    }


def main() -> None:
    """Save a new local assessment outside the public checkout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.resolve().is_relative_to(ROOT) or args.out.exists():
        parser.error("Use a new private output outside the public checkout")
    report = assess()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
