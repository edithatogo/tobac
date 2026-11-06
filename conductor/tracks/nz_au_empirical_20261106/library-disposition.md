# Phase 0 library disposition — 6 November 2026

| Component | Exact candidate / observation | Actual evidence | Remaining gate |
|---|---|---|---|
| Python | 3.15.1 repo-local baseline and candidates | Actual interpreter assertions | Newer patch census/qualification through runtime owner |
| Snakemake | 9.27.1 | Hash-install, CLI, real DAG, cache rejection/recovery | Default ILP solver incompatible with Apple Silicon; supported greedy qualified; interrupted-process recovery pending |
| Polars / Arrow | 2.1.0 / 26.0.1 | Hash-install/import, no pandas/xarray in analytics candidate | Reference promotion and numerical output parity |
| Voiage | 3.1.0 cp315 abi3 macOS arm64 | Wheel SHA256 ca1a625ea2e0f6c63ffd306f19cb62c1c69242643164553d5ca633e94146eb5b, hash install, pip check | Existing native/weighted/buffer consumer probe running; no success claimed until terminal receipt |
| Innovate | 0.6.0 published metadata and current main | Source/project URLs match user's repository; published metadata also requires pandas/pandasdmx | Polars-only runtime conflict; no dependency omission bypass; upstream migration or explicitly qualified boundary required |
| Searchright | main af8c282f4c0e92a958027ca352e82f1cc7180c57 | Exact GitHub commit read; executable absent from initial PATH | Actual CLI/build/provider qualification; no systematic search executed |

All original PyPI metadata, candidate wheel/locks and logs stay in local outputs/nz-au-phase0.
These are execution evidence, not public source datasets. Candidate locks are unpromoted;
existing four-profile lock_receipt.py coverage must be extended/reconciled by the integrator.

Full M1 calculation executed at current source, not --quick. Existing verify.py reported
nine core definitions verified and run_verified true. Native-byte numerical reference
comparison initially failed at import because PYTHONPATH omitted src; no numerical mismatch
or comparison success is inferred from this environment error. Correct exact command before
rerunning. Full eight-runner reproduction remains distinct from the M1 result.
