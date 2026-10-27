# Implementation plan

Status:[x] bounded evidence/method implementation and review complete; empirical issue#3 remains open.

## A: Evidence synthesis
- [x] Review primary retail-policy, assay/yield and existing administrative sources.
- [x] Record source extraction, shared-data/transport limits and access outcomes.
## B: Partial identification
- [x] Write failing analytic, independent-oracle and invalid-input tests.
- [x] Implement sharp marginal ratio bounds and native-unit supply reconciliation.
- [x] Produce source-bound real-data limits, synthetic sensitivity and conditional VOI summaries.
## C: Review and qualification
- [x] Review every changed file, apply fixes and preserve original results/receipts.
- [x] Run targeted/integration/full tests, strict checks, reproduction, clean-package and security.
## D: Publication
- [x] Commit/archive bounded work and prepare guarded publication with mandatory exact-head macOS and receiving-main verification.
- [x] Record only residual data-access, new-measurement and human-decision requirements.

## Qualification and publication boundary

Commits: 77d5e34 registration,366f37b initial implementation,c8af5c1 added primary
cost/source-arithmetic review. Current receipt: integration/m2_evidence_synthesis_20261027.json.
All five Nox sessions pass:981 tests/five skips,92% coverage;153 targeted/integration
cases,805 M2 invariants and 482 retained-table comparisons pass. Peak 815.1MiB.
Review:docs/reviews/2026-10-27-m2-evidence-synthesis.md. Thirteen primary/documentary
records retain access/estimand/transport limits;no target likelihood or prior adopted.

The archive closes source/method/software work only. Final-head hosted checks,guarded
merge and receiving-main proof remain mandatory publication gates and are recorded
in the PR;no unexecuted outcome is claimed here. Residual data/source-owner/human
requirements remain in evidence/m2/synthesis_20261027.json and research-gates.md.
