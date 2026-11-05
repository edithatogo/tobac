# Scientific adequacy review — 5 November 2026

Scope: bounded internal review of the active regulatory, retail, longitudinal and M3 contracts and selected model calculations at `05703849716372c4f2ecf09de402539ba43a54ad` (scientific source inherits published `7d24f608803e73cfc910bc766d7e8fcf444d741e`). This is not independent peer review, a line-by-line audit of every output or a validation against new field data. The bounded context receipt and independent arithmetic results are retained in the local audit outputs; the deterministic arithmetic seed was 20261105.

## Overall judgement

Appropriate for explicitly conditional, finite-state sensitivity and methods demonstrations; not adequate to claim a current population posterior, causal cap effect, real policy choice, monetary value or funded-study recommendation. Numerical reproducibility and algebraic coherence do not establish source validity, calibration or field performance. No claim of universal adequacy is made.

## Inputs and observations

The matched pathway record and research gates report zero available matched cells out of eight, and no raw current paired NZ assays. Historical survey-reported-to-recorded-lawful-supply ratios are working reconstructions from source intervals, with source uplift removed before fitting; geometric midpoints are not reported individual observations. Recorded releases are not total consumption and stock, visitors, legal unrecorded supply, product units and period alignment need substantiation. Context and source publication reviewed; the current data inventory and each original row were not independently recaptured in this pass.

## Current public-source check

The [Ministry of Health's 2025 tobacco sales-return announcement](https://www.health.govt.nz/news/2025-tobacco-sales-returns-published) reports the annual distributor-sales series for 2025. The [Health and Independence Report 2025](https://www.health.govt.nz/publications/health-and-independence-report-2025-online-version) reports 2024/25 daily smoking prevalence for adults aged 15 years and over. These are useful, public context with different units, periods and denominators. Neither alone is a matched, catchment-specific total-consumption and lawful-supply observation, an assay calibration, or an identified policy contrast. They are not newly conditioned into the model. Retain the existing public-only and source-applicability requirements before drawing stronger conclusions.

## Parameters, ranges and distributions

The M1 support uses two values per axis and analyst-specified probabilities; these are planning supports, not population distributions or confidence limits. Biomarker yield spread, 0.35/0.20/0.10 log SDs, cutpoints, classification accuracy, causal-study performance, stocks, visitor sensitivity and common-error assumptions are not field-calibrated. Equal axis weights and stipulated dependence grids constrain the scenario space and do not prove global robustness. Retail beta(23.4,97.2) is a published simulation input, not observed NZ cap efficacy. Independent calculation gives mean 0.19402985 and central 95% interval [0.12878861, 0.26887295], consistent with the cited source's rounded values. Midpoint quantile means at 2, 4, 8, 16 nodes are 0.19311137, 0.19354822, 0.19378199, 0.19390369; closeness of this single moment does not demonstrate convergence of decisions or all outputs.

The source's ~300-outlet/95% restriction also assumed reduced e-cigarette supply, whereas this model's ~600 smoked-retailer contrast holds vaping access constant. Applying the source-shaped net-cessation input as a fractional consumption response additionally needs the declared equal-intensity and estimand transport assumptions. Null/attenuation scenarios expose, but do not validate or exhaust, those differences. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC11672025/ and https://tobaccocontrol.bmj.com/content/tobaccocontrol/33/e2/e173.full.pdf?with-ds=yes .

`evidence/m2/publication_20261028/parameter_provenance.csv` is a bounded M2 publication table, not a universal configuration catalogue: it lists 11 of the 12 base regulatory axes, omitting the M1 `restriction` axis that the retail model replaces, and does not enumerate the full set of constants and measurement settings. Use the active configuration and contracts for complete interpretation; do not represent this CSV alone as a complete all-model provenance audit. `retail_channels` also declares a 0.2 lawful-comparison log SD and cutpoints directly in code; they are hypothetical study-performance inputs, not field measurements.

## Models and calculations

Independent seeded arithmetic generated 10,000 valid synthetic physical states. Comparing separate algebra against `retail_components` gave maximum absolute residuals below 5e-13 for pre-mitigation total, mitigation/replacement total, and lawful-plus-illicit accounting. This checks algebra under those assumptions; it does not show that the behavioural process, equal-intensity assumption or absence of other behavioural pathways holds in practice. The longitudinal Gaussian random-walk mixture is a conditional statistical model, not a causal or illegal-market identifier; summary interval reconstruction, finite process grid, innovation and common-error assumptions need sensitivity and data support. The M3 finite portfolio evaluates a selected design set, conditional independence or declared joint tensors, fixed-horizon timing and illustrative normalised costs; it does not establish an optimal real procurement, dynamic deployment, QALYs or money value.

## Choices, outputs and outcomes

Crime/resource weights and uptake profiles are analyst scenarios, not public/Māori preference distributions or observed implementation. Robustness challenges include null, dependence and value changes but do not cover every defensible prior, distribution, structure or metric. The 82-table eight-runner and publication replay evidence establishes reproduction to declared tolerances, not agreement with real outcomes. The 163 focused local tests cover retail, supply, value sensitivity, robustness, partial identification, matched pathway, M3 and workstream integration; they do not validate all inputs or a scientific conclusion. The 2026-11-03 two-platform receipt is `integration/scientific_reproduction_20261103.json`.

## Remaining next actions

1. Reconcile the policy/estimand differences and assess source transport and equal-intensity mapping before interpreting the beta-derived scenarios as a real intervention effect.
2. Establish target-specific matched consumption/lawful-supply data, covariance, physical conversions, assay calibration, counterfactual and held-out field validation within existing rights and public-only constraints.
3. Evaluate sensitivity to alternative continuous/discrete priors, measurement assumptions, dependence and structural model choices; document actual costs and governance/value choices rather than inferring them.
4. Audit the complete parameter-to-output inventory, including hard-coded likelihood constants and each source's applicability. Obtain applicable human and scientific review before any substantive policy or field-validity claim.
