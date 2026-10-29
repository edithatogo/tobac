# Scientific interface and integration checks

This document records the integration contract between regulatory and longitudinal components
in this single-developer repository. It is not a scientific endorsement or an automated
background synchronisation service.

## One source of truth

Use the current repository sources, not separate conversation archives.
`src/tobac/` owns the regulatory decision model, finite-state evidence conditioning and VOI.
`src/tobac_supply/` owns the reported-release and historical observation-scale components.
Shared handoff: `tobac.evidence.Scope`, `EvidencePacket`, `state_identifiers` and `condition`.
There is no second independent VOI engine or automatic import of a fitted supply posterior.

Before changes, read `AGENTS.md`, this contract and `conductor/tracks.md`. Before publishing,
re-read current `main`, preserve existing changes, rerun affected tests and use an expected-head
comparison without force. Verify the receiving ref and files. Historical issue #1 notes are
provenance; no coordination comment or independent review is required.

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
Record the publication commit and verification scope in the relevant Conductor track.

## Scientific ecosystem blocker recheck — 29 October 2026

Chat `01a184ba-0d0a-7111-969b-ef556b3bf966` owns the bounded managed-parser
recheck and its Conductor/review receipts in
`/Users/doughnut/.codex/worktrees/tobac-ecosystem-parser/tobac`, branch
`codex/ecosystem-parser-20261029`, base `428bced`. This is the writing lane for
these status and engineering context-selection updates; existing scientific-consumer,
source-binding, lineage and producer assignments remain separate. No scientific source, runtime, lock,
authentication or native graph-writing operation is assigned to this recheck.
Checkpoint: native recheck, local review and fixes complete; full tests pass
(1,063 passed/13 capability skips, 92% coverage), then 55 focused tests pass.
Next operation: guarded source publication and exact-head/receiving-ref readback.
The external managed root-parser gate remains open; no native graph write is assigned.

## Native lineage consumer continuation — 29 October 2026

Chat `01a184ba-0d0a-7111-969b-ef556b3bf966` now owns the consumer extraction
continuation in `/Users/doughnut/.codex/worktrees/tobac-ecosystem-parser/tobac`,
branch `codex/native-lineage-consumer-20261029`, base `346421b`. Owned paths are
the MOH extraction helper/tests, its optional Nox entrypoint, consumer interface
pins and the existing lineage Conductor/review records. Producer code is frozen
at `790044096f6946ff9a21662108f4d924cbad0ba2`; its active writer, checkout,
environment, captures and canonical CAS remain unchanged. Only identified frozen
originals are read and copied into consumer-owned private staging. No acquisition,
request, external submission or scientific-input replacement is assigned.
Next operation: qualify the installed producer artifact, implement exact workbook
extraction/native per-record receipts and review actual execution. Producer
manifest/closure and historical capture-time gaps remain gates; per-record success
cannot qualify the whole lineage. Scientific ecosystem remains open and blocked.

Native consumer terminal checkpoint: implementation `6fa2306`; 16 exact MOH rows,
nine native objects, two strict records and five rejected negative controls.
Full tests/strict/package/security/clean-package and clean-source numerical replay
pass. No producer estate or source changed. Next: publish bounded consumer packet
with hosted checks and receiving-ref readback; retain P2/P3/full track gates.

## Native lineage recovery continuation — 29 October 2026

Chat `01a184ba-0d0a-7111-969b-ef556b3bf966` owns the consumer-only recovery
continuation in `/Users/doughnut/.codex/worktrees/tobac-ecosystem-parser/tobac`,
branch `codex/native-lineage-recovery-20261029`, base `5ff282d`. Scope: consumer
recovery checks, native artifact readback, and the existing Conductor/review and
handoff records. The active archive producer retains its checkout, source files,
environments, canonical CAS and operations. Only frozen producer revisions and
previously identified source bytes are read; any new native attempts are isolated
in this worktree's private outputs. Scientific ecosystem remains open.

The prior worktree's ignored execution directory and runtime environment are not
present at continuation. Their committed summary survives but its referenced
private receipt files have not been found. Rebuild the pinned wheel, make a new
execution with new identity, and assess recoverability honestly; do not portray a
new attempt as restoration of unavailable historical records. Next: verify native
source/record contracts and perform bounded consumer-owned recovery controls.

Native recovery terminal checkpoint: a new exploratory attempt reproduced all 16
MOH values; original WARC payload and capture metadata were verified with capture
time unknown. A private same-device copy outside the managed worktree retained
nine verified objects, original WARC/capture bytes, and strict records. Native
restore/replay passed; missing/corrupt controls failed. Native harness empty/root/
duplicate false-success gaps are recorded, and the consumer MOH inventory preflight
rejects those cases. The earlier private receipts remain absent; no independent
backup, source registration or full native closure is claimed. Next: review and
publish this bounded consumer checkpoint; producer ownership and Scientific
managed-parser blocker remain unchanged.

## Native lineage portable producer replay — 29 October 2026

Chat `01a184ba-0d0a-7111-969b-ef556b3bf966` owns this consumer-only evidence
follow-up in `/Users/doughnut/.codex/worktrees/tobac-ecosystem-parser/tobac`,
branch `codex/native-lineage-portable-replay-20261029`, base `74e52a2`. Scope is
the existing native-lineage track, consumer documentation/review and technical
summary. No archive producer source, estate or authentication is assigned.
A new isolated repo-local Python environment installed the retained producer from
a relative-wheel hash lock with `uv --offline` and the existing cache. Native
records/objects and all 16 workbook values were verified from a working directory
outside the checkout. The consumer itself remains uninstalled; the environment is
inside the worktree and independent preservation remains open. Next: review and
publish this bounded evidence after PR #72 receiving checks; Scientific ecosystem
remains open pending native managed-parser acceptance.
