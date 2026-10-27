# Implementation plan

Status: [x] Bounded implementation and self-review complete; native publication acceptance is recorded in its PR. Base:e35b5abc5bf184c66b8d5c7540735bd0175f15ed.

## A: Protocol and source boundaries
- [x] Freeze dated conditional aim,normative supports,claim boundary and existing analyses.
- [x] Verify public ethics/reporting sources and source-to-parameter eligibility map.
- [x] Phase verification:source identities,scope and no-contact boundary.

## B: Computation
- [x] Write numerical/invalid-input/tie/dominance/threshold regression tests.
- [x] Implement consequence weighting and exact frontier/continuous-box checks.
- [x] Cross existing structural cases with values;compute conditional EVPI,groupEVPPI,EVSI.
- [x] Add source-bound runner,output manifest and Nox reproduction.
- [x] Phase verification:targeted tests and independent oracle.

## C: Publication and ethics assessment
- [x] Execute full declared analysis;generate tables/figures and substantive findings.
- [x] Write source/method/limitations and desk ethics/governance assessment.
- [x] Reconcile public-only directions and retain empirical issue#3 gates.
- [x] Phase verification:claim-to-output review and reproducibility.

## D: Review and publication to repository
- [x] Iterative self-review,apply fixes and run full bounded five-session qualification.
- [x] Prepare reviewed repository publication with exact-head hosted checks, guarded merge and receiving-main readback required; native outcomes are recorded in the associated PR.
- [x] Record implementation commits, verification scope, remaining gaps and interfaces; archive bounded work with native acceptance retained separately.

No requests or submissions. Repository PR/merge is explicitly authorised;external
research/journal/ethics submissions are not. No independent-review gate.

Protocol amendments after the first pilot are explicit:fixed-target EIG diagnostics
and2/4/8-node finite-resolution checks,with primary4node analysis unchanged.
Initial17unit tests passed;current53component/integration tests pass. Source/metadata
regression checks,field applicability and external approvals remain distinct.


## Implementation and review evidence

Implementation: fb997b3. Numerical/source-role fixes: 5371fea. Ethics/figure fixes:
cc2fbd1. Final SVG serialization fix: 7990b78. The refreshed executed snapshot uses that
computational commit; subsequent
manuscript/Conductor commits do not relabel it. All declared input/output hashes
verify. 125 profiles, 750 study values, 875 grouped-information rows, 90 EIG rows,
19 isolated primary-grid switches; 2/4/8-node diagnostics retain the one coarse-grid
gross-design tie change. No continuous-convergence or empirical-validity claim.
Primary analysis initial peak 503.8 MiB; final SVG-normalised replay 586.9 MiB,
both exit 0. Every numerical CSV, report value and PNG is unchanged; all six SVGs
parse and have clean whitespace. Sampled RSS is not leak proof.
53 targeted component/integration tests passed. The full qualification found the
missing mandatory workstream-contract path in the new context profile; this was
corrected without changing its test or budget. Final local/native outcomes follow.


## Final local acceptance and native publication protocol

Local macOS Python 3.15.1 qualification: tests 1008 passed / 5 capability skips,
93% coverage. strict_all (ALL Ruff/format; BasedPyright zero errors/warnings),
reproduce (existing M1/M2/M3, longitudinal and new 2/4/8-node analysis),
clean_package and security all pass. Initial five-session run peak 728.2 MiB;
its context-profile failure is retained in m2-publication-local.log. Focused cached
rerun: 1 passed / 10 deselected. Final complete tests session peak 671.3 MiB,
exit 0. No limit changed: 4096 MiB sampled group RSS, 2400 seconds. These are
sampled resource observations, not a memory-leak proof.

New interface: additive consequence/value-sensitivity module and fixed-protocol
publication CLI; no shared evidence, M3, original consequence/core, runtime dependency
or security-check semantics changed. Package manifest binds 60 files; all primary
and nested run hashes verify. Review: docs/reviews/2026-10-28-m2-conditional-publication.md.
Scientific and formal submission-readiness limits remain in research-gates.md.

Repository acceptance is recorded in the associated PR on branch
codex/m2-conditional-publication-20261028: verify exact reviewed head and every
executable PR check, merge with expected-head protection, then read receiving-main
jobs, numerical qualification artifact, accepted graph snapshot and signed package
provenance. This archive records completed local work; it does not predeclare any
unexecuted native check or merge successful. Owner's autonomous task continues
through that native acceptance; no request or journal/ethics submission is authorised.


Final post-SVG five-session qualification also passes in full on macOS Python
3.15.1: tests 1008 passed / 5 capability skips, 93% coverage; strict_all, reproduce,
clean_package and security pass. Guard peak 806.0 MiB, exit 0, unchanged 4096 MiB /
2400-second limits. Log: outputs/engineering/m2-publication-qualification-final.log.
Final refreshed analysis is bound to computational commit 7990b78, not the earlier
cc2fbd1 snapshot. All numerical CSVs, scientific report values and PNGs are unchanged;
SVG whitespace is normalised and XML parses. Final asset-inclusive diff-check passes.
Native publication acceptance: https://github.com/edithatogo/tobac/pull/58.
