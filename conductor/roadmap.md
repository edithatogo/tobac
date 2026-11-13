# Roadmap

## Deferred access-dependent empirical expansion — 11 November 2026

These requirements are **out of active scope**, not waived or presumed complete. The 10 November phase-1 retrieval and screening programme identified 9,760 reports for full-text review, of which 2,183 have a PMC-accessible route and 7,577 require publisher/institutional access. The active public-only task can use the accessible subset with a prespecified targeted appraisal; it does not depend on resolving all 7,577. Do not attempt licence circumvention, institutional subscription use without authority, new requests, paid access or field collection as part of the current sprint.

Future applied work, **only with explicit owner permission and appropriate data-rights/governance arrangements**:

- Secure legal access and rights for non-open full texts/supplements that materially affect specific estimands; retain source edition, selection, rights, bias and quantitative extraction evidence.
- Acquire appropriately governed raw catchment flow, contributing populations, paired biomarker assays, processing/censoring, and independent product consumption/validation records where missing from public sources.
- Where justified, pursue consented/authorised individual-level or linked cohort transitions, service implementation and causal intervention-response evidence; no observation should be imputed from aggregate survey marginals.
- Assess eligible institutional, Māori/Indigenous, ethical, privacy and publication approvals before restricted-data work, collection or operational decision claims.
- Reopen the prespecified ≥3 complete prior-year/complete holdout-year and ≥4 comparable-catchment validation conditions only when actual compatible observations exist. They remain unchanged, not softened because they cannot presently be met.

