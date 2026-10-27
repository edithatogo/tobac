# M2 public-source index and linked tables

Methods: [public-source protocol](../../../docs/research/M2_PUBLIC_SOURCE_METHOD.md).
Plan: [Conductor](../../../conductor/tracks/m2_public_sources_20261027/plan.md).
Public sources only; no author/custodian requests or new OIA submissions.

- [Source index](source_index.csv): 19 document records, comprising 17 source records
  and two candidate supplements. Six originals freshly captured and byte-verified;
  others explicitly uncaptured, failed or pending. Document count is not study count.
- [Source table](source_table.csv): applicability, source/group identity, access and
  review limitations. Structured study-design/funding appraisal remains pending.
- [Extraction table](extraction_table.csv): 72 reported-value/statement rows, each
  linked to a document and locator; old ledger imports distinguished from new text checks.
- [Assumption table](assumption_table.csv): eight analyst/source assumptions with role,
  alternatives and failure consequences. Supports are not automatically distributions.
- [Parameter table](parameter_table.csv): seven constructions/checks with input IDs,
  formulas, units, uncertainty method and permitted use. None adopted into a model.
- [Search log](search_log.csv) and [screening](screening.csv): four executed queries,
  one combined batch and 19 candidate dispositions. Earlier seed-search history is
  not reconstructed. No complete systematic-review count or coverage claim is made.

Fresh local payloads, WARC records and derived text are under the ignored
`outputs/engineering/m2-public-source-capture/` directory. Resolve each exact path
through source_index.csv or the [local catalogue](../../../integration/m2_public_sources_20261027/local-catalogue.json).
Hashes are tracked; source bytes are local, not committed/published. A fresh checkout
without those payloads does not have locally verified originals merely because receipts
are present. Reverify held objects before further extraction; preserve missing WARC dates.

Initial arithmetic checks reproduce the available-month HTP total and fee arithmetic.
The Treasury rounded 2025 forecast rows imply a difference one NZD million away from
its printed difference: both are retained as an unresolved source-precision discrepancy.
This does not establish an error in unrounded Treasury calculations. HTP imports,
forecasts, fee receipts and signed historical gaps are different quantities, and none
identifies the hypothetical cap's causal effect or current illicit consumption.

The capture verification initially failed because a temporary verifier consumed WARC
streams before reading payloads. The stream-lifetime fix was applied and all six
payloads then matched their CAS hashes. Both diagnostic logs remain local. No source
bytes, resource budget or archive implementation were changed to pass verification.

[Table manifest](manifest.json) binds the CSVs, methods and capture evidence. Cross-reference
and arithmetic verification is documentary/computational evidence, not source validity.
Further search streams, citation rounds, supplement acquisition and visual table review
remain unchecked in Conductor. Tables must be revised with provenance, not silently filled.
