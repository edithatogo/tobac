# Policy, health and equity expansion — 6 November 2026

## Initial readiness checkpoint
P3.1 conceptualisation/readiness preparation is implemented locally. Empirical Phase 3 is
blocked and remains incomplete. No new policy mechanism, health trajectory, QALY, distributional
result or PSA has been fitted or calculated. Numerical source, inputs and dependencies are
unchanged; this task does not change the owner's ongoing native qualification candidate.

## Deliverables and actual admission result

phase3-module-matrix.csv covers 11 requested policy, health, resource, equity and uncertainty
modules, with existing interfaces, units, missing inputs and positive/negative validation
requirements. phase3-design.md specifies sequencing and five formula contracts, perspective
accounting, HR-QoL provenance, competing risks, subgroup aggregation and PSA requirements.
These contracts do not constitute an implemented health/equity engine.

Executed the existing source_handoff.py against the actual maintained proposal and inventories:
28 rows, status blocked, scientific_qualification false, no conditioning performed. All 28
have source-value, scope, covariance and likelihood qualification gaps; 24 flag shared-data
dependence, 16 require separate unit-conversion qualification, and 12 are not observation-role
records. These are overlapping gap counts, not independent missing datasets. The audit did
not receive a raw-object directory, so capture_bytes_not_verified means unverified in this
execution, not proof that the owner lacks the originals. Existing archived source identities
and native ownership remain intact.

Actual command/result: phase3-task-card.md; outputs/nz-au-phase3/source-handoff.json and
source-handoff-qualified.log. The bounded command exited 0 at 58.6 MiB sampled process-group
RSS; that exit means the blocked report was written, not that empirical admission passed.
The initial direct invocation failed to import tobac; explicit PYTHONPATH=src selected this
checkout and the corrected invocation passed. Both logs are preserved; no runner guard or
scientific check was weakened.

Your vop_poc_nz revision ad84d3090a2d97f2805a86e94a7b9614a3d1ab14 is a reuse candidate
with verified manifest incompatibilities: Python <3.15, pandas, Polars <2 and Arrow <26.
No dependency was installed/bypassed and no code copied. tutorial_methods_equity was read
at 3fb9e78a7a068c3b5a3f991deb2c41c31aede3ce as context only; executable/citation review is
still needed. The existing reference engine was retained.

PHARMAC discount/health guidance and ISPOR DCEA evidence requirements were consulted for
methods, not treated as tobacco intervention-effect data. Actual acquisition outcomes are
in phase3-source-receipts.json; originals remain in external staging where retrieval succeeded.
No external repository or archive was written. Rights, durable archive admission and exact
health utility/causal parameter extraction remain open.

## Verification and next operation

Focused existing policy/evidence/value, source-handoff, publication-boundary and workstream
selection passed: 151 tests in 6.04 s, Python 3.15.2, bounded peak 223.6 MiB, exit 0.
Log: outputs/nz-au-phase3/focused-tests.log. git diff --check passes. Four methods/library
source files were retrieved into external staging and their bytes read back against hashes;
the ISPOR capture is the publisher abstract page, not the full article. Receipts identify
these limits; no external archive ingestion, recovery or empirical extraction is qualified.
The final bounded context profile retains regulation and the expansion contracts; it omits
full unchanged retail/value source already reviewed to stay below 60,000 bytes. An exploratory
size assertion rejected a 65,033-byte candidate before it was written; no budget was raised.
No numerical source was changed, so no new full-suite, clean-package, reference replay,
hosted run or empirical validation success is claimed.

Next: receive current native admission and complete the matched Phase 1–2 slice; then
implement and verify one supported policy mechanism at a time. Actual health/equity work
requires accepted disease histories, utility tariffs, costs, subgroup denominators and
opportunity-cost evidence. Missing evidence must not become default numbers or synthetic
data labelled empirical. No row in Phase 3's original plan is closed by this preparation.

## P3 methods checkpoint, 8 November 2026

Chat 01a1b3ac-76ef-7b12-a919-91fcb05de339 owns the scoped P3 evidence
continuation on branch codex/p3-policy-health-equity in its attached managed
checkout, based on 177e579. The checkout root is
`/Users/doughnut/.codex/worktrees/tobac-p3-policy-health-equity/tobac`.
Shared integration, native archive admission and publication retain their
existing owners. The next operation is to qualify scope-matched inputs for
one mechanism before implementation.

The external methods record has these source dispositions.

