# Archived source bindings

`archive-govt-nz` owns acquisition and preservation. This repository owns extracted
values, interpretation, source locators, units, populations, dependency groups and
scientific qualification. The existing evidence interface is unchanged.

The source register in `integration/archive/source-register.json` maps all four CSL
collections to stable archive IDs. Exact DOI identity (otherwise exact URL) groups
aliases without changing the consumer's source IDs. Differing legislative URLs remain
separate references even where a current redirect delivers identical bytes. A later
snapshot does not reconstruct the edition an agent originally consulted.

`consumer-inputs.json` records hashes and source-ID mappings for all 18 current input
and preserved CSVs (326 rows). `longitudinal_protocol` and
`v2.6.0_parameter_estimates` are internal references, not missing external documents.
Assumptions, templates, forecasts and model-derived summaries retain their original
classification; a mapping does not convert them into observations.

`source-bindings.json` records SHA-256 object and WARC identities from the archive's
offline verifier. `metadata_only` is bibliographic XML, not an article or underlying
dataset. `source_html_identity_observed` means the expected title was observed in
verified HTML, not that every table, attachment, supplement or extraction was reviewed.
Challenge pages and retrieval failures are retained explicitly and cannot support use
as original sources. Null capture dates reflect missing dates in the native WARC writer;
the run is dated 25 October 2026, with exact source versions unverified.

For reuse, resolve `source_id` through the appropriate CSL collection to `archive_id`,
then select a qualified capture's SHA-256 in the archive CAS. Verify its bytes before
extracting. Preserve the original extraction and its source locators; record any
replacement as a new revision and review changed values. Never silently substitute a
new current webpage for a historical source edition or condition shared MOH/NZHS data
twice. Refer to the archive's `docs/tobac/README.md` for acquisition and recovery.

The archive branch contains the source sets, source register, native capture receipts,
postflight verifier and operational readback. Raw payloads are locally retained in the
archive system; they have not been published to Hugging Face. Rights remain source
specific. No model input, prior, likelihood, result or M3 interface changes here.

The original Ministry of Health tobacco-volume XLSX was acquired directly from its
published file URL after the landing-page challenge. Its header and all 16 annual
values (2010–2025) match the existing CSV exactly. The additional
`workbook-reconciliation.json` binds both files' hashes and this comparison. This
closes the workbook-value check while retaining the existing conversion, duty-free
and measurement qualifications. The two supporting JSON/text extraction notes are
also hash-inventoried as agent records. They retain their original provenance role.
