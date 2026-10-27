# Voiage Polars consumer qualification

Owner-authorised implementation and exact unreleased-candidate acceptance:
27 October 2026. Published 3.0 acceptance remains an external gate. Baseline is
2.2.0+tobac3151.2; the unpatched candidate is PR #1202 at immutable 6c28ac5,
whose distribution version is 2.2.0.

## Completed macOS implementation

- [x] Reconcile the original PR with current main, preserving both histories.
- [x] Implement a hash-bound AST surface inventory and rejection fixtures for removed
  symbols; the scan is static and is not proof against arbitrary dynamic lookup.
- [x] Requalify the current baseline: 97 native ecosystem cases pass under Python 3.15.1.
- [x] Add an opt-in immutable candidate build, real native load, exact installed-wheel
  byte checks and independent uniform/weighted/finite-partition EVPI comparisons.
- [x] Resolve candidate metadata against genuine source-bound locks with Polars 2.1.0;
  scientific NumPy/SciPy pins and parity tolerances remain unchanged.
- [x] Preserve the default compatibility producer and pandas/xarray dependencies.
- [x] Add hosted macOS qualification with 4 GiB/time budgets, two build workers,
  pinned Actions and unchanged existing required checks.
- [x] Complete local verification: 924 passed/five capability skips, 92% coverage;
  97 baseline and 69 candidate component tests, 90 API comparisons per wheel;
  all eleven Nox sessions pass. Record exact source/wheel/commands and self-review.

Publication through guarded PR #41 requires every exact-head check and the new
macOS candidate job; receiving-main proof is maintained in that PR. Receipt:
integration/voiage_polars_consumer_20261027.json.

## External published-release gate — blocked

- [ ] Qualify an unpatched published Voiage 3.0.0 wheel when it exists (AC3).
- [ ] Decide patch retirement and the 3.0 dependency base from that release's actual
  metadata (AC4/AC5); do not substitute the unreleased candidate's version or metadata.
- [ ] Close/archive the entire track only when published-release acceptance is executed.

The owner explicitly accepted merging the bounded macOS candidate qualification
while retaining these release gates. No upstream merge/release, pandas-free claim,
generic EVSI qualification or empirical/scientific acceptance is implied.
