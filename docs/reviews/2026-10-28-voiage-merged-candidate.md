# Review Report: Voiage Polars merged-candidate qualification

## Summary

The opt-in candidate now qualifies the merged upstream caller-buffer fix while
preserving the default producer and the unavailable published-3.0 release gate.

## Verification Checks

- [x] **Plan Compliance**: Yes, immutable unpatched candidate with retained release gates.
- [x] **Style Compliance**: Ruff lint and formatting; complete strict session recorded below.
- [x] **New Tests**: Yes, an aliasing synthetic container fails and a snapshot container
  passes; six real candidate mutation cases run after exact wheel/native verification.
- [x] **Test Coverage**: Full suite: 1,032 passed, five capability skips, 92% coverage.
- [x] **Test Results**: Candidate: 72 tests, six ownership cases and 90 numerical comparisons
  passed under actual Python 3.15.1; maximum numerical error 2.842170943040401e-14.
  Strict Ruff lint/format and BasedPyright pass with zero errors/warnings.

## Findings and fixes applied

### High: stale candidate permits caller-buffer mutation

The installed previous 6c28ac5 candidate fails the new probe: mutating the caller's
Fortran-contiguous NumPy input changes all four stored values. Upstream PR #1202
has since merged; immutable head 65c5e76 includes an explicit buffer-snapshot fix.
Refresh only the opt-in source pin, build its unpatched wheel and require ownership
checks in the existing hosted candidate session. Verify all 194 installed archive
members and the loaded native binary before running scientific comparisons.
The real merged candidate passes all six ValueArray/ParameterSet construction paths.
Synthetic negative and positive fixtures verify the probe rejects aliasing and
accepts snapshots. This is input-ownership evidence, not a claim of leak freedom.

### Medium: Conductor status and missing track index

Replace the stale in-progress machine status with the externally blocked release
status, refresh the registry/index and add the missing track navigation index.
Preserve the original 27 October receipts and scope as historical evidence. Keep
AC3/AC4/AC5 and archiving open: the exact PyPI 3.0.0 endpoint returns HTTP 404 and
published PyPI/GitHub releases remain at 2.2.0 on 28 October 2026.

## Verification and boundaries

The candidate uses normal hash-enforced dependency resolution and wheel installation;
no patch, dependency bypass, runtime downgrade, tolerance widening or security waiver.
Dependency input files are unchanged, so existing source-bound locks remain valid.
The default compatibility producer remains 2.2.0+tobac3151.2; pandas/xarray remain.
Successful candidate scratch source and Cargo target trees were cleaned by Nox.
The bounded candidate run peaked at 673.5 MiB sampled process-group RSS.

Exact local milestone results are retained in the dated integration receipt. Hosted
checks and receiving-main artifacts must execute and are recorded in the linked PR;
local execution is not substituted for hosted acceptance. No outside scientific
review, publication, empirical calibration, release or default promotion is claimed.
