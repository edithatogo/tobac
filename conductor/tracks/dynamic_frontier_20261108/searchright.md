# Incremental systematic review with Searchright

This makes the parent empirical programme's R01 executable in stages. It is a
technical integration/review-workflow plan; no completed systematic review,
comprehensive retrieval, final screening or pooled effect is claimed.

## Current integration checkpoint — 9 November 2026

The parent programme already executed Searchright compilation/imports and
source-native searches. Reuse [its protocol and retrieval history](../nz_au_empirical_20261106/systematic-search.md)
and [search receipts](../nz_au_empirical_20261106/phase1-search-receipts-20261107.json).
The real executable at Searchright `4ddfbdbc54c500719889e09942783bdc04ee832b`
has its own recorded build/import scope. The separate source inspection below
does not replace that executed evidence or qualify a new provider route.

Across five PubMed families, 28,913 occurrences correspond to 27,507 unique PMIDs.
Those are source records, not included studies. Query-translation review, the
recorded Europe PMC count discrepancy, grey/citation coverage, full screening,
study linkage and downstream admission remain open. The eight recorded S5
assessments retain their original scope. Do not restart this corpus as a new pilot
or mark a native live-provider route qualified merely because compilation and
source-native acquisition/import succeeded.

The current increment is a [bounded first-comparison task](../nz_au_empirical_20261106/first-comparison-task-card-20261109.md):
resolve source roles, dependence, measurement applicability and original-value
checks for the evidence already relevant to the initial comparison. Its completed
dispositions do not claim completion of the broader systematic review. Searchright
continues to own review/search lifecycle; tobac's existing handoff decides whether
the evidence is suitable for the requested observation and model role.

## Inspected integration surface

