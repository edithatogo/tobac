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

First Windows DXP3 run `41553783852` reached synthesis after producing and
verifying the initial runners, then rejected Windows separators in the fresh
M2 manifest input path. The synthesis reader now canonicalizes only those runtime
references before the unchanged strict source/hash guard, explicitly rejecting
drive-qualified paths. Static source manifests, model code, numerical tolerances,
Nox commands and accepted scientific workflows are unchanged. Focused controls
cover correct Windows paths, changed hashes, traversal, UNC and drive escapes.

The first Linux run completed every existing Nox reproduction validator, then the
new all-table check found M1 gross_value_nzd 1302.2446720089888 versus
1302.2446720092391 (about 2.5e-10 NZD). The new checker had incorrectly selected
publication's absolute-only policy for non-publication reference families. It now
uses the existing longitudinal/reference rtol=1e-9, atol=1e-12 policy for M1,
M2-retail, M3 and longitudinal/calibration outputs; publication/no-grid/robustness
retain their original absolute 1e-10 limit. Exact identities and all established
Nox validators remain unchanged. The first failure and both numerical values are
retained for final evidence review; no model, input or existing oracle was edited.

The direct synthesis-reader fix was rejected by the existing native input gate,
as expected, and was restored before publication. Its patch remains private in
the DXP3 evidence directory. The accepted scientific reader/model inputs retain
their exact original bytes. Nox now prepares a separate validation view: every
original input and output hash is verified, only manifest input-key separators
are canonicalized, duplicate/escaping references fail, and the raw manifest and
outputs stay unchanged. A new signed orchestration capsule will be issued only
after full direct-native readback of all eight original accepted attempts. The
previous capsule/issuer generation is preserved for historical P8 readback.

DXP3 acceptance at 349f09f: GitHub run 41557415490 succeeded on Linux
(job 125659567578) and Windows (job 125659567143). Each ran full Nox reproduction
and no-grid M2, compared eight variants / 82 CSV tables with frozen native results,
and passed the 29-table isolated committed-source publication replay. Downloaded
raw/view and report hashes were checked. The largest normalized errors used
0.085887 of the declared tolerance on Linux and 0.068751 on Windows. Receipt:
integration/scientific_reproduction_20261103.json. Both first failures and the
prior PyPI timeout remain explicit. All 25 candidate checks passed with two
expected trusted-write skips. Seven deferred tasks remain; DXP4 is separate.
Next: final metadata publication checks, guarded receiving-main fast-forward
and exact receiving file readback. Original scientific/native inputs stay unchanged.

## DXP4 manual release and lock workflows — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DXP4 in
`/Users/doughnut/Documents/tobac`, branch `codex/dxp4-manual-workflows`,
from receiving main `68d9049`. Scope: two manual workflow definitions,
their contract tests, digest-only orchestration renewal, inspected execution evidence
and Conductor reconciliation. No local workload/native mutation is active.
Scientific inputs, native objects, dependency locks and private authority retain
their existing bytes and owners. Next: focused checks and native readback, source
publication, actual manual release/four-profile runs, then exact artifact readback.
Candidates are generated and hash-installed in isolated Linux environments; none is
automatically adopted. Release artifacts remain internal, with no PyPI publication.

DXP4 source packet is consolidated on `codex/dxp4-manual-qualified` from
unchanged main `68d9049`. Earlier branch/PR #112 remains preserved and superseded:
its first audit exposed two deferred-path test references, and its next source
security run rejected a prematurely inventoried future receipt. Both were fixed.
The exact final tree passes the complete local publication/security command.
The shared default pre-push hook was absent; the repository's normal installer
restored it without replacing a custom hook. Subsequent publication must pass it.
No force update or history deletion is used. Scientific workflow/capsule bytes
match the verified source packet; the single source commit keeps every outgoing
commit's inventory exact.

