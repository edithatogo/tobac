# Reported-release calibration: methods, inputs and limits

Author: Dylan A Mordaunt. Analysis date: 24 October 2026.

## Evidence reconciliation
The supplied successful browser completion concerns the *tobacco-release chart*, run
`d26e9dec-6327-41f7-a08e-ff95cb3fee3a`. It is not the failed NZ Health Survey extraction.
A saved transcription of that completion is in `data/calibration_20261024/raw/`.
All 16 transcribed 2010–2025 values equal the accepted v2.7 series exactly, with a difference of
0 tonnes on all 16 rows. The full 16-value v2.7 series is not retained in this repository (a
prior-work parameter file records the 2025 level of 755 tonnes only), so that comparison is
recorded rather than re-runnable here. They are the same observations and are
conditioned on once, not counted twice. Unquoted thousands commas are repaired only under
an exact series-specific grammar; generic ambiguous CSV rows are rejected.

Source: Ministry of Health, Tobacco returns 2025, numerical table
`highcharts-data-table-0`, label "Total tobacco sold tonnes (excl. cigars/cigarillos)".
https://www.health.govt.nz/regulation-legislation/smoked-tobacco/information-for-manufacturers-and-importers/tobacco-returns/tobacco-returns-2025
The original workbook URL is retained as a locator only. Workbook bytes and chart/workbook
parity have NOT been independently verified. No conversion, domestic/duty-free or catchment
basis is inferred from the completed browser extraction. Includes 2010–2025, excludes cigars,
cigarillos and heated tobacco; units are annual reported tonnes, represented as tonnes/year.

## Fitted component
Let R_t be the published administrative total and z_t=log(R_t/R_(t-1)).
Conditional on mu and sigma, z_t ~ Normal(mu,sigma^2), independently across years.
A full-history fit uses 15 annual changes from 16 levels. A four-change fit uses five levels.
This is a small univariate empirical transition model, not a tobacco-demand, observation-origin,
health, welfare or policy model. It does not explain *why* reported releases changed.

Priors are deliberately declared rather than described as empirical estimates:
- mu: Normal(0,0.10^2), truncated to [-0.50,0.25] annual log-change units.
- sigma: HalfNormal(0.10), truncated to [0.005,0.30] annual log-change units.
- 151 mu grid points and 60 sigma points; trapezoidal cell weights and normalized joint mass.
- Alternatives: all available changes, the latest four changes, and the latest eight changes.
- Sensitivities: each prior scale 0.05, 0.10, 0.20; doubled resolution on the same support.
The drift prior allows growth and decline. Bounded sigma ensures finite projected-level moments.
The chosen supports are assumptions; low grid-edge mass is a numerical diagnostic, not proof
that the support encompasses future shocks. Extended-support and nonstationary alternatives
remain suitable next sensitivity work before relying on long-horizon projections.

The posterior is proportional to prior cell mass times the Normal change likelihood. Calculations
use stable log-sum-exp. These are numerical quadrature posteriors; no MCMC convergence or ESS
claim is made. The Python code and independent likelihood tests expose the formulas.
For horizon h, log(R_(T+h)/R_T) conditional on a grid cell is Normal(h*mu,h*sigma^2).
Means are analytic finite-mixture expectations; quantiles solve the mixture CDF. Joint paths
choose one parameter pair per trajectory, then draw conditional annual innovations. Sampling
independent annual forecast marginals would destroy the joint dependence needed by later VOI.

## Training, prediction and data leakage
At each rolling origin the next reported observation is excluded. 2015–2022 is an exploratory
selection diagnostic, and 2023–2025 is shown separately. The series was already seen before this
split was chosen. This is neither blinded validation nor preregistration. Every observation comes
from the same 2026 source vintage, so this is not a real-time historical forecast exercise.
The recency candidates' likelihoods use different data subsets: their marginal likelihoods must
not be interpreted as comparable model evidences. All candidates remain separate structural
scenarios; no arbitrary posterior model probability is assigned.

Only 2026 is a primary forecast horizon. 2027–2030 extrapolate fixed parameters with no policy
shock, structural change or capacity model. Conditional intervals are not complete uncertainty.
Annual rounding, stock changes, issuer revisions and source-definition error are not estimated
in this likelihood. Their absence must not be represented as proof of exact consumption.

## Downstream link remains gated
A release forecast can inform the *recorded lawful-supply component* of a joint model only.
Moving to lawful local consumption requires a matched unit/basis and explicit stocks,
visitor/geographic allocation and lawful-unrecorded-supply evidence. Moving to total or illicit
consumption additionally requires a validated exposure and product-origin model. None is
supplied by this fit. No excise revenue, criminal harm, child smoking, QALY or funding value is
calculated from the release decline. Assay calibration and study prices remain separate.

Software documentation consulted:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
These document numerical primitives, not scientific validation of the proposed model.
