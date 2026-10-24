# Shared workstream synchronisation

Canonical repository: `edithatogo/tobac`, branch `main`. Coordination: issue #1.
This document is an integration contract, not a scientific endorsement or an automated
background synchronisation service.

## One source of truth

Both workstreams use the current main commit, not separate conversation archives.
`src/tobac/` owns the regulatory decision model, finite-state evidence conditioning and VOI.
`src/tobac_supply/` owns the reported-release and historical observation-scale components.
Shared handoff: `tobac.evidence.Scope`, `EvidencePacket`, `state_identifiers` and `condition`.
There is no second independent VOI engine or automatic import of a fitted supply posterior.

Before work: read main, issue #1 and `conductor/tracks.md`; record the exact base commit and
intended file scope on issue #1. Before publishing: re-read main and the thread, incorporate
concurrent changes, and rerun affected tests. Publish with an expected-head comparison and
without force. Verify the receiving ref and files, then post the commit and actual test scope.
Never reset another workstream to an older ZIP. Do not merge a dependency-update branch merely
to make all branch pointers equal. Divergent branches require a reviewed reconciliation;
ancestor-only longitudinal branch pointers may be fast-forwarded with expected-head checks.

## Accounting translation tested across namespaces

The longitudinal ledger uses:

    C = R + opening_stock - closing_stock + U + V + D

The regulatory observation bridge uses:

    reported_R = (T*(1-I) - unrecorded + stock_change + outbound + wastage) * bias

For the overlapping, no-wastage accounting case:

- `C = T*(1-I)` is a supplied lawful-consumption hypothesis, not inference of I.
- `stock_change = closing_stock - opening_stock`; positive means accumulation.
- `unrecorded = U + max(V,0) + D`; `outbound = max(-V,0)`.
- `D` may be nonzero only when the source excludes duty-free. This is one missing channel,
  not a second addition of duty-free already in R, U or V.
- Bias belongs to the observation model, not another physical consumption adjustment.
- Wastage is not a separate longitudinal-ledger field. Do not silently conflate it with
  visitors; a nonzero-wastage extension needs its own reviewed accounting contract.

Tests check both signs of inventory change and visitor flow and a supplied zero/nonzero
illicit share. They show agreement under the declared mapping, not identification of illegal
origin. All numerical cross-workstream examples are synthetic regression fixtures.

## Evidence handoff and unclosed scientific gates

Underlying data IDs survive citation changes, namespace changes and publications. Preserve
both source scope and target scope, physical product basis, population, date convention,
unit, reporting/calibration assumptions and shared covariance. Use half-open periods where
required by the longitudinal routines and explicitly align end-date conventions before
creating a packet. `Scope` validates geography/population/dates/unit; it does not independently
validate product equivalence, actual data provenance or the truth of a transport model.

Use `state_identifiers` on the same named physical/latent arrays in the same row order.
A shared integer row index is not adequate. Use the original observed-data likelihood and
condition D0 once. A historical ratio reconstructed from survey bounds is a summary-likelihood
approximation and must retain that status. A posterior, forecast or fitted trajectory is not
a new independent observation. Different papers or output tables based on MOH/NZHS records
must not be multiplied as independent evidence. Schema checks cannot detect dishonest relabelling.

The cross tests also require that supply evidence alone leaves an independently uncertain
policy-response parameter unchanged, and distinguish joint prospective EVSI from realised
D0-conditioned value. This mathematical check does not qualify a real causal pathway.

Scientific attachment of historical observations to the current regulatory state remains
open pending matched scope, product/measurement definitions, transport and dependence review.
No current NZ posterior, new causal effect or funding recommendation is produced by this pass.

## Joint checks

    PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -m pytest -q tests/supply_bridge tests/test_workstream_integration.py

The existing full-suite CI commands automatically collect the new file. Full regression
qualification on a complete network-enabled checkout should still run `python -m pytest -q`,
M1/M2a reproduction and both longitudinal runners when their inputs or interfaces change.
A local component receipt does not prove hosted CI, optional-library execution or whole-project
scientific validity. Preserve and investigate failures rather than weakening gates.

Execution receipt: `integration/workstream_sync_verification.json`.
Publication commit and any concurrent-work acknowledgement: issue #1.
