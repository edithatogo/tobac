# Shared workflow

1. Read live main, issue #1, AGENTS.md and the affected scientific contracts. Declare owned paths.
2. Choose a bounded context profile; record commit, source hashes and dirty state. Do not ingest
   all prior archives. A changed HEAD or source invalidates a prior context receipt.
3. Write the scientific/engineering scope and tests. Compare an existing library before new
   generic code. Preserve reference oracles, input units, shared identities and data-once rules.
4. Execute affected and cross-workstream tests. On a complete checkout run full test/reproduction
   sessions. Record unavailable checks without substituting a mock or self-authored receipt.
5. Review diffs, assumptions, failure cases and actual commands. An agent role is not an external
   scientific endorsement. Keep empirical calibration, metadata, software and security gates apart.
6. Re-read current main/#1. Reconcile concurrent edits, then guarded publication, remote readback
   and a coordination receipt. Never force-update a diverged workstream or weaken CI to get green.

The pinned vendor/conductor submodule is upstream tooling, not these project plans. Its host
checkout/activation must be verified separately. No automatic background worker is installed.
