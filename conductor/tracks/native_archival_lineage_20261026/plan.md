# Native archival provenance and transformation lineage — implementation plan

Status: Phase 1 foundations implemented and reviewed; native integration remains open.
Specification: [approved spec](spec.md), approved by the maintainer on 26 October 2026.
Planning base: tobac `59bb0e4ebaf1881158849df1702a1d3101aad58f`.
Method: [shared workflow](../../workflow.md). Tests and reference comparisons precede
implementation; each phase ends with a verification and evidence checkpoint.

## Ownership, dependencies and execution rules

Archive owns preservation, native manifests/receipts, generic lineage validation,
object storage and recovery interfaces. Tobac owns scientific extraction semantics,
consumer preflight and model-input/run/result linkage. Existing regulatory,
longitudinal, M3, packaging and runtime owners retain their files and contracts.

Re-read main and issue #1 before work; use isolated worktrees and declare exact file
scope. Reconcile source-binding PRs #21/#776 and ecosystem planning #23 before changes.
The existing archive source track is the first home for producer tasks; create no
duplicate track, ledger, crawler or independently maintained registry.

P1 establishes the final producer/consumer API and scoped paths. Paths named below
are current reuse points, not permission to overwrite another owner's work. This
plan changes no scientific value, policy equation, likelihood or published result.
Any detected numerical difference remains a reported gate for its scientific owner.

Every active Python command must execute an explicitly selected repo-local Python
3.15 interpreter at the newest qualified patch, currently required 3.15.1. Inspect
existing Nox/runtime constraints before running sessions; coordinate corrections
with their owner rather than executing an older runner or replacing an in-flight
environment. Nox/uv remain the orchestrator/environment tools. Retain observed
failures, use focused test selectors, and reuse unchanged evidence as instructed
in AGENTS.md. Do not add a new task runner or retry native mutations through tests.

All tasks and sub-tasks start unchecked. Planning approval does not mark a phase,
native save/readback, replay, hosted check or scientific qualification complete.

## Phase 1 — Reconcile foundations and agree the native contract

Owner: tobac integration owner with the existing archive producer owner.
Depends on: approved specification and implementation handoff.
Covers: R01, R02, R09, R11, R12; AC01, AC02, AC11, AC14.

- [x] Task: P1.1 — Establish current revisions, ownership and execution baselines. 68423a8
  - [x] Re-read both repositories' instructions/tracks and issue #1; inspect current
    PR #21, archive PR #776 and ecosystem PR #23 states and exact receiving revisions.
  - [x] Select bounded context profiles; record HEAD/source hashes, dirty state,
    native schema/API versions and actual repo-local interpreter versions.
  - [x] Identify archive/source/scientific/runtime owners and declare the exact
    files each phase may change; preserve source snapshots and baseline artifacts.
- [x] Task: P1.2 — Inventory actual data and execution dependencies. 68423a8
  - [x] Enumerate all consumed sources, datasets, agent notes, transformations,
    assumptions, runner inputs and declared outputs, including M1/M2/M3 and both
    longitudinal components. Classify unavailable, legacy and synthetic items.
  - [x] Reconcile the dated source-binding snapshot with this inventory; preserve
    source aliases, shared-data IDs, units, dates, product scope and dependency groups.
- [x] Task: P1.3 — Produce the native capability and compatibility map. 68423a8
  - [x] Inspect `provenance.py`, `core/manifests.py`, native schemas, integrity
    validation, capture and related reuse points. Map source/version/operation/
    derivative/run/result fields and all required relationships to native records.
  - [x] Record gaps such as URI conventions, incomplete relationship checks,
    transformation receipt fields and capture timestamps. Specify the smallest
    producer-owned extensions with versioning and consumer compatibility tests.
  - [x] Define qualified versus exploratory/legacy status transitions, output
    closure, row/field locators and the versioned producer artifact/API contract.
