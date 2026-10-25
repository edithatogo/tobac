# Plan and status

- [x] Inspect live main, shared contracts, dependency manifests, workflows and #1/#4.
- [x] Review adopted/deferred existing-library alternatives and document semantic boundaries.
- [x] Write failing backend requirement test; implement SciPy replacement; preserve tiny-SPD shape/domain semantics.
- [x] Write context tests before implementation; validate with real jsonschema; reject stale/unsafe/unbounded profiles.
- [x] Run the imported 151 tests, 26 existing cross-workstream tests and new executable checks.
- [x] Define secure bounded matrix/deep/canary/internal-candidate lanes with maintained tools and full action pins.
- [x] Attempt real dependency-lock generation; record the uncached/offline failure without a fake lock.
- [x] Add reviewed context profiles, small agent skill, Conductor project context and pinned upstream gitlink definition.
- [~] Execute new Nox/Ruff/BasedPyright/Hypothesis/mutation/security/profile tooling in a capable environment.
  - [x] 2026-10-25 at 044c995: real Nox `tests` (495 passed, 91% coverage) and `reproduce`
    (M1/M2/M3/longitudinal, all verifiers pass) executed in **bootstrap** mode.
  - [x] Ruff (both invocations), BasedPyright strict, zizmor and pip-audit executed and **green**
    after fixing three real defects they exposed.
  - [x] 2026-10-25 gap-closure pass: mutation (mutmut 3.7.0) executed natively on
    `src/tobac/supply.py` — 128 mutants, 79 killed, 49 survived (61.7%). The session passes
    because mutmut enforces no threshold; the survivor count is a recorded weakness, not a pass.
  - [x] 2026-10-26 Python 3.15.1 Scalene quick profile executed; artifact hash and scope are in
    `integration/engineering_hardening_python315_20261026.json`.
  - [ ] The Nox `audit` profile (Linux-scoped lock) itself remains unexecuted on Linux. A
    `audit_tools()` path now runs the same quality/security checks host-natively and labels
    itself `NATIVE AUDIT ... NOT release qualification`; the Linux profile stays authoritative.
- [x] Generate/review universal dependency and official Actions transitive locks.
  - [x] Universal `runtime` and `audit` candidates genuinely resolved by uv 0.13.5, receipt-verified,
    runtime hash-install proven, audit hash-checked for the Linux target.
  - [x] Review completed: 7 initial advisories remediated (pytest, Pygments, setuptools, virtualenv,
    and packaging as the required cascade). Final candidates report **0 advisories**.
  - [x] Both profiles promoted into `engineering/` after review of versions, origins, licences
    (89 packages, no copyleft/unknown) and advisories; `requirements.lock{,.json}` and
    `audit.lock{,.json}` now auto-verify as inputs change.
  - [x] Locked-qualification runs (TOBAC_REQUIRE_LOCK=1, `uv pip sync --require-hashes`):
    `tests` 495 passed / 91% coverage, `reproduce` five replays verified, `package` built both
    distributions, and the wheel installed and imported in a clean venv.
  - [ ] Official Actions transitive lock **rejected on review**: `gh actions-lock` produced
    `actions.lock` but only by replacing all 37 full-SHA action pins with mutable tags. Adopting
    tag+lockfile pinning is a security-policy decision, so the output was reverted. Open decision.
- [~] Verify hosted matrix, full scientific replay, package install, licensed attestations and independent review.
  - [x] Full scientific replay executed locally under the reviewed lock (verification/integrity only).
  - [x] `package` now succeeds under the reviewed lock; wheel install/import verified.
  - [x] Windows hosted failure root-caused to CRLF checkout changing hashed evidence bytes; fixed
    with `.gitattributes` (`* text=auto eol=lf`, `evidence/** -text`). Hosted re-run pending.
  - [x] Release-gate hermeticity defect found and fixed: three contract tests failed under
    `TOBAC_REQUIRE_LOCK=1` because the fixture inherited the release flag with an empty ROOT.
  - [ ] Hosted matrix confirmation, licensed attestations and independent review not obtained.
- [x] 2026-10-26 Python 3.15.1 locked local qualification: 611 tests passed (90% coverage),
  scientific reproduction and longitudinal output verification passed, package build and clean
  wheel install/import passed; native macOS quality/security checks and pip-audit passed.
  Receipt: `integration/engineering_hardening_python315_20261026.json`.
- [ ] Remaining Python 3.15.1 gates: post-migration hosted matrix, Linux execution of the locked
  audit profile, licensed attestations, independent review, and the open official Actions-lock
  security-policy decision.
- [ ] `strict_all` is measured, not green: 4,861 ruff `--select ALL` errors and 2,235
  BasedPyright-all errors across the whole source. Pre-existing and previously never executed;
  recorded as an open gate rather than claimed (26 October Python 3.15.1 measurement).

The publication receipt on issue #1 names the receiving commit. Engineering configuration is
not external scientific qualification; the open hosted failure is not closed by this track.

## Phase: Review Fixes
- [x] Task: Align BasedPyright targets with Python 3.15 and verify review fix f06d0b5
