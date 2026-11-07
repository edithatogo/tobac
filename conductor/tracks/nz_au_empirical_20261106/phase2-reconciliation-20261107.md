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

## P2.17 dated cessation guidance and funding context

Independent work after the goal's reactivation qualified a missing part of the
status-quo comparator. The official Health NZ announcement is dated 20 August
2026. The linked guideline's PDF page 2 states publication in August 2026 and
CC BY 4.0 licensing; the publisher page says this edition replaces 2021.
PDF page 82 expressly separates extended treatment from current funding.
Both pages were rendered and visually inspected. No guideline effect estimate
or recommendation has been converted to a population transition parameter.

The Pharmac varenicline page is the November 2026 edition; its SA1845 link
redirects to `/2026/11/01/SA1845.pdf`. The single-page form was rendered and
visually checked, preserving the initial criteria's AND/OR grouping and the
separate renewal criteria. A funded course is capped at 12 weeks; five-month
approval validity and six-month approval spacing are distinct. Initial access
also requires monitored support and prior unsuccessful treatment, with further
conditions retained in the original form. These are constraints on funding,
not observed uptake or effectiveness. No patient-specific inference is made.

The official NRT provider ordering page limits that route to authorised stop
smoking providers and says Pharmac pays the invoices. It supplies no measured
treatment coverage or delivered programme cost. Listed medicine subsidies on
the schedule are not adopted as total resource or incremental programme costs.

All four exact-target CLI HTML reads and three linked PDF reads returned 200
and passed content checks. This qualifies this CLI route despite the web
reader's separate 403 responses for the Health NZ pages; no browser was needed.
Originals, extracted text, page images, scripts and acquisition receipts remain
under `/Volumes/PortableSSD/tobac-p2-cessation.GtD3YW`. The receipt JSON hashes
and exact original hashes are recorded in phase2-context-receipts-20261107.json.
Acquisition peaks were 33.7 and 35.1 MiB sampled group RSS; extraction/rendering
completed under the same 4096 MiB / 2400 s guard, with a 39.0 MiB sampled peak.
The 6 November cut-off is retained separately from 7 November retrieval.

Only metadata changes. Existing full tests/typing/reference replay are reused;
no software, fit or native-admission verification is newly claimed. Complete
policy implementation, service coverage, costs, source admission, calibration
and frozen holdout gates remain open. Goal reactivation did not answer the
pending permission to message the retained integrator, and no handoff was sent.

## P2.18 PubMed S4 prerequisite retrieval

The open monitoring/public-health VOI search now has an executed PubMed edition.
Five connector pages advertise 101 records and return 100 unique hydrated
articles. Exact native ESearch identifies the missing PMID 42659019; the
connector exact-ID request also reports it missing. Native EFetch recovers it
as a PubmedBookArticle. Both routes and the initial incomplete page audit are
retained. The qualified Searchright binary is unchanged at SHA256
ebe162f2d4076f085af0702733d9623f22a2b1783c4d7571b354f3880a93297a.
Its native XML import warns that no PubmedArticle elements exist and yields
zero records. Supported CSV transport/import then accepts all 101 candidates
with zero quarantines. The book's original title, book authors, DOI and all
12 abstract sections are mapped explicitly; no journal is invented.

All 101 imported identifiers equal the native search ID set. Titles and
abstracts round-trip exactly after the importer's outer-whitespace trimming.
The explicit publication-cut-off diagnostic returns the identical ID set.
This is exact-query retrieval evidence, not 101 included studies, screening
or empirical observations. No parameter or likelihood has been adopted.

External originals and scripts: /Volumes/PortableSSD/tobac-p2-search-s4.x181rk.
Terminal receipt SHA256
5b4bbf93281cf6e4d84656af3b752fee605d1ec6aebb565d3f150b2b320c19d3;
explicit cut-off/round-trip receipt SHA256
5757a396519e1dfef5ae3a21edd0497bde2c997cda0dee75703a99f72b46ba35.
Local guarded logs: outputs/nz-au-phase2-search-s4-20261107. Native source
reads used at most 31.0 MiB sampled group RSS; local import/audit used at most
1.5 MiB. Existing 4096 MiB / 2400 s guard and actual Python 3.15.2 were retained.
No maintained executable source changed, so unchanged software/reference checks
are reused. S1/S3/S5 PubMed, screening, other Phase 1 gates, source admission,
calibration and eligible frozen holdout still precede the P2 fit. Current owner
readback remains idle with only Phase 0 accepted at c239b18; no chat message sent.

## P2.19 PubMed S5 and source-kind correction

Native publication-cut-off ESearch and ten connector pages reconcile 475 IDs.
The connector hydrates 474; the exact-ID request also reports PMID 30212113
missing. Native EFetch recovers the PubmedBookArticle chapter. The chapter's
ArticleTitle and three chapter authors are preserved, rather than substituting
the parent book title or its four editors. Three author-field continuations
on parent offset 300 recover all 395 authors of PMID 27490260. Source pages,
field fragments, failure evidence and exact request remain external.

The supported CSV import accepts 475 candidates with zero quarantines and
verified identifier/title/abstract round-trip. A subsequent semantic check
finds the importer defaults to journal_article, including the recovered S4
book. Supported CSL imports correct the book and chapter kinds without altering
source titles, abstracts or authors. Corrected S4/S5 candidate sets retain
101/475 IDs. The prior imports and receipts are preserved, with their kind
representations explicitly superseded. No Searchright code or native source
was changed to achieve this correction.

Eight actual title/abstract assessments have recorded per-record reasons and
source pointers. Six go to the full-text queue; two remain pending full-text
transferability assessment. The other 467 are unscreened. These are AI-assisted
single-owner assessments, not independent review, full-text inclusion decisions,
admitted observations or numerical effect extraction. Prioritisation by NZ
mention did not exclude any other country or method.

Originals, transformations, corrected editions and screening data remain under
/Volumes/PortableSSD/tobac-p2-search-s5.jLmFdk. Hash pointers are in the existing
context receipt. Guarded source/read and local audits peak at 38.7 MiB sampled
group RSS; screening-receipt verification peaks at 18.4 MiB. Actual local Python
3.15.2 and the 4096 MiB / 2400 s guard remain in use. Existing maintained-source
software/reference receipts are reused; no new model execution is claimed.
S1/S3 retrieval, remaining screening, current policy completion, archive/source
admission, calibration and frozen eligible holdout remain open. No chat message
or other-owner/native write occurred.

## P2.20 complete S1/S3 candidate retrieval and PubMed memberships

Frozen S1 and S3-v3 concepts compile to PubMed Title/Abstract queries with a
cross-dialect human-review warning retained. Original XML retrieval and
import are executed evidence for these candidate query editions. They do not
resolve that review flag or admit any evidence. The native date cut-off is
6 November 2026; retrieval is 7 November. Initial and final root counts and
available IDs match. S1's nine complete date leaves preserve 695 repeated ID
occurrences and reconcile to 25,067 IDs; S3's single leaf reconciles to 3,048.
Prespecified S1 seeds 36627213 and 41661592, and S3-v3 seed 36627213, are present.

The first acquisition terminates at 9,800 valid S1 records with an HTTP 200
partial XML response and an embedded upstream 503. No scientific rows are
read from that response. One exact 200-ID recovery succeeds under a new file;
the old bytes and receipt are preserved. All 126 S1 and 16 S3 verified XML
batches bind received IDs to requested IDs. Retained response volume for the
successful request set is 498,279,162 bytes, excluding the separate first
failure. Sampled peaks: initial failure 104.6 MiB, successful continuation
128.5 MiB. No resource limit changed.

Searchright native XML imports retain 25,026 S1 and 3,013 S3 journal-article
records. Supported CSL imports retain the source book/chapter kinds for the
other 41 and 35 occurrences. Full imported ID sets, source title/plain abstract
text and author counts reconcile. Article abstract section labels are omitted
by the native importer but retained in original XML. Import passed at 239.1 MiB
sampled peak. Exact PMID membership across the five query families gives
28,913 occurrences, 27,507 unique IDs and 1,388 IDs in multiple families.
This does not assert unique studies or propagate screening decisions.

Originals/scripts/receipts remain under /Volumes/PortableSSD/tobac-p2-search-s1s3.mV6Dai.
Only metadata/hash pointers enter tobac. The context receipt pins the acquisition,
failed/recovered XML, actual import and membership results. Earlier Europe PMC
S1 drift, translation review, grey-source/citation and screening gates remain;
no new eligibility decision, scientific admission, fit or holdout score exists.
No maintained code changed; existing software/reference checks are reused.

## P2.21 wastewater measurement screening

Eight S1 title/abstract records prioritised for the observation model were
assessed against the frozen protocol. This was an AI-assisted first pass.
The source is the retained S1 import at
/Volumes/PortableSSD/tobac-p2-search-s1s3.mV6Dai/s1-imported-records.jsonl,
SHA256 a3145b7a29cabbf9f070296214eefd27ea1348fb5e7f7a34288fb280f10d9a38.
All eight proceed to full-text review. The targeted selection leaves the
rest of the corpus in its existing screening state.

| PMID | Reason for full-text review |
| --- | --- |
| 41447812 | NZ multi-site 2023 sampling directly informs catchment and observation-period matching. Check site-level data availability, flow and denominator definitions, and the ratio used to separate nicotine sources. |
| 37192131 | Queensland pooled urine and wastewater analysis supplies a candidate cigarette-specific excretion calibration. Check shared samples and conversion assumptions before combining with downstream Australian estimates. |
| 32506745 | Australian product, urine and wastewater measurements bridge analyte loads to cigarette use. Separate per-person excretion from per-cigarette calibration and check overlap with other Australian work. |
| 32653706 | Australian reactor and influent experiments inform analyte-specific sewer loss and assay recovery. Check hydraulic conditions before transporting corrections to NZ catchments. |
| 26198173 | Municipal wastewater assay validation informs biomarker choice and analytical uncertainty. Check sampling scope and distinguish normalized analyte loads from consumption estimates. |
| 26980372 | Concurrent Belgian survey and wastewater sampling provides a matched-design comparator. The abstract reports no demonstrated correlation and low survey response. Review uncertainty and sampling alignment before using any validation statistic. |
| 26888732 | Dalian Monte Carlo analysis informs propagation of uncertainty through nicotine back-calculation. Check which inputs drive the interval and whether the cigarette-only attribution is defensible for the target setting. |
| 38154341 | Australian repeated sampling with tobacco and nicotine biomarkers informs temporal comparison. Check dependence on earlier excretion factors and distinguish a sales discrepancy from measured illicit origin. |