| Input | Result and use |
|---|---|
| [NZ EQ-5D-5L social tariff](https://doi.org/10.1016/j.socscimed.2019.112707), Tables 3–4 | Enumeration of the rounded coefficients yields 3,125 profiles, a range of −0.830 to 1.000 and 780 profiles below zero. Use as a scoring reference after tariff rights and edition review. |
| [COPD study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4072614/#Tab2), Table 2 | Applying the NZ tariff to the foreign cohort counts yields mean utilities of 0.773088, 0.765926, 0.691842 and 0.658440 by GOLD grade. Use as a transport sensitivity. Cross-dimension covariance, sampling uncertainty and NZ transport remain open. |
| [NZ COPD Atlas](https://www.hqsc.govt.nz/our-data/atlas-of-healthcare-variation/chronic-obstructive-pulmonary-disease/) and [Waikato cohort](https://pmc.ncbi.nlm.nih.gov/articles/PMC7897844/) | Hold the Atlas pending publisher review. The historical Waikato cohort distinguishes overall mortality from survival after discharge and censors death in its readmission analysis. Use only comparisons with matched time origins and competing-event definitions. |
| [BODE³ retail study](https://doi.org/10.1136/tobaccocontrol-2015-052846), Table 3 | Its historical equity scenario changes background mortality and morbidity assumptions. Use it as a structural comparator separately from normative weights applied to fixed gains. |
| [NZ excise evaluation](https://www.health.govt.nz/system/files/2024-05/evaluation-tobacco-excise-increases-final-27-nov2018.pdf), sections 5.1.7–5.1.8 | Original PDF SHA256 a294e59dd4f2f610404a6e16cbf1541b2b4054670961445b764dea72c7207ec2. Historical demand and prevalence ratios use distinct estimands. The prevalence regression controls only for price. Hold causal, intensity and subgroup parameters. |

The external evidence remains in local staging. No empirical input has been
admitted, and no model has been fitted or externally validated in this checkpoint.

## Nicotine standard evidence screen

The [Hatsukami et al. randomised trial](https://doi.org/10.1001/jama.2018.11473)
assigned 1,250 US smokers to immediate nicotine reduction, gradual reduction,
or usual nicotine content research cigarettes. The immediate arm received
0.4 mg nicotine per gram of tobacco. Over 20 weeks, immediate versus gradual
reduction gave a breath carbon monoxide difference of −4.06 ppm and geometric
mean ratios of 0.83 for the acrolein marker and 0.88 for the phenanthrene
marker. Use these contrasts as exposure benchmarks under the trial assignment.
The different measures and units require separate model outputs.

The immediate arm also had more dropout and nonstudy cigarette use.
Record nonstudy cigarettes separately from compliant study cigarettes.
The trial does not establish the lawful status of a future substitute,
national compliance, long-term disease risk, or NZ/AU transport. Its
[one-month follow-up](https://pmc.ncbi.nlm.nih.gov/articles/PMC10676511/)
reuses the randomised cohort. Group both reports as one evidence family
rather than combining them as independent experiments. A jurisdiction-specific
policy scenario and a justified exposure-to-disease bridge remain open.

## New Zealand Quitline adjunct contrast

[Walker et al.](https://doi.org/10.1111/j.1360-0443.2012.03906.x)
randomised 1,410 Quitline callers motivated to quit to usual care
or an offer of very low nicotine cigarettes alongside usual care.
Usual care included nicotine replacement and behavioural support.
At six months the reported seven-day point prevalence of abstinence
was 33% versus 28% (RR 1.18, 95% CI 1.01–1.39). Continuous abstinence
was 23% versus 15% (RR 1.50, 95% CI 1.20–1.87). Keep the endpoints
separate and retain the reported 24% loss to follow-up. The results
provide an assigned adjunct comparison within motivated Quitline
callers. Exact missingness handling and full-text readback remain open.

For P3, this is a candidate benchmark for a supported cessation
offer. A national nicotine standard changes the products available
to the full smoking population. Transport would require reach,
adherence, baseline risk and substitution evidence on that scope.
Keep this contrast separate from the US biomarker experiment and
from dispensing counts that do not measure incremental programme reach.

The [registered trial protocol report](https://doi.org/10.1186/1471-2458-11-37)
specifies six weeks of access to the reduced-nicotine product from quit
day and eight weeks of usual nicotine replacement. It prespecifies
classifying participants lost to follow-up as smoking and a per-protocol
sensitivity. This resolves the planned rule. Application in the results
and arm-specific missing counts still require the final analysis tables.
The trial offer is time-limited and starts at a chosen quit date.
Use the six-month point prevalence and continuous abstinence results
as distinct endpoints when checking a cessation model. Neither endpoint
by itself estimates a permanent quit transition or later relapse.

## Duration-dependent relapse evidence

The [ITC Four Country cohort analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC5993599/)
uses waves 1–9 in Australia, Canada, the UK and the US, with about annual
follow-up. It reports that associations with relapse vary by duration of
abstinence. This supports retaining time since quit in the model state.
The reported predictor hazard ratios do not supply baseline relapse
probabilities for New Zealand Quitline participants. The absence of
detected predictors beyond two years does not imply zero relapse.

An [earlier ITC analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC4517970/)
uses the same survey family. Keep the publications together pending exact
wave and participant reconciliation. Six-month trial abstinence remains
an endpoint check. A long-horizon projection needs baseline relapse by
time since quit, an outcome-definition crosswalk and transport assessment.

The [ITC New Zealand wave inventory](https://itcproject.org/countries/new-zealand/)
lists NZL3.5 as recontact only, with 624 interviews from 8 June to 26 July
2021. Prior NZL3 fieldwork ran from 8 November 2020 to 27 February 2021.
Request the linked NZL3 to NZL3.5 transition first. The published dates
imply possible interview gaps of roughly 101 to 260 days, so use each
respondent's dates rather than treating this as a fixed six-month
follow-up. The 238 quitters reported at NZL3 and the 223 at NZL3.5 are
wave totals. The latter includes people who could have quit since NZL3.
Neither the difference nor the ratio measures relapse or retention.

Use baseline quitters as the risk set and request baseline quit duration,
recontact disposition for all eligible baseline quitters, follow-up
smoking status, and any question that captures resumption followed by
another quit. Request eligible denominators, longitudinal weights and
survey design variables. Compare NZL3.5 to NZL4 and NZL4 to NZL5 only
within linked recontacts and keep replenishment separate. If the
questionnaire only identifies smoking at follow-up, estimate return
to current smoking by that interview and label it accordingly. First
relapse remains unidentified when intervening relapse and re-quitting
are unobserved. Exact item codes and routing still need confirmation
from the instruments or data custodian. No data request was submitted.

The [NZL3 and NZL3.5 technical report](https://itcproject.s3.amazonaws.com/uploads/documents/ITC-NZL3NZL3.5_Technical-Report_revised_18Jul2023.pdf)
narrows the request. Its NZL3 routing table (p. 51) identifies
`QA08342` for recontacts with prior derived smoking status 4–7.
It distinguishes continuous abstinence, return to smoking followed
by another quit, and current smoking. The derived frequency
`FR08225v` collapses the first two responses into the same quit status.
Request the NZL3.5 equivalent of the raw item, routing inputs,
nonresponse and exit codes, and any event timing. The report describes
a shortened NZL3.5 instrument. The NZL3 item alone does not verify its
retention or routing at NZL3.5.

Table 11 reports 605 eligible linked respondents from 1,230 valid
NZL3 interviews (49.2% overall retention) and 615 eligible for the
NZL3.5 cross-sectional analysis. Request the baseline-quitter-specific
response denominator by stratum and use the linked analytic weight
`ccwts08121v` from Appendix G for the primary weighted analysis.
Its calibration to NZL3 benchmarks does not resolve selection on
unobserved relapse. Preserve an attrition sensitivity and report
unweighted denominators separately.

The [NZL3.5 recontact instrument](https://itcproject.s3.amazonaws.com/uploads/documents/ITC_NZL3.5_Recontact_SQ_web_EN.pdf)
confirms `QA08342` at question 023, routed to recontacts with prior
`FR08309v` in 4–8. For this instrument, code 1 identifies reported
continuous abstinence, 2 resumption followed by another quit, and 3
current smoking after quitting. Codes 8 and 9 terminate the survey.
Retain the raw response and disposition, including partial interviews
if available. In the linked risk set, estimate reported resumption
(codes 2 or 3) and current smoking (code 3) separately. Review the
code 3 responses against current frequency and flag inconsistencies.

Request `QA08439` for quit duration bands and `QA08701`, `QA08706`
and `QA08711` for lapses and occasional smoking. The survey can
classify some people smoking less than monthly as quitters and uses
different recall windows for the puff item. Report the result as
self-reported resumption under the instrument's definitions. The
three-way item supplies interval status but no onset date or episode
count. A single puff, first relapse timing and repeated transitions
require separate evidence.

Appendix G reports 120 NZL3 quitters at up to 12 months and 118 at
more than 12 months after exclusions. Use those counts as checks
against the linked extract before imposing further eligibility
restrictions. Overall retention of 605/1,230 does not establish
retention in either quit-duration stratum. The follow-up
cross-sectional quit counts classify respondents at the later
interview and cannot supply those denominators.

For each baseline quit-duration stratum, let (N) be the eligible
baseline count, (R) the number with an interpretable raw resumption
response, and (E) the number reporting resumption. The unweighted
finite-cohort bounds are (E/N) to ((E+N-R)/N) if all missing
outcomes could be either value. Apply the same calculation to
current smoking separately and treat routing errors, refusal and
unknown responses as missing unless resolved. For population
bounds, use baseline weights for the entire eligible risk set and
sum weights in place of counts. Retain the complete-case estimate
using the linked analytic weights as a separate result. The public
report does not provide (R) or (E) for the baseline quitters,
so it supplies no numerical relapse bound narrower than 0 to 1
without further assumptions or linked results.

If the ITC team can produce a disclosure-reviewed table, the
first attrition analysis can use aggregates. For each baseline
quit-duration stratum, request the eligible baseline count and
separate counts for QA08342 codes 1, 2 and 3, item nonresponse,
routing exclusions and no follow-up. These categories must sum to
the eligible baseline count. Request baseline weight sums for the
same cells and linked analytic weight sums for codes 1–3. For
design-based uncertainty, request estimates and standard errors
computed by the data holder with the survey design. Treat suppressed
cells as unknown. This table suffices for marginal interval status
and attrition bounds. It cannot support respondent-specific interval
lengths, joint product transitions or adjustment for confounders.

For the Australian branch, the [ITC 4 Country Wave 9 to 10 analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC9064888/)
followed 584 former smokers across Australia and the UK for about
one year. Its regression concerns smoking relapse at follow-up
among respondents who were successfully recontacted. The pooled
predictor odds ratios do not yield an Australian absolute
transition probability. The reported lack of a significant
country interaction does not establish a common baseline risk.
Treat Wave 9 as potentially shared with the earlier Waves 1–9
analysis and reconcile person and wave overlap before assigning
independent validation status. A comparable Australian benchmark
needs AU-only eligible and observed denominators, absolute
outcomes by baseline quit duration and a crosswalk to NZL3.5
codes 2 and 3. Do not treat reported resumption followed by
another quit as current smoking at follow-up.

The newer [ITC Four Country Smoking and Vaping analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11035710/)
uses 2018 and 2020 observations on 1,064 retained baseline former
smokers, including 149 in Australia. Section 3.1 reports 114 events
across the four countries and higher pooled relapse among people
abstinent for up to a year. Using only the published pooled event
total and country sample sizes, anywhere from 0 to 114 events
could be Australian (0% to 76.5% of the retained Australian
sample). This is a counting bound conditional on those totals,
not a confidence interval or a bound on the Australian population.
Country-specific event counts and eligible denominators remain
needed. Prefer this newer cohort for an AU extract feasibility
check, with the earlier cohort retained for historical comparison.
Confirm endpoint and participant overlap before treating either
as a separate validation source.

The newer Australian study's Table 2 models smoking status at the
two-year interview. Its sensitivity analysis counts monthly smokers
as still quit. Align the primary cross-country comparison to
current smoking at recontact, using the frequency fields to
harmonise thresholds and carrying the monthly-smoker recoding as
a sensitivity. NZL3.5 codes 2 and 3 combined remain a separate
interval outcome. Even with a common threshold, the two-year
Australian outcome and shorter NZ interval are distinct prediction
targets. Score each at its observed follow-up horizon. Dividing
either probability by elapsed time would assume away re-quitting
and duration-dependent risk.

## Australian mortality comparator family

The NSW 45 and Up Study provides three related comparisons for
P3 disease history checks. The [all-cause analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC4339244/)
uses 204,953 participants aged 45 or older recruited in 2006–09
with selected major conditions excluded at baseline. The
[cause-specific analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11854379/)
reports mortality contrasts by smoking history and age at cessation.
The [Aboriginal participant analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC8271186/)
includes 1,388 eligible Aboriginal adults aged 45 or older and
reports absolute rates and relative risks by smoking history.

Retain all three in one cohort dependency group. If the cause-specific
results inform calibration, use the all-cause and Aboriginal results
as correlated consistency checks unless a disjoint validation slice
is verified. Reproduce each comparison on its own entry criteria,
age, observation period and reference group. Age at cessation does
not by itself identify risk reversal by elapsed time since quitting.
Cause-specific mortality cannot serve as disease incidence, and the
all-cause check must account for each underlying cause only once.
The Aboriginal cohort is a scoped NSW comparator. It supplies
neither a national Indigenous baseline hazard nor a Māori parameter.
Current baseline hazards, cross-cause dependence and independent
prediction validation remain open.

The [Busselton mortality study](https://pubmed.ncbi.nlm.nih.gov/6853663/)
offers a separate Western Australian cohort of 1,564 people observed
over 1966–79. Its smoking association is a historical directional
check. The era and published endpoint summaries do not support an
independent quantitative check of current mortality by quit history.

For the NSW all-cause paper, distinguish its cohort mortality
contrast from the national absolute-rate illustration. The latter
combines the cohort relative risk with 2010–11 Australian population
mortality and external smoking prevalence. If those same inputs
are used to reconstruct model baseline hazards, agreement with the
illustration is an accounting check. Reserve independent predictive
validation for an outcome from a separate eligible population or
period whose deaths were not used to derive the model inputs.

## Australian population mortality anchor

The [ABS Causes of Death 2025 release](https://www.abs.gov.au/statistics/health/causes-death/causes-death-australia/2025)
distinguishes final results through 2022, revised 2023, preliminary
revised 2024 and preliminary 2025. Default tables use registration
year and usual residence. Freeze the vintage, year basis and ICD-10
underlying-cause definitions before joining denominators. A historical
occurrence-year model needs occurrence-year counts and an allowance
for registration lag. Do not substitute the age-standardised
headline rate for an age-specific hazard.

Within a matched age, sex, year and cause stratum, a population
rate already mixes never, former and current smokers. Under a
multiplicative hazard model with compatible risk-set shares and
relative hazards, divide the observed rate by the share-weighted
mean relative hazard to recover the implied never-smoker rate.
Recombine the reconstructed rates as an accounting check. For
example, with shares 0.6, 0.3 and 0.1 and relative hazards 1, 1.5
and 3, a population rate of 13.5 per 1,000 person-years implies
10 per 1,000 for never smokers. Applying those multipliers directly
to 13.5 would reconstruct 18.225 instead. This arithmetic depends
on compatible stratum definitions and a transportable model. The
ABS aggregate alone does not identify the smoking-specific hazards.

The [ABS 2022 National Health Survey workbook](https://www.abs.gov.au/statistics/health/health-conditions-and-risks/national-health-survey/2022/NHSDC14.xlsx)
provides joint age and sex smoking shares. Table 14.3, cells F43–F44
and F73–F74, give current and former smoking at ages 45–54 as
17.8% and 33.1% for males and 12.8% and 28.6% for females.
Use total current smoking, which includes weekly and less frequent
smoking, when the relative hazard definition matches. Table 14.4
provides margins of error, which do not identify the joint covariance.

For a 2022 national candidate slice at ages 45–74, use the
non-overlapping survey bands 45–54, 55–64 and 65–74. Aggregate
finer mortality counts and matching exposure denominators to those
bands before dividing. Avoid using the overlapping 45–64 and 65+
survey totals in the same partition. Confirm household survey
coverage against the mortality population before interpreting the
shares as risk-set weights. The workbook does not split former
smokers by quit duration, so the three-status candidate cannot
identify duration-specific hazards. No mortality join was executed.

Readback of the [ABS national underlying-cause workbook](https://www.abs.gov.au/statistics/health/causes-death/causes-death-australia/2025/2025_01%20Underlying%20causes%20of%20death%20%28Australia%29.xlsx)
shows why it cannot complete the 2022 cause-specific join. The
2016–2025 underlying-cause series has sex and cause but no age
dimension. The 2025 age and sex table covers selected leading
causes. The historical age table lists only the top three causes
by age and registration year. None is a complete 2022
age-by-sex-by-cause table. Keep absent cells unknown. A release
with joint underlying-cause counts is required for cause-specific
baseline reconstruction. The age and sex all-cause join can be
qualified separately from the ABS Deaths series.

The 2022 all-cause candidate join was executed on Python 3.15.2.
The [ABS registration-year dataflow](https://data.api.abs.gov.au/rest/dataflow/ABS/DEATHS_AGESPECIFIC_REGISTRATIONYEAR/1.0.0?references=all)
supplied 24 unique observations for Australia, two sexes, six
five-year age groups and two measures (population and deaths).
No observation status flags were present in the selected cells.
Sum counts and ERP into 45–54, 55–64 and 65–74, then join to
Table 14.3 columns F, G and M using rows 43–44 and 73–74. The
six-cell table contains rates per 1,000 ERP. Male rates are
2.814232, 6.447483 and 15.161758. Female rates are 1.762851,
3.811155 and 9.204227, in ascending age order. These are
registration-based descriptive rates, with rounded precision.

The retained derived CSV has SHA-256
`075335e0ffdf1033cdcdf02c8b4fe5298ac6156694866479ca50cf59c141a02f`.
This executes the age-sex alignment diagnostic. Household survey
coverage, compatible relative hazards, joint covariance and
independent validation still gate any empirical hazard fit.

The [AIHW GRIM1008 workbook](https://www.aihw.gov.au/getmedia/169d8961-6672-4e0d-8775-2ae8dc1791f8/AIHW-PHE-229-GRIM1008.xlsx)
supplies a candidate COPD mortality anchor by age and sex. It
covers underlying cause J40–J44. Summing adjacent five-year
cells in Deaths row 129 yields 72, 362 and 914 male deaths
and 68, 289 and 748 female deaths for ages 45–54, 55–64
and 65–74 in 2022. AIHW identifies this year as revised in
this release. The male 45–54 denominator in Populations row
138 is 1,617,202, versus 1,616,427 in the retained ABS deaths
extract. Use the workbook's own denominator for its published
rates. Before deriving a residual cause group, reconcile
same-vintage all-cause counts and use a common denominator.
COPD underlying-cause deaths do not measure COPD incidence.

The [AIHW all-cause companion workbook GRIM0000](https://www.aihw.gov.au/getmedia/b3c7ec4d-55b7-4943-87df-f71c7d33e677/AIHW-PHE-229-GRIM0000.xlsx)
resolves the denominator mismatch for this comparison. The two
GRIM workbooks agree on all twelve selected five-year sex-specific
population cells in Populations row 138. The all-cause counts in
Deaths row 129 also match the earlier ABS extract after aggregation.
Subtracting the COPD counts gives 4,477, 9,176 and 16,939 male
deaths and 2,856, 5,603 and 10,927 female deaths from all other
underlying causes, in ascending age band. This verifies a two-cause
partition on the GRIM denominator. It is an accounting benchmark
for competing mortality. Smoking-specific rates and other disease
partitions still require their own evidence.

The four-cause 2022 partition adds lung cancer (GRIM0225,
C33–C34) and coronary heart disease (GRIM0909, I20–I25).
All four workbooks agree on the selected population cells.
Across six age-sex strata, the three non-overlapping
underlying causes plus the residual equal the all-cause count.
The retained derived CSV has SHA-256
`17cbed64567dd2a5879644d5d01d2bd98f35548fe5bda594fb6e1ea0aa5da072`.
Keep the 2022 partition separate from later vintages when
testing model reconciliation and predictive performance.

The [45 and Up cause-specific supplement](https://static-content.springer.com/esm/art%3A10.1186%2Fs12916-025-03883-9/MediaObjects/12916_2025_3883_MOESM1_ESM.pdf)
confirms that Table S3 uses the same ICD-10 underlying-cause
groups as the three named GRIM rows. Table S7 gives these
fully adjusted HR2 contrasts relative to never smoking.

| Cause | Current smoking HR (95% CI) | Past smoking HR (95% CI) |
|---|---:|---:|
| COPD J40–J44 | 36.32 (26.18–50.40) | 7.24 (5.37–9.76) |
| Lung cancer C33–C34 | 17.85 (14.38–22.17) | 5.52 (4.56–6.69) |
| Coronary heart disease I20–I25 | 2.78 (2.30–3.36) | 1.31 (1.17–1.47) |

This resolves the cause-code crosswalk. The pooled adjusted
contrasts are candidate sensitivity inputs, conditional on
transport to the 2022 national population. They do not establish
age-sex-specific effects, quit-duration trajectories or covariance
between causes and smoking statuses. The residual cause group
needs separate composition and risk evidence. Retain the GRIM
counts as population outcomes with the NSW contrasts as a separate
source family.

The conditional mixture calculation was executed for all 18
named cause and age-sex combinations. The observed GRIM rate
was divided by the smoking-share-weighted hazard multiplier.
Recombination passed for every point and each of the four
current/past HR endpoint combinations. The 54 status-specific
ranges hold population mortality and smoking shares fixed.
They are sensitivity ranges over a rectangle of HR values, with
no joint confidence interpretation.

Retained output SHA-256 values:

- Point reconstruction: `abdcbe7bce5921ec15fe33fede36c77fbfc719439be20efe03fffaa363bc2121`
- HR sensitivity: `c17e847786a6910a321ea39bc2acdf75026666f27e91b816da0e6e9a4482b0e4`

Other causes account for 73.75% to 86.80% of registered deaths
across the six strata. Adding the reconstructed named causes
therefore does not establish smoking-specific all-cause survival.
An all-cause contrast used to allocate the residual would need
compatible risk sets, a common adjustment model and non-negative
residual hazards for every smoking status. Retain the residual
population rate separately until that evidence is qualified.

## Conditional health accounting implementation

The all-cause HR2 point estimates from Table S7 are 2.82 for
current smoking and 1.37 for former smoking. Combining those
with the three named cause contrasts gives positive residual
rates in all six strata. All 256 combinations of marginal HR
endpoints per stratum preserve positive residuals and reproduce
the observed population residual when recombined. This is a
numerical sensitivity check under the shared transport assumption.

The health module implements competing mortality, survivor
carry-forward, and QALY valuation from living person-time.
Policy and reference comparisons share one duration grid and
valuation schedule. The benchmark uses fixed smoking status
and constant hazards within each interval. One-year cause
probabilities agreed with daily midpoint integration within
1e-10 across 18 age-sex-smoking groups. The workstream integration
suite passed 27 tests at commit 74adaac on Python 3.15.2,
including a changing-cause example with a negative utility.

The module matrix now records these conditional implementations.
Empirical disease incidence, risk reversal, policy-linked
exposure trajectories, utility admission and independent
prediction validation remain open.

Full suite at cadd79c on Python 3.15.2 returned 1,281 passed,
23 skipped and 19 failed in 60.83 seconds. All failures are
in hosted lineage. The scientific inventory includes
src/tobac/health.py and no longer matches the signed native
acceptance capsule. A read-only counterfactual hash with just
that new path omitted matches the capsule. This isolates the
cause of the inventory mismatch without altering the verifier.
The native evidence owner needs to qualify the integrated
scientific inventory and renew the signed capsule before a
full-suite acceptance claim. The 28 workstream integration
tests passed at the same source checkpoint.

## Australian COPD health-system cost comparator

[AIHW's COPD report](https://www.aihw.gov.au/reports/chronic-respiratory-conditions/copd)
reports about AUD 1.8 billion in 2023–24 health-system spending and
AUD 2,500 per prevalent case, with male and female estimates of
AUD 2,700 and AUD 2,300. Its [spending methodology](https://www.aihw.gov.au/getmedia/e3bcf5bf-06f2-4d66-a81c-accef0ff08d6/Health-system-spending-per-case-of-disease-and-for-certain-risk-factors.pdf)
divides allocated national expenditure by modelled Australian
Burden of Disease Study period prevalence. The 2022 self-reported
survey count for adults aged 45 and older uses another denominator.
Reconstruct the published spending-per-case result using the
modelled prevalence and the matched expenditure vintage.

Use this as a check on aggregate annual health-system spending
after matching disease scope and population. Marginal costs of
preventing an incident case require the timing and resource use of
diagnosis, continuing care and exacerbations. Keep the published
tobacco-attributable expenditure estimate separate from policy
savings because the modelled policy changes exposure over time
and affects multiple conditions and survival.

The [AIHW machine-readable cost-per-case workbook](https://www.aihw.gov.au/getmedia/c6b981c6-4952-4b60-b779-43f4b1959323/Health-system-spending-per-case-of-disease-and-for-certain-risk-factors-Cost-per-prevalent-case.xlsx)
gives 2023–24 COPD all-area spending per prevalent case of AUD
2,278.60 for females, 2,691.03 for males and 2,478.96 for persons
(Table 1 rows 1711, 3465 and 5345). These reproduce the rounded
COPD report estimates. The flat file publishes the ratios without
the underlying spending and prevalence columns. Keep the numerator
and denominator reconciliation open.

The COPD report lists 62% of COPD spending attributable to tobacco,
while the spending report summary shows 68% for the same stated
year. Keep both as source-specific claims pending the risk-factor
table and vintage reconciliation. The cost-per-case values above
are for all areas and do not resolve the attribution difference.

The [AIHW risk-factor flat file](https://www.aihw.gov.au/getmedia/de998187-ca0e-4af7-b3e4-aa704e1d14c5/HWE_88_-Risk_factor_flat_file.xlsx)
resolves the two percentages. Both 2023–24 COPD rows use total
spending of AUD 1,752,436,841.30. Row 544 (Summable) attributes
AUD 1,086,200,585.50 to tobacco, or 61.9823%. Row 1344 (Total)
attributes AUD 1,188,057,140.30, or 67.7946%. The former adjusts
for overlapping risk pathways and the latter is the single-risk
attribution. Select the row according to the estimand. Adding the
single-risk estimates across risk factors would count overlap.

Dividing the matched total expenditure by the persons cost per
prevalent case implies approximately 706,923 cases. This is a
back-calculation, pending direct verification of the modelled
prevalence count.

The ten service rows in the AIHW cost-per-case workbook (Table 1,
rows 5346–5355) sum to the persons all-area result within one
millionth of a dollar. Public admitted care contributes AUD
1,416.68 per prevalent case. Including private admissions, public
emergency and public outpatient services gives AUD 1,913.21
across hospital settings, about 77.2% of the all-area total.
Use the service-specific rows to check the mix of costs. The
all-area row already includes them. An admission-level model
needs admission counts and resource costs per episode before
using this population spending benchmark to check its totals.

## Australian temporal mortality benchmark

Using GRIM Deaths row 130 and Populations row 139, the frozen
2022 rates were applied to the observed 2023 populations for
the same six strata. The expected and observed counts each
reconcile across the disjoint causes. All-cause expected deaths
were 52,994.77 versus 50,465 observed. The mean absolute error
and sum of Poisson deviances across six cells are:

| Endpoint | Mean absolute error in deaths | Poisson deviance |
|---|---:|---:|
| All causes | 421.6288 | 130.7220 |
| COPD | 17.1125 | 19.0417 |
| Lung cancer | 29.5209 | 11.9805 |
| Coronary heart disease | 70.7094 | 42.3363 |
| Other causes | 328.2932 | 99.7331 |

Use each row as a separate comparison. The all-cause row overlaps
the component causes. The derived CSV has SHA-256
`d89d6206560335c6b5492c75e246fd6db93616bb47d006b2ec6fcd78e9719562`.
This is a temporal population benchmark conditional on observed
2023 ERP. It does not validate smoking-specific hazards. Any
model tuned after seeing these results needs a fresh holdout for
an independent predictive claim.

Using five-year age groups to transport the frozen 2022 rates
slightly worsened mean absolute error for every endpoint in the
exploratory 2023 comparison. In 2024, with GRIM Deaths row 131
and Populations row 140, the finer ages reduced all-cause mean
absolute error from 411.979 to 411.425 deaths per stratum.
Errors increased for each named cause. Keep the ten-year
reference as the simple comparator. The 2024 table uses observed
ERP and preliminary registration counts, and has SHA-256
`c4b9a9f383841aa22461a077ff9807553261f7ed30d7f27dab191b565764a005`.
These two evaluation years now form part of the visible evidence.

## New Zealand mortality acquisition

The [Health New Zealand Mortality Web Tool](https://tewhatuora.shinyapps.io/mortality-web-tool/)
reports a 24 March 2026 extract by registration year. It labels
2022 provisional and 2023 preliminary, and describes downloads
with three-character ICD-10-AM data. The visible subgroup table
has broader classifications. The retained internal browser tab
could not be rebound on the next turn, so the full export remains
unverified.

The [WHO raw mortality release](https://www.who.int/data/data-collection-tools/who-mortality-database)
provides a separate acquisition route. In the 23 February 2026
edition, the country-code file identifies New Zealand as 5150.
Streaming the entire ICD-10 Part 6 CSV (2021 onward) returned
zero rows for that code. This establishes a coverage gap in
that file. Check the release availability index and alternate
format file before drawing a wider conclusion about WHO coverage.

The WHO February 2026 availability workbook lists 2020 as
the latest New Zealand mortality and population year. The
alternate ICD-10 archive contains Germany and Norway only.
Part 5 contains 2,246 New Zealand 2020 records, all list 104
and death format 00. The national AAA rows report 17,005
male and 15,782 female deaths. The population file contains
one 2020 row per sex in format 01. Use the release format
dictionary to match age columns before computing rates. This
supports a historical national comparator. The contemporary
2022–23 and ethnicity-specific analysis needs Health NZ data.

The 2020 WHO list 104 file and population file align on the
six age-sex bands used in the Australian comparator. Death
format 00 and population format 01 both use columns 15–20
for ages 45–74. Detailed New Zealand death codes sum to AAA
in each band. Counts from J40–J44, C33–C34 and I20–I25 were
reconciled with the residual. The six-row New Zealand partition
has SHA-256 `5626b6b904024a1116a032ad89104ca0180122d1911b45df1e59335dad0f0522`.

The 2020 comparison uses AIHW GRIM Deaths row 127 and
Populations row 136 for Australia. Applying the pooled 2020
NZ–AU population weights for ages 45–74 to both countries
gives 609.18 versus 544.27 deaths per 100,000 residents.
The 64.91 difference decomposes into COPD 1.13, lung cancer
8.05, coronary heart disease 22.94 and other causes 32.78
before rounding. This is standardisation within the selected
six strata. It provides a historical population check while
keeping smoking histories and ethnicity-specific rates separate.
The standardised CSV has SHA-256
`dccbdbbe35669711c36610b3e2cc5068cb9334a7e4c39f47a5f11b97f4a21474`.

## New Zealand smoking-linked mortality comparator

[Teng et al.](https://www.nature.com/articles/s41598-017-11785-x)
link three New Zealand census cohorts to mortality at ages
25–74. Table 1 gives 2006–11 fully adjusted current versus
never smoking rate ratios of 1.79 for men and 1.90 for women
for all causes, and 6.71 and 11.0 for COPD. The all-cause
ratios for Māori men and women were 1.28 and 1.38, compared
with 2.01 and 2.14 for European/Other. Models adjust for age,
ethnicity where applicable, socioeconomic position and household
smoking. Most analyses set former smokers aside.

Retain these as historical comparisons on the study's adjustment
and population scope. European/Other excludes people prioritised
as Māori, Pacific or Asian and cannot be substituted for non-Māori.
A smaller relative contrast can coexist with greater absolute
burden when baseline mortality differs. Keep the rate-difference
evidence alongside the ratios for equity checks. These ratios
do not identify 2020 age-specific rates or risk by time since
cessation. The companion mediation analysis uses the same
cohorts and belongs in the same source dependency group.

The [Teng et al. supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-017-11785-x/MediaObjects/41598_2017_11785_MOESM1_ESM.doc)
provides age-standardised COPD rates by smoking status and ethnicity
for ages 25–74. In 2006–11, Māori men had 19.2, 69.8 and 95.5
deaths per 100,000 for never, former and current smoking. The
European/Other rates were 3.2, 18.4 and 52.8. The current-versus-never
rate difference was therefore larger for Māori men (76.3 versus
49.6), despite the smaller reported rate ratio (4.98 versus 16.4).
The women's COPD rows show the same ordering on the two scales.

Keep the COPD standardised contrasts (Tables S2–S3) separate from
the adjusted all-cause predictions (Table S4). For its specified
60–64-year-old covariate profile, Table S4 shows smaller all-cause
rate differences for Māori in 2006–11. The direction of the
absolute comparison depends on endpoint and estimand. The former
smoker rates in Tables S1–S3 are historical status averages and
do not identify a trajectory by time since quitting.

## Mortality by time since quitting

[Thomson and Islami](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2811807)
linked US NHIS interviews from 1997–2018 to deaths through 2019.
Among 438,015 adults, the adjusted mortality ratios for former
versus never smokers differed by cause and quit-duration band.
The 1–9-year and 30-plus-year contrasts were 1.47 and 0.97 for
cardiovascular deaths, 2.13 and 1.16 for cancer, and 6.35 and
1.31 for respiratory deaths. Duration is measured at recruitment.
These band averages cannot resolve a first-year change, a
continuous decay curve or an individual's effect of quitting.

The outcome definitions are wider than the P3 cause partition.
Respiratory mortality includes J40–J47, cancer C00–C97, and
cardiovascular mortality includes heart and cerebrovascular
causes. Do not directly assign the three curves to COPD,
lung cancer and coronary heart disease. Use them to check the
need for cause-specific lags and retained excess risk in
sensitivity scenarios. A matched NZ or AU time-since-quit
calibration and transport assessment remain open.

The [Australian cause-specific cohort paper](https://link.springer.com/article/10.1186/s12916-025-03883-9)
stratifies cessation by age at quitting below 55, using bands
under 35, 35–44 and 45–54. Figure 3 compares each band with
never smokers. Earlier cessation can imply both fewer years
of smoking and more years since quitting. These contrasts
cannot separate those effects or cover people quitting at 55
or later. Retain them as a historical age-at-cessation check.

The paper also redistributes deaths coded I50 as the underlying
cause using proportional allocation. The GRIM comparison uses
registered underlying causes. Matching the nominal codes in
Table S3 establishes the category crosswalk but does not
establish identical case assignment. Before using the cohort
hazard ratios with GRIM, reconcile the redistribution rule or
obtain estimates on the unredistributed endpoints. The existing
conditional reconstruction remains a numerical sensitivity.

The cohort cites the [Australian Burden of Disease Study 2011 methods](https://www.aihw.gov.au/getmedia/a5720628-caf4-4639-9837-6efec6dc3d2b/aihw-19666-bod6.pdf).
Appendix Table B2 describes direct evidence and indirect
multiple-cause-of-death methods for I50. It reports 2,903
redistributed deaths in that study. That historical count
and method description do not supply the cohort's realised
allocation weights by smoking status, sex and age.

The GRIM0907 sensitivity bounds the registered-count difference
in the 2022 six-stratum comparator. At most 292 I50 deaths
could be added to 5,248 registered coronary heart disease deaths
if every I50 death were assigned there. This increases the
combined count by 5.6%, with stratum rate increments of 0.42
to 10.61 per 100,000. The CSV has SHA-256
`4b4d6b1fde94a8ffc0c5e3d2842324e3ac4df4ac37a2017f2e9ef10b70a7b2e9`.
This bounds count reassignment on the GRIM side. It does not
bound changes in a fitted cohort hazard ratio.

## New Zealand first recorded COPD admission

The indexed [2024 respiratory impact report](https://www.asthmafoundation.org.nz/assets/documents/Respiratory-Impact-Report-2024sep10-FINAL.pdf)
confirms 6,596 people with a 2022 COPD admission and no
prior recorded COPD admission since 2000. It reports a
national rate of 128.9 per 100,000 and a mean age at first
recorded admission of 71.6 years, compared with 64.8 for Māori,
65.8 for Pacific and 74.4 for non-MPA. The report describes
age standardisation to 2018 Stats NZ population estimates.
Retain the reported ethnicity rate ratios as separate estimates
until the underlying model and denominators are read back.

This is an observed first hospital event within an available
lookback. It can check a hospitalised COPD transition if the
model matches the case definition and registration window.
It does not measure clinical onset, diagnosis outside hospital
or the entire population at risk after removing prior COPD.
The live publisher URL returned HTML in the direct download,
so the findings were verified against the indexed report text.

### Within-interval diagnosis and mortality

The health calculation integrates disease-free and diagnosed
person-years under constant hazards and irreversible diagnosis.
It counts incident diagnoses even when a person dies before the
interval ends. The analytical regression uses equal incidence
and post-diagnosis death hazards and checks both occupancy and
event counts. Empirical use still requires matched clinical
incidence and mortality for the same population and diagnosis
definition.

### Australian COPD cohort comparability

The [remote Aboriginal cohort](https://www.sciencedirect.com/science/article/pii/S1326020023022653)
reported 164 first hospital-diagnosed cases over 21,614 person-years
among 1,374 participants. The crude event rate is 7.59 per 1,000
person-years. The study separately estimated lifetime risk with competing
death at 53% overall, 61% for women and 45% for men. Keep the crude
rate and lifetime risks as separate comparators for that cohort. Neither
identifies an age-specific clinical diagnosis hazard or a national
Indigenous parameter.

The [South Australian tertiary cohort](https://pmc.ncbi.nlm.nih.gov/articles/PMC12964674/)
included 8,578 inpatients and outpatients with post-bronchodilator
spirometry diagnoses during 2006–2021. Its 3- and 5-year COPD mortality
predictions were evaluated on a temporal hold-out from the same site.
The hold-out discrimination measures can inform prognostic model choice
within that referral population. The cohort starts after ascertainment,
and discrimination measures do not identify an absolute all-cause death
hazard. Keep these estimates separate from the remote cohort's first
hospital diagnoses. Matched population incidence and mortality inputs
remain open.

### Australian linked COPD service-use mortality

The [AIHW linked report, page 7](https://www.aihw.gov.au/getmedia/efc80e4d-b373-43c2-953b-e6fe8b09cad2/aihw-acm-43.pdf)
reports one-year all-cause mortality of almost 7% among service-identified
COPD cases aged 35 and over at 30 June 2018, versus 1.0% among people
without that flag. The 46% with COPD on the death record refers to deaths
among flagged cases in the original report. The later overview places that
percentage after the unflagged comparison, so use the original denominator.

This is a benchmark for baseline service-identified prevalence. The
66,200 first service identifications in 2018–19 require survival to
30 June 2019 and no qualifying service record since July 2010. Their
count excludes people identified and dead within the same interval,
which the illness–death calculation explicitly counts. A matched
comparison would need either a model output filtered to surviving
first service identifications or linked transition counts that include
deaths before the reference date. Clinical diagnosis incidence and
mortality by time since first diagnosis remain open.

The locally verified AIHW report (PDF SHA-256
`92e6563637353638ab9ab717e8d9a880297897289478ce14336d06f931bdc7d0`)
specifies three qualifying routes in the year before 30 June. A case
requires at least two COPD medicine dispensings, a hospital event with
a principal or additional COPD diagnosis, or an emergency presentation
with either diagnosis position. Version 1.0 lacks WA and NT hospital
and emergency records and most private hospitalisations. Medicines
dispensed by remote Aboriginal health services cannot be linked to
individuals in this extract. A comparison needs these same observation
rules in addition to survival and prior-history eligibility. Coverage
differences also limit interpretation of equity contrasts.

The [AIHW technical report](https://www.aihw.gov.au/getmedia/4137c243-d3bc-4ec5-9bed-60c4a9847592/aihw-acm-44.pdf.aspx)
(PDF SHA-256 `11992c6dc6974d7a7d3c7242fd7e6096ca18051d948c94a9aca807710c282b9b`)
refines the 2018–19 one-year mortality benchmark to 6.8% among
baseline cases. Among June 2019 prevalent cases, 93% qualified via
dispensing and 82% qualified through dispensing alone. Hospital and
emergency records captured 16% and 7.4%, respectively, with overlap.
Dispensing captured 93–94% of linked cases at ages 55–84 and 90–91%
in the other age bands. These are observed shares of the linked case
definition. They give a dispensing-only sensitivity comparator for
prevalence, with neither a clinical sensitivity estimate nor a correction
factor for first identifications or areas with missing linkage.

Table A6 of the same technical report provides three comparable annual
prevalence snapshots after most ascertainment markers became available.
Counts rose from 347,440 in June 2017 to 350,340 in June 2018 and
365,110 in June 2019, while prevalence standardised to the 2001
Australian population was 2.3% in all three years at published precision.
Keep the reported crude 2019 prevalence of 2.7% separate. Exclude the
earlier rise from a disease-trend fit because AIHW identifies a change
in available markers. A temporal check can freeze the 2017 age-specific
prevalence and compare the 2018 and 2019 strata on the same observation
definition. These repeated snapshots share people and data infrastructure,
so a temporal comparison within this series cannot supply independent
external validation.

The fixed-2017 comparison was executed against the six Table A6 age
bands with equal weight and prevalence at the published one-decimal
precision. Mean absolute error was 0.050 percentage points for 2018
and 0.067 for 2019. Four bands matched at published precision in each
year. The largest error in both years was 0.2 points at ages 65–74.
Retain these errors as the simple temporal baseline for any model
using the same ascertainment and age bands. Rounded observations
support a descriptive error comparison, without a sampling uncertainty
test. The local 12-row calculation receipt is
`au-copd-2017-fixed-prevalence-benchmark.csv` (SHA-256
`14047a6bcdf14d7701392bb26b0d1f2d8577d66214455b51797ea4bc430eb525`).

Rounding sensitivity for that baseline allows each reported percentage
to differ from its unrounded value by up to 0.05 percentage points,
assuming rounding to nearest. Each absolute difference between the
2017 and later reported values can therefore move by up to 0.10 points,
with a floor of zero. Applied to the 12-row receipt, this gives
conservative mean absolute error ranges of 0.017–0.150 points in
2018 and 0.033–0.167 in 2019, rounded to three decimals. These
ranges reflect reporting precision only. When comparing a candidate
against the fixed baseline, score both on the same admissible values
within each rounding interval so a small apparent improvement at
published precision does not determine model choice.

For a second simple comparator, extrapolate the 2017–2018 change by
one year within each age band, using 2019 only for scoring. Against
Table A6, equal-weight mean absolute error at published precision is
0.100 percentage points for this trend and 0.067 for the fixed 2017
baseline. Retain the fixed baseline for comparison with a future
service-ascertainment model. The difference is small relative to the
reporting precision and does not establish superiority on unrounded
data. The six-row local receipt is
`au-copd-2019-linear-trend-benchmark.csv` (SHA-256
`e30ff518c5927156fd7c1668c643bf5bfd14af718f979fd2fea7d46c84bf049a`).

The ranking can reverse within the published rounding intervals.
For ages 65–74, perturb the 2017, 2018 and 2019 rates by −0.04,
+0.04 and −0.04 percentage points. For ages 85 and over, use −0.04,
+0.04 and zero. Leave the other bands at their published values.
All inputs round back to Table A6. With both comparators scored on
these same values, the fixed baseline error is 0.0733 points and
the linear trend error is 0.0533. This is a rounding sensitivity
example rather than a reconstruction of the underlying rates.

### Full-suite software checkpoint

At `b92c7b1f5200e15554e604634290ab696a6e3287`, the full checkout
ran `python -m pytest -q` with repo-local Python 3.15.2 and
`PYTHONPATH=src` under the 4 GiB, 40-minute resource guard.
Result was 1,300 passed, 23 skipped and 19 failed in 48.01 seconds,
with peak sampled process-group RSS of 740.2 MiB. All failures
were in hosted lineage, where the verifier rejected the scientific
inventory against signed native acceptance. The native inventory
owner must reconcile this before the full-suite gate can pass.
The local log `tobac-p3-full-b92c7b1.log` has SHA-256
`8a77d7ae575b19d39097156529a600bab2fb12972b92808e7137851cdc4c6483`.

### Australian excise and product substitution comparator

[Wilkinson et al. (2019)](https://pubmed.ncbi.nlm.nih.gov/31759897/)
used monthly survey prevalence among people aged 14 and over in five
capital cities. After the April 2010 excise increase, the estimated
immediate change was −0.745 percentage points (95% CI −1.378 to −0.112)
and the reported monthly trend was −0.023 points (−0.044 to −0.003).
Factory-made cigarette smoking drove the decrease, while roll-your-own
smoking prevalence rose over the subsequent segment. At the start of
the later annual increases, the immediate estimate was −0.997 points
(−1.632 to −0.362) and the subsequent trend was −0.044 points per
month (−0.063 to −0.026).

Use these as historical checks on aggregate prevalence and product
response for the study population and policy dates. The excise change
is a tax shock, and its percentage is insufficient to identify the
retail price change or a price elasticity. Product prevalence is
also insufficient to identify individual switching or cessation.
Separate estimated segments from the same survey share a dependency
group. Joint quantitative use requires the fitted coefficient
covariance and reconciliation of the study's prevalence definitions.

[Scollo et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4401343/)
provide observed prices paid around the December 2013 increase.
The repeated cross-sectional national adult smoker survey compares
December 2012–November 2013 with December 2013–March 2014. In real
March 2014 dollars, reported prices rose 10.7% for value, 13.2% for
mainstream and 15.7% for premium factory-made cigarettes, and 13.8%
for roll-your-own tobacco. The price units are per stick and per
0.8 g, respectively. Mean daily consumption among regular smokers
fell from 14.8 to 14.0 cigarettes over the same comparison.

Use the price changes as segment-specific historical observations.
They reflect both prices and the products that surveyed smokers chose
to buy. A pass-through estimate requires matched product prices and
the absolute duty change in the same unit. A prevalence elasticity
would additionally need a compatible counterfactual, exposure period
and population. These national adult price observations cannot be
divided into the five-city age-14-and-over prevalence coefficients
to obtain that elasticity.

[Bayly et al., Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9411903/)
tracked the same 18 products and pack sizes monthly in two Melbourne
supermarkets from December 2016 to December 2019. Relative to August,
adjusted month-on-month price changes were 6.50 percentage points
higher in September and 2.99 higher in October for factory-made
cigarettes. The corresponding contrasts for roll-your-own tobacco
were 11.10 and 1.56 points. Both October contrasts had confidence
intervals above zero. An excise model that moves the entire price
response into September misses this timing in the observed panel.
Use the contrasts as a historical timing check. They are changes
relative to August, so compounding the coefficients would not
recover the cumulative shelf-price change. The panel does not
identify national sales-weighted pass-through or the 2013 response.

For a descriptive two-month timing scenario, compound the Table 1
adjusted marginal means, rather than the August-relative contrasts.
September and October means were 6.51% and 3.01% for factory-made
cigarettes and 11.45% and 1.91% for roll-your-own. Starting each
series at an August index of 100 gives October indices of 109.716
and 113.579. The September share of the two-month rise is 0.670
and 0.843 respectively. These are constructed paths through
adjusted means, without sales weighting, a no-excise counterfactual,
or a joint confidence interval. They can exercise the realised-share
input with October as a stipulated endpoint. They cannot identify
the timing or magnitude of the eventual causal pass-through.

A replay through `excise_price_response` with August indexed to 100
recovered September indices of 106.51 and 111.45 for factory-made
and roll-your-own products and October indices of 109.715951 and
113.578695. The immediate-response comparator, given the same
stipulated October endpoint, overshot September by 3.205951 and
2.128695 index points respectively. The replay used a normalised
price increment equal to the two-month rise and unit pass-through
to isolate timing. It checks implementation and quantifies the
consequence of immediate adjustment within this constructed path.
Independent predictive evidence still requires a frozen timing
profile and a separate matched price series.

The [ABS October 2024 monthly CPI release](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/oct-2024)
provides an independent aggregate timing comparison outside the Melbourne
panel period. The monthly tobacco index rose 4.4% in September and
2.8% in October. Compounding the published changes gives a 7.323%
two-month rise, with 60.1% of that rise occurring in September.
This supports a delayed price-rise check at the aggregate tobacco
class level. The ABS class combines products and cannot validate the
two product-specific shares or isolate the excise effect. The earlier
ABS research-page mock-up workbook has a tobacco index header but
reports zero observations in that column. Use the populated release
for this comparison.

Conditioning each timing scenario on the same ABS October endpoint
gives September absolute errors of 2.923 index points for immediate
adjustment, 0.507 using the Melbourne factory-made timing share and
1.775 using the roll-your-own share, with August indexed to 100.
Both delayed scenarios reduce September error in this aggregate
comparison. Because the October endpoint is supplied from the
comparison series, this scores within-window timing only. The ABS
index does not identify the product mix needed for a combined
prediction, and the exercise cannot rank product-specific models.

A rounding sensitivity check allowed each Melbourne monthly mean to
vary by 0.005 percentage points and each ABS monthly change by 0.05,
assuming rounding to nearest. The September error ranges were
0.452–0.561 index points for the factory-made timing scenario,
1.722–1.829 for roll-your-own and 2.870–2.977 for immediate
adjustment. These extrema follow from evaluating the endpoints of
the reporting intervals. Delayed adjustment retains lower error
throughout these intervals for the aggregate timing comparison.
The ranges cover publication rounding only and do not quantify
sampling or transport uncertainty.

The [ABS October 2023 monthly CPI release](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/oct-2023)
provides a second out-of-panel aggregate window. Tobacco prices rose
4.8% in September and 3.4% in October, a compounded 8.3632% rise.
September accounts for 57.4% of that window. Conditioning on October
as in the 2024 comparison, the September absolute errors are 3.563,
0.804 and 2.252 index points for immediate, factory-made timing and
roll-your-own timing respectively. Both frozen delayed shares improve
on immediate adjustment in both ABS windows, with positive September
errors in each case. The aggregate series supports this timing
comparison while product-specific pass-through remains untested.

The [ABS October 2022 release workbook](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/oct-2022/648401.xlsx)
contains populated monthly tobacco index values, unlike the earlier
mock-up. The retained workbook has SHA-256
`4358d685e42cc45740970d87edb83e7194a25ca4dd9f082016039854aadf45a0`.
Outside the Melbourne panel, September accounted for 56.5%, 40.0%
and 61.3% of the August–October rises in 2020, 2021 and 2022
respectively. Both frozen delayed scenarios again reduce September
absolute error relative to immediate adjustment when given the same
observed October endpoint. The comparison spans different duty
regimes and measures timing of aggregate prices only. Do not pool
the windows as replications of a common causal tax effect.

A simple equal-increment comparator assigns half of the August–October
rise to September. Across the five ABS windows (2020–2024), with August
indexed to 100 and equal weight per year, its mean September absolute
error was 0.517 index points. The corresponding errors were 0.644
for the factory-made share, 1.763 for roll-your-own and 2.775 for
immediate adjustment. The equal split had lower error than the
factory-made share in three of five years. The comparison supports
staging within the two-month window, while the more detailed
Melbourne shares have yet to demonstrate incremental predictive
value against the simple aggregate split. All scenarios were given
each observed October endpoint.

Removing one ABS window at a time leaves the equal split ahead of
the factory-made share in all five four-year comparisons. Its mean
absolute error advantage ranges from 0.029 index points when 2020
is excluded to 0.216 when 2024 is excluded. Retain the equal split as
the simple comparator for aggregate timing. This sensitivity keeps
the October endpoint fixed to each observed value and does not
establish out-of-window price prediction.

The local receipt `au-excise-timing-abs-2020-2024.csv` preserves all
five windows, the original or reconstructed index basis and each
scenario error. Its SHA-256 is
`074e9df19e636bf7d95b4aaa5912a96966cc26a6b97e2224cf145be1df1645dc`.
The 2020–2022 rows use the October 2022 release index levels. The
2023–2024 rows reconstruct levels from the published monthly changes.
All errors are scored after normalising August to 100.

### Equity comparison for service-identified COPD

Table A7 of the [AIHW technical report](https://www.aihw.gov.au/getmedia/4137c243-d3bc-4ec5-9bed-60c4a9847592/aihw-acm-44.pdf.aspx)
reports age-standardised prevalence of 3.1% in the most disadvantaged
IRSD quintile and 1.5% in the least disadvantaged, a 1.6 percentage
point gap at published precision. Both regional groupings report 2.8%
versus 2.1% in major cities. The standard is the 2001 Australian
population. The five IRSD case counts sum to 363,739 and the three
remoteness counts to 363,805, leaving 1,371 and 1,305 cases respectively
against the national Table A6 total of 365,110. Preserve these residuals
in separate reconciliation checks. The two tables are marginal views
of the same cases and cannot identify joint strata. The gradients
reflect service ascertainment and area of residence, with coverage
differences relevant to interpretation.

Using the national case total as the common universe, Table A7
allows anywhere from 0 to 47,375 flagged cases to be both in the
most disadvantaged quintile and in the combined outer regional,
remote and very remote category. The bounds use the larger of zero
and the sum of the marginal counts minus the national total as the
lower limit, and the smaller marginal count as the upper limit.
The national total includes the unclassified residuals. These
bounds show that even the direction of the overlap concentration
is unresolved by the two tables. Intersectional prevalence and
policy effects need joint case counts and population denominators.

Table A8 reconciles 66,161 first service identifications among people
alive on 30 June 2019, including 33,208 men and 32,953 women. The six
age-band counts sum to the same total. Ages 65–74 contributed the
largest count (19,103, or 28.9% of first identifications), while ages
35–44 had the highest share of their own prevalent cases newly
identified (39.2%). Across all ages 35 and over that share was 18.1%.
These denominators answer different questions. A predictive check
should compare surviving first-identification counts in matched
strata, with the published proportions calculated over all cases
flagged at the reference date. The at-risk person-years needed for an
incidence rate are a separate input.

A leave-one-age-band-out baseline uses the other five bands to
estimate a common newly identified share, then multiplies it by
the held-out band's year-end case count. It underpredicts all three
bands below 65 and overpredicts all three older bands. At ages
35–44 the prediction is 1,337 versus 2,967 observed. At ages 75–84
it is 21,068 versus 15,358 observed. This is a conditional check of
the age distribution given the prevalent totals, using the same
source and year. It supports requiring age-specific ascertainment
checks before accepting a pooled service-identification parameter.

An ordinal age-band trend reduces conditional count error in the
same leave-one-band-out exercise. For each fold, fit an unweighted
straight line to the log odds of the newly identified share in the
five training bands, using indices zero through five for the ordered
bands. Convert the held-out prediction back to a share and multiply
by its observed year-end case count. Equal-weight mean absolute
count error was 1,714 versus 2,881 for the pooled share. The trend
improved four of six bands and worsened ages 65–74 and 85 and over.
The open-ended oldest band is treated as one ordinal step, not as a
numeric age midpoint. This comparison uses one source and one year.
An independent year or cohort is needed before transporting the
age pattern.

Table A8 publishes age-by-sex first-identification counts but rounds
their shares of prevalent cases to one decimal place. The age totals
in Table A6 and those rounded shares bound the missing age-by-sex
prevalent denominators. For example, men aged 35–44 can have
3,467–3,474 prevalent cases. The bounds intersect the integer counts
consistent with the men's rounded share with the complement of the
women's corresponding count interval. Across the six ordered bands,
the resulting men's ranges are 3,467–3,474, 10,785–10,817,
29,886–29,951, 57,110–57,315, 55,661–56,015 and 24,127–24,267,
assuming rounding to nearest. Use these as per-band bounds rather
than reconstructed exact denominators. Exact joint denominators
would allow a direct cross-sex prediction check.

A conditional cross-sex transfer check uses one group's
first-identification share to predict the other group's counts.
Within each age band, the two prevalent denominators sum to its
published total. Evaluating the admissible denominator endpoints
bounds the signed prediction error, and an interval that crosses
zero has a conservative absolute-error lower bound of zero.
Averaged equally over age bands, the count error for transferring
men's age-specific shares to women is bounded by 238–283, versus
1,157–1,182 using the men's pooled share. Transferring women's
shares to men gives 218–262 versus 1,138–1,162. These conservative
bounds need no exact joint denominators or assumption that the
per-band extremes can occur simultaneously. Both groups come from
the same source and year. This checks transfer of the age pattern
conditional on year-end case counts, with external validation open.

### Queensland COPD quality-of-life benchmark

[Endo and Clemens (2026)](https://doi.org/10.1007/s11136-026-04173-4)
linked the 2022–2023 Queensland adult health survey with hospital
administrative records. Using an Australian EQ-5D-5L value set with
a reported range of −0.301 to 1, they report mean utility of 0.780
among people with COPD and 0.917 across the cohort. The crude
difference of 0.137 compares COPD cases with the whole cohort,
which includes COPD. Their adjusted 36.5 disutility days correspond
to 0.100 of a 365-day year, a separate model-based estimand.
Retain both with the study population and ascertainment. The
adjusted contrast can inform sensitivity analysis once the model
and covariates are checked. Neither estimate identifies the utility
loss caused by incident COPD, severity-specific utilities, or a
New Zealand utility on its own tariff.

The Queensland study's propensity model used continuous age, smoking
status and the Charlson Comorbidity Index. It pooled current and former
smokers because cessation dates were unavailable, and disease onset
dates were also unavailable. The reported contrast targets adults with
pre-existing COPD under the study's adjustment assumptions. It cannot
separate a cessation-related utility change from a COPD effect. Among
adults aged 65 and over with COPD, 24.5% also had diabetes in the linked
study versus 19.8% in the comparison survey estimate. Keep the
COPD utility benchmark tied to the linked cohort's comorbidity mix.
Adding a separate diabetes decrement to its crude mean could count
some burden twice. Joint-state utilities or a validated adjustment
would be needed for that calculation.

Table 3 reports the adjusted COPD utility contrast as −0.100
(95% CI −0.122 to −0.078), corresponding to 36.5 disutility days
(28.6 to 44.5). A replay through the QALY calculation with one
undiscounted living person-year gives 0.078, 0.100 and 0.122 QALYs
for the corresponding positive decrement magnitudes. This checks
units and sign for sensitivity scenarios. The confidence interval
describes estimation uncertainty in the linked cohort. It provides
neither joint uncertainty with other disease contrasts nor uncertainty
about transport to incident disease or other populations.

A conditional illness–death replay starts with 1,000 disease-free
people and assumes annual incidence, pre-diagnosis death and
post-diagnosis death hazards of 0.02, 0.01 and 0.07. Over one year
it produces 19.703 first diagnoses, 19.026 surviving diagnoses and
9.673 diagnosed person-years. Valuing that person-time with the
Queensland decrement gives 0.967 undiscounted QALYs of morbidity
loss, or 0.755–1.180 using the reported interval endpoints.
Assigning a full year to each surviving diagnosis instead gives
1.903 QALYs at the central decrement. This replay uses illustrative
hazards and assumes the decrement starts at diagnosis and remains
constant. It isolates morbidity accounting and excludes any
mortality-related loss or uncertainty in the hazards.

A step-size replay began with 1,000 disease-free and 150 diagnosed
people, using annual hazards 0.02 for incidence, 0.01 for
pre-diagnosis death and 0.07 for post-diagnosis death. A single
one-year step and twelve equal steps agreed within an absolute
tolerance of 1e-10 for ending counts, first diagnoses, deaths by
origin, both person-time totals and QALYs. The QALY replay used
illustrative state utilities of 0.88 and 0.78 and zero discounting.
The check verifies accounting under constant hazards and utilities.
Different valuation dates under positive discounting are a separate
source of step-size differences.

With the same illustrative cohort and 5% effective annual discounting,
independent quadrature of the closed-form occupancy weighted by
`(1.05)**(-t)` gives 963.848195 QALYs. A single annual midpoint
gives 963.676902 and twelve monthly midpoints give 963.847005.
The respective errors are −0.171292 and −0.001190 QALYs per
1,150 entrants. The calculation isolates valuation timing because
the underlying person-time is integrated exactly in both runs.
Retain the reported valuation convention when comparing runs
across time steps.

### Paired health uncertainty replay

An illustrative two-year replay used 512 independent latent normal
pairs from NumPy's default generator with seed 3103. Log incidence
and log diagnosed mortality used standard deviations of 0.20 and
0.15 and latent correlation 0.60. The action multiplied incidence
by 0.80 on each shared draw, leaving other hazards unchanged.
Using the previous illustrative starting cohort, utilities and
midpoint discounting, the mean gain was 0.971 QALYs. The Monte
Carlo standard error was 0.00988 with matched draw IDs. Shuffling
the reference outcomes as a diagnostic left the mean fixed and
raised that error to 0.18194. The replay verifies the consequence
of pairing for simulation precision. The distributions, correlation
and intervention effect are illustrative and do not establish an
empirical probability of benefit.

Extending the same nested draw sequence to 1,024 and 2,048 draws
gave gains of 0.962 and 0.966 QALYs, with Monte Carlo standard
errors of 0.00676 and 0.00476. The 512-draw error was 0.00988.
Identical action and reference outcomes gave exactly zero mean
increment and simulation error. This checks the null comparison
and the expected reduction in simulation error as draw count
increases. It does not establish convergence for other actions,
parameter distributions or decision thresholds.

### New Zealand respiratory utility evidence lead

The [Auckland pulmonary rehabilitation registry](https://anzctr.org.au/Trial/Registration/TrialReview.aspx?id=381479)
specifies collection of EQ-5D responses and links the published
[preference-based rehabilitation trial](https://pubmed.ncbi.nlm.nih.gov/37465821/).
Keep it as a source lead. The registry identifies a planned measure,
while the publication metadata do not establish a usable COPD
utility distribution, scoring tariff or separable COPD subgroup.
The recruited rehabilitation population also differs from the
population at first diagnosis. For a local utility sensitivity
analysis, obtain the instrument version, country-specific scoring
basis, time points and COPD subgroup results before using this lead.
The [Pharmac health-benefit guidance](https://www.pharmac.govt.nz/medicine-funding-and-supply/the-funding-process/policies-manuals-and-processes/economic-analysis/prescription-for-pharmacoeconomic-analysis-methods-for-cost-utility-analysis/6-estimating-health-benefits)
specifically names NZ Tariff 2. Keep its instrument and edition
separate from the modern NZ EQ-5D-5L scoring reference.

Full-text readback from the [AUT repository](https://openrepository.aut.ac.nz/server/api/core/bitstreams/d2b7aed8-c178-43f6-9025-611b607c4411/content)
resolves the Auckland trial lead. The outcome reported in the
rehabilitation tables is EQ-5D visual analogue scale, with means
62.35 and 64.08 on the 0–100 scale at baseline. The paper provides
a descriptive respiratory quality-of-life comparator. Its reported
VAS values cannot be divided by 100 and used as tariff-based utility.
The study's planned EQ-5D measurement therefore does not close the
New Zealand COPD utility input.

A separate [New Zealand physiotherapy study](https://nzjp.otago.ac.nz/nzjp/article/download/354/311/1273)
reports EQ-5D-3L summary scores around 6–7 in its outcome table.
The reported scale is incompatible with a preference-based utility
anchored at one for full health. The table does not provide the
distribution of five-dimension profiles required to score utilities
on a New Zealand tariff. Retain this as descriptive rehabilitation
evidence. Scoring a mean summary as if it were a health-state
profile would lose both the dimensions and the response distribution.

### New Zealand excise price partitions

A [2014 retailer price study](https://pubmed.ncbi.nlm.nih.gov/26138823/)
reported median increases of 3% for the sampled budget cigarette
brand, 8% for premium and 11% each for mainstream and roll-your-own.
The study covered four products from one manufacturer. Keep the
percent changes in shelf prices separate from absolute pass-through
ratios and from sales-weighted price changes.

The [2010–2020 price partition study](https://tobaccocontrol.bmj.com/content/33/2/240)
uses volume-weighted real prices for manufactured cigarettes.
The premium to super-value gap widened from 19.7 to 30.5 cents
per stick. Together, the super-value and budget partitions rose from
20.0% to 74.0% of measured volume. This supports separate price
partitions and a check on aggregate composition. Changes in brand
availability, plain packaging and classification over time limit
causal interpretation. The volume shares do not identify individual
switching, and the study's time window overlaps the 2014 event.

A fixed-mix replay of Tables 1 and 2 normalises the four published
shares separately in 2010 and 2020 because rounding leaves each
sum at 99.9%. The resulting aggregate real prices are 62.64 and
135.89 NZ cents per stick. Applying 2020 prices to the 2010 mix
gives 147.85 cents. On this decomposition path, within-tier price
changes add 85.21 cents and the shift in sales mix subtracts
11.97 cents, for a net increase of 73.24 cents. The fixed mix is
an arithmetic comparator. It makes no assumption about how buyers
would have responded in the absence of the tax changes.

Reversing the decomposition order gives a mix effect of −6.46 NZ
cents per stick at 2010 prices and a within-tier price effect of
+79.70 cents at 2020 weights. Averaging the two orders allocates
+82.45 cents to price changes and −9.21 cents to composition.
Both orders reconcile to the same +73.24 cents total. The sales
mix offsets part of the price rise under either order, but the
size of the offset depends on the weighting convention. Keep
both orders when comparing a model's price and composition outputs.

### New Zealand cessation by baseline tobacco product

[Li et al.](https://pubmed.ncbi.nlm.nih.gov/20173806/) followed New
Zealand Quitline callers and measured seven-day point-prevalence
abstinence at six and twelve months. The study enrolled 2,002,
of whom 64% completed six-month follow-up and 42% completed the
study. Adjusted quit outcomes did not differ detectably across
roll-your-own, factory-made and mixed users. Keep a common product
response as a sensitivity comparator within the Quitline setting.
The result does not establish equivalence, continuous abstinence
or a population effect of excise. Product type was observed rather
than assigned, and both help-seeking selection and attrition matter.
A separate [NZ purchase-task panel](https://pubmed.ncbi.nlm.nih.gov/25744952/)
measured intended purchases around the 2013 tax rise. Retain its
outcomes separately from observed consumption and product switching.

[MacFarlane et al.](https://pubmed.ncbi.nlm.nih.gov/22132381/)
compared separate cross-sectional samples before and after the
April 2010 New Zealand tobacco excise increase. The proportion
reporting any quit attempt was 30% before and 39% after, with an
adjusted odds ratio of 1.5 (95% CI 0.95–2.3). The adjusted odds
ratio for reporting an attempt with cost as a reason was 3.6
(2.3–5.6). Keep those endpoints distinct. The first interval
includes no change on the odds scale, while cost motivation
can change without sustained abstinence. Neither estimate
identifies a sustained cessation transition or a product-specific
response. Use the results only for historical attempt and
motivation comparisons.

[Tucker et al.](https://pubmed.ncbi.nlm.nih.gov/27868298/) collected
three waves of questionnaires across two New Zealand excise changes
in 2012–2014. Cigarettes per day declined faster in the combined
Māori/Pacific group than in the NZ European group, while the change
in psychological dependence did not differ detectably. Use this as
a historical comparison for smoking intensity. The pooled group
cannot identify separate Māori and Pacific parameters, and the
reported outcome does not identify sustained cessation.

A [separate study of the 2014 and 2015 increases](https://pubmed.ncbi.nlm.nih.gov/27624346/)
found no detectable before-after change in smoking or product
behaviour around either increase. Retain this alongside the intensity
finding. The studies address different outcomes and time windows.
Neither establishes a causal subgroup cessation effect.

The indexed [Tucker et al. full text](https://doi.org/10.1111/1753-6405.12603)
labels the comparison group NZ European/Other. Reported means at
wave 3 were 7.09 cigarettes per day for Māori/Pacific and 10.07
for NZ European/Other. The paper reports 67% response at wave 2
and 45% at wave 3 among the 337 who began the study. The reported
14% quitting result is a cohort observation under substantial
follow-up loss. Preserve it separately from the intensity
comparison. No causal or sustained-cessation parameter can be
derived from that percentage alone.

The quitting result does not supply an exact wave-specific numerator
and denominator in the indexed text. As an attrition stress test only,
if 14% referred to the 45% responding at wave 3, the corresponding
baseline-cohort quit proportion would range from 6.3% if every
nonrespondent smoked to 61.3% if every nonrespondent had quit.
These are conditional extremes from rounded figures, not bounds on
the paper's estimand. Require exact follow-up denominators and the
abstinence definition before fitting a transition to this result.

### Independent reduced-nicotine trial comparison

[Donny et al.](https://doi.org/10.1056/NEJMsa1502403) report 14.9
total cigarettes per day at week six in the 0.4 mg/g group versus
21.3 in the 15.8 mg/g control group, a 30.0% relative reduction.
The assigned concentration fell by 97.5%. Across groups assigned
5.2 mg/g or less, 73–81% reported any nonstudy cigarette use during
the trial. This is participant-level occurrence rather than the
fraction of cigarettes consumed from outside the study. Expired
carbon monoxide did not decline in parallel with cigarette counts.
Use the trial as a separate short-term behavioural comparator to
Hatsukami et al. A nicotine concentration ratio cannot stand in
for the delivered dose, total consumption, or disease-risk ratio.

The [Donny et al. full report](https://www.nejm.org/doi/full/10.1056/NEJMsa1502403)
distinguishes three adherence summaries. Any nonstudy use was
reported by 57% in the 15.8 mg/g control and 73–81% in the lower
groups at 5.2 mg/g or less. Nonstudy cigarettes were smoked on 15%
versus 24–35% of days, respectively. The median count on days
with such use was two versus three or four. Multiplying those day
fractions by the conditional medians would not recover mean daily
nonstudy counts. Figure 1 reports adjusted total and study-cigarette
means separately, which offers a route to an approximate week-six
share after checking common analysis denominators and precision.
The reported adherence summaries alone cannot calibrate a quantity
share for the delivered-dose mixture.

The retained full-text PDF (SHA-256
`9b5de22c282c0fdbe318a19bc3333ed1e954508d51f6a4a4ff42411d634f896d`)
confirms that Figure 1A includes both study and nonstudy cigarettes
and Figure 1B shows study cigarettes. Both panels adjust for baseline
cigarettes per day. Figure 2 instead reports urinary biomarkers.
The week-six study-cigarette means are plotted without numeric point
labels in the main report. A subtraction of digitised points would
be approximate and would lack a joint uncertainty estimate.

Visual readback of Figure 1B on printed page 1345 places the
0.4 mg/g standard-tar marker near 13.4 study cigarettes per day
at week six. Subtracting this from the reported 14.9 total gives
roughly 1.5 nonstudy cigarettes per day, about 10% of the adjusted
total. This is a graphical sensitivity anchor, with uncertainty
from reading the marker and comparing separately adjusted means.
It is neither the mean of individual shares nor a tobacco-mass
share. The nonstudy cigarettes' nicotine content and delivery
are also needed to use it in a dose calculation.

A replay through the dose mixture assumed equal tobacco mass per
cigarette, equal delivery efficiency and nonstudy concentration of
15.8 mg/g. With a 1.5-of-14.9 nonstudy count, nonstudy cigarettes
contributed 81.6% of the resulting nicotine-content proxy. The
daily proxy was 8.63% of a 21.3-cigarette control at 15.8 mg/g,
versus 1.77% if all 14.9 cigarettes had contained 0.4 mg/g.
This verifies how the mixture responds to a small higher-content
share under the stated assumptions. It does not recover delivered
dose or validate against the trial biomarker measurements.

Figure 2A on printed page 1346 gives approximate week-six
creatinine-adjusted urinary total nicotine equivalents of 14 and
32 nmol/mg for the 0.4 and 15.8 mg/g groups, respectively, by
visual readback. The resulting geometric-mean ratio is about
44%, compared with 8.63% for the constructed content proxy.
The biomarker and proxy use different aggregation and measures.
The difference shows why the content replay cannot validate
delivered nicotine. It does not identify a compensation
multiplier. A quantitative fit needs aligned exposure and
biomarker records and an explicit observation model.

### New Zealand tobacco interception observation

The [Customs 2024 annual report, Figure 8](https://www.customs.govt.nz/media/3u4ne0om/customs-annual-report-2024.pdf)
reports 17,688 kg intercepted in 2021/22, 12,441 kg in 2022/23 and
10,095 kg in 2023/24. The last count is 57.1% of the 2021/22
count. In the P3 observation equation, attempted flow times effective
monitoring and detection yields interceptions. A constant detection
product would imply a 42.9% decline in attempted flow. An unchanged
attempted flow would instead require the detection product to fall to
57.1% of its earlier value. The aggregate series alone cannot choose
between these explanations. Customs reports enhanced capacity after
Budget 2022, while its [2025 report](https://www.customs.govt.nz/media/squnnrax/new-zealand-customs-service-annual-report-2025.pdf)
describes the difficulty of quantifying the market. Keep inspections,
targeting changes and domestic seizures separate when qualifying
the observation process.

The [2012–2023 consumption-gap study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12410603/)
estimates consumption from survey inputs and subtracts legal sales.
Its reported gap was 12.81% in 2019 and −2.62% in 2021. The negative
value indicates a measurement or coverage discrepancy rather than
negative illicit consumption. The calculation uses a 1.23
under-reporting uplift and the upper confidence limit for daily
smoking prevalence in its scenario. Treat the gap as a derived
observation that shares dependencies with NZHS and legal sales.
It cannot independently update a model already using those inputs.
The [border-closure discarded pack survey](https://pubmed.ncbi.nlm.nih.gov/36028304/)
provides a separate pack-based observation. Pack classification and
sampling differ from both the consumption gap and intercepted mass.
The three observation types cannot be pooled as estimates of the
same flow without explicit coverage and measurement models.

The [Ministry of Health baseline report, page 19](https://www.health.govt.nz/system/files/2023-10/report-on-illicit-tobacco-trade-baseline-report-oct23.v3.pdf)
reports a population-adjusted 7.2% classified illicit pack share
in its sampled urban centres and cites 5.4% in the border-closure
study. The report explains that foreign packaging alone does not
separate legal personal imports from smuggled tobacco. Disposal
and collection vary geographically, and roll-your-own packaging
may be less likely to enter street litter. Use the reported values
as pack-observation comparators with their sampling windows.
Population adjustment alone does not make them estimates of national
illicit consumption by weight or a measure of border detection.

A pack-selection sensitivity assumes perfect classification and
lets r be the relative probability that an illicit rather than a
legal pack enters the litter sample. If s is the observed illicit
share, the implied share among packs before selection is
`s / (r * (1 - s) + s)`. For the reported 7.2%, assumed ratios of
0.5, 1 and 2 yield 13.43%, 7.20% and 3.73%. Reapplying the
selection equation reproduces 7.2% in each scenario. These ratios
are illustrative and the results are pack shares. Estimation still
requires evidence on litter selection and classification, and any
conversion to tobacco weight would need separate product data.

The forward pack-observation model reproduces a 7.2% flagged
share under multiple selection and classification assumptions.
With equal sampling, 90% sensitivity and 99% specificity, the
implied pre-selection share is 6.97%. At the same sensitivity
and 95% specificity it is 2.59%. Allowing illicit packs to be
half to twice as likely to enter the sample gives 3.61–13.03%
in the first scenario and 1.31–5.05% in the second. These are
illustrative scenarios and do not bound the national market.
They show why independent classification checks are required
even when the flagged share itself is measured precisely.

The [Customs 2025 annual report](https://www.customs.govt.nz/media/squnnrax/new-zealand-customs-service-annual-report-2025.pdf)
reports an all-goods result rate among physically examined import
trade entries of 7.9% in 2023/24 and 9.4% in 2024/25 (OC1.08).
For selected mail examinations, the result rate fell from 49.5%
to 32.8% while the number examined increased from 9,608 to
11,627 (OC1.05–06). These are yields among selected inspections,
with risk-based selection. They are not probabilities of finding
tobacco among all illicit consignments. The same report describes
44 tobacco seizures associated with supply-chain referrals, with
more than 1.1 million cigarettes and over 87 kg loose tobacco.
Keep the referral subset and product units separate from total
interceptions. Tobacco-specific selection and detection remain
unidentified.

### New Zealand enforcement fiscal inputs

[Vote Customs, Budget 2025](https://budget.govt.nz/budget/pdfs/estimates/v3/est25-v3-cust.pdf)
lists the Addressing Tobacco Smuggling initiative under Revenue
Collection and Other Services, with NZD 2.132 million for 2024/25
and 3.272 million for 2025/26 in the policy-initiative table.
[Budget 2026](https://budget.govt.nz/budget/pdfs/estimates/v3/est26-v3-cust.pdf)
retains 3.272 million as the final budgeted amount for 2025/26.
Use these as fiscal benchmarks for the named initiative. Actual
resource use needs attributable expenditure and allocation across
activities. The separate tobacco debt write-off in the 2025 annual
report belongs in the fiscal account. It cannot be added as an
enforcement resource cost or used to infer marginal cost per seizure.

The [Customs 2025 annual report, page 105](https://www.customs.govt.nz/media/squnnrax/new-zealand-customs-service-annual-report-2025.pdf)
reports NZD 34.972 million in actual 2024/25 expenses excluding
remeasurements for the full Revenue and Other Services category.
The revised budget was NZD 36.674 million. The category combines
revenue collection with other services. Its NZD 1.702 million
underspend cannot be allocated to the tobacco initiative from
these accounts. The same report's NZD 17.7 million associated
with intercepted tobacco is described as foregone revenue, a
separate measure from collections, write-offs and resource use.
No tobacco-specific actual expense was found in this statement.

### Birth-cohort restriction implementation comparison

New Zealand's [2024 amendment Act](https://www.legislation.govt.nz/act/public/2024/6/en/latest/sections/LMS939068/)
repealed the 2022 provisions for the cohort born on or after
1 January 2009 before they took effect. Retain that rule only for
a historical counterfactual. The [Maldives Ministry of Health](https://health.gov.mv/storage/uploads/kobg5Xw8/c6vxsq6f.pdf)
confirmed commencement on 1 November 2025 for people born on or
after 1 January 2007. Its rule includes use and purchase as well
as sale, covers all forms of tobacco and operates alongside a
vaping ban. Use it as an implementation and eligibility comparator.
The scope differences preclude treating it as direct validation of
the proposed New Zealand smoked-tobacco sales rule. A matched
post-implementation initiation and substitution series was not
identified in the sources checked.

A nine-case boundary replay crosses birth dates 31 December 2006,
1 January 2007 and 2 January 2007 with observation dates 31 October,
1 November and 2 November 2025. The Maldives rule is inactive in
all three pre-commencement cases. From commencement onward, both
birth dates at or after the cutoff are covered and the earlier date
is outside the cohort rule. This verifies the existing inclusive
date predicate against the published commencement and cutoff. It
does not verify other age restrictions, enforcement or behavioural
effects.

[Brookline's sales rule](https://www.brooklinema.gov/3849/Tobacco-E-Cigarette-Product-Sales)
covers tobacco and e-cigarette sales to people born on or after
1 January 2000 within the town. The town also stopped issuing new
tobacco establishment permits. A local evaluation would need to
separate the sales cutoff from permit changes and track purchases
outside town. This is a geographic displacement comparator rather
than a direct analogue of a nationwide rule. The screened sources
did not establish an observed initiation effect for the bylaw.
California's [Tobacco 21 evaluation](https://pubmed.ncbi.nlm.nih.gov/29440328/)
reports a 14.2% tobacco retailer violation rate for decoys aged
18–19 (95% CI 9.3–19.1%). That is an observed compliance endpoint
under a different age rule and cannot serve as a cohort-specific
initiation reduction.

### Shared evidence admission recheck

The bounded source-handoff command at `7f748fb` again reported
28 blocked rows, a proposed target scope and no scientific
qualification or conditioning. This uses the maintained proposal
and bindings. The newer P3 comparison evidence has not been
added as observations to those inputs. The report SHA-256 is
`dcc6f3485f2cacae1c2b168a3db3c07e0fcdae1c146939ab3b34af98022cba83`.

### Recovered shared-evidence captures

The raw-object replay verified both source byte pairs: the national
sales workbook and its WARC, and the consumption-gap article HTML
and its WARC. All 28 rows cleared capture-byte verification. The
16 workbook rows also cleared the source-value reconciliation
check. The 12 article rows remain derived summaries. The exact
WARC records identify the source URIs and record IDs but lack
`WARC-Date` headers. The replay therefore leaves capture dates
unverified, with all 28 rows still blocked and no conditioning.
Its report SHA-256 is
`4128958407e7b3e79a22f68c6632967398655a905aa473b87b16f7ac49d78c04`.

The P2 context receipt binds a separate publisher download of
the same workbook digest to a browser completion observed by
2026-11-07T03:01:27.798153Z. This dates that acquisition only.
The archive's native source references leave both recovered
WARC timestamps null. A replacement capture would need its own
dated response record and binding to the workbook digest before
it could clear the date check. Do not apply the later download
timestamp to the recovered WARC.

A fresh publisher acquisition with GNU Wget 1.25.0 produced a
dated response WARC at 2026-11-08T11:21:56Z, record
`urn:uuid:0F6C3CE9-9BC0-49F4-860C-70138A24347C`. The decoded
HTTP 200 response body matched the retained workbook digest
`3a55a6469097ebc3fb27a6143db7749e5b885761ada76b197053dfe76f36e883`.
The new WARC digest is
`68ace480ab097e2a72360e12bb6eef59e4e38ca19a62530fd28d1649de04e6ab`.
This dates the new response. The maintained binding still
requires owner reconciliation before the audit can use it.

A fresh dated HTTP 200 capture of PMC12410603 at
2026-11-08T11:22:29Z has HTML SHA-256
`eb1ea28cf5fd1a6e074862d28612c9d3e6258e9ae1521edb2be6e0b689839700`
and WARC SHA-256
`4f35cab7bf041aa6c1b2f07479b6439d01eff962681813ebdca64603aff07911`.
The fresh and retained HTML are both 194,823 bytes, with 90
byte positions differing. All five table fragments match byte
for byte. Retain this as a separate capture of the same table
content and keep the older capture date unknown. The matching
tables do not change the derived-summary role of the 12 rows.

The dated article's Table 2 was reconciled against
`data/empirical_intake_20261024/nz_historical_legal_supply.csv`.
All 60 numeric fields checked across 2012–2023 matched exactly
after normalising thin-space separators and Unicode minus signs.
All 12 upper-scenario signed gaps equal estimated consumption
minus legal sales. This verifies the transcription, including
negative gaps. It leaves the summary's role and dependencies
intact. The maintained audit's source-value status currently
recognises reconciled workbooks rather than this HTML check.

The upper-scenario percentages reproduce for all 12 years as
100 times the signed gap divided by upper-scenario consumption.
The published lower endpoints do not follow one denominator.
For example, 2012's −5.02% matches the gap divided by legal sales,
whereas 2023's −29.63% matches the gap divided by lower-scenario
consumption. In 2021 the published −15.98% matches neither
(−19.25% or −16.14%, respectively). Keep the original lower
percentages as printed evidence and quarantine them from
quantitative calibration until the convention is reconciled.
The absolute upper-scenario values remain exactly transcribed.

Holding the upper smoker-count scenario and legal sales fixed,
the zero-gap under-reporting uplift is 1.23 times legal sales
divided by reported upper-scenario consumption. It ranges from
1.0724 in 2019 to 1.2898 in 2023. At an illustrative uplift of
1.10, only 2019 and 2022 have positive gaps. At 1.30 all years
have positive gaps, compared with ten at the source's 1.23.
The sign is therefore sensitive to survey scaling even before
changes in product coverage or stock timing. These thresholds
do not estimate the correct uplift or true illicit consumption.

Across the 12 overlapping calendar years, dividing the published
national release mass by the study's legal cigarette equivalents
gives apparent ratios from 0.690 g per equivalent in 2015 to
0.803 in 2022. The 2023 ratio is 0.765. These ratios diagnose
differences between the two series. They combine product mix,
return scope and conversion conventions, and cannot estimate
factory-made stick weight. The P2 scope receipt verifies separate
domestic and duty-free cigarette counts for one manufacturer
in 2025. Its loose-tobacco year remains quarantined, and the
market-type workbook does not establish a mass or count basis.
A national bridge needs compatible product-level totals.

A separate [publisher-listed 2024 BAT loose-tobacco return](https://www.health.govt.nz/system/files/2025-06/BATNZ-2024CigaretteTobaccoAnnualReturn_0.pdf)
was recovered. Its heading agrees with its 2024 listing, and its
product rows and quantities differ from the 2025-listed PDF with
a 2024 heading. The new capture SHA-256 is
`93b26f018ef37ae221a524585322328e40eb2ad47623b4d5e24ba569b9249ff0`.
The comparison establishes that the disputed PDF is a different
return, but does not establish whether it is a 2025 return or
a revision to 2024. Retain the disputed year quarantine.

The [consumption-gap study's methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC12410603/)
confirm that 0.7 g is used to convert loose tobacco into RYO
equivalents, after adding domestic and duty-free loose tobacco.
Factory-made cigarettes enter as counts. The study uses published
rounded totals for 2012–2016 and reconstructs 2017–2023 from
company returns. It does not supply the Ministry workbook's
factory-made mass convention. As a diagnostic only, imposing
identical coverage and using RYO shares of 27–32% would require
about 0.841–0.851 g per factory-made stick to reconcile the 2022
totals. This is a conditional residual, not a measured weight.
The source-basis change also needs explicit treatment in any
historical comparison.

### Reported-release temporal baseline

A retrospective split fits a straight line to the Ministry's
2010–2019 reported release tonnage and scores 2020–2025 without
refitting. The fitted decline is 78.01 tonnes per year. Mean
absolute error is 111.65 tonnes, compared with 345.50 for a
constant 2019 level. The trend predicts 1,036.47 tonnes in 2025
against 755 reported, an overshoot of 281.47 tonnes. The split
was selected after the series was available, so it is a descriptive
temporal benchmark rather than a preregistered validation. Compare
future predictions on the original release unit and scope.

For a one-year-ahead comparator, refit the linear trend at each
origin using all available years from 2010 up to the prior year.
Compare with carrying forward the most recent observed level.
Across 2020–2025 the trend's mean absolute error is 103.27 tonnes
versus 122.83 for persistence. Each wins in three years. In 2025
the trend misses by 218.85 tonnes versus 213.00 for persistence.
This scores a different forecast task from the frozen pre-2020
trend and reduces its apparent advantage. Retain both forecast
origins when specifying what a P3 model is asked to predict.

The four release benchmarks are retained as six scored rows in
`nz-reported-release-forecast-benchmarks.csv` (SHA-256
`e4f6f2e66c0b6a318f0829586564bd519d358f5cd7a610fe0c7a49c63e1938f0`).
The receipt recomputes ordinary least squares with rational
arithmetic before decimal display and retains separate forecast
origins. It is staged with the Ministry workbook and attribution.

The seven task-card test files passed at
`3c08493c14877be8d3ea7e12c9d5a1cbae546ba4` on repo-local
Python 3.15.2 with `PYTHONPATH=src`. The bounded run recorded
177 passed in 7.57 seconds and 213.0 MiB peak sampled group RSS.
This covers the selected evidence, retail, sensitivity, regulation,
source handoff, publication boundary and workstream integration
tests. The earlier complete-suite lineage rejection remains a
separate gate.

## Combined native admission — 8 November 2026

The combined P3 source at cebc786 reopened all eight runner attempts and
matched all 82 scientific CSVs across 140 outputs against Phase 0. The new
signed acceptance authenticates the combined inventory and its source pins.
See integration/archive/scientific-lineage-checkpoint_empirical_p3_20261108.json.
The native scope covers runner inputs, execution and output bytes. Empirical
policy, health and equity acceptance retain the existing prerequisites.
