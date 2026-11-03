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
outside the checkout. In that producer-only replay the consumer was not installed;
the environment is inside the worktree and independent preservation remains open. Next: review and
publish this bounded evidence after PR #72 receiving checks; Scientific ecosystem
remains open pending native managed-parser acceptance.

## Native lineage consumer-wheel replay and source candidate — 29 October 2026

Chat `01a184ba-0d0a-7111-969b-ef556b3bf966` owns this consumer-only follow-up
in `/Users/doughnut/.codex/worktrees/tobac-ecosystem-parser/tobac`, branch
`codex/native-lineage-consumer-wheel-replay-20261029`, base `3b41349`. Owned
paths are the existing native-lineage Conductor records, MOH documentation/review
and its existing technical summary. Native scope is read-only source assessment
and private consumer/producer artifact replay; the archive producer's source,
estate, active checkout and authentication remain with its existing owner.
Next: record installed-library replay and the bounded SHINE candidate without
promoting either to full lineage or scientific acceptance. Scientific ecosystem
remains open pending native managed-parser acceptance.

Consumer-wheel checkpoint: a second isolated local-cache replay installed both
libraries, verified 36 consumer wheel files against committed source, and matched
all 16 MOH values and output bytes. Script snapshots were run outside the checkout,
but are not installed commands; the environment remains inside the worktree.
A retained SHINE article was assessed read-only as a second-source candidate;
its hash differs from the earlier referenced source copy. No new native
transformation, source registration or scientific acceptance is asserted.

## SHINE extraction continuation — 29 October 2026

Chat `01a184ba-0d0a-7111-969b-ef556b3bf966` owns a bounded second-source
consumer extraction in `/Users/doughnut/.codex/worktrees/tobac-ecosystem-parser/tobac`,
branch `codex/native-lineage-shine-extraction-20261029`, base `b5e2214`. Scope:
SHINE Table 2 parser/parity tests and exploratory consumer evidence; the archive
producer's source, estate and active native operations remain with its owner.
Only the already-retained source bytes and committed consumer metadata are read.
Source capture and the earlier referenced edition remain distinct; no model input
or scientific conclusion is changed. Next: test a strict locator and compare the
published model-input parameters with the existing configuration. Scientific
ecosystem remains open pending native managed-parser acceptance.

The focused SHINE and workstream checks passed (48 tests), and a comparison of
retained source bytes to committed consumer metadata was saved privately at
`/Users/doughnut/Documents/tobac-native-lineage-private/20261029-shine-consumer-comparison/`.
The source copy and earlier reference have distinct hashes and unknown capture
equivalence. No native source registration, transformation receipt or scientific
qualification has been claimed. The next consumer operation is a separately
reviewed native transformation and strict record readback after the implementation
is committed; producer registration and closure remain with the producer owner.

## Native lineage Phase 8 acceptance and publication — 2 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns this bounded integration
in `/Users/doughnut/Documents/tobac` on local `main`, published for review
as `codex/native-lineage-phase8`. Producer source ownership for this packet
is `/Users/doughnut/Documents/archive-lineage-port-20261101` on
`codex/transform-closure-20261102`. Scope includes producer material checks,
consumer qualification/recovery, the existing native-lineage Conductor records
and receiving-ref verification. No native capture or authentication mutation
is in flight. Three untracked decision drafts remain outside this packet.
Next operation is terminal qualification readback and guarded receiving-ref
publication. Earlier assignments above remain historical.

## Native lineage hosted acceptance closeout — 2 November 2026

Chat 01a19a6e-2e47-7b10-8a35-4e7d7fedb965 owns the consumer integration and
Conductor closeout in /Users/doughnut/Documents/tobac. The integration and
fixture correction reached main through guarded fast-forwards at abcbcb4 and
14303e4. Producer /Users/doughnut/Documents/archive-lineage-port-20261101 remains
at the verified c76d78df receiving tree. The hosted route consumes signed local
native byte verification and rechecks current inputs. Original objects and the
local signing authority stay with their native owner. No capture/authentication
operation is active. The three pre-existing decision drafts remain untracked.
The final metadata-only publication is owned by branch
codex/native-lineage-acceptance-closeout. Earlier assignments remain historical.

