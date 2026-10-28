# Value-sensitive research priorities for tobacco regulation: a conditional decision analysis

## Abstract

**Background.** Evidence about a policy and judgments about its consequences both
influence decisions. Improving measurement need not resolve disagreement about which
consequences matter or identify the most useful future research.

**Methods.** Four tobacco-regulation action archetypes were compared in a synthetic
1,000-resident catchment. Five existing structural/prior cases were crossed with 25
crime/resource value profiles, with health weight fixed at one. Exact finite expected
value of perfect information (EVPI), grouped partial perfect information (EVPPI),
sample information (EVSI) and target-specific information gain were calculated.
Thirteen post-primary assumption specifications challenged prior margins, null-response
mass, parameter dependence and conditional report dependence/performance. No probabilities
were assigned to normative profiles or competing structures. No empirical target
likelihood was fitted.

**Results.** Each action was preferred under a different value profile with identical
factual assumptions. No action was co-optimal throughout the primary continuous weight
rectangle in any structural case. Across the 125 matched profiles, lowering the prior
probability of high diversion changed 26 policy sets; negative illicit-share/diversion
association changed no policy sets but changed eight gross-information design sets.
State-independent report replacement changed 57 gross-information design sets without
changing current policy choices. A combined stress specification changed 29 policy
sets and 80 gross-information design sets. These are finite-grid counts, not probabilities.
The challenge baseline exactly reproduced primary decision and information tables.

**Conclusions.** Conditional research priorities depend on value judgments and on
assumptions about latent states and reports. The analysis provides an auditable
illustration of that dependence, rather than a new VOI theorem, an observed NZ policy
effect, representative preferences or a recommendation to commission a study.

## 1. Introduction

### 1.1 Evidence, values and the research decision

Deciding whether to restrict tobacco retail access involves predictions about smoking,
substitution, resource use and criminal harms, together with judgments about how to
compare those consequences. A laboratory or administrative measurement may improve
knowledge of a quantity without changing the preferred action. Conversely, the same
measurement may be valuable under one objective and irrelevant under another.