The current independent public-only deliverable is an auditable *non-identification/decision-sufficiency methods* result, linked from [issue #3](https://github.com/edithatogo/tobac/issues/3) and the [empirical track](tracks/nz_au_empirical_20261106/index.md). Synthetic tests and conditional sensitivity analysis may validate methods but cannot validate observed NZ policy effects, target-specific WBE predictive performance or monetary study value.

This file records work intentionally deferred from active Conductor tracks. Items here are
planning commitments, not current development tasks, implementation authorization, or evidence
that a platform has passed qualification. There is no target date until the maintainer reprioritizes
the work.

## Cross-platform engineering qualification

Hosted Linux and Windows Python 3.15.1 runtime tests were restored and qualified by
PR #66 at receiving main `62056c5`; macOS remains the full engineering/reference
qualification platform. DXP1–DXP4 are complete for their declared workloads:

- [x] DXP1 — Installed and executed the source-bound Linux x86_64 audit lock on
  Python 3.15.1 in GitHub Actions run [41534684953](https://github.com/edithatogo/tobac/actions/runs/41534684953).
  All 96 locked packages match the installed inventory; strict/security sessions,
  96 focused tests and inspected artifact export pass. [Receipt](../integration/linux_audit_lock_20261103.json).
- [x] DXP2 — Qualified Linux/Windows package paths, dependency/extra markers,
  Unicode encodings and source/wheel build/install behavior in GitHub
  [run 41542664379](https://github.com/edithatogo/tobac/actions/runs/41542664379).
  Both direct and sdist-rebuilt wheels pass isolated imports/API/transport/quick CLI
  smokes and inspected export. [Receipt](../integration/package_portability_20261103.json).
- [x] DXP3 — Executed full scientific reproduction on Linux and Windows with
  Python 3.15.1 in [run 41557415490](https://github.com/edithatogo/tobac/actions/runs/41557415490).
  All eight runner variants and 82 scientific CSV tables match the accepted
  references within their declared policies; 29 isolated publication replay tables
  also pass on each host. [Receipt](../integration/scientific_reproduction_20261103.json).
- [x] DXP4 — Restored and qualified manual release and four-profile lock candidates.
  [Release run 41570769167](https://github.com/edithatogo/tobac/actions/runs/41570769167)
  passes seven Nox sessions, all eight scientific variants / 82 CSV tables,
  clean-package replay and inspected package upload on qualified Ubuntu 26.04.
  [Lock run 41567710835](https://github.com/edithatogo/tobac/actions/runs/41567710835)
  passes generation, source receipts, hash installation and exact installed-inventory
  readback for runtime, audit, Voiage and ecosystem. Six deliberate stale-source jobs
  reject before execution. [Receipt](../integration/manual_workflows_20261103.json).
  Candidates are review artifacts and have not replaced the committed locks.

Historical owner decision, 28 October 2026: Windows and Linux were not then
acceptance gates. PR #66 supersedes that decision for runtime tests. Retain the same scientific,
security, dependency-graph, provenance and numerical checks there. SourceRight
uses its hash-verified published macOS ARM64 binary on an ARM64 macOS runner;
the upstream asset filename misleadingly says x86_64.

The manual workflows are active under `.github/workflows/`, require explicit
source commits and export inspected evidence. The original definitions remain in
Git history. Scheduled lock generation stays disabled as optional automation;
DXP4 does not enable automatic adoption. macOS and Linux qualifications retain
separate receipts and platform scopes.

Superseded October runs and the first DXP4 failures remain historical evidence,
not passes. Fresh hosted qualifications above supersede the platform deferral
for these declared workloads. Branch protection and repository visibility are unchanged.

## Advisory CI/CD, automation, quality and security lane

Track: `conductor/roadmap/cicd_hardening_20261025/`.

DCI1 selection is complete: a bounded ty 0.0.95/Pyrefly 1.4.0 comparison and
Linux ARM64 static-diagnostic leg are selected; duplicate security/lint/action
wrappers and hook migration are omitted. [Decision](roadmap/cicd_hardening_20261025/selection_20261103.md).
DCI2–DCI4 are complete: the lane passed local and three-host qualification and was
published to main at `672894f` with receiving-tree verification. ARM qualification covers static
diagnostics and scanner execution only; scientific verifier profiles are unchanged.

## Optional macOS hardening follow-ups

These are improvements beyond the completed 26 October macOS acceptance scope, not
open execution gates or automatic implementation authorisation:

- [x] DH1 — Triaged all 12 supply survivors from PR #51; focused tests detect ten,
  and two are equivalent for the qualified SciPy call. A fresh local run detected
  129/131. [Evidence](../docs/reviews/2026-11-03-supply-mutant-triage.md).
- [x] DH2 — Reviewed the retained source/API Ruff exceptions; documented the reasons to
  retain them, including the scientific lineage impact of a tested refactor.
  [Review](../docs/reviews/2026-11-03-ruff-exception-review.md).

The earlier 100/131 and 102/131 mutation measurements and the 26 October inventory
of 175 source/style exceptions remain dated evidence, not current outstanding counts.
The separate bounded gremlins
campaign detected 68/68; its denominator does not replace mutmut. F6's non-macOS ARM
diagnostic execution remains deferred here; it is not an unchecked current macOS task.

## Reconciliation — 3 November 2026

DXP1–DXP4, DCI1–DCI4 and the two optional hardening tasks are complete.
The advisory lane is published and its receiving tree verified.
See [current status](status.md) for completed gates, open dependency-update PRs,
scientific requirements and the disposition of superseded decision drafts.

## Application-to-provider promotion — 8 November 2026

Status: maintainer-requested planning; implementation remains conditional on
qualified providers. Preserve current scientific assumptions, accepted reference
outputs, source/forecast identities, data-once guards, research gates and
no-outreach/no-submission boundaries. This plan is kept in the existing reviewed
roadmap path; no publication allowlist or security rule is relaxed.

### Responsibility

`tobac` remains a tobacco-specific research application. It is not a parallel
general diffusion, simulation, game-theory or VOI library. Promote reusable
methods to their authoritative provider only when a supported application need
and independent verification justify it.

| Reusable capability | Provider | What stays in tobac |
|---|---|---|
| Uptake, diffusion, competition, substitution, hype impact, repeat use | Innovate | Tobacco-product/state definitions, evidence, population assumptions and policy scenarios. |
| Simulation execution/time/resources/state/RNG | Kairos | Tobacco behaviour/process models and interpretation. |
| Decision uncertainty, perspective/equity and VOI | Voiage | Valuation choices, local costs/outcomes and application study design. |
| Generic game representation/solving | Paignia | Tobacco-market institutions, players, payoff construction and calibration. |
| Validated spline/surrogate fitting | MARS where appropriate | Domain training-design and approximation acceptance. |

Paignia is the reusable Rust provider at `edithatogo/paignia`. Its bounded
`paignia-core` / `paignia-solve` seed was transferred from reimbursement Track T17
at revision `12b22ce7571b9c590405bf53c2c1c5862b49cd64`. Source transfer is not
registry publication, broad solver qualification or acceptance by tobac. An
optional game adapter still requires an actual application need and TP02–TP04
evidence. VOP remains a separate proof of concept whose reusable decision
capabilities belong in Voiage after verification.

### Bounded execution leaves

Use existing engineering/test conventions. Each leaf changes one behaviour,
touches at most five files and records a failing assertion before implementation.
Resolve actual model/adapter paths before editing. Proposed test/ledger files
below are future work, not existing acceptance receipts.

#### [ ] TP01 — classify reuse candidates

Create `integration/provider-promotion-ledger.json` and
`tests/test_provider_promotion_ledger.py`. Inventory demonstrated methods; label
application-specific, existing-provider, reusable-candidate or unsupported. Test
that every generic candidate names one provider and no empirical gate is passed
by metadata. Run `python -m pytest tests/test_provider_promotion_ledger.py` with
nonzero tests. Do not infer method correctness from coverage or a publication
table. Review and register any new path under the existing publication policy
in the same bounded change; preserve all private bindings and history checks.

#### [ ] TP02 — independent scientific fixture before moving code

For one candidate, freeze a small independent numerical/reference case, its
parameter/data provenance and invalid-input controls. Extend existing evidence
contracts rather than duplicate acquisition. Distinguish adoption from repeated
consumption, switching and cessation; aggregate consumption is not first adopters.
Test that adding a provider does not silently change the study estimand or priors.
Promote/fix the method in the provider repository first.

#### [ ] TP03 — exact installed-provider migration

After upstream acceptance, change the adapter, focused test, dependency
manifest/lock and receipt; split if this exceeds five files. Require source and
package hashes, actual native dispatch, units/perspective/population/time/draw IDs
and known-reference output. A missing native provider fails explicitly on the
new path rather than invoking an undisclosed local replacement. Preserve the
accepted NumPy research baseline as an isolated reference during evaluation;
do not claim the existing application is already Rust-only.

#### [ ] TP04 — application reproduction and research boundaries

Run the existing scientific reproduction workflow with accepted source/input
identities. Compare affected published outputs and disclose scientifically
justified versioned differences; do not alter evidence to manufacture parity.
Preserve open empirical/posterior/decision-use gates. Test decision ranking and
uncertainty before adopting a surrogate or strategic model; speed alone is
insufficient.

#### [ ] TP05 — optional integration and release

Test that unrelated consumers do not acquire mandatory Innovate/Paignia/Kairos
imports. Feed Voiage explicitly valued joint outcomes, not raw consumption.
Feedback is an application-orchestrated strategy/study artefact, not a core
import cycle. Candidates follow exact security/build/numerical/consumer/resource
qualification and existing lock/source binding. No pin advance, retrospective
evidence rewrite or automatic package/manuscript publication is included.

### Coordination

Central policy: repository-standards PR #120. Innovate implementation/validation:
PR #570. Paignia extraction: reimbursement-game T17/PR #101. Kairos boundary:
PR #381. Voiage provider/VOP promotion: PR #1287. These proposed changes do not
supersede tobac's accepted scientific and provenance programme.

## Dynamic decisions, public evidence and systematic review — 8 November 2026

The [companion implementation plan](tracks/dynamic_frontier_20261108/plan.md) makes the next steps concrete: engineering/status fixes; a 282-record public comparison-data candidate; a small dynamic cohort reference; systematic review through Searchright; a joint empirical observation model; and adaptive policy/research decisions. The [design](tracks/dynamic_frontier_20261108/design.md) maps broader tax, retail, product, cessation, enforcement, health/fiscal, equity and surveillance decisions to their evidence needs. The [Searchright integration plan](tracks/dynamic_frontier_20261108/searchright.md) extends empirical requirement R01 through a qualified pilot, screening/extraction/synthesis, immutable evidence handoff and an on-demand living update. These proposals preserve TP01–TP05 provider ownership and all existing source, scientific and publication gates.

## Beyond-frontier capabilities and maintained-dependency co-design — 9 November 2026

To advance `tobac` and its maintained upstream provider ecosystem beyond published 2026 state-space nicotine allocation (ABS), cohort transition preprints (SHINE-Tobacco), static wastewater VOI (Impalli et al.), and i.i.d. robust decision updating (Cheng), the following co-designed application and provider enhancements are scheduled under the existing TP01–TP05 promotion gates:

| Capability domain | Maintained provider improvement | `tobac` domain integration |
|---|---|---|
| **Credal / LP decision sufficiency & Minimal Identifying Restrictions (MIR)** | **`edithatogo/voiage`**: add polyhedral/credal-set pairwise dominance ($\underline{\Delta}(a,b)$), minimax regret, primal attaining witnesses $(\theta_{\min}, \theta_{\max})$, dual Farkas non-dominance/infeasibility certificates, set-valued (upper/lower) EVSI bounds, and Minimal Identifying Restriction (MIR) solvers. | **`tobac.partial_identification` (F1/BF1)**: encode NZHS four-category daily-use crosswalks, lawful-release ledgers, censored wastewater slots and transport bounds; retain a small exact vertex-enumeration oracle for test parity. |
| **Endogenous observation-process & Tobit-censored VOI** | **`edithatogo/voiage` + `edithatogo/kairos`**: in `voiage`, support action-indexed observation operators $y_t \sim H(x_t, a_t, \eta_t)$ and left-censored (Tobit/LOD) channel EVSI without censored-value imputation; in `kairos`, provide three-clock orchestration (physical state, delayed assay arrival, decision epoch) with structural non-anticipativity guards. | **`tobac_supply.dynamic` & `tobac.research.staged` (F2/F3/BF2)**: couple VLNC/vaping/pouch policy actions to alkaloid-to-product identifiability and catchment LOD/LOQ censoring schedules. |
| **Semi-Markov exposure memory & Polars-native diffusion** | **`edithatogo/innovate` + `edithatogo/dapane`**: in `innovate`, remove legacy `pandas`/`pandasdmx` requirements in favour of the Polars/Arrow interchange contract and add reusable tunnel-state / multi-component hazard-decay cohort primitives; in `dapane`, qualify perspective-explicit microcosting and discount-schedule ledgers separating resource costs from excise transfers. | **`tobac.health` & `tobac_supply.dynamic` (F02/F04)**: represent fast/slow post-cessation excess-hazard decay (cardiovascular vs. lung cancer) against an exact convolution oracle without state-space explosion. |
| **Two-tier Merkle lineage & living-evidence invalidation cones** | **`edithatogo/archive-govt-nz` + `edithatogo/searchright` / `sourceright` / `citeweft`**: in `archive-govt-nz`, split the flat inventory digest into a **Runner Closure Merkle Root** (transitive AST/imports + declared runner inputs) and a **Candidate Evidence Registry Merkle Root** with fine-grained invalidation cones (`source -> extraction -> parameter -> bound -> decision`); in `searchright`/`sourceright`/`citeweft`, preserve CSL item kinds (book/chapter) across CSV/CSL round-trips and emit signed retraction/erratum diff manifests. | **`scripts/scientific_lineage.py` & `hosted_lineage.py` (F5/BF5)**: allow staging candidate evidence packs without invalidating unchanged runner closures, and automatically trace which action rankings change when a source is revised or withdrawn. |
| **Metamorphic property suites & process-group monitor resilience** | **`edithatogo/repository-standards` + `edithatogo/voiage` + `edithatogo/paignia`**: in `repository-standards`, scope macOS RSS sampling to the owned process group (`ps -g <pgid> -o pgid=,rss=`) rather than system-wide `ps -axo` scans that stall on uninterruptible third-party processes; in `voiage` and `paignia`, export Hypothesis strategies for Blackwell garbling monotonicity, dominance transitivity and equilibrium-set inclusion. | **`tests/` & `scripts/run_bounded.py` (H1/H2)**: enforce Hypothesis metamorphic laws for time-subdivision convergence (`exposure_health_step`), constraint monotonicity (`partial_identification`), and Blackwell monotonicity (`information.py`). |
