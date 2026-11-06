# Systematic evidence protocol — version 1, 6 November 2026

Status: prespecified protocol and qualified strategy interface; live systematic execution,
recall and complete screening are not established. Historical October searches remain
separate editions. General web discovery on 6 November is supplementary discovery only.

## Questions, eligibility and query families

Identify (1) tobacco/nicotine policy models and their parameters, (2) measurement and
calibration evidence for nicotine/tobacco WBE, (3) incremental decision value of measurement,
(4) NZ/AU public datasets and policy implementation, and (5) health, HR-QoL, cost, equity,
diffusion and competition methods that can fill a specified model component.

Include original empirical studies, model methods/code/supplements and official methods,
data and operative legislation. Search worldwide for methods; appraise country applicability
after retrieval. No initial language/date restriction; record inaccessible translations
as gaps. Reviews and WHO compilations aid discovery and dependence mapping; they do not
become independent measurements of their upstream surveys. Record industry funding and
data access without automatic exclusion. Pure non-nicotine drug WBE is contextual unless
a transferable measurement component is identified. Individual clinical diagnosis and
unrelated environmental toxicity are out of scope.

Execute separate source-translated families, without requiring outcome words in every search:

| ID | Concepts | Required source routes |
|---|---|---|
| S1 | tobacco OR nicotine; policy OR simulation OR model OR wastewater | PubMed, Europe PMC; Searchright AST in searchright-strategy.json |
| S2 | nicotine OR cotinine OR hydroxycotinine OR anabasine; wastewater OR sewage | PubMed, Europe PMC; biomarker synonyms checked against seeds |
| S3 | tobacco; cost utility OR QALY OR EQ-5D OR quality of life OR equity | PubMed, Europe PMC; supplement citation chasing |
| S4 | value of information OR expected value of sample information; monitoring OR public health | PubMed, Europe PMC; no country restriction |
| S5 | tobacco policy; diffusion OR competition OR spillover OR adoption | PubMed, OpenAlex/Crossref discovery; verify original reports |
| G1 | tobacco/nicotine/smoking/vaping + NZ source names | MOH, Stats NZ, Customs, Police, Justice, Treasury, legislation, WHO FCTC |
| G2 | tobacco/nicotine/wastewater + AU source names | ACIC, ABS, AIHW, ATO, ABF, Health/TGA, state authorities, WHO |

S2–S5 are protocol concepts, not compiled/executed strategies. Each needs an exact persisted
query and source translation before execution. Grey-source queries use publisher search/API
where available, then bounded site-search and reference chasing. Record failed/empty routes;
a search engine's displayed hit count is not a retrieved-record count.

## Searchright qualification and execution record

The retained 0.1.0-alpha.1 binary was built from af8c282f4c0e92a958027ca352e82f1cc7180c57.
Its providers command reports five fixture-backed no-network providers. The 6 November
GitHub main was 4ddfbdbc54c500719889e09942783bdc04ee832b; observing that revision is not
qualifying a newer binary. Reuse the installed CLI to validate/compile the portable AST.
Do not run fixtures and label their records a literature search. A future live adapter
must qualify exact source/API, request syntax, pagination, rate limits, errors and retained
responses before use. Supported source-native export/import is an alternative when live
Searchright execution is unavailable; qualify the actual import contract first.

For every real run retain protocol/strategy/source revision and hash, exact query,
source/platform/API, timestamp, limits, pages/cursors, records received, failures, raw-response
hashes, credentials redacted and terminal status. Use existing search_log.csv semantics
and Searchright receipts; never substitute manually claimed provider success.

Seeds are diagnostic challenges, not included studies: NZ Action Plan simulation
DOI 10.1136/tc-2022-057655 (identified in Ministry repeal analysis), AU nicotine/WBE
PMID 41661592, the ACIC report 25 programme and ABS experimental consumption article.
Verify original identity and eligibility before recall testing. Record seed retrieval by
each applicable family; missing seeds trigger documented translation/query review before
execution is frozen. Do not tune on held-out empirical model outcomes. PRESS-style
self-check covers concepts, Boolean logic, vocabulary, limits and translation loss; no
independent information-specialist review is claimed or required for this solo repository.

## Deduplication, screening and updates

Preserve source-native record IDs and DOI/PMID normalisation; exact identifiers precede
title/year matching. Retain ambiguous matches for review. Link multiple reports to one
study and shared datasets to one dependency group, preserving corrections/retractions.
Two-pass title/abstract then full-text screening records operator, time, criterion and
reason. Single-owner screening is explicit; no invented second reviewer. Unavailable full
text is unresolved retrieval, not evidence that the study is ineligible. Exclusion codes:
wrong exposure, wrong decision/method, no transferable component, duplicate report,
superseded edition (retained), and inaccessible original (pending, not exclusion).
Use actual unique-record arithmetic for PRISMA-style reporting; no synthetic flow counts.

Freeze each run. Refresh before empirical fitting and release, on source revision/retraction
or a changed policy baseline; scheduled refresh is a future optional operation, not an
installed background task. Preserve parents, additions/removals, changed queries and
screening amendments. Re-screen affected records; invalidate dependent inputs selectively.

## Extraction and medallion admission

Bronze originals stay in an existing qualified external archive; local external staging
is temporary acquisition evidence, not archive admission. Resolve source/register IDs,
rights, exact destination and byte readback before upload. Public availability does not
grant redistribution rights. Keep only allowed metadata/hash pointers here.

Reuse the archive register and observation-handoff schema, then existing extraction,
parameter and assumption tables; extend through their owner rather than create a second
canonical table. Every proposed Silver value must bind original hash, page/table/cell,
reported string/precision, unit, product, country/geography, population/denominator, dates,
uncertainty/covariance, missingness, extraction method and verification outcome. A second
pass reopens original bytes and verifies rounding and totals; an original abstract cannot
verify an unseen supplement. Reconcile versions and shared sources. Quarantine mismatches.

Gold requires model/formula applicability, identification, dependence and accepted assumptions;
Platinum requires run/parameter/formula/environment versions and validated interpretation.
The phase1-appraisal.csv queue covers all four object types and links existing authorities.
Disposition vocabulary: adopted, adapted, alternative, context-only, excluded, unavailable.
Disposition is intended use; verification/admission status is separate. No pending row is an
adopted empirical input. Capture gaps explicitly, including programme costs, origin/product
attribution, representative catchments, utility tariffs and transportable intervention effects.
