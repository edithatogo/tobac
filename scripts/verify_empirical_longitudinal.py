"""Verify run source/output hashes and scientific scope; not external validation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, cast

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Presence of a *_checks or *_summary file is not itself evidence; require the
# quantitative artefacts the runner claims to produce, independently of the manifest.
REQUIRED = (
    "aligned_observations.csv",
    "latent_ratio_summary.csv",
    "joint_historical_paths.csv",
    "process_sd_posterior.csv",
    "lawful_stock_ledgers.csv",
    "signed_discrepancy_sensitivity.csv",
    "fit_sensitivity.csv",
    "rolling_hindcasts.csv",
    "source_audit.json",
    "fit_scope.json",
    "FIGURE_CAPTIONS.md",
)
# run_manifest.json is loaded separately and cannot list its own hash.


def _read_json(path: Path, errors: list[str], label: str) -> Any:  # noqa: ANN401  # Raw JSON may have any root shape; callers validate the required schema.
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing {label}: {path.name}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {label}: {exc}")
    return None


def verify(out: str | Path, root: Path = ROOT) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0915  # Keep ordered model validation and report assembly in one visible operation.; Keep explicit fail-closed validation branches together.; Keep the declared numerical/report sequence visible and ordered.
    """Verify retained source and output integrity without claiming scientific qualification."""
    out = Path(out).resolve()
    root = Path(root).resolve()
    errors: list[str] = []
    manifest = _read_json(out / "run_manifest.json", errors, "run manifest")
    if manifest is None:
        return {
            "status": "fail",
            "sources": 0,
            "artifacts": 0,
            "errors": errors,
            "scope": "Run integrity and explicit interpretation only; not independent scientific validation",
        }
    if not isinstance(manifest, dict):
        return {
            "status": "fail",
            "sources": 0,
            "artifacts": 0,
            "errors": ["Run manifest must be a JSON object"],
            "scope": "Run integrity and explicit interpretation only; not independent scientific validation",
        }
    manifest = cast("dict[str, Any]", manifest)
    errors.extend(
        f"Run manifest is missing provenance field {key!r}"
        for key in ("commit", "command")
        if key not in manifest
    )
    for group, base in [("sources", root), ("files", out)]:
        items = manifest.get(group)
        if not isinstance(items, list):
            errors.append(f"Run manifest is missing a {group!r} list")
            continue
        for item in cast("list[Any]", items):
            if not isinstance(item, dict) or "path" not in item or "sha256" not in item:
                errors.append(f"Malformed {group} entry: {item!r}")
                continue
            item = cast("dict[str, Any]", item)
            target = (base / item["path"]).resolve()
            if not target.is_relative_to(base) or not target.is_file():
                errors.append(f"Invalid path: {item['path']}")
                continue
            if hashlib.sha256(target.read_bytes()).hexdigest() != item["sha256"]:
                errors.append(f"Hash mismatch: {item['path']}")
    listed = {
        cast("dict[str, Any]", item)["path"]
        for item in manifest.get("files", [])
        if isinstance(item, dict) and "path" in item
    }
    missing = [name for name in REQUIRED if name not in listed or not (out / name).is_file()]
    if missing:
        errors.append("Missing required artefacts: " + ", ".join(missing))
    scope = _read_json(out / "fit_scope.json", errors, "fit scope")
    if isinstance(scope, dict):
        scope = cast("dict[str, Any]", scope)
        if manifest.get("funding_recommendation") is not False:
            errors.append("Funding readiness overstated")
        if scope.get("funding_recommendation") is not False:
            errors.append("Funding readiness overstated in fit scope")
        if scope.get("current_joint_nz_posterior") is not False:
            errors.append("Current empirical status overstated")
        if scope.get("source_positive_gap_is_illicit") is not False:
            errors.append("Signed discrepancy relabelled illicit")
        if scope.get("primary_alignment") != manifest.get("primary_alignment"):
            errors.append("Primary alignment differs between scope and manifest")
        # Recompute the last paired year from the emitted rows rather than trusting
        # a literal repeated in both receipts.
        aligned = out / "aligned_observations.csv"
        if aligned.is_file() and isinstance(manifest.get("primary_alignment"), str):
            frame = pd.read_csv(aligned)
            if "alignment" not in frame:
                errors.append("Aligned observations carry no alignment field")
                subset = frame.iloc[0:0]
            else:
                subset = frame.loc[frame["alignment"].eq(str(manifest["primary_alignment"]))]
            if subset.empty:
                errors.append("No aligned observations for the declared primary alignment")
            elif int(subset.year.max()) != scope.get("latest_paired_year"):
                errors.append("latest_paired_year does not match the primary aligned rows")
        discrepancy = out / "signed_discrepancy_sensitivity.csv"
        if discrepancy.is_file():
            frame = pd.read_csv(discrepancy)
            if "interpretation" not in frame:
                errors.append("Signed discrepancy rows carry no interpretation field")
            elif not (frame.interpretation.astype(str).str.endswith("NOT_illicit_consumption")).all():
                errors.append("Signed discrepancy rows do not all deny illicit-consumption inference")
            base = f"uplift_{float(manifest.get('source_uplift', 0)):g}"
            if not frame.scenario.astype(str).str.startswith(base).any():
                errors.append("Declared base uplift scenario is absent from the discrepancy table")
    return {
        "status": "fail" if errors else "pass",
        "sources": len(manifest.get("sources", [])),
        "artifacts": len(manifest.get("files", [])),
        "errors": errors,
        "scope": "Run integrity and explicit interpretation only; not independent scientific validation",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    result = verify(parser.parse_args().out)
    print(json.dumps(result, indent=2))  # noqa: T201  # CLI emits the requested structured result on stdout.
    raise SystemExit(0 if result["status"] == "pass" else 1)
