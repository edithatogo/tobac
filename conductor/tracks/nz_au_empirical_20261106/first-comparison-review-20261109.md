# First-comparison evidence review — 9 November 2026

## Result and scope

The bounded review of the 21 records in
[the disposition table](first-comparison-dispositions-20261109.csv) is complete
for the first comparison's **permissible use and eligibility decision**. The
recorded evidence supports a reproducible non-identification result and scoped
source/method comparisons. It does not yet support the prespecified matched
empirical baseline-versus-wastewater score, fitted NZ policy response or monetary
research recommendation. The observation manifest remains unadmitted until its
separate source and scientific requirements pass.

This is the continuation of P2.126, P2.222 and P2.237 in
[the existing reconciliation](phase2-reconciliation-20261107.md), integrated on
main `d0e832b02b8b9e6791903f987245e8f6332e943a` and reviewed on PR #147 source
`c353d6fb11dbe0bb593f514e5883fbc68d05944e`. It consolidates the existing work
instead of restarting 237 source tasks. The selected set includes all eight S1
measurement records prioritised in P2.21, later calibration and national-method
comparators, the baseline sources, candidate validation outcomes and policy
bridges. Only the specific review mode stated in each row is claimed. Three
older methodological records have abstract-level target-scope assessments;
their full-text methodological appraisal remains open for the wider review.

The five-family systematic search and its unreviewed corpus remain open under
[the original protocol](systematic-search.md). This targeted disposition is
not complete screening of 27,507 unique PMIDs. Evidence cut-off remains the
decision contract's 6 November 2026; later retrieval checks existing editions
and is not a new observation date.

The decision remains no further study, a bounded wastewater pilot, or a wider
programme, evaluated for the same retail/cessation action set. Keep Australian
evidence's population and calibration scope explicit. Follow
[decision-definition.md](decision-definition.md) and retain the existing
public-only boundary. No request or access application was sent.

## New original-byte and missing-field checks

| Object | Observed retrieval | Bytes and SHA-256 | Verification scope |
|---|---|---|---|
| [Kim publisher supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0048969725028657-mmc1.pdf) | HTTP 200; application/pdf; request recorded 2026-11-09T08:44:01.313583Z | 1,306,212; `c2ce1d0c3fcc95e9c49acb5bf403cc2598b999a97b8a9e558557a3aa1614046c` | Matches the P2.22 original exactly. Reopened Tables S3, S19 and S20; rendered and visually checked PDF page 43. |
| [Weng article XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13389531/fullTextXML) | HTTP 200; application/xml; request recorded 2026-11-09T08:44:09.568766Z | 95,290; `b848cbc72f5e0785b4a899cd255ef354d1893a8c16863a7139bb957af140fdf0` | Reopened the factor definition, selection rule, Figure 3, limitations, licence and data availability. This is a new retrieval receipt, not an assertion of byte parity with the earlier XML. |

Originals and temporary extraction/rendering files remain outside the source
repository. These are local original-byte checks, not canonical archive-object
readbacks or native acceptance. The failed fresh ScienceDirect article access
(403) and Dalian Europe PMC XML access (500) do not invalidate retained originals
or establish absence of the published research. No failed endpoint was relabelled
as a successful full-text review.

### Kim: the missing normalisation data are substantive

The fresh S3 text contains 142 printed dates, 43 distinct calendar dates,
2 May–29 October 2023; seven dates are neither Wednesday nor Sunday. S19
contains 117 censored entries after removing its caption token. Its caption
places those observations between detection and quantification limits. They
must not be replaced with zero or discarded. The earlier independent full-cell
reconciliation remains the evidence for all 576 slots.

S20 publishes concentration ranges and explicitly notes varying populations
and daily flows; it supplies neither a dated flow table nor the contributing
population series. Visual readback confirms those fields are absent from that
table. Consequently its ranges cannot independently reconstruct normalisation
or effective sample-specific censoring limits. Published normalised loads remain
descriptive measurement candidates. P2.27–29 retain the processing, total-load
and replicate-spread discrepancies. This check does not reopen the public-data
access boundary or substitute settlement populations for catchments.

### Weng: dimensional reconciliation is possible; NZ calibration is not supplied

The original selects 19 cigarette users above its quantification threshold and
reports a 9.02% factor with a reported spread of 4.95%; the factor paragraph does
not explicitly define that spread's statistic. It uses assumed absorbed
anabasine of 0.0072 mg/cigarette and the literature COT+3HC excretion factor.
Under that same dose assumption, the unit conversion is:

`0.0902 × 0.0072 mg/cigarette × 1000 µg/mg = 0.64944 µg/cigarette`.

The corresponding scaled spread is 0.3564 µg/cigarette, without assigning an
uncertainty distribution. This arithmetic gives a clearly
labelled sensitivity alternative to the 0.91 and 1.13 µg/cigarette factors
reviewed in P2.30–33; it is not a fitted NZ prior. The reported spread cannot be
treated as a standard error or catchment-level uncertainty. Selection, assumed dose, shared calibration
literature and potential vaping contribution remain explicit. The article is
CC BY 4.0. Its raw-data statement requires author contact, so participant-level
calibration data remain unavailable within this public-only task.

