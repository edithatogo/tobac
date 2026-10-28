# Review Report: M2 manuscript robustness and publication readiness

## Summary

Iterative single-developer self-review finds the manuscript and finite challenges
coherent after the source-isolation, provenance and garbling corrections below;
full local qualification passes; native exact-head/main outcomes are recorded in the associated PR.

## Verification Checks

- [x] **Plan Compliance**: Yes — bounded literature/claim map, manuscript/supplement,
  all declared challenges, reporting crosswalk and actual independent-checkout replay.
- [x] **Style Compliance**: Pass for touched code under unchanged Ruff ALL/format;
  whole-source strict verification passes with zero typing errors or warnings.
- [x] **New Tests**: Yes — independent binary/Fréchet and conditional-report margins,
  garbling/scalar VOI parity, invalid supports, ties, source/identity and replay tampering.
- [x] **Test Coverage**: Yes — full suite and 92% branch-inclusive source coverage;
  component/integration paths and independent whole-paper replay executed.
- [x] **Test Results**: All five local Nox sessions passed after review fixes;
  1,030 tests passed, five capability skips.

## Findings — applied fixes

### Medium: preserve source roles and complete baseline identities

- **File**: scripts/run_m2_robustness.py (lines 166–170, 258, 291–292).
- **Context**: Reading the old retail config directly did not reuse its shared source
  ledger/model-input checks. A missing baseline row could silently use current optima,
  incorrectly manufacturing zero regret.
- **Suggestion applied**: reuse primary validated_inputs, bind both source-ledger/check
  files, and reject missing baseline profile identities. No new evidence contract.

### Medium: check garbling against the same coupled-report model

- **File**: scripts/run_m2_robustness.py (lines 139, 186–191);
  tests/m2/test_robustness_runner.py (lines 36–56).
- **Context**: The first invariant check covered only the named half-information
  challenge, not the combined specification; comparison there must retain the coupled
  joint report likelihood and prior, rather than compare to independent reports.
- **Suggestion applied**: construct the ungarbled counterpart using the same challenge,
  check every retained-information parameter below one, and exercise combined coupling/
  degradation in the executable small-grid regression test. Scientific outputs unchanged.

### Medium: actual independent source identity

- **File**: scripts/qualify_publication_replay.py (lines 169–201);
  docs/research/M2_REPRODUCIBILITY.md.
- **Context**: A source archive lacks Git metadata required by the existing runner and,
  when nested in the parent checkout, could accidentally discover the parent's Git state.
- **Suggestion applied**: independent local clone without hardlinks, detached at the
  exact committed SHA; require matching commit/tree and imported source path. No original
  ignored captures/runtime directories are inherited. The actual first replay passed all
  29 tables and scientific JSON fields with zero numerical difference at1e-10 tolerance.
  Reused dependencies are explicit; no fresh/offline install or OS network isolation claim.
  The same clone operation also passed against a real shallow local source checkout.

### Low: source access and reporting arithmetic

- **File**: source-catalogue.json; reporting_crosswalk.csv; methods supplement.
- **Context**: An HTTP200 browser challenge is not an article. CHEERS-VOI prose says33
  items, while Table2 displays34 topic identifiers. Source/metadata dates also differ.
- **Suggestion applied**: retain five usable new originals, reject the challenge and
  record four failed routes; preserve missing native timestamps. Cover every displayed
  topic and retain the source count discrepancy. Retail online2023/print2024 dates and
  undated web guidance remain distinct. No source-owner clarification is requested.

## Iterative scope and scientific review

Reviewed base4a6246c through protocol9367699, implementationdedecd0, manuscriptb47b6e5
and the present fixes by source/numerical module, runner/tests/schema, replay, source
metadata/tables, manuscript/reporting and Nox integration groups. Generated CSVs are
reviewed through complete keys/counts/numerical comparisons, not treated as human observations.
The original source/evidence/retail consequence core, M3 interfaces, dependencies,
full-SHA Action pins, security policies and existing check definitions are unchanged.
Robustness generation/verification and whole-paper replay are added within the existing
Nox session; no new task runner.

The manuscript makes no first-VOI-method, empirical NZ policy, public-preference,
equity or commissioning claim. Synthetic1000-resident daily rates are distinct from
NZ15+ target discussion. The combined stress is not a worst case; report replacement
probability0.5 does not imply half the EVSI/EIG. All optimal ties and baseline-tie regret
ranges are retained. No risk-averse criterion or actual study costs are estimated.

Literature QA independently checks all35 visible result blocks across the two retained
batches against32 unique URL dispositions. Eleven source/document/bibliography IDs,
ten claim links, three native reference edges and34 displayed reporting topic rows
cross-check. Scope is bounded/index-limited; no exhaustive systematic review or complete
raw-output preservation for all20 queries is claimed. Five new usable originals and
reused guidance are distinguished from inaccessible/native-stub/index-only material.

Authorship/funding/interests, final journal and applicable formal institutional/site/
cultural requirements remain unresolved author/external matters. No approval, exemption,
consultation or endorsement is invented. No independent-review requirement is introduced.

## Executed evidence and native publication protocol

Initial affected/component/integration tests:47 passed, peak382.4MiB. Review-fix focused
runner/comparator/integration tests:33 passed, peak394.5MiB. Full first challenge grid:
698.9MiB, exit0; baseline125/875/750 primary rows exactly match. Actual first independent
source replay atb47b6e5:717.2MiB, exit0;24 primary and5 challenge tables plus all scientific
report fields match with zero observed difference. Shallow clone identity fixture:
70.4MiB, exit0. All figures/model scores remain conditional research outputs.

Final local five-session and exact-head/receiving-main native outcomes follow actual
execution. Guarded publication requires expected PR head and receiving-main tree, jobs,
Dependency Graph acceptance and signed package provenance. No unexecuted check is
successful. No requests, contacts, registrations, deposits or journal/ethics submissions.

Final local qualification at 0a3f25a: tests, strict_all, reproduce, clean_package and
security all pass. Resource guard: 785.5 MiB sampled peak, exit 0, below unchanged
4 GiB/40-minute budgets. Full suite: 1,030 passed, five capability skips, 92% coverage.
Ruff ALL/format: pass, 124 files; BasedPyright: zero errors/warnings. Pip audit reports
no known vulnerabilities; unchanged zizmor policy passes. Whole-paper clean clone:
29 tables and all scientific JSON fields match with zero numerical difference.
[Executed receipt](../../integration/m2_readiness_20261028/local-qualification.json).
No unresolved self-review findings; native publication remains separately verified.
