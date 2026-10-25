"""The drift check must compare numbers against results/, and never raise.

The checked-in snapshot is regenerated here from the two runners in their small
modes, so the pass case is a real run directory rather than a hand-built table.
Only the four graded modules are copied into the synthetic snapshot; the rest of
the run output (paths, figures, manifests) is deliberately excluded because the
checker must not depend on it.
"""
from pathlib import Path
import csv
import importlib.util
import json
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load('check_longitudinal_results', 'scripts/check_longitudinal_results.py')
empirical_runner = _load('drift_empirical_runner', 'scripts/run_empirical_longitudinal.py')
release_runner = _load('drift_release_runner', 'scripts/run_release_calibration.py')


@pytest.fixture(scope='session')
def run_dirs(tmp_path_factory):
    """Real quick-mode runs: the empirical runner and the smallest valid release run."""
    base = tmp_path_factory.mktemp('drift_run')
    empirical = base / 'empirical'
    releases = base / 'releases'
    empirical_runner.run(empirical, quick=True)
    release_runner.run(releases, quick=True, draws=64, skip_figures=True)
    return empirical, releases


def _snapshot(empirical, releases, destination):
    """Write a results/ layout holding only the graded modules."""
    (destination / 'empirical').mkdir(parents=True)
    (destination / 'releases').mkdir(parents=True)
    for group, name, _ in checker.MODULES:
        source = (empirical if group == 'empirical' else releases) / name
        shutil.copy2(source, destination / group / name)
    return destination


@pytest.fixture(scope='session')
def results_dir(run_dirs, tmp_path_factory):
    empirical, releases = run_dirs
    return _snapshot(empirical, releases, tmp_path_factory.mktemp('drift_results'))


def _run_from(results, destination):
    """Build a run layout from the snapshot; run manifests are not needed."""
    (destination / 'empirical').mkdir(parents=True)
    (destination / 'releases').mkdir(parents=True)
    for group, name, _ in checker.MODULES:
        shutil.copy2(results / group / name, destination / group / name)
    return destination


def _read_csv_cell(path, column, row):
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    return rows[row + 1][rows[0].index(column)]


def _rewrite_csv(path, column, row, value):
    """Replace one data cell in a CSV, leaving the header untouched."""
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    rows[row + 1][rows[0].index(column)] = value
    with path.open('w', newline='', encoding='utf-8') as handle:
        csv.writer(handle).writerows(rows)


