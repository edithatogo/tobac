# Review Report: Scientific ecosystem modernisation

## Summary

The bounded blocker recheck confirms an external service gate; local status and
context-selection fixes preserve the implementation and its existing acceptance evidence.

## Verification Checks

- [x] **Plan Compliance**: Partial for whole-track closure; the local implementation
  remains complete, but the original managed root-parser gate stays unchecked.
- [x] **Style Compliance**: Pass; dated evidence is retained and current statements
  distinguish source, native inventory, hosted checks and managed-service acceptance.
- [x] **New Tests**: No new executable implementation; existing context, dependency
  snapshot and cross-workstream contracts are the affected verification scope.
- [x] **Test Coverage**: Full local suite, 92% branch-inclusive source coverage;
  exact-base hosted evidence is reused for unchanged numerical, clean-package,
  recovery and security behavior.
- [x] **Test Results**: 1,063 passed, 13 capability skips; Nox tests succeeds on
  actual repo-local Python 3.15.1. Resource guard exits 0 at sampled peak 739.4 MiB.
  The full suite includes `tests/test_workstream_integration.py`. A final focused
  context/snapshot/archive/integration run passes 55 tests (exit 0, 118.1 MiB
  sampled peak). [Local receipt](../../integration/ecosystem/managed-parser-local_20261029.json).

## Findings

### Low: engineering context selection exceeded its own budget — fixed

- **File**: engineering/context/engineering.json.
- **Context**: Building the selected profile failed at its unchanged 80,000-byte
  budget. Historical readiness content and the full Nox configuration together
  exceeded that selection budget. Truncation would conceal source evidence.
- **Suggestion applied**:
```diff
-    "docs/engineering/READINESS.md",
```
  Keep readiness as a separately read workflow reference; retain required ownership
  contracts, library review, Nox and active package/lint configuration. The narrowed
  actual profile builds successfully. The budget and builder behavior are unchanged.

### Low: track index still described implementation as in progress — fixed

- **File**: conductor/tracks/scientific_ecosystem_20261025/index.md.
- **Context**: The index contradicted the current registry and metadata, which
  correctly distinguish completed local implementation from external acceptance.
- **Suggestion applied**:
```diff
-**Implementation and review in progress; authorised 26 October 2026.**
+**macOS implementation reviewed and complete; external managed-parser acceptance blocked.**
```
  Updated the dated receipt and review pointers without replacing older evidence.

### Medium: publication inventory omitted the new technical receipts — fixed

- **File**: engineering/publication-policy.json.
- **Context**: The ordinary pre-push hook rejected the three new technical
  review/evidence paths as unreviewed. No push or PR succeeded on that attempt.
- **Suggestion applied**: inspect the exact new technical files and add only those
  three paths to the existing inventory. Preserve all local-document hashes,
  gitlink pins, baseline and scanner behavior. Correct the unpublished owned commit
  so every outgoing tree passes; a later commit alone would leave an invalid tree.

## Evidence and review scope

Reviewed the complete bounded delta from main `428bced`, including every Conductor
change, context selection, ownership entry and native recheck receipt. Existing
implementation batches and their reviews were reused rather than reviewed again.
No scientific formula/input/output, dependency/lock, interpreter, workflow/security
setting, authentication binding or archive-producer object changes.

[Native recheck](../../integration/ecosystem/managed-parser-recheck_20261029.json):
upstream main `ba14f49` still lists through 3.14.9; PR #16525 is unmerged.
Latest root-inclusive run 40446023419 remains a historical failure, with no new
current-head root job executed. Supported snapshot 115443786 binds exact main
`428bced`; all 113 submitted PURLs are in the native 126-PURL inventory. All four
lock files match committed bytes and submitted hashes. All 16 native checks at
the checked base pass. These are separate observations, not root-parser success.

The failed context build was retained as a failed attempt. The existing review
profile and subsequently narrowed engineering profile built without increasing
the byte budget. Final context is rebuilt when tracked inputs or HEAD change.

## Disposition

No unresolved local review finding remains. Whole-track completion remains blocked
on deployed upstream support, fresh native root-inclusive success at unchanged
requirements and reviewed inputs, and receiving-identity/graph readback. Keep the
track active and unarchived. No service mutation, request or external outreach
was performed to bypass that gate.
