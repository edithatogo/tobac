# Parallel engineering work: assessment and reconciliation strategy

Date: 26 October 2026 (Australia/Brisbane).

## Scope and current state

The relevant parallel code work is [PR #25](https://github.com/edithatogo/tobac/pull/25),
`review/m2b-longitudinal` at `a7d0e8d47615367856e06dd711a64bfe21953db7`: nine commits,
30 changed files, based on `main` `59bb0e4ebaf1881158849df1702a1d3101aad58f`.
The owner remains the single developer. This assessment adds no independent-review gate.

Our separate engineering checkout has Python 3.15.1 commits through `69f35b7`, followed by
uncommitted strict-check cleanup and the owner's macOS/single-developer policy changes.
Thirteen paths overlap PR #25, including Nox, type/lint configuration, the empirical runner,
two supply modules and active Conductor records. Neither checkout is an authoritative replacement
for the other. Preserve both histories and reconcile their changes explicitly.

The archival source-binding branch/PR #21 and native archival-lineage planning checkout are
separate work. Their provenance records are not substitutes for engineering acceptance evidence.

## Findings

### 1. High priority: runtime selection and checker resolution conflict with the required runtime

`engineering/bp_longitudinal.json:4,12` selects Python 3.13 and imports site-packages from
`.nox/quality/lib/python3.13`. `engineering/basedpyright.json:4,7-8` still targets 3.12 and binds
another profile to the named quality environment. These paths can make a check depend on a
previous session rather than the interpreter and dependencies of the session invoking it.

`noxfile.py:24-25,80` introduces a Linux audit path that sets `VIRTUALENV_PYTHON=3.13` inside
the session body. This does not select and verify the interpreter for the Nox environment
already created. The primary checkout's current Nox environments actually use Python 3.13;
the hosted matrix also runs 3.12/3.13. These passes do not qualify the requested 3.15.1 setup.

Fix on the reconciled branch: select the repo-local 3.15.1 interpreter before environment
creation, assert the actual session version, and pass that interpreter explicitly to BasedPyright
with `--pythonpath`. Use a source-root path instead of a different session's site-packages.
Align all active checker targets to 3.15. Treat existing non-macOS results as historical receipts;
move new non-macOS development/qualification work to the roadmap.

### 2. High priority: the mutation helper can approve incomplete results

`scripts/check_mutation_score.py:55-59,90-98` excludes interrupted/untested mutants from the
denominator without requiring a complete run. Reproduction with one killed mutant and 99
untested mutants prints `100.0% (1/1 killed)` and exits zero at the 60% floor. The existing test
at `tests/engineering/test_mutation_gate.py:63-70` explicitly endorses that incomplete-run pass.

The CLI also accepts a nonfinite threshold: `--minimum nan` passes a 50% result because the
comparison against NaN is false. The fixed Nox argument is 60, so this second defect concerns
the standalone CLI/input contract rather than the current fixed invocation.

Fix: require a completed result set before scoring; reject nonfinite or out-of-range thresholds;
bind the result to the selected source, current source hash, tool version and run. Scope metadata
reads to the intended target rather than every cached `.meta` file. Keep the score floor distinct
from completion and result validity. Preserve mutmut's status semantics and test them against the
installed tool. Then add tests that reject partial/stale results and invalid thresholds.

### 3. Medium priority: the runner is not fully typed, and one remaining error is not a pandas cascade

An explicit Python 3.15.1/macOS check of the parallel runner reports 133 errors: 130
`reportUnknown*`, two missing-stub errors, and one `reportArgumentType`.
At `scripts/run_empirical_longitudinal.py:491`, `list[float]` is passed to `sample_temporal`,
whose `query` annotation remains `Iterable[Real]` at `src/tobac_supply/empirical_longitudinal.py:214`.
This contradicts the current statement that every remaining error is a pandas cascade.

Fix: qualify compatible third-party stubs in an isolated 3.15.1 environment before regenerating
the appropriate tool dependency inputs, locks and receipts. Do not change scientific dependency
pins merely to satisfy a stub resolver. Give named outputs precise structures (for example,
TypedDicts for reconstruction/discrepancy results and NDArray aliases), use a consistent numeric
input contract, and remove unnecessary ignores after stubs resolve. A validated scalar/array
boundary should retain the existing runtime domain checks and scientific units.

Keep the failing focused session visible while correcting it. Once it is zero under the
qualified environment, include it in the normal quality checks. Its current separate placement
is transparent, but it is not automatically exercised by the existing CI session lists.

### 4. Medium priority: current status claims and the proposed advisory lane need reconciliation

PR #25's body still claims the runner passes strict typing and says no hosted run executed.
At assessment time its exact head has 15 successful hosted checks. They cover the existing
older Python matrix and do not execute `types_longitudinal`, whole-source strict checks,
mutation or profiling. Update the PR body and current Conductor status against the actual head;
retain earlier dated receipts rather than overwriting them.

The proposed CI/CD track adds several checkers and a Linux arm runner while the required
strict checks are already failing. Defer that expansion and place non-macOS work on the roadmap.
Use the existing Nox/tool stack to close the current defects first. Additional tools should have
a specific demonstrated gap and should not create substitute green badges for a red strict gate.

### 5. Lower priority: the track-name checker promises a check it does not perform

`scripts/check_conductor_track_names.py:4-6` says `plan.md` H1 is checked, but lines 83-93
only inspect the specification H1 and registry heading. Either implement the stated plan-title
check with the intended convention, or narrow the documented invariant. Do not silently rename
every plan's ordinary `Plan and status` heading just to satisfy a new convention.

## Ordered implementation strategy

1. Preserve the current engineering working tree and PR #25 head in separate commits/refs.
   Start one reconciliation branch from freshly checked `main`; use one writer for integration.
   Bring across the Python 3.15.1 runtime/dependency migration and the current macOS/single-owner
   policy, then apply the useful PR #25 changes file by file. Keep the new mutation tests and
   runner/interface improvements, while correcting the findings above. Format once after the
   semantic reconciliation so formatting does not obscure the merge.
2. Establish one reproducible baseline: exact Git/dirty state, Python executable/version,
   NumPy/SciPy/pandas/checker versions, configuration paths and command. Pass the same interpreter
   to Nox checks and direct checker invocations. Resolve our current 2,208-versus-2,052
   BasedPyright count difference before claiming an error reduction.
3. Repair mutation completion/threshold handling and qualify the focused runner's types.
   Run exact affected tests plus the integration suite, retain first failures, and then run a
   fresh scoped mutation measurement. The 60% floor remains a regression alarm; address surviving
   meaningful scientific mutants with independent numerical oracles rather than lowering it.
4. Work through whole-source strict findings in bounded modules: correct dependency/source
   resolution, annotate shared numeric and JSON boundaries, fix actual defects, then finish
   mechanical style/documentation issues. Report configuration-policy changes separately from
   code fixes; do not suppress unknown/type diagnostics or remove files to make the counts zero.
5. At the coherent integrated milestone run the complete Nox tests/coverage, all numerical
   reproductions and longitudinal output comparisons, package install/import, security and
   strict sessions. Execute hosted macOS qualification against that exact head. Update the PR
   description and Conductor once with receiving commit and retained artifacts. Merge only after
   reconciling any advance in main and verifying the receiving ref. Independent review is optional.

## Verification performed for this assessment

- Read the PR diff, active Nox/configuration, mutation helper/tests, worktree and branch state,
  latest issue #1 evidence, and live PR checks. PR #25's exact head has 15 successful checks.
- Used the existing engineering checkout's verified Python 3.15.1 environment, with its qualified
  newer scientific/tool dependencies, against the parallel source. This is a compatibility check,
  not a reproduction of that branch's older locked environment.
- Mutation-gate tests plus `tests/test_workstream_integration.py`: 35 passed.
- Consumption-ledger, empirical-core and empirical-runner tests: initial run 85 passed, two
  failures and three setup errors during disk exhaustion. Once free space returned, the exact
  five affected nodes all passed (five passes, no retry plugin). Total focused test coverage is
  125 passing cases across these selections; the storage interruption remains recorded.
- Direct mutation-helper probes reproduced both false passes described above.
- Explicit 3.15.1 runner type check: 133 errors, including the non-cascade numeric annotation
  mismatch described above. No stubs were installed and no dependency environment was replaced.
- No source edits, merge, new workflow, message to another agent, or full scientific reproduction
  was performed by this assessment. This strategy document is saved in our engineering worktree.