The restored guard's first owned publication was interrupted during repeated
historical blob reads, before any push. It is not a pass or budget breach.
Invocation-local reuse now keys successful byte/archive inspection by immutable
Git blob ID and the complete private path/hash policy. Every historical tree,
inventory, mode and protected-policy check still executes; limits and scanners
are unchanged. Controls retain rejection of intermediate copies, unknown paths
and newly protected raw/nested bytes despite an earlier cached inspection.
The current signed lineage preflight still passes after this guard-only change.

Full-history publication inspection found 34 already-published intermediate
commits with 22 omitted inventory paths, all currently reviewed public project
source/tests/lineage receipts. The original legacy baseline remains unchanged.
The current policy records each historical omission by exact commit, path and
Git blob ID; only currently public regular files qualify. Every historical byte
still undergoes document/archive inspection and full-history secret scanning.
Wrong commit/blob, newly private content and paths outside the current public
inventory remain failures. Strict whole-source typing passes with zero warnings.

## DXP4 corrected release route — 3 November 2026

The same chat owns `codex/dxp4-release-runner` in the existing consumer worktree,
from receiving main `3914060`. PR #113 passed 26 checks with two expected
trusted-write skips. The exact source passed full branch pre-push; a redundant
local main push was interrupted in native Actionlint. GitHub's non-force
fast-forward API then advanced main from the explicitly checked `68d9049`.
Both receiving refs and all 736 tracked path/object/mode entries were read back;
the default pre-push hook remains installed.

Stale-source dispatches 41567619304 and 41567622611 rejected release and all four
lock jobs before their workloads. Positive lock run 41567710835 passed four
profiles. Downloaded tar member hashes, current source receipts and every
Linux-marker-selected installed package match: runtime 37, audit 95, Voiage 50,
ecosystem 58. No candidate is adopted.

Release run 41567707353 rejected Ubuntu 24.04 OpenSSH before Nox, as required.
Ubuntu 26.04 is the actual already-qualified image in source reproduction run
41565105342. The correction selects that image without broadening any verifier
profile. Preflight JSON records and the original exit status are retained on both
success and rejection. All eight native attempts were reopened before renewing
only the release workflow pin; the previous signed generation is preserved.
142 focused tests and pedantic workflow audit pass. Next: publish the corrected
source, execute the real main release path, inspect artifacts and close DXP4.

## DXP4 final acceptance — 3 November 2026

The same chat owns metadata closeout on `codex/dxp4-closeout` from receiving
main `fdd6be0`. Source PR #114 passed every required gate before a non-force
fast-forward from the explicitly checked `3914060`. Both receiving refs and
all 738 file/object/mode entries were verified. Stale-source run 41570629439
rejected before Nox. Main remained `fdd6be0` throughout successful release
run 41570769167, including its final source-head guard and package export.

All seven Nox sessions pass. JUnit records 1,210 passed / 19 capability skips,
zero errors/failures. Coverage over all src is 92.03% combined (92.74% statements,
89.64% branches). All eight variants / 82 downloaded scientific tables pass
independent stored-byte comparison under the original policies. All 24 exported
clean-package files match receipt hashes; ten dependency-marker cases, source
module/license bytes and both installed CLI routes pass. Internal-package and
evidence exports match. The release wheel also matches the clean build byte for
byte. Repeated sdist archives differ in timestamps/pax metadata; member bytes,
types, modes and sizes match. An extra local byte-identity assumption was rejected
and retained; no existing package or numerical gate changed.

Lock candidates retain their separate `3914060` source and exact inventories.
No active lock, model, scientific input, frozen verifier profile or original
native object changed. DXP4 is complete for manual release/candidate workflows.
Six numbered advisory/hardening tasks remain. Next: publish this metadata-only
reconciliation with the existing guards and verify receiving refs/files. All
earlier source lanes remain preserved; no force update or history deletion.

