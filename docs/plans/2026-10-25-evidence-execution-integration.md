# Evidence execution integration plan

Goal: connect restored historical material to existing shared verification, without changing scientific models.
Initial base: 5218d831. Reconciled onto concurrently published M3 at fa39fd36cd924d21128a154d19f86bf0cab95bd6; M3-owned code remains untouched.
Design: extend the existing integration qualification CLI. Reuse the prior-work verifier and genuine Sourceright CLI; do not create another evidence model, citation resolver or package manager.

- [x] Add failing CLI/integration tests for complete inventories, missing material and external failures.
- [x] Add offline inventory mode and all-collection Sourceright mode, with per-file hashes and explicit execution status.
- [x] Connect inventories to Nox tests/reproduction/packaging and existing scientific CI preflight.
- [x] Add a bounded evidence-context profile and documentation of the restored data's roles.
- [x] Exercise actual copied source bytes and original archive; record missing tools honestly.
- [x] Reconcile concurrent M3 Nox/Conductor additions; include M3 in shared reproduction and rerun 60 scoped tests.
- [ ] Re-read current main, publish guarded additive updates, verify hashes and receiving commit.

Acceptance: every required bibliography is covered, future additional bibliography collections are discovered,
missing/malformed/changed/symlinked input fails, all external attempts are recorded, and no inventory pass is
labelled CSL validation, source-applicability review or an empirical posterior update. No new observations,
quotes, policy effects, priors or rankings. Fixture-backed library tests are not installed-library qualification.
