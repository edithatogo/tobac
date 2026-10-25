"""Check release-calibration input/output hashes and scope, not scientific validity.

The check fails closed: a missing or malformed manifest, a missing required
artifact, or a missing provenance field is reported as `fail` rather than raised.
Passing means the recorded bytes are unchanged and the scope labels still deny a
funding recommendation. It does not establish empirical validity.
"""
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ARTIFACTS = (
    'forecast_summary.csv',
    'predictive_scores.csv',
    'rolling_predictive_checks.csv',
    'posterior_parameter_summary.csv',
    'source_reconciliation.json',
    'fit_scope.json',
)
SCOPE = 'integrity only; empirical funding remains unestablished'


def _report(errors: list[str], sources: int, artifacts: int) -> dict[str, Any]:
    return {'status': 'pass' if not errors else 'fail', 'sources': sources,
            'artifacts': artifacts, 'required_artifacts': len(REQUIRED_ARTIFACTS),
            'errors': errors, 'scope': SCOPE}


def _load(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        loaded = json.loads(path.read_text())
    except OSError as exc:
        return None, f'Unreadable {path}: {exc}'
    except json.JSONDecodeError as exc:
        return None, f'Malformed JSON in {path}: {exc}'
    if not isinstance(loaded, dict):
        return None, f'Expected a JSON object in {path}; got {type(loaded).__name__}'
    return loaded, None


def verify(out: Any, root: Any = ROOT) -> dict[str, Any]:
    """Return a fail-closed integrity report for one calibration output directory.

    Args:
      out: Directory written by scripts/run_release_calibration.py.
      root: Repository root that manifest `sources` paths are relative to.

    Returns:
      Report with status 'pass' or 'fail', record counts and an explicit `errors`
      list. Missing inputs are reported, never raised.
    """
    out = Path(out).resolve()
    root = Path(root).resolve()
    errors: list[str] = []
    manifest_path = out / 'run_manifest.json'
    data, problem = _load(manifest_path) if manifest_path.is_file() else (
        None,
        f'Missing run manifest: {manifest_path}; run the calibration script first')
    if data is None:
        return _report([problem or f'Missing run manifest: {manifest_path}'], 0, 0)

    if data.get('funding_recommendation') is not False:
        errors.append(
            'Manifest funding_recommendation is not False; funding was overstated')
    for field in ('commit', 'command'):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(
                f'Manifest must record a non-empty {field!r}; '
                'rerun the calibration script')

    listed: list[Any] = []
    for group, base in (('sources', root), ('files', out)):
        items = data.get(group)
        if not isinstance(items, list):
            errors.append(
                f'Manifest field {group!r} must be a list of path/sha256 records')
            continue
        for item in items:
            if not isinstance(item, dict):
                errors.append(f'Manifest record must be an object; got {item!r}')
                continue
            if group == 'files':
                listed.append(item.get('path'))
            path, digest = item.get('path'), item.get('sha256')
            if not isinstance(path, str) or not isinstance(digest, str):
                errors.append(
                    f'Manifest record needs string path and sha256; got {item!r}')
                continue
            target = (base / path).resolve()
            if not target.is_relative_to(base) or not target.is_file():
                errors.append(
                    f'Invalid file path outside or absent from {base}: {path}')
                continue
            if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                errors.append(f'Hash mismatch for {path}')

    for required in REQUIRED_ARTIFACTS:
        if required not in listed:
            errors.append(f'Required artifact missing from manifest: {required}')
        if not (out / required).is_file():
            errors.append(
                f'Required artifact missing from output directory: {required}')

    scope_path = out / 'fit_scope.json'
    scope, problem = _load(scope_path) if scope_path.is_file() else (
        None, f'Missing fit scope: {scope_path}')
    if scope is None:
        errors.append(problem or f'Missing fit scope: {scope_path}')
    else:
        if scope.get('estimand') != 'reported_lawful_smoked_tobacco_releases':
            errors.append('Estimand changed in fit_scope.json')
        if scope.get('funding_recommendation') is not False:
            errors.append(
                'fit_scope funding_recommendation is not False; funding was overstated')

    return _report(errors, len(data.get('sources') or []), len(data.get('files') or []))


def main() -> None:
    """Print the integrity report; exit nonzero unless the status is `pass`."""
    parser = argparse.ArgumentParser()
    parser.add_argument('out', type=Path)
    result = verify(parser.parse_args().out)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'] == 'pass' else 1)


if __name__ == '__main__':
    main()
