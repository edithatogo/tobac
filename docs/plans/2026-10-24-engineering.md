# Library reuse and engineering implementation plan

Goal: replace commodity numerical code where parity is demonstrable; qualify engineering and context using existing tools without changing empirical assumptions.
Base: bb81a4bd596b2560a85e0cd10e9f9c8656408492. The current main and issue #1 take precedence over historical archives.

1. Audit current numerical, validation, evidence and workflow interfaces; preserve M3's owned namespaces.
2. Test and replace manual Gaussian log density with SciPy's Covariance/multivariate_normal, preserving shape, covariance and physical-domain contracts.
3. Use JSON Schema for bounded context/receipt contracts, Nox+uv for execution, pytest/Hypothesis for invariants, Ruff/BasedPyright for static quality, and pip-audit/SBOM tools for supply-chain checks. Do not implement another agent scheduler or VOI engine.
4. Add minimal role-based context with source hashes, commit/dirty-state records, task budgets, science-vs-execution gates and an explicit untrusted-evidence boundary.
5. Add tiered, SHA-pinned, least-privilege CI and manually gated release artefacts. Fast numerical/parity checks remain separate from strict legacy-debt audits, expensive mutation/profile work and experimental upgrades.
6. Verify local executable scope; record unavailable tools, failed network access and hosted limitations rather than marking configurations as passed.
7. Re-read main/#1, reconcile concurrent writes, publish additive changes through expected-head checks, then verify receiving files/commit.

Review focus: scientific/evidence invariants, singular covariance, shape regression, path traversal or secret inclusion, stale context, unsupported execution claims, private-artifact publication and races with M3. No current NZ funding conclusion is inferred.
