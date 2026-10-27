# Active research tracks

## Scientific ecosystem modernisation

**Status: [~] In progress — implementation/review authorised 26 October 2026.**
Track: `conductor/tracks/scientific_ecosystem_20261025/`.

The agreed macOS engineering implementation is complete. PRs #43, #47 and #48
qualified the ecosystem, evidence interchange and Polars 2 boundary. PR #49 qualified
Renovate profile discovery and four-profile lock candidates. [PR #51](https://github.com/edithatogo/tobac/pull/51)
merged at `b012758` with all 15 executable PR checks and all 13 receiving-main jobs
passing, including macOS Python 3.15.1, signed artifacts and native graph readback.
Ruff covers 108 maintained Python files; formatting, five exact preview rules,
process-group resource budgets and two-worker mutation are enforced.

The only unchecked track task is the upstream managed parser's Python 3.15 support
([dependabot-core #16524](https://github.com/dependabot/dependabot-core/issues/16524)).
Supported dependency submission and graph readback pass; the failed managed parser
is not hidden or marked successful. [Draft PR #41](https://github.com/edithatogo/tobac/pull/41)
remains separate planning for future Voiage producer qualification.

[PR #50](https://github.com/edithatogo/tobac/pull/50) qualifies Hypothesis 6.170.9:
all four source-bound locks are regenerated, with complete ecosystem input binding.
Its verification and receiving-main publication are recorded in the PR and
`integration/hypothesis_pr50_20261027.json`; no unexecuted check is implied complete.

## Completed work

Eight completed tracks are archived, including seven moved out of the active registry
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

Status: implementation authorised 27 October 2026; macOS baseline/candidate
qualification in progress. Track: `conductor/tracks/voiage_polars_qualification_20261026/`.
Published Voiage 3.0.0 remains unavailable; no upstream-release success is claimed.
