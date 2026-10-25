# Reproduced longitudinal results

These compact tables are from full local reruns after importing the predecessor v2.8/v2.9
components into the `tobac_supply` namespace. The release series and historical ratio are
separate estimands, not a fused current NZ exposure/origin posterior.

- `releases/forecast_summary.csv`: conditional reported-tonne projections, three window models.
  Only 2026 is a primary forecast horizon; 2027–2030 are fixed-parameter extrapolations with no
  policy shock, structural change or capacity model (see
  `docs/calibration/METHODS_AND_ASSUMPTIONS_v2.8.0.md`), so their intervals are not complete
  uncertainty.
- `releases/predictive_scores.csv`: retrospective current-vintage predictive checks.
- `empirical/latent_ratio_summary.csv`: historical raw survey-proxy / matched-release ratios;
  2024–2026 rows are unobserved extrapolations.
- `empirical/source_audit.json`: preserved source arithmetic/scope limitations.

All raw input records, declared model configurations and numerical code are checked in.
The full runners create posterior paths, complete sensitivity tables, PNG/SVG figures,
captions and fresh hash manifests. Run both workflows from the integration guide into new
output directories. These compact folders are not complete run-manifest directories and
should not be passed to the run verifier as if they contained every generated artifact.

These checked-in compact tables are a historical snapshot. CI regenerates its own outputs from
current code but does not diff them against `results/longitudinal/`, so nothing here is
currently gated against HEAD; a divergence between these tables and CI output would not be
reported automatically.

Local verification and archive parity: `integration/longitudinal_local_verification.json`, which
records a 42-of-43 byte comparison against a predecessor archive that is not retained in this
repository.
No new current paired assay data, measured inventory, causal effects or funding recommendation
was introduced by source integration.
