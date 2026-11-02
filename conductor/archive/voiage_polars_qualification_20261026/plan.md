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

- [x] Qualify an unpatched published Voiage 3.0.0 wheel when it exists (AC3).
- [x] Decide patch retirement and the 3.0 dependency base from that release's actual
  metadata (AC4/AC5); do not substitute the unreleased candidate's version or metadata.
- [x] Close/archive the entire track only when published-release acceptance is executed.

The owner explicitly accepted merging the bounded macOS candidate qualification
while retaining these release gates. No upstream merge/release, pandas-free claim,
generic EVSI qualification or empirical/scientific acceptance is implied.

## Resumed candidate qualification: 28 October 2026

- [x] Demonstrate caller-buffer aliasing on the previous 6c28ac5 candidate and
  qualify merged PR #1202 revision 65c5e76 with mutation-isolation regression checks.
- [x] Review and verify the updated unpatched candidate on macOS Python 3.15.1,
  retaining the original default producer and published-release gate (17a2530).
  Full suite: 1,032 passed/five capability skips, 92% coverage. Strict lint, formatting
  and typing pass; candidate: 72 component tests, six ownership cases, 90 comparisons.
- [x] Prepare the committed guarded-publication handoff. Exact-head checks, macOS
  numerical replay and receiving-main verification remain required before merge;
  actual hosted/receiving execution is maintained in the qualification PR.

Review and receipt: docs/reviews/2026-10-28-voiage-merged-candidate.md and
integration/voiage_polars_consumer_20261028.json. The complete track remains
externally blocked, with all three published-release/archiving tasks above open.


## macOS-only receiving qualification — owner direction, 28 October 2026

- [x] Defer Windows/Linux jobs (b2a9353); move remaining semantic checks to macOS and retain
  Linux-only manual workflow definitions in the roadmap. Preserve all security,
  scientific and numerical thresholds, source-bound locks and full-SHA Actions.
- [x] Review and verify the platform change with affected contracts, cross-workstream
  integration, full tests and strict checks; reuse unchanged numerical evidence.
  Final local: 1,033 passed/five capability skips, 92% coverage; security and strict
  checks pass. SourceRight validates all five citation collections natively.
  Follow-up trigger/concurrency contracts: 13 passed; workflow security passes.
- [x] Prepare the committed macOS-only publication handoff. Fresh exact-head checks
  and receiving-main artifacts, provenance and dependency-graph submission remain
  required for acceptance and are recorded in the platform-scope PR. Superseded
  mixed-platform main runs are not acceptance gates and are not recorded as passes.

Platform review: docs/reviews/2026-10-28-macos-only-ci.md. Receipt:
integration/macos_ci_scope_20261028.json. Windows/Linux return only through
roadmap reprioritisation; the published Voiage 3.0.0 gate remains externally blocked.

## Published 3.0.0 acceptance — 2 November 2026

The PyPI macOS arm64 cp315 wheel was downloaded without modification and
matched SHA-256 1609185222be3e69c064b2716ed57c03101b4e7b802cbde9f6093b03b7c1aa7c.
Its actual native extension loaded on Python 3.15.1. All installed wheel members
matched, all 90 uniform/weighted/finite-partition comparisons passed at the
unchanged 1e-10 tolerances (maximum difference 2.842170943040401e-14), and all
six buffer ownership checks passed. Pandas and xarray were absent.

The compatibility patch is unnecessary for the published 3.0.0 lane and is
retained only for the separate historical 2.2 regression build. Published
runtime dependencies are recorded in integration/voiage_published_20261102.json.
Pandas remains required by longitudinal scripts. Xarray remains only in the
legacy Voiage regression environment. The new voiage_published Nox session
syncs hash-locked genuine dependencies, checks the wheel digest, and runs the
same native consumer probe. Hosted candidate qualification also runs this
published lane. Voiage 3.1.0 was observed but is outside this exact release
acceptance. No automatic promotion to it is implied.

The initial probe completed its computations but failed while recording absent
pandas. Receipt generation now represents absent optional packages as null.
The exact released wheel installed without metadata patches. This closes AC3,
AC4 and AC5; the ordinary scientific/data acceptance gates remain independent.
