# Kim source-native measurement comparison — 9 November 2026

This pack makes the previously external Kim extraction and measurement checks
reproducible from the exact public supplement. It contains reported numerical
facts and conditional arithmetic. **It does not qualify the prespecified
existing-evidence-versus-wastewater empirical score, admit a likelihood, fit a
current NZ policy response, or estimate monetary value of information.**

The first-comparison [review](../../conductor/tracks/nz_au_empirical_20261106/first-comparison-review-20261109.md)
and [decision contract](../../conductor/tracks/nz_au_empirical_20261106/decision-definition.md)
continue to govern interpretation. The existing P2.23–29 calculations are
reproduced here rather than counted as another independent study.

## Source and files

Source: Kim et al., DOI [10.1016/j.scitotenv.2025.181223](https://doi.org/10.1016/j.scitotenv.2025.181223),
[publisher supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0048969725028657-mmc1.pdf).
The original is 1,306,212 bytes, SHA-256
`c2ce1d0c3fcc95e9c49acb5bf403cc2598b999a97b8a9e558557a3aa1614046c`.

| File | Contents and source locations |
|---|---|
| [occasions.csv](occasions.csv) | 144 plant/month/nominal-weekday slots from Table S3, PDF page 8; 142 collection occasions and two absent Whangārei October slots |
| [measurements.csv](measurements.csv) | 576 analyte slots from S13, S15, S17 and S19, PDF pages 34, 37, 40 and 42; original means, duplicate-assay SDs, cell text and source locations |
| [nicotine-diagnostics.csv](nicotine-diagnostics.csv) | 144 slots retaining S23's reported mean and SD, PDF page 46, alongside conditional reconstruction checks using the same COT/COT-OH observations |
| [anabasine-scenarios.csv](anabasine-scenarios.csv) | Each of 144 ANBA slots under three separate calibration assumptions: 75 numerical conversions, 351 censored entries and six absent entries |
| [comparison.json](comparison.json) | Original/layout/converter/code/output hashes, numerical findings, calibration provenance, source support and explicit target-validation refusal |

The 142 occasions span **2 May–29 October 2023**, with 43 distinct calendar dates
at 12 plant labels. Seven actual dates disagree with the nominal Wednesday/Sunday
column. Both fields are retained; the nominal weekday is never substituted for
the printed date. Four analytes and the derived nicotine total share each
collection occasion. Neither multiple analytes nor calibration scenarios create
independent observations.

## What the numerical checks establish

The analyte tables contain **451 quantified, 117 censored and eight absent cells**.
ANBA alone accounts for all 117 censored cells; only 25 ANBA occasions are
quantified. S19 places the censored measurements between detection and
quantification limits. Their numerical bounds are not established at the
sample-specific influent/load scale, so the corresponding means, SDs and
conditional conversions stay empty. Missing occasions remain a different status.

Using the reviewed reconstruction `1.35 × (COT + COT-OH)` and nearest-print
rounding, **136 of 142 reported nicotine means are compatible** and six exceed
the 1.85 mg/day/1,000 people rounding allowance. Hamilton on 25 June has the
largest signed residual: the reported 3,133 compared with reconstructed
3,123.90, a difference of 9.10. This diagnoses incompatibility under the stated
linear reconstruction, exact factor and rounding assumptions; it does not
identify which unrounded input or processing step explains the difference.

For exactly two paired replicates, the SD of a sum must reach one of the
positive/negative correlation endpoints. After allowing each printed SD its
rounding support, **137 occasions are compatible with a paired endpoint**, two
only with the wider correlation envelope, and three are outside that envelope.
For Auckland South on 22 October, the reported total SD is 325 while the largest
compatible value under these assumptions is 105.30. The published value is
preserved. Duplicate-assay spread is not population uncertainty, a standard
error for catchment consumption, or an identified joint covariance.

These reproduce the findings documented in
[P2.28–29](../../conductor/tracks/nz_au_empirical_20261106/phase2-reconciliation-20261107.md).
The agreement is a check of the new implementation against the retained
reconciliation; it does not assert a new canonical archive readback.

## Calibration scenarios

The conditional ANBA arithmetic divides the printed load by each factor below.
The conversion from mg to µg cancels the reported denominator of 1,000 people,
so the numerical result is a conditional cigarette-equivalent index per
reported contributing person per day. It is not an admitted consumption estimate.

| Scenario | Factor, µg/cigarette | Relevant limitations |
|---|---:|---|
| [Zheng 2023](https://doi.org/10.1021/acs.est.3c01510) | 0.91 | Assumed nicotine dose and excretion combined with a pooled urine ratio; the separate 1.07 sewer correction is not applied here |
| [Bade 2020](https://doi.org/10.1002/dta.2874) | 1.13 | Ten smokers, self-reported cigarette counts and assumed daily urine volume; retained table/narrative discrepancies |
| [Weng 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13389531/) | 0.64944 | Conditional arithmetic `0.0902 × 0.0072 mg/cigarette × 1000`; 19 selected above-LoQ cigarette users and an assumed absorbed dose |

These are separate sensitivity assumptions. They are not pooled, not independent
likelihoods, and not a calibrated uncertainty distribution. Weng's reported
4.95% spread has no independently established statistic and is not used as SD,
SE or a distribution. The output intervals cover **printed-load rounding only**;
they are not confidence intervals and exclude calibration, source attribution,
sewer losses, sampling, denominator and transport uncertainty. Computational
precision in derived values is not additional measurement precision.

No campaign or national mean is calculated from the selected 25 quantified
ANBA observations. The unquantified majority cannot be replaced by zero,
the limit of quantification, a foreign assay threshold, or an assumed midpoint.

## Reproduction

Keep the original PDF outside the source repository and run:

```sh
.venv-review315/bin/python scripts/compare_kim_measurements.py \
  --pdf /path/to/pinned-kim-supplement.pdf \
  --out outputs/kim-measurements-new-edition
```

The executed converter was **Poppler pdftotext 25.03.0**, using
`-layout -enc UTF-8`. Its 110,110 output bytes match the historical text SHA-256
`4675a51a4938a717434aa855ce90157a76722c6f2f31be0692793c3df60f7b7a`.
The manifest records the converter executable hash and version as well as the
PDF, text and code hashes. Converter identity alone does not pin all host shared
libraries; exact rendered-text parity is required before parsing. A different
converter output, changed PDF, malformed cell, unexpected missingness, changed
review status, or existing output directory is rejected.

This parser is qualified for this one source edition. It is not a general PDF
parser and does not fetch or silently adopt a newer source. No new Python
runtime dependency is added. Unit fixtures use synthetic text and do not claim
to execute an unavailable converter or retrieve publisher bytes in CI.

## Remaining empirical requirements and rights

The first comparison still requires compatible observation admission, dated
flow and contributing-population provenance, effective censoring/processing,
calibration and policy-response bridges, and an independent target outcome.
This six-month source supplies no complete validation year and three earlier
complete years. Twelve printed plant names do not establish four qualified
comparable catchments. The paired predictive score and empirical VOI therefore
remain unavailable; their absence does not establish zero decision value.

The original supplement, article text and graphics are not redistributed here.
The CSVs contain attributed numerical facts and authored derived checks. No
blanket licence or permission to redistribute the publisher original is asserted.
Canonical archive readback and native scientific qualification remain separate
requirements; all admission/automatic-conditioning flags in the manifest are false.
