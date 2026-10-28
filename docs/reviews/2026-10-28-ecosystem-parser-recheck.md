# Review Report: Scientific ecosystem modernisation

## Summary

The local macOS implementation remains qualified; current-status and evidence fixes
are applied, while the genuinely external managed root-parser gate remains blocked.

## Verification Checks

- [x] **Plan Compliance**: Yes for the bounded blocker recheck and remediation;
  the original external acceptance task stays unchecked rather than falsely closed.
- [x] **Style Compliance**: Pass; factual status updates preserve dated evidence and
  distinguish local, hosted, native inventory and external-service acceptance.
- [x] **New Tests**: No new executable behavior; existing full suite, snapshot/source
  contracts and integration tests executed. No implementation-mirroring tests added.
- [x] **Test Coverage**: Full local suite, 92% branch-inclusive source coverage;
  unchanged scientific/reproduction/package evidence reused from exact main base.
- [x] **Test Results**: 1,030 passed, five capability skips; tests/strict_all/security
  sessions pass, zero typing errors/warnings, no known audited vulnerabilities.

## Findings and applied fixes

### Medium: prevent false external-service completion

- **File**: conductor/tracks/scientific_ecosystem_20261025/metadata.json and plan.md;
  docs/engineering/DEPENDENCY_MAINTENANCE.md.
- **Context**: Current implementation is complete, but the historical root parser
  still rejects the required Python range. Successful snapshot submission and an
  engineering-only parser job cannot establish current root-service acceptance.
- **Suggestion applied**:
```diff
- "status": "in_progress"
+ "status": "blocked"
```
  Retain the unchecked root task, exact historical run/head/error and actual current
  graph coverage. Add closure criteria requiring deployed support and a fresh native
  root-inclusive success at the unchanged constraint, not merely an upstream merge.

### Low: correct stale and misplaced status statements

- **File**: conductor/tracks.md; docs/engineering/LIBRARY_REUSE_REVIEW.md;
  docs/engineering/DEPENDENCY_MAINTENANCE.md.
- **Context**: Archived-track/file counts, unavailable local tools and PR #41's draft
  state were stale. The first new ecosystem summary sat beneath the M2 manuscript
  heading; an old issue #1 coordination statement contradicted current ownership.
- **Suggestion applied**: correct archive count, avoid a stale fixed Ruff-file count,
  scope qualified tool execution to macOS, describe merged bounded candidate work
  without implying published Voiage 3.0 acceptance, move the ecosystem paragraph
  under its own track, and retain issue #1 only as historical context.

## Evidence and review scope

Base 1df7680 (PR #60) through implementation/status commit 3ee5111 and the review
fixes. Reviewed all four non-Conductor files (156 added lines/five removed at the
initial review) and each Conductor diff. No scientific model, source contract,
dependency/lock, package, runtime, security setting or workflow/pin changes.

Latest observed root-inclusive managed run 40446023419 failed at historical head
4ebc4af with tool_version_not_supported; no fresh current-head job is invented.
Pinned upstream main lists through 3.14.9. Open non-draft PR #16525's candidate lists
3.15.2 but is unmerged and not deployed-service proof; the project stays on 3.15.1.
Supported snapshot 115181647 binds reviewed main 1df7680. All 113 submitted PURLs
are in the native 124-PURL export; every lock hash/committed byte is verified.
The first SBOM read returned server-side HTTP500 timeout; one deliberate repetition
of the same read-only target succeeded. Both outcomes and exact source/log hashes
are retained. No stale graph-writing job is rerun or external message sent.

[Native recheck](../../integration/ecosystem/managed-parser-recheck_20261028.json)
and [executed local qualification](../../integration/ecosystem/managed-parser-local_20261028.json).
Resource guard: sampled peak 810.7 MiB, exit 0, unchanged 4 GiB/40-minute budgets.
Unchanged scientific/replay/package/recovery proof at the exact base is reused;
final-head hosted and receiving-main native acceptance is recorded in the associated
PR after execution. None closes the separate managed root-parser service gate.

No unresolved local review finding remains. The track stays externally blocked;
it is not archived, and no unavailable runtime or historical failing job is called
successful. Upstream release/deployment and native root acceptance are required.
