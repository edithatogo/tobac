# NZ endgame seed model appraisal — 7 November 2026

Original-source inspection of Ait Ouakrim et al., DOI
[10.1136/tc-2022-057655](https://doi.org/10.1136/tc-2022-057655),
[PMID 36627213](https://pubmed.ncbi.nlm.nih.gov/36627213/), PMC11672025.
Disposition: alternative model structure and historical counterfactual evidence.
No parameter, causal policy effect or current baseline is adopted.

## Source and rights

Original Europe PMC fullTextXML was retrieved outside tobac. SHA256:
b99ad040e7c84e0745d02082b5fdd21a8d288dd28b9c5ae994cf78fd337160f0.
The exact endpoint/time/type/bytes are in the external additional-original-receipt.json.
The original carries CC BY-NC 4.0. Preserve those terms and attribution; project-owned
code's Apache-2.0 licence does not relicense this article, supplementary material or
underlying data. Its data availability statement points to the article and supplemental
information; that is not proof that executable code, every original input and all
required reuse rights have been recovered.

## Structural applicability

Original Methods describes SHINE tobacco: a smoking/vaping Markov life-history model
coupled through population impact fractions to a proportional multistate life table.
It includes dual use and time-since-quitting tunnel states. Initiation is represented
at a single age, and quitting is represented by net cessation rather than explicit
relapse. These assumptions require comparison with the requested life-history scope;
do not claim that every transition needed by R07 is thereby implemented or validated.

Business-as-usual transitions were calibrated to NZHS-derived projections using UK
transition starting values and optimisation. Those predictions are not additional
NZ observations. Preserve the survey edition, extrapolation, optimiser, transition
constraints and shared-source covariance. Reusing both calibrated transitions and
NZHS prevalence as independent measurements would double-condition their common data.

Disease life tables apply incidence, prevalence, fatality, remission, disability and
relative-risk inputs, with disease lags and subgroup-specific aggregation. The paper's
HALY outcomes do not supply a directly interchangeable instrument-specific QALY tariff.
Do not sum disease tables or copy vaping-harm assumptions without checking the model's
population impact fractions, morbidity accounting and joint uncertainty.

Intervention parameters combine earlier modelling, stated intentions and expert
elicitation. They are not newly observed causal effects in current NZ settings.
Keep the historical denicotinisation, retail and cohort policies as counterfactual
scenarios until the operative legal baseline and implementation dates are verified.
Full parameter/formula enumeration, supplements, source code and independent numerical
reproduction remain open; this is a partial original-model appraisal.

## Source discrepancies requiring reconciliation

Q:SHINE2023:calibration-period: original Methods, Smoking and vaping life history model,
names NZHS 2013–2014 through 2019–2020 for calibration. Table 1's Smoking (daily) row
names years 2011–2019. Retain both assertions and resolve the actual input editions
and period conventions before admitting transitions or declaring a held-out split.

Q:SHINE2023:denicotinisation-effect: original Interventions narrative gives 84.8% for
the reduction in smoking prevalence due to cessation over five years, whereas Table 2's
corresponding cessation row states mean 84.4%. This comparison was checked in original
XML text; independent rendered-PDF and supplement/code reconciliation remain required.
Do not select a preferred number, silently average them or call the difference rounding.
Quarantine the affected effect parameter; this does not invalidate all model components.

## Retrieval sensitivity

The prior S3 query missed this prespecified seed: its original title/abstract uses
inequity and HALYs, which were absent from that query's terms. The explicit v3 strategy
adds these and related health/cost synonyms before fitting; v2 and its results remain
preserved. Recovering the seed is one sensitivity check, not proof of exhaustive recall.
No fitted empirical outcomes have been used to choose the amended query.

## P2.8 source-to-formula continuation — 7 November 2026

The actual linked supplement, tc-33-e2-s001.pdf, is recovered from the official
Europe PMC supplementaryFiles ZIP. ZIP SHA256
9d245cd688c497c875cc67773a3295832c9e40be51f83bcb63f99b4dca82c28b;
linked PDF SHA256 de9b73c15df4a697f462257894dcefe4c80b05d5458e4c6b420c9d17bfce97ea.
Originals, page renders, parameter cells and numerical diagnostics remain outside tobac
in tobac-evidence-intake-20261107-p2-contrast; source rights/admission remain separate.

Complete PDF pages 34 and 36 were visually checked. Appendix D/Table S22's six
elicited columns average to the displayed 65.8%, 84.8% and 96.6%. The unrounded
endpoint range divided by 3.92 reproduces the approximate SD of 7.84%; this is an
elicitation-range approximation, not a sampling SE from six behavioural observations.
Both the main-table beta shapes (17.78, 3.19) and supplement shapes (17.8, 3.2) imply
means rounding to 84.8%. Their exact beta SDs are about 7.662%, not the separate
range-based 7.84% summary. Do not require these approximate summaries to be jointly
exact, or treat expert judgements as observed cessation outcomes. The prior 84.4%
versus 84.8% main-table/narrative quarantine remains: this evidence supports an
internal interpretation but is not an authoritative correction or source-code replay.

**Q:SHINE2023:survivorship-complement**: PDF page 36 prints the survivorship equality
using `1 - (1 - 31.3%)^5 = 15.3%`. Independent Decimal arithmetic gives about 84.697%
for that expression; `(1 - 31.3%)^5` gives about 15.303%. The annual rate calculated
from the stated 84.8% target is about 31.393%, distinct from its printed 31.3% example.
Retain the printed expression and quarantine it for adoption. Do not silently repair
it or infer that the original executable model necessarily used the erroneous text.

The separate Table 2 retail beta (23.4, 97.2) is numerically coherent: mean about
19.403%, SD 3.586%, median 19.233%, central interval 12.879%–26.887%. The source
uses a one-off transition increase, split between quitting and switching, for a
roughly 300-outlet/95%-reduction scenario, then reverts to BAU transitions. This mixes
previous modelling with stated intentions; it is not measured current NZ efficacy.
The current finite-state retail_case instead uses an explicitly transported/null,
equal-intensity aggregate consumption multiplier for its prospective case. That is a
labelled adaptation, not a replication of all SHINE life-history transitions. Its code
blob is byte-identical to the P2.2 tested/replayed source. No shape, null/transport
weight, reference result or causal-status label was changed.

The source-to-formula distinction and independent numerical checks advance appraisal,
not empirical fitting or current-policy transportability. The remaining calibration
period discrepancy, full source/code/parameter mapping, archive admission, compatible
NZ observations, policy effects and prespecified held-out validation remain open.