VOI provides an established decision-theoretic framework for evaluating information
through its expected effect on choices. It can also be applied to estimation problems,
where the relevant loss differs from a policy objective. These uses should be stated
separately, rather than treating information gain as a universal research priority
([Jackson et al., 2022](https://doi.org/10.1146/annurev-statistics-040120-010730)).
The decision criterion, uncertainty specification and hypothetical study model are
part of the analysis, not facts established by running its calculations
([Rothery et al., 2020](https://doi.org/10.1016/j.jval.2020.01.004)).

Preference and prediction uncertainty have already been considered jointly in VOI.
Haag and Chennu's framework examines their relative importance in a multi-criteria
case study ([2023](https://doi.org/10.1016/j.omega.2023.102936); indexed publisher
abstract and bibliographic metadata reviewed; full native text unavailable here).
The present analysis therefore makes no claim to introduce preference-sensitive VOI.
It does not assign a probability distribution to social preferences or estimate the
value of eliciting them. Instead, it holds each stated objective fixed while examining
what empirical information would be valuable, and reports the differences between objectives.

### 1.2 Applied context and contribution

The motivating context is a hypothetical NZ tobacco-retailer reduction and its associated
research questions. The earlier source map found important mismatches between national
supply releases, resident consumption, laboratory calibration and causal policy response.
The historical approximately 600-retailer scheme did not supply an implemented,
identified national natural experiment; the [public-source completion report](M2_PUBLIC_SOURCE_COMPLETION.md)
retains the underlying official-source and extraction evidence.

The contribution is an applied audit linking those evidence limitations to a transparent
conditional analysis. It combines separate consequence reporting, all optimal ties,
analytical value-weight boundaries, a distinction between information gain and action
value, and explicitly declared dependence/report challenges. Small finite models make
the calculations directly inspectable. This complements established VOI methods; it
does not replace empirical validation or establish that the hypothetical policies are
implementable. Systematic examination of assumptions is consistent with modelling
uncertainty guidance ([Briggs et al., 2012](https://doi.org/10.1016/j.jval.2012.04.014)).

## 2. Methods

### 2.1 Design and analysis sequence

This is a synthetic, conditional decision analysis using published context and
inherited model inputs. Earlier M 1/M 2/M 3 analyses predate the
[primary protocol](M2_PUBLICATION_PROTOCOL.md). The
[readiness protocol](M2_READINESS_PROTOCOL.md) fixes the new challenge design before
its execution and identifies its post-primary status. Neither protocol is preregistered.
The source-isolation implementation amendment is in
[reproduction methods](M2_REPRODUCIBILITY.md).

The analysis sequence is current policy choice and EVPI, grouped EVPPI, target-specific
learning, then study EVSI. Gross study value is reported before any actual research
cost. An uninformative report represents no study. No study was commissioned, no sample
size was optimised and no net research benefit was estimated from actual prices.

### 2.2 Population, setting, horizon and units

The numerical population is a **synthetic 1,000-resident catchment**, without an age,
ethnicity or individual-person simulation. Consumption quantities are daily cigarette-
equivalent rates per 1,000 residents. The model describes a first-year comparative
response using those daily rates; it does not integrate them into an annual death,
QALY or monetary outcome. No temporal discounting or population research-lifetime
multiplier is applied to this single-period score comparison.

NZ residents aged 15+ using cigarettes/roll-your-own and an approximately 600-retailer
contrast are a **separate applied target**, to which transport remains unqualified.
The numerical denominator is not relabelled as age 15+, nor converted using an assumed
smoker count. Product-specific RYO mass/intensity, lawful unrecorded channels, stock
and visitor adjustments remain empirical limitations. No present agency decision,
legal authority or implementation acceptance is assumed.

### 2.3 Actions, consequences and objectives

The four action archetypes are reference, retail restriction, restriction with support,
and expanded cessation. They distinguish a retail-access response from additional
support and broader cessation; they are not an exhaustive feasible-policy set.
The existing [retail consequence contract](../m2_retail_contract.md) is retained.
For baseline total T, illicit I and lawful L=T−I, additional retail cessation q leaves
T(1−q). Diversion moves D=L(1−q)d from lawful to illicit supply. Support removes a
fraction m of the resulting illicit stream and replaces a case-specific fraction
lawfully. Expanded cessation reduces both baseline streams by the assumed fraction c.
The supplement gives the complete construction and input bindings.

Health score H is the assumed health coefficient times the reduction in total daily
exposure, divided by 1,000. Criminal-harm change C is the assumed marginal harm
coefficient times the change in illicit volume, divided by 1,000; it can be negative.
R is an illustrative fixed real-resource score. This is a restricted consequence
perspective, not a fully measured societal or regulator-budget economic evaluation.
Lawful-volume changes are reported separately and are not tax revenue or social costs.

The objective is U=H−wC C−wR R. Expected utility is maximised for each
declared objective; no risk-averse criterion is evaluated. Health weight is one; crime and resource weights each
take 0,0.5,1,2,4. These are analyst stress supports, not representative social/Māori
preferences, willingness-to-pay estimates or probabilities. Zero resource weight
removes the score from this objective without removing real-world resource needs.
The additive objective excludes rights constraints, nonlinear preferences, hard
budgets and distributional priorities. No single normative profile is selected.

### 2.4 Sources, parameter construction and priors

The earlier bounded empirical map contains 35 document records, 82 extracts and 213
candidate dispositions. These are not independent-study counts or an exhaustive
systematic review. None of its extracts is newly adopted as a target observation or
likelihood. Shared MOH/NZHS and biological inputs are not conditioned on again.
The current methods search, critical claim/source links and bibliographic metadata
are separately catalogued in the [literature supplement](M2_MANUSCRIPT_SUPPLEMENT.md).
Methods articles supply conceptual/reporting guidance, not new empirical parameters.

The inherited Beta(23.4,97.2) additional-cessation shape is a published model input
based on earlier modelling and stated quitting intentions
([Ait Ouakrim et al., online 2023/print 2024](https://doi.org/10.1136/tc-2022-057655), Table 2).
Its original outlet reduction and horizon differ from the present illustration.
Equal-intensity transport to consumption and the one-year response are assumptions.
Four midpoint-quantile nodes represent the non-null shape, with explicit null mass
and case-specific attenuation. No target posterior is estimated from the source.

The five original cases comprise zero additional retail cessation, attenuated
transport and source-shape cases with partial, no or full lawful replacement.
The identifier null_effect means zero **additional retail cessation**, not zero
consequences from diversion, support or expanded cessation. Other baseline axes
are independently equally weighted finite supports. The
[parameter provenance table](../../evidence/m2/publication_20261028/parameter_provenance.csv)
and configurations retain units, assumptions and formula links. Uncertainty ranges
and null probabilities are analyst assumptions, not fitted confidence intervals.

### 2.5 Information calculations and numerical checks

For a fixed prior p and objective, EVPI is E[max_a U(a,s)]−max_a E[U(a,s)]. EVPPI
conditions on a declared finite partition before maximising; seven overlapping
partitions cover market, behaviour, criminal harm, health consequences, implementation,
measurement and reachable baseline quantities. Their information values are not additive.
EVSI averages the optimal posterior expected value over a hypothetical report and
subtracts the current optimal expected value. All computations use the same finite
prior and retain every co-optimal action at absolute tolerance 1e-11.

The six designs are no information; biomarker panel plus supply; improved quantification
plus supply; calibration plus panel and supply; matched causal total/lawful comparison;
and criminal-harm research. They are coarsened hypothetical report channels, not
sample-size designs. Their bins, likelihoods and assumed conditional independence
are reported in the supplement. The causal design presupposes a valid counterfactual
and accounting bridge that baseline wastewater alone does not provide. Information
is assumed available and acted on for the modelled decision, without acquisition delay,
implementation failure or future-population extrapolation.

Expected information gain (EIG) about net cessation, diversion and the crime coefficient
is the report-averaged reduction in target entropy, in nats. It is independent of
utility weights for a fixed prior, target and report channel; changes to those assumptions
can change it. EIG and policy EVSI are not interchangeable.

The existing exact NumPy/SciPy engine and scalar reference oracle are retained.
Checks cover posterior martingales, nonnegative information values bounded by EVPI,
weighted-reference parity, ties, dominated intersections and marginal preservation.
The primary 2/4/8-node diagnostic examines finite-resolution stability, not continuous
convergence. For health weight one, expected-value differences are affine in crime
and resource weights; optimality at every rectangle vertex certifies optimality
throughout that rectangle under the fixed prior/structure.

### 2.6 Post-primary assumption challenges

Thirteen specifications, including unchanged baseline, cross all five cases and
25 objectives: 1,625 policy profiles, 11,375 grouped-information rows, 9,750 study-value
rows and 1,170 target-information rows. High illicit-share, diversion or crime support
probabilities are changed to the declared 0.2/0.8 margins. Other challenges set null
mass to 0 or 0.8. Zero transport still yields zero retail cessation in every such challenge.

Illicit-share/diversion dependence moves their binary high/high joint probability
80% from independence toward either Fréchet bound, preserving both marginal
probabilities. This fraction is not Pearson correlation. Conditional report dependence
mixes the independent joint likelihood with 80% common-uniform ordered-bin coupling,
preserving every constituent report's state-conditional marginal likelihood.
It is one positive shared-error alternative, not an empirical error estimate or a
bound over all possible dependence structures.

A report-degradation challenge replaces the report by an unobserved independent
prior-predictive draw with probability 0.5. The identifier half_information names
this replacement parameter; it does not imply that EVSI or EIG is halved.
For the same prior and objective this garbling cannot increase EVSI, which is checked.
The combined specification applies the stated high margins, high null mass, positive
association, shared reports and degradation. It is not a universal worst case.

Policy and gross-information co-optimal sets are compared on identical case/value
keys. Regret is evaluated under each challenged prior/objective for every originally
co-optimal action, retaining its minimum and maximum. Counts describe sampled profiles;
no averaging over social preferences or probability of a policy being correct is inferred.

### 2.7 Transparency, reporting and reproduction

The primary snapshot remains immutable. New results are in
[the robustness tables](../../results/m2_readiness_20261028/README.md).
Every execution binds source/configuration/output hashes. A clean-source replay uses
an independent local committed checkout, verifies import/commit/tree identity and
regenerates primary 2/4/8 and challenge outputs. It compares every table and scientific
report field at absolute tolerance 1e-10, excluding only checkout metadata. It reuses
qualified Python 3.15.1 dependencies and does not claim a fresh offline installation
or operating-system network isolation. Full execution receipts are reported separately.

The [reporting crosswalk](M2_REPORTING_CROSSWALK.md) covers all displayed CHEERS-VOI
topics and base CHEERS 2022 correspondence, with explicit partial applicability and
open author declarations. Reporting guidance is not methodological certification
([Kunst et al., 2023](https://doi.org/10.1016/j.jval.2023.06.014)). Numerical verification
is distinct from external validation
([Eddy et al., 2012](https://doi.org/10.1016/j.jval.2012.04.012)).

## 3. Results

### 3.1 Values change choices under identical factual assumptions

In the source-shape/partial-replacement case, health weight one with crime/resource
weights 0/0 favours restriction with support; 0/1 favours retail restriction; 1/1 favours
expanded cessation; and 0/4 favours reference. Those profiles vary only values, not
state probabilities. No action is co-optimal across the full continuous 0–4 rectangle
in any original case. The source-case retail/expanded-cessation switch at resource
weight one is approximately 0.3294 in crime weight, conditional on the primary finite model.

| Action | Daily total cigarette-equivalents/1,000 residents | Health score | Criminal-harm change | Resource score |
| --- | ---: | ---: | ---: | ---: |
| Reference | 600.0 | 0 | 0 | 0 |
| Retail restriction | 507.1 | 0.09290 | 0.10777 | 0.025 |
| Restriction with support | 454.4 | 0.14564 | 0.02866 | 0.120 |
| Expanded cessation | 531.0 | 0.06900 | −0.01035 | 0.040 |

Table 1. Expected synthetic consequences in the same source-shape/partial-replacement
case. Scores are constructed model quantities, not observed health effects, crime
incidence or NZD costs. Full case/action outputs retain calculated precision.

![Conditional policy grid](../../results/m2_publication_20261028/decision_grid.png)

Figure 1. Points are declared value profiles, not population-preference frequencies.
The zero-cessation panel retains other policy pathways. The figure is preserved from
the primary analysis; it is not a plot of the later empirical-assumption challenges.

### 3.2 Assumptions can change policy and information priorities differently

| Specification | Policy sets changed | Gross-design sets changed | Group sets changed | Maximum baseline-action regret |
| --- | ---: | ---: | ---: | ---: |
| baseline | 0 | 0 | 0 | 0.0000 |
| low market | 3 | 5 | 13 | 0.0350 |
| high market | 14 | 7 | 23 | 0.0574 |
| low diversion | 26 | 2 | 19 | 0.1096 |
| high diversion | 4 | 15 | 25 | 0.0373 |
| high crime | 8 | 6 | 13 | 0.0355 |
| positive market diversion | 3 | 7 | 14 | 0.0123 |
| negative market diversion | 0 | 8 | 14 | 0.0000 |
| no null mass | 18 | 17 | 11 | 0.0303 |
| high null mass | 18 | 27 | 9 | 0.0764 |
| half information | 0 | 57 | 0 | 0.0000 |
| shared report errors | 0 | 2 | 0 | 0.0000 |
| combined stress | 29 | 80 | 32 | 0.1670 |

Table 2. Changes from baseline among 125 matched profiles per specification. A policy-set
change means disjoint optima in these executed results; ties remain retained in the
underlying tables. Study columns compare gross-EVSI design sets before research cost.
Counts cannot be read as societal preference proportions. The combined row is a
specified joint challenge, not a global robustness bound.

Negative illicit-share/diversion association leaves current policy sets unchanged
on this grid, yet changes eight gross-information design sets and 14 grouped-information
sets. Changing only report likelihoods also leaves current policy choices unchanged,
as expected: reports have not been observed and the prior remains fixed. Nevertheless,
report degradation changes 57 gross-design sets and shared conditional report errors
change two. Preserving marginal report performance therefore does not guarantee
unchanged research rankings when their joint dependence changes.

The combined specification changes 29 policy sets and 80 gross-design sets. Its largest
regret from retaining a baseline-optimal action is approximately 0.1670 normalised
units; this is a constructed current-objective loss, not a measured welfare loss.
The baseline challenge reproduces all 125 primary decision rows, 875 grouped-information
rows and 750 study rows with maximum absolute numerical difference zero.

### 3.3 Learning, decision value and numerical resolution

In the primary source-shape/partial-replacement case, the matched causal report has
largest gross EVSI at crime/resource weights 1/1 (approximately 0.02212 units), while
the calibration-plus-panel/supply design leads at 0/4 (approximately 0.01374).
The criminal-harm report provides approximately 0.1927 nats about its target, yet its
EVSI is zero when crime weight is zero under the fixed independent prior. This
illustrates distinct inferential and action objectives, not a universal property
of criminal-harm research.

Primary refinement from 4 to 8 cessation nodes changes no policy, gross-design or
group-information co-optimal sets at the declared 125 profiles. Maximum absolute
EVPI,EVPPI and EVSI differences are approximately 0.0003123,0.0003900 and 0.0002949
units. A 2→4-node near-zero gross-design tie change is retained. These checks do not
prove continuous convergence, identical continuous switching frontiers or empirical accuracy.

## 4. Discussion

### 4.1 Interpretation and relationship to existing methods

This illustration applies established VOI principles to an evidence-constrained tobacco
question. Its substantive result is the explicit dependence of policy and information
rankings on declared values, joint priors and hypothetical report structure. Neither
high EIG nor a high gross EVSI under one profile is a value-neutral research mandate.
The paper does not measure the value of resolving disagreements about values themselves.
That differs from frameworks which assign distributions to uncertain preferences.

The challenge results also distinguish robustness of a current action from robustness
of a research priority. In the negative-association example, the former remains
unchanged on the selected grid while the latter changes. In the shared-report example,
individual conditional likelihoods remain unchanged while joint study rankings can change.
The paired comparisons support those conditional statements; they do not establish
which dependence or value specification is correct in NZ.

### 4.2 Factual disagreement, values and evidence use

A motivating proposal is that wastewater measurement could help narrow factual
aspects of disagreement over tobacco regulation. The calculations establish a
conditional decision-value framework for such measurement, rather than an effect
on ideological disagreement. The prior alternatives are sensitivity specifications,
not measured beliefs of political groups; value profiles are not stakeholder surveys.
No convergence, persuasion, trust or policy-adoption process is estimated.

For a fixed objective and stated prior, EVSI compares the expected utility of an
optimal report-dependent action with the best action chosen without that report.
It assumes the decision-maker can and does use information optimally. A change of
action is not necessary for every report, and greater agreement is not itself in
the utility function. Evidence may have value without producing agreement; actors
may agree on an action for different reasons. Identical beliefs can still produce
different choices when objectives differ, as the primary value comparisons show.

Interpreting EVSI as the benefit of reducing a political divide would therefore
require an additional, explicit link from reports to belief revision, decisions
and consequences, with a declared evaluation objective. Study costs, delay,
evidence uptake and implementation would also matter. No such empirical link or
common welfare objective is established here. The companion Viewpoint explains
this research proposition without converting model scores into measured social
benefits or repeating the numerical analysis as independent evidence.

### 4.3 Implications for evidence assessment

Public evidence can establish source identity, clarify units, expose estimand mismatches
and support alternative assumptions without supplying a fitted target likelihood.
The evidence map and model therefore serve complementary roles. An inaccessible
original remains an access limit; it does not become a zero effect or a verified
numeric extract. Forecasts and posteriors do not create new independent observations.

A report design that presupposes matched causal identification cannot obtain that
property merely from better baseline chemical precision. Conversely, measurement
research can have conditional value without identifying every causal quantity.
Actual study performance, feasibility, implementation and cost would be required
before treating these rankings as a funding decision. No collection or contact follows
from a positive conditional information value in this study.

### 4.4 Structural and external-validity limits

Finite enumeration removes Monte Carlo error for the stated supports, not uncertainty
about model structure or source transport. The selected supports, independence baseline,
Beta transport, fixed resource scores, additive objective and hypothetical report bins
are substantive assumptions. The challenges cover selected alternatives, not the
full space of plausible mechanisms, priors, error dependence or ethical positions.
The comparison does not identify a globally robust action outside the declared domain.

The reviewed public record does not jointly identify matched resident consumption and
lawful supply, stock/visitor effects, raw-matrix assay recovery, calibration covariance,
policy-induced diversion/mitigation, incremental criminal harms or current resource costs.
These remain limits on an empirical policy-effect or commissioning claim. The conditional
article does not require those effects to be relabelled as measured results in order
to report the present calculations. Future suitable public releases could change the
empirical assessment; none is presumed or requested.

### 4.5 Equity, ethics and public involvement

No subgroup effects or Māori-specific preferences are reconstructed from national
aggregates, and no public, patient or Māori consultation or elicitation occurred.
Averaged consequences do not establish distributional equity, cultural rigour or
community endorsement. The objective omits relevant equity/rights considerations;
sensitivity weights cannot stand in for governance or stakeholder representation.
The [desk assessment](M2_PUBLICATION_ETHICS.md) records the applicable public guidance
and the unresolved institutional/site/journal context. It is not a formal exemption
or approval. Any required review must be addressed prospectively; no retrospective
approval is assumed. No identifiable-health-record access, recruitment or external
person linkage occurred through this analysis.

## 5. Availability and research transparency

Code, explicit assumptions, source/claim indices and calculated tables are versioned
in the repository. Raw captured originals remain locally catalogued; their presence
in a fresh checkout is not implied by recorded hashes. The reproduction supplement
separates source isolation, dependency qualification, numerical agreement and empirical
validity. The analysis was developed with AI assistance for coding, searching,
extraction support and drafting; final author responsibility and journal-specific
disclosure wording remain to be confirmed, rather than claiming independent authorship.

The separate [author and declaration preparation record](M2_TWO_ARTICLE_DECLARATIONS.md)
retains unconfirmed author and formal requirements. The manuscript is being prepared
for MDM Policy & Practice and has not been submitted. Its related NZMJ Viewpoint
develops the measurement-and-disagreement proposal; it does not constitute a second
report of these numerical results. The related-work relationship must be disclosed
in any future authorised submission, with references appropriate to publication status.

## References

1. Briggs AH; Weinstein MC; Fenwick EAL; et al. (2012). [Model Parameter Estimation and Uncertainty: A Report of the ISPOR-SMDM Modeling Good Research Practices Task Force-6](https://www.ispor.org/docs/default-source/resources/outcomes-research-guidelines-index/model_parameter_estimation_and_uncertainty-6.pdf?sfvrsn=8bc10c8e_0). Source ID: `METHOD_UNCERTAINTY`.

2. Rothery C; Strong M; Koffijberg H; et al. (2020). [Value of Information Analytical Methods: Report 2 of the ISPOR Value of Information Analysis Emerging Good Practices Task Force](https://pmc.ncbi.nlm.nih.gov/articles/PMC7373630/). Source ID: `VOI_METHODS`.

3. Jackson Christopher H.; Baio Gianluca; Heath Anna; et al. (2022). [Value of Information Analysis in Models to Inform Health Policy](https://pmc.ncbi.nlm.nih.gov/articles/PMC7612603/). Source ID: `VOI_OVERVIEW`.

4. Haag Fridolin; Chennu Arjun (2023). [Assessing whether decisions are more sensitive to preference or prediction uncertainty with a value of information approach](https://doi.org/10.1016/j.omega.2023.102936). Source ID: `VALUE_PREFERENCES`.

5. Kunst Natalia; Siu Annisa; Drummond Michael; et al. (2023). [Consolidated Health Economic Evaluation Reporting Standards - Value of Information (CHEERS-VOI): Explanation and Elaboration](https://ris.utwente.nl/ws/portalfiles/portal/321016205/1-s2.0-S1098301523030310-main.pdf). Source ID: `REPORTING_VOI`.

6. Eddy DM; Hollingworth W; Caro JJ; et al. (2012). [Model Transparency and Validation: A Report of the ISPOR-SMDM Modeling Good Research Practices Task Force-7](https://www.ispor.org/docs/default-source/resources/outcomes-research-guidelines-index/model_transparency_and_validation-7.pdf?sfvrsn=24168dfb_0). Source ID: `ISPOR_VALIDATION`.

7. Ait Ouakrim Driss; Wilson Tim; Waa Andrew; et al. (2024). [Tobacco endgame intervention impacts on health gains and Māori:non-Māori health inequity: a simulation study of the Aotearoa/New Zealand Tobacco Action Plan](https://pmc.ncbi.nlm.nih.gov/articles/PMC11672025/). Source ID: `SHINE_RETAIL_TABLE2`.

8. Husereau D; Drummond M; Augustovski F; et al. (2022). [Consolidated Health Economic Evaluation Reporting Standards 2022 (CHEERS 2022) statement: updated reporting guidance for health economic evaluations](https://www.ispor.org/heor-resources/good-practices/cheers). Source ID: `CHEERS2022`.

9. Health and Disability Ethics Committees (undated; reviewed 28 October 2026). [General frequently asked questions](https://ethics.health.govt.nz/frequently-asked-questions/). Source ID: `HDEC_FAQ`.

10. National Ethics Advisory Committee (undated; reviewed 28 October 2026). [Research and Māori](https://neac.health.govt.nz/national-ethical-standards/part-two/3-research-and-maori/). Source ID: `NEAC_MAORI`.

11. EQUATOR Network (undated; reviewed 28 October 2026). [CHEERS Value of Information reporting standards](https://equator-network.org/reporting-guidelines/cheers-voi/). Source ID: `REPORTING_EQUATOR`.