The immediate extraction priorities are the NZ site-by-occasion measurement
availability and the Australian calibration lineage. The abstract evidence
supports separate assay, sewer, excretion and population components in the
appraisal. Full-text eligibility, calibration transport, admission, fitting
and held-out validation remain open.

## P2.22 NZ wastewater supplement and occasion matching

The [Kim et al. publisher supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0048969725028657-mmc1.pdf)
for PMID 41447812 returned HTTP 200. The PDF is retained at
/Volumes/PortableSSD/tobac-p2-kim.lBTiOt/mmc1.pdf with SHA256
c2ce1d0c3fcc95e9c49acb5bf403cc2598b999a97b8a9e558557a3aa1614046c.
The article page returned 403 on the checked routes, so this appraisal
covers the supplement and bibliographic record.

Table S3, PDF page 8, contains 142 printed dates across 12 plants. This
matches the abstract's sample count. Whangārei has two blank October
slots. A calendar check finds seven actual dates outside Wednesday or
Sunday, including Auckland West on 18 and 22 May. Use the printed date
as the occasion key and retain the source column label separately.
A weekday contrast requires explicit adjudication of the seven cases.

Tables S13, S15, S17 and S19 provide occasion-level normalized loads for
cotinine, hydroxycotinine, anatabine and anabasine. Preserve duplicate
measurement variability separately from catchment and temporal uncertainty.
Preserve censoring such as below quantification and above detection as
reported. Table S20 describes differing populations and daily flows.
The checked tables supply normalized loads and settlement classifications.
Exact contributing population and occasion flow inputs still require
verification before reconstructing the normalization or joining to survey
denominators. The supplement supports a candidate occasion-level extraction.
Admission, reuse rights, calibration and eligible holdout remain open.

## P2.23 NZ wastewater occasion manifest

The bounded extraction of Kim et al. Table S3 produced 144 explicit
site/month/day slots and 142 unique site/date keys. It retains the printed
cell, the nominal weekday, and a separate status for each slot. The two
Whangārei October gaps retain their missing status and all seven weekday
disagreements retain their printed dates. Every dated cell falls within
its source month. No date was imputed.

The external intake at /Volumes/PortableSSD/tobac-p2-kim.lBTiOt retains
candidate-occasions.csv (SHA256
382c00bdd8f53977578924ce576007617517fea0f6b5912c5c494236a435acc6)
and extract-occasions.py (SHA256
8a12388f1bfdd020e6353606f929f5426858757753b146072f219ddd1feac283).
The script reads the layout-preserving pdftotext output retained beside the
pinned PDF. Python 3.15.2 and the resource guard passed. The explicit
site/month/nominal-day fields provide the bridge to the load tables, whose
site order differs from Table S3. Load cells, normalization inputs and
eligibility still require verification before a fit or holdout.

## P2.24 NZ wastewater load extraction

The bounded extraction joined PDF pages 34, 37, 40 and 42 to the Table S3
occasion manifest by plant, month and nominal day. PDF word positions assign
wrapped values to the twelve source columns. The export retains the printed
load string, collection date, duplicate-measurement mean and SD, and censoring
status. The source load unit is mg/day/1,000 people.

Each analyte has 144 slots and two missing Whangārei October occasions.
COT, COT-OH and ANTA each have 142 quantified cells. ANBA has 25 quantified
cells and 117 reported below LoQ. The extraction retains those 117 cells
as censored with empty numeric fields. Checks confirm 576 unique slot/analyte
keys, missing-date consistency and selected exact source cells, including a
wrapped COT value and a censored ANBA value. Full independent cell review
and sample-specific numeric censoring bounds remain open.

The external intake at /Volumes/PortableSSD/tobac-p2-kim.lBTiOt retains
candidate-loads.csv (SHA256
1ee56fec14d8f81b7d1be1d2ee148f1c29fdc234adcff39dec4095784ef5f942)
and extract-loads.py (SHA256
b92422026b870b83b28d2d92453de9f01da39ee7d2cc1fd1fc8ff10aa4c64574).
The 568 dated analyte cells share 142 collection occasions. Preserve this
grouping for any future holdout. Normalization provenance, admission,
calibration and eligible holdout selection remain open.

## P2.25 NZ wastewater load reconciliation and validation eligibility

A second extraction from the retained layout text matched all 576 cells
in the coordinate-based load export after whitespace normalization. It
reconstructs site rows and wrapped cell tokens from character columns
instead of PDF word coordinates. This is a second algorithm on the same
source with zero disagreements. Counts are 451 quantified, 117 censored,
and eight missing analyte slots. The guarded check passed. The external
intake retains check-loads-layout.py with SHA256
3043948b75b34412e1eb3ecb84f5678c3c8e157c21e4de46bbf3c04c85c49532
and mmc1.txt with SHA256
4675a51a4938a717434aa855ce90157a76722c6f2f31be0692793c3df60f7b7a.

All dated occasions fall within May–October 2023. This source alone
fails the prespecified temporal validation requirement of a complete
year and three earlier complete years. Quantified anabasine is present
at eleven plants, with one to four quantified occasions per plant.
Auckland North has only censored anabasine. Catchment fold eligibility
still depends on matched population and flow provenance, comparable
coverage and a supported censoring likelihood. Dropping censored cells
would select on the response. No eligible fold has been frozen.

## P2.26 Conditional normalization and censoring bounds

Table S20 gives plant-level ANTA concentration ranges in ng/L. Pairing
these ranges with the Table S17 occasion loads gives 142 conditional
intervals for flow per contributing person. If the same concentration
statistic enters the normalized load, the unit relation is
Q/P = 1000 × normalized load / concentration, in L/person/day.
The lower endpoint divides the lower printed-load rounding bound by
the upper concentration rounding bound. The upper endpoint reverses
those choices. These intervals assume nearest rounding and that the
site range encloses the occasion concentration. They identify a ratio
conditional on the published processing and leave flow and population
separately unidentified. They are derived from the same assay data and
therefore share its evidence dependence.

At the 25 quantified ANBA occasions the paired ANBA/ANTA printed mean
load ratio cancels a common flow/population multiplier. This diagnostic
retains the assay and source-attribution limitations of both analytes.
For the 117 censored ANBA occasions, Table S19 gives the detection to
quantification interval symbolically. The supplement's visual detection
limit example describes COT calibration standards and says ANBA has a
higher quantification limit. It does not supply a verified effective
ANBA threshold in influent units for each occasion. The seven dilution
cases further motivate checking occasion-specific conversion. Numeric
censoring limits therefore remain open even with conditional Q/P bounds.

The guarded calculation passed for 142 intervals and 25 quantified
ratios. External intake /Volumes/PortableSSD/tobac-p2-kim.lBTiOt retains
check-normalization.py (SHA256
55933dfb8877b5914f5a6c1a2250be5315ee0dcda7c0e29a132bf25fc7717097)
and conditional-normalization.csv (SHA256
0efff53a12b3c91d364c1a26013e3cdf45d11228f0105da0cfb4b9e2f69463b8).
These diagnostics remain candidates for appraisal. Fit and holdout
eligibility still require source admission and supported normalization,
catchment and censoring semantics.

## P2.27 Anabasine threshold and dilution cross-check

