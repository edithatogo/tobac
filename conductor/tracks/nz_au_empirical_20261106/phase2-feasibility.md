# First empirical NZ/AU analysis — feasibility result, 6 November 2026

Outcome: historical input coverage and the Australian programme comparator can be audited;
the available admitted evidence does not support a new current NZ illicit-consumption fit,
transported policy effect or empirical monetary wastewater VOI. Phase 2 remains incomplete.
This is an explicit scope/identification finding, not a fitted empirical result.

## Executed coverage analysis

The tracked scripts/audit_empirical_coverage.py reopens existing CSV bytes through source_handoff
path/hash guards, checks their consumer inventory schema/count and complete unique annual
periods, then inventories them using Polars. It neither changes inputs nor fits a model.
It passed on actual Python 3.15.2 / Polars 2.1.0; bounded process-group RSS peaked at
89.2 MiB on the final audit, exit 0. Local output: outputs/nz-au-phase2/coverage.json and coverage-final.log.
The output binds the script and consumer inventory SHA256 values. Rerun with the exact
command in phase2-task-card.md; the external originals remain separately required.

| Existing input | Actual coverage | Quantity | Consequence |
|---|---|---|---|
| nz_historical_legal_supply.csv | 12 annual rows, 2012–2023 | cigarette-equivalents/year; source scenarios/bounds | Historical bridge only; bounds are not raw means, and fixed uplift shares source dependencies |
| nz_tobacco_release_tonnes_2010_2025.csv | 16 annual rows, 2010–2025 | tonnes/year, rounded chart extraction | Releases are not consumption; product exclusions, conversion and duty-free basis unresolved |

Both are existing consumer extractions, not newly verified publisher originals. They are
not independent surveys. Their overlapping years do not make the quantities compatible.
Their legacy numerical reference is preserved; neither is a current catchment assay series.
New matched NZ survey/intensity, prices, trade, population and actual WBE observations with
compatible uncertainty are not admitted by this task. No subtraction across these units,
current-year extrapolation or clamping negative historical discrepancies was performed.

## Actual Australian comparator and source discrepancy

