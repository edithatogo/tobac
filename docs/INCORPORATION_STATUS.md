# Incorporation status and prior-work preservation

Dylan A Mordaunt | 25 October 2026 | Original audit base: `886fc08929f8e4e7e34fb6443bbf81545e52c3db`; M3 receiving base: `5218d831f8b2452c7937da91ee00bf9b96183b2d`.

The live `main` branch is authoritative. This index distinguishes executable incorporation,
reference-only preservation, reproducible outputs and work that remains incomplete. It is
not a claim that every historical archive file or proposed feature is now active.

## Incorporated work

| Work | Location / evidence | Status |
| --- | --- | --- |
| Regulatory M1/M2a decision and evidence interfaces | `src/tobac/`, `results/milestone1/`, `results/milestone2/`, `docs/evidence_interface.md` | Existing live implementation preserved. |
| M3 research design and implementation | `src/tobac/research/`, `tests/m3/`, `results/milestone3/`, `docs/research/M3_CONTRACT.md` | Six approved additions implemented conditionally; installed Voiage and hosted qualification remain open. |
| Empirical longitudinal models | `src/tobac_supply/`, `docs/empirical_longitudinal/INTEGRATION.md`, `results/longitudinal/` | Previously incorporated code, inputs and compact results preserved. |
| Cross-workstream contracts | `tests/test_workstream_integration.py`, `docs/WORKSTREAM_SYNC.md`, issue #1 | Existing tests and coordination preserved; the 26 cross-tests rerun with M3. |
| Library reuse, agent context and Conductor | `docs/engineering/`, `engineering/context/`, `AGENTS.md`, `vendor/conductor` | Existing implementation preserved; checkout/host activation not certified. |
| Dependency, security and release gates | `noxfile.py`, `scripts/lock_receipt.py`, `scripts/actions_diagnostics.py`, engineering workflows | Implemented at 886fc08; M3 adds a Nox session and separate qualification workflow without weakening existing gates. |
| Earlier measurement, calibration and action evidence | `evidence/prior_work/v2.9.0/data/empirical_intake_20261024/` | Preserved as historical reference-only material. |
| Earlier uncertainty, cost, time and survey inputs | `evidence/prior_work/v2.9.0/data/longitudinal_20261024/` | Preserved with original assumptions, limitations and source-version labels. |
| Candidate actions and information portfolios | `evidence/prior_work/v2.9.0/docs/decision_contracts/` | Prior candidate catalogue, not a replacement for live M2/M3 action definitions. |
| Data/pricing templates and assay/longitudinal addenda | `evidence/prior_work/v2.9.0/requests/` | Draft templates; not received observations, quotations, approvals or newly sent requests. |

## Exact preservation scope

The preserved snapshot has **19 files**, including **298 CSV rows** and **28 inherited CSL
records**. The rows mix source summaries, analyst assumptions, candidate definitions and
request fields; they are not 298 independent empirical observations. The 76-entry parameter
register includes aliases and shared uncertainties that must not be counted twice.

The source is the supplied `tobac_v2.9.0_20261024_EMPIRICAL_LONGITUDINAL.zip`, SHA-256:

```text
858fbdeebb5fd4ba8b224bc545c0283dda5a6138199959598eda943fbcf94473
```

The archive contains 1,007 regular non-Git entries. Only selected files absent from the live
repository were restored by the original audit. CSVs retain their fields, values and prose
with CRLF normalised to LF. Markdown addenda are byte-preserved. The reference list selects
the exact archived record objects used by these tables, with JSON whitespace reformatted.
This is not new bibliographic validation or confirmation that every source supports its
inherited extraction.

`integration/prior_work_manifest.json` records original archive member paths and hashes,
imported hashes, roles, row counts and source IDs. The snapshot subtree was matched against
the tested local Git tree. Existing active supply series were not duplicated or re-ingested.

The internal assumption labels `longitudinal_protocol` and `v2.6.0_parameter_estimates` are
explicitly recorded as non-bibliographic source tokens. Embedded archive paths retain their
historical meaning; they do not imply that every referenced predecessor file is in live main.
Some survey rows are deliberately marked superseded; select appropriate versions rather
than treating revisions as independent data. Missing confidence limits remain missing.

## Use before promotion into the live model

A preserved table is not a new likelihood. Review its observation period, matrix, product,
population, units, source identity, dependence and evidence role before any use. Historical
assays are not current observations; urine limits are not wastewater limits; AU derived
endpoints are not raw NZ measurements. Request fields are not supplier quotations. Planning
costs and policy-effect transfer factors remain analyst assumptions.

Use the existing `tobac.evidence` route for a scientifically supported update. Reconcile
underlying MOH/NZHS data identities and source versions once. Forecasts and posterior paths
cannot be relabelled as independent observations. Changes to the live parameter set require
a separate reviewed mapping, tests and relevant numerical reruns, not an automatic import.

## Still separate, pending or blocked

- **M3 qualification:** source, tests, contracts and complete saved full/refinement outputs
  are incorporated. `integration/m3_requirement_status.csv` separates implemented methods
  from the blocked genuine installed-Voiage acceptance criterion. Innovate/Kairos remain
  optional; no fitted external output is claimed. See `results/milestone3/report.md`.
- **Full predecessor archive:** legacy engines, older protocols, manuscript/submission
  packages and previous outputs remain in the original archive unless separately mapped.
  Obsolete submission-ready wording is not promoted into the active project. Neither the
  audit nor M3 deletes the original archive or claims all its files are replicated in GitHub.
- **Large generated results:** current longitudinal posterior paths and rendered figures are
  produced by checked-in runners. M3's complete 24 CSV/JSON files are saved in the hashed
  archive with a bounded restoration script. Generated results are not new observations.
- **External execution:** transitive hash locks, full strict/security execution, genuine
  third-party qualification and hosted runner availability remain open. A preserved receipt
  describes its actual scoped run, not fresh execution of the entire current repository.
- **Scientific readiness:** current paired NZ assays, qualified action consequences, costs,
  governance and empirical funding inference remain distinct requirements.

## Verify

```sh
python scripts/verify_prior_work.py
python -m pytest -q tests/incorporation/test_prior_work.py
# Optional: compare imported members against the actual predecessor ZIP.
python scripts/verify_prior_work.py --archive /path/to/tobac_v2.9.0_20261024_EMPIRICAL_LONGITUDINAL.zip
python scripts/unpack_m3_results.py --out outputs/m3_saved
python scripts/verify.py outputs/m3_saved/full
python scripts/verify.py outputs/m3_saved/refined
```

The prior-work verifier rejects altered/missing/unregistered files, invalid paths, inconsistent
row counts, lost source-ID linkage and declarations that the import supplies current data.
The M3 unpacker checks part/full hashes, member paths, bounded sizes and non-overwrite.

The original incorporation audit executed **21 scoped tests**, archive/member comparison and
compilation checks; `integration/incorporation_verification_20261025.json` records that run.
M3 executed **162 scoped tests** and **2,105 full-run invariants**, including the real shared
interface tests, but not every supply/engineering/incorporation test in the live checkout.
See `integration/m3_local_verification.json` for exact scope. Receiving commits and actual
hosted outcomes are posted to issue #1/#4, not assumed from these documents.
