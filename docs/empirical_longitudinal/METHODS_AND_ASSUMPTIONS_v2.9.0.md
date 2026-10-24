# Empirical longitudinal consumption bridge — methods and assumptions

Author: Dylan A Mordaunt. Version 2.9.0. Analysis date: 24 October 2026.

## What has actually been fitted
A historical summary-data model of the ratio of a survey-derived consumption proxy to
period-matched recorded lawful supply. The input evidence is national repeated cross-sectional
survey and administrative supply summaries, not individual longitudinal follow-up or a newly
received wastewater panel. This is an additional empirical component of the NZ VOI programme.
It is not a current joint NZ exposure/origin posterior, illicit-market estimate, causal policy
model or monetary funding recommendation.

## Sources and transformations
The existing `data/empirical_intake_20261024/nz_historical_legal_supply.csv` records Tables 1–2
of Phyo and Bullen (2025), *Trends in the illicit tobacco market in New Zealand: a consumption
gap analysis*, DOI 10.1136/bmjph-2025-002853, PMCID PMC12410603. The source was re-read through
the PubMed/PMC connector on 24 October 2026. This is a re-verification of the existing evidence,
not another independent dataset. The PDF/workbook was not downloaded anew.

The publication uses national annual cigarette-equivalent releases, including domestic and
duty-free sales, and 0.7 g per RYO cigarette equivalent. Its demand-side upper/lower scenarios
are based on daily-smoker-count limits, a fixed mean intensity, and an uplift factor of 1.23.
The prominent upper scenario is not a central estimate. The uplift itself was anchored using
a historical illicit/foreign-pack assumption and supply data. It cannot be entered again as
an independently measured parameter. The related source consumption gaps, intensity series
and NZHS percentages must not be added as independent likelihoods for the same observations.

We preserve all 12 input years, 2012–2023, exactly. Primary alignment needs the previous year's
supply, leaving 11 paired periods, 2013–2023. No 2011 cigarette-equivalent supply is invented.
The 2010–2025 reported-tonne series remains in its existing fitted component and is NOT silently
converted to sticks or appended as compatible paired consumption observations.

### Working summary likelihood (an explicit approximation)
For published bounds L_t, U_t and source uplift u=1.23:

    m_t = [log(L_t) + log(U_t)] / 2 - log(u)
    s_t = [log(U_t) - log(L_t)] / [2 Phi^-1(0.975)]

The exp(m_t) centre is reconstructed, not reported. Bounds are not treated as interval-censored
assay data or as two independent observations. This log-Gaussian approximation covers the
count-bound component only. Primary extra CVs are 10% for intensity and 5% for alignment,
explicit analyst assumptions. Arithmetic-midpoint, source-upper/source-lower stress centres,
zero/20% intensity CV, 15% alignment CV and correlated alignment errors are separate challenges.
The bounds omit uncertainty about non-daily use, people under 15, intensity measurement,
reporting error, product conversion, visitors and source bias. A good fit is not proof those
components are negligible.

The 2014 Table 1 printed lower consumption does not equal its printed lower smoker count times
intensity. Published lower value: 2,149,262,500; 539,000 x 3,978.5 = 2,144,411,500. The 4,851,000
stick discrepancy is recorded without correcting the source. An exclusion sensitivity removes
that period. The source bounds are not regenerated from our preferred arithmetic.

## Period matching
The source originally pairs a survey ending in year t with calendar-year releases in t. We show
that replication, then compare an explicit nominal July-to-June alignment. Calendar-year totals
are spread uniformly across the actual calendar-year days. The period average is multiplied by
365 to match the source annual-equivalent convention, not treated as a total over a 13-month
collection window. Leap-year allocation is exact. This does NOT recover monthly releases.

A documented-window sensitivity uses September 2020–August 2021 and July 2021–July 2022 for the
relevant survey collections, based on existing source-vintage notes. These are month-resolution
bounds, not exact participant dates. Any overlapping collection and residual survey dependence
remain uncertainties; optional correlated error sensitivity is not a fitted correlation.

## Lawful consumption accounting
At a fixed unit, geography and product basis:

    C_t = R_t + S_(t-1) - S_t + U_t + V_t + D_t

R is reported releases; S is nonnegative inventory at boundaries; U is lawful supply absent
from the recorded series; V is a signed net geographic/visitor adjustment; D is an added duty-
free channel only where the source excludes it. This source includes duty-free, so D must be
zero. Stocks have n+1 boundaries; changes telescope. Invalid negative implied consumption fails.

