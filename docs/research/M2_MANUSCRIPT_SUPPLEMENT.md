# Supplement: source methods, constructions and robustness

Companion to [the current manuscript](M2_MANUSCRIPT.md), 28 October 2026. Sources,
parameters, value choices and model outputs are distinct. This is a bounded methods
map and conditional numerical analysis, not a systematic review or empirical policy fit.

## S1. Complete model and report constructions

The [primary construction description](M2_CONDITIONAL_PUBLICATION.md#construction-details-and-complete-configuration-links),
[parameter provenance table](../../evidence/m2/publication_20261028/parameter_provenance.csv),
[base configuration](../../configs/regulatory.json) and
[retail cases](../../configs/m2_retail.json) are preserved inputs. Other than the
explicit challenges, neither their consequences nor their units are changed.

Baseline axes include tobacco volume 350/850 cigarette-equivalents per 1,000 residents/day;
illicit fraction 0.08/0.32; other nicotine 500/1,800 mg per 1,000/day; diversion 0/0.8;
expanded-cessation response 0.05/0.18; crime coefficient 0/1.5; health coefficient 0.75/1.25;
mitigation 0.15/0.65; yield 0.675/1.125µg/cigarette; supply ratio 0.9/1.1; and unrecorded
lawful fraction 0.01/0.06. These are illustrative supports, not empirical intervals.
The original gross-displacement restriction axis is replaced by net cessation.
An additional policy-supply bias multiplier has support 0.85/1.15.

For n non-null cessation nodes, q_j=transport×BetaQuantile((j+0.5)/n;23.4,97.2).
The explicit zero receives the case's null mass and each non-null node receives
(1−null mass)/n. Duplicate supports are merged and zero-mass supports removed.
All other baseline axes have independent equal masses. The whole product is normalised.
The five original cases retain transport/null/replacement triples
(0,1,0.5),(0.5,0.5,0.5),(1,0.2,0.5),(1,0.2,0),(1,0.2,1).
No probabilities are attached to those competing structures.

With L=T−I, retail lawful and illicit streams are Lr=L(1−q)(1−d) and
Ir=I(1−q)+L(1−q)d. Support removes M=Ir×m, giving lawful Lr+rM and illicit Ir−M.
Expanded cessation gives lawful L(1−c) and illicit I(1−c). Health score is
h(T−total)/1,000 and criminal-harm change is k(illicit−I)/1,000.
Action resource scores are 0,0.025,0.120,0.040. Lawful-volume changes are descriptive;
no tax rate, consumer surplus or actual incremental budget is estimated.

Biomarker mappings retain flow 200 L/person/day, population 1,000, nicotine 0.9 mg/cigarette,
nicotine recovery 0.74 and anabasine survival 0.85. Report-bin probabilities are
integrated lognormal probabilities, not observed detection/classification performance.

| Report channel | Ordered cutpoints | Assumed log SD or performance |
| --- | --- | --- |
| Anabasine | 2,4 ng/L | log SD 0.35 |
| Improved anabasine | 0.5,2,4 ng/L | log SD 0.35 |
| Nicotine equivalent | 3,000,6,500 ng/L | log SD 0.35 |
| Lawful supply | 300,600 cigarette-equivalents/1,000/day | log SD 0.20 |
| Yield calibration | 0.8,1.0µg/cigarette | log SD 0.10 |
| Causal total-consumption ratio | 0.7,0.9 | log SD 0.12 |
| Causal lawful-consumption ratio, including policy-supply bias | 0.2,0.5,0.8 | log SD 0.20 |
| High/low criminal-harm coefficient | binary report | assumed accuracy 0.80 |

The panel/supply design combines anabasine, nicotine and lawful supply. Improved
quantification replaces the first channel; calibration adds the calibration channel.
The causal design combines total and lawful ratios. Criminal-harm research uses its
single binary channel. No information is one outcome with probability one. Baseline
combinations multiply likelihoods conditional on every shared state. Neither baseline
conditional independence nor alternative shared errors is empirically calibrated.
Each design is one coarsened report; no physical sample count or recruitment design
is inferred from the number of report bins.

The seven EVPPI partitions use the existing configured groups. Their overlapping
parameter sets are executable in `grouped_labels`; individual/group VOI need not sum.
Scientific-information targets are net cessation, diversion and crime coefficient.
No mixture of normative weights or information-gain objective is hidden in the policy utility.

## S2. Methods literature identification and appraisal

[Search log](../../evidence/m2/readiness_20261028/search_log.csv):20 English-term
queries in five four-query batches on 28 October 2026: four initial topic/scoping
queries; four targeted source queries; four checklist/author-repository tracing
queries; four source/metadata routing queries; and four journal/bibliographic queries.
No date restriction or engine language filter was imposed. Domain-like terms in
some queries were literal search text, not guaranteed domain restrictions. Search
ranking, engine indexing and combined-batch attribution limit coverage.

Two complete retained result batches support the 32-row
[candidate disposition ledger](../../evidence/m2/readiness_20261028/candidate_dispositions.csv).
These are unique literal URLs within those batches, not 32 independent papers,
all results of all 20 queries, or an exhaustive novelty search. Initial scoping and
routing/journal results are recorded as queries and selected-source notes; their
complete raw result sets are not claimed preserved. Three selected native reference
edges are recorded in [citation edges](../../evidence/m2/readiness_20261028/citation_edges.csv).
This is a bounded one-hop trace, not a complete backward/forward citation graph.

Primary methods articles, official reporting sources and author-institution versions
were eligible. Tertiary summaries, duplicate routes and unrelated applications did
not become methodological evidence. The
[source index](../../evidence/m2/readiness_20261028/source_index.csv),
[source appraisal table](../../evidence/m2/readiness_20261028/source_table.csv) and
[claim table](../../evidence/m2/readiness_20261028/claim_table.csv) retain source/document
IDs, exact locators, use and access limits. No method source is ingested as a target
observation, prior update or likelihood. The earlier empirical-map search is separate.

Eight original acquisition targets produced six captured objects: five usable native
originals and one rejected browser challenge. Two routes failed. Two subsequent
metadata/checklist fallbacks also failed. All six captured object hashes, WARC hashes
and exact response-payload equality were checked; the challenge is byte-verified
but remains ineligible as an article. Native WARC capture timestamps are absent and
remain null. Review date is not substituted for a native capture timestamp.
Originals and text derivatives remain locally catalogued in
[integration records](../../integration/m2_readiness_20261028/source-catalogue.json).

Haag/Chennu's publisher abstract is available through the retained index result;
its native PDF and repository page were unavailable. DOI/title/authors/date were
separately checked using public Crossref metadata, which does not itself contain
or verify the abstract. Only the high-level conceptual comparison relies on this
access-limited source. The article's published authorship and DOI are verified;
its full methods, funding and interests are not asserted reviewed.

Four public Crossref metadata responses were saved and hashed. They clarify that
the tobacco source was online 10 January 2023 and in print December 2024; the manuscript
uses the print year with the online date explicit. Metadata checks do not establish
claim support or scientific validity. The existing official validation/ethics sources
and inherited model original are reused with their earlier capture identities.

Appraisal distinguishes professional guidance from empirical studies. Briggs' source
financial statement reports no other financial relationships; the Rothery task-force
report describes voluntary participation and NIH-NHLBI support for one author.
Jackson's overview acknowledges MRC support. Kunst's report discloses research support
and editorial roles, with the funder reported uninvolved in study conduct. These
statements are source-specific; they do not establish this manuscript's author funding
or interests. Unknown full-text disclosures remain unknown. Funding is not an automatic
inclusion/exclusion rule or a substitute for methodological appraisal.

## S3. Executed challenge details

[Challenge configuration](../../configs/m2_robustness.json) and
[execution report](../../results/m2_readiness_20261028/report.json) define all 13
specifications. Each case retains the same four actions and the same 25 normative
profiles. Baseline case/score/EVPI/EVPPI/EVSI comparisons to the primary tables have
maximum absolute difference zero at their saved precision.

A binary high-probability challenge preserves within-stratum conditional weights
while changing its marginal to the declared value. For high illicit-share probability
a and high-diversion probability b, independence gives p11=ab. The positive Fréchet
endpoint is min(a,b), and the negative endpoint is max(0,a+b−1). Strength±0.8 moves
80% toward the corresponding endpoint; the other three cells follow from those
margins. This is not an estimated covariance or a Pearson correlation. Tests verify
unequal margins, boundary roundoff, unsupported cells and invalid inputs.

For conditional reports with CDF intervals [lower_j,upper_j], a common-uniform draw
gives joint-cell mass max(0,min_j upper_j−max_j lower_j). Mixing 80% of that table
with 20% independent joint probabilities preserves each report's conditional marginal.
The common ordering is a specific positive-association assumption and does not span
all error copulas. Single-report and no-information likelihoods remain unchanged.

For report degradation, L'(y|s)=0.5 L(y|s)+0.5 q(y), where q(y)=sum_s p(s)L(y|s).
The replacement indicator is unobserved and q is state-independent. This defines a
garbling, not a claim that exactly half of EIG/EVSI remains. The decision-value
inequality is checked for each objective under the same prior. Combined challenges
apply prior margins, association, null response, joint reports and degradation in
the declared order. No prior probability or universal worst-case label is attached.

Regret of a retained baseline action is max_a E_challenge U(a)−E_challenge U(retained).
Where the original objective has several optima, both smallest and largest resulting
regret are retained. The summary reports the largest upper endpoint over the selected
profiles. This is conditional regret in normalised units, not national expected harm.

## S4. Reproduction and claim-to-output checks

[Reproduction protocol](M2_REPRODUCIBILITY.md) records the independently cloned source,
actual Python 3.15.1 dependency reuse, commit/tree/import checks, all table/report
comparisons and tolerance 1e-10. The primary analysis is unchanged. Each replay verifies
its actual input/output hashes; figures receive new execution hashes rather than an
unverified cross-platform pixel-identity claim. Raw originals and remote access are
separate from running the explicitly assumed finite model.

| Manuscript claim | Executed source |
| --- | --- |
| Four value profiles favour four different policies | Primary decisions.csv, source_shape_partial_replacement |
| No action spans the primary continuous rectangle | Primary robustness.csv and analytic vertex test |
| Consequence means | Primary consequences.csv, same selected case |
| Challenge set changes and regret | New summary.csv plus decisions.csv and study_value.csv |
| Negative association: zero policy changes, eight design changes | New summary.csv, negative_market_diversion |
| Shared reports: unchanged policy, two design changes | New summary.csv, shared_report_errors |
| Replacement: zero policy changes,57 design changes | New summary.csv, half_information |
| Combined challenge:29 policy/80 design changes | New summary.csv, combined_stress |
| Target EIG versus decision value | Primary scientific_information.csv and study_value.csv |
| Finite 2/4/8 differences | Primary report.json grid_check and nested outputs |

Numerical verification does not supply empirical calibration or external scientific
endorsement. No request, contact, elicitation, registration, deposit or submission.
