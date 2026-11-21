# M2a: a specified retail-policy contrast

Date: 24 October 2026. Status: source-informed structural analysis, not an adopted NZ policy, measured causal effect, fitted current posterior or funding recommendation.

## Decision and scope
The proposed primary contrast is a prospective licensing cap of at most 600 **smoked-tobacco** retailers against otherwise unchanged reference retail availability. Treat the first full year after implementation as the comparison period; no implementation date or current outlet count is asserted. Nicotine-content restrictions, generational sales restrictions, excise changes and vaping access are held constant. Accompanying support/enforcement and expanded cessation remain separately defined alternatives. Existing M1 actions and normative consequences are retained for comparison, not represented as measured NZ costs or QALYs.

The cap is a real historical policy design, not an implemented natural experiment. The Ministry's June 2023 announcement specified at most 600 retailers and a planned 1 July 2024 start. Its March 2024 notice records suspension and repeal. Do not code a national 2024 outlet-reduction treatment effect from that announcement. See `evidence/m2/source_review.json`.

## Source parameter is not the same estimand
Ait Ouakrim et al., DOI 10.1136/tc-2022-057655, Table 2, used Beta(23.4,97.2) for a one-off **additional net cessation** input for roughly 300 outlets / 95% reduction. The mean is approximately 19.4%; reported uncertainty interval 12.9–26.9%. This combines a previous model and stated quitting intentions, not observed post-policy effectiveness. Its prevalence-to-consumption mapping, outlet count, baseline population and timeframe do not match this new case automatically.

M2a uses that shape only as an explicitly transported structural alternative. The configuration compares no effect, attenuated transport and an 80% source-shaped / 20% point-null mixture. Null and transport probabilities are analyst assumptions, not elicited probabilities. Consumption reduction equals net cessation only under an explicit equal-intensity mapping of quitters and continuing smokers. There is no lifetime health extrapolation or direct import of the source paper's HALYs.

The earlier Pearson model (DOI 10.1136/tobaccocontrol-2013-051362) predicts 9.6% versus 9.9% prevalence after a ten-year phase-in. That is a different estimand/horizon, not an independent one-year net-cessation observation. It is retained as a structural warning, not pooled with the Table 2 parameter.

## Accounting and causal assumptions
Let T denote baseline total consumption, I illicit consumption, L=T-I, q additional net cessation and d switching from lawful to illicit tobacco among continuing consumers:

    L_after = L * (1-q) * (1-d)
    I_after = I * (1-q) + L * (1-q) * d

Consequently total consumption after the restriction is T*(1-q); lawful-to-illicit switching is not counted as quitting. Accompanying mitigation removes a fraction m of I_after. A fraction r of that removed quantity is replaced with lawful cigarettes. Compare r=0, 0.5 and 1. Health gains occur only for net consumption removed; legal replacement can reduce illicit activity without reducing smoking. No assumption that every disrupted illicit purchase becomes a quit is hidden in the equations.

This is an alternative to M1's gross lawful-demand displacement mechanism, not a fit correcting M1 or a second estimate to pool. Report the two separately. Incremental criminal-harm coefficients and normative weights remain scenarios including zero; market share, revenue and fiscal loss are not themselves incremental crime harm.

## Information designs
Reuse M1's chemical, calibration, supply and hypothetical causal-study likelihoods. Add a **matched causal total-and-lawful-consumption comparison**, with an explicit differential supply-bias latent factor. It requires an appropriate counterfactual and reconciled supply; a raw release ratio is not such an observation. The report's log-scale SD and cutpoints are assumed performance, not a measured study effect. Conditional independence is only asserted after all shared state variables; that assertion requires field qualification.

A total-consumption contrast can inform q but cannot identify d in this structure. Matched lawful-consumption information can help separate d. Baseline wastewater does not become a causal effect estimate. No dynamic network optimisation or claim of retrospective identification is made.

## Scientific outcomes and numerical method
Use the existing exact finite-state decision and information functions. Report EVPI, grouped EVPPI, study EVSI, targeted information gain, decision changes and parameter learning separately. Normative units are not currency. Quantile quadrature at 2/4/8 source-effect nodes tests one numerical axis only: the other binary supports, source transport, policy mapping and likelihood structures remain uncertain. Exact outcome enumeration does not establish a continuous posterior or empirical validity.

## Qualification still needed
A real comparative design, contemporary baseline availability, population-specific policy response, field assay sensitivity, longitudinal supply/stock data, mitigation substitution, incremental harms and monetary consequences need qualification. Governance and Maori interpretation/permissible-use authority cannot be inferred from a checkbox or chemical signal. No ethnicity or individual criminality is inferred from catchment chemistry. These are open empirical tasks, not reasons to suppress transparent conditional analysis.
