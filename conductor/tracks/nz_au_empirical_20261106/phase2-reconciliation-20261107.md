# First empirical slice — source reconciliation, 7 November 2026

P2 remains in progress. Public NZ survey originals are now acquired and a reproducible
candidate extraction is implemented; a matched consumption likelihood, supported policy
contrast and held-out wastewater comparison are not established. No P2 plan row is closed
by these enabling results alone.

## Original NZ survey edition

The Ministry's official Annual Data Explorer 2024/25 provides three CSV downloads:
prevalence/mean, subgroup comparisons and changes over time. The internal browser
successfully downloaded all three into a separate external intake edition. Its visible
copyright statement identifies CC BY 4.0; retain attribution and the original terms.
The stable prevalence URL is:
https://minhealthnz.shinyapps.io/nz-health-survey-2024-25-annual-data-explorer/data/nz-health-survey-2024-25-prevalences.csv

A supported CLI GET to that observed application asset returned HTTP 200, text/csv and
6,088,525 bytes with SHA256
6d3e0a019d7e32030147f128c21098f074683cd3cfef41b0dcfff85b74b6b915.
Those bytes equal the browser download exactly. Use this qualified CLI route for the
remaining source work. The four separate health.govt.nz page/workbook/PDF requests
returned HTTP 403; preserve those failures without labelling their bodies source data
or treating this as a denial of the working Shiny-hosted route.

Original CSVs and candidate rows remain outside tobac in
/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2. Exact request/download time
precision, source asset names, hashes, byte counts and failure responses are retained
there. Download completion observations are not fabricated HTTP response timestamps.
No upload, native registration or redistribution permission beyond the observed source
terms is inferred from a successful acquisition.

