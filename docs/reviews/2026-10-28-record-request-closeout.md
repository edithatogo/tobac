# Review Report: record-request preparation closeout

## Summary

The completed preparation is withdrawn under the owner's public-data-only decision;
archival reconciles stale track text without preparing or sending new requests.

## Verification Checks

- [x] **Plan Compliance**: Yes, historical preparation and subsequent supersession preserved.
- [x] **Style Compliance**: Pass, documentary scope and scientific claim discipline retained.
- [x] **New Tests**: No, no executable behavior changed; direct fixity/link/state checks used.
- [x] **Test Coverage**: Existing archive and cross-workstream contracts, 27 passed.
- [x] **Test Results**: Current-state/fixity checks pass with explicitly versioned hashes;
  all 18 Conductor names consistent. Fresh macOS hosted evidence is recorded in the PR.

## Findings

### High: historical specification could be mistaken for renewed outreach authority (fixed)

- **File**: conductor/archive/m2_record_requests_20261027/spec.md
- **Context**: The original specification authorised preparation; PR #56 subsequently
  implemented the owner's public-data-only decision and withdrew every draft.
- **Fix**: Add a current supersession banner and separate the historical specification.
  Machine-readable disposition preserves completed historical work while explicitly
  denying renewed preparation, sending and new OIA authority. No new recipient work,
  correspondence, restricted access, commissioning or collection occurs.

### Medium: one manifest digest identifies a historical document, not current bytes (resolved)

- **File**: requests/m2_20261027/manifest.json
- **Context**: A direct current-file check failed for docs/research/M2_DECISIONS.md.
  The declared digest matches the approved withdrawal snapshot at 0001273; the current
  digest matches the approved conditional-publication update at 4a6246c. All other
  twelve manifest entries still match current files, including every withdrawn draft.
- **Fix**: Preserve the original manifest unchanged. The dated closeout receipt verifies
  all thirteen historical hashes, identifies the twelve current matches, and traces
  the one later document revision. No blind hash refresh or thirteen-current-match
  claim is made. The initial failed assumption is retained in this review.

### Low: completed withdrawn track remained in the active registry (fixed)

- **Files**: conductor/tracks.md, conductor/index.md, conductor/archive/index.md
- **Fix**: Archive the track, repair navigation and update the completed-track count.
  Public-source successors and issue #3 scientific/publication gates remain explicit.

## Verification scope

The four drafts, field schedule, decisions, manifest, research evidence, source code,
model inputs, dependency locks, workflow definitions and security settings are unchanged.
No product-purpose, stack or branding update is warranted. Current checks used the
actual repo-local Python 3.15.1 and the existing 4 GiB/40-minute process-group guard;
27 tests passed at 119.4 MiB sampled peak. The name checker reports 18/18 consistent.
Direct checks validate thirteen historical hashes, twelve current hashes, four
withdrawn/unsent declarations and navigation links; these do not establish a live
send-prevention control, custody, empirical identification or publication permission.

Unchanged full-software/numerical evidence from main a1d621e is retained with its
original scope. New exact-head and receiving-main macOS checks and artifacts must
execute before their results are recorded in the closeout PR. Archive completion
cannot close issue #3 empirical or author/formal submission-readiness gates.
