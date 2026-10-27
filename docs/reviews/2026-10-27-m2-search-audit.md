# Corrective self-review — saved public-search result completeness

Base:00012735f640f74dfeea6cde23af1e64c628ad1a,receiving main from PR#56.
A final audit found that the temporary result parser limited titles to180characters
and omitted five visible results. The first merged map's208dispositions were not a
complete screening of the saved batches. This report corrects that bounded claim;
it does not make a broader systematic-review claim.

## Fix and evidence

The title cap is removed. An independently executed table check now compares every
saved title/URL/rank against the current screening ledger, allowing URL parentheses
and deduplicating canonical URLs within each batch. Candidate IDs/ranks and indexed
citation links are rebuilt;native57reference edges remain unchanged. All213candidate
rows,435citation rows and their IDs/links pass. The five additions and per-batch
hashes/counts are in integration/m2_public_sources_20261027/search-parse-audit.json.

- Clinical urine-validation abstract: primary published abstract captured; vendor
  affiliation noted,complete funding unknown. Clinical cutoff/denominator/selection
  limitations prevent target-sewage transport. No numeric target extract.
- US flavour-policy review: full native article captured; Truth Initiative/RTI
  funding and declared no conflicts recorded. Different policy/endpoint and design
  limitations retained;no600-retailer effect inferred.
- Treasury20240568: public advice compilation captured with redactions and forecast/
  policy context;shared official material is not independent empirical evidence.
- Hungarian laboratory page: captured reproduction of the same primary abstract,
  linked as an attachment/alias;not the missing full paper or another study. The
  earlier40,000/6046legacy extracts remain unqualified by this abstract.
- ACS fluorescence-sensor paper: failed public route;materials-sensor/transport
  mismatch excludes numerical use. No contact or bypass attempted.

Four new objects verified by CAS/WARC/text hashes and exact WARC response payloads.
Additional acquisition guard peak155.1MiB;verification87.2MiB;both exit0. Totals now
35document records,44additional retrieval attempts,30captured objects,21usable,
9rejected challenge/stub objects and14failed routes. Initial six PDF objects remain
separate. Source/assumption/parameter/extract IDs and no-adoption flags rechecked;
all nine arithmetic checks remain unchanged. No production code,model inputs,
interfaces,dependencies,security policies or workflow edits.

## Verification and publication

The five-session local macOS Python3.15.1 evidence from PR#56 remains applicable to
unchanged production code. New targeted map/hash/completeness checks pass on actual
repo-local Python3.15.1. Conductor names15/15;git diff-check clean. Full original
visible-batch parsing is the regression check;there is no maintained new parser API.
Current manifest binds these revisions and preserves the pre-audit manifest.

This follow-up receives its own exact-head hosted qualification before guarded
merge,and receiving-main checks after merge. Those statuses are read from native
GitHub results;this pre-publication report does not declare them successful.
The archived track remains bounded-complete with explicit public-access/scientific
limits. No new request,contact or numerical adoption occurred.
