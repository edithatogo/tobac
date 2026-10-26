# Shared workflow

1. Read the current base, AGENTS.md and affected scientific contracts. State the intended scope.
2. Choose a bounded context profile; record commit, source hashes and dirty state. Do not ingest
   all prior archives. A changed HEAD or source invalidates a prior context receipt.
3. Write the scientific/engineering scope and tests. Compare an existing library before new
   generic code. Preserve reference oracles, input units, shared identities and data-once rules.
4. Execute affected and cross-workstream tests. On a complete checkout run full test/reproduction
   sessions. Record unavailable checks without substituting a mock or self-authored receipt.
5. Self-review diffs, assumptions, failure cases and actual commands. Keep empirical calibration,
   metadata, software and security gates apart. Independent review is optional and is not a gate.
6. Re-read current main, reconcile any changes, then use guarded publication and verify remote
   readback. Never force-update or weaken CI to get green.

The pinned vendor/conductor submodule is upstream tooling, not these project plans. Its host
checkout/activation must be verified separately. No automatic background worker is installed.
