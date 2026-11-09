# Parameter evidence and a testable frontier programme

Date: 9 November 2026. Reviewed source base: `e0e5609c77138a32c2f77f14fa8caa687a79cb4b`.

## Objective and present deliverable

Turn the remaining parameter gaps into an explicit distinction between what can be estimated, what can only be transported or varied, and what cannot currently be learned from the available observations. The accompanying [candidate registry](../../../evidence/parameter_candidates_20261109/README.md) supplies 65 numeric candidates from 12 sources and retains 20 residual gaps. It does not change the live model, the first-comparison contract, its cutoff or its source-admission decisions.

The numerical candidates cover historical NZ demand, dated excise, discount conventions, foreign model comparators, trial cessation, relative disease/mortality effects, short-run nicotine-standard responses, utilities, ED use/cost and published expert judgements. All retain their different meanings. Actual original-byte/canonical registration, unreviewed full texts and source-alias mapping remain open. In particular, new utility or price inputs do not create a missing matched wastewater outcome.

## Where the external frontier already is

Three comparators prevent overstating novelty:

- The [ABS experimental nicotine method](https://www.abs.gov.au/articles/household-consumption-illicit-tobacco-and-nicotine-products), released 3 June 2026, already fuses wastewater and auxiliary survey/administrative information through a Kalman-filter allocation. It explicitly assumes relative stability of product composition, excretion and measurement relationships.
- The opened [PBO nicotine-price costing edition](https://www.pbo.gov.au/for-parliamentarians/how-we-analyse/costing-concepts/nicotine-prices), dated 28 April 2026, already separates products and legal/illegal channels and allows substitution. Its stated costing assumptions largely omit supplier and second-round illegal-market responses. This is an external model comparator, not empirical truth.
- The [SHINE-Tobacco Australian preprint](https://www.medrxiv.org/content/10.64898/2026.07.08.26357588v2.full) already describes annual smoking/vaping/dual-use transitions, legal/illicit supply and health/equity outcomes. Its preprint and review status must remain explicit. Detailed model-to-model benchmarking needs the methods/code review, not just the abstract.

Recent [Australian VLNC elicitation](https://www.medrxiv.org/content/10.64898/2026.07.21.26358615v1.full) provides public distributions of expert judgements, while explicitly warning that they are not empirical effects or consensus. [Cheng's robust-decision paper](https://doi.org/10.3982/TE6439), first published 29 July 2026, already investigates when data improve robust decisions and when conventional updates may not. Its independence assumptions cannot simply be transferred to serially dependent wastewater observations. These sources make a claim of novelty from 'Bayesian + dynamic + multi-product' inadequate.

## Recommended research target

**A policy-and-learning system that can show when its preferred action is justified despite incomplete identification, choose the evidence that could change that action, and remain reliable as product composition, measurement calibration and market behaviour change.**

This is a research hypothesis, not a claim that the present repository is uniquely capable or already beyond published work. The contribution must be demonstrated against defined simpler alternatives.

### F1. Decision sufficiency under partial identification

For each supported parameter/model set Θ and pair of feasible actions a,b, calculate bounds on Δ(a,b,θ)=U(a,θ)−U(b,θ). A strictly positive lower bound establishes dominance only within that declared set. An interval spanning zero means the available restrictions do not order those actions. Report which additional constraints or observations could change that conclusion.

The useful output is not merely another wider interval. It is an inspectable explanation: which combinations of biology, product attribution, stock changes, transport and values determine the choice; which unresolved parameters cannot change it; and where a conclusion relies on an assumption rather than observations. Preserve conflicts between source restrictions instead of silently averaging them away.

Implementation: reuse current partial-identification and exact finite decision routines. Add parameter/estimand/source links and an optimisation witness for each claimed bound. Use a maintained LP/nonlinear solver only where its semantics match; retain enumerated/analytic tiny examples as independent checks. Do not call a loose outer bound sharp without an attaining construction or solver certificate.

Acceptance: exact small-case bounds, deliberately non-identifying cases, invalid/contradictory constraints and once-only source conditioning; coverage and decision regret under known-truth simulations. Whether a certificate is useful in the actual NZ application remains an empirical test, not a consequence of correct optimisation.

### F2. Choose calibration, behavioural evidence and routine sampling jointly

Compare additional wastewater samples against biological calibration, product-mixture measurement, lawful-supply reconciliation and target policy-effect evidence. Evaluate combinations as well as individual studies: a calibration study may unlock the value of monitoring, while more precise monitoring may remain irrelevant when a policy response is unidentified.

Implementation: build a typed catalogue of research designs and their observation mechanisms using existing M3 portfolio/staged interfaces. Preserve delays, shared costs, correlation, achievable uptake and the same downstream action set. Distinguish observations that inform a parameter from data that inform the source-to-target transport assumption. Do not assign performance numbers to an imagined study merely to calculate EVSI.

Acceptance: exact portfolio oracles and ablations comparing naive independent-study rankings, current M3 portfolios and the revised design. In the properly specified, optional-information Bayesian case, gross EVSI should be nonnegative. Negative net benefit after costs is possible; losses from misspecification or strategic responses are different estimands and must not be relabelled negative classical EVSI.

### F3. Adaptive policy with changing observation mechanisms

A policy can change both actual use and the meaning of the observations: switching products changes biomarker attribution, enforcement changes supply availability, and stocks create delays between purchases and consumption. Fixed measurement coefficients can then produce confident but incorrect policy responses.

Implementation: retain separate physical-state, evidence-arrival and decision clocks. Extend the existing cohort/health timing contract with only the age, exposure-history and time-since-cessation states justified by the decision. Couple a product-aware observation model to sequential actions and beliefs/uncertainty sets. Compare fixed policy, fixed surveillance, myopic EVSI and joint adaptive policy/study selection over identical horizons. Stop, expand and reverse choices must use only information available at the decision time.

Acceptance: an open known-truth simulation benchmark varying calibration drift, serial dependence, stockpiling, product substitution, reporting bias, missingness and implementation delays. Prespecify meaningful regret/coverage/false-confidence criteria before comparing methods. Demonstrate performance under misspecification, not just fitting data generated by the same preferred model. Do not claim that a more complex filter improves real policy decisions until held-out field evidence supports that claim.

### F4. Heterogeneity, perspective and strategic adaptation

Heterogeneity asks whether different groups face different risks or benefit from different actions. Perspective asks how a declared decision-maker values outcomes. These are not interchangeable: evidence can resolve facts without resolving a value disagreement.

Implementation: retain disjoint group denominators and explicit health, household, fiscal and societal accounts. Use Voiage for reusable value-of-information/perspective/heterogeneity methods, not a new tobac implementation. Report Pareto sets and perspective-specific robust choices unless a common welfare function is justified. Add Paignia-based supplier/enforcement response only when an exogenous-response benchmark exposes a material decision vulnerability. Keep multiple equilibria and equilibrium-selection assumptions visible.

Acceptance: checks for overlapping groups, cost/transfer double counting, unidentified group effects, and disagreement that cannot be resolved by more factual measurement. Separate signed strategic information value from classical decision VOI. No group-level wastewater pattern may identify individual behaviour, ethnicity or criminality. Normative weights and governance cannot be filled by statistical convenience.

### F5. Living evidence with controlled model revision

Use the existing Searchright search editions and study identities to turn a new or corrected source into a new, inspectable model edition. The central question is not whether an LLM can extract a number, but whether the update preserves estimand, units, direction, uncertainty type, cohort dependence and the valid scope of the result.

Implementation: link source → estimate → parameter → mechanism → outcome → decision. Hash original editions through the existing archive, retain immutable outputs and explicit aliases, and invalidate only genuinely dependent derived results. Require extraction verification and a documented model handoff; Searchright retrieval is not empirical admission. Handle retractions, corrections, changed definitions and conflicts between online editions. The PBO discrepancy encountered in this sourcing pass is a useful fixture.

Acceptance: replay the same source bundle without conditioning twice; revise/retract a source and show exactly which estimates and actions change; detect confidence/credible/IQR substitution, reversed cross-elasticities, currency-year changes, incompatible denominators and inappropriate annualisation. Track abstentions and unresolved extractions, not just apparent precision. Automated extraction evaluation should compare deterministic/table-aware baselines with model-assisted extraction on public, independently checked fixtures.

## Executable sequence and boundaries

| Stage | Deliverable | Completion criterion |
|---|---|---|
| P0: source packet | This targeted registry, explicit gaps and source-edition warnings | Bundle representation checks; no claim of complete code coverage or original-byte admission |
| P1: parameter crosswalk | Inventory configuration fields, formula constants and dynamic arrays; map source aliases and estimands | Every in-scope parameter has a unit, status, owner module and dependency group; gaps remain explicit |
| P2: F1 small oracle | Bounded action rankings and witnesses under partial identification | Independent analytic/enumerated tests, null/contradictory data and duplication controls pass |
| P3: F2 study portfolio | Calibration-versus-sampling-versus-policy-evidence designs | Exact numerical comparison with existing M3 and prespecified cost/timing scenarios |
| P4: F3 simulation challenge | Time-varying measurement, physical state and adaptive decisions | Frozen benchmark, no future leakage, coverage/regret and complexity ablations |
| P5: real application | Existing-evidence versus wastewater comparison in issue #3 | Existing matched-data, causal, independent-validation and native requirements met; otherwise bounded no-identification result stays scoped |
| P6: F4/F5 extensions | Heterogeneity/strategy and one real source update | Independent method checks plus a traceable effect on an application decision |

Prioritise P1–P3 over accumulating broader model features. A paper-ready negative result may show that additional baseline monitoring cannot resolve a specified policy-response ambiguity. That does not prove surveillance has zero value in every decision, nor complete the stronger empirical milestone in #3.

Tobac owns tobacco-specific measurement, causal assumptions, states and interpretation. Searchright owns review lifecycle; Voiage generic decision-value methods; Innovate optional diffusion/competition; Kairos optional execution/time resources; Paignia optional strategic solving. No runtime dependency or provider qualification is asserted by this plan.

## What a credible advance would look like

A convincing result would show, for an explicitly defined class of decision problems, that the new method either reduces prespecified decision loss relative to the best comparable baseline or reliably detects a dangerous unsupported conclusion that the baseline misses. It must also disclose the settings where it adds no benefit. Source-rich documentation, passing CI, a complex architecture and a novelty claim are not substitutes for that result.

No new contact, study registration, restricted access or collection is authorised. The work remains public-source based. Repository implementation, native qualification, empirical support and external scientific review retain distinct claims.

## Candidate-catalogue identity audit — 9 November 2026

The [20-row crosswalk](../../../evidence/parameter_candidates_20261109/alias_crosswalk.csv)
reconciles duplicated source-level numbers between the 61-entry embedded catalogue
and the 65-entry registry. Every mapped value was checked at the candidate head;
two trial risk differences require percentage-point-to-fraction conversion.
Preserve the original source aliases and the scope narrowing for the NZ tobacco
excise classification; these are not 20 new observations or evidence admissions.
Pending: review unmatched entries, reconcile any remaining study identity aliases
through Searchright, and require the original existing handoff/native acceptance
before model fitting. No live parameters changed.
