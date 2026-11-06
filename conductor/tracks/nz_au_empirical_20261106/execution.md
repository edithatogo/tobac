# Execution by enablement and data maturity

Status: design contracts, not an installed lake or executable gate implementation.
Use existing external repositories/storage; no new platform or data copies in tobac.
Platinum is this project's decision/reporting layer, not a universal medallion standard.
Layer promotion never implies empirical validity, human approval or permission to publish.

## Work packages and dependencies

| Package | Enabling tools and responsibility | Depends on | Done when |
|---|---|---|---|
| E0 Runtime | Python 3.15.1, uv/locks, Nox, Polars/Arrow; existing dependency owner | Baseline ownership | Actual installed versions, parity and lock receipts verified |
| E1 Evidence access | Searchright, existing external archive producer, GitHub/HF supported APIs | E0 for execution | Exact sources/destinations, rights and retrieval/readback qualified |
| E2 Data contracts | Existing Scope/EvidencePacket/SupplyBasis; schema and unit validation | E1 | Bronze-to-silver validation and quarantine pass |
| E3 Analytics orchestration | Logged DAG, manifests, resources, seeds, recovery; requested Snakemake qualification | E0 | Failed/stale inputs rejected; resume and offline replay proven |
| E4 Scientific engine | Existing tobac/tobac_supply and reference oracles; health/equity modules | E2, E3 | Gold model inputs and outputs validated for declared scope |
| E5 Decision methods | Voiage and Innovate actual qualified adapters | E4 | VOI, uptake and competition agree with bounded reference cases |
| E6 Interpretation | PSA, clustering, held-out prediction and report generation | E4; E5 when used | Platinum results traceable with calibrated claims |
| H Hardening | Existing lint/type/security/package/CI controls | Starts at E0; release follows E6 | Separate hardening track acceptance |

These packages regroup plan.md; they do not create duplicate implementation tasks.
Read-only discovery may overlap E0, but execution cannot bypass dependencies.

## Medallion contracts

| Layer | Contents and ownership | Promotion gate |
|---|---|---|
| Bronze | External immutable original PDFs/workbooks/API responses, query receipts, rights, timestamps and source hashes; evidence producer owns bytes | Retrievable original, exact hash, source/version identity, access/rights status; failures quarantined |
| Silver | External versioned verified extractions and canonical typed observations; preserve country, dates, products, denominators, units, uncertainty and shared-source IDs | Source cell/page verification, dimensional/total reconciliation, schema checks, duplicates and covariance provenance; no invented missing values |
| Gold | Analysis-ready scoped inputs, accepted parameter distributions, formula/model registry, calibrated states and simulation ensembles | Target applicability, identifiability, dependence/data-once checks, versioned assumptions, model validation and numerical checks; distinguish observed, inferred and synthetic |
| Platinum | Decision comparisons, equity/frontiers, VOI, sensitivity, cluster validation and reproducible reports with limitations | Run/input/formula/environment hashes, convergence and holdout evidence, perspective/cost consistency, permissible-use scope and release checks |

Gold model-derived records must never return to Silver as new observations. Country remains
an explicit key through every layer; harmonisation does not erase differences in policy.
Store allowed metadata/pointers in Git, originals and derived datasets externally under their
rights. Content-addressed references and manifests bind all layers without copying the lake.

Every promotion receipt must identify input/output hashes, schema/transform version, source
and target scope, command, actual environment, timestamps, verification outcome and exclusions.
Stage outcome vocabulary: passed, failed, blocked, not_run. A skipped check is not passed.
Quarantine retains reason and original identity. Corrections create new editions; descendants
are invalidated and recomputed selectively. Missing legal/geographic/measurement applicability
can block Gold while leaving a valid Silver extraction useful for contextual analysis.

## Task contract for constrained coding agents

Execute one bounded task at a time. Before editing, create a task card with:

1. Stable task ID and linked requirement IDs; one observable deliverable.
2. Exact base commit/worktree/owner and allowed files; prohibited native writes.
3. Prerequisite receipts, immutable input references and required schema versions.
4. Existing implementation/API to reuse and explicit scientific invariants.
5. Exact commands with repo-local interpreter, bounded runner, log destination and selectors.
6. Positive and negative acceptance cases, expected units and numerical tolerances with rationale.
7. Stop conditions and rollback preserving other work; maximum execution budget, zero blind retries.
8. Output paths/hashes, actual command/exit status and evidence links; next unblocked task.

Do not execute a task card with unresolved placeholders. Resolve ordinary implementation
choices from code/help first. Stop dependent work on an ambiguous scientific estimand,
unknown units, unavailable data, ownership conflict or failed prerequisite; continue only
independent tasks. Never fabricate an input, receipt, successful test or API. Never weaken
checks, alter old evidence or broaden file ownership to make a task pass.

Each implementation phase must first instantiate its task cards from this template. Cards
are not executable automation until exact commands are qualified. Add machine-checkable
schema/receipt validators in E2/E3; prose alone cannot prevent agent mistakes. Small commits,
focused diff review and a terminal handoff reduce recovery costs. A second agent is optional.

## Further refinements

- Prespecify decision-relevant accuracy, numerical error budgets and validation tolerances.
- Use identical seeded draws/common random numbers for paired policy comparisons where valid;
  keep independent validation seeds and report Monte Carlo standard errors.
- Maintain a source-to-claim graph and a model/parameter applicability matrix, not just citations.
- Require subgroup sample-size/uncertainty disclosure; do not turn unstable clusters into policy targets.
- Separate acquisition, empirical identification, computational and governance blockers.
- Define a minimal useful result and stop expansion when additional complexity cannot be validated.
