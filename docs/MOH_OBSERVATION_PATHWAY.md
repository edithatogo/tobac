# MOH tobacco-release observation pathway

The 26 October 2026 qualification re-executed the existing archive producer's verifier
against the retained source objects. The workbook and WARC match their original hashes;
the WARC payload equals the CAS object and binds the request URL. Native openpyxl parsing
and a fresh consumer comparison reproduce all 16 year/value pairs exactly. These checks
close current transcription/fixity questions, not empirical calibration.

Receipts and specifications:

- `integration/archive/moh-workbook-qualification_20261026.json`: actual native execution,
  producer/tool identities, original hashes and 16 matched rows.
- `integration/archive/moh-observation-specification.json`: established scope, explicit
  unknowns and measurement/dependence requirements.
- `integration/archive/moh-observation-proposal_20261026.json`: dated consumer proposal.
- `integration/archive/moh-observation-handoff-report_20261026.json`: report regenerated
  while the verified workbook and WARC were locally staged.

The original archive bindings, consumer CSV, earlier handoff proposal/report and all model
inputs/results are unchanged. Current acquisition/recovery remains owned by archive-govt-nz;
its open PR #776 is separate from this consumer execution. No raw source objects are committed.

## Scope established and scope still unknown

The [official 2025 page](https://www.health.govt.nz/regulation-legislation/smoked-tobacco/information-for-manufacturers-and-importers/tobacco-returns/tobacco-returns-2025)
identifies a national retail-release aggregate for calendar 2025, separates heated products,
and links the retained workbook. Its chart/workbook excludes cigars and cigarillos. This was
reviewed on 26 October; the page's update date is not an archive capture time.

The workbook labels years 2010–2025. Only the 2025 calendar scope has been explicitly
re-established from that current page; the earlier consumer calendar labels remain declared
periods pending historical-definition confirmation. The aggregate is not a sample of resident
consumption. Pipe-tobacco treatment, older product definitions and duty-free aggregation are
unresolved. Returns can distinguish domestic/duty-free channels; their existence does not prove
how this particular aggregate combines them. The 2025 source Scope is recorded, while the
unresolved historical scopes remain null. The target catchment/population remains proposed.

Total tonnes cannot be divided by 0.7 g to obtain the model's combined factory-made/RYO count.
That requires separate factory-made counts and RYO mass with an audited convention, plus
consistent pipe/heated-product and duty-free treatment. No conversion is performed here.

## Measurement and dependence specification

The structured specification separates compatible national release mass from shared reporting
error, period error and reporting resolution. Integer values show a one-tonne reporting
resolution; they do not establish a uniform rounding distribution or zero measurement error.
The documented covariance family is a candidate to qualify, with no fitted variances or
correlations. The existing `release_loglikelihood` interface already requires compatible units
and an explicit positive-definite covariance; this task adds no second likelihood engine.

For overlapping allocation windows, the covariance must propagate as `A Sigma A^T`. A
singular/redundant set of derived aggregates cannot become independent observations. Phyo
summaries reuse MOH/NZHS data: use a single underlying-data representation and a justified joint
model, not separate likelihood factors for the same records. Stock, border flows, product
coverage and source-to-target transport remain scientific work.

## Capture date and replay

The original WARC has no `WARC-Date`. The new receipt's `verified_at` records this verification
execution only. It does not repair the original capture date or reconstruct a historical edition.
Earlier receipts and source bytes are preserved. The report therefore retains the capture-date
gap even for the verified workbook rows.

Use the repo-local Python 3.15.1 Nox environment and explicitly selected qualified producer paths:

```sh
uvx --python 3.15.1 --from nox==2026.10.20 nox -s moh_workbook -- \
  --producer /path/to/archive-producer-checkout \
  --producer-python /path/to/archive-producer-checkout/.venv/bin/python \
  --archive /path/to/retained/canonical/archive \
  --objects outputs/engineering/NEW-moh-objects \
  --out outputs/engineering/NEW-moh-receipt.json
```

The input descriptor pins the producer script, register, capture receipt and qualified Python /
openpyxl / warcio identities. Changed inputs fail closed. The command is read-only against the
producer/canonical archive; it creates a new consumer staging directory and receipt. Existing
output paths are refused. Missing native objects are a real execution gap, not a synthetic pass.

Regenerate the dated proposal report using `scripts/source_handoff.py --proposal
integration/archive/moh-observation-proposal_20261026.json --objects <new staged directory>
--out <new report>`. Hosted tests check protocol/parity guards, not the availability of the
local canonical archive. A retained receipt is dated execution evidence, not fresh remote recovery.
