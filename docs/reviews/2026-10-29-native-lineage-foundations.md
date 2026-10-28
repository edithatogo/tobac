# Review Report: Native archival lineage foundations

## Summary

The Phase 1 consumer inventory and frozen native capability assessment preserve
scientific meaning and expose producer gaps; full hosted qualification is required
before publication acceptance, following an interrupted local full-suite attempt.

## Verification Checks

- [x] **Plan Compliance**: Partial for the full track; Phase 1 addresses revisions,
  inventory, capability mapping and the requirements checkpoint. Later phases remain open.
- [x] **Style Compliance**: Pinned Ruff lint and formatting pass on changed code.
- [x] **New Tests**: Inventory coverage, unknown-source preservation, missing-input
  rejection, immutable Git-source loading and receipt preservation.
- [x] **Test Coverage**: Focused source-handoff/probe and workstream tests executed:
  57 passed before the final receipt-preservation additions. Whole-source typing
  passed with zero errors/warnings using the explicit qualified interpreter path.
- [ ] **Test Results**: Local full Nox run interrupted with exit 138. No full-suite,
  coverage, reproduction, package, security or recovery success is inferred from it.
  The PR's required hosted jobs must pass before merge; final hosted results are
  retained in that PR and the receiving commit's checks.

## Findings

### Medium: fixed Nox receipt paths conflicted with evidence preservation — fixed

- **File**: `noxfile.py`, source-handoff/reproduction sessions.
- **Context**: Refusing receipt overwrite would make repeated qualification fail
  on an old fixed filename. The previous writer could also replace earlier evidence.
- **Resolution**: Each invocation now uses a fresh UUID receipt path. Both CLIs
  refuse existing outputs, with explicit preservation tests.

### Medium: metadata coverage could be mistaken for native lineage — bounded explicitly

- **Files**: `scripts/source_handoff.py`, native diagnostic and engineering checkpoint.
- **Context**: Source hashes, record schemas and synthetic fixtures do not establish
  real native object closure, empirical calibration or independent observations.
- **Resolution**: Inventory/probe receipts explicitly leave native and scientific
  qualification false. Source aliases/dependencies remain under the existing register.
  The inventory is a coverage superset rather than an executed dependency graph.

### Open producer requirements

The frozen native probe accepts duplicate objects and incomplete transformation
receipts, rejects a valid strict transformation record at the manifest boundary,
and produces a WARC without a capture date. Source URI/schema and actual-object
closure requirements are mapped separately. These are not fixed by a consumer
schema bypass or a second provenance engine. The producer has an active owner;
the inspected working tree and native estate remain unchanged.

## Qualification boundary

The local SIGBUS event is retained in
`integration/archive/lineage-local-interruption_20261029.json`. Its cause is not
established. No owned descendants remained, and no failed run was relabelled as
a pass. Full qualification continues on the existing hosted platform jobs.
No requests, contacts, captures, scientific input changes or submissions occurred.
