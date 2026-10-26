# Archival source integration

Status: consumer bindings reconciled; bounded handoff implemented, bounded consumer software complete and hosted-qualified; scientific qualification open.

Base: `59bb0e4ebaf1881158849df1702a1d3101aad58f`.
Owner scope: `integration/archive/`, consumer handoff script/schema, documentation and tests.
Preserve other workstreams and scientific gates. Issue #1 is historical provenance.

- [x] Inventory four bibliography collections and exact source aliases.
- [x] Map preserved and active input CSVs without changing values or scientific status.
- [x] Bind archive CAS/WARC fixity and explicit retrieval/identity outcomes.
Original-source acquisition remains partial and outside this bounded consumer implementation.
- [x] Publish draft consumer PR #21; 614 full tests and final 30 focused tests passed.
Companion archive publication and remote raw-object recovery are not claimed here.

Current implementation: [plan](plan.md), [metadata](metadata.json),
[consumer guide](../../../docs/SOURCE_OBSERVATION_HANDOFF.md).

PR #21 receiving commit: `cf8295b5c1b649685ba78f4977ec7f1b5883d1a8`; all 15 PR checks passed.
