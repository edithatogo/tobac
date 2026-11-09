# First comparison review, admission decision and implementation — 9 November 2026

Owner direction: finish evidence review/admission for the first comparison and
continue implementation. Start from PR #147 head `c353d6f`, including accepted
main `d0e832b`. This continuation supersedes earlier task-card restrictions on
which local files this work may edit; scientific source-admission requirements,
the public-only direction and historical receipts remain in force.

## Scope

Finish a bounded review of the evidence needed to compare existing evidence with
the addition of wastewater for the declared retail/cessation decision. Reuse the
237 recorded source checks and existing Searchright/source-native search corpus.
Do not label the much broader unfinished screening programme complete. Resolve
specific public-source gaps where possible and issue an explicit disposition for
each source and each proposed role. A source can support methods or descriptive
checks while remaining unsuitable for an empirical likelihood or independent score.

Reacquire the pinned official NZHS export, independently reconcile the public
comparison pack against its original values/intervals/flags, and implement an
executable first-comparison eligibility/admission audit using existing
`source_handoff`, `Scope` and candidate extraction contracts. Review labels are
not admission authority. Native original/WARC readback, measurement calibration,
matched outcome and policy-effect requirements must be demonstrated or retained
as explicit failed gates. A missing datum is not zero.

Implement the next conditional dynamic-model interface by reusing the existing
health kernel: competing mortality and origin-state person-time within an
interval, followed by survivor movement at its boundary. Keep mortality supplied
in hazards only on this interface, so it cannot also be applied in the transition
matrix. No empirical hazard, tobacco effect or national decision is inferred.

## Owned changes and reusable components

- Existing empirical/dynamic Conductor records and dated first-comparison review,
  source dispositions, task and execution receipts.
- `scripts/audit_first_comparison.py` and focused engineering tests, reusing the
  existing admission and source-coverage checks.
- `scripts/reconcile_public_nzhs.py`, focused engineering tests and public-pack
  verification metadata, reusing the exact official export schema and hash guards.
- `src/tobac_supply/dynamic.py` and `tests/supply_bridge/test_dynamic.py`, reusing
  `tobac.health.exposure_health_step` rather than duplicating mortality equations.
- Exact reviewed publication inventory entries and current navigation/status.

Original downloads remain outside the source checkout. New extraction/verification
tables are source-attributed derived facts; no third-party article prose or graphics
are published. The accepted native checkpoints and numerical references are preserved.

## Execution and acceptance

- [x] Review first-comparison source roles, dependence, scope and unavailable fields;
  independently check live primary sources for specific resolvable gaps.
- [x] Verify the pinned NZHS original and map the existing public fact pack to exact
  source records, fields, intervals, rounding and publication flags.
- [x] Implement executable eligibility/admission decisions with meaningful positive
  and negative tests; no fit when existing admission/calibration checks fail.
- [x] Implement and test explicit mortality/person-time/boundary-transition timing.
- [x] Run affected tests and workstream integration; strict checks, complete suite
  diagnostic/qualified attempts and applicable numerical replay at coherent checkpoint.
- [x] Record source/admission decisions and actual verification, reconcile current
  main, publish with expected-head protection and verify the receiving tree.

Use repository Python 3.15.2 at `.venv-review315/bin/python`. Run expensive commands
serially with the existing 4096 MiB / 2400 second guard. Retain failed commands.
Native and signed hosted acceptance cannot be self-declared from ordinary tests;
the owner-held source/attempt estate and signing setup remain required when the
changed candidate is finally admitted. No package or manuscript release is part
of this continuation.

## Executed first-comparison finding

The bounded review contains 21 source/use records: two blocked likelihood uses,
six context-only uses, six calibration/sensitivity uses, four scope exclusions
and three exclusions from independent validation. All 28 existing handoff rows
remain blocked. The executable audit rejects empirical admission for all three
required roles: baseline observation, wastewater measurement and independent
validation. This is a completed eligibility decision, not a fitted comparison or
completion of the broader Searchright screening programme.