## DCI1 selection ownership — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DCI1 selection in
`/Users/doughnut/Documents/tobac`, branch `codex/dci1-selection`, from verified
main `6830891`. The checkout was clean, with one worktree and no active local
Nox/test/native signing operation. Scope is the existing advisory track's
selection/specification/metadata, Conductor status and the public-path inventory.
No runtime, scientific source, workflow, lock, pre-commit hook or native authority
change is assigned. Next: select nonduplicative additions, verify upstream refs
and delivery metadata, record DCI2–DCI4 handoff, then publish the selection packet.
Earlier source assignments remain history.

## DCI1 selection result — 3 November 2026

The same chat/worktree owns the completed selection packet on
`codex/dci1-selection`. Select ty 0.0.95 and Pyrefly 1.4.0 as one bounded
differential type-diagnostics experiment, with macOS/Linux x64 comparators and a
Linux ARM64 static-diagnostic leg. Ty 0.0.96 is below the existing three-day
release-age threshold. Six expected wheel hashes, 14 upstream refs and ten active
action refs were re-read; GitHub tag objects were resolved to actual commits.
Pyrefly's canonical upstream is meta/pyrefly. Publisher ARM scanner checksum
manifests exist; archives were not downloaded/executed.

Omit duplicate Ruff/Zizmor/pip-audit/Gitleaks/attestation/hook wrappers and prek
migration; preserve existing hardening policy. Current source-bound locks,
runtime/scientific inputs, required gates, hooks and native authority are untouched.
The original red-strict/pre-runner/private-entitlement proposal notes are preserved
as historical metadata; issue #4 is closed. DCI2 must implement the isolated
source-bound profile and ARM scanner delivery, DCI3 must execute actual pinned
compatibility/report/import/exit/budget/export checks, and DCI4 must publish the
qualified lane. This packet publishes only selection; those three tasks and DH1/
DH2 remain deferred. Next: focused metadata/integration checks, guarded publication
of this decision, and receiving-ref/file readback.

DCI1 verification: 70 focused metadata/workflow/publication/workstream tests pass
under repo-local Python 3.15.1 and 4 GiB/40-minute bounds. All 20 track records,
Conductor JSON, new/changed local links, selected release age and expected digests
verify. Baseline file hashes match immutable main `6830891`; scientific/runtime/
workflow/lock/hook/config bytes remain unchanged. Current signed-input preflight
passes without renewal. No selected checker or ARM job was executed. Publication
of this decision remains separate from DCI4 publication of an implemented lane.

## DH1 mutant triage ownership — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DH1 in
`/Users/doughnut/Documents/tobac` on branch `codex/dh1-mutant-triage`.
Scope: `tests/engineering/test_scipy_supply.py`, mutation evidence and Conductor
status; native scope: none. The DCI checkpoint remains on its own remote branch.
Next: test concrete missing assertions and classify all twelve hosted survivors.

DH1 result: twelve hosted survivor IDs reconciled; targeted cases detect ten
in a fresh local 129/131 campaign. The remaining two are equivalent for the
qualified SciPy zero-mean path. See `docs/reviews/2026-11-03-supply-mutant-triage.md`.

## DH2 Ruff exception review ownership — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DH2 in
`/Users/doughnut/Documents/tobac` on `codex/dh2-ruff-exceptions`.
Scope: retained source/API Ruff exceptions, focused fixes/tests, policy and
Conductor reconciliation; native scope: none. Parent includes local DH1 commit.
Next: inventory live suppressions and verify behavior-preserving candidates.

DH2 review classified 91 source diagnostic instances. A tested vintage helper
removed one complexity diagnostic but invalidated accepted native lineage, so it
was reverted; all 91 retained diagnostics and their reasons are documented.
No scientific source or interface is changed by the final review packet.

## DH1/DH2 publication and reconciliation — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns publication in
`/Users/doughnut/Documents/tobac` on `codex/dh2-ruff-exceptions`. Scope is the
DH1/DH2 commits and Conductor reconciliation; native scope: none. The separate
DCI checkpoint `e007807` stays unmerged with its evidence and unfinished work.
Next: exact-source guarded publication and receiving-ref readback.

