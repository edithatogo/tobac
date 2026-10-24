# Reproduced longitudinal results

These compact tables are from full local reruns after importing the predecessor v2.8/v2.9
components into the `tobac_supply` namespace. The release series and historical ratio are
separate estimands, not a fused current NZ exposure/origin posterior.

- `releases/forecast_summary.csv`: conditional reported-tonne projections, three window models.
- `releases/predictive_scores.csv`: retrospective current-vintage predictive checks.
- `empirical/latent_ratio_summary.csv`: historical raw survey-proxy / matched-release ratios;
  2024–2026 rows are unobserved extrapolations.
- `empirical/source_audit.json`: preserved source arithmetic/scope limitations.

All raw input records, declared model configurations and numerical code are checked in.
The full runners create posterior paths, complete sensitivity tables, PNG/SVG figures,
captions and fresh hash manifests. Run both workflows from the integration guide into new
output directories. These compact folders are not complete run-manifest directories and
should not be passed to the run verifier as if they contained every generated artifact.

Local verification and archive parity: `integration/longitudinal_local_verification.json`.
No new current paired assay data, measured inventory, causal effects or funding recommendation
was introduced by source integration.