The pinned official NZHS export reconciles all 89 published point estimates,
69 interval pairs and 54 explicit caution flags in the four existing extract
tables. The derived checks reference 73 distinct source cells in 67 original
records, preserve common survey dependence, and add zero independent observations.
Original PHCC/summary HTML capture gaps and native archive admission remain open.

The affected selection passed 224 tests, including workstream integration. Nox
`strict_all` passed: nine Ruff policy tests, lint/format over 190 Python files and
zero strict typing errors, warnings or notes. Full-suite, reproduction and
publication results are recorded below; these focused results do
not qualify the changed native scientific inventory.

## Verification execution — 9 November 2026

The complete diagnostic suite ran on local implementation commit
`a766f8acb5b0b79f9903919fd9002afd9e12288d`, tree
`25858c66bc16c4d2d8f72ab7cc973533b52a1c03`. Later receipt/status edits change
documentation only. All commands used repository Python 3.15.2 and the existing
4096 MiB / 2400 second resource guard; no budget was breached.

| Executed check | Actual outcome |
|---|---|
| Affected audit, NZHS, coverage, handoff, public comparator, dynamic and workstream tests | 224 passed; sampled peak 182.5 MiB |
| Nox `strict_all` | Passed; nine policy tests, 190 Python files linted/formatted, zero typing errors/warnings/notes; peak 921.5 MiB |
| Nox `publication` | Passed; 21 boundary tests, staged/full-history gitleaks and Actionlint; peak 192.1 MiB |
| Nox `tests reproduce` | Both sessions failed before workloads: `Missing TOBAC_LINEAGE_PYTHON for native lineage preflight`; combined exit 1, peak 5.3 MiB |
| Direct full diagnostic pytest | 1,428 passed, 21 skipped, 19 failed, zero collection errors in 57.06 s; exit 1, peak 687.1 MiB |

The normal Nox commands used `--force-python` pointing to the selected
`.venv-review315/bin/python` and `-r`; this selects the installed interpreter,
not an exemption from lineage verification. The diagnostic command was
`python -m pytest -q --strict-markers --basetemp=<new outside-checkout directory> --junitxml=outputs/first-comparison-20261109/full-diagnostic.xml`.
It is not a passing full suite or qualified numerical replay. Skips concern
separate Voiage, native-producer, Snakemake and selected-verifier environments,
the diagnostic environment's absent Ruff import, and normal collection skips.
Ruff actually executed in the successful strict environment.

All 19 failures are in `tests/engineering/test_hosted_lineage.py`. This host's
OpenSSH binary is outside the accepted runtime profiles, so the verifier
correctly reports `OpenSSH verifier differs from qualified binaries`. One
negative test expected a later executable-bytes error but encounters this earlier
OpenSSH guard; it is retained as a failure. The exact failed cases are:

- `test_actual_signed_native_acceptance_and_all_inputs`
- `test_rejection_precedes_hosted_workload[missing]`
- `test_rejection_precedes_hosted_workload[signature]`
- `test_rejection_precedes_hosted_workload[payload]`
- `test_rejection_precedes_hosted_workload[source]`
- `test_rejection_precedes_hosted_workload[inventory]`
- `test_rejection_precedes_hosted_workload[runtime]`
- `test_rejection_precedes_hosted_workload[authority]`
- `test_rejection_precedes_hosted_workload[stage]`
- `test_rejection_precedes_hosted_workload[stage_context]`
- `test_rejection_precedes_hosted_workload[dag]`
- `test_valid_object_substitution_is_not_accepted[artifacts]`
- `test_valid_object_substitution_is_not_accepted[originals]`
- `test_valid_object_substitution_is_not_accepted[executed_input_objects]`
- `test_valid_object_substitution_is_not_accepted[manifest]`
- `test_wrong_runner_manifest_selection`
- `test_failed_native_readback_cannot_qualify`
- `test_alternate_executable_cannot_report_its_own_success`
- `test_runtime_profile_substitution_is_rejected`

Logs are retained in the ignored local `outputs/first-comparison-20261109/`
directory. Their hashes bind this execution record; they are not native
acceptance receipts, and no private accepted input or signing key was copied.

