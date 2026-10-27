# M2 matched evidence pathway

27 October 2026. This is a prespecified research pathway and source-feasibility
assessment. Available public observations do not identify the proposed cap's causal
consumption, lawful-origin or incremental criminal-harm effects. No current national
posterior, fitted policy response or commissioning recommendation is produced.

## Decision, estimands and actions

Retain M2a's prospective national cap of at most 600 smoked-tobacco retail premises
versus unchanged availability. This is a genuine historical policy design, not a
currently approved intervention. The Ministry's [current regime page](https://www.health.govt.nz/regulation-legislation/smoked-tobacco)
records repeal of the approved-retailer scheme. No new statutory authority,
commencement date or contemporary baseline outlet roster was obtained. A future cap
requires those substantive decisions; an analyst cannot assign a treatment date.

Primary consumption estimands concern New Zealand residents aged 15+ using
factory-made cigarettes and roll-your-own (RYO) tobacco, in the first complete
12 months after actual implementation, compared with the same period under the
reference availability. Preserve factory-made counts and RYO mass separately until
physical conversions are qualified. The intervention covers smoked tobacco more
broadly; cigar/pipe substitution and cross-border purchasing remain spillovers,
not assumed zero. Vaping/heated products are separate exposure channels.

Candidate actions remain the existing M2 reference, restriction, and restriction
with accompanying mitigation/support. Hold nicotine content, generational sales,
excise and vaping rules constant in the primary estimand; cointerventions require
explicit adjustment or a separate structural scenario. Support/enforcement costs,
implementation and cessation access must be specified before operational use.
No study and null effects remain admissible. A decision can reverse under supported
switching, net quitting, replacement, incremental harm or implementation scenarios;
normalised M2 payoffs are not monetary decision thresholds.

## Current source audit

The dated machine record is `evidence/m2/matched_pathway_20261027.json`.
This is a targeted feasibility review, not a systematic review.