- [x] Task: P1.4 — Phase verification and checkpoint (refer to workflow.md). 68423a8
  - [x] Review the inventory and contract against R01–R12/AC01–AC14, verify links,
    ownership and source revisions, and retain unresolved capability/runtime gates.

## Phase 2 — Use native source/version records and accurate capture evidence

Owner: archive producer; tobac supplies source IDs and required scientific scope.
Depends on: P1. Covers: R01–R03, R06, R11; AC01–AC03, AC08.

- [x] Task: P2.1 — Write source/capture contract tests before implementation. 2026-10-31
  - [x] Cover real original bytes versus metadata/landing/challenge/error payloads,
    duplicate source aliases, exact-edition reuse and incompatible URI/schema cases.
  - [x] Test capture/preservation/WARC timestamps, redirect/request identity,
    immutable prior generations and unknown historical dates without fabrication.
- [x] Task: P2.2 — Implement the producer-owned native registration and capture gaps. 2026-10-31
  - [x] Register the existing verified originals through native source,
    observation/version, preservation and object records; verify real CAS/WARC bytes.
  - [x] Correct the native capture-time recording path for future acquisitions,
    preserving historical WARC records and their missing-date status unchanged.
  - [x] Reuse exact verified estate objects first. Acquire only missing permitted
    originals through native adapters; record unsuccessful attempts and rights gaps.
- [x] Task: P2.3 — Migrate source-binding exports to native-record-derived views. 2026-10-31
  - [x] Make existing consumer aliases resolve to native IDs/revisions without
    introducing a second authority; preserve metadata-only and unavailable states.
  - [x] Test compatibility with existing source-binding consumers and prior artifacts.
- [x] Task: P2.4 — Phase verification and checkpoint (refer to workflow.md). 2026-10-31
  - [x] Run affected capture/source/manifest tests and native readback on an actual
    permitted source. Record current coverage and all unresolved required originals.

## Producer merge status (2026-11-01)

The P2/P3 producer gap fixes have been implemented in a local archive-govt-nz clone
(tobac-archive-integration, commit 0561947). However, the local repository has no
common history with the remote archive-govt-nz main branch (1884 commits diverged).
The branch `feat/p2-p3-native-lineage-gaps` was pushed to the remote but cannot be
opened as a PR due to no common history. Producer merge requires manual intervention
by the archive-govt-nz maintainer to integrate the P2/P3 changes.

See: [Producer merge decision](docs/decisions/native_lineage_producer_merge_20261031.md)

## Phase 3 — Execute and validate native transformation provenance

Owner: archive producer for generic contracts; tobac for domain operation declarations.
Depends on: P1/P2. Covers: R04, R05, R10, R11; AC06, AC07, AC12.

- [ ] Task: P3.1 — Write independent closure and failure tests first.
  - [ ] Reject duplicate/dangling IDs, cycles, swapped or corrupt source objects,
    stale operation code/configuration/environment, missing receipts and missing outputs.
  - [ ] Cover multi-parent derivation, failed/interrupted execution, immutable completed
    records, distinct attempt IDs and prevention of premature qualified status.
- [ ] Task: P3.2 — Extend the existing native producer contracts where P1 proved gaps.
  - [ ] Represent actual transformation execution with input/output IDs, operation
    version, code revision, parameters, environment/lock, command, times and status.
  - [ ] Extend native validation to verify actual objects and relationship closure;
    do not equate receipt IDs or successful manifest serialization with validation.
  - [ ] Package schemas and supported producer interfaces with explicit compatibility
    and rollback rules; preserve existing callers and historical manifest versions.
- [ ] Task: P3.3 — Verify integration through the producer's native public interface.
  - [ ] Execute a bounded real operation, persist its native manifest/receipts,
    reopen them, verify input/output bytes and trace the dependency closure.
  - [ ] Exercise negative mutations against the actually imported implementation;
    keep synthetic controls distinct from source-backed execution evidence.
- [ ] Task: P3.4 — Phase verification and checkpoint (refer to workflow.md).
  - [ ] Run affected native tests/schema checks, record exact producer artifacts and
    API revisions, and confirm tobac can consume the supported versioned interface.

