# Engineering follow-through implementation plan

Goal: turn approved dependency/release recommendations into checked, replayable gates.
Base: live edithatogo/tobac main 711705cb49b98ed24f66d29240d7cd7bc9c100e1.
Architecture: retain Nox and uv as execution/resolution engines. Small standard-library
receipts bind their outputs to dependency inputs; no custom package resolver or fake lock.
Preserve scientific code/results and the parallel M3 paths. No account/billing/security setting writes.

## Tasks
- [x] Write failing tests for missing/tampered/stale lock receipts and unsuccessful resolution.
- [x] Implement candidate lock generation through real uv and source-bound receipt checks.
- [x] Separate portable runtime/test lock inputs from Linux-oriented audit tools.
- [x] Make Nox use exact sync when locked, no extra floating installs, and non-isolated local builds.
- [x] Split lint/type and workflow/package-security audits so one failure does not hide another.
- [x] Add read-only gh diagnostics; classify absent runner separately from executed failure.
- [x] Harden internal candidate workflow; upload failed-run evidence separately from successful packages.
- [x] Execute scoped tests/CLI checks; record unavailable commands as blocked, not passed.
- [ ] Re-read main/#1, publish with expected-head guard, verify readback and coordinate.

## Review focus
Stale dependency inputs, missing receipt, mutated lock, resolver failure, forbidden overwrite,
symlink/path escape, unsupported audit platform, ignored child process status, partial job
pagination, lack of runner, and success labels on unexecuted checks.

Independent scientific validation and a calibrated funding recommendation are out of scope.
