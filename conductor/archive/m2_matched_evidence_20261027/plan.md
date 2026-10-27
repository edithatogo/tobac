# Implementation plan

Status: [x] bounded source-feasibility/protocol implementation and review complete.
Applied empirical acceptance for issue #3 remains open in conductor/research-gates.md.

## A: Decision and source qualification
- [x] Refresh legal/policy and current evidence sources; retain unavailable raw captures.
- [x] Specify contrast, population/products, relative windows, actions and counterfactual.
## B: Executable evidence pathway
- [x] Add failing tests for unmatched cells, scope/product mismatches and data reuse.
- [x] Implement metadata audit reusing Scope and existing source identity helpers.
- [x] Record real-source feasibility and identifiability limits without empirical fitting.
## C: Verification and review
- [x] Run affected/integration/full tests, strict checks and numerical reproduction.
- [x] Self-review by file, apply fixes and record exact verification and gaps.
- [x] Commit bounded work and update Conductor, retaining empirical issue #3 open.

## Execution and remaining gaps

Implementation: 0bdb6ad; registration: 8817e80. Receipt:
integration/m2_matched_pathway_20261027.json. All five final Nox sessions pass:
950 tests/five capability skips, 92% coverage; 805 M2 invariants and 482 retained
numerical comparisons pass. Self-review: docs/reviews/2026-10-27-m2-matched-pathway.md.

The real-source audit returns blocked with all eight matched consumption cells missing.
No posterior is updated. Current legal delivery/counterfactual, source transport,
field assay/measurement, mitigation/replacement, incremental crime, monetary costs,
held-out prediction and Māori governance remain empirical requirements. This archive
closes only the bounded software/protocol scope; it does not close issue #3.
Hosted exact-head and receiving-main results are maintained in the publication PR.