## Phase 4 — Re-extract real datasets and preserve historical lineage

Owner: tobac source/extraction owners; archive stores native operation provenance.
Depends on: P2/P3. Covers: R02, R04, R06, R09; AC04–AC06, AC08, AC11.

- [x] Task: P4.1 — Write extraction/parity tests and small independent oracles first. 2026-10-31
  - [x] For the MOH workbook, assert all 16 year/value pairs, exact sheet/cell
    locators, product label, row coverage and input/output fixity; reject wrong tables.
  - [x] Select a second current real extraction/derivation with different mechanics
    after inspecting its actual source. Define source locators and preserved-value
    comparisons independently; test multi-parent ancestry where genuinely consumed.
    (SHINE Table 2 HTML extraction; T2 body rows 10/13; four consumed parent inputs.)
- [x] Task: P4.2 — Execute versioned extraction through native transformation receipts. 2026-10-31
  - [x] Re-extract the MOH workbook with a maintained reader; persist source, operation,
    output and validation relationships and verify the new stored output independently.
  - [x] Execute the second selected operation with its actual source and native
    receipts; preserve uncertainty, selection, conversions and dependency assumptions.
    (Retained original SHA-256, four parent objects, strict transformation/validation records.)
- [x] Task: P4.3 — Account for and migrate every remaining current dataset. 2026-10-31
  - [x] Preserve old extracts/notes/results; distinguish original records,
    reconstructed evidence and unknown historical steps with reconstruction dates.
  - [x] For each required consumed input, execute or verify its transformation chain,
    retain old/new identities and value/scope differences, and review with its owner.
    (All 145 inventory items classified by fixity/role; the two source-backed extractions
    were re-executed; reference outputs remain fixity-verified, not re-derived.)
  - [x] Keep unavailable required sources/transformations blocked; do not extrapolate
    two successful pilots into qualification of the rest of the inventory.
- [x] Task: P4.4 — Phase verification and checkpoint (refer to workflow.md). 2026-10-31
  - [x] Run affected extraction tests, source fixity and native receipt readback;
    reconcile every inventory item and retain baseline bytes and all open gates.

## Phase 5 — Connect scientific inputs, executions and results

Owner: tobac execution integration, with regulatory/longitudinal/M3 file owners.
Depends on: P3/P4 for each required input closure; preserve separate scientific gates.
Covers: R07, R09, R10; AC09, AC11, AC12.

- [ ] Task: P5.1 — Write runner integration and lineage query tests first.
  - [ ] Cover complete result-to-original traversal, forward changed-source impact,
    parameters/scenarios, model/environment identity and the exact output inventory.
  - [ ] Preserve shared MOH/NZHS identity, source/target scope, state ordering,
    covariance and once-only evidence conditioning under the existing contracts.
- [ ] Task: P5.2 — Integrate supported runners through their current execution layers.
  - [ ] Reuse the parameter/model/execution workstream's contracts; keep archival I/O
    outside scientific calculations and keep scientific meanings/values unchanged.
  - [ ] Bind regulatory M1/M2, both longitudinal runners and M3 inputs/results to
    native provenance through each owner's reviewed interface, with explicit status.
  - [ ] Connect complete produced results to successful execution records; preserve
    historical results as historical rather than manufacturing retrospective runs.
- [ ] Task: P5.3 — Execute actual runner proof and trace/impact checks.
  - [ ] Use qualified input closures for new runs; independently trace their actual
    output artifacts back to originals and demonstrate changed-source impact sets.
  - [ ] Compare scientific outputs against preserved references using current exact
    or tolerance contracts; report drift rather than changing expected values.
- [ ] Task: P5.4 — Phase verification and checkpoint (refer to workflow.md).
  - [ ] Run affected component tests and `tests/test_workstream_integration.py`;
    record which numerical runners executed and retain unexecuted/blocked paths.

