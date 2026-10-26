# Review Report: Scientific ecosystem modernisation and completed tracks

## Summary

The bounded macOS changes preserve reference scientific inputs and reuse the existing producer interfaces; external migration and empirical gates remain explicit.

## Verification Checks

- [x] **Plan Compliance**: Partial - implementation hold released by the owner; phase evidence and unresolved gates are mapped in the active plan.
- [x] **Style Compliance**: Pass - configured Ruff and strict BasedPyright pass; existing style/API exceptions remain explicit.
- [x] **New Tests**: Yes - parameter identity, scenario isolation, recovery, context requirements, security dispositions, archive registration and accounting boundaries.
- [x] **Test Coverage**: Partial - full reference suite/branch coverage and separate native optional-library execution; these establish bounded software evidence.
- [x] **Test Results**: Passed - current executed scopes belong to integration/ecosystem/verification_20261026.json; PR #43 final-code checks and the trusted six-job dispatch passed; four signed subjects were verified downstream.

## Findings

### Medium: Mutation coverage contaminated the reference coverage store

- **File**: noxfile.py
- **Context**: gremlins produced statement-only coverage files alongside branch data, so a passing pytest run failed the coverage gate. This was retained as a failure.
- **Suggestion applied**: give each Nox test execution its own COVERAGE_FILE generation; retain mutation coverage separately.

### Medium: Recovery reused a log filename after a boundary interruption

- **File**: src/tobac/replay.py
- **Context**: an interrupted stage could leave its log before creating its output directory. Exclusive creation of the same log prevented an otherwise safe resume.
- **Suggestion applied**: use immutable unique log generations and test interruption/resumption without overwriting the completed receipt.

### Medium: Root-only parameter validation admitted ignored nested fields

- **File**: src/tobac/parameters.py
- **Context**: an unknown nested constant could be serialized despite having no model effect.
- **Suggestion applied**: require declared constant/measurement/event/axis fields at this serialization boundary; test rejection and an allowed additional scenario.

### Medium: Archival invalidated the active-only registry checker

- **File**: scripts/check_conductor_track_names.py
- **Context**: completed tracks must leave the active registry, but their names and links still need validation.
- **Suggestion applied**: read the archive index as a separate registry and test that archived entries remain verifiable.

### Low: Clean-package location check compared macOS path aliases

- **File**: scripts/qualify_clean_package.py
- **Context**: /var and /private/var represented the same clean environment but failed a lexical path comparison.
- **Suggestion applied**: resolve both the module path and environment prefix; real installed-API/CLI execution passes afterwards.

### Medium: Artifact binding included hidden build metadata outside the upload

- **File**: .github/workflows/engineering.yml
- **Context**: uv created a hidden .gitignore beside the distributions. The manifest included it, but the artifact upload correctly omitted hidden build metadata, so downstream byte verification failed.
- **Suggestion applied**: restrict the digest binding to actual wheel/sdist/SBOM subjects; rerun hosted signing and downstream verification.

---

Review performed sequentially by the implementing agent under conductor-review; it is not independent scientific endorsement. The >300-line iterative review was authorised by the user's autonomous implementation/review instruction. Files were reviewed by responsibility: parameter/model boundary, backend/interchange probe, replay/recovery, clean package, security/workflow, tests and Conductor. Existing completed-track specifications and retained reviews were read before archival. No source value, prior, likelihood or published result was recalibrated. Disk exhaustion and initial failed checks remain in local evidence.

## Native receiving-ref follow-up review

The managed root graph parser rejects Python 3.15 (upstream issue 16524). The supported additive snapshot helper was reviewed as a <300-line change: exact interpreter/HEAD/committed-lock checks, no inferred dependency edges, trusted job-only API permission and preserved existing settings. Six new cases and affected graph/lock/workstream checks pass. API branch acceptance is distinct from default-branch graph readback.

A Windows PR failure exposed a mutation freshness clock-domain mismatch. A deterministic regression reproduces a wall clock ahead of file timestamps. Preparation now records filesystem time, retaining cached-output removal, source/tool hashes, stale-result rejection and score/completeness checks. No retry, tolerance window or waiver was added.
