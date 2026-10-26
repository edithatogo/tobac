# Bounded source-to-observation consumer handoff

- [x] Reconcile PR #21 with current main; preserve archival receipts and scientific payloads.
- [x] Bind source aliases, input hashes, row identities and existing Scope/SupplyBasis contracts.
- [x] Report missing capture, scope, product, transport, likelihood and covariance qualifications.
- [x] Detect shared MOH/NZHS data, overlapping periods and previously conditioned IDs.
- [x] Test derived-role rejection, ambiguous/changed inputs and unsupported independence.
- [x] Execute full tests, strict checks, scientific reproduction and package build on macOS Python 3.15.1.
- [x] Publish the reconciled consumer change and verify exact-head hosted outcomes.

Scientific qualification remains open. Raw-object acquisition, remote archive recovery and the
broader native archival lineage plan are outside this bounded consumer implementation.

Executed local evidence: `integration/archive/handoff-verification_20261026.json`.

PR #21 merged at `cf8295b5c1b649685ba78f4977ec7f1b5883d1a8` after 15/15 checks passed at `752436646da5a97f45bef38088f49ac4a2d39d2b`.