Indexed publisher text for [Kim et al.](https://doi.org/10.1016/j.scitotenv.2025.181223)
exposes Table 1 and section 2.4.2. Table 1 gives ANBA LoD 0.5 ng/mL and
LoQ 2.5 ng/mL on the calibration scale. Section 2.4.2 describes loading
100 mL of wastewater and reconstituting the residue in 0.5 mL.
The nominal volume-only conversion under unit recovery and no further
dilution gives 2.5 and 12.5 ng/L on the influent scale.

Table S12 identifies seven distinct dilution-trial occasions, including
two trial factors for Hamilton June Wednesday. Joining these seven keys
to the verified S19 export finds six censored cells and one quantified
cell, Hamilton June Wednesday (5.6 ± 1 mg/day/1,000 people).
Applying a factor of two indiscriminately to that occasion would put its
nominal influent LoQ at 25 ng/L. This exceeds the Hamilton site maximum
of 18.7 ng/L in S20 despite the quantified S19 cell. The inconsistency
rules out that blanket mapping under the volume-only assumptions.
The trial table records tested factors and responses. Effective
sample thresholds require the selected processing path, recovery and
concentration-scale convention. The nominal thresholds remain diagnostic
and the 117 censored cells retain symbolic bounds in the candidate data.

## P2.28 Nicotine-total reconstruction and denominator provenance

Indexed publisher text in [Kim et al. §2.5.5](https://doi.org/10.1016/j.scitotenv.2025.181223)
attributes daily flow to wastewater plants and catchment population to
councils. The data availability statement specifies access by request.
The supplement gives normalized results. The actual plant flow and
council denominator series remain unavailable in the checked sources.

The paper reports a nicotine correction factor of 1.35 for COT and
COT-OH. Using the printed loads, the candidate reconstruction
1.35 × (COT + COT-OH) was checked against every Table S23 mean.
136 of 142 agree within 1.85 mg/day/1,000 people, the maximum rounding
residual if the two source loads and the total each round to a nearest
integer and the factor is exact. Six exceed that tolerance. Hamilton
June Sunday has the largest residual, with 3133 reported and 3123.90
reconstructed. Keep both values and flag the discrepancy pending the
unrounded inputs and exact processing. Treat S23 as a derived summary
of the same metabolites when constructing the likelihood.

The guarded check retained all 142 residuals outside Git at
/Volumes/PortableSSD/tobac-p2-kim.lBTiOt/nicotine-total-crosscheck.csv
(SHA256 0a0341ca8311fb9593a4e5bf58ae71b00d0a6ee38e204c371a9988727b6580f1).
The script check-nicotine-total.py has SHA256
ba5dfb1baa80fcd8139ca77b7955cbf321165a5cd513ede95f5e48ec4a72de82.

## P2.29 Duplicate-measurement spread compatibility

Table S23 describes duplicate-measurement SDs. Under the candidate
linear reconstruction with exact factor 1.35, a joint replicate SD
lies between 1.35 times the absolute difference of the two metabolite
SDs and 1.35 times their sum. With exactly two paired replicates and
the same SD convention, only the two endpoints are possible. The check
widens each printed SD by half its last displayed unit before testing
the resulting intervals.

Of 142 occasions, 137 are compatible with at least one paired endpoint,
two fit the broader correlation envelope only, and three lie outside
even the broader envelope. The strongest discrepancy is Auckland South
on 22 October, with reported total SD 325 and upper bound 105.30
mg/day/1,000 people. The two other broader-envelope discrepancies
are Auckland North on 16 August and 21 September. These checks depend
on the stated linear transform, identical replicate pairs and SD
conventions. The compatible cases establish feasibility under those
assumptions. They do not identify a population covariance or justify
using S23 spreads to calibrate a joint likelihood. Original paired
replicates and processing details remain necessary.

The bounded check passed and retained 142 comparisons externally at
/Volumes/PortableSSD/tobac-p2-kim.lBTiOt/nicotine-spread-crosscheck.csv
(SHA256 462131de4a9ad9bde4a6f3d483199859449e4dce1ce2284a7a11373addf58f91).
The script check-nicotine-spread.py has SHA256
d016a55e9ad4159eb795fc30eb305aa3de422eb99153105bdeba975e788fe2b7.

## P2.30 Australian anabasine calibration lineage

The Adelaide repository accepted manuscript of Zheng et al., DOI
10.1021/acs.est.3c01510, is retained externally at
/Volumes/PortableSSD/tobac-p2-zheng.4lTlnK/manuscript.pdf with SHA256
0447aec602905446b3f743df534f1615d44c327f34a0e1a73ec607247800d232.
Sections 2.4–2.6 and the discussion separate excretion calibration,
sewer correction and sales comparison.

The reported 0.91 µg/cigarette follows from the assumed 900 µg absorbed
nicotine per cigarette, 72% combined metabolite excretion on the
paper's basis and a 0.0014 anabasine-to-metabolite ratio from
deconjugated pooled urine. The printed inputs reproduce 0.9072.
This is a linked calibration estimate. Its uncertainty includes
nicotine intake per cigarette, the literature excretion factor and
the pooled urine ratio. The urine samples were surplus pathology
specimens from south-east Queensland with no exact wastewater
catchment match. The separate 1.07 sewer multiplier is conditional
on local retention time and earlier stability work, DOI
10.1016/j.scitotenv.2020.140551.

The manuscript explicitly reuses earlier wastewater measurements
for the February 2016–December 2017 sales comparison. Its longitudinal
WWTPB source series covers 2012–2017. The resulting sales comparison
and original wastewater observations belong in the same dependence
group. Exact sample overlap with the later 2013–2021 study and the
national Wang study remains unresolved. Keep the factor as an
Australian calibration candidate, with distinct assay, sewer and
product applicability checks before any NZ transport or fit.

## P2.31 Queensland longitudinal comparison and assay overlap

Wang et al. (Water Research 250, 121040, PMID 38154341) explicitly
uses the Zheng et al. 0.91 µg/cigarette anabasine factor in Eq. 2.
Any comparison of cigarette estimates derived in these studies must
share that calibration dependency. The 2013–2017 Wang measurements
use large-volume injection. The 2018–2021 series uses direct injection.
A temporal split across that boundary also changes assay method.

The [publisher supplement](https://ars.els-cdn.com/content/image/1-s2.0-S004313542301480X-mmc1.docx)
is retained at /Volumes/PortableSSD/tobac-p2-wang-queensland.GOsVz8/mmc1.docx
with SHA256 02da1df22e87de9cd23f07e7342e141da5683b686b857b0d02dd1fc92b6347a6.
Table S4 identifies five paired method comparisons on 12–16 February
2017. The same samples appear under both methods. Group the two
measurements by occasion in any calibration or validation split.
Reported signed differences span 0–17% for anabasine, −5–19%
for cotinine and −17–14% for hydroxycotinine. These paired comparisons
inform the assay transition within this catchment and retain their
sample dependence. Table S2 gives direct-injection anabasine detection
and quantification limits of 1 and 3 ng/L in wastewater. These limits
apply to that method and matrix and require separate qualification
before any use with NZ solid-phase extraction.

The supplement provides assay QA and the five paired comparisons.
The complete date-by-analyte series, cross-paper sample keys and a
prespecified eligible holdout still require verification.

## P2.32 National and regional Australian calibration crosswalk

The retained Wang national XML (PMC12887742, Eq. 2–3) gives 1.13
µg anabasine per cigarette and 0.9 mg nicotine per cigarette. The
regional Queensland study uses 0.91 µg anabasine per cigarette.
At fixed anabasine load and with other corrections held equal, the
national factor yields 0.8053 times the regional cigarette estimate.
This is a calibration-only sensitivity ratio. It leaves assay,
sewer, denominator and sampling differences unresolved.

The national supplement eTable 2 lists Queensland sites 2, 5, 12,
22 and 24 in its first anabasine batch and 11, 19, 23, 28 and 36 in
its second. The first pools one week of daily samples every two
months. The second pools one week of daily samples monthly.
Sites 22 and 24 have first-batch population bands that contain the
regional study's approximate population of 100,000. That filter
identifies possible matches only. The table supplies coded site
identities and bands, while §e2.2 describes plant questionnaires for
daily flows and interpolated census populations from boundary overlays.
The table does not resolve a cross-paper plant identity or link the
regional daily measurements to national composite pool members.
Treat overlaps as unresolved when evaluating independence and fold
eligibility. The existing site 33 state discrepancy remains quarantined.

## P2.33 Original denominator for the national calibration

The [Bade et al. accepted manuscript](https://digital.library.adelaide.edu.au/items/4be605da-7620-4946-87f7-460bc02cfc91)
for DOI 10.1002/dta.2874 is retained at
/Volumes/PortableSSD/tobac-p2-bade.WnW42y/manuscript.pdf with SHA256
b6b7402a66a987eb453c2935356bb38655ff647ee0ab085832e2e92ef3e25a88.
The abstract describes 1.13 in per-person daily units. The methods
and results establish the intended per-cigarette denominator. The
authors divide individual urine concentrations by self-reported
cigarettes in the preceding day and multiply by an assumed 1.5 L
daily urine volume. The narrative value 0.75 µg/L per cigarette
gives 1.125 µg per cigarette, consistent with 1.13 after rounding.

Table 2 prints a different normalized mean, 0.78, which gives
1.17 under the same conversion. The printed mass-load median
0.47 is also incompatible with converting the printed concentration
median 1.43 by a common factor of 1.5. Preserve these discrepancies
pending original calculation inputs or an authoritative correction.
The factor is based on ten regular smokers of lawful cigarettes,
with reported daily counts ranging from 2 to 25. The printed
mass-load CV is 104%, with a range of 0.03–5.74. Those participant
summaries do not establish uncertainty for a national or NZ catchment
conversion. Retain the 1.13 factor as a source-linked sensitivity
scenario and keep its denominator, transport and internal reconciliation
conditions explicit. No calibrated likelihood has been admitted.

## P2.34 National residual dependence and calibration sensitivity

Wang national Eq. 2–5 and Figure 4, checked in the retained
PMC12887742 XML (SHA256
6cc389a161ce27d498d20beb959441cbd6161bffed48230f1db751ea4b3d7c23),
derive tobacco nicotine from anabasine using the cigarette conversion.
The national estimates combine remoteness strata with population
weights of 72%, 18% and 10%. The annual tobacco mass calculation
assumes 0.7 g per cigarette. Subtracting the FTI lawful estimate
from that annual mass yields the reported illicit residual.
Treat that residual and the reported annual WBE total as linked
outputs. The residual also inherits FTI coverage and stock assumptions.

Using the rounded published endpoint totals, implied lawful inputs
are 13,300 tonnes in 2017 and 6,900 tonnes in 2023. A one-factor
arithmetic diagnostic holds those inputs, all observed loads and
other conversions fixed and replaces 1.13 with 0.91 µg/cigarette.
The endpoint residuals then move from 1,350 and 3,400 tonnes to
approximately 4,892 and 5,890 tonnes. The endpoint increase changes
from 2,050 to about 998 tonnes. This calculation tests dependence
on the factor and rounded inputs. It does not estimate illicit use,
transport the Queensland factor, or supply an uncertainty interval.
Any empirical comparison needs a common calibration basis and
separate verification of lawful-flow coverage.

## P2.35 Australian lawful comparator provenance

Wang reference 28 resolves to the June 2025 FTI report for 2024.
The original is retained externally at
/Volumes/PortableSSD/tobac-p2-fti.nKsvfF/report.pdf with SHA256
b23475ed9abee1d46f31d76b6ff19c02d840b56ddcb649f0c342ddea81fd9087.
Sections 3.3 and 4 distinguish domestic sales from lawful traveller
imports. Domestic manufactured and RYO sales combine scanned retail
transactions and industry-supplied sales. The traveller component
uses arrivals, smoking participation assumptions and the allowance.
The report calls their sum consumption, but the measured basis of the
domestic component is sales and the traveller component is modelled.
The study was commissioned by tobacco companies and the disclaimer
states that inputs were unaudited and reproduction is restricted.

The implied Wang lawful endpoints from P2.34 match the displayed FTI
Figure 4-1 domestic sales at chart precision. That coincidence cannot
establish whether Wang used domestic sales alone or the total with the
small traveller component. The exact annual input series, stock
adjustment and product-to-mass treatment remain open. Keep the lawful
series and Wang residual linked in the dependence map. Source
verification supports comparator appraisal and leaves empirical
admission and rights to reproduce the underlying material open.

## P2.36 Australian administrative clearance comparator

The [ATO 2024 tobacco tax gap edition](https://www.ato.gov.au/api/public/content/0-882626e8-a57b-4b7a-ab16-0894492a4ff2)
reports 7,736 tonnes of lawful clearances for financial year 2022–23.
Its reported market total of 9,392 tonnes reconciles to clearances
plus the estimated 1,656-tonne net illicit gap. Gross attempted
supply is a different quantity that includes intercepted material.
The original is retained at
/Volumes/PortableSSD/tobac-p2-ato.zYOhCK/report.pdf with SHA256
55548c04af658ffea51933a3593eed1c99e9bf2c8763313b6f0dda8ab9a7c734.

The lawful-clearance row offers an administrative comparator to
the FTI retail series. ATO's 7,736 tonnes falls between the rounded
FTI calendar-year domestic sales values of 8,500 and 6,900 tonnes
for 2022 and 2023. The overlapping periods prevent an exact match.
For an aligned period, reconciling clearances with retail sales
requires a bridge for changes in stocks after clearance, coverage
and other flows. Traveller allowances also need a separate basis.
The ATO illicit gap is modelled from importation, cultivation,
historical warehouse leakage and enforcement adjustments.
Keep those components grouped with their enforcement inputs.
The fiscal-year administrative series is a candidate comparator
pending a period and stock bridge. A direct substitution into
Wang's calendar-year residual would confound those differences.

## P2.37 NZ wastewater candidate review packet

The external intake now contains a single review manifest binding
the original supplement, occasion and load extracts, and three
diagnostic tables by SHA256. The bounded assembly verified that all
142 plant/date keys occur in each diagnostic and have exactly four
analyte statuses in the load extract. It records 451 quantified and
117 censored dated cells, preserves whole-occasion grouping, and
identifies nicotine totals and normalization diagnostics as derived.

The artifact is
/Volumes/PortableSSD/tobac-p2-kim.lBTiOt/candidate-review-packet.json
(SHA256 e311db792b39a967146061c7fc156955f5d6cb9c4125e4964be80b2e760ef21d).
The assembly script has SHA256
1fcee31e12b1072c2eacbc40ea95873ccc2eb479919977277f4d03e27d7c8c08.
This review packet has zero admitted observations. It records the
remaining rights and archive readback, contributing population and
occasion flow provenance, effective censoring and processing, paired
replicates, calibration transport and comparable holdout requirements.
The current integrator checkout still reports c239b18, covering Phase 0.
The proposed admission handoff remains pending messaging authorization.

## P2.38 NZ survey fieldwork and wastewater overlap

The Ministry's 2022/23 methodology report, Table 5, gives 19 July
2023 as the last collection date. Three nominal sampling quarters
were opened, with overlapping actual interview windows. Its fourth
quarter was unopened. The 2023/24 methodology report, section 9,
gives 13 July 2023 as the first collection date and 24 July 2024
as the last. These are national fieldwork envelopes.

Comparing the 142 Kim plant/date keys with those inclusive envelopes
gives 56 occasions within 2022/23 only, 76 within 2023/24 only and
10 within both. The overlapping occasions occur on 16 July (four)
and 19 July (six). This date check uses the verified Table S3
manifest. Assigning waves by a 1 July boundary would discard the
earlier wave's overlapping fieldwork. The annual survey aggregates
do not supply interview-level timing, plant catchment assignments
or age-aligned contributing populations. Retain both wave memberships
for the ten overlapping occasions as coverage metadata and require
a supported geographic and estimand bridge before a numerical join.

- [2022/23 methodology report](https://www.health.govt.nz/system/files/2023-12/methodology-report-2022-23-new-zealand-health-survey-dec23.pdf)
- [2023/24 methodology report](https://www.health.govt.nz/system/files/2024-11/methodology-report-2023-24-new-zealand-health-survey-nov24.pdf)

## P2.39 Wellington catchment candidate check

The public [Wellington Water catchment layer](https://gis.wellingtonwater.co.nz/server/rest/services/Hosted/Wastewater_Treatment_Plant_Catchments_View/FeatureServer/0)
describes a 29 June 2021 InfoAsset export. Its native API returns
distinct Moa Point and Western plant polygons. The bounded candidate
query returned both named features in NZTM2000 (EPSG:2193) with
closed rings. The polygons are retained externally at
/Volumes/PortableSSD/tobac-p2-wellington.MjqdNf/candidate-polygons.json
(SHA256 6aaddddd74633ec55828cfab2f48d2facb9aaf0c04178b1b6cc790541e1351db).

The [September 2023 ESR surveillance report](https://www.phfscience.nz/media/mybppfcs/esr-wastewater-monthly-surveillance-report-september-2023.pdf)
lists these as separate Wellington sites, with populations of
168,000 and 14,000 respectively. Its retained PDF has SHA256
7c79d06da42f33272ca4d65abb0023ecabd01118d513ff65f673b737be4d572f.
Those populations are twelvefold apart and apply to that surveillance
report. Kim Table S3 identifies twelve occasions only as Wellington.
The public operator layer and contemporaneous surveillance report
establish candidate catchments, while the plant key, boundary vintage,
age structure and denominator used by Kim remain unverified.
Keep the Wellington join pending a source crosswalk.

## P2.40 September 2023 surveillance roster crosswalk

All twelve Kim labels were checked against Appendix B of the retained
September 2023 ESR report. Seven labels covering 82 occasions have a
single same-name candidate after normalizing the Whangārei macron.
Dunedin and Wellington account for 24 occasions and have three and
two named candidates respectively. The other 36 occasions use
Auckland Central, North or South, whose literal labels do not appear
in that roster. The report has other Auckland site names and a
source-supported alias mapping remains necessary. Even the single
label matches require confirmation of the sampling location and the
denominator used by Kim. Westport, for example, is listed as grab
sampling in the ESR roster, which is programme-specific metadata.

The candidate CSV keeps the published ESR population and sampling
method separate from the Kim occasion counts. It retains every
ambiguous candidate and blank fields for unresolved aliases.
No candidate population was joined into the load table. The CSV is
/Volumes/PortableSSD/tobac-p2-wellington.MjqdNf/roster-crosswalk-candidates.csv
with SHA256 7d15d4fc2ba7998ef757d2b67ae1ef3b917b22ae81c64e096a44eab686d42502.
The counts reconcile to the 142 dated occasions.

## P2.41 Study sampling rules and population-class crosswalk

Figure S3 on PDF page 6 is a settlement map. It shows a single
Auckland marker and lacks plant identifiers. Table S2 on page 7
retains the settlement classes used by the study. Indexed publisher
§2.3.1 defines major urban as a plant-served population above 100,000
and large urban as 30,000–99,999. Applying these definitions to the
separate ESR roster narrows the Wellington candidates to Moa Point
and the Dunedin candidates to Tahuna. The screen is conditional on
the study and roster using comparable catchment population bases.
It does not identify the denominator used in the published load.
The three unresolved Auckland aliases remain open. Section 2.3.2
describes inlet autosampling, while the ESR Westport row describes
grab sampling for its own programme. Keep those sampling protocols
separate.

Section 2.3.1 explicitly permits Tuesday or Thursday as Wednesday
replacements and Monday as a Sunday replacement. All seven flagged
Table S3 dates satisfy those rules. Six are weekday replacements.
Auckland West on 22 May was collected Monday in the nominal Sunday
slot. Preserve the actual weekday for calendar-based analysis and
the nominal slot for reconstructing the paper's contrast. The
study also attributes the two missing Whangārei October occasions
to plant maintenance. These checks resolve scheduling semantics
without changing the original dates or imputing load values.

[Publisher article](https://doi.org/10.1016/j.scitotenv.2025.181223)

## P2.42 Earlier NZ wastewater comparator and source scope

Kim cites Chappell et al. (PMID 35760179) for the settlement
classification. The cited study measures other drugs and its
bibliographic record supplies no Kim plant alias crosswalk.
It belongs in the methods lineage rather than the nicotine
observation series.

Trowsdale et al. (PMID 33715226) collected samples from seven
plants in three regions for seven consecutive days around the
March 2018 census. The original abstract reports the nicotine
result as 1,528 cigarette equivalents per day per 1,000 people.
Kim cites the earlier result as 1,910 mg/day/1,000 people and
compares it with a population-weighted 2023 estimate of 2,467.
The two 2018 summaries imply a conversion of 1.25 mg per
cigarette equivalent. This is an arithmetic cross-check on the
printed summaries. The available publisher abstract does not
verify the original conversion or its weighting.

The 2018 survey-aligned design offers a candidate external
comparison for total nicotine. Its single week and the later
six-month campaign leave the complete-year validation requirement
unmet. Comparable plant keys, denominator vintages, analyte
calibration and averaging weights are needed before interpreting
the difference as a change over time. The 2018 aggregate adds
no independent tobacco-origin measurement.

- [Chappell study](https://pubmed.ncbi.nlm.nih.gov/35760179/)
- [Trowsdale study](https://pubmed.ncbi.nlm.nih.gov/33715226/)
- [Kim study](https://doi.org/10.1016/j.scitotenv.2025.181223)

## P2.43 Trade coverage during NZ wastewater collection

Stats NZ's final 2023 HS10 import and export files cover all six
calendar months intersecting the 142 wastewater occasions. Polars
identified 78 import and 45 export rows in chapter 24 for those
months. Both flows have six monthly rows for 2402209000 in MIL
and 2403199015 in KTC. The heavy cigarette line 2402201000 appears
once among imports and has no displayed export row in this window.
Preserve distinct product codes, units and export/re-export fields.
These are national monthly border flows. Any catchment or occasion
allocation and stock-to-consumption linkage remain unverified.

The first audit stopped when sorting mixed null and string units.
The corrected run counts nulls explicitly and retains 14 import
and three export rows without units. The first partial extract is
preserved. Guarded Python 3.15.2 audit v2 passed and verified
unique month/HS10 keys within each flow.

Originals and outputs remain under
/Volumes/PortableSSD/tobac-p2-trade2023.3PoIyO. SHA256 pins are:

- Imports ZIP: 2a50a505f89cc07b2e533725e8915b1305ada9d4a5f6530ca8e239177f945727
- Exports ZIP: c3e3376d0bd0418454db0f9e202c6df13c5204e801ad0ea8fecd48eb97d8408a
- coverage.json: da78b7fb07618e1ea1a5d83244a1ef10bc69a1285951221b3caa641e1303741a

[Stats NZ trade datasets](https://www.stats.govt.nz/large-datasets/csv-files-for-download/overseas-merchandise-trade-datasets/)

## P2.44 Occasion-level context coverage keys

The bounded Polars check maps all 142 unique dated plant occasions
to six national trade months, three price and estimated resident
population quarters, and the single 2023 annual release period.
Quarter counts are 48, 72 and 22 for Q2, Q3 and Q4. It retains both
survey fieldwork memberships where the annual waves overlap.
The price and population files were checked against their existing
byte pins and source headings. The release check reads the existing
2023 source row of 1,052 tonnes.

The output contains period keys and survey envelope flags. These
keys preserve the many-to-one source relationships for a later
admission review. Quarter-end population figures do not establish
the contributing population on any sample date. Quarterly prices
are national index-derived proxies. Full calendar-year releases
and revised trade and population editions require explicit availability
and stock treatment for a prospective held-out comparison.

The external output
/Volumes/PortableSSD/tobac-p2-trade2023.3PoIyO/occasion-context-keys.csv
has SHA256 3ee1d4670696e35f5bd13cba59a830914fbb9ef9bbe961769a6863228f1363b6.
The guarded assembly script occasion-coverage.py has SHA256
b90467f9248c5b0d9248a455f3705ed8741bb605c8ff074d10086da701af5613.

## P2.45 As-of availability of occasion context

All 142 occasions precede the end of their matched trade month,
price quarter and release year. This checks availability for a
prediction dated at the sampling occasion. The matched complete
period values would use information after that origin. For example,
Stats NZ published the September 2023 CPI on 17 October, after all
September sample dates. The retained 2023 HS10 annual archives are
the final September 2026 edition. The retained population edition
uses a census base that Stats NZ first released on 16 April 2025.
Earlier contemporaneous estimates could differ from these values.

The external occasion-availability-audit.csv retains the checks for
all occasion keys and labels their context as retrospective candidate.
It has SHA256
71b43a276c6b2b4af13297a5853da65a8fbaf9ef845ed9617d00b86c909a9a0e
under /Volumes/PortableSSD/tobac-p2-trade2023.3PoIyO.
A prospective comparison needs an explicit prediction origin and
verified earlier vintages or lagged values. These checks preserve
the same-time context for retrospective appraisal and leave the
prespecified complete-year and catchment validation gates open.

- [September 2023 CPI release](https://www.stats.govt.nz/information-releases/consumers-price-index-september-2023-quarter/)
- [2023-base population release date](https://www.stats.govt.nz/assets/Uploads/Legislation-page/registers/Register-of-people-who-received-2023-estimated-resident-population-data-and-methodology-under-embargo.pdf)

## P2.46 Lagged price availability candidates

The official CPI release dates for 2023 Q1, Q2 and Q3 are 20 April,
19 July and 17 October. Selecting the latest release strictly
before the recorded sampling date gives 66 Q1, 64 Q2 and 12 Q3
occasion memberships. Six July 19 occasions retain Q1 because the
manifest has a date and no collection timestamp. This conservative
rule avoids assuming that the same-day release preceded sampling.

The 20 April Stats NZ release independently confirms the exact
NZD 48.71 per 25-cigarette figure in the retained historical series.
The later CPI release dates are verified, while the exact selected
item values from those contemporaneous editions remain unverified.
The candidate CSV records those 76 values as blank and preserves
release-date eligibility separately from verification of the value.
The national price proxy still requires an appropriate prediction
origin and source admission before model use.

The external lagged-price-candidates.csv has SHA256
5e92d37a0fb518a57def6616b2b205b974ac84a9d774a82292075a4e623b0ef3
under /Volumes/PortableSSD/tobac-p2-trade2023.3PoIyO.

- [Stats NZ March 2023 release and cigarette price](https://www.stats.govt.nz/news/annual-inflation-6-7-percent/)
- [Stats NZ June 2023 release listing](https://www.stats.govt.nz/information-releases/?filters=Housing%2CBuilding+consents+issued&sort=2&start=492)
- [Stats NZ September 2023 release](https://www.stats.govt.nz/information-releases/consumers-price-index-september-2023-quarter/)

## P2.47 Exact archived lagged price values

Stats NZ's June and September release-page metadata links the original
Infoshare CSVs. The archived files each contain one FINAL row for
CPIQ.SAP0240 in their respective reference quarter. The values are
NZD 48.75 in June and NZD 49.01 in September, matching the retained
historical series. The first parser attempt rejected a Windows-1252
byte under UTF-8. Explicit Windows-1252 decoding recovered both rows
while retaining original bytes. The workbook reader was unavailable
and exact verification used the publisher CSVs.

The v2 crosswalk verifies all 142 prior-release price values:
66 at 48.71, 64 at 48.75, and 12 at 49.01. Each release date strictly
precedes its sampling date. The six same-day exclusions remain.
This is verified national price context. It still requires source
admission and a defined prediction origin for a model comparison.

The external intake /Volumes/PortableSSD/tobac-p2-trade2023.3PoIyO retains:

- cpi-june-infoshare.csv SHA256 78a1c0fb1cc8b7dc6333d52d4c921eb00504873c9a8098d1feae24c2b451996d
- cpi-september-infoshare.csv SHA256 5ac018004e2fbd95e46038494ff8377548fa6117d47cd9ee6c9a412bef3bcace
- lagged-price-candidates-v2.csv SHA256 c3f18c3e2a39d70b4a3017821dd46473800614839805b921d603f510ce042fc9

[June release](https://www.stats.govt.nz/information-releases/consumers-price-index-june-2023-quarter/)
and [September release](https://www.stats.govt.nz/information-releases/consumers-price-index-september-2023-quarter/).

## P2.48 Population available before collection

Stats NZ's original provisional national all-ages estimates were
5,151,600 at December 2022 (released 20 February 2023), 5,199,100
at March 2023 (18 May), and 5,223,100 at June 2023 (16 August).
Selecting the latest release strictly before collection assigns
18, 72, and 52 of the 142 unique plant-date keys to those vintages.
One occasion on 18 May and six on 16 August retain the preceding
release under this date-only rule. The June 2023 census-rebased
estimate of 5,200,000 belongs to a later vintage. The crosswalk
provides national context only. Adult and plant-specific contributing
populations require separate evidence.

The external intake /Volumes/PortableSSD/tobac-p2-erp-vintage.zR7Cpn retains:

- 31-december-2022.html SHA256 4afc037f3b1cbcb5ddf4f267417e8f7c8a1c45df959575679b96c514a5e637a8
- 31-march-2023.html SHA256 a88500ba4a06a4790e3d2524722d778b848fd2d431269867d9ecaea69a8dff2a
- 30-june-2023.html SHA256 7b596cf740993f527c21fcb2221fe7bd3371e86eec27a18c2e686129ec9baeb7
- june.xlsx SHA256 498354eea1b3ec90452871ee72008ee3e79c15d6625fd9f4ad6947337bf4f2d9
- lagged-population-candidates.csv SHA256 68a1611f32721a94fccb8c08ee39485d7490fa92ab01f25c35eeccb8530f53d9

[December release](https://www.stats.govt.nz/information-releases/national-population-estimates-at-31-december-2022/),
[March release](https://www.stats.govt.nz/information-releases/national-population-estimates-at-31-march-2023/),
[June release](https://www.stats.govt.nz/information-releases/national-population-estimates-at-30-june-2023/),
and [2023 census rebasing](https://datainfoplus.stats.govt.nz/item/nz.govt.stats/57468853-e913-43df-8cca-51b40bf558f0).

## P2.49 Original June 2023 national population aged 15 and older

In the workbook pinned in P2.48, the June 2023 provisional national
estimate for ages 15 and older is 4,254,800 at the precision of Table 2
(sum E19:G19). Table 3's five-year bands sum to 4,254,780 (M12:M28).
Subtracting the independently tabulated under-15 bands from the all-ages
total gives 4,254,820 (M29 less M9:M11). Both checks round to the
same hundred. The later census-rebased June estimate is 4,230,100,
a difference of 24,700 from the original broad-age sum.

The August workbook is strictly prior to 52 collection dates in P2.48.
This supports a dated national 15+ context value for those occasions.
Earlier dates require their own original age-specific release evidence.
The 15+ estimate does not establish the population served by any plant
or the eligible survey population after survey-specific exclusions.

[Stats NZ original June release and workbook](https://www.stats.govt.nz/information-releases/national-population-estimates-at-30-june-2023/).

## P2.50 Earlier national 15+ context

The original 16 August 2022 release supplies a June 2022 annual
reference for the 90 occasions preceding or on the August 2023
release date. Table 2 E19:G19 sums to 4,159,800 aged 15+, which also
equals the published all-ages figure (5,124,100) less under-15s
(964,300). The August 2023 edition gives 4,153,400 for June 2022
by summing those same broad age bands, a revision of −6,400.
Use the original annual estimate if carrying forward a known
historical context value. The December 2022 and March 2023 release
pages direct age-specific queries to Infoshare and do not expose an
original workbook. Those quarterly age-specific vintages remain
unverified. Any annual carry-forward has a different reference
period and should be explicitly identified in analysis.

External intake /Volumes/PortableSSD/tobac-p2-erp-vintage.zR7Cpn retains:

- june2022.html SHA256 1b5387fdb77870f2ce3bb8616e0f7c650fbfcc06bb75e89bb26ec849115337d6
- june2022.xlsx SHA256 deac1050f80b949094fed32bbaee28ae02956977683197ba8335f4efce922b43

[Stats NZ June 2022 release and workbook](https://www.stats.govt.nz/information-releases/national-population-estimates-at-30-june-2022/).

## P2.51 Annual national age-specific crosswalk

The annual context crosswalk preserves all 142 unique plant-date keys
from P2.48 and selects the latest of the two verified original June
workbooks released strictly before collection. It carries the June
2022 value for 90 keys, including six on 16 August 2023, and the June
2023 value for 52 keys. Each row carries both the estimate date and
publication date. This is an annual context series with carry-forward.
Quarterly age-specific estimates and catchment denominators remain open.

External intake /Volumes/PortableSSD/tobac-p2-erp-vintage.zR7Cpn retains
lagged-annual-15plus-candidates.csv, SHA256
1241a9a77e0d7a776beb245f3d4014abfcb605ced9fcab69c8657605ad74bb32.

## P2.52 Joint time support for lagged national context

An exact inner join of the pinned P2.47, P2.48 and P2.51 crosswalks
preserved all 142 unique plant-date keys. The three national covariates
are constant across plants within each of the 43 collection dates.
Their joint support consists of five chronological regimes.

| NZD per 25 | Annual 15+ ERP | Quarterly all-ages ERP | Occasions | Dates | Plant labels |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 48.71 | 4,159,800 | 5,151,600 | 18 | 6 | 12 |
| 48.71 | 4,159,800 | 5,199,100 | 48 | 13 | 12 |
| 48.75 | 4,159,800 | 5,199,100 | 24 | 7 | 12 |
| 48.75 | 4,254,800 | 5,223,100 | 40 | 12 | 12 |
| 49.01 | 4,254,800 | 5,223,100 | 12 | 5 | 6 |

Both population series change on the August release transition.
The final price regime has half the plant-label coverage of the
earlier regimes. Collection-date fixed effects absorb all variation
in these national covariates. A held-out plant can still share its
national context with training plants. Such a split can assess
spatial transfer conditional on shared context, but cannot establish
performance at a new national price or population vintage. The
counts describe support and do not estimate a price effect.

## P2.53 Shared collection-date support across plants

The 142 P2.47 keys define a bipartite incidence graph with 12 plant
labels and 43 dates. There are two connected components. Invercargill
and Westport share a component with 12 dates. The other ten labels
share a component with 31 dates. An additive plant-and-date design
therefore has rank 53 (12 + 43 − 2). A plant contrast across the two
components is confounded with the date offsets unless an additional
assumption links their time baselines.

Within the October price regime, Wellington occupies two dates in
its own component. The other five labels occupy three dates and
are connected through shared collection dates. Three of the five
October dates have only one label. This limits within-regime
comparison even when conditioning on the same national covariate
values. The graph uses study labels and dates. It makes no claim
about catchment comparability or covariance.

## P2.54 Date support under candidate plant holdouts

Leaving out each plant label in turn, 135 of the 142 test occasions
have at least one training occasion on the same collection date.
Seven dates vanish from training in their respective folds: one
each for Auckland North and Dunedin, three for Auckland West, and
two for Wellington. The other eight folds retain every test date
in training. Counts use the unique P2.47 plant-date keys and keep
all analytes for each key together.

A spatial evaluation with date effects estimated only from training
would require a prediction rule for unseen dates. A score restricted
to shared dates would cover 135 occasions and omit observations
unevenly across plants. Record coverage separately before comparing
scores. These are candidate fold diagnostics. Catchment qualification
and the prespecified holdout gate still apply.

## P2.55 Candidate spatial holdouts with disjoint collection dates

For each held-out label, exclude from training every P2.47 key
whose collection date occurs for that label. Keep test membership
limited to the held-out label and keep each occasion intact. The
12 resulting designs leave 74–118 training occasions and 8–11
training labels per fold. All three price vintages remain present
in every training fold.

Auckland Central, Auckland South and Hamilton each lose the same
four labels from training, including Whangārei. Holding out either
Invercargill or Westport removes both labels from training. The
other seven folds lose only the held-out label. This sensitivity
design removes exact date overlap but retains shared national
vintages, and changes spatial coverage in five folds. It does
not replace the prespecified catchment qualification or constitute
a temporal holdout. No outcomes were used to construct these counts.

## P2.56 ANBA evaluation support by candidate fold

The P2.55 date-disjoint training sets each retain 12–20 quantified
ANBA loads. Held-out labels have zero to four quantified loads each.
Auckland North has 12 censored occasions and zero quantified loads.
A quantified-only ANBA score would omit that plant entirely and
condition evaluation on detection at the other plants. An
all-occasion censored likelihood score requires qualified
sample-specific censoring limits, still unresolved in P2.27.

The first extraction filtered to the nominal dated status and
failed the 142-row count. The corrected extraction used all
nonblank actual dates, retaining seven documented weekday
replacements and excluding two missing slots. Its 142 unique
plant-date keys contain 25 quantified and 117 censored loads.
The coverage audit does not qualify a fold or fit a model.

## P2.57 Published ANBA quantification indicator

All 117 censored ANBA cells on actual collection dates carry the
same printed label, less than LoQ. These support an indicator of
whether a load was quantified under the study protocol. They do
not distinguish detection below quantification from nondetection.
September and October account for 20 of the 25 quantified loads
across 46 of the 142 occasions. July contributes 24 occasions
with zero quantifications. The 25 quantified loads span 16
collection dates.

A future binary evaluation can use the reported quantification
indicator without assigning a numerical load to censored cells.
Its target depends on assay and reporting conditions. It cannot
substitute for the censored-load likelihood or establish the
incremental value of wastewater for predicting the policy outcome.

## P2.58 Partial bounds on sampled ANBA means

Treating published quantified point values as fixed and censored
loads as nonnegative, the quantified sum divided by all observed
occasions gives a lower bound on the unweighted sampled mean.
The May through October bounds are 1.221, 0.233, 0, 0.133,
1.933 and 3.477 mg/day/1,000 people (rounded to three decimals).
The denominator is 24 occasions per month through September and
22 in October. The two missing October slots are excluded.

The zero July bound reflects zero quantified loads. A finite upper
bound from the censoring labels would require numerical thresholds
on the load scale. These lower bounds alone cannot order the true
sampled monthly means. The calculation neither imputes censored
loads nor propagates error in the published quantified point values.
It does not estimate a population-weighted mean or a policy effect.

## P2.59 Conditional upper envelopes from reported site maxima

Table S20 describes concentration ranges for all samples at each
plant and reports numerical ANBA maxima for 11 labels. If those
maxima enclose the concentration statistic for each censored
occasion, a conditional upper load envelope is the plant maximum
plus 0.05 ng/L for rounding, multiplied by the P2.26 upper Q/P
endpoint and divided by 1,000. The 105 resulting censored-cell
envelopes range from 4.238 to 35.474 mg/day/1,000 people. All
25 quantified point values are compatible within printed rounding.
Auckland North has no numerical maximum, leaving 12 censored
cells without this envelope.

This is a sensitivity bound using an observed site summary. It
depends on shared concentration and normalization semantics.
The site maxima incorporate observations across the campaign, so
they cannot supply training-only limits for held-out observations.
Effective assay thresholds and unconditional monthly upper
bounds remain unresolved.

## P2.60 September-to-October ANBA contrast under conditional bounds

Restrict to the ten labels with two observations per month and a
numerical P2.59 envelope. This excludes Auckland North and Whangārei.
Holding quantified points fixed, the September sampled mean is
conditionally bounded by 2.320–10.675 and October by 3.825–7.685
mg/day/1,000 people. The October-minus-September contrast ranges
from −6.850 to +5.365 at the displayed precision. Both signs are
compatible with these constraints alone, even on the balanced
plant panel. The sign remains unresolved under these bounds.
This uses full-campaign site summaries for retrospective sensitivity.
It does not establish predictive limits or a policy contrast.

## P2.61 Censoring precision needed to resolve the sampled contrast

For the balanced P2.60 panel, quantified loads sum to 46.4 in
September and 76.5 in October. With quantified points fixed and
October's eight censored loads bounded below by zero, a strictly
positive lower bound on the contrast requires the sum of upper
bounds on September's 12 censored loads to be below 30.1
mg/day/1,000 people (an average below 2.5083 per occasion).

Under a hypothetical common concentration cap and the P2.26
upper Q/P endpoints, the cap would need to be below about
2.925 ng/L. The nominal undiluted 12.5 ng/L volume-only conversion
from P2.27 would instead give a September upper contribution
of 128.634 on the summed load scale. This is a sufficient-condition
sensitivity calculation. Sample-specific caps or tighter Q/P
bounds could change it. No effective assay threshold was inferred.

## P2.62 Fully quantified ANTA comparison on the same panel

The same ten labels in P2.60 have two quantified ANTA loads per
month in September and October. Their unweighted sampled means
are 8.185 and 7.250 mg/day/1,000 people respectively, a difference
of −0.935. Pairing by plant label and nominal sampling slot gives
13 decreases and seven increases across 20 pairs. Nominal slots
can contain documented weekday replacements.

This comparison holds panel composition fixed and avoids ANBA
censoring. The ANTA measurements share the study's sampling and
normalization and do not resolve ANBA's direction of change.
Neither a sampling-error interval nor a policy effect follows
from this descriptive comparison.

## P2.63 Paired analyte composition on the balanced panel

An exact join of ANTA, COT and COT-OH by plant and actual collection
date gives three quantified values for each of the 40 P2.62 occasions.
The unweighted mean of the occasion-level ANTA / (COT + COT-OH)
mass-load ratios falls from 0.003350 in September to 0.002862 in
October. Fourteen of 20 plant-and-nominal-slot pairs decline. Mean
combined COT and COT-OH load rises from 2,548.75 to 2,602.50
mg/day/1,000 people.

The ratio cancels the flow-to-population multiplier if the three
analytes share that multiplier within each occasion. This is a
composition diagnostic. Differential recovery, source mixtures
and sewer behavior remain possible explanations. The ratio shares
evidence with all three component measurements and should not enter
a likelihood as an independent observation.

## P2.64 Sensitivity to the cotinine denominator

For the 40 P2.63 occasions, the mean occasion-level ANTA/COT ratio
falls from 0.010999 to 0.008935 between September and October
(14 of 20 paired declines). ANTA/COT-OH falls from 0.004837 to
0.004223 (13 paired declines). The sign of the sampled mean change
persists with either denominator. Meanwhile the COT-OH/COT ratio
falls from 2.278 to 2.114 (13 paired declines), so assuming a fixed
empirical metabolite ratio would discard observed composition
variation. These comparisons reuse the same measurements and
retain the shared-multiplier and assay qualifications in P2.63.

## P2.65 NZ statutory excise inputs for the policy baseline

The order effective 1 January 2026 sets NZD 1,309.71 per 1,000
manufactured cigarettes at or below 0.8 kg tobacco per 1,000 and
NZD 1,866.34 per kg tobacco content for cigarettes above that
threshold and other smoking tobacco. Rates exclude GST. Customs
reports a 2.96% indexation based on the 12 months to September 2025
using all-groups CPI excluding credit services. The light-cigarette
rate implies NZD 32.74275 excise per pack of 25 before GST.
Weight-based rates require actual tobacco content. This dated
schedule supplies statutory inputs and leaves pass-through,
retail prices, and the accepted full policy baseline open.

[Amendment order](https://www.customs.govt.nz/media/qkvjprql/excise-and-excise-equivalent-duties-table-tobacco-products-indexation-2025.pdf)
and [Customs rate notice](https://www.customs.govt.nz/about-us/news/important-notices-archive/important-notices-archive-2025/new-excise-duty-rates-for-tobacco-products-from-1-january-2026).

## P2.66 Australian statutory excise inputs for the policy baseline

Effective 1 September 2026, the Commonwealth Gazette sets excise
at AUD 1.55274 per stick under item 5.1 and AUD 2,587.90 per kg
of tobacco content under item 5.5. The corresponding customs
notice covers specified imported products from the same effective
date. The per-stick rate implies AUD 38.81850 per 25 sticks.
The 0.8 g per-stick classification boundary differs from the
0.60 g equivalisation weight used to set the per-kg rate:
1.55274 divided by 0.00060 equals 2,587.90. The latter is a
tariff calculation parameter and supplies no empirical conversion
for wastewater, sales or trade mass. Ordinary indexation uses
AWOTE in March and September. Keep these rates separate from
historical sample dates and from retail price or pass-through.

[Excise gazette](https://www.legislation.gov.au/C2026G00551/asmade/2026-09-01/text/original/pdf),
[customs gazette](https://www.legislation.gov.au/C2026G00591/asmade/2026-09-07/text/original/pdf),
and [Treasury equivalisation schedule](https://treasury.gov.au/sites/default/files/2025-12/p2025-721342.pdf).

## P2.67 NZ excise during the 2023 wastewater campaign

The 1 January 2023 schedule sets NZD 1,177.75 per 1,000
manufactured cigarettes containing at most 0.8 kg tobacco per 1,000
and NZD 1,678.29 per kg tobacco content for heavier cigarettes
and smoking tobacco, before GST. The light-cigarette rate implies
NZD 29.44375 per 25 cigarettes. It is constant across the May–October
campaign. The three observed national retail price vintages in P2.47
therefore do not provide within-campaign variation in this statutory
rate. The 2026 rate in P2.65 belongs to the later policy baseline.

[2023 amendment order](https://www.customs.govt.nz/media/45sl0kmj/order-in-council-excise-and-excise-equivalent-duties-table-tobacco-products-indexation-amendment-order-2022.pdf)
and [Customs rate notice](https://www.customs.govt.nz/about-us/news/important-notices-archive/important-notices-archive-2022/new-excise-duty-rates-for-tobacco-and-tobacco-products-from-1-january-2023).

## P2.68 Australian historical import duty anchor

ABF notice ACN 2021/34 records excise-equivalent customs duty from
1 September 2021 of AUD 1.11905 per stick for tariff subheading
2402.20.20 and AUD 1,598.64 per kg tobacco content for 2402.20.80.
These give a historical policy anchor at the end of the regional
study's 2013–2021 coverage. They cannot be carried back across the
study years. Each observation needs its own date match to the
applicable schedule, and tariff units do not identify tobacco
consumed, inventory movement or illicit share.

[Australian Border Force notice](https://www.abf.gov.au/help-and-support-subsite/CustomsNotices/2021-34.pdf).

## P2.69 Australian 2021 pre-indexation anchor

ABF's tariff pages in ACN 2021/30 show AUD 1.10360 per stick
for cigarette subheading 2402.20.20 and AUD 1,576.57 per kg
tobacco content for 2402.20.80 for the illustrated originating
goods schedule on 2 August 2021. ATO's domestic excise example
independently uses AUD 1.10360 per stick on 10 March 2021.
The P2.68 September import rates are about 1.4% higher in both
units. These are dated anchors. Applying them to actual regional
samples requires collection dates and the applicable tariff scope.
The August notice itself addresses alcohol CPI indexation and
does not establish a new August tobacco rate.

[ABF August tariff pages](https://www.abf.gov.au/help-and-support-subsite/CustomsNotices/2021-30.pdf)
and [ATO tobacco excise guidelines](https://www.ato.gov.au/law/view/pdf?DocId=SAV%2FTOBACCO%2F00005&PiT=99991231235958&filename=law%2Fview%2Fpdf%2Fsos%2Ftobacco20211217.pdf).

## P2.70 Australian 2021 tariff timing and regional sampling

Wang et al. describe one week of daily samples every two months
from February 2013 through December 2021. Applied as a nominal
calendar, this puts February, April, June and August 2021 before
the 1 September tariff change and October and December after it.
The retained supplement gives quality-control and paired-method
information but does not provide an exact 2021 daily collection
roster. The nominal calendar therefore supports a pre/post
design check only. It does not confirm individual observations
or establish four versus two complete campaign weeks. Tariff
matching must use actual dates, and this single regional series
would still lack an independent untreated comparison.

[Wang et al., regional study](https://pubmed.ncbi.nlm.nih.gov/38154341/).

## P2.71 Exact institutional record for the regional study

UQ's author publication list links DOI 10.1016/j.watres.2023.121040
to eSpace record UQ:2198f1f. The exact public record returned HTTP
403 in both web retrieval and a bounded direct CLI request. The
candidate UQ library API path also returned 403 and was not qualified
as a record route. The institutional listing verifies the record
identity. Manuscript availability and a daily sampling roster
remain unknown behind the access response.

[UQ author publications](https://about.uq.edu.au/experts-publication/49869/4748)
and [eSpace record](https://espace.library.uq.edu.au/view/UQ%3A2198f1f).

## P2.72 Public eSpace readback and cadence coverage

The Codex internal browser rendered the exact P2.71 record
without login. Its public Links section points to the publisher
DOI for full text and displays no institutional manuscript or
sampling roster. The record labels access as Hybrid and lists
CC BY 3.0 in its metadata. The licence of an actual source
file still needs verification against that file.

The record reports 340 analysed daily samples for February
2013 through December 2021. A strict every-two-months
calendar across that interval yields 54 nominal weeks or 378
daily slots. The difference of 38 prevents treating the
nominal cadence as a complete daily roster. It does not
locate the gaps or determine why the counts differ.

## P2.73 Publisher licence metadata and full-text access

The Crossref version-of-record licence is CC BY 4.0, effective
19 December 2023. Elsevier's exact article XML metadata independently
identifies full open access and gives the same CC BY 4.0 licence URL.
This resolves the published-version metadata in favor of the
publisher declaration over UQ's CC BY 3.0 display. The default
article XML contains core metadata only. An explicit FULL request
returned HTTP 401, and the internal browser showed a CAPTCHA on the
publisher landing page. The article bytes and daily sampling roster
remain unverified. The article licence does not establish rights
for underlying sampling records.

[Crossref record](https://api.crossref.org/works/10.1016/j.watres.2023.121040)
and [Elsevier article metadata](https://api.elsevier.com/content/article/PII:S004313542301480X?httpAccept=text/xml).

## P2.74 What the Australian sample total can verify

If all 340 analysed samples occupy distinct slots of the strict
378-slot nominal calendar in P2.72, the 38 unoccupied slots can
be allocated anywhere absent a roster. The resulting conditional
count bounds for 2021 are 4–42 overall, 0–28 before the September
tariff change, and 0–14 after it. The period-specific bounds are
marginal and their lower endpoints cannot both occur together.
Even under this calendar assumption, the aggregate count cannot
verify that both sides of the tariff change have observations.
A dated sampling roster or an explicit period-level count is
needed before a pre/post split can be qualified.

## P2.75 Tariff context for the Australian paired-assay bridge

Australian Customs Notice 2016/27 gives the rates effective
1 September 2016 as AUD 0.61054 per stick and AUD 763.20 per kg
of tobacco content for the relevant cigarette categories. Both
the excise and excise-equivalent schedules use those rates.
This supplies the historical tariff context for the five February
2017 paired-method samples in P2.31. Each pair reuses the same
sample, so the tariff exposure is identical within the pair.
Differences within those pairs can inform method comparability.
They provide no within-pair evidence on response to duty changes.

[Australian Customs Notice 2016/27](https://www.abf.gov.au/help-and-support-subsite/CustomsNotices/2016-27.pdf).

## P2.76 Paired-method sensitivity for the Australian composition signal

Recomputing from the rounded concentrations in Wang regional
Table S4, direct injection changes the combined COT and COT-OH
concentration by −12.50% to +14.95% relative to large-volume
injection across five paired days. ANBA / (COT + COT-OH) changes
by −13.01% to +28.05%, with two increases and three decreases.
The same day and sample enter both sides. This demonstrates
method sensitivity even for a ratio that cancels common
flow/population normalization. The range is descriptive for
five samples from one week. It supplies neither a transferable
correction nor a calibration uncertainty interval.

## P2.77 Rounding sensitivity of the Australian assay bridge

If Table S4 rounds ANBA to the nearest 1 ng/L and each cotinine
metabolite to the nearest 100 ng/L, propagate ±0.5 through each
ANBA concentration and ±100 through each two-metabolite sum.
For the direct-injection versus large-volume-injection ratio
change in P2.76, the resulting percentage intervals on
12–16 February are [2.37, 27.59], [−8.94, 9.29],
[16.71, 40.56], [−13.11, 5.65], and [−21.35, −3.78].
Two increases and one decrease survive this rounding assumption.
The other two signs are unresolved. These intervals describe
display precision only and exclude assay error and dependence.

## P2.78 Limit of a constant assay correction

Under the P2.77 rounding assumptions, the 14 February paired
ratio requires a direct-injection multiplier of at least 1.1671,
whereas 16 February permits at most 0.9622 at displayed precision.
The intervals have no common multiplier. Even allowing both
true ratios to take their closest compatible endpoints, a
constant multiplier leaves a worst-case multiplicative residual
factor of at least sqrt(1.1671 / 0.9622), about 1.101.
This is a lower bound on residual discrepancy within the
rounded pairs. It does not estimate a population error term.
A harmonization model needs residual variation beyond a single
fixed shift to accommodate both pairs.

## P2.79 NZ retail display and wholesale notification baseline inputs

Ministry guidance requires general retailers to conceal regulated
products and packaging from public areas inside and outside the
store, subject to limited visibility during delivery. Separately,
smoked-tobacco distributors have had to notify the Director-General
of wholesale sales and product types since 1 October 2023, with
annual renewal. The Ministry describes notification at the legal
person level, including one notification for a person with multiple
stores. The notification count therefore cannot measure outlet
density. These controls can coexist with repeal of the approved
smoked-tobacco retailer scheme. Observed store coverage, enforcement,
and compliance remain separate baseline inputs.

[Retail display guidance](https://www.health.govt.nz/regulation-legislation/vaping-herbal-smoking-and-smokeless-tobacco/retailers-of-vaping-and-tobacco-products/retail-visibility-and-display-of-regulated-products)
and [distributor notification guidance](https://www.health.govt.nz/regulation-legislation/smoked-tobacco/information-for-distributors).

## P2.80 NZ retail outlet count provenance

The 2014 Pearson et al. modelling team's briefing maps roughly
6,000 tobacco retailers as historical scenario context. The
Ministry's 2022 consultation describes a proposed national maximum
of 600 approved premises for the subsequently repealed scheme.
Neither number establishes the observed 2026 outlet count. The
first is a historical model input and the second a proposed legal
ceiling. Preserve both roles and leave the current count and
catchment-level retail access unfilled pending dated outlet evidence.

[Modelling team's briefing](https://www.phcc.org.nz/briefing/would-reducing-number-tobacco-retail-outlets-achieve-smokefree-2025-goal)
and [Ministry consultation](https://consult.health.govt.nz/tobacco-control/proposals-for-the-smoked-tobacco-regulato/supporting_documents/Proposals%20for%20regulation%20%20Smokefree%20Environments%20and%20Regulated%20Products%20Act%201990%20%2022%20Dec%20final.pdf).

## P2.81 New Zealand outlet estimate and enumeration scope

Robertson et al. report 5,008 outlets identified from District
Health Board lists and distinguish an industry estimate of about
8,000. The 2021 Ministry consultation cites their work for a
5,000–8,000 range. The 2023 TDB/Infometrics analysis estimates
7,100 by updating a 2012 benchmark using growth in selected
Stats NZ business categories to 2022. Its high assumption of
8,700 uses the total businesses in those categories. That
adjustment updates the proxy's date but does not enumerate
which stores sold tobacco. The estimates are suitable for
historical sensitivity scenarios with explicit provenance.
Current outlet coverage remains unverified.

[Robertson et al.](https://nzmj.org.nz/journal/vol-129-no-1432/regulating-tobacco-retail-in-new-zealand-what-can-we-learn-from-overseas)
and [TDB/Infometrics analysis](https://www.tdb.co.nz/wp-content/uploads/2023/04/TDB-Infometrics-Smoked-Tobacco-Amendment-Act-Review.2023.pdf).

## P2.82 Retail contrast scale under historical outlet scenarios

Holding the proposed 600-premise ceiling fixed, full take-up of
all 600 approvals would imply national outlet reductions of
88.02%, 90.00%, 91.55%, and 93.10% against the historical
5,008, 6,000, 7,100, and 8,700 scenarios in P2.80–81.
These are changes in national premise counts under a hypothetical
scheme. They cannot be mapped directly to reductions in access,
sales, or smoking. A spatial contrast still requires the
placement of retained outlets and a compatible baseline map.

## P2.83 Published allocation for the revoked retail scheme

The Ministry's published area schedule allocated 599 premises
(354 urban and 245 rural), within the 600 national ceiling used
in P2.82. Using the exact allocation and the 5,008–8,700
historical scenarios gives hypothetical reductions of 88.04% to
93.11% if all approvals are used. The Ministry marks the area
schedule revoked. It is a dated counterfactual design input.
Urban allocation examples include Auckland 25, Christchurch 13,
Hamilton 9 and Wellington 8. These areas are not wastewater
catchments, and a numerical cap does not locate approved stores
or establish realised accessibility.

[Ministry area schedule](https://www.health.govt.nz/publications/maximum-numbers-of-approved-smoked-tobacco-retail-premises-permitted-in-areas-of-new-zealand).

## P2.84 Geographic keys for the revoked NZ retail allocation

The 15 September 2023 Ministry schedule keys urban areas to
Stats NZ Urban–Rural 2023 generalised (layer 111198) and rural
areas to Regional Council 2023 generalised (111182). Airside
allocations are separate and use SA2 layer 111227 and meshblock
layer 111228. The Ministry lists the schedule as CC BY 4.0.

A label-only review associates the twelve Kim plant labels with
nine urban names and 78 nominal approvals, counting Auckland's
25 once for its four labels. That total excludes airside and
rural allocations. It is a lookup diagnostic, not a spatial
allocation. The underlying polygons and qualified wastewater
catchment boundaries are required to resolve intersections
before using these caps to model retail access.

[Ministry schedule and boundary references](https://www.health.govt.nz/publications/maximum-numbers-of-approved-smoked-tobacco-retail-premises-permitted-in-areas-of-new-zealand).

## P2.85 Wellington urban geography candidate

Stats NZ identifies Wellington as Urban–Rural 2023 code 1402.
The ArcGIS mirror returned a single code 1402 polygon in
NZTM2000 (EPSG:2193), matching the coordinate system of both
P2.39 wastewater candidate polygons. The mirror is clipped to
the coastline, while the Ministry schedule cites layer 111198.
Its bounding rectangle intersects both candidate rectangles
and contains neither. This does not establish actual polygon
overlap or select the Kim catchment.

External intake /Volumes/PortableSSD/tobac-p2-wellington.MjqdNf
retains urban-1402-clipped.json, SHA256
1514613f0283918fef7fcc77b18787c86b915b48bb8a1f2c7a806bc76f9a76e4.
The exact schedule-layer geometry and plant identity remain required.

[Stats NZ schedule layer](https://datafinder.stats.govt.nz/layer/111198-urban-rural-2023-generalised/)
and [clipped ArcGIS mirror](https://services2.arcgis.com/vKb0s8tBIA3bdocZ/ArcGIS/rest/services/UR2023/FeatureServer/0).

## P2.86 Wellington candidate polygon intersections

Intersecting the P2.85 clipped urban polygon with the two P2.39
operator polygons in EPSG:2193 gives 65.392 km² for Moa Point
and 4.650 km² for Western. These areas are 77.44% and 51.68%
of the respective candidate catchment polygons. Both candidates
cross the urban boundary. The fractions measure area and do
not estimate the share of residents or retail outlets served.

Shapely 2.2.0 / GEOS 3.14.1 ran on repo-local Python 3.15.2
using dependencies installed into a separate external target.
The calculation combined rings by parity and checked ring and
output validity. These are geometric diagnostics for the clipped
mirror and operator vintages. They leave the Kim plant identity
and exact retail schedule geometry unresolved.

## P2.87 Topology of the Wellington candidate catchments

The two valid EPSG:2193 operator polygons retained in P2.39
touch and have zero intersection area, using the same Shapely
ring reconstruction as P2.86. They are distinct spatial units
in that operator export. Geographic adjacency still permits
shared exposures, sewer operations or correlated measurement
errors. The topology alone does not verify the Kim plant key,
2023 contributing populations or independent validation folds.

## P2.88 Replay of the Wellington geometry diagnostics

The external P2.39 intake now retains check-overlap.py (SHA256
2527ece2bd7822f4c2b6d98c3eb1c17a4738b3fee693dae0e98cf8633d2f8ed1).
With the external spatial-deps target on PYTHONPATH and repo-local
Python 3.15.2, it verifies both input hashes, EPSG:2193, unique
feature identities, ring validity and output topology. It
reproduces P2.86 and verifies 1,990.172 m of shared catchment
boundary. Reported overlap percentages use full operator
polygon area as denominator. They are not separately measured
land-only, population, or outlet shares.

## P2.89 Exact schedule-layer area check

The public attribute table for Stats NZ layer 111198 confirms
Wellington code 1402, major urban classification, 112.71221247 km²
land area and 112.84839723 km² total area. The P2.86 clipped
mirror geometry measures 112.71117433 km². The near match to
the official land-area attribute supports the mirror's clipped
description. The 0.137223 km² difference from the schedule-layer
total is a net area difference. It cannot bound the change in
either catchment intersection without verifying polygon nesting
or obtaining the exact geometry. No exact-layer overlap is claimed.

[Stats NZ layer and attribute table](https://datafinder.stats.govt.nz/layer/111198-urban-rural-2023-generalised/).

## P2.90 Exact schedule-layer service readback

The public Stats NZ layer API identifies 111198 version 350683,
EPSG:2193 multipolygon data, 745 feature records and four empty
geometries. The sample endpoint supplies attributes without
geometry. The service catalogue marks WFS and vector queries as
API-key routes. An anonymous, noninteractive Git read on the
advertised Kart HTTPS remote requested credentials. The exact
geometry remains unverified through these CLI routes.

External P2.39 intake retains layer-111198.json, SHA256
c78dcec40debb484ac1bdfe5232b5e6f50ae2246196063c05f68f03507a5ae61.

[Stats NZ layer API](https://datafinder.stats.govt.nz/services/api/v1/layers/111198/).

## P2.91 Observed NZ cessation service funnel

Ministry aide-mémoire H2024036635 reports 1,522 enrolments in
the Counties Manukau stop-smoking service from October 2022
through September 2023. Of these, 770 set a quit date and 626
had a biochemically validated four-week quit. The reported 81%
uses quit-date setters as its denominator (81.30%); the same
numerator divided by all enrolments is 41.13%. The briefing's
one-year figure is an extrapolation from relapse evidence.
The local funnel gives a measured historical service example
and separates enrolment, quit-date setting and short-term
outcome. It supplies neither national reach nor a causal
contrast with unaided quitting.

[Ministry aide-mémoire, pp. 3–4](https://www.health.govt.nz/system/files/2024-08/h2024036635_briefing_-_stop_smoking_services_and_health_promotion_activities_black_box.pdf).
