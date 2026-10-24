# NZ wastewater VOI: empirical longitudinal amendment

Dylan A Mordaunt | 24 October 2026 | Version 2.9.0

This local protocol amendment follows the v2.8 reported-release fit. It is not an OSF upload,
preregistration, ethics approval, agency endorsement or a prospective claim about already-run
analyses. The completed analyses in this release are retrospective and exploratory.

## Decisions retained
1. Whether to purchase anabasine, cotinine, optional 3HC, lawful-supply information or calibration.
2. Which feasible NZ regulatory or service action improves outcomes after receiving information.

The remote regulatory screening prioritises regulatory EVPI/grouped EVPPI before study EVSI.
This component contributes source alignment and uncertainty qualification, not causal policy
payoffs. The no-study option retains all feasible actions under existing information.

## New empirical component
Use the 2012–2023 published cigarette-equivalent supply and survey-derived bound series.
Fit 11 period-aligned summary ratios, 2013–2023. Preserve 2012 rather than invent missing 2011
supply for its preceding survey half-year. Keep the latest reported-tonne series separate.
Reconstruct a working Gaussian likelihood only with explicit centre/error assumptions.
Compare nominal survey, source calendar, and documented-collection-window alignments.
Implement a conserving stock/flow ledger, including lawful absent channels and signed visitors.
Fit the latent historical ratio process with integrated drift/intercept/process uncertainty.
Retain signed discrepancies and common reporting error; do not infer legality by truncation.

## Prespecified implementation checks (specified before this implementation)
Code tests check source duplication, period/unit consistency, stock conservation, duty-free
scope, Gaussian conditioning, correlated posterior paths, negative discrepancies, data-vintage
and forecast boundaries. The work-log and test receipts distinguish tests from field validation.

## Completed exploratory checks
Process prior/grid/support sensitivity, summary-centre alternatives, intensity/alignment error,
common reporting-factor scenarios and accounting stresses were run. Historical rolling checks
use seven unique target years and current-vintage data; neither counts of scenario rows nor
in-sample fit constitute independent validation.

## Excluded claims
No new current paired NZ assay samples; no measured stocks or catchment consumption; no causal
learning of prohibition/diversion/enforcement effects; no calibrated criminal harms or child,
ethnicity or socioeconomic outcomes; no clinical QALY or funding recommendation. Historical
survey numbers do not identify source-specific nicotine loads without additional product and
measurement evidence. Population subgroup inference from aggregate chemistry remains prohibited.

## Next empirical gate
Obtain real paired assay rows, raw-scale LOQs, dates, sites, flows/populations and batch/stability
metadata; reconcile product-matched current lawful consumption, non-daily and under-15 use,
visitor effects and source error; fit joint observable predictions. Challenge independent
held-out periods/sites. Do not pass this historical signed gap as an illicit-share prior to the
regulatory engine. No empirical monetary recommendation before consequences and marginal costs
are qualified. Existing request drafts remain unsent unless separately authorised.

Full methods and source rationale: docs/empirical_longitudinal/METHODS_AND_ASSUMPTIONS_v2.9.0.md
