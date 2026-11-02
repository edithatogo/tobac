# Reconciled repository status — 2 November 2026

No implementation track is in progress. The retained native-lineage track has
**8/8 phases and 32/32 primary tasks complete**, with zero in progress or pending.
The 18 archived tracks have no active execution tasks. Five historical graph
proposal entries were superseded by bounded inventory acceptance and are explicitly
labelled historical in their archived plan, rather than marked as executed.

## Verified baseline

Consumer receiving main `e88d56366c512df3e71243ac341722bb3a52e1ae` and producer
receiving main `c76d78df37ffa89469e8fca5f2db521553525276` were read back on
2 November. All six consumer receiving-main workflows succeeded. The functional
consumer implementation is `14303e4`; `e88d563` records its Conductor closeout.
[Reconciliation receipt](../integration/reconciliation_20261102.json).

[Native lineage](tracks/native_archival_lineage_20261026/plan.md) closes P1.1–P8.4
and AC01–AC14 for the declared eight-runner closure. The independent USB restore,
interruption recovery, installed replay, hosted verifier and guarded publications
are verified in [final acceptance](../integration/archive/p8-final-acceptance_20261102.json).
Published Voiage 3.0.0 qualified in [PR #104](https://github.com/edithatogo/tobac/pull/104)
and its [receipt](../integration/voiage_published_20261102.json).

Snapshot 117127776 binds `e88d563` and all four committed lock hashes. All 115
submitted PURLs appear in the native 128-PURL aggregate. This is resolved package
inventory coverage. Native package edges, deployment exposure and managed-parser
success remain unqualified. Upstream issue #16524 and PR #16525 are still open.
The archived ecosystem's queued receiving-main and Voiage release gates are resolved.

## Remaining deferred phases and tasks

These are roadmap commitments pending prioritisation, with no task in progress.
There are **three deferred work groups/phases and ten pending tasks**; the advisory
lane is the one existing deferred track. Platform and hardening groups remain in
[the roadmap](roadmap.md), rather than newly registered implementation tracks.

| Group / phase | Tasks remaining |
| --- | --- |
| Cross-platform release and numerical qualification | DXP1 — install/execute the source-bound Linux audit lock on qualified Python 3.15; DXP2 — qualify non-macOS package paths, markers, encodings and release behavior; DXP3 — execute platform-specific scientific reproduction; DXP4 — reconsider and requalify deferred manual release/lock-generation workflows. |
| Advisory CI/CD lane | DCI1 — select nonduplicative additions and current pins; DCI2 — implement selected advisory commands/workflow/ARM leg; DCI3 — execute local and hosted qualification; DCI4 — guarded publication and receiving-ref verification. [Plan](roadmap/cicd_hardening_20261025/plan.md). |
| Optional macOS hardening | DH1 — triage the 12 surviving supply mutants from the dated 119/131 measurement; DH2 — review retained source/API Ruff exceptions where behavior and scientific meaning are preserved. |

Linux/Windows runtime tests and hosted lineage verification already passed.
Those outcomes do not qualify their platform-specific release, audit or numerical
jobs. Mutation counts are dated evidence, not a fresh current mutation result.

## Open dependency maintenance

These PRs are outside the completed research tracks. Exact checked candidate SHAs
and check counts are retained in the reconciliation receipt. All three are blocked
by failing checks; no update is merged or marked qualified here.

| PR | Remaining task |
| --- | --- |
| [#80](https://github.com/edithatogo/tobac/pull/80) — verified action pins | Diagnose the candidate's failures, qualify updated pins against all required checks, then guarded publication and receiving readback. |
| [#91](https://github.com/edithatogo/tobac/pull/91) — Python Docker 3.15.2 | Qualify the newer patch consistently across runtime/build/test/CI and the pinned verifier runtime contract before promotion; the current executed baseline remains 3.15.1. |
| [#94](https://github.com/edithatogo/tobac/pull/94) — pytest-gremlins 1.13.1 | Diagnose failures and qualify the tool/locks and required checks before promotion. |

## Scientific and submission requirements

[Research gates](research-gates.md) retain the selected target/legal/counterfactual
facts, source year/unit/channel reconciliation, physical conversions, matched
consumption/measurement and covariance records, source-to-target transport,
policy/biomarker calibration, Māori governance/permissible use/current costs,
and held-out empirical validation. All eight matched consumption cells remain
unavailable. Issue #3 remains open. No empirical national posterior or policy
acceptance follows from software qualification.

Historical capture timestamps and archive coverage beyond the declared runner
closure remain limited. AC13's completed independent restore is no longer an open
current-closure requirement. Remote/wider-estate recovery is separately owned.

The MDM article and NZMJ Viewpoint still require author facts, contributions,
affiliations, actual funding/interests, personal final approval and applicable
institutional/cultural/journal determinations. Public-only/no-request constraints
continue. No external requests, submissions, registrations or deposits are authorized
by this status reconciliation.

## Decision drafts and Git disposition

All three November 1 drafts are retained as superseded historical proposals,
with current acceptance links, original-draft digests and unverified approval
placeholders identified. They create no pending wheel rebase, placeholder source-ID,
media-format or recovery task.

- [Phase 5/6 sequencing](../docs/decisions/phase5_6_sequencing_20261101.md)
- [Phase 5/6 implementation](../docs/decisions/phase5_6_implementation_20261101.md)
- [AC13 independent-copy recovery](../docs/decisions/ac13_independent_copy_recovery_20261101.md)

There is one consumer worktree. Existing non-ancestor local branches are preserved
historical/superseded lanes, including the saved divergent former main. No changes
are discarded or silently merged. The only open repository PRs at this checkpoint
are the three dependency candidates above. This reconciliation changes documentation
and the exact public-path inventory only; scientific inputs, outputs, runtime,
locks, native objects and private authority remain with their existing owners.

## Reconciliation verification

The track-name check passes for all 20 registered track records. All Conductor
metadata JSON parses, and local Markdown targets in the current public status
records resolve. Intentionally excluded manuscripts and requests are explicitly
labelled local-only. The focused archive, publication-boundary and cross-workstream
suite passes 41 tests on repository-local Python 3.15.1 under the 4 GiB/40-minute
guard. Scientific/runtime source is unchanged; the full executed receiving-main
qualification is reused at its exact baseline. The final publication guard and
receiving-ref readback are recorded with the reconciliation commit.
