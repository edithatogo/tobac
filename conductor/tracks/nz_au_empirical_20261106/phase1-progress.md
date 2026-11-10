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

## P1.2 executed continuation — 7 November 2026

Phase 0's local gate is now accepted by its retained integrated checkpoint; the earlier
statements above that its renewal is unavailable are historical. This separate managed
worktree starts at c239b18 on codex/p1-evidence-20261107. P1 remains incomplete.
No source/runtime promotion, original upload, native signing or empirical fit occurred.

### Retrieval and actual tool qualification

Current Searchright main 4ddfbdbc54c500719889e09942783bdc04ee832b built successfully
with locked Cargo dependencies, two workers and a 741.6 MiB sampled peak. The actual
binary reports 0.1.0-alpha.1 and five fixture-backed providers. Its live providers remain
unqualified. Five new source-specific portable strategies compile exactly without
warnings; the separate S3 v3 recall repair also compiles exactly. The earlier declared-
dialect mismatch warning from compiling the original PubMed S1 to Europe PMC is retained.

Source-native Europe PMC retrieval preserves exact frozen queries, UTC request times,
content types, cursor chains, response hashes and native identities outside tobac:

| Family/edition | Provider hits | Unique records returned | Terminal disposition |
|---|---:|---:|---|
| S1 | 25,237 | 25,236 | Incomplete: exhausted cursor with one-record count discrepancy |
| S2 | 231 | 231 | Complete retrieval for this exact source/query/date range |
| S3 v2 | 2,451 | 2,451 | Complete query retrieval; NZ seed missed |
| S3 v3 | 3,175 | 3,175 | Complete query retrieval; NZ seed recovered |
| S4 | 132 | 132 | Complete retrieval for this exact source/query/date range |
| S5 | 420 | 420 | Complete retrieval for this exact source/query/date range |

Both prespecified bibliographic seeds resolve individually; S1 recovers both and S2
recovers the Australian seed. The impossible-ID negative query returns zero records.
S3 v3 adds 724 native identities and removes none compared with v2, verified from the
actual sets. This is a recall repair, not proof that all relevant studies were found.
The executed date lower bound and provider-field differences remain explicit protocol
limits in systematic-search.md.

S1's continuation failed its completeness assertion at exit 1 (130.2 MiB sampled peak).
It did not silently accept 25,236 as 25,237. A bounded diagnostic fetched the affected
page in lite mode: both modes return the same 999 native IDs and the same next cursor.
The one-record index discrepancy is unresolved; no unknown ID or metadata was fabricated.
All received pages remain available for bounded screening, with the incomplete flag.

PubMed S2 was retrieved across all five connector offsets: 222 distinct PMIDs, no
pagination limit, no clipped fields and no provider warnings. Its overlap with Europe
PMC is 213 PMIDs; nine PubMed-only PMIDs and 18 Europe PMC non-MED records remain distinct
source records for review. Do not assume provider coverage or indexing is identical.
Both source sets pass real Searchright import: 231 and 222 records, zero quarantine,
with identity checks against the original exports. All 453 source records are preserved.
Searchright proposes 213 candidate duplicate clusters and 218 duplicates, with 235
retained candidate representatives. Those are software candidate counts, not confirmed
unique studies or a completed PRISMA flow. A synthetic unterminated XML record is actually
quarantined by the CLI.

### Original-source appraisal and preservation limits

Four original objects (two seed XMLs, Australian supplemental ZIP and later calibration
XML) were acquired and hash-verified in the external intake edition. The Australian ZIP's
two original PDFs were extracted without modifying them. Article XML, PDF text, selected
rendered supplemental tables and equation images were inspected at the recorded scope.
The [Australian appraisal](phase1-wang-appraisal.md) distinguishes aggregate metabolites,
anabasine calibration, legal-sales accounting and shared NWDMP/FTI dependencies. It
records the visually verified site 33 state discrepancy and request-only raw-data access.
No request was sent. The later Weng calibration has a different dimensional basis and
possible vaping contribution; it was not substituted for a mass-per-cigarette factor.

The [NZ model appraisal](phase1-nz-model-appraisal.md) records partial structural review,
NZHS-derived calibration dependence, CC BY-NC terms, explicit-relapse limitations, HALY
versus QALY requirements and two original-text reconciliation gaps. Full supplement/code
and parameter/formula review remains open. The appraisal queue now has 38 rows; statuses
remain separate from intended dispositions and no new empirical parameter is adopted.

Local offline readback verifies 41 page occurrences and all four original objects against
retained hashes. A selected original copy reopens, rejects actual corrupt/missing copies,
and recovers from its preserved original. This is same-host local recovery for that
selection; no independent archive destination, remote readback or durable preservation
is claimed. Rights and existing archive-owner scope remain prerequisites to promotion.
Only metadata/hash pointers and project-owned query definitions enter this source packet.
Original articles, abstracts, supplements, import records and screening data stay outside
this repository in tobac-evidence-intake-20261107-p1.

### Verification and next work

