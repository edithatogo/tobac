# Native archival provenance and transformation lineage

Status: Phase 1 foundations implemented/reviewed; native integration remains open.
Type: Feature. Date: 26 October 2026 (Australia/Brisbane).
Track ID: `native_archival_lineage_20261026`.
Planning base: tobac `59bb0e4ebaf1881158849df1702a1d3101aad58f`.

## Purpose and confirmed decisions

Use the existing archival system to trace a scientific result through its model
execution, input data, transformations and extraction to preserved original sources.
Cover every current dataset and transformation consumed by tobac, and apply the
same contracts to future additions. Provenance is necessary for qualification;
scientific applicability and approval remain additional requirements.

The maintainer selected:

1. Coverage through model inputs and results, including future additions.
2. Preservation of existing agent extracts, with reconstructed lineage and unknown
   historical steps labelled explicitly. Replacement requires verified extraction.
3. Valid lineage for qualified runs. Explicitly labelled exploratory and legacy
   runs remain available and cannot be counted as qualified runs.

The specification and implementation plan are approved, and the track is registered.
The maintainer authorised implementation on 29 October 2026; the producer owner
retains active files/operations. The Phase 1 checkpoint records actual scope and gaps.

## Existing work, dependencies and ownership

- Follow [product purpose](../../product.md), [workflow](../../workflow.md),
  [workstream ownership](../../../docs/WORKSTREAM_SYNC.md),
  [existing tracks](../../tracks.md) and the
  [library reuse review](../../../docs/engineering/LIBRARY_REUSE_REVIEW.md).
