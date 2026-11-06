# Decision/evidence preparation — 6 November 2026

P1.1 preparation and P2.1 feasibility are implemented locally; both empirical phases remain
incomplete. No data, posterior, policy effect or native receipt was promoted.

## Delivered and qualified

- decision-definition.md fixes the initial research decision, country/product scope,
  perspectives, planning horizons, estimands, validation eligibility and amendment rules.
  Current detailed legal/excise settings and input-level holdout membership remain open.
- systematic-search.md specifies query families, eligibility, seed challenges, single-owner
  screening, exclusions, deduplication, update rules and medallion extraction requirements.
- Searchright S1 portable strategy passes validate-strategy and compiles to PubMed with
  exact fidelity, no warnings/loss codes; compilation hash
  1165e2b74d203d047303edcc6c2b523c78fe551adb5938dc12bfab79325158f2.
  Logs: outputs/nz-au-phase1/strategy-validation.json and compiled-pubmed.json.
  This validates syntax/translation, not live retrieval, seed recall or review completeness.
- phase1-appraisal.csv contains 34 source/model/parameter/formula queue rows with intended
  disposition, verification status, dependency group and gap; it reuses existing authorities.
  Pending appraisal is not accepted parameter justification or exhaustive model coverage.
- GitHub identifies edithatogo/archive-govt-nz and aegisarchive; HF whoami confirms
  edithatogo with read-repos access. HF dataset search connector returned UNAVAILABLE;
  a public HF dataset-list API worked and identified existing legislative/source archives.
  No new dataset destination or write scope is qualified; no unrelated corpus was modified.
- Three publisher originals were saved and hashed in external staging (AU policy, ABS
  article and ACIC report). Direct NZ policy-page acquisition returned HTTP 403; web reading
  supplied context only. Failed acquisition is retained in phase1-source-receipts.json.
  Rights and durable external archive ingestion/readback are open; staging is not Bronze
  admission or recovery proof. No complete new numerical input is admitted.
- phase2-feasibility.md records the executed Polars historical coverage audit, actual AU
  comparator and quarantined narrative/table denominator discrepancy, with a dimensional
  identification argument. Existing formulas and numerical reference remain unchanged.

## Checks and remaining gates

Context profile: engineering/context/nz-au-evidence.json; actual HEAD/hash/dirty manifest
under outputs/nz-au-phase2/context-final-v2. Context was narrowed explicitly and classified through
the existing publication policy; no byte-budget or private-path guard was weakened.
The first attempt rejected a not-yet-classified new task-card path; classification was
added and the builder passed. The acquisition 403 and HF connector limitation remain gaps.

Final focused context/source-handoff/audit/publication-boundary/workstream selection:
103 passed in 8.75 s on Python 3.15.2, bounded peak 176.7 MiB, exit 0
(outputs/nz-au-phase2/final-focused-tests.log). This includes synthetic negative tests for
changed bytes, duplicate years and schema mismatch. Ruff check and format pass for the new
audit and its tests. git diff --check passes. The final source coverage audit passed at
89.2 MiB, exit 0 (coverage-final.log); it records no native admission check or new observation
admission. The earlier 78-test and four-test runs remain separate receipts. A context rebuild
correctly refused an existing output directory; a new context-final-v2 directory passed.
No previous context/output directory was overwritten. Phase 0 latest-lock native admission is still
owner-held. The owner's chat was read for current status; no new message or mutation was
sent. The earlier Phase 0 handoff had already been delivered under the user's authorisation.

Next: qualify exact source/destination rights and current policy inputs, then complete the
Phase 1 gate before fitting. Complete the initial empirical slice only after admission,
source verification, matched-unit reconciliation and prespecified holdout eligibility pass.