| Source | Actual observation and coverage | Suitability for this contrast |
| --- | --- | --- |
| [MOH 2025 returns](https://www.health.govt.nz/regulation-legislation/smoked-tobacco/information-for-manufacturers-and-importers/tobacco-returns/tobacco-returns-2025) | National retail releases, calendar 2025; chart excludes cigars/cigarillos, heated products separate | Administrative supply, not resident consumption. Stock/border/reporting/product corrections still required. Existing workbook verification is retained. |
| [NZHS 2024/25](https://www.health.govt.nz/monitoring-statistics/surveys/new-zealand-health-survey/publications/202425-survey-publications/trends-in-smoking-and-vaping) | Daily smoking prevalence for ages 15+; collection described as July 2024 to July 2025 | Does not give total tobacco volume or lawful origin, is not calendar-2025 matched, and does not identify cause/effect. Exact day endpoints are not asserted. |
| Historical MOH/NZHS-derived summaries | Already registered source dependencies and period uncertainties | Reuse original data identities. A new paper or posterior cannot become another independent observation. |
| SHINE retail-effect input | Published model/stated-intention parameter for a different outlet reduction | Retain M2a's transported scenario and null/attenuated alternatives; no observed causal effect or automatic 600-outlet mapping. |

The current pages were reviewed through rendered primary-source access. Direct
Python downloads returned HTTP403 on all three pages. No fresh raw-capture hash,
original capture time or historical-edition recovery is claimed. The previously
verified workbook/source receipt remains byte-bound independently. Missing raw
capture does not invalidate that dated verification, nor does it create a new one.

## Feasible comparative design and stop rule

A prospective controlled interrupted time series is a candidate, conditional on
legal implementation and access. A geographically phased rollout could offer
not-yet-treated comparator catchments only if rollout selection, anticipation and
cross-catchment shopping can be addressed. No such rollout is known to be assigned.
A simultaneous national cap instead needs defensible external/synthetic donors;
parallel trends, comparable products/tax regimes, measurement and no interference
must be evaluated rather than presumed. If neither route is defensible, report
non-identification and retain transparent elicitation/structural scenarios.

Proposed sampling schedule: 24 pre-implementation and 12 post-implementation monthly
windows, matched total/lawful measurements within each window and arm. This is an
analyst design proposal, not a powered sample-size calculation. Register actual
catchment boundaries, denominators, start/end days and acquisition feasibility first.
Use the 12-month pre/post aggregates as the minimal four-cell metadata check; do
not count the monthly observations and their aggregates as separate evidence.

Reserve the final six pre-implementation months for a temporal prediction check
before causal fitting; compare observed total/lawful trajectories with held-out
predictions, assess residual calibration and uncertainty coverage, and record
failures. Set scientifically tolerable errors with decision-relevant scale and
pilot variance before field commissioning. No arbitrary fitted threshold is adopted
here. Retain independent post-period prediction where feasible. Pretrend/placebo
checks cannot prove the causal assumptions.

Measure actual outlet availability/compliance, travel and displacement, not only
licences. Prespecify adjustment for excise/prices, cessation support, vaping,
income, migration, seasonality and concurrent enforcement. Test anticipation and
spillovers with exposure definitions and alternative donor sets. If effects cannot
be separated, use a bundled-policy estimand rather than naming the cap as cause.

## Measurement and joint evidence handoff

Each of treated-before, treated-after, comparator-before and comparator-after
needs total and corrected lawful consumption. Their native periods, population,
products, geography and units must match within cell. Population definitions and
products/units must match across arms; geography is intentionally different.
Before/after scope must be stable, ordered and nonoverlapping. Positive dates alone
do not establish a 12-month window or sufficient sample size.

Lawful consumption reuses `tobac.supply.expected_releases`: undo reporting bias;
subtract inventory accumulation, outbound flows and wastage; add lawful inputs
outside recorded releases. Visitors, duty-free and exports need mutually exclusive
allocation. Uncertain quantities remain latent with correlated errors. Do not
subtract resident total consumption from unrestricted all-purchaser releases.
An observed negative total-minus-lawful discrepancy stays signed: it diagnoses
measurement/accounting mismatch, not negative illicit consumption and not zero.

Wastewater total needs raw-scale assay detection/quantification, recovery,
biological yield, population/flow denominators and non-tobacco-source qualification.
Catchment chemistry includes all contributors; it cannot alone isolate residents
aged 15+, ethnicity or individuals. Obtain a qualified population mapping or revise
the estimand transparently. A prevalence survey requires intensity/product and
selection models to become volume. No constant grams-per-stick is supplied here.

Build one joint likelihood with shared yield, assay/calibration, reporting, stock,
serial and geographic errors. Propagate allocations as A Sigma A^T; redundant
aggregates are not independent. Use `Scope`, `EvidencePacket`, `Belief` and the
existing likelihood functions, preserving exact state IDs/order. Reconcile all D0
underlying-data identities before `condition`; Phyo/other summaries do not add new
MOH/NZHS observations. Named covariance or transport notes are not fitted models.

`audit_pathway` is deliberately narrower: it checks declared cells, scopes,
products, roles and exact data-ID reuse. It cannot detect concealed dependencies,
prove exchangeability, fit covariance or authorise field work. Its best possible
status is `metadata_compatible`; `empirically_qualified` and `conditioned` remain
false. Shared data must be reconciled in a justified joint representation before
using the existing evidence interface; relabelling IDs is not a remedy.

## Identification, learning order and remaining issue criteria

Under M2a's equal-intensity/no-additional-mechanism structure, matched causal ratios
satisfy R_total=1-q and R_lawful=(1-q)(1-d). Total alone cannot identify lawful-to-
illicit switching d. With both, d=1-R_lawful/R_total only when R_total is positive
and the counterfactual, differential reporting and accounting assumptions hold.
Unknown differential lawful bias multiplies R_lawful and is confounded with d.
Biological calibration may be valuable jointly even when standalone EVSI is zero.
These equations are an identification argument, not an estimator for public totals.

Reproduce existing M2 EVPI and grouped EVPPI first, then report study EVSI,
targeted information gain and same-data prior robustness separately. Do not add
EVPPI groups or confuse information gain with action value. Original M2 null,
attenuated, source-shaped and replacement structures, crime weights and grid
refinement remain; M3's structure/uptake/dependence comparisons remain conditional.
No new field likelihood or numerical prior is inserted merely to generate a result.

Incremental organised-crime harms require additional harm/resource outcomes under
the contrast, separate from participation, sales, profits, seizures and tax loss.
Include zero marginal harm, lawful replacement and displaced activity. Empirical
mitigation response, near-limit assay, cost/value units and transport stay open.
Governance/permissible use and Māori equity interpretation require substantive
agreement before deployment; there is no authority to infer them from public data.
No individuals or ethnic groups are assigned criminality from chemistry.

Issue #3 remains open: the contrast and protocol are specified for research;
current matched observations, causal response, assay and consequence calibration,
held-out field results, monetary costs and governance have not been obtained.
The next dependency is a legally feasible implementation/counterfactual and access
to matched measurements. If unavailable, non-identification is the qualified result.

## Execution and interpretation

The existing Nox `reproduce` session now writes `m2-pathway.json` into its fresh
replay directory before the unchanged M1/M2/M3 numerical runs. A standalone audit
can be run with the qualified repo-local Python 3.15.1 environment:

```sh
.nox/tests/bin/python scripts/qualify_m2_pathway.py --out outputs/engineering/NEW-m2-pathway.json
```

The command refuses an existing receipt path. It records checkout identity, the
actual command, source-bound input hashes and remaining gaps. `status: blocked`
is a successful feasibility assessment with unresolved research requirements;
invalid declarations, source hash drift and malformed metadata fail execution.

A limited discovery search also located the 2026 Dutch supermarket-ban compliance
evaluation (DOI 10.1136/tc-2025-059985) and the New Zealand wastewater-method study
(ScienceDirect S0048969725028657). Direct full-text access was denied. These are
candidates for subsequent source/transport review; no numerical extraction, causal
NZ effect, assay calibration or new prior is inferred from search snippets.
