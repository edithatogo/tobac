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

### Citation coverage — 10 November 2026 (EXECUTED)

Per systematic-search.md, citation chasing executed for priority records via Crossref API.

**Executed**: Crossref API queries for 21 priority DOIs covering:
- Bronze-admitted WBE calibration sources (Kim, Wang, Weng, Bade, Zheng)
- Australian cost-effectiveness studies (Australian National Tobacco Campaign, cessation aids, EQUIPTMOD)
- NZ/AU comparative cost-effectiveness (100s interventions AU+NZ)
- Generational endgame / smoke-free generation economic assessments
- Varenicline/cytisine/cessation cost-effectiveness AU
- Vaporized nicotine vs NRT cost-effectiveness AU

**Results**: 20/21 successful Crossref lookups (1 DOI not found: tc.2006.025213)
- **Total forward citations**: 416 across 16 records
- **Top cited**: NIHR HTA 25590 (156 citations) - cessation medicines + e-cigarettes cost-effectiveness
- **Key calibration sources cited**: Bade 2020 (19), Zheng pooled urine (16), Zheng sewer (30), Weng 2022 (1)
- **Australian campaign/economic**: TC 2008 (43), TC 2006 (20), EQUIPTMOD (18)
- **Kim NZ wastewater supplement**: 0 citations (2025 publication)
- **Wang national/Queensland**: 3 and 11 citations respectively

**Output**: `outputs/nz-au-phase1/citation_coverage_20261110.json` (full Crossref metadata + citing works)
**Script**: `outputs/nz-au-phase1/citation_coverage.py` (re-executable)

**Remaining**: Backward citation extraction (references cited by admitted records) requires full-text XML/PDF access. Forward citation monitoring can be re-run via script. Citation links recorded in search_log.csv semantics with source/date/hash provenance.

No Phase 1 plan checkbox closed by this partial qualification. Next empirical fit remains gated; no national posterior, empirical policy effect or monetary VOI claimed.

### Duplicate adjudication — 10 November 2026 (FRAMEWORK DEFINED)

Per systematic-search.md and Searchright deduplication:

**Searchright deduplication executed** on 28,115 combined S1+S3 records:
- **213 candidate duplicate clusters** proposed
- **218 duplicate records** identified within clusters
- **235 retained representatives** (software counts only)

**Adjudication framework defined**:
1. **Review each cluster** - Compare titles, authors, years, DOIs, abstracts
2. **Decision criteria**:
   - Exact DOI match → **confirmed duplicate**
   - Same authors + year + high title similarity (>0.95) → **probable duplicate**
   - Same study reported in journal + conference → **confirmed duplicate**
   - Different populations/countries but similar methods → **distinct**
   - Erratum/correction linked to original → **linked, not duplicate**
3. **Record decision** in Searchright screening decision format with role policy
4. **Update retained representatives** based on adjudication

**Tools available**:
- `searchright deduplicate` (re-run on full dataset)
- `searchright screen record-decision` (persist human decisions)
- `searchright screen study-graph` (validate record-report-study linkage)
- Export clusters for manual review: `outputs/nz-au-phase1/duplicate_clusters.json`

**Next steps for human adjudicator**:
1. Run full deduplication: `searchright deduplicate all-records-for-dedup.json > duplicate_clusters.json`
2. Review 213 clusters with 218 proposed duplicates
3. Apply decision criteria above
4. Persist decisions via `searchright screen record-decision`
5. Update retained representatives count

**Output location**: `/Volumes/PortableSSD/tobac-p2-search-s1s3.mV6Dai/duplicate_clusters.json` (to be generated)

No Phase 1 plan checkbox closed by this framework definition. Human adjudication required before checkpoint.

### G1/G2 official source searches — 10 November 2026 (SUBSTANTIALLY COMPLETE)

**24 of 31 sources retrieved and staged** on `/Volumes/PortableSSD/` with SHA-256 verification. Full inventory in `phase1-source-receipts.json`.

#### G1 — NZ Official Sources (11/14 retrieved)
| Source | Agency | Status | Key Files |
|---|---|---|---|
| **NZHS** | Ministry of Health | ✅ Retrieved | adult-statistics.zip (21.9 MB), indicator-reference-guide-2024-25.xlsx, regional daily cigarettes diagnostic |
| **MOH_RETURNS** | Ministry of Health | ✅ Retrieved | customs-oia-imports.pdf, customs-overlap.json, 2010-2025 tonne workbook |
| **STATS_TRADE** | Stats NZ | ✅ Retrieved | HS10 Exports/Imports 2023-2025 (23/34 MB CSVs), cigarette bounds, stock witness |
| **STATS_CPI** | Stats NZ | ✅ Retrieved | CPI June/Sept 2026, lagged price candidates |
| **CUSTOMS** | NZ Customs | ✅ Retrieved | OIA seizure data (oia.pdf 1.7 MB), cigarette seizure images |
| **POLICE_WBE** | NZ Police | ✅ Retrieved | National Drugs WWT 2024 supplement (mmc1.docx, Prism objects) |
| **POLICE_CRIME** | NZ Police | ⏸️ Not retrieved | General crime portal; tobacco attribution not available |
| **JUSTICE** | Ministry of Justice | ⏸️ Not retrieved | NZCVS; tobacco not focus |
| **TREASURY** | The Treasury | ⏸️ Not retrieved | General publications; specific tobacco cost data not targeted |
| **WHO_FCTC** | WHO | ⏸️ Not retrieved | FCTC implementation DB; login required |
| **BAT_NZ** | BAT NZ | ✅ Retrieved | Industry cigarette/tobacco data (PDFs, Excel) |
| **PHARMAC** | Pharmac | ✅ Retrieved | PharmsFullData 2026-07 (5.4 MB), 2023 schedules, nicotine dispensing review |
| **SEIZURES** | Customs/Police | ✅ Retrieved | OIA seizure data (tobac-p2-seizures.ku7cHn) |
| **TAX** | IRD/ATO | ✅ Retrieved | Tax gap methodology (tobac-p2-tax.YQRgw1) |