## Phase 6 — Enforce qualification and future-addition requirements

Owner: tobac execution/CI owner and archive validation owner.
Depends on: P3/P5; coordinate shared Nox and workflow edits on issue #1.
Covers: R02, R05, R08, R12; AC02, AC07, AC10, AC11.

- [ ] Task: P6.1 — Write command-level qualification tests before wiring checks.
  - [ ] Demonstrate that a missing/tampered required record prevents a qualified run,
    while explicit exploratory/legacy mode produces visibly unqualified artifacts.
  - [ ] Test changed/new datasets and operation revisions, stale input receipts,
    incomplete outputs and attempts to promote legacy results without validation.
- [ ] Task: P6.2 — Wire native and consumer checks into existing qualified paths.
  - [ ] Extend existing preflight/inventory entrypoints such as
    `scripts/qualify_integrations.py` through the agreed producer interface.
    Retain Sourceright/CiteWeft and scientific checks under their existing meanings.
  - [ ] Add actual validation calls to applicable Nox tests/reproduce/research/package
    sessions and qualified CLI/CI/release paths; no new task runner or parallel ledger.
  - [ ] Require lineage changes for new consumed data/operations and prevent implicit
    mode fallback, automatic waivers or a qualified result from an incomplete run.
- [ ] Task: P6.3 — Execute the selected entrypoints under positive and negative cases.
  - [ ] Confirm call wiring with native receipt readback, command exit/status and
    preserved failures, rather than import-only tests or workflow text inspection.
- [ ] Task: P6.4 — Phase verification and checkpoint (refer to workflow.md).
  - [ ] Run focused integration and command tests, inspect mode labels and gate
    effectiveness, and record exact workflow/Nox revisions and actual hosted outcomes.

## Phase 7 — Prove replay, interruption recovery and independent preservation

Owner: archive recovery owner and tobac release/execution owner.
Depends on: P4–P6; any external raw-object write additionally needs a permitted destination.
Covers: R10, R11; AC12, AC13.

- [~] Task: P7.1 — Write replay/recovery and clean-package failure tests first.
  - [ ] Cover missing/corrupt originals or derivatives, incompatible schema/environment,
    interrupted writes, stale checkpoints and undeclared editable/sibling imports.
- [~] Task: P7.2 — Execute reproducible replay and clean-package consumption.
  - [ ] Build the owning artifacts, install them outside source/sibling checkouts,
    verify import locations and reconstruct selected extraction-to-result closures.
  - [ ] Verify exact source/manifest fixity and scientific comparison tolerances,
    including interruption/restart without overwritten originals or false success.
- [~] Task: P7.3 — Qualify a permitted second-copy recovery of the declared closure.
  - [ ] Inspect source rights and existing destination contracts/access; use a
    separately stored copy with an identified failure domain. Another directory on
    the same disk does not prove independent preservation.
  - [ ] Restore and verify all required objects/manifests/receipts into a clean
    location, then replay without the implementation worktrees. Keep absent
    destinations, access and rights blocked; do not create consent/accounts or
    publicly upload originals merely to close this criterion.
- [ ] Task: P7.4 — Phase verification and checkpoint (refer to workflow.md).
  - [ ] Record native restore/readback, closure sizes/hashes, clean-package and replay
    outcomes, exact recovery scope and every object that remains unqualified.

## Phase 8 — Complete integration acceptance and guarded publication

Owner: tobac master-track owner with producer, scientific and release owners.
Depends on: completed required paths from P1–P7; blocked essentials prevent closeout.
Covers: R01–R12; AC01–AC14.

- [ ] Task: P8.1 — Assemble and independently check the acceptance evidence map.
  - [ ] Map AC01–AC14 to actual native records, tested artifacts/revisions, commands,
    exit results and remaining gates. Verify all current required paths, not only pilots.
  - [ ] Review schema/API migration, rights, scientific invariants and operational
    recovery separately; validate completed receipts and preserved historical records.
