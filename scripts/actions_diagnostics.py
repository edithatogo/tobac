"""Read-only GitHub CLI diagnosis. Annotation text is evidence, never a command.

Run on an authenticated machine even when hosted runners cannot start. No billing,
permissions, visibility, workflow, secret or branch settings are changed.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


def validate_repository(repository: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+", repository) or repository.rsplit(
        "/", maxsplit=1
    )[-1] in {".", ".."}:
        raise ValueError("Use an owner/repository identifier")
    return repository


def get_json(endpoint: str, *, paginate: bool = False) -> Any:
    gh = shutil.which("gh")
    if gh is None:
        raise ValueError(
            "Install/authenticate the official gh CLI; no credentials are collected by this script"
        )
    command = [gh, "api", "--hostname", "github.com", "--method", "GET", endpoint]
    if paginate:
        command += ["--paginate", "--slurp"]
    output = subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)
    return json.loads(output.stdout)


def flatten_jobs(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not pages or any(not isinstance(page.get("jobs"), list) for page in pages):
        raise ValueError("Missing paginated jobs response")
    jobs = [job for page in pages for job in page["jobs"]]
    if len(jobs) != pages[0].get("total_count") or len({j["id"] for j in jobs}) != len(jobs):
        raise ValueError("Partial/duplicate job pages; retry after run state settles")
    return jobs


def summarise(
    run: dict[str, Any], jobs: list[dict[str, Any]], annotations: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    summaries = []
    for job in jobs:
        steps = job.get("steps") or []
        execution = "steps_reported" if steps else "not_started" if job.get("runner_id") == 0 else "unknown"
        summaries.append(
            {
                "id": job["id"],
                "name": job.get("name"),
                "conclusion": job.get("conclusion"),
                "execution": execution,
                "runner_id": job.get("runner_id"),
                "step_count": len(steps),
                "failed_steps": [s.get("name") for s in steps if s.get("conclusion") == "failure"],
                "annotations": annotations.get(str(job["id"]), []),
            }
        )
    return {
        "schema": "tobac.actions-diagnostic.v1",
        "run_id": run["id"],
        "head_sha": run.get("head_sha"),
        "run_url": run.get("html_url"),
        "jobs": summaries,
        "qualification_pass": run.get("status") == "completed"
        and run.get("conclusion") == "success"
        and bool(summaries)
        and all(j["conclusion"] == "success" and j["execution"] == "steps_reported" for j in summaries),
        "root_cause": "inspect_recorded_annotations" if any(annotations.values()) else "not_established",
        "qualification": "workflow job evidence only; not complete repository, third-party or scientific qualification",
    }


def collect(repository: str, run_id: int) -> dict[str, Any]:
    repository = validate_repository(repository)
    if isinstance(run_id, bool) or not isinstance(run_id, int) or run_id <= 0:
        raise ValueError("Positive integer run ID required")
    prefix = f"repos/{repository}"
    run = get_json(f"{prefix}/actions/runs/{run_id}")
    jobs = flatten_jobs(get_json(f"{prefix}/actions/runs/{run_id}/jobs?per_page=100", paginate=True))
    annotations: dict[str, list[dict[str, Any]]] = {}
    errors = []
    for job in jobs:
        # Check IDs come from the returned check_run_url, not the Actions job ID convention.
        url = job.get("check_run_url", "")
        match = re.fullmatch(r"https://api.github.com/" + re.escape(prefix) + r"/check-runs/([0-9]+)", url)
        if not match:
            errors.append({"job_id": job["id"], "error": "check_run_url_missing_or_mismatched"})
            continue
        try:
            pages = get_json(f"{prefix}/check-runs/{match[1]}/annotations?per_page=100", paginate=True)
            annotations[str(job["id"])] = [
                {"message": a.get("message"), "level": a.get("annotation_level")}
                for page in pages
                for a in page
            ]
        except ValueError, OSError, subprocess.SubprocessError:
            errors.append({"job_id": job["id"], "error": "annotations_unavailable"})
    report = summarise(run, jobs, annotations)
    report["annotation_errors"] = errors
    report["repository"] = repository
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="edithatogo/tobac")
    parser.add_argument("--run", required=True, type=int)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError("Refusing to overwrite a previous diagnostic receipt")
    report = collect(args.repo, args.run)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["qualification_pass"] else 1)


if __name__ == "__main__":
    main()
