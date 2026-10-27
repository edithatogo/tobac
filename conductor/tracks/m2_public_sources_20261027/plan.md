# Implementation plan

Status: [~] Evidence map in progress; no external data requests.

## A: Protocol and initial catalogue
- [x] Inspect existing source IDs/archive bindings and preserve earlier targeted-review status.
- [x] Specify search/screen/capture/extraction/parameter methods and acceptance criteria.
- [x] Execute bounded public-source capture and seed linked source/extraction/assumption/parameter tables.
- [x] Verify all cross-references and calculations; record remaining work accurately.

## B: Complete the public-source map
- [ ] Execute/log all prespecified official/publication/repository search streams.
- [ ] Complete one backward/forward citation round; disposition all candidates with reasons.
- [ ] Retrieve public supplements and remaining originals or record specific unavailability.
- [ ] Recheck critical extracts against source table rendering; resolve or retain discrepancies.
- [ ] Appraise source funding/design/transport and shared underlying data; review table revisions.
- [ ] Report public-only residual gaps, conditional estimates and sensitivity assumptions.

No outreach, new OIA, restricted-data access, commissioning or automatic model ingestion.
The source-map plan remains open until phase B is executed; computational checks do not
substitute for source review or empirical qualification.

## Initial execution receipt — 27 October 2026

Methods:docs/research/M2_PUBLIC_SOURCE_METHOD.md. Tables and verification manifest:
evidence/m2/public_sources_20261027/. Initial counts:19 document records (17 source
records,two supplement candidates),72 extracts,eight assumptions,seven constructions/
checks,four queries and19 candidate dispositions. Seed imports are not newly re-extracted.

Qualified archive producer Python3.15.1 saved six originals and WARCs locally;one
OUP page failed. Six PDF signatures,object/WARC hashes,payload equality and derived
text hashes verified with warcio1.8.1. Native WARC dates remain null. Capture guard
peak189.3MiB,exit0 (partial acquisition is not full success); corrected verification
peak54.1MiB,exit0. Initial temporary-verifier stream-consumption error retained in logs.
Decimal arithmetic and all table foreign keys passed;Treasury rounded forecast
discrepancy is retained,not silently corrected. Conductor names15/15.

No production code/model/dependency or input changes;no full software-suite rerun is
claimed for this documentation/data-map task. Full public search,appraisal,supplements
and visual extraction qualification remain pending in phase B. No outreach/new OIA.
