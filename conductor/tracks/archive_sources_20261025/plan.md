# Bounded source-to-observation consumer handoff

- [x] Reconcile PR #21 with current main; preserve archival receipts and scientific payloads.
- [x] Bind source aliases, input hashes, row identities and existing Scope/SupplyBasis contracts.
- [x] Report missing capture, scope, product, transport, likelihood and covariance qualifications.
- [x] Detect shared MOH/NZHS data, overlapping periods and previously conditioned IDs.
- [x] Test derived-role rejection, ambiguous/changed inputs and unsupported independence.
- [x] Execute full tests, strict checks, scientific reproduction and package build on macOS Python 3.15.1.
- [ ] Publish the reconciled consumer change and verify exact-head hosted outcomes.

Scientific qualification remains open. Raw-object acquisition, remote archive recovery and the
broader native archival lineage plan are outside this bounded consumer implementation.

Executed local evidence: `integration/archive/handoff-verification_20261026.json`.