Scenarios include 0/30/60 days of stock, absent lawful channels of 0/2/5% of recorded releases,
and net visitor adjustments of -5/0/+5%. These are analyst accounting stresses, not estimates
of observed inventory, home-grown tobacco, duty-free imports or tourism. A 30-day stock scenario
sets initial inventory at the initial annual release rate and subsequent closing inventories
at each current release rate. It cannot manufacture the same stock drawdown every year.
The source's physical/RYO conversion and scope remain imperfect; this accounting does not fix
that empirically. Neither population nor catchment allocation is inferred from national totals.

## Longitudinal likelihood and posterior
Define y_t = m_t - log(period-matched reported supply). With elapsed time relative to the first
observation:

    x(t) = a + b t + W_q(t)
    a ~ Normal(0, 0.7^2); b ~ Normal(0, 0.10^2)
    Cov[W_q(t), W_q(s)] = q^2 min(t,s)
    y | x ~ Normal(x, Sigma_obs)

q has a half-normal(0.10) prior truncated to 0.005–0.35 annual log-SD, numerically integrated on
41 geometric grid locations with trapezoidal weights. Grid density is on q, not log(q).
The intensity term is independent across years in the primary model; an alignment component
can instead use exponential actual-lag correlation, with a stated half-life. No unknown
correlation is estimated from unpaired published marginals.

Intercept and slope uncertainty are integrated analytically. Gaussian conditioning uses
Cholesky solves, not explicit inverses. Process-SD uncertainty is integrated with log-sum-exp.
Each joint path samples one q component and one complete correlated trajectory. The intervals
are latent-process intervals; retrospective predictive checks separately add the anticipated
summary-observation error. That anticipated error is obtained from preceding periods only.

The primary run uses 8,192 seeded paths. An 81-point grid, wider q support, alternative q priors,
error assumptions, source-centre choices and date alignments are retained separately. Different
centre/alignment datasets cannot have their marginal likelihoods naively compared as model
probabilities. No MCMC ESS, convergence, national causal validity or arbitrary model averaging
claim is made. 2024–2026 ratios are unobserved extrapolations. Their associated current absolute
consumption cannot be calculated without a compatible lawful-consumption denominator.

## Reporting bias and signed discrepancy
One common reporting/calibration factor per full path maps the fitted raw ratio into a
conditional survey proxy. Median factors of 1.0, 1.23 and 1.5 and log SDs 0, 0.20 and 0.40 are
varied. The uncertain multiplier is a net reporting/calibration stress and can be below one;
it is not a strictly one-sided underreporting prior. All values are assumptions, not a new fit.
The same raw posterior paths are used across alternatives. The mapping preserves shared error
instead of letting repeated years average it away.

    proxy_t = exp(x_t) x matched_recorded_supply_t x reporting_factor
    signed_gap_t = proxy_t - adjusted_lawful_consumption_t

Signed gaps are not truncated at zero. Their probability of being positive is conditional on
this incomplete measurement model. It is NOT P(illicit market exists), illegal market size,
criminal harm, or a probability of harm from endgame. Daily smokers aged 15+ are not an exhaustive
consumption population; missing scope must be reconciled before origin inference.

## Validation and interpretation
Seven unique years, 2017–2023, are held out in sequential retrospective checks for each of
three alignment scenarios. Each model is refitted using only earlier ratio observations.
The same yearly targets recur across alignments; 21 rows are not 21 independent validations.
Overlapping administrative denominators and current-vintage source publication mean this is
not real-time or blinded external validation. All seven targets fell within each alignment's
broad 95% interval; such small-sample coverage does not establish calibration of the nominal
level and may reflect wide working errors. No causal conclusion follows from these checks.

Source code, input bounds, assumptions, outputs, figures and hashes are available. The
remaining sample-level WBE, product/catchment alignment, identified causal effects, criminal
harm and current supplier-quote requirements remain separate.

## Method references
- Phyo and Bullen (2025): https://doi.org/10.1136/bmjph-2025-002853
- Source data: https://pmc.ncbi.nlm.nih.gov/articles/PMC12410603/
- SciPy numerical primitives: https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cho_solve.html
- Derived kernel and accounting equations above are the present implementation, not a claim
  that an external paper has validated this particular model for NZ funding decisions.