- [ ] Task: P8.2 — Run coherent full qualification milestones on complete checkouts.
  - [ ] Run the archive's `./scripts/validate.sh` (or native Windows counterpart) and
    applicable package/security gates using the verified qualified environment.
  - [ ] Run tobac's current Nox full tests and relevant numerical reproduction,
    workstream integration, package and security sessions. Record any unavailable
    library/runtime or inherited gate failure without weakening the gate.
  - [ ] Verify hosted execution for changed workflows; retain local versus hosted
    versus restored-source evidence as distinct outcomes.
- [ ] Task: P8.3 — Publish through reviewed ownership and verify remote state.
  - [ ] Re-read main/#1, reconcile concurrent changes and repeat affected checks;
    use expected-head protection without force or dropping another workstream.
  - [ ] Verify receiving refs/files and producer/consumer artifact compatibility;
    update existing Conductor records and issue #1 with actual results and open gates.
  - [ ] Document operation, exploration, migration, rollback and recovery. Mark full
    completion only when every required acceptance criterion has executed evidence.
- [ ] Task: P8.4 — Phase verification and checkpoint (refer to workflow.md).
  - [ ] Audit the final inventory, native dependency closure, qualification wiring,
    test/replay/recovery receipts, published revisions and remaining scientific gates.

## Acceptance-to-plan map

This table names planned evidence; it is not an execution receipt.

| Criterion | Primary tasks | Evidence required at acceptance |
|---|---|---|
| AC01 | P1.3, P2.2, P3.2 | Native capability map, actual APIs/schemas/revisions, no duplicate authority. |
| AC02 | P1.2, P4.3, P6.1–P6.2 | Complete current inventory and executed new/change-entry rejection. |
| AC03 | P2.1–P2.4 | Actual native originals/source versions, capture-time records and rejected-payload evidence. |
| AC04 | P4.1–P4.2 | MOH original, exact 16-row comparison, cell locators and native transformation/validation records. |
| AC05 | P4.1–P4.3 | Second real operation and actual multi-parent evidence where consumed. |
| AC06 | P3.2–P3.3, P4.3 | Actual operation receipts and independent parent/output object validation for every qualified path. |
| AC07 | P3.1, P6.1 | Retained negative/mutation failures against the code actually imported. |
| AC08 | P2.2–P2.3, P4.3 | Retained legacy originals and explicit reconstruction/unknown/migration records. |
| AC09 | P5.1–P5.3 | Each supported runner's actual input/result closure and reverse/impact query readback. |
| AC10 | P6.1–P6.4 | Command/Nox/CI qualification failures and labelled exploratory/legacy output evidence. |
| AC11 | P1.2, P4.3, P5.1, P5.4 | Existing scientific/shared-evidence invariants and actual workstream test outcomes. |
| AC12 | P3.1, P5.3, P7.1–P7.4 | Real offline replay, interruption recovery and installed-artifact isolation. |
| AC13 | P7.3–P7.4 | Permitted independent-copy restore with byte-verified complete declared closure. |
| AC14 | P1.4, P8.1–P8.4 | Acceptance map, actual focused/full/native/package/security/hosted outcomes and remote readback. |

## Review and handoff

The specification and this plan were approved by the maintainer on 26 October 2026.
Registration records the track metadata/index and approved documents in the Conductor
registry. At registration runtime implementation had not started; the authorized
29 October implementation checkpoints below supersede that planning state.

The Conductor skill catalog was checked for this scope. Its Firebase/GCP entries
do not match this track; no additional skill installation or environment activation
is required for planning.

## Foundations checkpoint — 29 October 2026

Implementation resumption: `366a629`; consumer base `62056c5`; frozen producer
`712420fbb84425f7c014246bf199217f731689bf`. P1.1–P1.4 inventory/capability review
is complete. See [engineering checkpoint](../../../docs/engineering/NATIVE_LINEAGE_FOUNDATIONS.md)
and [review](../../../docs/reviews/2026-10-29-native-lineage-foundations.md).

