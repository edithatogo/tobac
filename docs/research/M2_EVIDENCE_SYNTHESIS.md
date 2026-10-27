# M2 evidence synthesis and partial identification

27 October 2026. This targeted primary-source synthesis and conditional identified-set
analysis advances issue #3. It supplies no fitted current NZ posterior or regulatory
recommendation. The source ledger is `evidence/m2/synthesis_20261027.json`; access,
extraction locators, numerical estimands and dependence groups are recorded there.
Rendered/indexed source review is distinguished from retained byte-verified objects.
This is not a systematic review or proof that no other evidence exists.

## What existing evidence resolves

| Evidence | Supported use | Transport or identification limit |
| --- | --- | --- |
| DUTCH_RETAIL_2026: [primary abstract](https://pubmed.ncbi.nlm.nih.gov/41748428/) | Observed supermarket compliance and changes in nearby outlets after an implemented policy | Retail counts/access are different endpoints; neither identifies adult NZ quitting, total consumption or illicit diversion. |
| CVS_PURCHASE_2017: [primary abstract](https://pubmed.ncbi.nlm.nih.gov/28207340/) | Controlled interrupted-time-series purchasing evidence | Purchasing is not smoking cessation or origin; nonrandom exposure, retailer-affiliated authors and transport matter. |
| CVS_BEHAVIOUR_2020: [primary abstract](https://pubmed.ncbi.nlm.nih.gov/31761514/) | Difference-in-differences quit-attempt evidence, with null daily/nondaily endpoint | Attempts are not successful net cessation; shares the CVS policy with the purchase study, not an independent policy replication. |
| HUNGARY_YOUTH_2024: [primary study](https://tobaccocontrol.bmj.com/content/34/4/430) | Observed licensing, youth access and smoking trends | Single-country pre/post design, concurrent measures, population/horizon and compensatory access prevent a direct adult NZ causal effect. |
| NZ_WASTEWATER_2025: [primary study](https://doi.org/10.1016/j.scitotenv.2025.181223) | Reported analytical performance, analytes, quantification/censoring and coverage limitations | Instrument/method concentration cannot silently become raw wastewater concentration or tobacco volume. Mixed-product contributions and yield remain relevant. |
| ANABASINE_YIELD_2026: [primary study](https://doi.org/10.1093/ntr/ntag042) | Preliminary human excretion evidence; literature gap is narrower than 'no yield evidence' | Selected cigarette-user subset; inherited metabolite/machine calibration; observed range is not population coverage or a confidence interval. Vaping contribution is unresolved. |
| NZ_RETURNS_2025 and NZHS_202425 | Native-unit reporting and existing historical reference data | Products, channels, stock, visitors, resident exposure/intensity and observation windows do not match automatically. |
| NZ_CUSTOMS_CASE_2025 and AU_CRIME_INQUIRY_2026 | Offence occurrence and contextual harm mechanisms | Cases, testimony, market turnover, profits and seizures are not incremental NZ harm under the cap. The Australian inquiry is limited indexed discovery, not a quantitative causal extraction. |
| NZ_ACTIONPLAN_RIS_2021: [primary RIS](https://www.health.govt.nz/system/files/2021-12/ris-smokefree-aotearoa-action-plan-mar24.pdf) | Historical package-wide regulator/enforcement cost benchmark | Not current600-cap or study costs; total monetised costs were not calculated and further implementation costing was explicitly required. |
| NZ_BASELINE_REPORT_2022: [primary report](https://www.health.govt.nz/system/files/2023-10/report-on-illicit-tobacco-trade-baseline-report-oct23.v3.pdf) | Reproduce consumption-gap arithmetic and challenge its fixed uplift | Shares MOH/NZHS inputs with the later Phyo summary; not another independent illicit observation or a causal contrast. |
| NZ_CUSTOMS_BUDGET_2025 | Identify an existing public cost source and its scope | Whole-agency appropriations and excise losses are not target-specific incremental resource costs. No monetary coefficient is imported. |

The source ledger records the verified numerical extracts. No pooled effect, foreign
point estimate or confidence interval becomes an NZ observation or prior. The original
SHINE source-shaped M2 scenario, its null/attenuated transport and alternative mechanisms
remain unchanged. A published estimate and an elicited judgment have different provenance;
none of these sources is a completed elicitation for the new decision.

## Analytical measurement specification

For a final-extract threshold, a raw-wastewater equivalent would require compatible
sample/final-extract volumes, dilution, recovery and matrix/calibration definitions.
Symbolically, where the method definitions justify it:

    C_raw = C_extract * V_extract / (V_raw * recovery)

No source-independent numeric multiplier is assigned. Extraction recovery, biological
excretion and product absorption are separate stages. A high calibration R-squared
is not near-limit accuracy. Preserve below-quantification observations as censored
raw-scale information; do not replace them with zero, LOQ/2 or a precise volume.

Anabasine in vaping/non-use groups cannot be set to zero merely because group
comparisons are not statistically significant. The new human yield estimate is a
percentage of estimated absorbed anabasine, not a universal mass-per-cigarette factor.
The assumed nicotine-metabolite excretion and machine-derived absorption are shared
calibration inputs. They must not become independent likelihood factors when the same
underlying experiments are reused. Repeated samples can reduce random error without
removing shared yield/reporting bias.

These relationships specify a joint model and sensitivity dimensions. Fitting its
censoring, covariance, target-product mixture and transport requires suitable raw
records. Such records may already exist; their absence from this repository does not
establish that a new sampling campaign is necessary.

## Existing lawful-release evidence, without invented conversion

The runner recomputes audited subset totals from the hash-bound reconciliation rows.
Factory-made counts remain sticks, RYO remains tonnes, and channels retain their
original declarations. The R&S table/note are mutually exclusive interpretations of
one quantity, never two additive observations. The BAT document year produces a
separate conditional cohort case; a filename is not permission to relabel 2024 as2025.
Both conflicts are therefore usable as alternatives without pretending they are resolved.

A fresh rendered review of the [currently linked BAT PDF](https://www.health.govt.nz/system/files/2026-08/BAT-Sales-RYO-2025.pdf) still shows2024 in its heading. This is fresh source-text verification, not a new raw-byte capture.

The generated report includes the R&S interpretation width and the BAT-year case.
These are reported-subset comparisons, not national bounds or probabilities over
interpretations. Unknown reporting/channel coverage prevents a justified finite
national upper bound; inventory/visitor/border adjustments prevent resident-consumption
identification. The national lower bound and cigarette-equivalent total remain null
because national comparability itself is not established. No divided-by0.7 conversion
or subtraction from the755-tonne mass comparator is performed.

`accounting_bounds` reuses the algebra of `tobac.supply.expected_releases`:

    lawful = releases / reporting_bias - stock - outbound - wastage + lawful_unrecorded

Its inputs are explicit intervals in a qualified common Scope/product/unit. Stock is
signed, unrecorded is an absolute amount, and no component silently defaults to zero.
Cartesian projection preserves a negative accounting residual as a discrepancy.
It is not automatically a physical illicit-consumption interval. A justified joint
error set may narrow the projection; prose independence does not establish such a set.

## Historical source arithmetic and uplift sensitivity

The baseline2022 report's Table3 supplies a reported pre-uplift consumption total,
lawful release total and fixed underreporting uplift. The runner verifies the exact
published gap arithmetic with Decimal and reproduces a signed gap over the analyst
stress support uplift[1,1.3]. This support is not an empirical confidence interval.
It reports the zero-gap uplift threshold: below it the observed discrepancy is negative.
That is a source/accounting challenge, not evidence of negative illicit consumption.
No forecast/posterior or derived gap is bought as another observation; all original
MOH/NZHS dependencies, survey/calendar/product conventions and source-to-target
transport remain explicit. Published numerical inputs and calculated outputs are
retained in the ledger/receipt rather than rounded into a new market-size claim.

## Partial-identification contract and proof

For restriction alone, before mitigation/replacement, retain M2a's equal-intensity
structure. Let q be mapped additional net cessation, d lawful-to-illicit switching,
a the true total-consumption causal ratio and b the true lawful-consumption ratio:

    a = 1-q; b = (1-q)*(1-d); 0 <= q,d <= 1; 0 <= b <= a <= 1
    R_total = bias_total * a; R_lawful = bias_lawful * b

This excludes consumption increases and extra mechanisms. An incompatible observation
set is reported empty under this structure, not repaired by clipping data or calling
the structure empirically true. Each observed ratio and each strictly positive bias
has an explicitly declared interval. No measurement is represented by `None`, not zero.
The division and structural-support intersection give a in[A,B] and b in[C,D].

Feasibility requires C<=B. Put M=max(A,C). The sharp marginal support is:

    q in[1-B, 1-M]
    d in[1-min(1,D/M), 1-C/B] when M>0

If M=0, a=b=0 is feasible: q=1 and d is irrelevant/unidentified, so its marginal
support remains[0,1]. Every endpoint has a feasible witness; an independent SciPy
linear-programming oracle checks the nonzero case using x=1/a,y=b/a and linear
constraints C*x<=y<=D*x,0<=y<=1. Grid samples independently check containment.
These are sharp marginal projections of the declared Cartesian inputs. Their cross
product is not the joint identified set: q,d remain coupled by the two equations.
Correlated support restrictions can narrow the set; no independence probabilities,
confidence coverage or posterior is assigned.

A missing matched pair leaves the structural supports unrestricted. Total information
alone cannot identify d. Matched information can narrow d only when reporting/transport
are bounded; wider calibration supports widen identification. Shared multiplicative
calibration would cancel in R_lawful/R_total only if the same factor actually applies.
Unknown differential bias does not cancel. Non-tobacco contributions or mitigation
require another explicit structure, not mechanical substitution into this one.

All nonmissing numerical ratios in the scenario manifest are labelled synthetic
assumption demonstrations. No reviewed policy study supplies matched NZ ratios.
The no-data result is a structural identified set, not a uniform prior on[0,1].

## Conditional VOI and historical prediction

The existing Nox reproduction runs M1, M2 and M3 and verifies their outputs before
this synthesis reads them. M2 EVPI/grouped EVPPI precede study EVSI as before; no groups
are added. The synthesis verifies original input/output hashes and complete unique
configured scenario/design tables. It reports ranges of gross study-cost ceilings
from existing EVSI in normalised decision units. These are conditional on the existing
finite priors, causal/reporting structures and adoption assumptions; no probabilities
across scenarios are invented. They are not costed ENBS, NZD or a new study optimisation.
Incremental same-unit study cost must be below the applicable gross EVSI ceiling for
positive net value; real cost/value calibration is still needed to use that condition.

Historical release prediction is already computable from existing data. The synthesis
checks that every rolling-origin fit stops before its test year and reports actual
reserved diagnostic coverage with its denominator. This is single-vintage retrospective
national-release prediction. It is not real-time source-vintage validation, raw-assay
prediction or held-out evidence about a policy that was not implemented. No such
field acceptance is inferred from successful software execution or historical fit.

## Residual requirements

The machine-readable residual register in the source ledger distinguishes:

- human selection of a legally feasible contrast/timing/target and defensible comparator;
- access to existing matched raw laboratory, survey, supply/stock/border and population records;
- source-owner correction/clarification only where carrying alternatives is insufficient;
- new measurement/validation only if existing records cannot support the selected target;
- suitable causal response/mitigation/incremental-harm and held-out outcome data;
- target-specific incremental resource costs and adoption/timing information;
- Māori governance, permissible use, privacy/equity constraints and normative trade-offs.

Expert elicitation may support a conditional analysis where observational identification
is unavailable, but human expert responses are new information and do not establish
empirical causal validity or operational permission.

These are data or substantive decisions. Literature access limitations are recorded
as review scope, not mislabeled as requirements for a new field study. Optional
continuous/library expansion is not required for this exact finite analysis. No
external contact, data-access application, field deployment or governance decision
is made by this work. Issue#3 remains open for actual empirical acceptance.

## Reproduction

Nox `reproduce` writes `m2-synthesis.json` into its fresh replay directory after all
original model/longitudinal checks. The standalone entry point uses the qualified
repo-local Python3.15.1 environment and refuses an existing receipt:

```sh
.nox/tests/bin/python scripts/qualify_m2_synthesis.py --replay outputs/engineering/replays/EXISTING --out outputs/engineering/NEW-synthesis.json
```

Each report binds the source ledger, source-dependent files, code, replay artifacts,
checkout identity and actual command. `target_empirically_identified=false` and
`conditioned=false` are retained. Archived previous reports and source bytes remain
unchanged; successful execution establishes the stated computational evidence only.