## Eligibility decisions for the first comparison

| Evidence role | Supported use | First-comparison disposition |
|---|---|---|
| NZHS and Ministry returns | Survey indicators and administrative release summaries, retaining native periods and units | Do not infer catchment-month consumption from annual estimates. Joint prevalence/intensity uncertainty, eligible population, stocks and lawful-flow adjustments remain required. Reuse the official source copies and exact editions. |
| Kim NZ campaign | Reported dates, normalised analyte loads and censoring patterns; method and measurement sensitivity | Hold target likelihood admission on the specific measurement/matching fields above. A six-month campaign cannot supply a complete temporal holdout year and three earlier complete years. |
| Australian human/assay studies | Separate excretion, assay and sewer sensitivity scenarios | Do not pool assumptions, shared samples or calibration factors as independent observations. Preserve units and population transport requirements. |
| Wang regional and national results; ACIC | Programme design and alternative measurement/accounting comparisons | National illicit estimates inherit wastewater and lawful-supply inputs. They cannot independently validate the wastewater addition that helped construct them. Regional raw data remain request-only in the freshly checked publisher statement. |
| ABS and ITEC | Alternative modelling and supply-context comparisons | Exclude from the independent consumption score: ABS uses ACIC and auxiliary inputs; ITEC inherits the ATO baseline and checks against wastewater. Their derived/forecast values are not new outcomes. |
| ATO and AIHW purchase survey | Contextual supply estimates and an independent purchase diagnostic, respectively | Exclude as the planned target outcome: fiscal supply and packet purchases have different quantities, dates and geographic support from matched consumption. Keep the AIHW diagnostic independent of ABS/ITEC; do not overstate its predictive-validation role. |
| Retail model, cessation trial, dispensing | Explicit conditional policy scenarios and historical service context | Trial offer effects do not establish population reach or routine implementation. Dispensing is not quitting or absorbed nicotine. The prospective retailer model is not an observed implemented-policy contrast. |

The foreign Belgian and Dalian records are excluded from the **NZ target
validation outcome** on country/population/period scope. They remain method
context. The Belgian abstract reports very low survey participation and no
demonstrated survey–wastewater correlation. That is not evidence that wastewater
has zero decision value. The Dalian abstract's Monte Carlo comparison does not
provide a frozen NZ holdout. Their target-scope exclusions do not require an
invented full-text assessment.

Primary follow-up locations: [Weng original](https://pmc.ncbi.nlm.nih.gov/articles/PMC13389531/),
[Wang national original](https://pmc.ncbi.nlm.nih.gov/articles/PMC12887742/),
[Wang regional publisher](https://www.sciencedirect.com/science/article/pii/S004313542301480X),
[Belgian study abstract](https://pubmed.ncbi.nlm.nih.gov/26980372/),
[Dalian study abstract](https://pubmed.ncbi.nlm.nih.gov/26888732/),
and [Tscharke assay abstract](https://pubmed.ncbi.nlm.nih.gov/26198173/).
Exact previously verified tables and formulas are linked per row in the CSV.

## How the disposition table is interpreted

`source_id` reuses the existing bibliography/receipt identity where one exists;
in particular, `parallel-S01`, `parallel-S03`, `parallel-S05`, `parallel-S08`,
`zheng2023`, `wang2026` and `SHINE_RETAIL_TABLE2` are existing identities.
Alternate bibliographic aliases must not create a second observation.

`comparison_role` is the intended use being reviewed, not a claim of fitness.
`matched_target_data_available` concerns the joint first-comparison target,
not whether a public source exists. A value of `no` therefore does not deny
that an original trial, survey or analyte table contains real observations.
Review dispositions and claimed availability cannot override the existing
`Scope`, `EvidencePacket`, `SupplyBasis` or source-handoff validation.

Semicolon-separated `dependency_group` values identify shared observations or
assumptions that require reconciliation. They are conservative dependence
warnings, not estimates of covariance or proof that every sample overlaps.
The named dose/excretion groups are shared assumptions; a repeated group must
not be interpreted as a new independent likelihood contribution.

The `scientific_blockers` and `archive_blockers` columns deliberately distinguish
two kinds of remaining work. A verified archive readback could resolve storage
provenance; it would not supply missing flows, calibration, policy response or
independent outcomes. Conversely a source may be suitable for contextual use
while remaining unsuitable for the fitted comparison. `existing_receipt` lists
repository-relative evidence records; no private path is an admission receipt.

## Completion and next supported execution

Completed here: current, source-linked dispositions for the declared first-use
set; exact separation of reuse, sensitivity, exclusion and blocked likelihood;
fresh Kim original parity and missing-field check; fresh Weng units, selection,
rights and access review. The independent admission audit can now consume a
finite table rather than parse thousands of progress-note lines.

The next empirical fit requires a compatible observation manifest, measurement
and policy-response bridges, and an independent target outcome with the frozen
validation coverage. The reviewed public packet does not supply those. Preserve
this non-identification checkpoint while completing source parity, admission
auditing and dynamic-interface implementation that are supportable now. The
first comparison's bounded review is complete; the full systematic review and
stronger empirical acceptance remain separate open requirements.