Repository: [edithatogo/searchright](https://github.com/edithatogo/searchright).
Source inspected on 8 November 2026 at exact revision
`f6aa483e6ff729dd337d0c0149c660afcddc41cd`:

- [README and evidence ceiling](https://github.com/edithatogo/searchright/blob/f6aa483e6ff729dd337d0c0149c660afcddc41cd/README.md)
- [Review plan example](https://github.com/edithatogo/searchright/blob/f6aa483e6ff729dd337d0c0149c660afcddc41cd/contracts/examples/review-plan.yaml)
- [Search strategy example](https://github.com/edithatogo/searchright/blob/f6aa483e6ff729dd337d0c0149c660afcddc41cd/contracts/examples/search-strategy.yaml)
- [Schema catalogue](https://github.com/edithatogo/searchright/blob/f6aa483e6ff729dd337d0c0149c660afcddc41cd/contracts/schema-catalog.json)

The inspected source declares protocol/query/source receipts, conservative
deduplication, record–report–study linkage, screening, PRISMA reporting and immutable
living updates. The README calls it a source-verified technical alpha and separates
source, compiler, fixture, live-provider and downstream evidence. Inspection here
does not execute or qualify its current CLI, providers or tobac handoff.

Keep ownership distinct: Searchright manages search/review lifecycle; Sourceright
verifies citations; CiteWeft can supply extraction evidence; tobac evaluates
measurement meaning, causal transport, parameterisation and decision relevance.
Use immutable exports and existing contracts, without copying the search engine
or making Searchright a mandatory runtime import for accepted tobac analyses.

## Review questions, in priority order

| Review stream | Model gap | Extraction focus |
| --- | --- | --- |
| Measurement calibration | Mapping biomarker quantities to total/product exposure | Analyte, matrix, excretion/recovery, route/product, assay/censoring, population, sampling time, flow, uncertainty and dependence |
| Policy and service effects | Initiation, cessation, relapse, intensity and switching transitions | Policy contrast, co-interventions, causal estimand, design, counterfactual, effect scale, follow-up, implementation and transport |
| Product and health pathways | Risk and recovery over time, competing outcomes | Smoking/vaping/dual-use history, cumulative exposure, time since cessation, age, absolute risks, uncertainty and applicable population |
| Economics and implementation | Actual costs, uptake, resource limits and supply response | Currency/price year, perspective, capacity, delay, programme uptake, tax pass-through, substitution and displacement |
| Methods/frontier comparison | Whether proposed methods add something useful | Measurement/identification, dynamic VOI, robust decisions, equity, strategic response and benchmark validation |

Start with one bounded calibration question and one policy-transition question.
Use baseline decision sensitivity to prioritise review effort, while retaining a
prespecified relevance rule so preferred model results do not select the literature.
Existing reviews can map the field; link their primary studies to avoid counting
the same evidence twice. Reviews of clinical cessation interventions and policy
natural experiments need different estimands and synthesis assumptions.

## SR1 — protocol and offline qualification

Specify population, intervention/exposure, comparator, outcomes, context and
eligible designs before searching. Record date/language restrictions and rationale;
do not require outcome terms or NZ-only terms unless seed-recall testing supports
them. Give the versioned protocol an identity and record subsequent amendments.

Use the pinned `org.searchright.review-plan.v1` and
`org.searchright.search-strategy.v1` schemas, plus database-specific query
translation. Qualify `validate-plan` and `compile` against small golden fixtures
in the pinned executable. Test exact query preservation, translation-loss warnings,
schema errors and replay. Schema validation alone is not a passed live search.

**Acceptance:** exact source/package/compiler identity; successful positive and
negative fixtures; reviewed eligibility and seed studies; recorded search-quality
checks. A human remains responsible for the review protocol and final inclusion
decisions. Independent search/selection checks are methodological goals, not a
new blanket repository publication-approval requirement. Record any single-reviewer
deviation transparently rather than simulating a second reviewer with an agent.

## SR2 — actual search, screening and study linkage

Use PubMed/MEDLINE and suitable complementary open sources; add economic and policy
databases, trial registers, citation searching and NZ/AU official sources to match
each question. Licensed sources require genuine user-held access. Record unavailable
sources as coverage gaps rather than silently substituting an internet search.

Retain exact queries, platform, execution date, provider response/receipt, result
count, original record IDs, rights and retrieval failures. Deduplicate records
conservatively, then link reports to studies/cohorts; preprints, final papers,
supplements and reused national datasets are not independent studies. Preserve
title/abstract and full-text decisions, reasons and unresolved disagreements.
Ranking assistance can prioritise work; it cannot silently exclude low-ranked
records. Retain source coverage and amendment history on updates.

**Acceptance:** reproducible source logs, reconciled screening counts and study
links, final human-reviewed decisions, and an explicit unresolved-retrieval list.
Report using [PRISMA 2020](https://www.prisma-statement.org/prisma-2020) and
[PRISMA-S](https://www.prisma-statement.org/prisma-search) as applicable; a flow
diagram documents the process and does not certify completeness or low bias.

## SR3 — extraction, bias, certainty and synthesis

Use source spans/table cells and exact study/report IDs. Extract estimates with
standard errors/intervals, sample size, follow-up, units, effect scale, adjustment
set, missingness, population and intervention implementation. Separate observed
estimates, model-derived outputs and analyst assumptions. Record shared cohorts
and inputs before any pooling; preserve multiple outcomes and timepoints jointly.

Assess bias for the actual result being used. Use an appropriate RoB 2 approach
for randomised intervention results and ROBINS-I for non-randomised intervention
effects, with the version and domain judgements recorded. Measurement/calibration
studies need a fit-for-purpose assay/sampling appraisal rather than an inapplicable
intervention checklist. See [Cochrane guidance](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-25).
Assess certainty and transport to NZ separately from citation correctness.

Pool only compatible estimands. Retain heterogeneity, confounding sensitivity,
selective reporting, transport attenuation and alternative model structures.
Do not turn a risk-of-bias score mechanically into a precision weight. A percentage
cessation effect from a published simulation is not an observed policy trial.
Translate pooled effects to interval-specific transition parameters only through
an explicit, tested baseline-risk and competing-transition model.

**Acceptance:** each candidate parameter links to study results, bias/transport
judgements, synthesis code, uncertainty and a declared model role. Leave unsuitable
evidence as context and unidentified parameters as explicit assumptions or bounds.

## SR4 — one qualified export-to-model handoff

Freeze a Searchright review bundle and verified audit head. Validate its declared
schemas and map report/study/source identities into tobac's existing evidence
contract. Preserve hash, version, population, period, products, units and dependence.
Source identifiers must survive deduplication and report linkage. Test duplicate
study rejection, revised reports, mismatched units/time/population and unavailable
uncertainty. Replaying the same bundle must never condition the posterior twice.

**Acceptance:** golden fixture and installed-provider execution, round-trip readback,
negative controls, source-bound receipts and fresh tobac scientific qualification.
Retain a comparison with the pre-review assumptions; never replace them silently.

## SR5 — living evidence and decision updates

Begin with an explicit, on-demand update. Preserve the previous review and model,
search incrementally with overlapping date windows where required, deduplicate
against prior records and record revised/retracted reports. Produce an update
report distinguishing new records, newly eligible studies, revised estimates,
changed certainty and changed model decisions. Refit only after admission gates.

Separate three clocks: **publication/evidence updates**, **population/policy
evolution**, and **decision opportunities**. New publications may change beliefs
without changing the physical state; time may pass without new evidence. Compare
decision changes under the same policy horizon and previously frozen evaluation
set. Use materiality thresholds and expected decision value to prioritise future
review/search effort. Automated scheduling is a later, separately configured step;
this roadmap does not install a background task or claim a living review is running.