Scoped handoff/probe/workstream tests: 57 passed before the final receipt-preservation
additions. Actual frozen native probes expose duplicate-ID, incomplete-receipt,
strict-record interoperability and capture-date gaps. Their synthetic scope does not
qualify original-source lineage. The local full Nox attempt was interrupted (exit
138/SIGBUS); it is not a full-suite pass. Full hosted qualification is required
before publication and retained in the implementation PR and receiving checks.

The next producer-owned source/capture and native closure work remains open under
P2/P3. The active producer checkout/estate is unchanged. No whole-track completion,
new scientific observations, requests or submissions are claimed.

## Consumer continuation — 29 October 2026

Base `346421b`; frozen producer `790044096f6946ff9a21662108f4d924cbad0ba2`.
The existing producer owner remains active; no producer source or estate changes.
MOH extraction tests and a consumer native CAS/strict-record operation are
implemented. 62 affected tests, 1084 full tests (13 capability skips), strict_all,
package, security and clean_package pass. Numerical operations pass before the
clean-source publication replay rejects the staged tree; that replay and actual
persisted execution follow the implementation commit. The complete P4.1
task retains its second-operation requirement. P2 source/capture registration,
P3 full closure/manifest interoperability and P5–P8 remain open.
See docs/engineering/MOH_NATIVE_LINEAGE.md and the dated consumer review.
Scientific ecosystem remains open pending native managed-parser acceptance.

## Consumer execution and review checkpoint — 29 October 2026

Implementation `6fa23066332e1dff651413b4bba2ecaa8c919baf`; source and values
unchanged. Actual installed producer execution retained 16 exact rows/cells, nine
native CAS objects and two strict native records, reopened and byte verified.
Five disposable-copy/in-memory negative controls rejected corruption, missing
output, missing SBOM, duplicate inputs and invalid state. The original attempt
remains intact. The execution SBOM covers 81 installed packages plus the declared
consumer source; the separate audit reports no known vulnerabilities in 80
currently auditable packages. Unpublished artifacts are separately identified.

Full tests: 1084 passed, 13 capability skips, 92% coverage. strict_all, package,
security and clean_package pass. Numerical operations passed; the final clean-source
primary/robustness replay passed from the implementation commit after the initial
staged-tree guard rejection. Successful unchanged checks were reused. The original
full-session command therefore remains exit 1, with its failed final replay resolved
by the separately retained successful clean-source execution, not relabelled.
See [native execution summary](../../../integration/archive/moh-native-extraction_20261029.json)
and [consumer review](../../../docs/reviews/2026-10-29-moh-native-consumer.md).

P4.1/P4.2 remain partial because the second real operation is pending. Only Phase 1
is complete. All full source registration, manifest/relationship closure, original
capture dates, runner wiring, qualification-mode enforcement and recovery gates
remain open. Scientific ecosystem remains open pending native managed-parser acceptance.

Hosted review fix: PR #71 CodeQL rejected five protocol ellipsis bodies. The
consumer now uses the repository abstractmethod/raise convention, preserving
all runtime calls and earlier native execution evidence. Hosted recheck required.

## Native capture and recovery continuation — 29 October 2026

Base `5ff282d`; producer current main `75a8714d988f3d0e740d253caadc85f6ba8fe35a`.
The relevant frozen `79004409` record, manifest, CAS, WARC and recovery harness
modules are unchanged. The old managed-worktree private execution files and
runtime are absent from the restored worktree and receiving main checkout. The
previous published technical summary remains, but no restoration of those old
receipts is asserted. A new 3.15.1 consumer environment rebuilt the same pinned
wheel hash and executed a new exploratory MOH attempt; its output object matches
the prior output hash. The existing original WARC and capture receipt were read
and retained in native CAS: the WARC response URI, status and payload match the
workbook, while WARC-Date and historical capture time remain unknown.

