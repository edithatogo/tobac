# Longitudinal component incorporated into tobac

Dylan A Mordaunt | 24 October 2026 | Imported component version 2.9.0

## What is incorporated
The reported-release transition model (v2.8) and historical survey/supply ratio model (v2.9)
are executable sibling modules under `src/tobac_supply/`. Existing `src/tobac/` regulatory
M1/M2a code, assumptions, source records and results are preserved. This is a bounded source
integration, not replacement of the live repository with the 74 MB predecessor archive.

Included: four numerical/accounting modules, runners and integrity verifiers, historical
input tables, declared configurations, methods, protocol amendment, 151 imported tests,
source metadata and compact checked-in result tables. The runners regenerate all posterior
paths, sensitivity tables, eight PNG/SVG figure pairs, captions and source/output manifests.
Large path matrices and rendered figures are generated artifacts rather than duplicated
Git history. The complete predecessor archive remains a separate conversation download.

## Reproduce from a clean Python 3.15.1 checkout

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps .
python -m pytest -q
OPENBLAS_NUM_THREADS=1 python scripts/run_release_calibration.py --out outputs/my_releases
python scripts/verify_release_calibration.py outputs/my_releases
OPENBLAS_NUM_THREADS=1 python scripts/run_empirical_longitudinal.py --out outputs/my_empirical
python scripts/verify_empirical_longitudinal.py outputs/my_empirical
```

Use new output directories; runners reject nonempty directories. A focused check is
`python -m pytest -q tests/supply_bridge`. The longitudinal Actions workflow runs the same
full analyses and uploads their complete outputs. A workflow definition is not a successful
hosted run; see "Hosted execution" below for the run that did complete, and issue #4 for
current runner availability.

## Scientific boundary
The 16 administrative tonne observations and 12 historical cigarette-equivalent records
are distinct source series. No implicit tonne-to-stick conversion is allowed. Eleven
nominal survey-period ratios are fitted because the first period lacks preceding supply.
The count-bound midpoint is reconstructed; it is not a published central observation.
Stocks, visitors, absent lawful channels, reporting factors and error assumptions remain
explicit sensitivity inputs. A positive or negative discrepancy does not identify legality.

No code in this import automatically updates the regulatory prior. A future connection to
`src/tobac/evidence.py` must use underlying source identities, aligned Scope and shared state
IDs, with scientifically reviewed transport and dependence. Posterior draws and forecasts
must not be passed as new observations. Shared MOH/NZHS records must condition existing
information once. Current paired assays, causal diversion/mitigation, criminal harms and
NZ monetary funding conclusions remain unqualified.

## Verification of this import
The renamed package and relocated tests passed 151 local tests. Both full runners were
executed with 8,192 paths (per model for releases); their six-source integrity checks passed
for 21 empirical and 23 release artifacts. A local one-off comparison of generated output
against the predecessor archive reported 42 of 43 comparable files as byte-identical, with a
maximum absolute difference of 2.45e-15 on `release grid_convergence.csv`, attributed in the
receipt to relative-difference rounding. That is a recorded result, not a reproducible check:
the comparison table, the per-file hashes and the command were not retained, and the
predecessor archive is not part of this repository, so the 42-of-43 count cannot be re-derived
here. Source hashes change with namespace/LF changes.

Known limitation. The runners were refactored after the receipt above was written (commit
`b47af43`, type annotations), and the verification scripts hash the runner sources, so the
retained local output directories no longer pass `scripts/verify_*.py` against current HEAD.
The compact checked-in tables under `results/` were re-checked separately and were reported to
agree to about 1e-15, but no command or receipt for that re-check is retained here. Treat the
current-HEAD state of this section as a recorded limitation, not a passing check.

This is a fresh check of the imported component, not a claim that the parallel regulatory
suite or third-party integrations were freshly executed locally. Existing regulatory source
and result trees are preserved by the Git base-tree operation. See the local receipt in
`integration/longitudinal_local_verification.json` and the coordination record in issue #1.

### Hosted execution

The current workflow revision has now executed on `main`. Push run 40180241081 at
`903ca35` completed every step: the preserved-evidence inventory, `pytest` (**582 passed in
48.69 s**), both full runners and both verifiers (`errors: []`). The regulatory, engineering
and M3 push workflows on the same commit also succeeded. This supersedes the earlier attempt
(run 40064143521, which failed before any step ran) and removes "no hosted pass" as an open
gate; it does not establish scientific validity, external review or a current-NZ posterior.

The uploaded artefact was then compared with the checked-in compact tables at that same
commit: `source_audit.json`, `forecast_summary.csv` and `predictive_scores.csv` are
byte-identical, and `latent_ratio_summary.csv` differs only in the last bits of
`median_ratio` (maximum absolute difference 3.4e-13 on a 0.85-scale value, about 4e-13
relative; every other column within 2e-15). That comparison was performed once for this
review and is recorded in `integration/m2b_review_20261025.json`; it is not a CI gate, so
the tables can still drift silently in future.

## Sources and methods
- [Historical ratio methods](METHODS_AND_ASSUMPTIONS_v2.9.0.md)
- [Reported-release methods](../calibration/METHODS_AND_ASSUMPTIONS_v2.8.0.md)
- [Protocol amendment](../../protocols/NZ_Empirical_Longitudinal_Amendment_2026-10-24_v2.9.0.md)
- [Compact results](../../results/longitudinal/)
- [Source references](../../evidence/longitudinal/references.csl.json)

No OSF registration, agency endorsement, newly commissioned study or current empirical
funding recommendation is implied by repository publication.
