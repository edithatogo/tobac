# Current repository status

## Research scope

The active deliverable is a public-evidence feasibility, non-identification and
decision-sufficiency study. Use existing public material and permitted archive
copies. The current milestone keeps restricted-source access, custodian requests,
new collection and external submission outside its scope.

- The [empirical track](tracks/nz_au_empirical_20261106/index.md) records the
  public appraisal and source reconciliation. The
  [first-comparison audit](tracks/nz_au_empirical_20261106/first-comparison-audit-20261109.json)
  records the missing compatible baseline, wastewater and independent outcome
  observations. The applied comparison remains open in
  [issue #3](https://github.com/edithatogo/tobac/issues/3).
- The [research gates](research-gates.md) carry identification, calibration,
  provenance, governance and permissible-use decisions. The
  [roadmap](roadmap.md) records access-dependent work and the steps to qualify
  an upstream provider for a specific application need. The
  [library reuse review](../docs/engineering/LIBRARY_REUSE_REVIEW.md#first-provider-use-case)
  records the first Voiage use case.
- Follow the [manuscript checkpoint](workflow.md#manuscript-checkpoint) and
  paper-specific records for author facts, declarations and approval. The
  [dynamic methods track](tracks/dynamic_frontier_20261108/index.md) records
  candidate methods and their remaining empirical requirements.

## Engineering and dependency maintenance

- Protected pull requests run the five required jobs. Use the
  [Engineering workflow](../.github/workflows/engineering.yml) for their
  definitions and [PR #193](https://github.com/edithatogo/tobac/pull/193) for
  the last quality-session consolidation.
- Engineering owns the hosted Voiage qualification. Its single macOS job runs
  both the locked application suite and the exact published-wheel check. The
  [Voiage guidance](../docs/engineering/VOIAGE_PYTHON315.md) records the two scopes.
- The package portability and scientific reproduction workflows skip a
  `main` push that only changes this status page. Use their manual dispatch
  routes for an explicit cross-platform qualification.
- Renovate groups `jax` and `jaxlib`. Review the ecosystem lock and actual
  native execution together before adopting the next candidate. The
  [maintenance guide](../docs/engineering/DEPENDENCY_MAINTENANCE.md) gives
  the lock, security and dependency graph requirements.

## Verification and remaining work

- Baseline `5809c50` passed [alint and RepoHealth](https://github.com/edithatogo/tobac/actions/runs/44985096496).
  The revised workflows require the owner-held signature renewal and hosted
  verification before publication. Both Voiage sessions keep their existing
  numerical and installed-library checks.
- The [Scorecard run](https://github.com/edithatogo/tobac/actions/runs/44981202222)
  records the dependency-pinning fixes. The remaining findings concern
  [fuzzing recognition](https://github.com/edithatogo/tobac/security/code-scanning/33),
  [repository age](https://github.com/edithatogo/tobac/security/code-scanning/38),
  [review activity](https://github.com/edithatogo/tobac/security/code-scanning/39)
  and [badge registration](https://github.com/edithatogo/tobac/security/code-scanning/40).

## History

Use the [tracks registry](tracks.md) for track dispositions and the
[archive index](archive/index.md) for completed plans. The
[status record through 22 November 2026](https://github.com/edithatogo/tobac/blob/5809c50e425e82b8caff09acb057867b8725ce6e/conductor/status.md)
retains the dated acceptance receipts, scope decisions and superseded checkpoints
in their published edition.