| Log | SHA-256 |
|---|---|
| `focused-tests.log` | `cf93df365886411cbc3f4d61540da1b9af20733e54893fe4e4481727c12accfa` |
| `strict-all.log` | `7548bc742693768756aa53322b1c9b75b7f68b54064e23682789beba10e7e761` |
| `publication.log` | `ecd62c38872a0ba0ca351a51604ecb21f875507328214045ee30ac7352da89c1` |
| `qualified-tests-reproduce.log` | `02ea1e5007dc6c4f774e3192e3712675ddeb23a2e64b85694cd3c9c67b38df6a` |
| `full-diagnostic.log` | `5964743e3a33b8f82fc654df9881fe98c19cd1ce08c2ea4ea05d9e832f25d7a8` |
| `full-diagnostic.xml` | `38d0fc987171c4749dac6ed6c7b2e7538c3173d29822d716fd79b57a4816d88e` |

The first-comparison scientific finding remains negative admission. Completing
the native-qualified suite, coverage, numerical reproduction and hosted checks
requires the existing native source/attempt estate and reviewed signed renewal
for the changed inventory and workflows. No accepted capsule, runtime profile,
test, numerical tolerance or gate was changed.

## Published candidate and receiving verification

[Draft PR #147](https://github.com/edithatogo/tobac/pull/147) now contains
implementation and verification commit
[`c8ecd8c6b9f6f1c98dd07203e63f65bdf5c4b2bf`](https://github.com/edithatogo/tobac/commit/c8ecd8c6b9f6f1c98dd07203e63f65bdf5c4b2bf).
Current main was reread as `d0e832b02b8b9e6791903f987245e8f6332e943a` before
publication and is an ancestor of the received candidate. The expected PR head
`c353d6fb11dbe0bb593f514e5883fbc68d05944e` was checked before the guarded
fast-forward; no force was used.

All 24 changed file blobs matched their local Git hashes. The fetched full tree,
`a3c46d88d681fae83aec8513f83e7904e599162f`, exactly matches the reviewed local
publication tree, including documentation-only verification updates after the
diagnostic suite. Outgoing publication-boundary, full-history/staged secret scans
and Actionlint passed (157.3 MiB sampled peak). The ordinary Git push dry run
lacked HTTPS credentials; the existing GitHub connector published the same
verified tree with an expected-head check. No signing authority was inferred from
that Git publication.

Changed interfaces are `HealthProjection` / `project_health_cohorts`, the explicit
review CSV and audit CLI, and the exact-snapshot NZHS reconciliation CLI with
separate verification annotations. The original ten fact tables, evidence
conditioning interfaces, accepted lineage and numerical references are unchanged.
All new observations remain unadmitted. The first hosted readback started 12
workflows; no aggregate hosted success is claimed while jobs remain in progress.
This receiving record is a subsequent documentation-only update.

At the 09:10 UTC implementation-commit readback, the eight completed failed jobs
across cross-platform, package, reproduction and M3 families all stopped before
workloads with `Stale native acceptance pin: .github/workflows/advisory-types.yml`.
The source-inventory check lies beyond that earlier failure; it was not reached
in those runs. Their valid-signature and tamper-rejection probes passed, and the
package/reproduction/M3 export steps skipped after preflight abort without the
old absent-output exception. Examples: [Linux package](https://github.com/edithatogo/tobac/actions/runs/42591197697/job/129072944963),
[Windows reproduction](https://github.com/edithatogo/tobac/actions/runs/42591197798/job/129072946195)
and [M3 numerical](https://github.com/edithatogo/tobac/actions/runs/42591197693/job/129072944441).
Other jobs were still running or queued; these are observed failures, not an
inference that an unexecuted workload passes.

The subsequent implementation-commit readback found all 12 workflows completed:
four success and eight failure. Publication/source security, Linux audit,
advisory typing and Scorecard passed. These results belong to `c8ecd8c6`; any
later documentation head has its own separately triggered checks.
