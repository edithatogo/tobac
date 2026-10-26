# 2025 product-return reconciliation

The bounded intake covers nine files for the eight issuers listed on the
[official 2025 returns page](https://www.health.govt.nz/regulation-legislation/smoked-tobacco/information-for-manufacturers-and-importers/tobacco-returns/tobacco-returns-2025).
All nine local CAS/WARC hashes, payloads and request identities were verified. Raw documents
stay in the consumer-owned local archive; Git retains metadata, numeric extracts and locators.
The native WARC writer omitted capture timestamps. The dated verification receipt does not
invent those timestamps or establish remote recovery.

The generated review table contains 28 measurement records. `product-extractions.json` retains
numeric components, original units, document/listing years, locators and extraction methods.
PDF text was reviewed; scanned PM tables used OCR followed by visual checks. Workbook numeric
cells were read with openpyxl and rendered to 15 significant digits to remove binary display
artefacts. This declared rendering and the source hashes remain auditable. These are dated
consumer extractions, not independent scientific endorsement or a fully automatic PDF parser.

## Findings that prevent national closure

- **BAT RYO year conflict:** the [linked RYO PDF](https://www.health.govt.nz/system/files/2026-08/BAT-Sales-RYO-2025.pdf)
  has a 2024 document heading. Its domestic/duty-free reported totals remain in the table but
  are excluded from 2025 subtotals. Filename and listing year cannot override that conflict.
- **R&S King quantity conflict:** the workbook's volume header/table implies 3,820 packs of
  20 (76,400 sticks); a separate note says 3,820 cartons of ten packs (764,000 sticks).
  Both interpretations are retained and excluded; they are alternatives, not additive sales.
- **Unknown channels stay unknown:** unlabelled workbook channels are kept as `unspecified`.
  PM's RYO schedule explicitly reports domestic sales; no duty-free RYO schedule was observed.
  That missing quantity remains null, not zero.
- **Measures stay separate:** sales mass, ingredient mass and additive mass have separate
  subtotal groups. PM RYO ingredient mass less additives equals the domestic sales sum:
  39.37814 − 4.67861 = 34.69953 tonnes. This useful arithmetic check does not prove an
  unreported channel is zero or establish the Ministry's national aggregate definition.
- **Products stay separate:** pipe tobacco is not RYO. Cigars/cigarillos are excluded from
  the workbook comparator; heated products belong to separate reporting outside this intake.
  Havana's aggregate tobacco weight is retained with unresolved product basis.

The verified workbook comparator is 755 tonnes for 2025. Factory-made sales counts cannot be
turned into tobacco mass without a justified product-specific mapping. Aggregate ingredient
weight conventions also differ or lack channel scope. Consequently reconstructed national
mass, mass residual and total cigarette equivalents remain **null**. The report's status is
`incomplete_source_conflicts`; valid software execution does not close those source questions.

Factory-made quantities with an explicit stick unit can retain their stick equivalents.
RYO mass is normalized between kg and tonnes, but a 2025 grams-per-stick convention has not
been independently qualified. The historical 0.7 g convention is not silently promoted into a
new empirical conversion. No RYO or national cigarette-equivalent total is emitted.

## Reproduce and review

```sh
uvx --python 3.15.1 --from nox==2026.10.20 nox -s product_reconciliation
```

Outputs: `outputs/engineering/product-reconciliation/report.json` and `table.csv`.
The retained dated output is `integration/reconciliation_2025/generated/`.
The command verifies the extraction/source receipt hashes, recomputes exact decimal sums,
checks overlapping/duplicate measurement declarations and keeps unlike units apart.
It does not download sources, re-extract scanned PDFs or condition a belief.

The native acquisition uses the existing archive producer CLI and the bounded consumer-owned
`integration/reconciliation_2025/tobac-products-2025.yml` source set. Select the retained
qualified producer environment (Python 3.15.1), a new WARC run directory and local CAS root:

```sh
/path/to/archive/.venv/bin/archive-govt-nz capture \
  --source-type tobac-products-2025 --config-dir integration/reconciliation_2025 \
  --store-root /path/to/local-cas --warc-dir /path/to/NEW-warc-run --format json
/path/to/archive/.venv/bin/python scripts/verify_product_assets.py \
  --store /path/to/local-cas --warcs /path/to/NEW-warc-run --out /path/to/NEW-verification.json
```

The verifier requires the qualified warcio version and actual object bytes; existing receipts
are not overwritten. A new source revision must receive a new extraction/provenance review.
The initial unconfigured CLI attempt was disabled, not counted as acquisition; the explicit
source-set execution captured all nine targets. Source interpretation is a separate check.

Matching-period rows retain the existing coarse MOH-returns underlying-data identity for 2025.
Period-conflicted or missing-quantity rows receive no qualified observation data ID. Splitting
one return into companies/channels does not make the national aggregate and its components
independent evidence. Signed return adjustments are preserved. No measurement-error parameter,
regulatory prior, existing scientific input/result, dependency lock or workflow pin changes.

Remaining research work is source clarification/revision for the conflicts, channel/product
coverage and physical conversions, followed by a justified target population, covariance and
transport model. This reconciliation does not implement broader ecosystem or archival-lineage
plans and does not imply a causal policy effect or current illicit-market estimate.
