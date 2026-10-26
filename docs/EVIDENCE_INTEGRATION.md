# Executable evidence integration

Dylan A Mordaunt | 25 October 2026 | Initial base: 5218d831; reconciled receiving base: fa39fd36cd924d21128a154d19f86bf0cab95bd6

## What this closes
The historical reference snapshot had been copied and tested, but the shared reproduction
session did not explicitly verify it. The external citation job covered the root and M2
bibliographies, not the longitudinal or preserved collections. This change connects those
materials to the existing execution paths without changing scientific models or inputs.

The existing `scripts/qualify_integrations.py` now has an offline inventory mode. It calls
`scripts/verify_prior_work.py`, then inventories every `*.csl.json` file below `evidence/`.
The four existing collections are required; additional collections are discovered automatically.
Missing or malformed collections, duplicate identities within a file and symlinks fail closed.
Source hashes and literal citation identities are recorded, not rewritten or merged.

```sh
python scripts/qualify_integrations.py --mode inventory --out outputs/evidence-inventory.json
# Optional archive-level provenance check, in addition to normal preserved-byte verification:
python scripts/verify_prior_work.py --archive /path/to/tobac_v2.9.0_20261024_EMPIRICAL_LONGITUDINAL.zip
```

At the audited base there are four collections and 43 reference-record occurrences, including
repeated entries and aliases. These counts are NOT numbers of independent studies. The
preserved snapshot still has 19 files, 298 mixed-purpose CSV rows and 28 inherited records.
No parameter, observation, cost assumption, source version or reference record was changed.

## How it is used
The Nox `tests`, `reproduce`, `package` and `research_m3` sessions run the inventory before environment setup.
A failed gate stops the session. An additional `evidence` session performs only this offline
standard-library check. Session-specific receipts avoid overwriting each other's evidence.
Use fresh output paths; existing execution receipts are never silently replaced.

The regulatory and longitudinal scientific workflows run the same preflight and retain its
receipt with their outputs. The engineering matrix and internal candidate inherit the Nox
gate; their locks, scientific checks and external qualification requirements are not weakened.

The pinned Sourceright job now uses the real CLI on every bibliography, rather than only two:

```sh
python scripts/qualify_integrations.py --mode sourceright --all-csl --out outputs/sourceright-all.json
```

Each result records its file/hash, command, exit status or timeout, stdout and stderr. A failure
in one collection does not hide the remaining attempts; any failure keeps the overall result
unsuccessful. Source and executable changes during the check invalidate success. Missing
Sourceright returns an explicit unsuccessful receipt, never a fabricated validation result.
The original single-collection interface and 51-case equal-weight voiage probe remain available.
M3 owns the broader weighted/portfolio/staged interfaces and is not replaced by this change.
A regression test also exposed that Python max-error aggregation could overlook a nonfinite
VOI result after an earlier finite result. The equal-weight probe now explicitly rejects NaN
and infinite values; valid finite test cases and their 51-case scope are unchanged.

## Context and scientific boundaries
`engineering/context/evidence.json` is an optional bounded profile for the existing context
builder. It includes authoritative instructions, provenance, the parameter register and these
execution boundaries. It does not add an agent, activate a plugin, or run in the background.

An inventory pass establishes preserved bytes and internal identity, not CSL schema validity.
A genuine Sourceright CLI pass would establish its stated structural checks, not provider-backed
claim verification, causal applicability or independence. Neither pass updates `tobac.evidence`
or a live posterior. M1/M2/M3 source-identity, time/unit/population and dependence requirements
remain authoritative. In particular, preserved assumptions, forecast paths and old posterior
samples do not become newly observed current NZ data. Request templates remain unsent templates,
not quotations. Superseded engines/manuscripts in the predecessor archive remain outside the
active code unless separately reviewed and mapped.

Actual executed tests, archive checks, missing-library attempts and scope limitations are in
`integration/evidence_execution_verification_20261025.json`. The inventory receipt is in
`integration/evidence_inventory_20261025.json`. These are local scoped evidence; hosted success,
full scientific replay and genuine third-party validation remain separate.

The tracked inventory receipt documents the 2026-10-25 pass at base `5218d83`. One digest in it
is now stale: the longitudinal CSL file gained its PMCID in commit `005364e`, changing
`evidence/longitudinal/references.csl.json` from `cf853de8…` to `af009648…`; every other field
still matches the live CLI output. Re-inventory current bytes with
`python scripts/qualify_integrations.py --mode inventory --out <fresh path>` or `nox -s evidence`.
The source-archive comparison in the execution receipt was run against a predecessor ZIP that is
not retained in this repository, so it is an executed-at-the-time claim, not a reproducible gate.

## Concurrent M3 reconciliation
M3 arrived on main during this pass at fa39fd36cd924d21128a154d19f86bf0cab95bd6. Its source,
configurations, 24 saved output files, dedicated workflow and verification records are preserved
by using that commit as the receiving base. The live Nox and Conductor file hashes were checked
before combining additions. The M3 Nox session retains its tests/runner/verifier and adds the
same fail-stop evidence preflight. Shared `reproduce` now runs M1, M2, M3 and both longitudinal
analyses, so internal candidates cannot omit M3 merely because it has its own workflow.

Two additional command-contract checks bring this pass to 60 tests. They do not constitute
re-execution of the M3 scientific model, genuine Nox, or its released-Voiage qualification.
The current M3 incorporation status supersedes the initial pending-work observation.