## DCI2 implementation ownership — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns DCI2 in
`/Users/doughnut/Documents/tobac`: isolated advisory lock, runner, workflow,
scanner support, focused tests and Conductor reconciliation. Native scope: none;
next operation: implement and qualify locally, preserving earlier assignments.

Checkpoint: source-bound advisory lock and prototype reports exist locally;
missing Voiage interfaces stop the full-source run. Remaining ownership includes
Nox/CI wiring, report comparison, fixtures, capsule renewal and ARM execution.
The checkout remains dirty for this lane; no native object is owned or active.

DCI3 checkpoint: the pinned Voiage wheel was built and its existing qualification
passed; it resolved both checkers' missing imports locally. Direct fixture and
full-source diagnostic evidence is recorded in the DCI3 qualification note.
There is no hosted advisory workflow to dispatch; DCI2, DCI3 and DCI4 remain open.
No native operation remains active.

DCI4 checkpoint publication ownership: the same chat owns the isolated DCI
checkpoint branch and its remote ref; receiving `main` is guarded. This branch
is a draft implementation and local evidence handoff, not qualified DCI4
completion. Next operation: validate publication boundary and push the exact
checkpoint branch with ordinary hooks, then read back the receiving ref.


## DCI2 resumed implementation ownership — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns the DCI2 integration in
`/Users/doughnut/Documents/tobac`, branch `codex/dci2-implementation`. Scope:
advisory lock/runner/Nox/workflow/scanner, tests, lineage capsule and Conductor.
Native scope: read-only reopening of the eight accepted attempts for signing.
Next: implement fail-closed diagnostics and repeatable wheel delivery.

DCI2 terminal implementation checkpoint: the isolated Nox session, fail-closed
reporter, three-host workflow, ARM scanner pins and renewed eight-runner signed
capsule are locally verified. Full tests and strict checks pass. DCI3 hosted
qualification and DCI4 publication remain; no hosted result is claimed.

## DCI3/DCI4 hosted qualification and publication — 3 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns the existing
`/Users/doughnut/Documents/tobac` checkout and `codex/dci2-implementation`
branch. Scope: run the advisory fixture matrix, read-only hosted checks and
receipts, then guarded DCI4 publication. Native scope: no changes; the signed
lineage capsule is verified. Next: submit the exact candidate to hosted checks.

DCI3 result: all three advisory jobs passed on source `4b6dbf18`; downloaded
artifacts verified their source/report hashes, fixture exits and native scanner
execution. Receipt: `integration/advisory_typing_qualification_20261103.json`.
Next: test this metadata-only reconciliation head and guarded DCI4 publication.


## DCI4 guarded publication and reconciliation — 3 November 2026

The same chat owns the metadata closeout in `/Users/doughnut/Documents/tobac`,
branch `codex/dci4-closeout-20261103`; native scope is read-only. The exact
source candidate `672894f70bebd4ba17ba38fe8116c938ad13fe4f` passed 28 hosted
checks, with two conditional skips. All three advisory hosts passed again in
run 41623880425. PR #118 was published using a non-force fast-forward after
verifying expected main `afec3a48ce7bae14f9602c48d6c30a8b3f8dab29`. GitHub
readback confirmed source commit `672894f70bebd4ba17ba38fe8116c938ad13fe4f`
and tree `b80bc11653d601ce8892a9d617132147f8059163`, identical to the local
qualified tree. This closeout records the completed source publication; its own
metadata commit still requires guarded publication. ARM evidence covers static
diagnostics and scanner execution, not ARM scientific reproduction.


