# M1: Regulatory uncertainty before surveillance procurement

## Decision contract
The purposes are (1) supporting NZ decisions about introducing wastewater testing,
(2) demonstrating public-health VOI, and (3) making contested empirical claims
investigable. Success can be a no-study conclusion, a different research priority,
or a non-identification result. It is not predetermined funding or policy support.

The primary question is: which uncertainties about current tobacco consumption,
policy-induced switching and additional criminal harms can change the preferred
regulatory approach? The secondary question is how much of that information a
feasible wastewater/supply/calibration study could supply.

M1 is an exact *conditional screening experiment*, not a fitted NZ posterior,
regulatory impact assessment, approved study, or monetary funding recommendation.
The previous cessation-allocation analysis is retained as a secondary teaching
application in the predecessor archive, not the justification for this milestone.

## Four action archetypes
A0 retains the reference approach. A1 reduces retail availability enough to displace
an uncertain fraction r of lawful cigarette demand. A2 combines A1 with cessation
access and illicit-supply mitigation of uncertain net effectiveness e. A3 expands
cessation access, reducing total smoked consumption by uncertain fraction c.
These are research archetypes, not approved interventions or predictions of the
repealed 2022 package. Retail restriction is not denicotinisation or a generation
ban. Exact instruments, delivery costs and causal effects require empirical work.

Let T be total cigarette-equivalent consumption, i illicit share, L=T(1-i), I=Ti,
and d the fraction of displaced lawful consumption diverted to illicit supply.
A1 gives L1=L(1-r), I1=I+rLd. A2 gives L2=L1, I2=I1(1-e); e is a *net* effect,
not an assumption that seizures necessarily prevent consumption. A3 reduces L and
I by c. The reference has no incremental effect or cost.

Health gain is a normalised exposure consequence, not QALYs. Additional criminal
harm depends on absolute illicit-volume change and an uncertain harm coefficient,
not market share, turnover or excise loss. The zero-diversion and zero-marginal-
criminal-harm hypotheses are retained. Health, criminal, resource and lawful-tax-
base changes are exported separately. A declared crime weight combines only the
first three in normalised decision units. Taxes are never added as resource gains.
This short-run model omits initiation, relapse, cigarette intensity compensation,
market recruitment and many other mechanisms; it is deliberately not a full causal
forecast. These omissions must be addressed before applying monetary projections.

## Evidence and uncertainty
Sources establish historical estimates and measurement relationships, not a
current joint posterior. Twelve binary axes create 4,096 explicit hypotheses.
The yield centre of 0.9 ug/cigarette is source-supported; its two-point spread is
assumed. Current consumption/share, causal response, harm, implementation and
measurement-bias supports are analyst scenarios. They are not elicited or fitted.
The historical NZ 8.4% estimate is not a 2026 observation or a confidence bound.
Nine prior/dependence scenarios and four normative weights are kept separate.
A declared association between current illicit share and future diversion is a
sensitivity assumption; indirect learning through it is not causal identification.

## Primary method and learning targets
The inherited DecisionProblem, EVPI and finite-partition definitions are reused
without body changes. A single new exact finite-outcome evaluator calculates
EVSI, posterior action changes, target-specific mutual information (nats), Brier
risk, and confidence-based resolution. A scalar oracle independently checks it.
Because axes are genuine discrete hypothesis variables, grouped EVPPI is exact
for this finite model. It is not continuous-parameter EVPPI obtained by labelling
PSA draws uniquely. Group EVPPIs are not additive.

Order of analysis: regulatory EVPI -> grouped EVPPI -> scientific learning ->
research-design EVSI -> conditional ENBS. Existing evidence defines D0; it is not
purchased again. When real baseline observations arrive, condition once before
prospective calculation. The reported marginal combined-minus-existing values
are preposterior marginal comparisons, not conditioning on unseen actual results.

Scientific targets separate current illicit share/absolute volume from future
policy diversion and criminal harm. The event of material illicit growth is an
increase of at least 5% of baseline total under A1, not merely a rising share.
A second illustrative event is current illicit consumption >=150 equivalents per
1,000 residents/day. Neither threshold is a recommended enforcement trigger.
Confidence 90% is a declared study-design criterion; information gain is never
converted to money or added to EVSI.

## Measurement and identifiability
Anabasine depends on total smoked exposure and biological yield; cotinine/3HC
enter as molar nicotine-equivalent concentration, including other nicotine.
Neither signal depends directly on legal origin. Matched lawful-supply data must
allow stock/reporting discrepancy and lawful unrecorded consumption.
The likelihood integrates lognormal probability into reported concentration bins,
including the below-LOQ interval. Cutpoints and error levels are planning values,
not local assay validation. Lowering the LOQ refines an existing partition while
holding error fixed; it is not an assumed gain in biological calibration.
Calibration, supply, and product-composition information are valued jointly with
chemistry. Errors are independent only conditional on the full latent state.
Residual dependence and additional batch/flow uncertainty remain sensitivity gaps.

A causal policy-study channel presupposes a credible counterfactual design and
measures a policy/reference consumption ratio. Ordinary baseline wastewater must
never be relabelled as that study. A criminal-harm channel is a hypothetical
classification research experiment, not a biomarker or observed enforcement rate.
Both require separate feasibility/cost specification; their gross values are
research-screening scenarios only.

The same-data robustness analysis applies all candidate priors to identical
possible observations under one common reference predictive law. It holds values
and likelihood fixed. It is not an experiment on political persuasion and does
not promise that real stakeholders will agree.

## Monetary and implementation scope
Normalised results can be multiplied by explicitly hypothetical NZD value scales
and compared with hypothetical costs; these yield threshold statements, not NZ
social-loss estimates. Earlier tariff-based programme costs remain useful planning
context but are not automatically assigned to these coarsened signal experiments.
EVPI requires no assay/cost. EVSI requires a likelihood, not a quote. ENBS needs a
compatible value scale and cost scenario. An implementation-adjusted policy study
needs evidence on how confidence changes adoption/delay; it remains a follow-on,
not a speculative monetary credit for overcoming rhetoric.

## Verification and next empirical increment
Check Bayes martingales, probability sums, EVSI <= reachable-group EVPPI <= EVPI,
zero information, perfect information, null harm/diversion, common-payoff and
replicated-row invariance, scalar/vector parity, and scientific gain without
policy value. Exact enumeration removes outer simulation error from the primary
results; finite-model and structural uncertainty remain. The independent MC check
is only an integration diagnostic, not evidence of current NZ predictive validity.

Next: define one real regulatory contrast; qualify a matched repeated WBE/legal-
supply series; investigate causal switching and mitigation effectiveness; obtain
separate criminal-harm evidence. Predefine cross-source bias, holdout tests and
Māori governance/permissible-use arrangements. Do not infer ethnicity or criminal
network membership from wastewater. Preserve the option of declining research.
