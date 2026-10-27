# M2 public-source mapping, extraction and estimation protocol

Version 2, 27 October 2026; version 1 remains in Git history. Scope: hypothetical NZ 600-retailer conditional research,
NZ residents aged 15+ using cigarettes/roll-your-own, with societal and regulator-budget
consequences kept separate. Heated-tobacco records are contextual unless a product-
compatible estimand is explicitly specified. Public material only; no outreach or OIA
submission. This is a reproducible evidence-map protocol and initial extraction, not
a completed systematic review or evidence of exhaustive coverage.

## 1. Identification and screening

Search streams: (a) MOH/NZHS publications, tobacco returns, regulatory impact statements
and Cabinet/briefing releases; (b) Customs/Treasury public statistics, annual reports and
already-published OIA responses; (c) primary retail-policy/biomarker studies via PubMed,
publisher full text and public repositories; (d) publicly accessible supplements and
backward/forward citations. Earlier targeted-review records are imported as a labelled
seed set, not retrospectively assigned a systematic search history.

Record exact query, platform/domain constraints, run date, result batch and limits in
`evidence/m2/public_sources_20261027/search_log.csv`. The initial batch uses four exact
queries with no engine date or language filter. Search ranking changes over time;
queries alone cannot reconstruct earlier result sets. The engine exposes a combined
batch rather than query-specific counts; do not invent those counts. Save the screened
candidate URLs/outcomes in `screening.csv`. Later batches must preserve the visible
result order and retrieved snippets locally, sanitising transient signed URLs.

Executed completion pass (48 queries, 12 combined batches): cover each stream above, using tobacco/cigarette/RYO,
retail availability/reduction, switching/cessation/illicit, anabasine/cotinine, validation/
recovery/censoring, and cost/expenditure/excise terms; record every exact executed
combination. No publication-date exclusion initially. English discovery is an explicit
coverage limitation; retain relevant non-English candidates for feasibility review.
Follow one backward/forward citation round per included primary policy/assay study,
log each parent link, and assess supplements separately. Complete the prespecified
streams and citation round before assessing whether further searching changes the
map. Update searches before a publication claim; do not equate saturation with absence.

Include public primary data, documented methods, official assumptions and implementation
or cost records that address an identified M2 gap. Retain qualitative/context-only and
null findings. Funding or advocacy origin is recorded and appraised, not an automatic
exclusion. Secondary news/opinion can locate primary material but cannot be the sole
source of a quantitative input. Exclude unrelated topics and superseded duplicates with
reasons; preserve editions needed to explain changing assumptions. Record inaccessible,
redacted and not-yet-reviewed candidates separately from exclusions. Do not describe
an unavailable supplement as a need to request data or collect new samples.

## 2. Identity, preservation and catalogue

Reuse existing synthesis IDs and archive aliases; DOI is the work identifier where
available, otherwise an exact official document URL/reference. Assign a document ID to
each edition/attachment, including each supplement, and a separate underlying-data group.
A publication, supplement, summary and OIA reusing the same records are not independent
studies. URL redirects do not establish edition identity.

The maintained archive-govt-nz producer owns capture. Use the explicit source set in
`integration/m2_public_sources_20261027/capture-config/` with an isolated output CAS and
WARC directory. CAS is a content-addressed store: original payloads are named by SHA-256.
Preserve raw originals, WARC responses, PDF text/OCR derivatives and extraction revisions
separately. Never overwrite an earlier edition. Save locally; no raw source publication
or archive-service reconfiguration is part of this task.

`source_index.csv` records canonical URL, source/document/group IDs, local object/WARC/
text paths, hashes, current capture outcome and actual native capture date. Missing
capture dates stay blank. The initial writer produced no WARC-Date: the work is dated
27 October, but an exact native capture timestamp is not established. `capture-receipt.json`
and `local-catalogue.json` retain command outcomes and independent byte verification.
HTTP success, filename or an abstract does not prove full-text table applicability.
Failed/challenge responses are not usable source payloads.

