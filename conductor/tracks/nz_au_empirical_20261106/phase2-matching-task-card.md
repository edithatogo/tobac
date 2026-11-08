# P2.9 reproducible candidate-source matching

R03/R04/R16/R18. Owner chat 01a1b3ac-76ef-7b12-a919-91fcb05de339;
worktree /Users/doughnut/.codex/worktrees/tobac-p1-evidence/tobac;
branch codex/p2-empirical-slice-20261107; clean base d72af89.
The prior turn made source-to-formula progress. This task implements the next
bounded audit; it does not redefine the full P2 fit/contrast/holdout requirements.

Own scripts/reconcile_empirical_candidates.py, tests/engineering/test_empirical_matching.py,
this card, exact publication classifications, focused context and P2 metadata/handoff.
Reuse audit_empirical_coverage.nzhs_candidates, source_handoff checked/read/same_hash,
and the existing Scope type. Input JSON is CLI file/hash configuration only, not a
new observation/admission authority. Never construct EvidencePacket, SupplyBasis,
likelihoods or fitted states from unadmitted raw-unit candidates. No M3, locks,
scientific/reference code, source register, archive/native or shared-main writes.

One result: a deterministic Polars source-compatibility report from pinned NZHS,
native historical SAP0240 prices, native DPE054AA population, original HS10 import/
export CSVs and the existing registered release CSV. Bind the declared survey Scope
to the verified methods PDF bytes; report the distinction between declaration and
semantic/source admission. Preserve labels, unavailable values, flags and units.
Report overlapping price quarters, nominal ERP benchmark quarters and non-overlapping
trade months without interpolation, period allocation, consumption conversion or
an automatic numerical join. Retain source-dependence and admission barriers.

Tests: meaningful negative cases for malformed/duplicate periods, source drift,
unknown flags and missing benchmark occasions, plus positive overlap/missingness
cases and existing workstream integration. Synthetic fixture values are not raw
publisher data. Actual originals and CLI input configuration stay external; audit
logs/reports are ignored outputs/nz-au-phase2-matching-20261107.
Use actual .venv Python3.15.2 and scripts/run_bounded.py, 4096MiB/2400s, streamed logs,
serial heavyweight commands and zero retries. Run exact affected tests first, full
Nox at the coherent source milestone, and reuse unchanged numerical reference receipts.
Fail before output on malformed input; exclusive output creation preserves old reports.
Unknown scope/admission blocks downstream use rather than being filled by assumptions.

## Executed verification

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python scripts/reconcile_empirical_candidates.py --inputs /Users/doughnut/Documents/tobac-evidence-intake-20261107-p2-matching/inputs.json --out outputs/nz-au-phase2-matching-20261107/actual-v3.json
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/engineering/test_empirical_matching.py tests/engineering/test_empirical_coverage.py tests/engineering/test_source_handoff.py tests/test_workstream_integration.py
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv-quality/bin/basedpyright --pythonpath .venv-quality/bin/python --project engineering/basedpyright-all.json
```

Full Nox tests used the previously qualified attested route and an explicit fresh
outside-repo basetemp on the user-owned PortableSSD:
`env TOBAC_LINEAGE_ROUTE=attested TOBAC_LINEAGE_PYTHON="$PWD/.venv/bin/python"`
followed by the same bounded guard and
`uvx --python .venv/bin/python --from nox==2026.10.20 nox -r -s tests -- --basetemp=/Volumes/PortableSSD/tobac-p2-match-test.f303vb5z/full`.
The fixture-only scratch is removed after terminal completion; select a fresh writable
outside-repo directory for a later run, not this historical path.

First full attempt failed: 1,264 passed, 22 skipped, 9 failed, 26 fixture errors;
shared-volume ENOSPC and wrong in-repo scratch semantics retained in log and JUnit.
The alternative local volume passed exclusive write/fsync/symlink readback. A scoped
`--lf --last-failed-no-failures=none` run in the same Nox interpreter passed all
35 affected cases before the corrected full run. Final: 1,299 passed, 22 capability
skips, 92% source-only coverage, 755.7 MiB sampled group RSS, status 0. Focused 87
passed; strict whole-source typing 0 errors/0 warnings, Ruff passes. No scientific
model/input/config/lock/workflow diff from the existing P2.2 numerical receipt;
reuse it without claiming another numerical replay. Exact artifacts and hashes are in
phase2-context-receipts-20261107.json. No shared/native/cache deletion or owner write.