## Repository and decision-draft reconciliation — 2 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns this documentation-only
reconciliation in `/Users/doughnut/Documents/tobac`, from main `e88d563`.
Scope includes Conductor status/registry/archive metadata, the three existing
November 1 decision drafts and exact reviewed publication paths. No scientific,
native object, authentication, runtime or dependency mutation is in scope.
The three drafts are now retained as superseded historical proposals with actual
acceptance links and unverified approval placeholders identified. Producer
`c76d78df` remains unchanged. Next operation is focused validation, ordinary commit
and guarded receiving-main publication. Earlier ownership entries remain history.

## DXP1 Linux audit-lock qualification — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DXP1 in
`/Users/doughnut/Documents/tobac`, branch `codex/dxp1-linux-audit-lock`,
from receiving main `803e800`. Scope is the Linux audit job in the existing
cross-platform workflow, its workflow security contract, focused qualification
and Conductor/evidence readback. No native capture/authentication operation is
active. The existing audit lock and scientific inputs remain unchanged unless
an actual hosted failure establishes a necessary bounded fix. Next operation is
hash-checked Linux installation and the existing strict/security Nox commands
through GitHub Actions. DXP2–DXP4 remain deferred.

First hosted attempt `41534027128` installed the unchanged lock and passed strict,
security and 95 focused tests. Its export failed because the scanner installer was
macOS-only. The existing scientific workflow edit also correctly failed its signed
acceptance pin. Corrective scope moves the audit into a dedicated `linux-audit.yml`
and adds exact checksum-pinned Linux scanner support; the pinned cross-platform
scientific workflow is restored byte-for-byte. No lineage waiver or new signature
is required for this separate engineering audit command.

DXP1 acceptance at `a17d90b`: GitHub run `41534684953` / job `125583466187`
succeeded, including source-bound hash installation, strict_all, security, 96
focused tests and scanner-checked artifact export. Downloaded environment matches
all 96 locked packages plus the editable project; no unexpected packages or known
vulnerabilities. Receipt: `integration/linux_audit_lock_20261103.json`. No audit
lock or scientific input changed. The original scientific workflow bytes remain
identical to receiving main. Next operation is exact-head checks, guarded
publication and receiving-ref readback; DXP2–DXP4 remain deferred.

## DXP2 package portability — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DXP2 in
`/Users/doughnut/Documents/tobac`, branch `codex/dxp2-package-portability`,
from receiving main `c024f4c`. Scope is the existing clean-package checker,
package metadata/path oracles and focused tests, a separate hosted portability
workflow, and Conductor/evidence reconciliation. Native capture, authentication,
scientific inputs, Nox entrypoints, dependency pins and accepted scientific
workflow bytes remain unchanged. No local expensive operation is active.
Next: build and install both direct and sdist-reconstructed wheels in external
Unicode/space paths, verify metadata/markers/contents and run installed API/CLI
smokes on Linux and Windows. DXP3 numerical reproduction and DXP4 release/lock
workflows remain separately deferred.

DXP2 acceptance at `d2551a0`: GitHub run `41542664379` succeeded on Linux
(job `125610440252`) and Windows (job `125610440607`). Downloaded wheel/sdist,
Nox, environment and clean-package evidence was verified against retained hashes.
Both installed routes pass outside the checkout with Unicode/space paths and
Unicode transport identities. Ten dependency-marker cases agree. Platform wheel
members differ only in METADATA LF/CRLF and its RECORD hash; within each platform,
direct and sdist-rebuilt contents match exactly. Receipt:
`integration/package_portability_20261103.json`. The existing scientific workflows,
Nox entrypoints, runtime/audit locks and native objects remain unchanged. Next:
exact-head checks, guarded publication and receiving-ref verification. DXP3/DXP4
remain deferred; no numerical or public-package-release acceptance is inferred.

## DXP3 scientific reproduction — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DXP3 in
`/Users/doughnut/Documents/tobac`, branch `codex/dxp3-scientific-reproduction`,
from receiving main `1e9e69e`. Scope is a separate Linux/Windows reproduction
workflow, a fail-closed comparison of all eight accepted runner variants and
82 scientific CSV tables, focused tests and Conductor evidence. Original native
objects, authentication, model/configuration code, Nox commands and existing
scientific workflows retain their owners and bytes. No native mutation is active.
The reference ZIP contains only project-generated CSV results reopened through
the actual pinned installed producer's public CAS verification API. Every byte
matches its existing accepted checkpoint object ID; no archival originals or
manuscript content is exported. Next: execute full Nox reproduce plus the no-grid
M2 variant on both hosts and verify all numerical/identity comparisons.
Prior receiving run 41545029388 failed because pip-audit's PyPI read timed out;
that failed scan is retained, with fresh security qualification required here.
