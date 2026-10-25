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
  - [x] Partial 2026-10-25 at 044c995: real Nox `tests` (495 passed, 91% coverage) and `reproduce`
    (M1/M2/M3/longitudinal, all verifiers pass) executed on macOS in **bootstrap** mode.
  - [ ] Ruff, BasedPyright, mutation, security and profile remain unexecuted: the `audit` profile is
    Linux-only by design and no Linux container/VM was started.
- [ ] Generate/review universal dependency and official Actions transitive locks.
  - [x] Universal `runtime` and `audit` candidates genuinely resolved by uv 0.13.5, receipt-verified,
    hash-install proven for runtime and dry-run hash-checked for the Linux audit target.
  - [ ] Review outcome is **not** a pass: pip-audit found 7 advisories in 3 packages (pygments 2.19.2,
    pytest 9.0.2, setuptools 82.0.1). Candidates are deliberately not committed to `engineering/`.
  - [ ] Official Actions transitive lock not generated.
- [ ] Verify hosted matrix, full scientific replay, package install, licensed attestations and independent review.
  - [x] Full scientific replay executed locally on the bootstrap profile (verification/integrity only).
  - [ ] `package` aborts on the reviewed-lock gate as designed; hosted matrix, attestations and
    independent review not obtained.

The publication receipt on issue #1 names the receiving commit. Engineering configuration is
not external scientific qualification; the open hosted failure is not closed by this track.