Original: [ACIC report 25 research findings](https://www.acic.gov.au/sites/default/files/2026-04/Research%20findings.pdf),
saved outside tobac; SHA256 and retrieval are in phase1-source-receipts.json. PDF page
numbers below count this downloaded section from one; printed report pagination differs.

- PDF page 3 / printed 23: capital-city collection weeks occur every two months, regional
  weeks every four; public reporting changed to annual in 2025. Sampling and reporting
  frequencies are different fields.
- PDF page 6 / printed 26: cotinine and hydroxycotinine estimate aggregate nicotine;
  this method cannot separate tobacco, vaping and NRT. Programme cost, site-level raw
  observations and complete calibration uncertainty remain unverified for this model.
- PDF page 5 / printed 25, Table 7: visual and text checks agree on August 2025's
  22 capital and 42 regional plants, totalling 64; rounded catchment populations sum
  to 14.5 million. These are period-specific programme descriptors, not NZ parameters.
- Quarantine Q:ACIC25:coverage: page 3's capital-only population range conflicts with
  Table 7's October value of 11.1 million. Its narrative also names July where the
  collection/table sequence uses June. Preserve both locations; do not silently select
  a preferred denominator or construct a time-series likelihood from the discrepancy.
- PDF page 4 / printed 24: visual/text verification agrees on cumulative sample
  arithmetic, 12,269 + 1,611 = 13,880. These are programme samples, not nicotine-only
  independent measurements or a population denominator.

Text was extracted with pdftotext; pages 4 and 5 were rendered and visually inspected.
The text-only methodological fields are labelled accordingly, not independently verified
calibration. Figures were not digitised to invent site concentrations. The ABS experimental
nicotine article uses ACIC data; it is a linked derived estimate, not a second independent
nicotine observation. Its product-allocation assumptions need separate appraisal.

## Identification argument

Let N be total nicotine exposure in a matched country/catchment and period, after valid
measurement calibration. In compatible nicotine-mass units, write

    N = N_combustible_lawful + N_combustible_illicit + N_vaping + N_NRT + N_other.

This is an accounting identity, not a fitted likelihood. Even with N known exactly,
one aggregate equation does not determine the five nonnegative components. Shifting an
admissible amount between illicit combustible exposure and another unknown component
leaves N unchanged. A second metabolite of the same aggregate need not add a product- or
origin-specific restriction. Product-specific markers or independent compatible evidence
are needed to improve the rank/identified set; biomarker response assumptions matter.

With no further restrictions, illicit combustible nicotine can range from zero to N.
That is a trivial conditional bound on nicotine mass, not an estimated illicit tobacco
share. Releases L are an administrative flow in different units; they cannot replace
N_combustible_lawful without product conversion, consumption timing, stock, trade/tourism
and lawful unrecorded-flow reconciliation. An observed negative discrepancy is not proof
of negative illicit trade. Uncertain calibration and sampling coverage further weaken the
inference. Historical policy assumptions or an AU derived estimate do not supply the
missing current NZ equations.

Thus nicotine WBE may reduce aggregate-exposure uncertainty while leaving policy-relevant
product/origin uncertainty large. This does not establish zero decision value. EVSI needs
a joint measurement model and downstream policy consequences; ENBS also needs study costs,
delay and implementation. No empirical EVSI, ENBS or cost ceiling was computed here because
the required accepted joint model is absent. No hypothetical number is labelled empirical.

## Next executable milestone

1. Receive the existing owner's latest-lock native renewal; reopen actual admission and
   reuse unchanged foundation evidence. Do not mutate signatures or copy private bindings.
2. Complete Phase 1 live/native search qualification, exact policy baseline, external
   archive rights/destinations/readback, matched extractions and source-dependence review.
   Resolve or exclude the quarantined ACIC denominator with an explicit rationale.
3. Build the matched Silver panel using existing Scope/EvidencePacket/SupplyBasis, then
   prespecify the eligible holdout manifest and numerical tolerances before fitting.
4. Fit the simpler baseline and one supported retail/cessation contrast; compare WBE addition
   on held-out predictions. If identification remains insufficient, report bounds and
   unpriced decision ceilings only when their assumptions and joint decision model support them.

No full-suite/numerical replay is repeated for unchanged model code. Focused test outcomes
are recorded in phase1-progress.md; they establish software evidence, not source acceptance.

## Superseding source checkpoint — 7 November 2026

The Phase 0 local renewal is now qualified; the earlier missing-renewal statements above
are historical. The workbook's 16 release values already match its retained original
exactly in integration/archive/workbook-reconciliation.json. That closes value parity
at its original scope, not product/duty-free compatibility or current consumption.

P2.2 now acquires actual published NZHS 2024/25 CSVs outside tobac and reconciles 87
adult-total candidate records with their source hash and record ordinals. Three smoking/
intensity series have 14 survey-start labels; five vaping-related series have nine, with
2016 absent. No missing value is interpolated. New original-source definitions expose
range/top-code intensity measurement and a pipe/cigar denominator mismatch. A direct
Shiny-hosted CLI GET matches the browser original exactly; four separate Ministry-site
403s do not invalidate that route or the retained workbook qualification.

See phase2-reconciliation-20261107.md, phase2-task-card.md and
phase2-receipts-20261107.json for code, actual verification and the remaining gates.
The original identification argument still applies to aggregate nicotine alone;
Wang's additional anabasine/sales method has separately documented assumptions and
cannot be dismissed as an aggregate-metabolite-only method. Neither supplies an
accepted current NZ panel or a supported causal retail/cessation contrast here.
The complete P2 fit, held-out information comparison and empirical acceptance remain open.