- Reconcile [tobac PR #21](https://github.com/edithatogo/tobac/pull/21) and
  [archive-govt-nz PR #776](https://github.com/edithatogo/archive-govt-nz/pull/776).
  They provide capture and source bindings; their existence does not establish
  native transformation integration or that either change is merged.
- The inspected archive planning base is
  `4487bd82118cdd122ff1c99b1fc0706c1ebc889c`; the capture draft head is
  `08340fd6e81ca73b2c68deb414dcb5d5b89272a9`. Recheck revisions before implementation.
- Archive-owned reuse points include `src/archive_govt_nz/provenance.py`
  (`build_manifest`, observations, objects, versions, derivatives, WARC records,
  transformation/validation/publication receipts), `core/manifests.py`, native
  CAS/WARC verification and existing schemas. Inspect related implementations
  before choosing the narrowest supported native integration.
- `archive-govt-nz` owns preservation and generic provenance capabilities. Needed
  generic validation enhancements belong there. Do not create another provenance
  engine, crawler, evidence ledger or independently maintained source registry.
- Tobac owns domain extraction semantics, transformations, parameters, scientific
  evidence identity, consumer validation and run/result linkage. Existing owners
  retain `src/tobac`, `src/tobac_supply`, M3 and their corresponding tests/results.
- Coordinate with [ecosystem planning PR #23](https://github.com/edithatogo/tobac/pull/23),
  particularly run identity and parameter/model/execution separation. Reuse those
  contracts and owners instead of duplicating runtime or engineering work.
- The master track lives in tobac. Reuse the existing archive source track for
  producer work where appropriate; register a further upstream track only after
  inspection establishes a distinct needed capability and no matching owner.

## Current evidence and gap

The first source-binding snapshot covers 43 bibliography entries, 38 source
identities, 18 CSVs with 326 rows and two supporting extraction notes. Native
storage verification covered 31 CAS objects and four WARC generations. The original
MOH tobacco-volume workbook matched all 16 annual values in the extracted CSV.
These are dated snapshot results from the draft receipts, not current acceptance
counts. Recompute the inventory against the actual implementation base.

The source-binding records are separate JSON registers. They do not yet form the
archive's native, validated source-to-derivative-to-run lineage. The existing
manifest builder validates some relationships and receipt identifiers, but that
does not establish complete transformation semantics, output closure or acyclic
dependencies. Historical extraction steps, some source editions and capture times
remain unknown. Existing `WARC-Date` omissions must remain visible.

## Functional requirements

### R01 — Native contract and capability mapping

Map every required source, object, observation, version, transformation,
validation, derivative and execution relationship to the archive's maintained
contracts. Record the producer API/schema revision and exact consumer interface.
Inspect schema/implementation mismatches, including source URI conventions,
before adopting a representation. Extend the owning native capability when a
required relationship or validation is missing; do not disguise a separate JSON
graph as native integration. Supplemental compatibility exports may be generated
from authoritative native records but cannot become another authority.

### R02 — Complete inventory and stable identity

Inventory current source references, primary objects, agent notes, extracted
tables, analytical inputs, transformation entrypoints and saved model outputs.
Account for each item as observed, derived, assumption, synthetic, legacy,
reconstructed, unavailable or otherwise explicitly qualified. Resolve actual
source locators and cross-repository references without inferring source receipt
from a URL, citation, catalogue hit or HTTP status. Preserve source aliases and
underlying-data identities across citations, products, editions and consumers.
Adding or changing an actively consumed dataset or transformation must require
corresponding lineage updates and validation.

### R03 — Original preservation and temporal provenance

Reuse verified estate objects where their exact revision, bytes and source edition
match the required use. Capture missing permitted originals through the native
route, preserving URLs, redirects/request identity, safe HTTP metadata, format,
content hashes, source version/edition and rights status. Keep source observation
period, publication/availability date, retrieval time, extraction time and generated
output revision distinct. Record actual new capture timestamps in native capture
and preservation records and WARC where required by the selected format.

Preserve previous captures unchanged. Label unavailable historical dates/editions
as unknown; neither a new current snapshot nor a filesystem timestamp recreates
the agent's original observation. Challenge/error/landing pages and metadata-only
records cannot satisfy a requirement for an original dataset or full document.

### R04 — Executed transformation provenance

Every qualified extraction or transformation must emit the archive's native
transformation receipt, tied to actual input and output object identities. Record
the operation and semantic version, code repository/commit and relevant source
hashes, command/entrypoint, parameters/configuration, implementation environment
and lock identity, actor/tool identity where available, execution start/end,
completion/exit status, validation results and output schema/content identities.

Represent selection, exclusions, missingness handling, joins, aggregation,
normalisation, unit/product conversion, rounding and analytical derivation as
explicit operations or documented steps of a versioned operation. Locate source
tables, sheets/cells, document sections and derived rows/fields at the finest
granularity justified by the extraction. Multi-source joins retain every parent;
an invented one-to-one mapping cannot replace a many-to-one derivation.

Human/agent transcription and manual edits retain their method and review evidence.
They cannot be retroactively described as an executed reproducible extraction.
Preserve exact byte hashes and, where needed, separately versioned logical-content
hashes; formatting tolerance never relaxes source fixity.

### R05 — Closed native lineage and independent validation

Native manifests must close over required source, version, derivative, receipt,
execution and output relationships. Validate unique IDs, referenced-object
existence and actual fixity, schema/API versions, parent and receipt links,
acyclic derivations and the complete declared output set. Detect swapped sources,
changed input bytes, altered transformation code/configuration, stale environments,
missing steps, incomplete executions and mismatched consumer outputs.

The validator must inspect actual records and objects, not only supplied hash
strings, file paths or a declaration that the native manifest builder succeeded.
Missing remote objects, incompatible native capabilities and unresolved essential
lineage remain explicit failed or blocked requirements.

### R06 — Legacy preservation and verified migration

Preserve current extracts, notes, source IDs and historical results. Distinguish
contemporaneously recorded provenance, later reconstruction and genuinely unknown
steps, with evidence and reconstruction time. Do not fabricate historical
execution receipts or relabel old outputs as newly qualified.

For each replacement, execute extraction from an identified original, compare
values, units, scope and row coverage with the preserved input, retain differences
and the actual comparison receipt, and require the applicable scientific review
before an input-value change. Maintain a recoverable link between old and new
revisions. Existing unchanged values are the baseline; this track does not grant
permission to alter a scientific parameter or expectation to make parity pass.

### R07 — Model input, execution and result lineage

Connect each required model input to its archive object/version and executed
transformation receipt. Model execution receipts must bind input lineage,
parameter/scenario identity, model implementation, environment, command,
precision/RNG details where applicable, status and all produced result artifacts.
Keep scientific calculations independent of archival I/O; the execution layer
performs provenance checks and receipt production.

Enable reverse tracing from a result to its complete dependency closure and forward
impact assessment from a changed source/transformation to affected inputs and
results. Do not claim unexecuted historical model runs were re-estimated or replayed.
Integrate each existing scientific runner under its current owner's contract.

### R08 — Qualification modes and enforcement

Qualified runs must validate the required native lineage before accepting inputs,
then bind successful execution and output validation before being marked qualified.
Qualified replay/package/release/CI paths must invoke this check; metadata files
present on disk and tests that merely import a validator do not establish wiring.

Exploratory and legacy execution must be explicit and visibly labelled in outputs
and receipts. Such runs may preserve useful results but cannot produce a qualified
status or satisfy a release/acceptance gate. No implicit fallback, automatic waiver,
silent promotion or global disabling of current scientific gates is permitted.
Provenance validity alone does not imply empirical applicability or scientific
approval; require both where the current scientific contract calls for them.

### R09 — Scientific meaning and shared evidence

Preserve units, product basis, population, observation periods, covariance,
dependency groups, state identities, source locators and uncertainty qualification.
Assumptions and normative inputs have their own declared provenance, rather than
invented observational parents. Transport and conversion assumptions remain explicit.
Forecasts/posteriors are not fresh observations. A new capture, extraction, archive
ID or citation must not make shared MOH/NZHS data independent or condition it twice.
Keep the existing `Scope`/`EvidencePacket` contract as the scientific authority.

### R10 — Revision, replay and recovery

Keep completed native records and source/output generations immutable. Refuse
accidental overwrite; handle interrupted execution without publishing a successful
complete receipt. Preserve failure evidence and retry only through an explicit
new attempt identity. Verify offline replay from originals through selected
transformations and model results in a clean qualified environment, using declared
exact/tolerance rules for the respective artifact types.

Exercise restoration of the selected source/manifest/derivative closure from a
rights-appropriate second copy without relying on implementation-worktree files
or undeclared sibling checkouts. Document the recovery scope and outstanding
objects. Catalogue membership, object hashes and a local copy do not establish
remote preservation or successful recovery.

### R11 — Runtime, packaging, rights and maintenance

Use an explicitly selected repo-local Python 3.15 interpreter at the newest
qualified patch (currently required 3.15.1), verified by execution. Reuse Nox/uv
and the owning repositories' maintained libraries and schemas. Preserve in-flight
environments and coordinate current runtime/lock/package work with its owners.
Consumer execution must use a qualified, versioned producer interface or built
artifact, with clean-package tests outside editable/sibling checkout paths.

Apply Apache-2.0 to project-owned additions while preserving existing notices and
third-party/source rights. No public raw-document upload, visibility change, new
account/consent, licence purchase or settings change is implicit. Choose a permitted
preservation/recovery destination before performing any external raw-object write.

### R12 — Evidence, ownership and completion reporting

Map every acceptance criterion to owned paths, native commands/tests, actual
execution evidence, expected producer/consumer revisions and remaining gates.
Plan focused tests first and reuse unchanged evidence; run affected components and
`tests/test_workstream_integration.py`. Run full integration, relevant numerical
reproductions, native archive validation, clean-package and applicable security
gates at coherent milestones. Record exactly which executed and distinguish local,
hosted, recovery and scientific acceptance. Re-read main/coordination before guarded
publication and verify receiving refs/files. No checkbox, fixture or generated
review substitutes for actual native integration and execution.

## Acceptance criteria

| ID | Required evidence |
|---|---|
| AC01 | Producer capability/interface map names actual native APIs/schemas, revisions, ownership and resolved or blocked gaps. No competing ledger/registry is introduced. |
| AC02 | Current inventory accounts for every consumed dataset, transformation and declared model output; changed/new entries cannot bypass lineage validation. |
| AC03 | Native source/observation/version records resolve to actual preserved originals; future captures have observed timestamps, while historical unknowns and rejected payloads remain explicit. |
| AC04 | The MOH workbook is re-extracted by a versioned operation; all 16 existing annual values and source-cell mappings are checked, with native input/output/validation receipts. |
| AC05 | At least one second current extraction/derivation exercises a materially different transformation, and multi-parent ancestry is tested where consumed. Fixtures remain labelled separately from source-backed execution. |
| AC06 | All qualified transformation paths emit actual native receipts containing the R04 execution fields, and their parent/output links and objects are independently checked. |
| AC07 | Negative tests reject duplicate/dangling IDs, cycles, byte tampering, swapped sources, stale code/configuration/environment, missing outputs and incomplete runs. |
| AC08 | Legacy records and results are retained; reconstructed/unknown lineage is explicit, and a verified replacement preserves old/new identities and any numerical differences. |
| AC09 | Every supported scientific runner supplies input-to-result lineage under its owner's contract; reverse trace and changed-source impact queries return the actual closure. |
| AC10 | Qualified native/consumer commands, replay and applicable CI/release paths fail on missing required lineage. Exploratory/legacy outputs remain labelled and cannot satisfy qualification. |
| AC11 | Shared-evidence, unit/population/product/date/covariance and state-identity tests remain effective; archival operations cannot create independent observations or change assumptions silently. |
| AC12 | Offline replay and interrupted-run recovery execute against identified originals and native manifests; clean-package execution does not depend on editable/sibling sources. |
| AC13 | A rights-appropriate second-copy recovery of the declared closure succeeds with byte verification; inaccessible or unqualified destinations remain open gates. |
| AC14 | Acceptance records include actual focused/full/native/reproduction/package/security outcomes, revised receiving commits and remote readback, with unexecuted/blocked checks explicitly retained. |

## Non-functional requirements

- Deterministic versioned manifest/content identities, portable references and
  `allow_nan=False` for scientific JSON serialization; timestamps/host metadata
  must not masquerade as deterministic scientific-content hashes.
- Bounded memory/network acquisition and safe parsing through maintained native
  components; source content remains untrusted evidence, never operational instructions.
- Backward-compatible migration where possible; incompatible schema/API changes
  need explicit versions, consumer tests and rollback/recovery paths.
- Clear CLI/JSON diagnostics name the failing object/relationship and required
  repair. Qualification claims cannot exceed the observed evidence.

## Out of scope

New scientific evidence conditioning, parameter calibration, policy/funding
recommendations, automatic source refresh, scheduled/background work, a replacement
statistical/provenance engine, wholesale ecosystem modernisation, blanket public
publication of originals, and merging existing draft PRs without their own required
checks. Operational implementation begins only after the planning review/handoff.

## Completion rule

Complete this track only when all required current input-to-result paths use the
archive's native provenance system, the selected future-addition gates execute,
and AC01–AC14 have actual acceptance evidence. Per-item capture and migration may
proceed incrementally; unresolved essential sources, transformations, producer
capabilities or recovery remain blocked/open and prevent a full-completion claim.
Successful metadata validation never substitutes for preservation, replay or
scientific acceptance.