def _rewrite_json(path, mutate):
    document = json.loads(path.read_text(encoding='utf-8'))
    mutate(document)
    path.write_text(json.dumps(document, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def test_regenerated_run_passes_against_its_snapshot(run_dirs, results_dir):
    empirical, releases = run_dirs
    result = checker.compare(empirical, releases, results_dir)
    assert result['status'] == 'pass', result['errors']
    assert result['errors'] == []
    assert result['compared'] == ['empirical/latent_ratio_summary.csv',
                                  'empirical/source_audit.json',
                                  'releases/forecast_summary.csv',
                                  'releases/predictive_scores.csv']
    assert result['tolerance'] == {'rtol': checker.RTOL, 'atol': checker.ATOL}


def test_perturbation_within_tolerance_passes(tmp_path, results_dir):
    empirical = _run_from(results_dir, tmp_path / 'empirical_run')
    releases = _run_from(results_dir, tmp_path / 'releases_run')
    forecasts = releases / 'releases/forecast_summary.csv'
    _rewrite_csv(forecasts, 'median', 0,
                 repr(float(_read_csv_cell(forecasts, 'median', 0)) * (1 + 1e-10)))
    _rewrite_json(empirical / 'empirical/source_audit.json',
                  lambda doc: doc['source_2014_lower_count_arithmetic'].__setitem__(
                      'stated_smokers_times_intensity',
                      doc['source_2014_lower_count_arithmetic']['stated_smokers_times_intensity']
                      * (1 + 1e-10)))
    result = checker.compare(empirical / 'empirical', releases / 'releases', results_dir)
    assert result['status'] == 'pass', result['errors']


def test_perturbation_beyond_tolerance_names_file_column_and_row(tmp_path, results_dir):
    run = _run_from(results_dir, tmp_path / 'run')
    ratios = run / 'empirical/latent_ratio_summary.csv'
    _rewrite_csv(ratios, 'median_ratio', 2,
                 repr(float(_read_csv_cell(ratios, 'median_ratio', 2)) + 1e-3))
    result = checker.compare(run / 'empirical', run / 'releases', results_dir)
    assert result['status'] == 'fail'
    assert len(result['errors']) == 1
    error = result['errors'][0]
    assert 'empirical/latent_ratio_summary.csv' in error
    assert "'median_ratio'" in error
    assert 'data row 2' in error
    assert '1 cell(s) differ' in error


def test_missing_file_fails_without_raising(tmp_path, results_dir):
    results = tmp_path / 'results'
    shutil.copytree(results_dir, results)
    run = _run_from(results, tmp_path / 'run')
    (results / 'empirical/source_audit.json').unlink()
    result = checker.compare(run / 'empirical', run / 'releases', results)
    assert result['status'] == 'fail'
    assert any('source_audit.json' in error and 'Missing' in error
               for error in result['errors']), result['errors']
    assert 'empirical/source_audit.json' not in result['compared']


def test_missing_results_directory_fails_without_raising(tmp_path, results_dir):
    run = _run_from(results_dir, tmp_path / 'run')
    result = checker.compare(run / 'empirical', run / 'releases', tmp_path / 'absent')
    assert result['status'] == 'fail'
    assert result['compared'] == []
    assert any('results directory' in error for error in result['errors'])


def test_missing_csv_column_fails(tmp_path, results_dir):
    run = _run_from(results_dir, tmp_path / 'run')
    path = run / 'empirical/latent_ratio_summary.csv'
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    drop = rows[0].index('sd_log')
    rows = [row[:drop] + row[drop + 1:] for row in rows]
    with path.open('w', newline='', encoding='utf-8') as handle:
        csv.writer(handle).writerows(rows)
    result = checker.compare(run / 'empirical', run / 'releases', results_dir)
    assert result['status'] == 'fail'
    assert any('column header differs' in error and "'sd_log'" in error
               for error in result['errors']), result['errors']


def test_nan_matches_only_nan(tmp_path, results_dir):
    expected = tmp_path / 'expected'
    shutil.copytree(results_dir, expected)
    run = _run_from(expected, tmp_path / 'run')
    for side in (expected, run):
        _rewrite_csv(side / 'releases/forecast_summary.csv', 'mean', 0, 'nan')
    passing = checker.compare(run / 'empirical', run / 'releases', expected)
    assert passing['status'] == 'pass', passing['errors']

    _rewrite_csv(run / 'releases/forecast_summary.csv', 'mean', 0, '704.8')
    failing = checker.compare(run / 'empirical', run / 'releases', expected)
    assert failing['status'] == 'fail'
    assert any("'mean'" in error and 'data row 0' in error
               for error in failing['errors']), failing['errors']


def _add_key(document):
    document['scope_note'] = 'added in the run only'


def _drop_key(document):
    document.pop('upper_bounds_not_points')


def _change_int(document):
    block = document['source_2014_lower_count_arithmetic']
    block['published'] = block['published'] + 1


def _change_string(document):
    document['period_overlap_status'] = 'tampered'


@pytest.mark.parametrize('mutate,path,label', [
    (_add_key, '$.scope_note', 'added key'),
    (_drop_key, '$.upper_bounds_not_points', 'missing key'),
    (_change_int, '$.source_2014_lower_count_arithmetic.published', 'integer differs'),
    (_change_string, '$.period_overlap_status', 'value differs'),
])
def test_json_structural_change_fails_naming_the_path(tmp_path, results_dir, mutate, path, label):
    run = _run_from(results_dir, tmp_path / 'run')
    _rewrite_json(run / 'empirical/source_audit.json', mutate)
    result = checker.compare(run / 'empirical', run / 'releases', results_dir)
    assert result['status'] == 'fail'
    assert any(path in error and label in error for error in result['errors']), result['errors']


def test_json_integer_is_exact(tmp_path, results_dir):
    run = _run_from(results_dir, tmp_path / 'run')
    _rewrite_json(run / 'empirical/source_audit.json',
                  lambda doc: doc['source_2014_lower_count_arithmetic'].__setitem__(
                      'published', doc['source_2014_lower_count_arithmetic']['published'] + 1))
    result = checker.compare(run / 'empirical', run / 'releases', results_dir)
    assert result['status'] == 'fail'
    error = next(error for error in result['errors'] if 'integer differs' in error)
    assert 'difference 1' in error
    assert '2149262500' in error and '2149262501' in error
