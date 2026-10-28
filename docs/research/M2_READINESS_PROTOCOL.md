# Post-primary manuscript and robustness protocol

28 October 2026, frozen before new numerical challenge execution. The primary
analysis in results/m2_publication_20261028/ and its protocol are historical inputs;
this extension is not preregistered. Four initial scoping queries preceded this
freeze; four targeted queries identified prior methodological work. Search metadata
is saved separately. No results of the new robustness challenges have been inspected.

The numerical target is a synthetic 1,000-resident catchment, smoked cigarette-
equivalent consumption and a one-year response. NZ residents aged 15+ and an
approximately 600-retailer contrast remain a separate, unqualified applied context.
Do not silently rescale the catchment, claim lifetime benefits or calibrate a policy.

## Fixed challenge design

configs/m2_robustness.json declares 13 challenge specifications, each crossed with
all five existing structural cases and the same 25 value profiles (health weight1).
Keep all ties. No weights/probabilities over challenges, structures or value profiles.

Baseline reproduces the existing prior/consequences/report channels. Reweight high
illicit, diversion or crime support probabilities to 0.2/0.8 as declared, preserving
other independent supports. Market/diversion dependence moves their high/high joint
probability 80% from independence toward its positive or negative Fréchet bound,
with both marginal probabilities preserved. This parameter is not Pearson rho.

Null-mass challenges use 0 or 0.8; transport remains case-specific. A zero-transport
case still collapses to zero retail cessation whatever the null mass. These are
assumptions, not posterior probabilities or elicited beliefs.

The shared-report-error challenge mixes 20% conditionally independent joint report
probabilities with 80% common-uniform (comonotonic ordered-bin) coupling conditional
on each state. Each individual report's marginal likelihood is preserved. This is
one hypothetical positive dependence alternative, not a fitted shared-error model
or an exhaustive dependence bound. Single-report/no-information designs are unchanged.

The half-information challenge mixes each full study likelihood equally with its
prior-predictive state-independent report distribution. This is a stochastic
unobserved garbling of the existing report. For the same prior and objective,
EVSI cannot increase; check that invariant. The combined scenario applies the
explicit high probabilities, null mass, positive coupling, shared reports and
half-information sequentially; it is not named or interpreted as a universal worst case.

For every profile compute expected-action values, all co-optimal policies, EVPI,
seven grouped EVPPI partitions before six gross study EVSI values, all study/group
co-optimal sets and current-prior regret from reusing baseline-optimal actions.
Report the min/max regret over baseline ties without arbitrary tie breaking. Compare
challenge choices to baseline on exact case/value keys; counts are finite-grid counts,
not preference frequencies or risk probabilities. Retain no-information comparator.

## Public-method literature and reporting

Bounded English-language search of four topic streams: VOI reporting; preference vs
prediction uncertainty; model parameter/dependence uncertainty; robust decisions.
Initial/scoping and targeted query strings are logged, with engine/ranking limitations.
Include primary articles, author institutional manuscripts and official reporting
sources. Exclude tertiary summaries, duplicate mirrors and unrelated applications;
log the candidate dispositions. Trace a bounded one-hop set of the most relevant
references, not an exhaustive systematic review or a claim of first discovery.
Source IDs, original-byte/text hashes, locators and methodological use are separate
from the existing empirical source map; no new numerical observation is adopted.

Complete a CHEERS-VOI 33-item crosswalk, with the CHEERS2022 28-item correspondence
and exact applicable source locators. A conditional normalised-score illustration
is not a calibrated health-economic evaluation. Mark genuinely inapplicable monetary,
QALY, implementation/population extrapolation and study-design items with reasons;
missing author/institution/journal/approval facts remain open, not falsely inapplicable.

## Reproduction and review

Use the existing exact NumPy/SciPy finite engine and scalar oracle; no new library,
VOI backend or evidence contract. Test marginal preservation, zero support, invalid
weights, neutral parity, conditional report marginals, garbling and tie-regret bounds.
All heavyweight execution uses repo-local Python3.15.1, 4096MiB sampled group RSS,
2400seconds and serial runs. No automatic retries or budget increases.

Fresh-source replay must extract the committed Git tree into an empty local directory
without ignored originals, .nox or the existing checkout as its source. Reuse an
explicitly verified Python3.15.1 dependency environment; this is source isolation,
not an independent dependency installation or offline lock-install demonstration.
Verify imported source paths, regenerate primary2/4/8 outputs and the challenge
outputs, validate each new manifest and compare identity/string/numerical fields to
saved artifacts at declared absolute tolerance1e-10. Exclude only checkout metadata;
regenerated figure bytes get their own hashes, not a cross-platform pixel-equality claim.
No network is allowed during the numerical replay; no remote captures are necessary
for executing the assumed model. Raw originals remain separately catalogued local evidence.

Author facts, final journal and applicable formal ethics/cultural requirements remain
open. No requests, contacts, applications, registrations, deposits or submissions.


## Administrative/source-reading amendments before challenge execution

Visual review of the retrieved CHEERS-VOI Table2 (printed pp1464–1466) finds
34 displayed topic identifiers: 1–28 and S1–S6. The article prose reports33.
The crosswalk will retain every displayed identifier and this source discrepancy,
rather than silently drop a row to satisfy the initial33-item description. This
changes reporting bookkeeping, not any numerical challenge specification.

Source-isolated replay invokes no source-download command. Operating-system network
isolation is not implemented and is not claimed; qualified dependencies are reused.
Five captured originals are usable; one captured PMC browser challenge is rejected,
and four PDF/metadata/checklist retrieval routes failed across two capture batches.
Those failures do not count as original-text review or justify an access bypass.