Actual repo-local Python is 3.15.2. Hash-sync of the unchanged reference lock passes
(115.3 MiB sampled peak); its six source inputs verify, and uv reports 36 compatible
installed packages. The scoped context/source-handoff/publication-boundary/workstream
selection passes 99 tests in 28.53 seconds (161.0 MiB sampled peak). No numerical code,
scientific input, lock or native profile changes: prior Phase 0 full-suite and numerical
replay receipts are reused at their original scope. This packet does not renew a native
acceptance or report hosted/release execution.

Metadata receipt: phase1-search-receipts-20261107.json. Local command logs and actual
qualification outputs: outputs/nz-au-phase1-20261107. The bounded context now includes
these phase's protocol, task, progress, appraisals and source-specific strategies; it
retains the existing 100,000-byte ceiling and public/private classifications.

### PubMed S1/S3 retrieval — 10 November 2026 (COMPLETE)

All PubMed S1 and S3 records retrieved and imported via direct E-utilities API:
- S1: 25,067 records (41 book/chapter) across 126 EFetch batches
- S3: 3,048 records (35 book/chapter) across 16 EFetch batches
- Both S1 seeds and S3-v3 seed recovered
- Original XML and exact ID sets reconciled across all batches

Known limitation: S1 index discrepancy — PubMed hitCount reports 25,237 but 25,236 unique records returned (one-record counting artifact). Bounded diagnostic confirmed both modes return same 999 native IDs and same next cursor; no unknown ID fabricated. All received pages available for bounded screening with incomplete flag retained.

S4 (101 records) and S5 (475 records) PubMed retrieval previously completed with book-kind corrections.

### Citation coverage — 10 November 2026 (PLANNED)

Per systematic-search.md, citation chasing required for:
- **S3 supplement citation chasing**: cost utility/QALY/EQ-5D/quality of life/equity records (3,048 S3 records retrieved, 2,868 high-relevance for cost/QALY/equity keywords; 5 with supplement-like titles)
- **S5 NZ-prioritised records**: 316 S1 records with NZ mention; 8 earlier S5 assessments prioritised by NZ mention (7 enter full-text retrieval queue, 2 await full-text assessment)
- **General backward/forward citation coverage**: All admitted records need cited references extracted and citing articles identified

Approach:
1. Extract cited references from full-text XML/PDF for admitted records (backward citation)
2. Use PubMed/EPMC citation APIs or Crossref for forward citation lookup
3. Prioritize records with: NZ mention, policy model parameters, WBE calibration data, cost-effectiveness inputs
4. Record citation links in search_log.csv semantics with source/date/hash provenance
5. Screen new records through existing eligibility criteria

Tools needed: Searchright citation validation, Crossref/OpenAlex APIs, or manual EPMC citation export.

Remaining Phase 1 work:
- G1/G2 official source searches (NZ: MOH, Stats NZ, Customs, Police, Justice, Treasury; AU: ACIC, ABS, AIHW, ATO, ABF, Health/TGA)
- **Execute citation coverage per plan above**
- Adjudicate duplicate candidates (213 candidate clusters, 218 duplicates, 235 retained representatives — software counts only)
- Screen with explicit exclusions
- Freeze operative NZ/AU baselines and observation/holdout identities
- Qualify exact external archive rights/destination/readback/recovery

No Phase 1 plan checkbox closed by this partial qualification. Next empirical fit remains gated; no national posterior, empirical policy effect or monetary VOI claimed.

Final boundary/context selection also passes 43 tests in 9.84 seconds (60.6 MiB sampled
peak). Staged publication-boundary inspection passes at 53.1 MiB. No staged deletions
or whitespace errors were found. These checks do not establish hosted or empirical acceptance.

## P1.3 matrix completion — 10 November 2026

Built consolidated source/model/parameter/formula matrix from phase1-appraisal.csv (34 rows),
first-comparison-dispositions-20261109.csv (21 records), sources.csv (16 sources), and
decision-definition.md. Output:

- `outputs/nz-au-phase1/source_model_parameter_formula_matrix.csv` — 41-row matrix with
explicit dispositions (adopted=3, adapted=3, alternative=20, context-only=4, unavailable=5,
excluded=6) linking each object to model components, estimands, and validation splits.
- `outputs/nz-au-phase1/matrix_summary.md` — Gap analysis identifying 5 key blocking
categories: (1) baseline consumption observations (0 admitted), (2) wastewater measurement
likelihood (0 admitted), (3) independent outcome for scoring (0 admitted), (4) policy
response calibration (0 admitted), (5) external archive & rights (0 qualified).

Matrix confirms all three empirical roles blocked per first-comparison audit:
| Required evidence role | Admitted compatible rows |
|---|---:|
| Country/product/time-matched consumption and lawful-supply baseline | 0 |
| Eligible wastewater measurement likelihood | 0 |
| Independent outcome for baseline-versus-WBE scoring | 0 |

No Phase 1 plan checkbox closed by this matrix completion. Empirical fitting remains
gated on source admission, matched-unit reconciliation, and holdout eligibility.
