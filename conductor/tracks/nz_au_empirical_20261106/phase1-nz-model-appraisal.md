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
