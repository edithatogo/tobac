# Plan and status

- [x] Inspect live main, shared contracts, dependency manifests, workflows and #1/#4.
- [x] Review adopted/deferred existing-library alternatives and document semantic boundaries.
- [x] Write failing backend requirement test; implement SciPy replacement; preserve tiny-SPD shape/domain semantics.
- [x] Write context tests before implementation; validate with real jsonschema; reject stale/unsafe/unbounded profiles.
- [x] Run the imported 151 tests, 26 existing cross-workstream tests and new executable checks.
- [x] Define secure bounded matrix/deep/canary/internal-candidate lanes with maintained tools and full action pins.
- [x] Attempt real dependency-lock generation; record the uncached/offline failure without a fake lock.
- [x] Add reviewed context profiles, small agent skill, Conductor project context and pinned upstream gitlink definition.
- [x] Execute new Nox/Ruff/BasedPyright/Hypothesis/mutation/security/profile tooling in a capable environment.
  - [x] 2026-10-25 at 044c995: real Nox `tests` (495 passed, 91% coverage) and `reproduce`
    (M1/M2/M3/longitudinal, all verifiers pass) executed in **bootstrap** mode.
  - [x] Ruff (both invocations), BasedPyright strict, zizmor and pip-audit executed and **green**
    after fixing three real defects they exposed.
  - [x] 2026-10-25 gap-closure pass: mutation (mutmut 3.7.0) executed natively on
    `src/tobac/supply.py` — 128 mutants, 79 killed, 49 survived (61.7%). The session passes
    because mutmut enforces no threshold; the survivor count is a recorded weakness, not a pass.
  - [x] 2026-10-26 Python 3.15.1 Scalene quick profile executed; artifact hash and scope are in
    `integration/engineering_hardening_python315_20261026.json`.
  - The Linux-scoped locked audit install and execution are deferred to the roadmap. The current
    development platform is macOS; existing workflow definitions remain unchanged.
- [x] Generate/review universal dependency and official Actions transitive locks.
  - [x] Universal `runtime` and `audit` candidates genuinely resolved by uv 0.13.5, receipt-verified,
    runtime hash-install proven, audit hash-checked for the Linux target.
  - [x] Review completed: 7 initial advisories remediated (pytest, Pygments, setuptools, virtualenv,
    and packaging as the required cascade). Final candidates report **0 advisories**.
  - [x] Both profiles promoted into `engineering/` after review of versions, origins and
    advisories; `requirements.lock{,.json}` and
    `audit.lock{,.json}` now auto-verify as inputs change.
  - [x] Locked-qualification runs (TOBAC_REQUIRE_LOCK=1, `uv pip sync --require-hashes`):
    `tests` 495 passed / 91% coverage, `reproduce` five replays verified, `package` built both
    distributions, and the wheel installed and imported in a clean venv.
  - [ ] Official Actions transitive lock **rejected on review**: `gh actions-lock` produced
    `actions.lock` but only by replacing all 37 full-SHA action pins with mutable tags. Adopting
    tag+lockfile pinning is a security-policy decision, so the output was reverted. Open decision.
- [x] Complete macOS-focused qualification.
  - [x] Full scientific replay executed locally under the reviewed lock (verification/integrity only).
  - [x] `package` now succeeds under the reviewed lock; wheel install/import verified.
  - [x] Windows hosted failure root-caused to CRLF checkout changing hashed evidence bytes; fixed
    with `.gitattributes` (`* text=auto eol=lf`, `evidence/** -text`).
  - [x] Release-gate hermeticity defect found and fixed: three contract tests failed under
    `TOBAC_REQUIRE_LOCK=1` because the fixture inherited the release flag with an empty ROOT.
  - [x] Post-reconciliation macOS hosted qualification obtained at c645028 (PR #29).
    Non-macOS qualification is deferred to `conductor/roadmap.md`.
- [x] 2026-10-26 Python 3.15.1 locked local qualification: 611 tests passed (90% coverage),
  scientific reproduction and longitudinal output verification passed, package build and clean
  wheel install/import passed; native macOS quality/security checks and pip-audit passed.
  Receipt: `integration/engineering_hardening_python315_20261026.json`.
- [x] Whole-source `strict_all`: zero configured Ruff findings and zero BasedPyright
  errors across all source and CLI modules on the same Python 3.15.1 interpreter.
  See `docs/engineering/LINT_POLICY.md`: 175 explicit style/API exceptions are recorded
  separately from code corrections. No whole-project type diagnostics were disabled.
- [x] Confirm hosted macOS qualification at c645028; publish through expected-head guarded PR #29.
- [ ] Official Actions-lock policy decision remains open; existing full-SHA pins are retained.
  Linux/Windows qualification remains in the roadmap.

Record the receiving commit in the local Conductor track. Engineering configuration is not
external scientific qualification; the open hosted failure is not closed by this track.

## Phase: Review Fixes
- [x] Task: Align BasedPyright targets with Python 3.15 and verify review fix f06d0b5

## Reconciliation of PR #25

- [x] Preserve both development histories and reconcile the empirical runner and core.
- [x] Qualify scientific stubs on Python 3.15.1; focused runner reports zero type errors.
- [x] Reject incomplete mutation results and nonfinite/out-of-range thresholds.
- [x] Fresh source/tool-bound mutation run and repeat run verified; detection improved from
  79/131 to 92/131 (70.2%), with 39 survivors retained as a coverage limitation.
- [x] Local integrated Nox checks, runtime boundaries and clean wheel import verified.
- [x] Hosted macOS qualification at c645028: 721 passed, 93% coverage; all six
  engineering sessions pass; hosted mutation 100/131 killed (76.3%).
  Final documentation-only PR head must retain passing macOS checks before merge.
- [x] Commit final receipts and reconcile remote main through 8f9b98f.
- [x] PR #29 merged after both final-head macOS checks passed (run 40270043750).
  Receiving commit `104729a615e19ccf8da2cb52e729d46df624037d` verified on remote main.
  Optional Voiage installation probes remain blocked by upstream dependencies.

The parallel 916a41e profile attempt is retained in Git history as an uninformative run; it is
not substituted for the separate Python 3.15.1 profile receipt.

## Voiage Python 3.15.1 compatibility

- [x] Build a locally versioned metadata-only candidate from pinned Voiage 2.2.0 source;
  preserve implementation, native code and upstream licence. No dependency bypass.
- [x] Qualify resolver consistency, installed equal/weighted/partition EVPI and Arrow round trips.
- [x] Replace both incompatible hosted install routes with the same qualified source build.
- [x] Affected/full/macOS checks pass; all 15 hosted PR #33 checks pass.
  Verified receiving commit `f06eed630a8832174328a0472bdcaf55c98a4af9` on main.
  Receipt: `integration/voiage_python315_compatibility_20261026.json`.
