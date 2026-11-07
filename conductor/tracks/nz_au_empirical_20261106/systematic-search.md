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

## Executed continuation — 7 November 2026

This edition supersedes the earlier statement that no live source-native retrieval
has run. It does not supersede the requirement for screening, grey-source coverage,
original verification or external archive admission. See phase1-progress.md and the
metadata-only phase1-search-receipts-20261107.json for actual terminal counts and gaps.

Current Searchright main 4ddfbdbc54c500719889e09942783bdc04ee832b was fetched and built
with its own locked Cargo dependencies. The actual CLI reports 0.1.0-alpha.1 and five
fixture-backed providers with no network hosts. No fixture search was represented as
a live search. The source-native export/import alternative is now exercised: Europe
PMC REST search/core/cursor exports and the PubMed connector are retained outside
this repository, then bibliographic transport CSVs are imported by the real CLI.
This is supported interchange qualification, not a new Searchright live provider.

Before the first Europe PMC request, exact S1–S5 native queries, scope, cutoff and
pagination policy were persisted in the external protocol.json. Source-specific
Searchright ASTs in searchright-s1-europepmc.json through searchright-s5-europepmc.json
were subsequently authored and validated/compiled with exact fidelity and no warnings.
They document translation qualification after that initial run; do not backdate them
as its prespecified executable strategies. The original S1 PubMed-declared strategy
also remains unchanged. Compiling it directly to Europe PMC correctly emits a declared-
dialect mismatch warning, which is retained rather than suppressed.

Executed Europe PMC queries use TITLE_ABS fields and FIRST_PDATE from 1800-01-01
through the retained evidence cutoff 2026-11-06. That explicit lower date boundary is
a restriction relative to version 1's unrestricted-date intent; no unrestricted or
exhaustive historical-recall claim is made. Results also depend on each provider's
current indexing and date conventions. No country or language restriction was applied.
S1 initially retained one page, then a separately frozen continuation consumed its
cursor. Completeness requires terminal record/unique-ID counts to equal hitCount;
empty responses, repeated cursors, duplicates or count drift fail that check.

S2 PubMed used the corresponding explicit [tiab] Boolean terms, publication-date
cutoff 2026/11/06, publication-date ordering and all five returned offsets. Exact
query translation, connector response and field-pagination metadata are retained.
Its first-page retrieval time is known only to the date from the retained invocation;
subsequent pages have explicit UTC start times. Do not invent missing timestamp precision.
PubMed [tiab], Europe PMC TITLE_ABS, indexing and date semantics are not assumed identical:
the actual S2 PMID overlap and source-only records are reported separately.

The real Searchright CSV imports reopen the retained exports, bind receipt IDs and
check imported identity/title/count against source records. CSV transport omits some
native metadata and does not independently parse Europe PMC's authorString into author
identities. Native exports remain authoritative. The malformed-XML negative control
is quarantined by the actual CLI. Deduplication produces candidates; original source
records are preserved and no candidate cluster is an adjudicated study identity.

S3 v2 missed the prespecified NZ endgame seed, whose title/abstract uses inequity and
HALYs. The separately persisted searchright-s3-europepmc-v3.json adds explicit health-
and cost-related synonyms before fitting. It compiled without translation loss and
was then executed through the source API, recovering the seed. Retain both editions
and compare actual added/removed identities rather than subtracting hit counts to
invent flow totals. This is a documented recall repair, not complete PRESS validation.

S2's Australian seed is individually appraised in phase1-wang-appraisal.md; its later
calibration study is also considered there. The NZ model seed is partially appraised
in phase1-nz-model-appraisal.md. Those selected appraisals do not screen the remaining
corpus. S1/S3/S4/S5 PubMed retrieval, G1/G2 official-source coverage, citation chasing,
full-text decisions/exclusions and comprehensive parameter/formula matrices remain open.
No automated keyword filter has been counted as a completed eligibility assessment.

## PubMed S4 continuation — 7 November 2026

The existing S4 concept groups were translated directly to PubMed Title/Abstract
fields, with the 6 November publication cut-off and no language/country limit.
The exact request was saved before execution. Five connector pages at offsets
0/25/50/75/100 reached the terminal cursor without field continuations or a
pagination limit, but returned only 100 unique records against 101 advertised.
This first terminal result was retained as incomplete.