## Receiving-main hosted verification — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns the Conductor-only
reconciliation in `/Users/doughnut/Documents/tobac`, branch
`codex/receiving-checks-20261105`; scope is `conductor/status.md` and this
handoff. Native scope is read-only; no native operation is active. Receiving
main `927bfdaacc49421456da0f94dc661fd4ec245579` has nine successful push
workflows, including Linux and Windows reproduction and every engineering job.
Next operation: validate and commit this evidence update. Earlier assignments
above remain historical.


## Hosted macOS runtime renewal — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/receiving-checks-20261105`.
Scope: hosted verifier runtime profiles, signed digest-only capsule, preserved
prior generation, focused tests, publication inventory and Conductor handoff.
Native scope: read-only reopening of the eight accepted attempts before signing;
the signing key and original bytes remain in their existing private estate.
Next: issue a fresh generation, verify it and rerun the hosted qualification.
Two actual macOS Python 3.15.1/OpenSSH combinations passed signature and tamper
controls in PR #122; the old profile rejected the new OpenSSH binary before work.

Runtime renewal checkpoint: local full tests, strict checks and committed-source
reproduction passed. Hosted source `3695fd64441c884553ef158a4023df2f82fb0f08`
passed 28 executable checks, with two conditional skips. Quality job 127027899235
verified the signed inputs using the newly observed OpenSSH hash; both original
profile-probe combinations passed positive and tamper controls. The setup-python
combination's complete signed-input check on the new image was not separately
observed. Next: qualify this metadata closeout, then guarded publication and
receiving-ref readback.


## Receiving-main evidence reconciliation — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/post-publication-evidence-20261105`.
Scope: hosted run readback and `conductor/status.md` plus this handoff. Native
scope: read-only; no native operation is active. Next: record exact outcomes for
receiving commit `c30cae8d1f37b7335ed8f18dd0383324d625899f` as jobs complete.

Receiving-main terminal evidence: all nine push workflows at `c30cae8` passed,
including Linux and Windows reproduction and every engineering job. Voiage
parity job 127035471814 passed signed-input verification using the new OpenSSH
binary. The other setup-python/Python-build combination with that binary has
probe evidence only; its full check on that particular image was not observed.
The Conductor-only evidence update is local pending any future publication.


## Receiving-main hosted evidence — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/hosted-main-evidence-20261105`.
Scope: read-only hosted status and `conductor/status.md` plus this handoff.
Native scope: none. Next: record actual outcomes for receiving commit
`669eb8851b89eef91b3b014787639fb2765768ef`; preserve prior assignments.

Terminal readback: all nine workflows at `669eb8851b89eef91b3b014787639fb2765768ef`
passed. Both reproduction jobs and all engineering jobs report success. The
Conductor-only evidence update is local pending any future publication.


## Receiving-main verification — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/post-publish-097c7a1`. Scope:
read-only hosted checks, `conductor/status.md` and this handoff. Native scope:
none. Next: record outcomes for receiving commit
`097c7a1130f2c2eb2a53b0ef1559ace9811e9c58` as jobs complete.

Terminal readback: all nine workflows at `097c7a1130f2c2eb2a53b0ef1559ace9811e9c58`
passed, including scientific reproduction and engineering qualification. The
Conductor-only evidence update is local pending any future publication.


## Receiving-main checks at `50a348a` — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/verify-50a348a`. Scope:
read-only hosted checks, `conductor/status.md` and this handoff. Native scope:
none. Next: record outcomes for receiving commit
`50a348a2d96e541c7c87dedc5f181aff8a22696f` as jobs complete.

Terminal readback: all nine workflows at `50a348a2d96e541c7c87dedc5f181aff8a22696f`
passed, including scientific reproduction and engineering qualification. The
Conductor-only evidence update is local pending any future publication.


## Receiving-main checks at `1759fe7` — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/verify-1759fe7`. Scope:
read-only hosted checks, `conductor/status.md` and this handoff. Native scope:
none. Next: record outcomes for receiving commit
`1759fe7176a26a78dc4a878f236da48a3d5da5af` as jobs complete.

