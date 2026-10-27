# Active research tracks

## Scientific ecosystem modernisation

**Status: [~] In progress — implementation/review authorised 26 October 2026.**
Track: `conductor/tracks/scientific_ecosystem_20261025/`.

The agreed macOS engineering implementation is complete. PRs #43, #47 and #48
qualified the ecosystem, evidence interchange and Polars 2 boundary. PR #49 qualified
Renovate profile discovery and four-profile lock candidates. [PR #51](https://github.com/edithatogo/tobac/pull/51)
merged at `b012758` with all 15 executable PR checks and all 13 receiving-main jobs
passing, including macOS Python 3.15.1, signed artifacts and native graph readback.
Ruff covers 112 maintained Python files; formatting, five exact preview rules,
process-group resource budgets and two-worker mutation are enforced.

The only unchecked track task is the upstream managed parser's Python 3.15 support
([dependabot-core #16524](https://github.com/dependabot/dependabot-core/issues/16524)).
Supported dependency submission and graph readback pass; the failed managed parser
is not hidden or marked successful. [Merged PR #41](https://github.com/edithatogo/tobac/pull/41)
implements separate exact-candidate qualification; published-3.0 acceptance remains open.

[PR #50](https://github.com/edithatogo/tobac/pull/50) qualifies Hypothesis 6.170.9:
all four source-bound locks are regenerated, with complete ecosystem input binding.
Its verification and receiving-main publication are recorded in the PR and
`integration/hypothesis_pr50_20261027.json`; no unexecuted check is implied complete.

## Completed work

Nine completed tracks are archived, including seven moved out of the active registry
on 26 October and the earlier longitudinal archive. See
[the archive index](archive/index.md) for their specifications, plans and dated receipts.

## Research gates

[Open research gates](research-gates.md) retain decision scope, source conflicts,
measurement/covariance, transport, empirical calibration and permissible-use requirements.
M1/M2/M3 computational results are conditional research, not a current national posterior
or a commissioning recommendation. Source/forecast identities and data-once guards remain.

## Deferred development

[Roadmap](roadmap.md): non-macOS qualification, optional advisory promotion and explicitly optional
mutation/source-style follow-ups. Existing hosted checks and full-SHA pins remain required.

## Voiage Polars consumer qualification

Status: bounded macOS baseline/candidate implementation complete; published-3.0
acceptance blocked externally.

Track: `conductor/tracks/voiage_polars_qualification_20261026/`.
Published Voiage 3.0.0 remains unavailable; no upstream-release success is claimed.

Current receipt: integration/voiage_polars_consumer_20261027.json. Default producer
2.2.0+tobac3151.2 retained; unpatched candidate at 6c28ac5 is unreleased version
2.2.0. pandas/xarray remain required. Hosted/receiving-main execution is recorded in PR #41.

## Issue #3 bounded pathway implementation

The source-feasibility audit and prospective matched-consumption protocol are implemented
and self-reviewed at 0bdb6ad. [Completed plan](archive/m2_matched_evidence_20261027/plan.md).
The applied issue remains open: all eight matched consumption cells are missing,
with no causal/empirical posterior or deployment acceptance. Current requirements
remain in [research gates](research-gates.md) and issue #3.