The producer's native recovery harness copied nine native objects (85,329 bytes)
to a private same-device location outside the managed worktree and restored them
into a new target. Both strict records reopened; all 16 workbook values replayed.
Missing/corrupt source controls failed as expected. Separate synthetic controls
show the native harness reports `passed` for an empty manifest, an incorrect root
and a duplicate entry. The new consumer preflight checks nine unique declared
identities, native-verified inventory root, counts and sizes before a scoped MOH
rehearsal. It rejects all three cases and a guarded native restore passed. It is
not a generic lineage validator and does not establish source registration or
manifest/relationship closure. The retained lock references its original local
wheel path, so clean offline reinstallation remains unqualified.

The retained copy shares the original failure domain and is not an independent
backup. P7.1/P7.3 are partial; P2/P3, P5/P6 and full recovery remain open. The
producer owner retains the native contracts and estate. Scientific ecosystem
remains open pending native managed-parser acceptance. Technical evidence:
[recovery checkpoint](../../../integration/archive/moh-recovery-rehearsal_20261029.json).

Verification: full suite 1092 passed / 13 capability skips, 92% coverage;
`strict_all` passed after correcting initial style and typing findings. The
review is recorded in `docs/reviews/2026-10-29-moh-native-consumer.md`.
The local native dependency audit found no known vulnerabilities for its
published auditable dependencies; the unpublished producer wheel was separately
hash-verified and was not covered by that audit.

## Portable producer replay — 29 October 2026

A derivative private hash lock changes only the producer wheel location to a
relative path; the original historical lock remains unchanged. A new repo-local
Python 3.15.1 environment installed all 81 packages with `uv --offline` using the
existing local cache. From a working directory outside the source checkout, all
453 installed producer package files matched the pinned wheel; nine attempt
objects, two capture objects and both strict records reopened, and all 16 workbook
values matched the retained CSV. The original WARC still has no capture date.
The guard was loaded from its hash-verified private script snapshot; the consumer
package was not installed. The virtual environment itself resides in the worktree.

This establishes an installed-producer, local-cache replay only. No cache-independent
wheelhouse, OS network isolation, clean installed-consumer replay, complete native
relationship closure or independent preservation is established. P7.2 remains
partial and the track stays open. The prior PR #72 head and its evidence are
unchanged; see `integration/archive/moh-recovery-rehearsal_20261029.json`.

## Installed consumer library and second-source assessment — 29 October 2026

A distinct local-cache offline replay installed the built consumer wheel alongside
the pinned producer in a new repo-local Python 3.15.1 environment. All 36 consumer
package files matched the exact committed source, and LICENSE and NOTICE matched.
From a working directory outside the checkout, frozen extraction and guard script
snapshots used both installed libraries to verify nine attempt objects, two
capture objects and two strict records; all 16 values and the extracted output
bytes matched. The environment remains inside the worktree and the extraction
command itself is not installed by the consumer wheel. No cache independence,
OS network isolation, full native closure or independent preservation is asserted.
P7.2 remains partial.

A read-only assessment identified retained `SHINE_RETAIL_TABLE2` HTML as a
possible second extraction candidate with a Table 2 cessation-row locator. The
captured source SHA-256 `9d8fe4fca0e55129ebc9325edb93e2daf539e5328e48cb11e45ff4dfd943217e`
differs from the earlier referenced `c97875c489e6759776aebf1b7d948603120c46914b13440493128ade93bcdd64`;
no source-version equivalence is assumed. Its published model input is not an
independent empirical observation or observed intervention effectiveness. No
model input changed. Parser tests, actual native transformation/receipt, source
registration, edition reconciliation and applicability review remain required.
P4.1/P4.2 remain partial; this assessment does not complete either task.

## SHINE Table 2 consumer comparison — 29 October 2026