Terminal readback: all nine workflows at `1759fe7176a26a78dc4a878f236da48a3d5da5af`
passed, including scientific reproduction and engineering qualification. The
Conductor-only evidence update is local pending any future publication.

## Receiving-main checks at `135487e` — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/verify-135487e`. Scope:
read-only hosted checks, `conductor/status.md` and this handoff. Native scope:
none. Next: record outcomes for receiving commit
`135487ea288298e43d5592eda08a7ecbf3e90f0b` as jobs complete.

Terminal readback: all nine workflows at `135487ea288298e43d5592eda08a7ecbf3e90f0b`
passed, including scientific reproduction and engineering qualification. The
Conductor-only evidence update is local pending any future publication.

## Dependency failure reconciliation at `218baf0` — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/dependency-reconcile-218baf0`.
Scope: current dependency PR readback and Conductor status; native scope: none.
PR #128 was published by non-force fast-forward from `135487e` to `218baf0`;
GitHub ref and tree readbacks matched. The local #94 candidate lives in its own
worktree and remains unpromoted. All nine receiving-main push workflows at
`218baf09763b211e0849cab5ed15d4553b350942` passed; run IDs and qualification
scope are recorded in Conductor. This evidence update remains local.

## Receiving-main checks at `bf77c6b` — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/verify-bf77c6b`. Scope:
read-only hosted checks, `conductor/status.md` and this handoff. Native scope:
none. Next: record outcomes for receiving commit
`bf77c6b9ac8d36396bbd12713cfc299c8f6735f7` as jobs complete.

Terminal readback: all nine workflows at `bf77c6b9ac8d36396bbd12713cfc299c8f6735f7`
passed, including scientific reproduction and every engineering job. The
Conductor evidence update is local pending any future publication.

## PR #130 publication check handoff — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/pr130-check-handoff`. Scope:
record publication-check readback; native scope: none. PR #130 was published
by guarded non-force fast-forward to `7d24f608803e73cfc910bc766d7e8fcf444d741e`;
GitHub ref and tree readbacks matched. All five protected-branch checks passed.
The non-required Voiage parity job's scientific comparisons passed, but its
artifact export failed after the pinned Actionlint download returned HTTP 504;
the one bounded retry reproduced this failure. The original and retry are
https://github.com/edithatogo/tobac/actions/runs/41997837879/job/127145307902
and https://github.com/edithatogo/tobac/actions/runs/41997837879/job/127149778602.
The numerical and required macOS retries passed. Push-event workflows for the
new receiving commit were still queued or running at handoff. This handoff is local.

## Hosted recovery and scientific adequacy review — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/pr130-check-handoff`. Scope:
hosted check recovery, bounded scientific review and Conductor status; native
scope: no mutations. The Actionlint 1.7.12 Linux archive's exact qualified hash
was independently verified after the upstream 504; Linux audit and both package
portability jobs passed on their first retry. PR #130's Voiage parity job passed
on attempt 3 after the route recovered; prior failed attempts remain visible.
A local bounded review is retained under `outputs/research-audit-20261105/`;
it does not establish empirical adequacy or independent peer review. Next:
record terminal receiving-main workflow outcomes.

Terminal readback: all nine receiving-main workflows for
`7d24f608803e73cfc910bc766d7e8fcf444d741e` passed. Engineering qualification
passed on its targeted second attempt after its original Actionlint 504.
Conductor contains the hosted and bounded-scientific review status; this
update remains local pending any future publication.

## Repository discovery and Scorecard — 5 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/repository-scorecard`.
Scope: public repository discovery metadata, README, citation, Scorecard workflow,
publication inventory and status; native scope: exact GitHub repository metadata.
Next: prepare a narrowly scoped, independently qualified candidate on top of the
Conductor publication branch. Scientific models and private data remain unchanged.