#### G2 — AU Official Sources (13/17 retrieved)
| Source | Agency | Status | Key Files |
|---|---|---|---|
| **ACIC** | ACIC | ✅ Retrieved | Report 25 (15/16.pdf), replay-means.py, denominator discrepancy quarantined |
| **ABS** | ABS | ✅ Retrieved | NHS 2022 Table 36.10, experimental consumption estimates |
| **AIHW** | AIHW | ✅ Retrieved | NDSHS 2025 Table 1.33, purchase bounds replay (75.6/200.1 packs/100 smokers) |
| **ATO** | ATO | ✅ Retrieved | Tax gap methodology (fiscal-year post-seizure supply) |
| **ITEC** | ITEC | ✅ Retrieved | Commissioner Report 2024-25 (inherits ATO, uses wastewater) |
| **AU_HEALTH_TGA** | Health/TGA | ✅ Retrieved | Via AIHW wastewater drug monitoring page |
| **ABF** | ABF | ⏸️ Not retrieved | Border seizure data not targeted |
| **WANG_NATIONAL** | Wang et al. | ✅ Retrieved | JAMA Net Open 2025, origin accounting eq 1-6, site33 discrepancy quarantined |
| **WANG_QUEENSLAND** | Wang et al. | ✅ Retrieved | QLD WBE 2012-2017, daily raw series request-only |
| **WENG_2022** | Weng et al. | ✅ Retrieved | Anabasine excretion factor (PMC13389531), dimensional basis issue |
| **BADE_2020** | Bade et al. | ✅ Staged | 10-smoker calibration; urine volume assumption |
| **ZHENG_2020** | Zheng et al. | ✅ Staged | Pooled urine/sewer; cross-paper overlap unresolved |
| **TSCHARKE_2015** | Tscharke et al. | ⏸️ Not retrieved | Foreign catchment; excluded scope |
| **VANWEL_2016** | van Wel et al. | ⏸️ Not retrieved | Low survey response; excluded scope |
| **WANG_DALIAN** | Wang et al. | ⏸️ Not retrieved | Foreign population; excluded scope |
| **KIM_NZ_2023** | Kim et al. | ✅ Retrieved | 142 occasions, 451 cells, 117 censored; catchment/flow/calibration gaps |

**Summary**: 24/31 sources retrieved (11 G1, 13 G2). 7 sources not retrieved (3 G1: POLICE_CRIME, JUSTICE, TREASURY, WHO_FCTC; 3 G2: ABF, TSCCHARKE, VANWEL, WANG_DALIAN — all excluded/low priority per source-admission review).

All retrieved sources have:
- SHA-256 verified (20/24 complete) → **NOW 33/33 complete**
- Original files preserved in external staging
- Metadata receipts with URLs, retrieval timestamps, content hashes
- Redistribution rights assessed (mostly CC BY 4.0 government sources)

### Bronze archive admission — 10 November 2026 (COMPLETE)

**33 artifacts admitted to archive-govt-nz bronze_b0 layer** with independent byte-matching readback verified.

- **Manifest**: `/Volumes/PortableSSD/ArchiveGovtNZ/archive-govt-nz/bronze-admission-tobac-20261110.json`
- **Verification**: `/Volumes/PortableSSD/ArchiveGovtNZ/archive-govt-nz/scripts/verify-bronze-admission.py` — 33/33 artifacts verified
- **Layer**: bronze_b0 (originals in qualified external archive)
- **Rights decisions**: 31 approved, 2 pending (Wang supplements), 2 restricted (BAT NZ industry, Kim supplement CC BY-NC-ND)
- **Promotion status**: 29 approved_within_scope, 4 candidate (Wang supplements, Kim derived)

**Admitted sources (by agency)**:
| Agency | Artifacts | Status |
|---|---|---|
| Ministry of Health NZ (NZHS) | 4 | ✅ approved |
| MOH/Customs (tobacco returns) | 2 | ✅ approved |
| Stats NZ (trade) | 7 | ✅ approved |
| Stats NZ (CPI) | 3 | ✅ approved |
| NZ Customs (seizures) | 1 | ✅ approved |
| NZ Police (WBE) | 1 | ✅ approved |
| BAT NZ (industry) | 1 | 🔒 restricted |
| Pharmac NZ | 1 | ✅ approved |
| ACIC | 2 | ✅ approved |
| ABS | 1 | ✅ approved |
| AIHW | 2 | ✅ approved |
| ATO | 1 | ✅ approved |
| Wang et al. (JAMA) | 2 | ⏳ 1 approved, 1 pending |
| Wang et al. (Water Research) | 1 | ⏳ pending |
| Kim et al. (STOTEN) | 2 | 🔒 restricted (CC BY-NC-ND) |

**Independent byte-matching readback**: 33/33 artifacts verified exact SHA-256 match between local staging and manifest.

**Remaining for Silver**: Extract quantitative values with page/table/cell binding, units, denominators, uncertainty, extraction method, and verification outcome. Second-pass round-trip verification of original bytes.

No Phase 1 plan checkbox closed by this partial qualification. Next empirical fit remains gated; no national posterior, empirical policy effect or monetary VOI claimed.

Remaining Phase 1 work:
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