## 3. Cross-referenced tables

| Table | Unit of a row | Links and required interpretation |
| --- | --- | --- |
| source_index.csv | Source edition/attachment | Stable source ID, parent ID, underlying-data group, URL, local paths/hashes, capture status/date |
| source_table.csv | Source characteristics and applicability | Source ID; design, population/product/time/units, access, purpose, limitations, funding/appraisal status |
| extraction_table.csv | One reported value/statement or retained interval | Extraction ID; source ID, page/table/row locator, exact value/unit, estimand, observation window, uncertainty type, extraction mode and review status |
| assumption_table.csv | One source-authored or analyst assumption | Assumption ID; source/extraction links or explicit analyst origin, role, alternative supports, rationale, dependence and consequence of failure |
| parameter_table.csv | One constructed/estimated quantity | Parameter ID; extraction and assumption IDs, formula, operation/unit, result, uncertainty method, rounding and permitted use |
| search_log.csv / screening.csv | Search execution / candidate decision | Batch/query ID, seed versus search origin, URL/parent, disposition and reason |

Every numeric parameter must resolve to extraction rows and/or explicit assumptions.
Every extraction must resolve to a source edition and locator. Unknown is blank with
an explicit reason/status, not zero. An index can include a source that is not usable
for numerical extraction. Cross-references establish traceability, not scientific validity.

## 4. Extraction and quality control

Transcribe published values verbatim in native units and preserve printed precision,
denominator, products, population, observation/forecast periods and uncertainty label.
Keep publication/release dates separate from observation windows. Use text extraction
for navigation; check original tables/rendering before promoting a final numerical input.
For scans, retain OCR and review ambiguous characters; OCR alone is not verification.
Differentiate observations, source-model outputs, source assumptions, analyst supports,
forecasts, intermediate calculations and qualitative claims.

Initial legacy numbers are explicitly labelled imports from the earlier synthesis
ledger; they have not all been re-extracted from newly saved originals. New Customs
and Treasury rows are checked against locally captured PDF text with printed locators.
Critical Treasury/Customs/RIS/baseline/funding/application tables were subsequently
checked against page renderings; human-yield and CVS full HTML were checked against
native sections. Inaccessible foreign/wastewater source numbers retain their explicit
limited-access or unverified status; none is promoted into a numerical model. No row enters a model automatically.

Check signs, percentage versus percentage points, SD versus SE versus confidence interval,
original-matrix versus extract concentrations, row/column totals, missing months and
revision mismatches. Record discrepancies without silently correcting the source. For
example, rounded Treasury baseline/policy totals can differ by NZD1m from a printed
costing-difference row. Carry both source figures and arithmetic-check result until
underlying precision explains it. Do not treat forecast differences as observed effects.
A second pass by the same analyst is self-review, not independent review.

## 5. Construction, estimation and uncertainty

Use exact decimal arithmetic for financial/table arithmetic. Store formulas and input IDs,
not just results. Preserve original units; never add sticks to tonnes or apply an assumed
grams-per-stick conversion without a declared product/year-specific assumption. RYO is
roll-your-own. Keep source-reported estimates distinct from estimates constructed here.

Current examples: sum monthly HTP kilograms within the explicitly available July2024–
May2025 window; calculate historical fee receipts from count × fee; reproduce the source
consumption-gap identity (pre-uplift total × assumed uplift) − lawful release. HTP means
heated tobacco product. These are descriptive/accounting quantities, not current resident
consumption or incremental social costs. Do not fill June2025 with zero or annualise it.

For sensitivity/partial identification, state structural equations, support endpoints,
shared calibration and target-transport conditions. Cartesian interval bounds are not
confidence intervals or probability distributions. Sharp marginal bounds are not a joint
rectangle. Retain infeasibility, null effects and no-study conclusions. The existing
`tobac.partial_identification` and shared evidence contract remain authoritative.

