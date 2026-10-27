# Conductor self-review — M2 public-source map

Historical PR#56 snapshot. The subsequent [search audit](2026-10-27-m2-search-audit.md)
corrects five omitted long-title results and supersedes its screening-completeness
counts/claim. Original software verification remains evidence for unchanged code.

Scope: current main805f7db3 plus local public-only decisions c20cc78/initial map5bdf6f0
and the completed bounded search/retrieval/extraction revisions. The owner authorised
implementation, review, fixes, commit, checks and merge autonomously. This is a single-
developer self-review, not independent scientific endorsement. Larger-than300-line
scope was reviewed in file groups with the linked source objects and current tables.

## Review and fixes

- Decisions/withdrawn requests: all four letters remain historical and unsent;
  manifests and superseding public-only direction agree. No contact or new OIA.
- Methods/search/screening/citations: exact48queries,12combined batches,208candidate
  dispositions; malformed query restrictions and forward/backward index limits are
  explicit. Native lists contain34+23references. Batch co-discoveries are not asserted
  citation edges. No exhaustive systematic-review or saturation claim.
- Capture configurations/receipts/catalogues: isolated local archive producer;
  byte/WARC/text hashes checked. Rejected9HTTP200challenge/stub objects among26captured
  additional objects;17are usable content,13other attempts failed. All39routes are
  dispositioned. Both actual human-yield supplement PDFs retrieved through published
  links; public transient signatures excluded from tracked URLs. Raw sources remain
  local; missing native WARC dates stay null.
- Source/extraction/assumption/parameter tables: corrected shared NZHS/fiscal data
  groups; checked source/document pairing and all ID references. Clarified percentage
  versus percentage-point units, CI labels, censoring, missingness and legacy extract
  ineligibility. Rounded factors give9.0263/4.9578, not exact9.02/4.95; comparison is
  rounding-limited and does not establish a population distribution or an author label.
- Original page rendering: Treasury demand/revenue, Customs imports and later duty,
  RIS costs, baseline gap, regulator funding, application counts/fees and S2A/S2D.
  Financial sums/signs and the retained−1m Treasury discrepancy checked using Decimal.
  Human-yield/CVS fullHTML and Dutch/CVS primary abstracts checked; unavailable
  current foreign/wastewater full texts are not called verified numerical inputs.
- Funding/design/transport: CVS employee/funder involvement, TDB tobacco clients,
  research/agency funding and unknown declarations preserved. Unlike outcomes,
  foreign matrices, repeated policy episodes and shared MOH/NZHS/calibration inputs
  cannot be pooled as independent target observations. No model inputs changed.
- Conductor: bounded phase complete and archived; issue#3 scientific/value/governance
  limits retained. Request-preparation index wording corrected to withdrawn.
- CSV line endings normalised toLF after diff-check identified CRLF whitespace.
  Checked all current manifest hashes and no transient URL signatures in tracked files.

No unresolved software/documentary finding remains within this bounded scope. Public
access restrictions and scientific non-identification remain in the completion report
and research-gates.md; these are not silently promoted into acceptance.

## Executed local verification

Darwinarm64, actual repo-local Python3.15.1. Serial bounded command:

```
.nox/tests/bin/python scripts/run_bounded.py --timeout 2400 -- \
  uvx --python .nox/tests/bin/python --from nox==2026.10.20 nox -r \
  -s tests strict_all reproduce clean_package security
```

All five sessions passed.981tests passed,5capability-conditioned skips;92%branch-aware
coverage;Ruff lint/format passed,114files formatted;BasedPyright0errors/warnings;
numerical replays/invariants passed;clean-package install/API/M1CLI passed;security
findings check,zizmor and pip-audit passed. Audit retains its declared native-macOS
qualification rather than claiming the Linux lock was used. Sampled process-group
peak722.3MiB,guard exit0;this bounded run is not proof of absence of memory leaks.

Separate table verification checks31documents,82extracts,10assumptions,9constructions,
foreign keys,held object/WARC/text hashes and no automatic model adoption. Receipt:
integration/m2_public_sources_20261027/table-verification.json. Manifest binds the
current CSVs/methods/capture receipts;initial snapshot remains separately retained.
Conductor names15/15,git diff-check clean. No dependencies,production code,CI/security
policies,Python version or full-SHA Action pins changed.

## Publication acceptance

Commit/PR will carry this self-review and the archived plan. Exact-head hosted macOS
Python3.15.1 checks must pass before guarded merge;receiving-main checks/readback must
also be verified. Their native run links/status belong to the PR and final handoff;
this pre-publication report does not claim those jobs have already run.
