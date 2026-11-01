# Active research tracks

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
implements separate exact-candidate qualification; published-3.0 acceptance remains open.

[PR #50](https://github.com/edithatogo/tobac/pull/50) qualifies Hypothesis 6.170.9:
all four source-bound locks are regenerated, with complete ecosystem input binding.
Its verification and receiving-main publication are recorded in the PR and
`integration/hypothesis_pr50_20261027.json`; no unexecuted check is implied complete.

Scientific ecosystem recheck: [receipt](../integration/ecosystem/managed-parser-recheck_20261029.json).
The submission and native inventory readback were verified at source revision `62a4712`;
they do not establish dependency edges or deployment exposure. The subsequent `00fb336`
changes only documentation; its receiving-main CI and new submission were queued at
closure, and remain unverified. Upstream PR #16525 remains unmerged; its parser failure
remains recorded, not reported as a pass.

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

[Roadmap](roadmap.md): non-macOS release/numerical qualification, optional advisory promotion and explicitly optional
mutation/source-style follow-ups. Existing hosted checks and full-SHA pins remain required.

## Voiage 3.0.0 Polars consumer qualification

Status: bounded macOS baseline/candidate implementation complete; published-3.0
acceptance blocked externally.

Track: `conductor/tracks/voiage_polars_qualification_20261026/`.
Published Voiage 3.0.0 remains unavailable; no upstream-release success is claimed.

Current receipt: integration/voiage_polars_consumer_20261028.json. Default producer
2.2.0+tobac3151.2 retained; merged candidate at 65c5e76 is unreleased version
2.2.0. Six caller-buffer isolation cases now supplement 90 numerical comparisons.
The previous 6c28ac5 candidate failed the new ownership probe. pandas/xarray remain
required. Published-3.0 acceptance remains unexecuted; historical proof remains in PR #41.
The 28 October macOS-only direction is historical. PR #66 restored hosted Linux
and Windows runtime tests at Python 3.15.1. Candidate qualification remains on
macOS; the Linux-specific manual locked-release workflows remain deferred. Earlier
platform receipt: integration/macos_ci_scope_20261028.json.

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

**Status: [~] Phase 1 and Phase 4 complete; Phase 2/3 producer receipts implemented locally but unmerged; Phase 5/6 complete; Phase 7 partial; Phase 8 open.**
Track: `conductor/tracks/native_archival_lineage_20261026/`.

The current inventory and frozen producer capability map are implemented (Phase 1). Phase 2/3 producer gap fixes were implemented in a local archive-govt-nz clone (commit 0561947, branch `feat/p2-p3-native-lineage-gaps`): duplicate object ID rejection, complete receipt validation (transformation/validation/publication), WARC-Date header, native URI scheme validation, source register CLI command, record adapter functions. 20 provenance tests pass. All 4 probe gaps resolved: duplicate_object_id, incomplete_transformation_receipt, strict_record_interop (via adapter), warc_capture_date. P2.3 source-binding export migration implemented (script: derive_native_source_refs.py, output: native-source-refs.json). P2.4 phase verification completed (20 tests pass, 4 probe gaps resolved, checkpoint recorded).

**Producer merge status (2026-11-01):** The P2/P3 changes exist in a local archive-govt-nz clone (commit 0561947) but the local repository has no common history with the remote archive-govt-nz main branch (1884 commits diverged). The branch `feat/p2-p3-native-lineage-gaps` was pushed but cannot be opened as a PR due to no common history. Producer merge requires manual intervention by the archive-govt-nz maintainer. See [Producer merge decision](../docs/decisions/native_lineage_producer_merge_20261031.md).

P5 runner provenance integration and P6 fail-closed qualification enforcement are implemented with explicit exploratory/legacy unqualified modes. P5 and P6 receipts record six runner interfaces and ten qualification tests. Native lineage and scientific qualification remain false until the P7 replay and P8 acceptance gates are executed.
[Foundations](../docs/engineering/NATIVE_LINEAGE_FOUNDATIONS.md);
[MOH consumer checkpoint](../docs/engineering/MOH_NATIVE_LINEAGE.md). Phase 4 is complete at implementation `d2a04f5`: the MOH workbook and a second SHINE Table 2 operation each emit actual native CAS objects and strict transformation/validation records through the frozen producer wheel, with four-parent ancestry for SHINE and negative controls. 72 affected extraction/workstream tests and both native sessions pass under Python 3.15.1. The 145-item dataset accounting is regenerated with zero blocked items. Native source registration, graph/cluster closure, per-file chain re-execution and independent preservation remain open; `native_lineage_qualified` and `scientific_qualification` stay false. Hosted checks apply to each publication. Public-source-only and no-request constraints continue to apply.

## Hosted Linux and Windows test qualification

The cross-platform test workflow was qualified on PR #66 source commit `b05d0b5`:
GitHub run 40712230697 passed on Python 3.15.1 with 1,056 passed / 13 skipped on
Ubuntu and 1,041 passed / 28 skipped on Windows, each with 92% coverage. Linux used
the process-group RSS guard; Windows used the hosted job timeout. Existing macOS
and security checks remain in place. This evidence does not qualify the unexecuted
platform-specific release or research jobs.
