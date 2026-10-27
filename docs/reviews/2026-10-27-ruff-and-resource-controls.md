# Review Report: Ruff coverage and bounded verification

## Summary

Extend the existing strict policy to tests and Nox tooling, enforce stable formatting,
qualify five explicit preview rules, strengthen rejection tests and bound macOS
verification processes. No scientific dependency pins, reference inputs, security
policy, hosted check or Python 3.15.1 requirement is removed.

## Verification checks

- [x] Plan compliance: source/scripts/tests/Nox lint and formatter gates; exact preview selection.
- [x] Style compliance: root and Nox use the same Ruff policy; formatter preview stays off.
- [x] New tests: real Ruff counterexamples and real process-group resource/cleanup cases.
- [x] Local tests: 903 passed, five capability skips, 92% coverage; nine real Ruff
  policy tests also pass in strict_all, including the latest discovery regression.
- [x] Numerical/package/security/recovery and bounded mutation pass: 114/131 killed
  (87.0%). All nine Nox sessions have successful current evidence; see
  `integration/ruff_resource_controls_20261027.json`. Hosted checks remain required.

## Iterative self-review

The change exceeds 300 lines, principally due to formatting and annotations across
existing tests. The user explicitly authorised implementation, fixes, review, commit,
verification and merge. Reviewed source and tooling diffs separately from test formatting;
no independent reviewer is a single-developer gate.

Four of five changed source modules have identical Python ASTs. The fifth (`tobac.run`)
batches adjacent list appends without changing expression order, values or scientific
formulae; none of the expressions observes the intermediate list. Historical extraction
bytes and numerical reference inputs are preserved. UTF-8 text reads match retained
JSON/CSV inputs. Empty-string comparisons were changed only for declared string cells.

Test fixtures retain dynamic argument/heterogeneous return conventions through explicit
scoped exceptions. Source/script strictness is retained. All 153 broad exception contexts
now check observed diagnostic prefixes, with alternatives where the existing parameter
matrix legitimately reaches several validation paths. Two jsonschema cases now require
`ValidationError`; the observed diagnostic records came from an actual 885-pass run.
The probe was temporary, read-only with respect to repository inputs, and not installed.

Targeted mechanical fixes were reviewed for return/zip/assert behaviour. No general unsafe
fix command is adopted as an ongoing gate. One renamed parametrized argument initially
left its decorator's name stale: full-suite collection detected it; both now use
`likelihood`. That failed run is retained and does not count as successful verification.

Resource tests exposed macOS EPERM when a group has only an unreaped zombie. Cleanup
now reaps the leader and distinguishes an empty/zombie-only group from a live denied
group. A live denial remains a failure. Memory is summed only for a new owned group;
normal exit, timeout, memory breach, SIGINT and SIGTERM unwind through cleanup. Inherited
output avoids unbounded stdout buffers. Native probes have deadlines. A genuine memory
leak is not established by a peak measurement. Polling/daemon/SIGKILL limitations are
explicit in `docs/engineering/RUFF_POLICY.md`; unrelated processes are not targeted.

## Remaining boundaries

Other experimental Ruff rules are not implicitly enabled, and no scientific/data gate
is closed by linting or process budgets. The upstream managed graph parser remains its
existing external gate. Non-macOS development remains deferred; existing jobs are retained.

Final local sampled peak was 830.7 MiB with a 4 GiB guard; 37 protected input/lock
files match the base byte-for-byte. Editor discovery and explicit Nox discovery
cover the same 108 Python files. The root policy is authoritative and the legacy
engineering config extends it, avoiding relative-glob drift between entry points.

Final bootstrap review replaced the workflow mkdir helper's bare Python with explicit
3.15.1 selection and an actual version assertion. The guard likewise rejects any other
runtime before launching a child. Thirty focused guard/policy/workflow tests pass.

Hosted Windows tests caught two POSIX assumptions in the newly strengthened message
assertions. The path reason now accounts for Windows drive-relative parsing; the
receipt regex accepts either path separator while retaining the exact filename.
Fifty-six affected tests pass locally. The other 14 executable PR checks, including
macOS tests/qualification, passed on 4b36b61; fresh final-head checks remain required.