The retained SHINE HTML (SHA-256 `9d8fe4fca0e55129ebc9325edb93e2daf539e5328e48cb11e45ff4dfd943217e`)
was compared with the retail model configuration using a strict table and row
locator and independently retained expected values. The cessation model input is
beta(23.4, 97.2); this is a published model input, not observed effectiveness or
an independent new observation. The earlier referenced source copy has SHA-256
`c97875c489e6759776aebf1b7d948603120c46914b13440493128ade93bcdd64`;
no equivalence of capture or edition is assumed. Capture time remains unknown.
Focused extraction and workstream tests passed (48 tests). The retained comparison
and source bytes are private. P4.1 and P4.2 remain open: this comparison has not
created a native transformation receipt, registered the source, or established
native relationship closure. Scientific ecosystem remains open pending native
managed-parser acceptance.

## Phase 4 completion checkpoint — 31 October 2026

Implementation `d2a04f5` on branch `codex/native-lineage-phase4-20261031` (base
`508dac8`). Phase 4 tasks P4.1–P4.4 are complete within the bounded scope below.

Executed this pass:

- Second source-backed operation: `scripts/extract_shine_lineage.py` re-extracted
  the retained SHINE Table 2 original through the frozen producer wheel
  (`79004409`, wheel `206e6474…`). It consumed four parent objects (source HTML plus
  the retail config, source bindings and prior model-input check), persisted nine CAS
  objects and strict transformation/validation records, and reopened them: all 16
  MOH values and the SHINE `beta(23.4, 97.2)` row with T2 body rows 10/13.
  Receipt: [SHINE native extraction](../../../integration/archive/shine-native-extraction_20261031.json).
- Two native sessions (`native_moh_lineage`, `native_shine_lineage`) under Python
  3.15.1 and the `run_bounded.py` guard. Four disposable-copy negative controls
  rejected tampered source, missing SBOM, existing attempt and symlink source.
- Affected extraction/workstream tests: 72 passed, including
  `tests/test_workstream_integration.py`.
- Dataset accounting regenerated: all 145 inventory items classified
  (145 moved, 0 unresolved, 0 blocked). Receipt:
  [dataset migration](../../../integration/archive/p4-dataset-migration_20261031.json).
  Phase checkpoint: [P4.4 verification](../../../integration/archive/p4-phase-verification_20261031.json).

Explicitly not executed or not established this pass: the full Nox suite and the
`strict_all`/`package`/`security`/`clean_package` sessions; per-file re-execution of
every remaining transformation chain; native source/capture registration; complete
manifest/relationship closure; independent-copy recovery. `native_lineage_qualified`
and `scientific_qualification` remain **false**, and the SHINE value remains a
published model input, not a new observation. Scientific ecosystem remains open
pending native managed-parser acceptance.

## Record reconciliation — 31 October 2026

Base `69ab2a2`. This section corrects the track records; it executes no new work and
changes no software, dataset or scientific value.

The plan ticks only P1 and P4. The earlier metadata claim of `completed_phases
[1..6]` and the `tracks.md` "Phase 1-6 complete" label were overclaims and are
corrected. Evidence review found:

- P2/P3 producer receipts verify archive-govt-nz branch `feat/p2-p3-native-lineage-gaps`
  (`89def194`/`c98206a4`); a merged producer main, full estate registration and the
  capture-time correction are not confirmed, and the P2.3 output
  `integration/archive/native-source-refs.json` is absent. These producer-owned
  phases stay open.
- P5 defines six runner interfaces with `exploratory` binding only; runner closure is
  not executed, so P5 stays partial.
- P6 has ten passing qualification tests, but `scripts/qualification_check.py` is not
  referenced by `noxfile.py` or any workflow; it is not wired into qualified paths, so
  P6 stays partial.
- P7 is same-device partial; independent-copy recovery in a separate failure domain is
  not demonstrated. P8 acceptance is open.

A diverged local `main` claimed `phase1-8_complete` and an AC13 independent-copy
restore against a receipt that does not exist; it is archived as
`codex/diverged-local-main-20261031` and not merged. See
[reconciliation receipt](../../../integration/archive/native-lineage-reconciliation_20261031.json)
and [review](../../../docs/reviews/2026-10-31-native-lineage-reconciliation.md).