An exact-query native ESearch read identified PMID 42659019 as the missing ID.
The connector's exact-ID retrieval reported it missing; native EFetch returned
a PubmedBookArticle. Searchright's PubMed XML importer returned zero records
and an explicit no-PubmedArticle warning. Its supported CSV import then accepted
all 101 candidates, including the source-bound book title, book authors, DOI and
12 abstract sections; no journal was manufactured for the book. Every identifier
matches the native search set. Titles and abstracts round-trip without loss.
An explicit native publication-date-range diagnostic returns the same 101 IDs
and exposes the translated cut-off in its response. The diagnostic's year-1000
lower endpoint removed no IDs relative to the original query.

Original responses, transport/import, failed-route evidence and terminal receipts
remain outside tobac under /Volumes/PortableSSD/tobac-p2-search-s4.x181rk.
Metadata/hash pointers are in the P2 context receipt and reconciliation. This
closes retrieval of this exact source/query edition only: no title/abstract or
full-text decisions, duplicate-study adjudication or new admission are counted.
S1/S3/S5 PubMed, grey sources, citation coverage and the other Phase 1 gates
remain open; the frozen earlier search editions are preserved.

## PubMed S5 and book-kind correction — 7 November 2026

The prespecified S5 title/abstract concept groups now have a native PubMed
edition with 475 identifiers, matching an explicit publication-cut-off ESearch
query. Ten connector pages returned 474 unique articles. Three same-parent
continuations recovered the remaining author fragments for PMID 27490260,
preserving all 395 authors. Native EFetch recovered the connector-omitted
PMID 30212113 as a book chapter. Its chapter title and three chapter authors
were retained separately from its parent book and four book editors.

Semantic inspection found the CSV importer defaults to journal_article. The
initial S5 chapter and the earlier S4 book therefore required a correction:
supported CSL import now retains Other(chapter) and Other(book), respectively.
The original CSV imports remain preserved as superseded kind representations.
Corrected editions retain all 475 S5 and 101 S4 IDs with unchanged titles,
abstracts and source authors. The correction does not imply that the remaining
record types or fields have all received full semantic appraisal.

Eight actual title/abstract assessments are recorded externally: seven records
prioritised by an NZ mention and the recovered chapter. Six enter the full-text
retrieval queue; two await full-text assessment of methodological transferability.
This prioritisation is not an eligibility rule. The remaining 467 S5 records
are unscreened. No final inclusion, exclusion, duplicate-study adjudication or
empirical admission is claimed. Assessment is single-owner and AI-assisted;
there is no claimed independent human review. See the per-record reasons and
source hashes under /Volumes/PortableSSD/tobac-p2-search-s5.jLmFdk.

S1/S3 PubMed retrieval, remaining screening, grey sources, citation coverage,
source verification and archive admission remain open. These source/query
retrieval results do not complete the systematic evidence or P2 fit gates.

## PubMed S1 and S3-v3 candidate editions — 7 November 2026

The retained Searchright compiler translated the frozen S1 and amended S3-v3
ASTs to PubMed Title/Abstract syntax. Both compiled receipts flag a different
declared dialect and require human review; these runs qualify source retrieval
and seeds without claiming approved PRESS review or an accepted translation.
The explicit publication cut-off remains 6 November. Native ESearch was used
to reconcile the ID universe, and EFetch retains original XML for those IDs.

S1 exceeds the PubMed result window: the root exposes 9,999 of 25,067 IDs.
Nine complete inclusive date leaves contain 695 repeated ID occurrences;
their union matches 25,067, including the available root IDs. S3 returns all
3,048 IDs in one leaf. Root counts and available ID sets stay stable from
initial to final read. Both designated S1 seeds and the amended S3-v3 seed
are recovered. The earlier Europe PMC S1 count discrepancy stays open.

Original XML and exact ID sets reconcile across 126 S1 and 16 S3 batches.
The first S1 run stopped at 9,800 verified records on an HTTP 200 partial
XML response with an embedded upstream 503. That response and failed run
remain preserved; one exact-batch recovery succeeded, with prior verified
batches reused. Existing Searchright PubMed XML import and kind-preserving
CSL transport account for all 25,067/3,048 records, including 41/35 native
book or chapter occurrences. Source title, plain abstract text and author
counts were checked. Article abstract section labels remain in original XML;
the article importer joins the text without those labels.

Across all five PubMed query families, 28,913 occurrences represent 27,507
unique PMIDs, including 1,388 with multiple family memberships. The external
membership index preserves source links and performs no title/DOI or study
deduplication. No new screening decisions were made in this retrieval run;
the eight earlier S5 assessments remain at their original scope. Remaining
translation review, grey sources/citations, screening, original appraisal
and archive/admission gates stay open. Originals, exact requests, failed
response, corrected continuation and hashes are in the P2.20 external intake.
