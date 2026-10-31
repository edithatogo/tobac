# Native archival provenance and transformation lineage

Status: **in progress** — Phase 4 complete (MOH and SHINE source-backed native operations); later replay/acceptance phases and native source registration remain open.
Track ID: `native_archival_lineage_20261026`. Type: Feature.

Trace every current and future dataset through native archival preservation,
extraction, transformation, scientific execution and results. Preserve legacy
records with explicit unknown/reconstructed lineage; enforce valid lineage for
qualified runs while retaining labelled exploratory and legacy execution.

- [Approved specification](spec.md)
- [Approved implementation plan](plan.md)
- [Metadata and ownership](metadata.json)
- [Maintainer approvals](approvals.json)
- [Registration validation](registration-validation.json)

The plan contains eight phases and 32 primary tasks, mapped to all 14
acceptance criteria. `archive-govt-nz` owns native archival capabilities; tobac owns
its scientific transformations and consumer integration. Existing file owners
retain their assignments. No duplicate provenance system is introduced.

Coordination: [issue #1](https://github.com/edithatogo/tobac/issues/1).
The original planning approval required a separate implementation handoff. Planning approval and
registration do not constitute native execution, scientific or archival acceptance.

Implementation handoff: the maintainer's 29 October instruction to proceed
authorises this track. Tobac owns the current consumer changes; the archive
producer has a separate active writer and is inspected at frozen committed
revisions only. No producer edits, requests or external submissions are included.

Integration note, 29 October 2026: this plan was transferred from its isolated
planning branch. Its baseline and producer interfaces must be reconciled against
current revisions before implementation. Current user direction permits public
sources only and prohibits requests, contacts, access applications and submissions;
older plan language does not override that direction. Issue #1 is historical.

Phase 1 checkpoint: [capability and inventory map](../../../docs/engineering/NATIVE_LINEAGE_FOUNDATIONS.md).
Four foundation tasks are complete; 28 native implementation/acceptance tasks remain.
The foundations local interruption remains historical. The consumer checkpoint
now records 1084 passing tests, strict/package/security/clean-package checks and
clean-source numerical replay. Required hosted checks remain the publication gate.

Consumer checkpoint: [actual MOH native extraction](../../../docs/engineering/MOH_NATIVE_LINEAGE.md)
and [execution summary](../../../integration/archive/moh-native-extraction_20261029.json).
P4.1/P4.2 are partial; complete native archival lineage remains unqualified.

Recovery continuation: [capture and same-device native rehearsal](../../../integration/archive/moh-recovery-rehearsal_20261029.json). The earlier private receipts are absent from the restored worktree; a new attempt and retained local copy do not satisfy independent preservation or native closure.
