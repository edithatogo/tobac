# Public comparison data — 8 November 2026

This candidate contains **282 table records in ten CSVs**: 193 Australian
records and 89 New Zealand records. It closes part of the public comparison-data
gap. It does not close the matched current NZ empirical-evidence gate and is not
loaded by the accepted model or evidence conditioner.

## What is included

| Files | Coverage | Interpretation |
| --- | --- | --- |
| Five `abs_*_quarterly.csv` tables | 37 quarters, December 2016–December 2025 | Nicotine quantities; current-price spending; spending sensitivity scenarios; price indices; volume indices |
| `abs_total_hfce_growth_annual.csv` | 2018–2025 | Effect of the experimental treatment on total household consumption expenditure growth, not tobacco-only growth |
| `nzhs_prevalence_2024_25.csv` | 18 percentages, nine reported population strata × two indicators | Published daily smoking and daily vaping prevalence |
| `nzhs_counts_2024_25.csv` | Two estimated national counts | Daily smokers and daily vapers; the same survey information as the prevalence estimates |
| `nzhs_smoking_ci_2024_25.csv` | 15 daily-smoking estimates with 95% confidence intervals | Published academic reporting of the same NZHS, including additional deprivation/age strata |
| `nzhs_vaping_union_ci_2024_25.csv` | 54 estimates with 95% confidence intervals | 18 strata × current vaping, daily vaping, and the union of daily smoking/vaping; two high-sampling-error flags retained |

