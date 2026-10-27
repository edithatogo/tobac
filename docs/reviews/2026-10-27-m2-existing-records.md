# Review Report: M2 existing-record assessment

## Summary

The assessment is ready for publication after correcting uncertainty and access claims;
empirical issue #3 acceptance remains open.

## Verification Checks

- [x] **Plan Compliance**: Yes — review the existing-record assessment, apply fixes,
  qualify macOS Python 3.15.1 and publish with a guarded merge. Owner decision options
  are recommendations, not silently adopted instructions.
- [x] **Style Compliance**: Pass — Conductor context and style guides reviewed;
  scientific claims, assumptions and substantive decisions remain distinct.
- [x] **New Tests**: No — changes are documentary evidence and a static assessment
  ledger, with no executable interface or model changes. Adding a mirror test would
  not establish source applicability. Exact arithmetic, source hashes, IDs and null
  semantics were checked directly.
- [x] **Test Coverage**: Yes for software — 92%; this does not validate field inference.
- [x] **Test Results**: Passed — local full suite: 981 passed, five capability skips.
  `tests`, `strict_all`, `reproduce`, `clean_package`, `security` all passed.
  Strict diagnostics: zero errors/warnings; nine native Ruff policy tests passed.

## Findings

### Medium — Unknown collection requirement encoded as false (fixed)

- **File**: `evidence/m2/existing_records_20261027.json`
- **Context**: A machine consumer could interpret false as evidence that no collection
  is required, although suitability of inaccessible raw records is unknown.
- **Fix**: Schema version 2 uses null with explicit undetermined status and semantics.
  Repository search found no executable consumer of this assessment field.

### Medium — Availability offer conflated with required raw-field coverage (fixed)

- **Files**: assessment, source ledger and Conductor research gates.
- **Context**: Authors offering data does not establish delivery of raw assays, QC,
  paired observations, flow denominators or retained aliquots. A dated NZHS route
  description is not a current refresh inventory.
- **Fix**: Raw-field coverage/current refresh remain unverified; complete sample
  pairing is not inferred from the weekday/weekend design. Conditional/no-study
  analysis remains permissible without additional empirical collection.

### Low — Cited sources absent from ledger and decisions too abstract (fixed)

- **Context**: The assessment cited showcards and returns outside its seven-source
  follow-on ledger and left owner choices dispersed across residual requirements.
- **Fix**: Nine source IDs now cover those citations with access modes and assessment
  dates; a separate owner decision register states recommended and alternative paths,
  consequences and non-adoption. Acronyms are expanded for standalone reading.

## Execution and publication evidence

Base main: `b5155ca49803e07e7022211b6dec9e8b83b13756`.
Original assessment: `b20f6b14e4ab02118108badd9894016d51a0f495`.
Reviewed every changed assessment/ledger/gate file and the new decision register.
Rechecked official survey access and Cabinet release sources in the review turn.
No unresolved correctness finding remains within this bounded documentary scope.

Actual repo-local interpreter: `.nox/tests/bin/python`, Python 3.15.1.
Local command:

```sh
.nox/tests/bin/python scripts/run_bounded.py --timeout 2400 -- uvx --python .nox/tests/bin/python --from nox==2026.10.20 nox -r -s tests strict_all reproduce clean_package security
```

Log: `outputs/engineering/m2-records-review-local.log` (ignored local evidence).
Owned group sampled peak 744.9 MiB, exit 0 under default 4096 MiB/2400 seconds.
The run executed the final substantive changes; subsequent edits only reflowed prose
and refreshed its hash, added this review record and the owner decision register.
Exact fee arithmetic, eight local content hashes, nine unique source IDs, null status,
core Conductor files and 13/13 track-name consistency passed direct verification.
No model, source input, library pin, security setting, tolerance or workflow changed.
Original untracked `.DS_Store` files are excluded from publication.

Exact-head hosted checks, guarded merge and receiving-main readback are recorded in
this publication's PR. They are separate from local test evidence and from empirical
acceptance. No external request or new data collection is authorised by these files.
