# First empirical slice — source reconciliation, 7 November 2026

P2 remains in progress. Public NZ survey originals are now acquired and a reproducible
candidate extraction is implemented; a matched consumption likelihood, supported policy
contrast and held-out wastewater comparison are not established. No P2 plan row is closed
by these enabling results alone.

## Original NZ survey edition

The Ministry's official Annual Data Explorer 2024/25 provides three CSV downloads:
prevalence/mean, subgroup comparisons and changes over time. The internal browser
successfully downloaded all three into a separate external intake edition. Its visible
copyright statement identifies CC BY 4.0; retain attribution and the original terms.
The stable prevalence URL is:
https://minhealthnz.shinyapps.io/nz-health-survey-2024-25-annual-data-explorer/data/nz-health-survey-2024-25-prevalences.csv

A supported CLI GET to that observed application asset returned HTTP 200, text/csv and
6,088,525 bytes with SHA256
6d3e0a019d7e32030147f128c21098f074683cd3cfef41b0dcfff85b74b6b915.
Those bytes equal the browser download exactly. Use this qualified CLI route for the
remaining source work. The four separate health.govt.nz page/workbook/PDF requests
returned HTTP 403; preserve those failures without labelling their bodies source data
or treating this as a denial of the working Shiny-hosted route.

Original CSVs and candidate rows remain outside tobac in
/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2. Exact request/download time
precision, source asset names, hashes, byte counts and failure responses are retained
there. Download completion observations are not fabricated HTTP response timestamps.
No upload, native registration or redistribution permission beyond the observed source
terms is inferred from a successful acquisition.

