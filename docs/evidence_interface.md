# Evidence conditioning and the lawful-supply boundary

`src/tobac/evidence.py` is the common interface for observed evidence. It reuses the finite decision engine; it is not a new inference library or a claim of a current NZ posterior.

## Required contract
An `EvidencePacket` declares an evidence ID, **underlying data IDs**, source IDs, state IDs, log likelihood, source/target scope and likelihood-model identity. Scope includes geography, population, period and units. Use `state_identifiers(states)` to fingerprint all named physical/latent values in each state. The exact state IDs **and order** must match. Index-only identifiers are not sufficient for cross-repository exchange.

Only `role='observation'` is accepted. A forecast or another model's posterior is not a new observed-data likelihood. Multiple papers using the same tobacco returns must preserve the same underlying data IDs. Reusing those IDs, even under a different citation, is rejected. A change in scope needs an explicit transport note; a sequential update needs a conditional-dependence note. Shared errors must actually be in a joint likelihood or latent state, not only mentioned in prose. Metadata checks cannot detect dishonest relabelling, undisclosed shared data or an incorrect transport model.

`condition(belief, packet)` uses log-scale Bayesian reweighting, permits probability **densities** above one, rejects unsupported observations and preserves joint dependence. Its receipt records predictive density, finite-state ESS and source/model identifiers. These are diagnostics, not independent scientific certification.

`prospective_value` rejects proposed reuse of evidence already included in D0. `incremental_value` distinguishes:
- marginal prospective value: EVSI(A,B)-EVSI(A), averaged over A;
- value of B after a particular realised A, which can be higher or lower.

Supply a joint outcome tensor for correlated reports; multiplying marginal likelihoods is valid only conditional on a sufficient shared state. Repeating the same report is tested to have zero incremental value. The expected remaining EVPI identity is checked. Remaining EVPI after one particular surprising observation can increase without violating the preposterior identity.

## Release accounting
All amounts must use the same time, geography, population and physical unit:

    recorded_consumption = total*(1-illicit_share) - lawful_unrecorded
    releases = (recorded_consumption + stock_change + outbound + wastage) * reporting_multiplier

`lawful_unrecorded` is an **absolute quantity**, not a fraction. Positive stock change means accumulation; negative stock change is permitted, but negative implied consumption/releases are rejected rather than clipped. Inbound lawful consumption outside the release channel belongs in lawful_unrecorded; avoid duplicating visitors or duty-free across adjustments. Unit conversions, dates and denominator harmonisation must precede the numerical bridge.

`release_loglikelihood` accepts an explicitly specified positive-definite covariance across jointly observed periods. The Gaussian reporting-error approximation is a modelling choice; precision is not inferred from the fact that releases are administrative records. Forecast paths are predictions, not independent evidence. A posterior exchange requires the original prior/likelihood and shared-data reconciliation, not silent multiplication by another posterior.

## Parallel integration
Issue #1 proposes `tobac_supply` on the separate longitudinal branch. At this inspection it still points to its initial commit; no completed supply module was received. These adapters are additive under `tobac`. No parallel namespace, branch or empirical series has been overwritten or merged. The intended handoff is dated observations plus a reviewable likelihood/transport/accounting contract, preserving shared draw/state and data identity.

The conditioning examples in M2a use synthetic observations of 250 and 500 with assumed SD 80. They are deliberately fixtures, not NZ observations or current illicit-market estimates.
