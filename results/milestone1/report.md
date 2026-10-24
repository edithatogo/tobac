# M1 — Which uncertainty can change a regulatory decision?

24 October 2026. Completed conditional screening experiment; not a calibrated NZ policy or funding recommendation.

## Change in question

Regulatory EVPI and grouped EVPPI now precede assay design. Scientific learning is reported separately from decision value. The prior cessation-allocation model remains a secondary application in the preserved source archive.

Four archetypes are compared: reference approach, retail restriction, that restriction with supporting cessation/supply mitigation, and expanded cessation. None is claimed to be an exact implementation of current or repealed NZ legislation. Twelve binary uncertainty axes define 4,096 hypotheses, not 4,096 observed people or wastewater samples. Nine prior/dependence scenarios are kept separate, as are four normative criminal-harm weights. Thirteen study experiments are evaluated.

## Reference results

All values below are **normalised decision units**, not NZD, QALYs or estimates of national harm. The reference prior is balanced and the normative crime weight is one.

| Perfect information target | Value |
|---|---:|
| All decision uncertainty: EVPI | 0.071142 |
| Behavioural policy response: EVPPI | 0.032580 |
| Mitigation effectiveness: EVPPI | 0.027475 |
| Current market state: EVPPI | 0.010398 |
| Incremental criminal harm: EVPPI | 0.009100 |
| Health consequence coefficient alone: EVPPI | 0.000000 |
| Calibration and supply measurement alone: EVPPI | 0.000000 |

Group values are not additive. Zero partial value does not mean that a quantity is scientifically unimportant: it means perfect knowledge of that group alone does not improve the selected action under this model. In particular, calibration can complement later measurements despite having no immediate policy value alone.

Behaviour or mitigation has the highest grouped value in all nine prior/dependence scenarios at weight one. This is robustness within the **declared** supports and equations, not a finding that these must dominate in NZ. The reference prior prefers restriction plus support; high-diversion beliefs prefer expanded cessation. These are scenario outputs, not recommendations.

| Information experiment | Gross EVSI |
|---|---:|
| No new information | 0.000000 |
| Nicotine-equivalent report | 0.000130 |
| Anabasine report | 0.001126 |
| Biomarker panel | 0.001632 |
| Matched lawful-supply information | 0.003579 |
| Panel plus supply | 0.004651 |
| Improved quantification plus supply | 0.004678 |
| Biological calibration plus panel/supply | 0.005601 |
| Credible causal policy comparison | 0.017427 |
| Hypothetical criminal-harm study | 0.000000 |
| Causal comparison plus harm study | 0.018796 |
| Linked market and causal comparison | 0.024365 |

The causal comparison and criminal-harm experiments have assumed performance. They are not achieved study designs. Baseline wastewater must not receive their information value. No study costs are imputed from earlier unmatched programme tariffs. Conditional price tables vary explicit monetary scales and hypothetical costs.

The baseline-reachable perfect-information bound is 0.010398, around 14.6% of total EVPI in this reference scenario. The panel/supply EVSI is below that bound. Thus a large overall EVPI would not, by itself, justify buying baseline wastewater data.

## Scientific learning is different

Under independent prior components, the panel provides 0.302944 nats about total tobacco but essentially zero about illicit share, future diversion or criminal harm. Adding matched supply gives 0.085871 nats about illicit share and 0.671072 nats about absolute illicit volume. Some information about absolute illicit volume comes from learning total consumption even without resolving share.

The hypothetical criminal-harm study supplies 0.192745 nats about its target but zero reference EVSI: its noisy results do not move the policy choice. The causal comparison provides 0.234600 nats about future diversion and a 24.98% probability of resolving the specified material-growth event at 90% confidence. That event and confidence level are design assumptions, not policy triggers.

Three alternative diversion priors were applied to the **same** possible observations. Baseline panel/supply data leave the expected range of beliefs about material policy-induced illicit growth at 0.600000. The causal experiment reduces it to 0.396340 under the reference predictive law. This is a mathematical sensitivity comparison, not a study of real stakeholder persuasion. Normative disagreement remains separate.

## Numerical qualification

- 29 local tests passed, including null effects, mass balance, legal-origin invariance, independent-information exclusions, shifts, replication and analytic binary cases.
- 974 full-run invariants passed.
- Independent scalar/vector finite-signal EVSI error: 8.67e-19.
- Independent 50,000-draw outcome-integration check: 0.00461404 (SE 0.00002853), compared with exact 0.004650638.
- Primary results enumerate all declared states and outcomes. They have no outer Monte Carlo error; continuous-model, structural and empirical errors remain.
- Small negative information quantities near 1e-14 are floating-point roundoff, not negative scientific information.

Source/output hashes are preserved with the complete local run. The repository includes compact projections of the result tables and the completed validation record; the runner and hosted workflow reproduce the full tables.

## Limitations and the next milestone

This model excludes important mechanisms, including initiation/relapse, intensity compensation, market recruitment, detailed nicotine-product substitution and dynamic criminal displacement. Its normalised linear consequences, binary supports, one-report experiments and prior probabilities are deliberately simplified. Chemistry is represented as anabasine plus molar nicotine-equivalent reporting, not a fully validated laboratory pipeline. Assumed dependence can induce indirect learning but does not create causal identification.

The next empirical milestone is therefore **not an optimal national sampling network**. It is a matched consumption/supply observation study linked to a prespecified real policy contrast, alongside evidence on response, mitigation and incremental criminal harms. The exact priority ordering must then be rerun under defensible fitted or elicited priors. No empirical claim is certified merely because the software, CSL or external-library parity checks pass.
