# Native archival provenance and transformation lineage

Status: **new** — specification and plan approved; implementation unstarted.
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

The plan contains eight phases and 32 unstarted primary tasks, mapped to all 14
acceptance criteria. `archive-govt-nz` owns native archival capabilities; tobac owns
its scientific transformations and consumer integration. Existing file owners
retain their assignments. No duplicate provenance system is introduced.

Coordination: [issue #1](https://github.com/edithatogo/tobac/issues/1).
Runtime implementation requires a separate handoff. Planning approval and
registration do not constitute native execution, scientific or archival acceptance.

Integration note, 29 October 2026: this plan was transferred from its isolated
planning branch. Its baseline and producer interfaces must be reconciled against
current revisions before implementation. Current user direction permits public
sources only and prohibits requests, contacts, access applications and submissions;
older plan language does not override that direction. Issue #1 is historical.
