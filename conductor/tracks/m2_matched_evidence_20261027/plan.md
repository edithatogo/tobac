# Implementation plan

Status: [~] in progress; owner authorised implementation and review.

## A: Decision and source qualification
- [x] Refresh legal/policy and current evidence sources; retain unavailable raw captures.
- [x] Specify contrast, population/products, relative windows, actions and counterfactual.
## B: Executable evidence pathway
- [x] Add failing tests for unmatched cells, scope/product mismatches and data reuse.
- [x] Implement metadata audit reusing Scope and existing source identity helpers.
- [x] Record real-source feasibility and identifiability limits without empirical fitting.
## C: Verification and review
- [ ] Run affected/integration/full tests, strict checks and numerical reproduction.
- [ ] Self-review by file, apply fixes and record exact verification and gaps.
- [ ] Commit bounded work and update Conductor, retaining empirical issue #3 open.