The Ministry’s separate [2023/24 correction notice](https://www.health.govt.nz/monitoring-statistics/surveys/new-zealand-health-survey/publications/202324-survey-publications/corrections-made-to-202324-data) names specific access/mental-health and child questionnaire items, rather than
smoking questions. Do not infer a smoking-series retraction from that notice. This
web-read context does not replace original-byte/version qualification of the CSV.

## Executed extraction and coverage

The existing audit_empirical_coverage.py now optionally reopens this hash-bound CSV
through the existing source_handoff path/fixity checks and Polars. It retains the original
19 columns plus a logical data-record ordinal, then selects adult total-population rows
for eight prespecified smoking/vaping indicators. Only the total estimate/CI triplet is
audited numerically; sex-specific fields remain original unvalidated fields. No second
canonical observation contract or EvidencePacket is constructed.

The source export contains 47,708 records. Its selected 87 candidate records comprise:

| Series | Actual survey-start labels | Records |
|---|---|---:|
| Current smokers, daily smokers, mean cigarettes | Each 2011 through 2024 | 14 each |
| Daily vaping and four daily-only/dual/union indicators | Each 2015 and 2017 through 2024 | 9 each |

All selected total estimate/CI triplets are present and unflagged in this source edition.
The missing 2016 label in the vaping-related series remains absent; the extraction does
not interpolate it or infer why it is absent. Other source rows can carry S/e publication
flags. The helper preserves flagged values and withholds their numeric triplets from
usable coverage; unknown flags, nonfinite/reversed/out-of-range marginal intervals,
duplicate indicator/year records and changed schemas or hashes are rejected.

Raw source year 2024 corresponds to the explorer's 2024/25 survey label. The helper
preserves the source-start-year convention and does not invent exact ISO observation
boundaries. The native page says collection spanned July 2024 to July 2025, which does
not establish calendar-year consumption. Suppressed/missing values are not zeros.
Existing candidate editions and in-repository candidate-output destinations are refused.

## Measurement and matching constraints

The native indicator definition says daily-smoking prevalence covers established
smokers aged 15+ who smoke daily and have smoked more than 100 lifetime cigarettes.
The intensity definition is the mean number of cigarettes per day among daily smokers,
excluding those who mainly smoke pipes/cigars. It is calculated from categorical ranges
using midpoints and a top-coded final category. These definitions were checked after
the selected indicator and loaded definition agreed; the UI updates asynchronously.

Consequently, multiplying the two published marginal quantities does not produce a
verified all-person/all-product total. Missing corrections include the differing pipe/
cigar population basis, nondaily and younger consumption, range/top-code measurement
error, survey weights and joint covariance. Published estimated counts are rounded and
share the survey source; do not reconstruct a precise denominator by division or treat
counts, prevalence, ratios and trend exports as independent measurements. An uncertainty
interval for a product cannot be manufactured from unrelated marginal CI endpoints.

The existing release workbook is already source-verified in
integration/archive/workbook-reconciliation.json: all 16 values match the original
workbook, whose SHA256 is 3a55a6469097ebc3fb27a6143db7749e5b885761ada76b197053dfe76f36e883.
The earlier feasibility statement that these are only unverified chart extractions is
historical at this checkpoint. This does not resolve the workbook's product conversion,
duty-free/stock/tourism or administrative-scope limits. A failed fresh HTTP request does
not invalidate the retained original-byte qualification or prove source absence.

Do not join a survey-start label to calendar-year releases as if their intervals and
products matched. Prices, trade, compatible population denominators, lawful unrecorded
flows and NZ nicotine/tobacco WBE observations are still not assembled as accepted matched
inputs. Australian NWDMP and Wang/FTI-derived estimates retain their own dependence and
calibration limitations; they are not new NZ observations. The P1 source quarantines remain.

## Validation and the next empirical operation

The source helper retains explicit false values for new observation admission, verified
ISO dates, available joint covariance and a frozen holdout manifest. This is deliberate:
these conditions have not passed. Preserve the previously specified holdout rule, but do
not label a complete survey marginal year a complete matched country/product panel.

Before fitting, close original/destination admission and scope reconciliation; freeze
the actual joint observation/holdout manifest; establish a supported retail/cessation
contrast under the current legal baseline and a justified measurement/dependence model.
Then evaluate the simpler baseline and incremental WBE on the same held-out observations.
If the required data remain unavailable, report the supported identified set and explicit
non-identification limits. Do not substitute synthetic observations, an independence
assumption, a transported causal effect or a zero programme cost to produce a fit.

Actual command outcomes and retained corrections are in phase2-receipts-20261107.json.
The original finite-state engine, its reference inputs and all M3 interfaces are unchanged.

## Source freeze verification

The final Nox tests session passes 1,289 tests with 22 real capability skips and 92%
coverage of src. New audit tests run; the skipped cases concern separately qualified
clustering, native/private lineage, Snakemake, mutation tooling, Voiage and Ruff tool
environments. They are not empirical tests claimed successful. Whole-source typing
passes with zero errors/warnings in the lane’s own Python 3.15.2 audit environment;
affected-file Ruff check/format passes with its locked 0.17.4. The independent CSV reader
reopens all three original hashes and verifies every original field of all 87 candidate
records against its logical source ordinal. All three candidate editions have identical
bytes. The first unbounded extraction and corrected bounded runs remain separate.

The combined tests/reproduce attempt retains its final failure: numerical checks ran,
but the clean-source publication replay refused the uncommitted checkout. Source will
be committed before that required clean-source operation is rerun; this is not a waived
gate or a successful full reproduction claim. Terminal clean-source evidence follows
as a separate metadata closeout. No empirical likelihood or native original is changed.

## Terminal clean-source reproduction

Nox reproduce passes from clean source a818f28860196e61661fdb2b685320699c892ad2
using actual repo-local Python 3.15.2 (705.5 MiB sampled group peak, exit 0). Its
independent clone has the same commit and source tree. Both publication variants
reproduce all 29 compared CSV tables with zero numerical difference and zero report
difference. The source-defined absolute comparison tolerance remains 1e-10; none was
changed. This reuses qualified dependencies and is not a fresh/offline install or
OS network-isolation claim. The earlier dirty-source refusal remains in the receipt.

Source code is frozen at a818f28; the subsequent closeout changes metadata only. The
P1 branch remains frozen at 403600b. The existing integrator is idle at the scoped
readback and retains native/archive ownership. The three new NZHS originals and their
87 candidate records still require exact destination/source admission before fitting.
No cross-chat message, external upload or publication has been performed.

## P2.3 matching-source candidates — 7 November 2026

Continued independently from b1cb8f4 with unchanged maintained code. Hash-bound
originals, raw candidate fields and native query descriptor are outside tobac in
`/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2-context`.
`phase2-context-receipts-20261107.json` records original hashes, routes, exact
coordinates, extraction checks and retained failures. No source is admitted and
none enters the likelihood or existing scientific inputs.

- Population: native internal-browser Statistics NZ table DPE054AA, 142 quarters
  1991Q1–2026Q2; As at and Mean year ended, Male/Female/Total, Under 15/15 and over/
  All ages. The first export omitted flags and is retained. A second export with
  ShowNonFinalFlags and its native TQX descriptor preserve 2,556 selected cells,
  27 `..` unavailable values and 108 literal ` P` provisional flags. Every raw
  value/flag is checked against its source CSV record/column. The published
  rounding footnote accompanies age-sum residuals of −100, 0 or 100; no tolerance,
  adjustment or independent status is invented. The export records 2023 ERP and
  post-2018 revisions, last updated 18 August 2026. ERP is not automatically the
  NZHS source-defined survey population or a wastewater catchment denominator.
  P2.5 below corrects the earlier private-household-only shorthand.
- Price: September 2026 official CPI CSVs and original XLSX downloaded through
  publisher links. Windows-1252 decoding of the Infoshare CSV roundtrips exactly;
  no replacement characters or edited originals. The broad 42 current-quarter
  and 621 historical tobacco-labelled rows are candidate matches, including
  aggregate alcohol and tobacco and distinct series. Exact CPIQ.SE9022 subgroup
  has 207 quarterly Index records, 1975.03–2026.09, published FINAL. Workbook
  sheet 2.01 A4 gives June 2017 = 1000; A16/B16 identify cigarettes and tobacco /
  SE9022, K16 gives 1889. Sheet 4 A11/B11/C11 identifies cigarette retail prices /
  SAP0240 / pack of 25; D4/F4 are Jun-26/Sep-26, D5 is `$`, D11/F11 are 61.28/61.5.
  Indexes, dollar prices and percent changes remain distinct. Currency/tax,
  historical selected-item prices and transaction/survey-period bridges remain open.
- Trade: actual September 2026 HS10 import and export CSVs downloaded from the
  official overseas-merchandise-trade dataset page. All-string Polars selection
  with literal empty strings, then independent stdlib CSV equality by ordinal,
  verifies 15 HS24 import candidates out of 8,660 rows and four export candidates
  out of 5,930. All are provisional. HS codes stay ten-character strings; exports,
  re-exports and total exports remain separate. HS24 contains tobacco substitutes,
  nicotine and mixed NMB/LTR/KTC/KGM/MIL/unspecified units: no quantity pooling or
  inference that these flows are duty-paid consumption. One month qualifies a
  source route; a historical product-matched trade bridge is still required.

The native exports, original source pages and observed CC BY 4.0 publisher footer
are retained externally. That footer alone does not establish downstream archive
admission, exact rights scope or substantive appraisal. No external message,
archive/native write, shared-main publication or private-binding transfer occurred.
The existing owner handoff question remains unanswered; it does not prevent these
independent source reads and does not authorise a cross-chat message.

Initial flag/empty-string/API mismatches are preserved and diagnosed in the receipt;
corrected guarded extraction checks pass. No maintained code, lock, model or tests
changed: reuse P2.2's full test/typing/reproduction evidence at its stated scope.
P1 source/rights/policy gates and P2 period/product/dependence/calibration/holdout
identification remain open. This source reconciliation is not an empirical fit,
held-out result, policy contrast, VOI result or a completed P2 task.

## P2.4 historical cigarette-price proxy — 7 November 2026

Official Infoshare exact-series search CPIQ.SAP0240 returned the selected quarterly
weighted-average price table. Internal-browser native exports retain all 82 quarters,
2006Q2–2026Q3, two decimal places, ShowZeroRows and ShowNonFinalFlags. The options
initially inherited zero decimal places from population work; these were changed to
two before the first price download, avoiding rounded price originals. CSV SHA256
62071f35b5e4c70fdf84c2733a084c26282d67f8199bbc2c2fe39e183e40a1ce;
TQX SHA256 dbd805e1fd7e05f33ad6b745742b399386fb373061c715a7e189c9836762621d.
Native query tableID CPI324601 differs from the published table reference CPI019AA;
retain both rather than inferring table identity from a download filename.

The original CSV footnote confirms `$`, units, cigarettes from supermarket/convenience
stores, pack of 25. Crucially, it says these levels are calculated by applying index
movements to June 2006 weighted prices and are not statistically accurate measures of
average transaction-price levels. They support percentage price movements within the
publisher's stated scope. This refines P2.3's provisional price disposition: **retain
as an index-derived price proxy, not independent observed paid prices**. Do not condition
on the proxy and its source index movements as independent measurements. The separate
SE9022 subgroup includes cigarettes and other tobacco; it is not automatically the
exact item index generating SAP0240. Historical pack-definition revisions, currency/tax
metadata and survey-period compatibility still require qualification.

Originals and the native query are outside tobac in
`/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2-price`, with a saved
extractor and immutable candidate CSV. The guarded Python 3.15.2 / Polars extraction
passes: 82 contiguous unique quarters, all source-record/value roundtrips, query
series/time/options equality, exact unit/method footnotes and numeric agreement with
the earlier September 2026 CLI CSV. The Jun–Sep rounded percent change also agrees
with workbook sheet 4. No non-final flag cells appear in this export; no status,
confidence interval or covariance column is invented. Source last-updated is
22 October 2026 10:45am, distinct from retrieval and observation periods.

See phase2-context-receipts-20261107.json historical_price_continuation for exact
original/candidate/extractor hashes and execution scope. This closes historical
coverage of that particular published proxy. It does not establish paid-price levels,
causal elasticity, source admission, empirical consumption, a policy contrast or
validation. No maintained code/runtime/scientific inputs changed, so unchanged P2.2
full tests/typing/numerical replay remain reused. P2 remains incomplete.

## P2.5 source-defined survey periods and benchmark — 7 November 2026

The existing CLI 403s remain route-specific failures. The internal browser opens the
actual Ministry annual and methodology publication pages, and downloads the original
55-page 2024/25 methodology PDF from the observed publisher link. SHA256:
b938a5bd2959468a5da5be1d7d56539f215d1c2a0589753bd8410c7a22cd210b.
Publication page: 19 November 2025, Ministry-owned CC BY 4.0; this is source rights
metadata, not a native archive admission. Originals, rendered pages, an external
quarter ledger and saved extraction scripts remain outside tobac in
`/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2-methods`.

Ten complete relevant PDF pages were rendered and visually checked against extracted
text. PDF page numbers count from one; printed numbers differ by six:

- PDF 11–12 / printed 5–6: target is the usually resident population, including
  non-private accommodation. The covered survey includes rest homes and specified
  student accommodation, with explicit exclusions including hospitals, prisons and
  higher-level care. This corrects this lane's overly narrow private-household-only
  shorthand; it does not make the survey frame identical to catchment contributors.
- PDF 32–33 / printed 26–27: ERP counts inform calibration. Total population benchmarks
  average quarter-end ERP over a survey year. The survey uses census-rebased benchmarks
  and does not typically adopt every subsequent quarterly revision. Survey estimated
  numbers, prevalence and these calibration totals cannot be conditioned on independently.
- PDF 35 / printed 29: 100 delete-a-group jackknife replicates are recalibrated. Since
  2015/16, reused PSUs retain replicate groups across adjacent years to account for
  clustering in differences and pooled estimates. The marginal CSV intervals do not
  supply that joint covariance or prove independent annual errors.
- PDF 43–44 / printed 37–38, Tables 5–7: nominal survey quarters are July–September,
  October–December, January–March and April–June. Actual 2024/25 fieldwork ran
  9 July 2024–20 July 2025; quarter-specific interview windows overlap and extend
  beyond their nominal quarters. Four adult counts sum exactly to 9,253 and four
  child counts to 2,805. Do not use those counts as interview-date or calibration
  weights for quarterly prices. This verifies this edition's dates only, without
  assigning normal July–June fieldwork to pandemic-affected historical years.
- PDF 49 / printed 43, Table 9: published adult population count is 4,339,820;
  published gender population subtotals sum one lower (children one higher). Retain
  published totals and rounded subtotals without an invented adjustment. Current ERP
  sex categories are not a substitute for reported survey gender categories.
- PDF 52–53 / printed 46–47: the 2024/25 edition rebases historical weights. Specific
  interviewer-item corrections for 2023/24 list GP access, mental health, child sleep,
  food security and diet, not tobacco/vaping. This does not prove tobacco estimates
  unchanged across editions because population rebasing is a separate revision.

The guarded Polars/stdlib reconciliation verifies the four-quarter source ledger,
ISO conversions, respondent totals, original hash, source locations and exact CSV
roundtrip. Applying the documented equal-quarter average to the later DPE054AA
18 August 2026 edition's Total age-15-plus As-at counts yields 4,338,100, 1,720 below
Table 9. Two selected ERP quarters are provisional. This is a cross-vintage diagnostic,
not evidence that either publisher is wrong, a measure of excluded people or an
accepted denominator replacement. No point population, mean-year-ended population,
rounded prevalence inversion or arbitrary fieldwork allocation is substituted.

The existing source receipt now binds methods, ledger and extractor hashes. The
context builder initially exceeded its unchanged 100,000-byte ceiling; two frozen P1
model appraisals were removed from this task's context selection, not from the repo,
and the narrowed context passes. One shell heredoc failed for lack of temporary
space before executing its diagnostic. A scoped write/fsync/readback probe and small
bounded reconciliations subsequently pass; shared-volume headroom remains low.
No unrelated caches, archives, environments or native objects were removed or changed.

This advances period/frame/dependence matching. Historical methods, source/rights
admission, lawful-product/stock flows, causal policy effects and the frozen validation
manifest still constrain the first empirical fit. P2 remains active and incomplete;
no maintained model/audit/runtime source changed, so prior P2.2 tests/typing/replay
are reused at their original scope.

## P2.6 reported-market-flow scope and year quarantine — 7 November 2026

The Ministry returns pages open in the internal browser despite the retained CLI
403s. The general page specifies January–December annual returns; the 2025 page
(last updated 21 August 2026) describes manufacturer/importer releases to the NZ
retail market and expressly excludes heated tobacco from that smoked-tobacco summary.
The 16-year workbook is byte-identical to the already-qualified original SHA256
3a55a6469097ebc3fb27a6143db7749e5b885761ada76b197053dfe76f36e883;
reuse integration/archive/workbook-reconciliation.json's exact 16-value comparison.
This is a reported-market flow, not independently verified Customs tax clearance or
same-period resident consumption. Original label excludes cigars/cigarillos; product
conversion, stock, visitors, lawful unrecorded flows and duty-free treatment still matter.

Original workbooks and a bounded manufacturer-form check are external in
`/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2-returns`.
The BAT cigarette PDF (5274d4108faf2cbf2527aeb300634591f3f7684aa953f18219751dec214bce98)
was visually checked on complete pages 1–2: domestic and duty-free quantities are
separate, pack size is in sticks, and quantity is cigarettes released for sale.
Its domestic price column is a recommended 2025 exit retail price, NZ dollars incl.
GST, not realised transaction receipts or a representative annual paid price. The
44 domestic line quantities sum exactly to the printed total; 11 duty-free lines
also match their printed total. No cigarette-to-mass conversion is inferred.

**Q:BAT2025:RYO:year**: the publisher's 2025 listing and file BAT-Sales-RYO-2025.pdf
conflict with the original PDF's visible `2024` heading (page 1). SHA256
5c683fe95b250f357d622c5aeb84a31dbbf1d3abf7ac82b983ba10ce41b63430.
Retain both assertions and quarantine the year assignment; do not decide which is a
typo. The page separately reports domestic and duty-free loose-tobacco quantities
in tonnes. Seventeen domestic and four duty-free rows reproduce the respective
one-decimal printed totals after explicit decimal rounding; no rounding tolerance
is used to resolve the year. A bounded adjacent-2024 PDF check returned cigarette
tables, not a comparable RYO return, and does not resolve this conflict. No additional
source request was sent and no value is admitted as either year.

The market-type workbook (11d1e5f4aff99b59689017529c713613df84518107407855fbbfca0bc1d01074)
uses Excel percent formats 9/10: stored fractions are not already percentage points.
Displayed shares sum to 99.85%; preserve source lexemes and display rounding rather
than normalising them. The inspected chart/workbook does not establish whether the
shares represent value, mass or item counts. It cannot divide the aggregate tonnage
into product-specific resident consumption. Company shares, receipts and product
shares are not independent quantities merely because the page draws different charts.

Guarded Python 3.15.2 Polars/Decimal extraction preserves 76 raw line candidates,
source PDF pages, extracted-line locations, unit/pack/price lexemes and both year
assertions outside tobac. Exact candidate-string roundtrip, original hashes, domestic/
duty-free sums and workbook cell/format inspection pass. This is one manufacturer's
scope check, not complete national return reconciliation. Third-party company PDFs
need their own rights assessment; public links do not confer blanket Ministry licensing.

The existing P2 receipt binds all originals/extractors and the year quarantine. No
scientific source/runtime/native object changed, no original was uploaded or admitted,
and no model, policy effect or held-out result was fitted. This removes ambiguity about
some administrative fields while retaining the unresolved source/rights/product/period
and validation gates. P2 remains active and incomplete.

## P2.7 selected statutory baseline fields — 7 November 2026

The official NZ legislation CLI route is qualified: installed curl 8.7.1 fetched
substantive HTML for the 2024 repeal Act and current principal Act with HTTP 200,
using exact official targets, bounded time/size, redirects and zero retries. Original
HTML, response headers, extracted provisions and scripts are external in
`/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2-policy`. The initial
urllib attempt produced no expected receipt/output; no success is attributed to it,
and that failure does not invalidate the separately verified curl route.

Principal HTML SHA256 529a47630e1627c4b8e10dcad676d8832afb729b27a0336b13a6e056dacb3795
identifies the official consolidation as at 10 July 2026, observed on its latest route.
Repeal Act HTML SHA256 53e4810bd3361da89780432395081906897899529c9bd78390c8fcf207d450ab
identifies 2024 No 6, as enacted 5 March 2024. Section 2 starts it the day after Royal
assent; the 6 March 2024 result agrees with the current Act's repeal history notes.
Original source bodies remain unmodified; whitespace normalisation is for assertions.

- Current section 20M (LMS809014), within repealed Part 1B subpart 1, is explicitly
  repealed; the removed approved-smoked-tobacco-retailer maximum scheme is not an
  active baseline outlet reduction. Do not infer absence of all other retail rules.
- Section 57I (LMS809297), smoked-tobacco nicotine limits, is expressly repealed on
  the same date. Historical denicotinisation assumptions remain counterfactuals.
- Section 40 (LMS428470) retains the under-18 sale/delivery prohibition. The current
  age rule is verified; the full original-2022 cohort-provision mapping is not.
  The extractor's initial `generation` entry duplicates current section 40 context,
  so review excludes it as independent proof of the historical cohort repeal.
- Section 20FA (LMS1448824) prohibits disposable vaping devices, with insertion on
  17 June 2025. This is distinct from banning all vaping or measuring actual compliance.
- Section 100 (LMS428822) contains annual reporting requirements. The Ministry's
  legacy section-35 label does not identify that current provision. The Act delegates
  sales-related fields to regulations; section 100 alone does not resolve the
  national summary's product conversion, duty-free or stock-consumption bridge.

The guarded stdlib HTML extraction verifies actual provision containers and IDs,
repealed markers, date notes, statutory text and original hashes; it does not use
keyword occurrence in the contents as proof that a repealed heading remains active.
`decision-definition.md` now records only these qualified statutory fields. No
numeric policy-effect parameter, price elasticity or implementation rate is adopted.

This latest route was read after the fixed 6 November 2026 evidence/policy cut-off;
it is not a frozen capture made on that date. Its HTML has a dynamic alert-loading
placeholder, so no live alert state or absence of later/prospective amendments is
asserted. Actual regulations, excise schedules, service/cessation coverage, costs,
enforcement, retailer counts, AU baseline and original-cohort mapping remain open.
Official legal access is also separate from exact archive rights/destination admission.
No external message, source upload, native write, empirical fit or held-out result
occurred. P2 remains active; maintained-code tests and numerical replay are unchanged.

## P2.8 retail/cessation parameter and formula bridge — 7 November 2026

The source-linked SHINE supplement is saved externally and verified by its ZIP/PDF
hashes; complete Appendix D pages 34 and 36 were rendered and inspected. Independent
Decimal beta moments agree with installed SciPy 1.18.1, and the six source Table S22
elicitation columns reproduce their printed averages and approximate range-based SD.
The retail beta is internally coherent, while the prior denicotinisation mean conflict
remains uncorrected. A new source-expression quarantine records a printed survivorship
complement mismatch on page 36; no executable-code fault is inferred from that text.
See the appended phase1-nz-model-appraisal.md and the existing P2 receipt for locations,
hashes, checked values, distinctions and the retained exclusions.

This qualifies what the existing retail contrast actually represents: a transported,
null-inclusive aggregate consumption scenario inspired by a one-off source transition
assumption, not a full SHINE transition implementation or a fitted causal NZ effect.
The current src/tobac/retail_case.py blob is identical to a818f28, so its previous full
suite/finite numerical replay is reused. New diagnostics are guarded at 4 GiB/40 min;
Python 3.15.2 / SciPy 1.18.1, status 0, sampled peak 127.0 MiB. They establish arithmetic
and source interpretation only. No observation admission, parameter replacement,
fit, empirical policy contrast, held-out prediction or monetary VOI occurred.

For this formula task, the same bounded context profile now selects the NZ model
appraisal and retail source/test, replacing the unrelated coverage audit/test and
accumulated source-reconciliation narrative in context selection only. Files and
history remain intact, the 100,000-byte ceiling is unchanged, and current P2
constraints remain in the decision definition/task card. Archive/source admission,
policy transport and calibrated/validated empirical inputs still gate fitting.

## P2.9 executed source compatibility audit — 7 November 2026

`scripts/reconcile_empirical_candidates.py` reopens the pinned originals through the
existing source guards and uses the declared, methods-byte-bound NZ adult survey
Scope. It is a reproducible audit, with no new observation/admission authority. It
keeps the source periods and product/quantity semantics distinct, rather than joining
survey-start labels to calendar years or allocating stock and sales to fieldwork.

Actual 2024/25 scope: eight selected NZHS candidates out of 87; 82 original SAP0240
quarters with five overlapping actual fieldwork (including 2025Q3 mop-up); four
nominal quarter-end ERP benchmark occasions with two provisional flags; the same
4,338,100 cross-vintage diagnostic without replacing the survey benchmark. Two
calendar-year release records overlap. The original September 2026 HS10 import/
export sources contribute 15/four HS24 candidates, zero overlapping months. No
missing trade is read as zero flow; no weighted price, quantity conversion, covariance,
joined observation or likelihood is constructed. Different source units remain explicit.

Two final real-source reports are byte-identical. Focused tests pass 87, corrected
full Nox tests pass 1,299 / 22 capability skips with 92% src-only coverage, and strict
whole-source typing has no errors or warnings. Preserve the first failed test run
and the isolated-scratch recovery evidence; the code was not weakened to pass it.
See phase2-matching-task-card.md and the P2 receipt for exact invocation, hashes,
resource evidence and limitations. The unchanged finite reference remains separately
qualified. This advances executable source reconciliation, not P2 acceptance: historical
trade and earlier scope coverage, source admission, calibration, a supported policy
contrast and frozen holdouts remain open. No empirical fit or information comparison.

## P2.10 historical trade coverage

The 2024 and 2025 Stats NZ annual HS10 import and export archives cover every
month from July 2024 through July 2025 in both flows. The existing reconciler
reports 363 import and 162 export HS24 candidates across the two calendar
years. These counts cover the full archives. The intersecting fieldwork
window includes partial first and last months. Source quantity units include
KGM, KTC, LTR, MIL, NMB and blank entries. The report preserves separate
domestic export, re-export and total export fields.

The four publisher archives, ZIP/member hashes, header mapping script,
derived CSVs, configuration and executed report are retained in
`/Volumes/PortableSSD/tobac-p2-historical-trade.e1sT5C`. The annual headers
were mapped to the existing CLI names and the annual records concatenated
by flow with Polars. Both guarded commands exited zero. The original-source
receipt hash is
`1dfefacecd8ef5b0b170ef6e822efce2bfcb792a98cfffe5c8ec0c247ae4c20b`.
The executed report hash is
`8ac4db8401ad4799666d55adbd98ba0c6efae578d94413f9a440c64e50c39caf`.
Source admission, product conversion, calibration and held-out fitting
remain open.

## P2.11 trade product and unit coverage

The prior turn established historical month coverage. The product audit
checks the pinned CSVs over the 13 intersecting months and finds 203 HS24
import records and 91 export records. Tobacco cigarettes (240220) include
a MIL code present in both flows in all 13 months and a heavier-cigarette
KTC code present in four import months and one export month. Smoking tobacco
under 240319 includes KTC records in both flows in every intersecting month.
The six-digit group also needs its full product descriptions for allocation.
Cigars, water-pipe products, heated tobacco and other nicotine products
require separate dispositions. Absent product-month rows remain missing.
Any eventual stock-flow reconciliation needs explicit product conversions,
an export/re-export accounting rule and coverage of stock and lawful flows.

The bounded Polars audit and JSON are in
`/Volumes/PortableSSD/tobac-p2-historical-trade.e1sT5C`.
The first execution treated month bounds as column names. Explicit string
literals corrected the filter and the second execution exited zero. The
report SHA256 is
`112bbcdb46d1b7d1bf2cf3b99bc5a7c48073b2626d50dafbc10f0b622fc68964`.

## P2.12 reported cigarette trade mass ceiling

The preceding product audit identified HS10 2402209000 as the count-based
cigarette series. The [Stats NZ quantity dictionary](https://www.stats.govt.nz/large-datasets/csv-files-for-download/overseas-merchandise-trade-datasets/)
defines MIL as thousands and KTC as kilograms of tobacco content. The
description on each count-based series specifies at most 0.8 kg tobacco
per thousand cigarettes. The checked July 2024–July 2025 records contain
927,834 thousand imported sticks and 43,280 thousand total exported sticks.
The latter comprises 450 thousand exports and 42,830 thousand re-exports,
with the identity checked in each of 13 months. Multiplying the reported
counts by the classification ceiling gives 742,267.2 kg for imports and
34,624.0 kg for total exports. These ceilings apply separately to reported
flows and include the entire first and last months. A difference of the
ceilings cannot bound net tobacco mass. Actual weights, withheld flows,
stock changes and the heavier cigarette series remain separate inputs.

The guarded Decimal audit reads both pinned CSVs and verifies unique
monthly records and final status. Its source and result are retained in
`/Volumes/PortableSSD/tobac-p2-historical-trade.e1sT5C`. Result SHA256
`25c84d74f1c6d06c84537e35c1e164a094e3dcef78ead6e1cc6a7a74b0ede260`.

## P2.13 reported net cigarette trade interval

The heavier cigarette line (2402201000) reports 596 kg of imported tobacco
content across four rows and 1 kg of re-exported content in one row. The
lighter line (2402209000) contributes between zero and its classification
ceiling on each side. Subtracting opposite endpoints yields an outer
interval of −34,029 to 742,862.2 kg for net tobacco mass in the reported
rows of both lines across July 2024–July 2025. The interval spans zero.
Its width follows from unknown tobacco mass per stick. The calculation
uses complete calendar months and applies only to visible rows, with
withheld flows, stock movements and survey alignment still open.

The bounded Decimal audit checks the pinned CSV hashes, unique heavy-line
months, KTC units and the export identity. The script and report are under
`/Volumes/PortableSSD/tobac-p2-historical-trade.e1sT5C`. Report SHA256
`386cb0c3440609d29ba40da6f66a5bd204e27dbfdd571b697d5e7e8718f333ed`.

## P2.14 stock-boundary identification check

The prior net-trade interval constrains visible border flows. The existing
ledger uses releases plus opening stock minus closing stock and separate
lawful adjustments. Even with the adjustments fixed at zero, any
nonnegative consumption vector fits a given release vector when opening
stock is free. Start from cumulative offsets (d_0=0),
(d_t=d_{t-1}+R_t-C_t). Set every stock boundary to
(d_t-\min_j d_j). These boundaries are nonnegative and reproduce (C_t)
exactly. Holding the reported trade records fixed does not constrain this
construction without a separately supported relationship between border
flows, releases and inventory.

The guarded integer audit verifies the workbook consumer hash and uses
the rounded annual release totals of 968 and 755 tonnes. Three illustrative
stock paths give consumption pairs of (0, 0), (968, 755) and (2,000, 2,000)
tonnes under the same releases. They are feasibility witnesses in source
mass units. Empirical ledger admission still requires matched product,
duty-free and time coverage and credible stock constraints.

The script and result are under
`/Volumes/PortableSSD/tobac-p2-historical-trade.e1sT5C`. Result SHA256
`18d3518cdbf697e785d942d8ca37f15b5bdc591aa12124fdc0f668a2649abf3d`.

## P2.15 Customs and Stats NZ import cross-check

[Customs OIA 25-187](https://www.customs.govt.nz/media/adyjbo2l/volume-and-excise-collected-on-various-tobacco-imports.pdf)
Appendix 1, PDF pages 6–7, reports quantities by entry lodgement month from
a 28 March 2025 extract. The light-cigarette tariff line reports thousands
of sticks despite the request specifying kilograms. Visual transcription
and the pinned Stats NZ CSV comparison give differences of −63, +1, −1,
+32, 0, 0, +1 and +69 thousand sticks from July 2024 through February 2025,
respectively, for a net difference of +39 thousand sticks. Keep the
extracts separate and treat them as linked Customs-derived evidence.
Vintage, timing and coverage remain possible explanations for the differences.
The duty column is monetary, and the appendix supplies neither actual tobacco
mass for the light line nor a measured opening or closing stock.

The original PDF, page renders, script and result are under
`/Volumes/PortableSSD/tobac-p2-historical-trade.e1sT5C`. The guarded
comparison passed. Result SHA256
`0ef4fafde0b23aad6c7a1d4c838e8563106d09aade8393fc9b1ec7393d072a58`.

## P2.16 RYO source-vintage cross-check

Customs OIA 25-187 Appendix 1 (PDF page 7) labels its mass series as
manufactured tobacco used in RYO. The inspected Stats NZ records distinguish
2403199015 cigarette-smoking tobacco from 2403199010 pipe tobacco within
the same HS6 group. Comparing the cigarette-smoking line in KTC units gives
Customs-minus-Stats differences of −45, 0, +1, 0, +1, −4, −2 and 0 kg
from July 2024 through February 2025. The aggregate difference is −49 kg.
This supports retaining full HS10 identity in the source mapping and treating
the two extracts as dependent vintages. Pipe tobacco remains a separate row
where it appears. The comparison still requires the declared source units
and measurement dates before empirical use.

The guarded audit passed against the pinned Stats NZ file and the previously
rendered Customs page. Script and result are retained under
`/Volumes/PortableSSD/tobac-p2-historical-trade.e1sT5C`.
Result SHA256
`6571fc19c72120371be4ddbff1c699553577a80c56176c1988e4a54bd837017c`.

## P2 terminal source packet and admission gate audit

The source packet through `2f16206` is ready for the existing integrator's
consideration. P1 is frozen at `403600b`; P2.2 closes at `b1cb8f4`;
the executable candidate reconciler is `12c0716`; P2.10–P2.16 add historical
trade, product/unit, stock-feasibility and Customs-vintage evidence above.
These later additions change metadata only. Original sources and derived
candidate artifacts remain at their recorded external paths.

The latest full software receipt remains 1,299 passed and 22 capability skips,
with 92% source coverage and zero strict typing errors or warnings. The
initial storage failure and subsequent corrected full run remain recorded.
No new model code requires repeating that unchanged software evidence.
The existing numerical replay is reference-model evidence, not a fitted
empirical result.

Current readback finds the native/integration checkout clean at
`c239b18139b91dc170758f88a343b987fb7d880f`. Its owner remains chat
`01a19a6e-2e47-7b10-8a35-4e7d7fedb965`; this lane has not mutated its
checkout, private bindings or source admission. Phase 0 local qualification
does not close Phase 1 or Phase 2.

The next dependency is the existing owner's source-admission decision using
the frozen packet. Before fitting, the plan also requires resolved rights
and destinations, original-source acceptance, compatible product/period/
denominator and dependence semantics, a complete dated policy contrast,
and a frozen eligible observation/holdout manifest. Source inventories,
mass bounds and stock witnesses cannot close those tasks. No new empirical
baseline, policy fit, held-out predictive score or WBE information result
has been produced. All Phase 1 and Phase 2 acceptance rows remain open.

Proposed single handoff: ask the retained integrator to review this packet
for its existing admission scope and return an exact acceptance or blocker
receipt. It does not authorize publication, native activation or scope
expansion. No message has been sent: the chat messaging tool explicitly
requires human authorization to message the destination chat, and the prior
request has no recorded answer. Further source arithmetic does not resolve
this recurring admission dependency.