A statistical estimate additionally requires a declared sampling/measurement model,
justified uncertainty, shared-data covariance and target applicability. Report any
inherited model assumptions and transport separately; no inverse-variance pooling of
unlike endpoints or independent treatment of repeated releases of the same observations.
Retain full precision in machine calculations, display no more than inputs support,
and perform sensitivity analyses before interpreting conditional VOI or ranking studies.
No new posterior, empirical cap effect, crime coefficient or normative weights are fitted.

## 6. Completion and reporting

Acceptance for the full evidence map: all search streams/citation rounds logged;
all candidates dispositioned; included public originals/supplements saved and verified
or explicitly unavailable; source/assumption/extraction/parameter tables linked;
locators and critical values rechecked; arithmetic and uncertainty checked; exclusions,
funding limitations, shared inputs and remaining public-only gaps reported.

The bounded completion pass and access dispositions are recorded in
M2_PUBLIC_SOURCE_COMPLETION.md and the completed Conductor plan. Source unavailability
is a qualified outcome, not verified extraction. One citation round used native reference
lists where accessible and exact-DOI searches elsewhere; forward search coverage is
index-limited. No exhaustive systematic-review or empirical-acceptance claim is made.


## 7. Executed search and retrieval limits

B01 is the four-query initial map; B02-B12 execute 44 additional queries, with no
engine date/language filter and English terms. Preserve exact spelling, including
B02's literal site.health.govt.nz queries (not a valid site: restriction) and B08Q1's
unhelpful quoted site:repository phrase. B04/B05 use proper site: constraints and
B11Q2 supplies a real Auckland repository query. Do not retroactively claim the
malformed queries were domain-restricted searches. Search snippets/full responses
are local; canonical candidate URLs, batch ranks, decisions and query logs are tracked.
The engine returns combined results; a batch result cannot be attributed to a single
seed/query or prove a forward-citation edge. Repeated batch appearances are retained.

Backward lists were checked for all 34 human-yield and 23 CVS-purchase references.
For the four other seeds, limited indexed primary sections/abstracts and exact-DOI
searches replace inaccessible native reference lists; completeness is not asserted.
One-hop contextual documents were retrieved where available; their entire reference
and supplement trees are outside this bounded round. Context-only reviews/validation
papers do not supply unverified numeric inputs. No automatic iterative expansion.

The human-yield S2D reconstruction uses 19 reported one-decimal factors, excludes three
dashes and calculates arithmetic mean and sample SD (n−1 denominator). It gives
9.02631578947 and4.95780440935 percentage points. Compare with source9.02±4.95 under
rounding; do not substitute rounded-table estimates or assert an unreported SD label.
Urinary total-anabasine limits0.1/0.2µg/L and supplement censoring replacements remain
urine-specific and cannot resolve a raw-wastewater method threshold.


## 8. Final visible-result audit

A title-length cap in the initial local parser omitted five visible search results.
The corrective audit removed the cap, re-enumerated every saved title/URL line,
reassigned visible batch ranks and rebuilt candidate/citation links. All five are
now dispositioned: clinical anabasine abstract, US flavour-policy review, older
Treasury advice compilation, Hungarian laboratory abstract alias and a fluorescence
materials-sensor paper. Four public objects were retrieved; the ACS route failed
and that materials assay does not qualify target sewage recovery or excretion.
No numerical model input changed. Current counts are213candidate dispositions and
35document records. search-parse-audit.json records every batch match/count/hash,
while the prior31-document manifest remains pre-audit-map-manifest.json.

Completeness is checked against the saved visible batches with no title-length
limit and with parentheses permitted inside URLs; it is not an engine-recall or
per-query completeness claim. Candidate IDs now reflect the complete visible
batch order. The clinical abstract has a vendor-affiliated author and no verified
complete funding disclosure. The flavour review reports Truth Initiative support
to RTI and no conflicts; flavour-product policies are not retailer-number caps.
The Hungarian institutional abstract reproduces the same study, not new evidence.
