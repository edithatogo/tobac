# Source-to-observation handoff

This bounded consumer report connects the archival register from PR #21 to the existing
`Scope` and `SupplyBasis` contracts. It does not create an `EvidencePacket`, likelihood,
posterior or new observation. It leaves the regulatory prior unchanged.

Run on the qualified repo-local Python 3.15.1 environment through Nox:

```sh
uvx --python 3.15.1 --from nox==2026.10.20 nox -s source_handoff
```

The output is `outputs/engineering/source-handoff.json`. The existing reproduction session
also writes `source-handoff-reproduction.json`. A valid report can have `status: blocked`:
that means the declared scientific gaps were reported successfully. Invalid schemas, missing
inventories or changed input bytes raise errors and fail the command. `metadata_compatible`
means only that the declared metadata passed these checks; it is never scientific qualification.

## What is bound

`integration/archive/observation-handoff.json` declares the proposed contrast, source IDs,
row years, roles, periods and underlying-data mappings. Its JSON Schema rejects unknown fields,
wrong types and empty declarations. Unknown scope, product and scientific-model declarations
stay null rather than acquiring a default approval.

The initial report covers 16 MOH release rows (2010–2025) and 12 historical measurement-summary
rows (2012–2023). The prospective target is an explicitly unresolved example scope for reviewing
compatibility, not a selected research design. Its `target_scope_status: proposed` is an
explicit gap. Different physical units also remain blocked until a separately qualified input
conversion is available; a transport note cannot supply that conversion. Calendar periods on historical summary rows are
proposals; the missing source date convention remains a gap. All 18 inventoried CSVs, supporting
files and four bibliography collections are verified before selecting a row. Source aliases resolve
through the existing archive IDs. Byte hashes, source locators, source limitations and acquisition
outcomes remain visible.

MOH releases and the Phyo summary share underlying MOH returns. IDs use the declared data group
and half-open period (`group:YYYY-MM-DD/YYYY-MM-DD`), independently of citation or observation
label. The consumer mapping is explicit and reviewable; it is not an independent determination
of actual source dependencies. Both exact reuse and overlapping periods within a shared group
are blocked. A prose assertion of independence cannot waive this block. Existing D0 identities
must be reconciled into this convention before use; legacy ambiguous IDs fail closed.

The report does not assemble a joint likelihood. Shared-data rows require a separately justified
joint model or a non-overlapping selection. Naming a covariance model does not establish that its
matrix is positive definite, correctly estimated or scientifically appropriate. Execution and
numerical validation belong to the existing likelihood and evidence interfaces.

## Capture verification and current gaps

By default no raw archive payload is present, so the report preserves capture hashes without
claiming their bytes were verified locally. To check already-held source and WARC objects, stage
copies in an explicit flat directory named by their full SHA-256 and pass
`--objects /absolute/path/to/staged-objects` after `nox -s source_handoff --`.
This is a local staging contract, not an assumption about the archive's native layout. No
acquisition, copying from another service or publication is performed by the command.

Both original payload and WARC must match their digests. Metadata-only records, challenge pages
and failed retrievals cannot substitute for original source objects. HTML title identity alone
is not a numerical extraction check. Missing capture dates remain unverified; a newer snapshot
cannot recover the historical edition originally consulted. The retained workbook comparison is
executed-at-the-time evidence, not a fresh workbook extraction by this command.

The real-data report remains blocked for missing capture verification/dates, scope and product
qualification, likelihood, covariance and transport declarations. The historical summaries also
retain their derived role and uncertain period convention. These are research decisions and
source limitations; the software does not fill them with synthetic observations or assumptions.

## Ownership and limits

`archive-govt-nz` retains acquisition and preservation ownership. This change does not implement
the broader native archival lineage plan or scientific ecosystem modernisation plan. It adds no
second evidence engine and changes no source observations, numerical assumptions or results.
Synthetic fixtures test rejection behavior and metadata compatibility only. Independent scientific
endorsement, current-NZ calibration and policy conclusions remain unclaimed.

The subsequent [MOH pathway qualification](MOH_OBSERVATION_PATHWAY.md) retains a new dated
report using locally verified objects. The earlier report/proposal above remain unchanged
historical snapshots. Native source/value verification does not waive the remaining scientific gaps.
