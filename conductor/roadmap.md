# Roadmap

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

Paignia is a working name for the Rust capability incubated in
`new-drug-reimbursement-game` Track T17; no extracted repository or published
`paignia-*` dependency is asserted. An optional game adapter requires an actual
application need. VOP is a separate proof of concept whose generic decision
capabilities belong in Voiage.

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
