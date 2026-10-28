# Native archival lineage: foundations checkpoint

This is an engineering inventory and native capability assessment. It does not
establish original-source preservation, an executed transformation chain, a new
observation or scientific qualification. Existing scientific inputs are unchanged.

## Revisions, execution and ownership

The consumer resumption base is tobac `62056c566d1d7f9280d63df6c26b7673de8be98a`.
The producer inspection is frozen at archive-govt-nz
`712420fbb84425f7c014246bf199217f731689bf`. Its live checkout has unrelated dirty
work and a separate active owner. Only committed producer bytes were read; no
producer files, environment, CAS objects, captures or native records were changed.

Tobac PRs #21 and #23 are merged. Archive PR #776 remains open at
`08340fd6e81ca73b2c68deb414dcb5d5b89272a9`; its old capture receipts are historical
evidence, not proof that its changes or objects are current native acceptance.
Issue #1 is closed historical context and is not an approval channel.

Consumer ownership is limited to the existing source-handoff helper, its inventory
and tests, the diagnostic native probe and these Conductor/engineering records.
M3 interfaces, numerical kernels, parameters and reference results are unchanged.
The selected local interpreters executed Python 3.15.1. Heavy commands used the
existing 4 GiB / 40-minute guard, serially. The original evidence context exceeded
its byte budget; it was narrowed explicitly to four existing contracts (42,412
source bytes), without increasing the limit. Context is rebuilt after source/HEAD
changes; the earlier context receipt is not current-source validation.

## Inventory and method

`scripts/source_handoff.py --inventory --out NEW_RECEIPT.json` reuses the existing
source register, capture bindings and consumer CSV verification. The generated
[inventory](../../integration/archive/lineage-foundations-inventory_20261029.json)
enumerates every reviewed public path under `data/`, `configs/`, `evidence/` and
`results/`, plus hashes of maintained Python implementation files. It records CSV
shape and explicit row source/role/dependency metadata. It does not infer missing
source links, turn bibliography entries into observations, or include local-only
documents. It is a derived export, not another source registry.

The current snapshot has 38 registered source identities, 43 bibliography aliases,
18 legacy CSV inputs and 145 public scientific assets: four data files, eight
configuration files, 57 evidence files and 76 saved result artifacts. The latter
remain reference outputs. New evidence assets without native links are visible
with unknown relationships. Capture statuses are copied as recorded metadata;
no native original bytes are independently verified in this inventory run.

The published-path inventory is a coverage superset. It does not resolve arbitrary
dynamic file reads or prove a complete executed dependency graph. AC02's ongoing
change enforcement and result-to-original closure remain open implementation gates.

| Execution family | Existing inputs and implementation | Declared output/provenance contract |
|---|---|---|
| M1 regulatory | `src/tobac/run.py`, `configs/regulatory.json` | `tobac.run.v1` input/output hashes; saved conditional reference tables |
| M2 retail | `src/tobac/m2.py`, regulatory/retail configs, `evidence/m2/source_review.json` | `results/milestone2/manifest.json`; source review is not a current policy posterior |
| M2 publication/robustness | `scripts/run_m2_publication.py`, `scripts/run_m2_robustness.py`, their configs and public-source map | Saved publication/readiness manifests and conditional result tables |
| Release calibration | `scripts/run_release_calibration.py`, calibration config, release CSV and completion-text extract | Generated `run_manifest.json` with source/file hashes; retained compact reference outputs |
| Empirical longitudinal | `scripts/run_empirical_longitudinal.py`, empirical config and historical intake CSV | Historical summary process; periods, source dependence and annualised units stay explicit |
| M3 | `src/tobac/research/runner.py`, regulatory/retail and M3/refinement configs | Generated `tobac.run.v1`; retained reference CSVs and preserved source-output archive |
| Workbook extraction | `scripts/qualify_moh_workbook.py` and existing workbook-reconciliation receipts | Existing 16-value parity evidence; not a newly executed native transformation receipt |

Assumptions and normative configurations retain declared provenance. Legacy
extracts and transcriptions remain preserved extracts; unknown capture or extraction
dates are not reconstructed from filesystem times. MOH/NZHS aliases, periods,
dependencies, scope and state IDs continue to use the existing shared contracts.

## Native capability map and actual probes

Run `scripts/probe_archive_contract.py --repository PRODUCER_CHECKOUT --revision
FULL_COMMIT_SHA --out NEW_RECEIPT.json` with the qualified interpreter under
`scripts/run_bounded.py`. It reads three fixed paths using Git at the immutable
revision and executes those native modules from an isolated temporary directory.
The synthetic Git-loader tests do not substitute for this actual native execution.
The [native receipt](../../integration/archive/native-contract-probe_20261029.json)
binds source hashes and interpreter identity. It has no network capture or full
producer-package, CLI, preservation, recovery or scientific acceptance claim.

| Native surface at the frozen revision | Observed capability / gap | Required producer-owned resolution |
|---|---|---|
| `provenance.build_manifest` | Deterministic bytes; rejects dangling observations; accepts duplicate object IDs | Reject duplicates and verify complete relationship/output closure |
| `records.TransformationRecord`, `validate_archive_record`, `canonical_record_bytes` | Strict per-record fields include input/output IDs, implementation revision, environment, parameters, times and state | Reuse this maintained record contract; do not replace it with consumer JSON |
| Strict record to manifest receipts | Valid `record_id` transformation fails with `missing_transformation_receipt_id`; an ID-only `receipt_id` entry is accepted | Define a versioned native adapter and validate the full record before manifest inclusion |
| `ContentAddressedStore.verify`, `cli_integrity.verify_cas` | Maintained actual-object fixity APIs exist; not executed against the tobac estate in this phase | Bind native object verification and all required transformation inputs/outputs |
| `core.manifests.SourceManifest`, source-manifest schema | Dataclass accepts strings; schema requires native schemes including `web://`, rather than a bare HTTPS URI | Specify/validate the source-URI encoding; do not silently change source identity |
| `warc.write_response_record`, capture/preservation records | Actual synthetic writer emits no `WARC-Date`; preservation timestamps alone do not supply it | Record observed capture time through the owning capture/WARC path; preserve historical unknowns |
| Packaged native producer interface | Selected source modules executed; full installed-artifact compatibility not qualified | Publish/qualify the supported package/interface before qualified consumer adoption |

Qualified status requires native object and relationship verification plus successful
execution/output closure. Legacy and exploratory results remain labelled; this phase
does not wire a silent fallback or promote any existing result to qualified lineage.

## Acceptance map and next work

AC01 has a revision-bound capability/ownership map. AC02 has current asset and
implementation coverage, but full execution relationships and future-addition gates
are pending. AC11 retains the scientific interface and cross-workstream regression
contract. AC14 is satisfied only for the explicitly recorded phase-level checks;
full-track acceptance is open. AC03–AC10 and AC12–AC13 require subsequent native
record integration, extraction, execution, replay and second-copy recovery evidence.

The next tasks are the producer-owned source/capture contract tests (P2.1), native
capture/registration changes (P2.2) and generic closure/record adapter work (P3.1–P3.2).
The active producer owner retains those files and operations. This checkpoint is a
concrete handoff specification, not authorisation to modify that owner's dirty tree.
Public-source-only, no requests/contacts/submissions and local-only research documents
remain the operating scope. No full-track completion or archive is claimed.
