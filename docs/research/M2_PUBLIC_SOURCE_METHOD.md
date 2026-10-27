# M2 public-source mapping, extraction and estimation protocol

Version 1, 27 October 2026. Scope: hypothetical NZ 600-retailer conditional research,
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

For the next comprehensive pass: cover each stream above, using tobacco/cigarette/RYO,
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
Their final visual/table review remains explicit. No row enters a model automatically.

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

Current deliverable is the protocol plus seeded, cross-referenced tables and a bounded
capture/extraction pass. Outstanding search, supplement and visual-review work stays
unchecked in Conductor. No full systematic-review or empirical-acceptance claim is made.
