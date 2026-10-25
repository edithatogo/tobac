"""Check release-calibration input/output hashes and scope, not scientific validity.

The check fails closed: a missing or malformed manifest, a missing required
artifact, or a missing provenance field is reported as `fail` rather than raised.
Passing means the recorded bytes are unchanged and the scope labels still deny a
funding recommendation. It does not establish empirical validity.
"""
import argparse
import csv
import hashlib
import json
import math
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
    'grid_convergence.csv',
    'monte_carlo_checks.csv',
)
SCOPE = 'integrity only; empirical funding remains unestablished'
GRID_HORIZONS = (1, 5)
GRID_MEASURES = ('mean', 'median', 'lower_95', 'upper_95')
# Observed maximum 2.25e-6 comparing the default 151x60 grid with the doubled
# 301x119 grid at full draws; the bound leaves two orders of magnitude of margin.
GRID_RELATIVE_TOLERANCE = 1e-4
# Observed maximum |z| of ~1.47 at 8192 draws; the bound catches a broken
# sampler without rejecting ordinary Monte Carlo noise.
MONTE_CARLO_SIGMA_TOLERANCE = 5.0


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


def _rows(path: Path) -> tuple[list[dict[str, str]] | None, str | None]:
    """Read a CSV table, reporting an unreadable file instead of raising."""
    try:
        with path.open(newline='', encoding='utf-8') as handle:
            return list(csv.DictReader(handle)), None
    except (OSError, csv.Error) as exc:
        return None, f'Unreadable {path}: {exc}'


