# Research tracks and current disposition

No implementation track is in progress. See [reconciled status](status.md) for
remaining deferred work, dependency PRs and scientific requirements.

## Scientific ecosystem modernisation

**Status: [x] Bounded implementation closed by owner — 29 October 2026.**
Track: `conductor/archive/scientific_ecosystem_20261025/`.

The agreed macOS engineering implementation is complete. PRs #43, #47 and #48
qualified the ecosystem, evidence interchange and Polars 2 boundary. PR #49 qualified
Renovate profile discovery and four-profile lock candidates. [PR #51](https://github.com/edithatogo/tobac/pull/51)
merged at `b012758` with all 15 executable PR checks and all 13 receiving-main jobs
passing, including macOS Python 3.15.1, signed artifacts and native graph readback.
Ruff covers maintained Python source, tests and tooling; formatting, five exact preview rules,
process-group resource budgets and two-worker mutation are enforced.

The upstream managed parser's Python 3.15 support remains an unresolved limitation
([dependabot-core #16524](https://github.com/dependabot/dependabot-core/issues/16524)).
Supported dependency submission and graph readback pass; the failed managed parser
is not hidden or marked successful. [Merged PR #41](https://github.com/edithatogo/tobac/pull/41)
implements separate exact-candidate qualification. Published Voiage 3.0.0 acceptance
was completed by PR #104 with `integration/voiage_published_20261102.json`.

[PR #50](https://github.com/edithatogo/tobac/pull/50) qualifies Hypothesis 6.170.9:
all four source-bound locks are regenerated, with complete ecosystem input binding.
Its verification and receiving-main publication are recorded in the PR and
`integration/hypothesis_pr50_20261027.json`; no unexecuted check is implied complete.

Scientific ecosystem reconciliation: [current receipt](../integration/reconciliation_20261102.json).
All six receiving-main workflows at `e88d563` succeeded. Snapshot 117127776
binds that revision and the four unchanged lock hashes; all 115 submitted PURLs
appear in the native aggregate. This establishes resolved inventory coverage.
Package dependency edges, deployment exposure and managed-parser success remain
unqualified. Upstream issue #16524 and PR #16525 remain open as of 2 November.
Earlier queued-run statements are historical, not current implementation blockers.

## Completed work

Completed tracks are archived, including the two-article preparation and
the superseded, withdrawn record-request preparation. No outreach is authorised. See
[the archive index](archive/index.md) for their specifications, plans and dated receipts.

## Research gates

[Open research gates](research-gates.md) retain decision scope, source conflicts,
measurement/covariance, transport, empirical calibration and permissible-use requirements.
M1/M2/M3 computational results are conditional research, not a current national posterior
or a commissioning recommendation. Source/forecast identities and data-once guards remain.

## Deferred development

DXP1 Linux x86_64 audit-lock installation and strict/security execution is complete
on Python 3.15.1. [Actual hosted receipt](../integration/linux_audit_lock_20261103.json).
DXP2 Linux/Windows package portability is complete through actual direct/rebuilt
wheel installation and Unicode/path/metadata checks.
[Hosted package receipt](../integration/package_portability_20261103.json).
DXP3 scientific reproduction is complete on both hosts: all eight variants,
82 tables and the 29-table isolated publication replay pass.
[Scientific reproduction receipt](../integration/scientific_reproduction_20261103.json).
Seven tasks remain deferred, including DXP4 manual release and lock generation.

[Roadmap](roadmap.md): non-macOS release/numerical qualification, optional advisory promotion and explicitly optional
mutation/source-style follow-ups. Existing hosted checks and full-SHA pins remain required.

## Issue #3 bounded pathway implementation

The source-feasibility audit and prospective matched-consumption protocol are implemented
and self-reviewed at 0bdb6ad, with final review fix 4c1f818. [Completed plan](archive/m2_matched_evidence_20261027/plan.md).
The applied issue remains open: all eight matched consumption cells are missing,
with no causal/empirical posterior or deployment acceptance. Current requirements
remain in [research gates](research-gates.md) and issue #3.

## Issue #3 evidence synthesis and partial identification

The bounded source/method phase is complete at `c8af5c1`.
[Archived plan](archive/m2_evidence_synthesis_20261027/plan.md).
Thirteen sources, sharp conditional ratio bounds, native-unit source alternatives,
signed historical uplift sensitivity and conditional study-cost ceilings are
qualified. Existing records,needed target validation and substantive human
decisions are distinguished in [research gates](research-gates.md). Issue #3
remains open;no empirical target posterior or deployment approval is supplied.

## M2 public-source map and traceable extraction

**Status: [x] Complete — bounded public-source map; scientific gates remain.**
Track: `conductor/archive/m2_public_sources_20261027/`.

Searches, citation round, published supplements, extraction and self-review complete
with explicit access limits. See docs/research/M2_PUBLIC_SOURCE_COMPLETION.md.
No requests or model adoption; issue #3 scientific gates remain open.

## M2 conditional publication and value sensitivity

**Status: [x] Bounded implementation and self-review complete.**
Track: `conductor/archive/m2_conditional_publication_20261028/`.

Executed conditional analysis and documentary ethics assessment. Full local five-session
qualification passes; native exact-head/receiving-main acceptance is recorded in the
associated PR. Issue #3 empirical/formal submission-readiness gates remain. No requests/submissions.

## M2 manuscript robustness and publication readiness

**Status: [x] Bounded implementation, self-review and local qualification complete.**
Track: `conductor/archive/m2_manuscript_readiness_20261028/`.

Public-only literature, robustness, manuscript, reporting and fresh-checkout replay.
No requests or submissions; author/formal requirements remain explicit.

All five local Nox sessions pass. Native exact-head/receiving-main acceptance is
recorded in the associated PR after execution. Issue #3 empirical gates remain open.

## M2 two-article development and original-remit assessment

**Status: [x] Bounded development, self-review and local qualification complete.**
Track: `conductor/archive/m2_two_articles_20261028/`.

Distinct MDM research article and NZMJ Viewpoint focused on wastewater, factual
disagreement and conditional decision value. No requests or submissions.

## Native archival provenance and transformation lineage

**Status: [x] Complete for the declared current closure. Phases 1–8 verified.**
Track: `conductor/tracks/native_archival_lineage_20261026/`.

The scoped producer port merged through [archive-govt-nz PR #849](https://github.com/edithatogo/archive-govt-nz/pull/849) at
`a8815d634c9ef5ec6eeb88a3419620f8937b238d`. The reviewed head was
`a5b733d2893e4fcf89fed01c670403b5b4c634db`. A fresh fetch confirmed
ancestry and identical source and test trees. The old #842 branch was not used.

The merged wheel is qualified for the source-reference export. Two independent
replays verified all 38 identities and 43 aliases, with 11 native registrations
for matched originals. P3.3 and P3.4 passed the merged-wheel MOH replay.
P3.1/P3.2 are complete locally at producer 08dc5fed. Phase 5 traced all 140 output files from eight
scientific runner variants and reproduced all 82 numerical tables exactly.
Changing the Phyo source in isolation changed only the longitudinal runner's
scientific input. Phase 6 verified local command enforcement, including rejection
of missing, stale and tampered inputs before launch. Phase 7 restored the declared closure from external USB and replayed
all eight scientific runners offline. P8.1–P8.4 are complete. Producer c76d78df and consumer 14303e4 are published and
verified. Hosted lineage, scientific/test, security and package gates passed.
[Final Phase 8 acceptance](../integration/archive/p8-final-acceptance_20261102.json).
[Phase 7 recovery receipt](../integration/archive/ac13-recovery-receipt.json).
[Phase 6 evidence](../integration/archive/qualified-command-enforcement_20261102.json).
[Phase 5 evidence](../integration/archive/scientific-lineage-checkpoint_20261102.json).
[Source references](../integration/archive/native-source-refs.json).

[Foundations](../docs/engineering/NATIVE_LINEAGE_FOUNDATIONS.md);
[MOH consumer checkpoint](../docs/engineering/MOH_NATIVE_LINEAGE.md). Phase 4 is complete at implementation `d2a04f5`: the MOH workbook and a second SHINE Table 2 operation each emit actual native CAS objects and strict transformation/validation records through the frozen producer wheel, with four-parent ancestry for SHINE and negative controls. 72 affected extraction/workstream tests and both native sessions pass under Python 3.15.1. The 145-item dataset accounting is regenerated with zero blocked items. At the Phase 4 checkpoint, native source registration, graph closure and independent preservation were still open. Those Phase 4 flags remain historical. Final Phase 8 accepts the declared native runner closure. Scientific qualification retains its separate requirements. Hosted checks apply to each publication. Public-source-only and no-request constraints continue to apply.

## Hosted Linux and Windows test qualification

The cross-platform test workflow was qualified on PR #66 source commit `b05d0b5`:
GitHub run 40712230697 passed on Python 3.15.1 with 1,056 passed / 13 skipped on
Ubuntu and 1,041 passed / 28 skipped on Windows, each with 92% coverage. Linux used
the process-group RSS guard; Windows used the hosted job timeout. Existing macOS
and security checks remain in place. This evidence does not qualify the unexecuted
platform-specific release or research jobs.
