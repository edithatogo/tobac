# Dynamic decisions and stronger empirical evidence

Status: implementation and parameter-evidence candidate; native scientific qualification pending.
Owner: repository owner. Started 8 November 2026 from accepted main `d735896`.

- [Implementation plan and completion evidence](plan.md)
- [Model design, broader decisions and frontier benchmarks](design.md)
- [Parameter evidence edition: 61 typed candidate values and constraints](design.md#parameter-evidence-update--9-november-2026)
- [Machine-readable catalogue and reproducible JSON/CSV export](design.md#portable-catalogue)
- [Executable frontier experiments BF1–BF6](design.md#executable-frontier-extension--9-november-2026)
- [Incremental systematic review with Searchright](searchright.md)
- [Public comparison-data pack](../../../evidence/public_data_20261108/README.md)
- [Dynamic reference implementation](../../../src/tobac_supply/dynamic.py)
- [Parent NZ/AU empirical programme](../nz_au_empirical_20261106/index.md)
- [Existing research gates](../../research-gates.md)

This companion implements bounded improvements requested after the repository
assessment. It extends the parent programme, including its existing Searchright
requirement R01; it does not replace that programme or mark its empirical gates
complete. PR #146's source review is now merged; source acquisition and empirical
admission remain separate. Current development is consolidated in draft PR #147.

## Active parameter-sourcing continuation — 9 November 2026

- [x] Source and attribute 61 numerical entries from 14 source/reuse identities:
  dated rates/prices, cessation outcomes, demand responses, mortality, dynamic
  endpoints, dose-response and assay-method values; distinguish source assumptions.
- [x] Preserve units, populations, periods, actual uncertainty and shared-study
  identity; record review depth and ten remaining gap groups.
- [x] Derive the four-category daily-use NZHS crosswalk and rounding envelopes
  without claiming never/former-state identification or joint confidence intervals.
- [x] Validate the portable packet: 104 assertions including six negative controls;
  supply canonical JSON hash and an exporter that refuses to overwrite outputs.
- [x] Specify BF1–BF6 with explicit baselines, measurements of success, ordering and
  provider boundaries; retain existing empirical validation and native gates.
- [ ] Reconcile candidate study aliases with the existing Searchright corpus and
  finish result-specific appraisal where only abstracts have been inspected.
- [ ] Complete source-edition capture, archival verification, source-to-target
  transport and existing-contract admission before changing any runtime parameter.
- [ ] Extract and reconcile age/sex/cause baseline hazards; complete utility,
  incremental resource-cost and subgroup evidence. Located sources are not extracted tables.
- [ ] Implement BF1 using the existing finite oracle and partial-identification
  machinery; then execute the bounded two-product BF2 adaptive-calibration benchmark.
- [ ] Complete PR #147's separate native qualification and issue #3's matched
  measurement, causal-response and independent-validation requirements.

This edition is an auxiliary evidence catalogue inside the existing public design
record, with standalone JSON/CSV export. No publication allowlist, source hash,
accepted output, active default, prior, likelihood or dependency is changed.
Catalogue validation is not a fresh full-repository or native test result. The
original source-byte archive and broader systematic screening remain incomplete.