The Ministry’s separate [2023/24 correction notice](https://www.health.govt.nz/monitoring-statistics/surveys/new-zealand-health-survey/publications/202324-survey-publications/corrections-made-to-202324-data) names specific access/mental-health and child questionnaire items, rather than
smoking questions. Do not infer a smoking-series retraction from that notice. This
web-read context does not replace original-byte/version qualification of the CSV.

## Executed extraction and coverage

The existing audit_empirical_coverage.py now optionally reopens this hash-bound CSV
through the existing source_handoff path/fixity checks and Polars. It retains the original
19 columns plus a logical data-record ordinal, then selects adult total-population rows
for eight prespecified smoking/vaping indicators. Only the total estimate/CI triplet is
audited numerically; sex-specific fields remain original unvalidated fields. No second
canonical observation contract or EvidencePacket is constructed.

The source export contains 47,708 records. Its selected 87 candidate records comprise:

| Series | Actual survey-start labels | Records |
|---|---|---:|
| Current smokers, daily smokers, mean cigarettes | Each 2011 through 2024 | 14 each |
| Daily vaping and four daily-only/dual/union indicators | Each 2015 and 2017 through 2024 | 9 each |

All selected total estimate/CI triplets are present and unflagged in this source edition.
The missing 2016 label in the vaping-related series remains absent; the extraction does
not interpolate it or infer why it is absent. Other source rows can carry S/e publication
flags. The helper preserves flagged values and withholds their numeric triplets from
usable coverage; unknown flags, nonfinite/reversed/out-of-range marginal intervals,
duplicate indicator/year records and changed schemas or hashes are rejected.

Raw source year 2024 corresponds to the explorer's 2024/25 survey label. The helper
preserves the source-start-year convention and does not invent exact ISO observation
boundaries. The native page says collection spanned July 2024 to July 2025, which does
not establish calendar-year consumption. Suppressed/missing values are not zeros.
Existing candidate editions and in-repository candidate-output destinations are refused.

## Measurement and matching constraints

The native indicator definition says daily-smoking prevalence covers established
smokers aged 15+ who smoke daily and have smoked more than 100 lifetime cigarettes.
The intensity definition is the mean number of cigarettes per day among daily smokers,
excluding those who mainly smoke pipes/cigars. It is calculated from categorical ranges
using midpoints and a top-coded final category. These definitions were checked after
the selected indicator and loaded definition agreed; the UI updates asynchronously.

Consequently, multiplying the two published marginal quantities does not produce a
verified all-person/all-product total. Missing corrections include the differing pipe/
cigar population basis, nondaily and younger consumption, range/top-code measurement
error, survey weights and joint covariance. Published estimated counts are rounded and
share the survey source; do not reconstruct a precise denominator by division or treat
counts, prevalence, ratios and trend exports as independent measurements. An uncertainty
interval for a product cannot be manufactured from unrelated marginal CI endpoints.

The existing release workbook is already source-verified in
integration/archive/workbook-reconciliation.json: all 16 values match the original
workbook, whose SHA256 is 3a55a6469097ebc3fb27a6143db7749e5b885761ada76b197053dfe76f36e883.
The earlier feasibility statement that these are only unverified chart extractions is
historical at this checkpoint. This does not resolve the workbook's product conversion,
duty-free/stock/tourism or administrative-scope limits. A failed fresh HTTP request does
not invalidate the retained original-byte qualification or prove source absence.

Do not join a survey-start label to calendar-year releases as if their intervals and
products matched. Prices, trade, compatible population denominators, lawful unrecorded
flows and NZ nicotine/tobacco WBE observations are still not assembled as accepted matched
inputs. Australian NWDMP and Wang/FTI-derived estimates retain their own dependence and
calibration limitations; they are not new NZ observations. The P1 source quarantines remain.

## Validation and the next empirical operation

The source helper retains explicit false values for new observation admission, verified
ISO dates, available joint covariance and a frozen holdout manifest. This is deliberate:
these conditions have not passed. Preserve the previously specified holdout rule, but do
not label a complete survey marginal year a complete matched country/product panel.

Before fitting, close original/destination admission and scope reconciliation; freeze
the actual joint observation/holdout manifest; establish a supported retail/cessation
contrast under the current legal baseline and a justified measurement/dependence model.
Then evaluate the simpler baseline and incremental WBE on the same held-out observations.
If the required data remain unavailable, report the supported identified set and explicit
non-identification limits. Do not substitute synthetic observations, an independence
assumption, a transported causal effect or a zero programme cost to produce a fit.

Actual command outcomes and retained corrections are in phase2-receipts-20261107.json.
The original finite-state engine, its reference inputs and all M3 interfaces are unchanged.

## Source freeze verification

The final Nox tests session passes 1,289 tests with 22 real capability skips and 92%
coverage of src. New audit tests run; the skipped cases concern separately qualified
clustering, native/private lineage, Snakemake, mutation tooling, Voiage and Ruff tool
environments. They are not empirical tests claimed successful. Whole-source typing
passes with zero errors/warnings in the lane’s own Python 3.15.2 audit environment;
affected-file Ruff check/format passes with its locked 0.17.4. The independent CSV reader
reopens all three original hashes and verifies every original field of all 87 candidate
records against its logical source ordinal. All three candidate editions have identical
bytes. The first unbounded extraction and corrected bounded runs remain separate.

The combined tests/reproduce attempt retains its final failure: numerical checks ran,
but the clean-source publication replay refused the uncommitted checkout. Source will
be committed before that required clean-source operation is rerun; this is not a waived
gate or a successful full reproduction claim. Terminal clean-source evidence follows
as a separate metadata closeout. No empirical likelihood or native original is changed.

## Terminal clean-source reproduction

Nox reproduce passes from clean source a818f28860196e61661fdb2b685320699c892ad2
using actual repo-local Python 3.15.2 (705.5 MiB sampled group peak, exit 0). Its
independent clone has the same commit and source tree. Both publication variants
reproduce all 29 compared CSV tables with zero numerical difference and zero report
difference. The source-defined absolute comparison tolerance remains 1e-10; none was
changed. This reuses qualified dependencies and is not a fresh/offline install or
OS network-isolation claim. The earlier dirty-source refusal remains in the receipt.

Source code is frozen at a818f28; the subsequent closeout changes metadata only. The
P1 branch remains frozen at 403600b. The existing integrator is idle at the scoped
readback and retains native/archive ownership. The three new NZHS originals and their
87 candidate records still require exact destination/source admission before fitting.
No cross-chat message, external upload or publication has been performed.
