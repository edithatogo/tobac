# Plan and status

- [x] Inspect live main, shared contracts, dependency manifests, workflows and #1/#4.
- [x] Review adopted/deferred existing-library alternatives and document semantic boundaries.
- [x] Write failing backend requirement test; implement SciPy replacement; preserve tiny-SPD shape/domain semantics.
- [x] Write context tests before implementation; validate with real jsonschema; reject stale/unsafe/unbounded profiles.
- [x] Run the imported 151 tests, 26 existing cross-workstream tests and new executable checks.
- [x] Define secure bounded matrix/deep/canary/internal-candidate lanes with maintained tools and full action pins.
- [x] Attempt real dependency-lock generation; record the uncached/offline failure without a fake lock.
- [x] Add reviewed context profiles, small agent skill, Conductor project context and pinned upstream gitlink definition.
- [ ] Execute new Nox/Ruff/BasedPyright/Hypothesis/mutation/security/profile tooling in a capable environment.
  - [x] 2026-10-25 at 044c995: real Nox `tests` (495 passed, 91% coverage) and `reproduce`
    (M1/M2/M3/longitudinal, all verifiers pass) executed in **bootstrap** mode.
  - [x] Ruff (both invocations), BasedPyright strict, zizmor and pip-audit executed and **green**
    after fixing three real defects they exposed.
  - [ ] Mutation (mutmut) and profiling (Scalene) not executed; tools installed natively only.
  - [ ] The Nox `audit` profile itself remains unexecuted: it is Linux-gated to protect the
    Linux-scoped lock install, so these checks ran natively on macOS rather than in that session.
- [ ] Generate/review universal dependency and official Actions transitive locks.
  - [x] Universal `runtime` and `audit` candidates genuinely resolved by uv 0.13.5, receipt-verified,
    runtime hash-install proven, audit hash-checked for the Linux target.
  - [x] Review completed: 7 initial advisories remediated (pytest, Pygments, setuptools, virtualenv,
    and packaging as the required cascade). Final candidates report **0 advisories**.
  - [ ] Candidates are recorded in `outputs/engineering/lock-candidate` but deliberately **not**
    copied into `engineering/`; promotion is an explicit human review action.
  - [ ] Official Actions transitive lock not generated.
- [ ] Verify hosted matrix, full scientific replay, package install, licensed attestations and independent review.
  - [x] Full scientific replay executed locally on the bootstrap profile (verification/integrity only).
  - [ ] `package` aborts on the reviewed-lock gate as designed; hosted matrix, attestations and
    independent review not obtained.

The publication receipt on issue #1 names the receiving commit. Engineering configuration is
not external scientific qualification; the open hosted failure is not closed by this track.
