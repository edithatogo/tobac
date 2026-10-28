# Review Report: macOS-only CI qualification

## Summary

The owner's 28 October direction is applied to active hosted workflows; Windows
and Linux qualification is deferred, while substantive scientific/security checks
continue on macOS with Python 3.15.1 and existing pass thresholds.

## Verification Checks

- [x] **Plan Compliance**: Yes, macOS only; platform deferrals are explicit roadmap work.
- [x] **Style Compliance**: Pass, strict Ruff lint/format and BasedPyright zero errors/warnings.
- [x] **New Tests**: Active-platform/runtime/guard contract; deferred contracts remain checked.
- [x] **Test Coverage**: Full suite, 1,033 passed/five capability skips, 92% source coverage.
- [x] **Test Results**: Affected contracts/integration 51 passed; corrected ordering regression
  passed; final full suite and dependency/workflow security checks passed.

## Findings and fixes applied

### High: platform scope did not match active execution

The previous roadmap deferred non-macOS development while active CI still required
Windows/Linux runners. Remove those matrix entries and move quality, scientific,
longitudinal, M3 and scheduled audit/canary execution to macOS. Keep every substantive
command, full-SHA Action pin and scientific/security threshold. Run once per PR
and on main; remove duplicate branch-push executions and cancel superseded
scientific runs through per-ref concurrency. Preserve the Linux-only
manual locked-release and lock-generation definitions byte-for-byte under the roadmap;
they cannot execute there. Their original locked-release contract remains tested,
not re-labelled as native macOS locked-release acceptance. Defer the scheduled
lock session as well, since it resolves the Linux audit profile. Preserve native
security, strict, mutation, profiling and canary execution. Branch protection/rulesets
were inspected; neither is configured for main, and no settings were changed.

### High: published SourceRight asset name misstates its architecture

The v0.1.20 asset named sourceright-macos-x86_64 has verified SHA-256
b405f4a4dc09ad8af03bfd49a84484df194aac8401a188a08510334a8aa77a5c;
file inspection identifies ARM64 Mach-O. Match those actual bytes with macos-latest
ARM64, retain hash checking and use the actual CLI to validate all CSL collections.
Local native execution succeeds with unchanged input and executable hashes. Hosted
native execution is separately required; the asset name alone is not architecture proof.

### Medium: interpreter bootstrap invalidated a positional test assumption

One initial full-suite contract expected inventory to be the first shell command.
Selecting/checking repo-local Python must precede that inventory. The test now
requires inventory before dependency installation and scientific execution, preserving
its original substantive gate. Its failure-only rerun passed, then the full suite passed.
Retain the initial failure log and do not count that first run as successful.

## Evidence and retained boundaries

See integration/macos_ci_scope_20261028.json for actual commands, hashes and results.
Numerical/scientific sources, dependency inputs/locks and Nox implementations are
unchanged from 94c4712; the existing 29-table zero-difference replay remains valid
local numerical evidence. Hosted qualification executes that replay again at the
new head and receiving main. All expensive migrated commands retain owned process
group RSS/time guards; mutation remains limited to two children. No leak-free claim.

Superseded mixed-platform main workflows for 94c4712 were cancelled where active;
the completed longitudinal run was preserved. Those cancellations are not failures
of executed tests and are not passes. Exact new-head and receiving-main macOS jobs,
artifact readback, signed package provenance and dependency submission are recorded
in the platform-scope PR. The separate published Voiage 3.0.0 gate remains open.

The general engineering context exceeded its 80 kB budget after documentation growth.
A dedicated macos-ci profile selects this task's sources within 40 kB; its actual
build and existing profile-schema test pass. No context or process limit was raised.