## PR #94 current qualification — 6 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/pr94-current`. Scope: exact
previously generated ecosystem lock and receipt on PR #94 head `f73c031`.
Source receipt verification passes. The same candidate hash-installed in the
isolated Python 3.15.1 worktree and passed 1,225 tests with 20 skips; reuse that
unchanged result. The candidate also updates dateutil and typing-inspection.
Next: qualify current PR hosted checks before guarded publication. Native scope:
no mutations. PR #132 receiving ref/tree is `b57b4e1`; all ten push workflows
passed and Scorecard API reports that exact commit, score 7/10.

## Polars verifier preparation — 6 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns
`/Users/doughnut/Documents/tobac`, branch `codex/polars-longitudinal`.
Scope: `scripts/verify_empirical_longitudinal.py` conversion from pandas to Polars;
#94 remains frozen at `adb3f81` while hosted qualification runs. Native scope:
no mutations. Ruff passes; the existing focused verifier tests are running.
Full runner migration and scientific-lineage renewal remain required before
publishing this source change.

## Phase 0 integration readback — 6 November 2026

The NZ/AU empirical handoff at `1c07e4c` was read without modifying its worktree.
No terminal qualified Polars conversion commit exists. This checkout retains its
dirty verifier and coordination file. The focused Polars verifier tests pass:
8 passed in 29.92 seconds on repository-local Python 3.15.1 under the resource
guard, sampled peak 326.9 MiB. Log: `outputs/polars-verifier-20261106/focused.log`.
The source is not yet admitted by renewed native lineage. Remaining pandas
runners and legacy dependencies still require conversion and output parity.

The wrapper's inventory mismatch is expected. Renew acceptance only for a frozen
integrated snapshot through the existing owner native route with signatures and
negative controls; the other lane's moving dirty tree is not a signing target.
Existing owner environment/signing paths are retained; no private bytes were
copied, displayed or changed. No empirical-lane files or native objects were mutated.

## Frozen Polars source packet — 6 November 2026

Chat `01a19a6e-2e47-7b10-8a35-4e7d7fedb965` owns the root checkout on
`codex/polars-longitudinal`: both longitudinal runners, their verifier and two
runner test modules. The source packet replaces dataframe operations only;
NumPy/SciPy models, inputs, seeds and scientific assumptions are unchanged.
Full-size baseline/Polars runs (8,192 draws each) agree across all 21 CSV tables
at rtol/atol 1e-12; all 16 PNG/SVG figures are byte-identical. Release exports
retain 12-significant-digit formatting, empty missing cells, sorted grouping
and stable selection ties. Empirical boolean CSV spelling changes case only.
Missing source conventions/identities are rejected explicitly because Polars
reductions otherwise ignore nulls. Evidence: `outputs/polars-migration-20261106/`.
Ruff passes; selected BasedPyright reports zero errors (334 existing/interface
warnings). Focused baseline: 81 pass/one migrated-test API failure; failure-only
rerun: one pass; three new null controls pass. No full-suite/native acceptance
claim is made for this source packet. Inventory/capsule renewal must use the
integrated frozen snapshot, including the empirical lane's optional wrapper.

PR #94 was received as merge `e1d9b8848ab261f0ed992a74b3a2750e980512aa`;
GitHub tree `0c209ae2756257a78d47836da024b489db5a919b` exactly matches
qualified head `adb3f81`. All 29 executed checks passed, with two conditional
skips and the separate neutral Scorecard bot result. Current main contains the
merge. This lane did not repeat an already-completed publication.

Storage recovery preserved the inactive `.nox/strict_all` environment at
`/Volumes/PortableSSD/tobac-strict-all-preserved-20261106`; no source, evidence,
private binding or another lane's environment was removed or replaced.

Terminal source qualification: the final focused selection passes 85 tests in
21.85 seconds. Full replay's maximum parsed numerical difference is zero; five
cells differ only in float spelling, besides boolean letter case. All 16 figure
files remain byte-identical. No scientific calculation module was modified.