def _finite(value: Any) -> float | None:
    """Return the finite float value, or None for missing, malformed or NaN/inf."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _summary_scope(
    out: Path, errors: list[str],
) -> tuple[list[str] | None, set[tuple[str, int]] | None]:
    """Return the model names and (model, year) pairs declared by forecast_summary."""
    path = out / 'forecast_summary.csv'
    if not path.is_file():
        return None, None
    rows, problem = _rows(path)
    if rows is None:
        errors.append(problem or f'Unreadable {path}')
        return None, None
    models: list[str] = []
    pairs: set[tuple[str, int]] = set()
    for row in rows:
        model = row.get('model')
        if model not in models:
            models.append(model)
        try:
            year = int(row.get('year', ''))
        except (TypeError, ValueError):
            errors.append(
                f'forecast_summary.csv has a non-integer year: {row!r}')
            continue
        pairs.add((model, year))
    return models, pairs


def _check_grid(
    out: Path, errors: list[str], models: list[str],
) -> None:
    """Require one converged row per configured model, horizon and measure."""
    path = out / 'grid_convergence.csv'
    if not path.is_file():
        return
    rows, problem = _rows(path)
    if rows is None:
        errors.append(problem or f'Unreadable {path}')
        return
    horizons = set(GRID_HORIZONS)
    measures = set(GRID_MEASURES)
    expected = len(models) * len(horizons) * len(measures)
    if len(rows) != expected:
        errors.append(
            f'grid_convergence.csv has {len(rows)} rows; expected {expected} '
            f'({len(models)} models x {len(horizons)} horizons x '
            f'{len(measures)} measures)')
    seen: set[tuple[str, int, str]] = set()
    for row in rows:
        model = row.get('model')
        try:
            horizon = int(row.get('horizon', ''))
        except (TypeError, ValueError):
            errors.append(
                f'grid_convergence.csv has a non-integer horizon: {row!r}')
            continue
        measure = row.get('measure')
        key = (model, horizon, measure)
        if model not in models or horizon not in horizons or measure not in measures:
            errors.append(
                'grid_convergence.csv contains an unexpected row: '
                f'model={model!r} horizon={horizon!r} measure={measure!r}')
            continue
        if key in seen:
            errors.append(
                'grid_convergence.csv repeats '
                f'model={model!r} horizon={horizon!r} measure={measure!r}')
            continue
        seen.add(key)
        observed = _finite(row.get('relative_difference'))
        if observed is None:
            errors.append(
                'grid_convergence.csv relative_difference is not finite for '
                f'model={model!r} horizon={horizon!r} measure={measure!r}: '
                f'{row.get("relative_difference")!r}')
        elif observed > GRID_RELATIVE_TOLERANCE:
            errors.append(
                'grid_convergence.csv relative_difference '
                f'{observed!r} exceeds {GRID_RELATIVE_TOLERANCE!r} for '
                f'model={model!r} horizon={horizon!r} measure={measure!r}')
    for model in models:
        for horizon in GRID_HORIZONS:
            for measure in GRID_MEASURES:
                if (model, horizon, measure) not in seen:
                    errors.append(
                        'grid_convergence.csv is missing '
                        f'model={model!r} horizon={horizon!r} '
                        f'measure={measure!r}')


def _check_monte_carlo(
    out: Path, errors: list[str], pairs: set[tuple[str, int]],
) -> None:
    """Require a finite, sufficiently precise simulated mean for every model/year."""
    path = out / 'monte_carlo_checks.csv'
    if not path.is_file():
        return
    rows, problem = _rows(path)
    if rows is None:
        errors.append(problem or f'Unreadable {path}')
        return
    if len(rows) != len(pairs):
        errors.append(
            f'monte_carlo_checks.csv has {len(rows)} rows; expected '
            f'{len(pairs)} (one per model/year in forecast_summary.csv)')
    seen: set[tuple[str, int]] = set()
    for row in rows:
        model = row.get('model')
        try:
            year = int(row.get('year', ''))
        except (TypeError, ValueError):
            errors.append(
                f'monte_carlo_checks.csv has a non-integer year: {row!r}')
            continue
        key = (model, year)
        if key not in pairs:
            errors.append(
                'monte_carlo_checks.csv contains an unexpected row: '
                f'model={model!r} year={year!r}')
            continue
        if key in seen:
            errors.append(
                'monte_carlo_checks.csv repeats '
                f'model={model!r} year={year!r}')
            continue
        seen.add(key)
        draws = _finite(row.get('draws'))
        if draws is None or draws < 1:
            errors.append(
                'monte_carlo_checks.csv draws must be a finite value >= 1 for '
                f'model={model!r} year={year!r}: {row.get("draws")!r}')
        analytic = _finite(row.get('analytic_mean'))
        simulation = _finite(row.get('simulation_mean'))
        mcse = _finite(row.get('mcse_mean'))
        for statistic, value, raw in (
            ('analytic_mean', analytic, row.get('analytic_mean')),
            ('simulation_mean', simulation, row.get('simulation_mean')),
        ):
            if value is None:
                errors.append(
                    f'monte_carlo_checks.csv {statistic} is not finite for '
                    f'model={model!r} year={year!r}: {raw!r}')
        if mcse is None or mcse <= 0:
            errors.append(
                'monte_carlo_checks.csv mcse_mean must be finite and > 0 for '
                f'model={model!r} year={year!r}: {row.get("mcse_mean")!r}')
        elif analytic is not None and simulation is not None:
            z = (analytic - simulation) / mcse
            if abs(z) > MONTE_CARLO_SIGMA_TOLERANCE:
                errors.append(
                    'monte_carlo_checks.csv simulation_mean differs from '
                    f'analytic_mean by {z!r} MCSE (bound '
                    f'{MONTE_CARLO_SIGMA_TOLERANCE!r}) for model={model!r} '
                    f'year={year!r}: analytic_mean={analytic!r} '
                    f'simulation_mean={simulation!r} mcse_mean={mcse!r}')
    for model, year in sorted(pairs):
        if (model, year) not in seen:
            errors.append(
                'monte_carlo_checks.csv is missing '
                f'model={model!r} year={year!r}')


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

    models, pairs = _summary_scope(out, errors)
    if models is not None and pairs is not None:
        _check_grid(out, errors, models)
        _check_monte_carlo(out, errors, pairs)

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
