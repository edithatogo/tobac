# Review Report: Native archival lineage consumer extraction

## Summary

The consumer implementation uses a frozen installed producer and keeps full
lineage unqualified while advancing the MOH extraction and per-record interface.

## Verification Checks

- [x] **Plan Compliance**: Partial; MOH portion of P4.1 and the consumer portion
  of P4.2/P3.3 advance. Producer source registration and complete closure stay open.
- [x] **Style Compliance**: Ruff checks/formatting and strict typing pass.
- [x] **New Tests**: Independent sixteen-value/cell oracle, wrong sheet/header/
  coverage/order/types/nonfinite values, changed bytes, symlinks, unreviewed wheel
  and immutable/private attempt boundaries.
- [x] **Test Coverage**: 62 affected extraction/parity/workstream tests pass.
- [x] **Test Results**: Full suite: 1084 passed, 13 capability skips, 92% coverage.
  Strict checks, package, security and clean-package sessions pass. Numerical
  operations passed; the final primary/robustness clean-source replay passed from
  commit `6fa2306` after the initial staged-tree rejection. Actual native execution
  and five negative controls passed, with nine objects and two records reopened.

## Findings and applied fixes

- Fixed input and wheel check/use races: one bounded verified snapshot is consumed,
  with parsing from the actual stored input bytes. Source metadata snapshots are
  retained alongside data rather than represented by a hash alone.
- Require installed package files to match the reviewed wheel. uv's direct-URL
  metadata omits the archive hash, so that field is not accepted as artifact proof.
- Restrict attempts to new private consumer output directories. Preserve originals,
  unknown capture time, failed attempts and existing scientific inputs.
- Explicitly label the operation exploratory. Native per-record success does not
  close manifest, source registration, scientific, runner or recovery acceptance.

## Review scope and open gates

Reviewed the consumer helper, independent tests, optional Nox route, interface pin
and documentation. No producer code/estate, scientific kernel, parameter, baseline
lock or M3 interface changes. Native producer core manifest/record/WARC source is
unchanged from the prior frozen capability assessment; historical evidence is reused.
No generic graph validator, source registry or adapter shim is introduced.

Installed producer preflight at Python 3.15.1 verifies package/module bytes and all
sixteen original workbook values and cell locators. It is read-only and does not
substitute for the separately recorded persisted native execution. Source captures,
closed provenance, second extraction, all runners and recovery remain required.

The review also requires a schema-valid CycloneDX 1.6 SBOM whose complete
name/version inventory matches the actual execution import context, including the
declared consumer source distribution. The private environment audit reports no
known vulnerabilities in 80 auditable installed dependencies; the unpublished
producer artifact and consumer source are separately identified.

No unresolved critical/high consumer findings remain in this bounded scope.
The actual native receipt remains exploratory with full qualification false.
Review does not close the outstanding track acceptance criteria.

Hosted CodeQL on PR #71 identified five ineffectual ellipsis bodies in the new
protocols. Replaced them with the existing repository abstractmethod/raise pattern;
no producer call or extraction behavior changed. Existing native execution is
bound to `6fa2306` and reused for this typing-only correction.

## Recovery continuation review — 29 October 2026

The native producer harness reports success for empty manifests, mismatched roots
and duplicate entries. The bounded consumer preflight was added for the MOH
rehearsal and rejects those cases against a native-verified nine-object inventory.
It is explicitly called before the guarded native rehearsal; it does not change
or independently qualify the producer's general harness or full source graph.

A new extraction and native restore/replay passed with nine objects and 16 exact
rows. Missing/corrupt object controls failed as expected. The actual original WARC
payload matches the workbook and has no WARC-Date. The private rehearsal copy is
on the same device and its local-path lock does not prove clean offline install.
The previous execution's private receipts were absent from the restored worktree
and main checkout, so they are not represented as recovered. Source registration,
full native closure and independent recovery remain open.

The consumer guard, targeted tests, source readback, native controls, ownership
and publication boundaries were reviewed. Initial strict style/type findings and
preflight script import/stream-handling errors were corrected before their native
mutations; their original logs are retained. Full suite: 1092 passed, 13 capability
skips, 92% coverage. Corrected `strict_all` passed. These establish the stated
consumer scope only; no scientific or archival acceptance is asserted.

## Installed producer replay review

The derivative lock changes only the local wheel reference and preserves the
historical lock. Actual `uv --offline` installation used the existing cache and a
repo-local Python 3.15.1 environment. Readback from outside the checkout verifies
453 producer files, nine attempt objects, two capture objects, two strict records
and all 16 workbook values. The guard is a retained private script; no clean
installed-consumer or independent-backup qualification is implied. No source or
scientific model change is part of this follow-up.

## Installed consumer library and candidate assessment review

A separate offline, local-cache environment installed the consumer and producer
libraries. Thirty-six consumer wheel files and the licence/notice match committed
source. Frozen script snapshots outside the checkout reproduced all 16 MOH values
and output bytes from native CAS. The runnable extraction command is not packaged,
the environment is inside the worktree and the cache is not an independent backup.
A separate retained SHINE article was assessed as a second-extraction candidate;
its source hash differs from the earlier referenced copy. No source-version
identity, native transformation or scientific qualification is inferred.