The ABS tables are from its [3 June 2026 experimental release](https://www.abs.gov.au/articles/household-consumption-illicit-tobacco-and-nicotine-products).
The NZ figures are from the Ministry of Health's [2024/25 smoking and vaping summary](https://www.health.govt.nz/monitoring-statistics/surveys/new-zealand-health-survey/publications/202425-survey-publications/trends-in-smoking-and-vaping),
updated 19 November 2025. The [manifest](manifest.json) records publishers,
licences, source sections, units, dates, hashes, dependence groups and restrictions.

The additional interval/union extracts are attributed numerical facts from
[Nip et al., 26 November 2025](https://www.phcc.org.nz/briefing/smoking-prevalence-and-trends-important-findings-2024-25-new-zealand-health-survey)
and [Edwards et al., 3 December 2025](https://www.phcc.org.nz/briefing/vaping-prevalence-and-trends-findings-2024-25-nz-health-survey).
These authors report/analyse the same NZHS. The records supplement the Ministry
summary; they do not constitute an independent survey. Article text, images and
original files are not redistributed. No blanket PHCC article licence is claimed.

## Acquisition and reproducibility

The ABS original HTML was downloaded and SHA-256 checked. Every displayed table
was extracted mechanically; thousands separators were removed and original
decimal precision retained. The original remains in ignored acquisition storage;
transfer to the repository's canonical external source archive is still pending.

To reproduce from that exact downloaded HTML into a fresh directory:

```sh
python scripts/extract_public_comparators.py \
  --abs-html /path/to/abs-nicotine.html --out outputs/abs-comparators-reextracted
```

The extractor rejects changed original bytes, unexpected table shapes and
existing output files. A new source revision requires a new reviewed data version.
Each published CSV has a separate digest and schema in `manifest.json`.

The NZ official page was readable through web retrieval, but direct downloads
from the acquisition environment returned HTTP 403. Its 20 numerical facts were
transcribed from the identified text sections, not digitised from charts. **No
original-byte snapshot or source-file hash is claimed for that page.** The CSV
hashes prove the identity of this extraction, not its equivalence to an archived
original. The PHCC interval/union tables were also readable through web retrieval,
but direct HTTP downloads returned 403; their numerical facts were transcribed
from the specified table/text sections. Original capture and independent extraction
readback remain open for all three NZHS-related pages.

### Official NZHS reconciliation — 9 November 2026

The separate official Annual Data Explorer CSV was retrieved successfully and
matches the parent's previously captured edition exactly: 6,088,525 bytes,
SHA-256 `6d3e0a019d7e32030147f128c21098f074683cd3cfef41b0dcfff85b74b6b915`.
The publisher's Data Explorer explicitly licenses its work and downloadable
aggregate datasets under CC BY 4.0. [Retrieval and rights record](verification/official-source-retrieval-20261109.json).

[Reconciliation](verification/nzhs-reconciliation.json) verifies all **89 point
estimates, 69 confidence-interval pairs and 54 explicit caution flags** against
that original CSV. [The separate annotation table](verification/nzhs-reconciliation.csv)
records exact original row ordinals, field names, estimates, marginal intervals
and publication flags. It also supplies original-source marginal intervals for
the 20 summary rows without rewriting their initially reported uncertainty.

The 89 representations resolve to 73 distinct source cells across 67 original
records. Counts and percentages share survey information, and the strata overlap;
73 distinct cells do not establish 73 independent observations. No numerical
tolerance or repair was needed. Original extract bytes and source attribution
are preserved. The earlier failed summary/PHCC page downloads remain historical
capture limits for those pages; they no longer block checking these numbers
against the official CSV. Canonical archive admission, joint covariance and
the matched consumption/causal requirements remain open.

The maintained `scripts/reconcile_public_nzhs.py` reproduces these annotations
from the pinned original and this pack. It rejects changed source/extract bytes,
unknown or suppressed values, incorrect scopes, interval/flag mismatches and
duplicate identities before writing a new output edition. Its output adds no
independent observation and never conditions the accepted model.

## Interpretation constraints

- Australia and NZ have different geography, population, product and time scopes.
  Do not transport the Australian illicit fraction directly into NZ.
- ABS results reuse wastewater, survey and administrative inputs. Its product
  splits and related ACIC/ATO/ITEC outputs are not independent observations.
  An ABS model output is a comparator, not a fresh likelihood contribution.
- Kilograms of nicotine are not cigarette counts, per-capita exposure or health
  effects. Price and volume indices are not physical quantities. Spending is AUD,
  not NZD. No conversion is supplied implicitly.
- ABS lower/central/upper spending scenarios vary assumptions. They are not
  confidence or credible bounds. Published rounding can make the sum of the four
  product columns differ from the displayed total; no cell has been repaired.
- NZHS smoking and vaping overlap. Population strata overlap the national total,
  and ethnicity groups must not be assumed mutually exclusive. Counts and
  percentages are derived from the same survey. They cannot be summed into the
  prototype's mutually exclusive states.
- The original Ministry summary extract lacks numerical confidence intervals.
  The linked PHCC extracts supply 69 published intervals and smoking-or-vaping
  union estimates, while survey covariance, a full never/former/current state
  partition and catchment population crosswalks remain missing. A union is not
  dual use alone; do not combine marginal intervals as independent errors to
  construct a dual-use interval. Missing uncertainty is not zero. Cross-sectional
  prevalence does not identify initiation, cessation, relapse or switching rates.

## Still missing

A usable current NZ measurement panel needs matched catchment/date flow and
population, effective detection/censoring limits, processing/recovery information,
measurement covariance and product-specific calibration. Policy simulation also
needs transported causal effects and implementation parameters. These remain open.

The parent's [workbook reconciliation](../../integration/archive/workbook-reconciliation.json)
already records the retained official 2010–2025 tobacco-release workbook and
exact original-value parity for 16 annual records. This supersedes the earlier
pack-wide impression that the workbook had only been located. Source-specific
product/channel compatibility and conversion into matched consumption remain open.
Company sales, dispensing counts and seizures do not directly observe consumption,
successful quitting or the total illicit market. No restricted data collection or
contact with data holders was performed.

Before empirical use: complete canonical source capture, independently verify
extraction, resolve units/uncertainty/dependence, pass the existing evidence
contract and renew native scientific lineage. This pack is reviewable public
comparison material while those requirements remain open.
