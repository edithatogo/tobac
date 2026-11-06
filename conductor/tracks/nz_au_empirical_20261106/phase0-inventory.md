# Phase 0 capability and ownership inventory

Inspected 6 November 2026 at adb3f8127355f210c1df959d629730873b381fc2.

| Scope | Existing implementation | Maturation action / evidence |
|---|---|---|
| Regulatory decision engine | src/tobac/regulation.py, information.py, retail_case.py | Preserve exact finite oracles; 1225-test baseline passed; empirical assumptions remain open |
| Longitudinal | src/tobac_supply; scripts/run_empirical_longitudinal.py and run_release_calibration.py | Existing owner converting verifier; runners still import pandas; await scoped terminal commit, then numerical parity |
| Data contracts | src/tobac/evidence.py, interchange.py, normalized bundle | Reuse source/state identity and dependence guards for later medallion promotion |
| Research methods | src/tobac/research, tests/m3 | M3 retains ownership; qualify library adapters without changing meanings |
| Native provenance | scripts/scientific_lineage.py, lineage_preflight.py and scientific_receipts.py | Reuse immutable source/native receipts; orchestration must not bypass inventory/input guards |
| Context | scripts/context_bundle.py | Existing evidence profile too large; narrow reviewed planning profile now passes |
| Dependency locks | scripts/lock_receipt.py, four existing profiles | Existing updater/integrator owns promotion; local analytics candidate is separate and unpromoted |
| Engineering | noxfile.py, bounded runner, strict quality/security/package checks | Nox remains engineering entry; full baseline test scope executed, reproduction/typing/security still pending |
| Runtime manifests | pyproject.toml, .python-version, engineering profiles, workflows | Baseline Python actual 3.15.1 verified; old pandas declarations retained until owner parity evidence |
| Notebooks/containers | Repository file inventory | No new notebook/container added; complete active-runtime census still to be finished |

No duplicate numerical engine is proposed. New orchestration must wrap existing entry points,
not copy equations. Preserve named contract invariants and validate errors at boundaries.
Baseline full suite: 1225 passed, 20 skipped in 86.76 seconds; skipped capabilities do not
become verified. Resource guard exit 0, sampled peak group RSS 704.7 MiB. No numerical replay,
clean-package, native lineage or empirical calibration is inferred from this suite.

Latest dependency metadata census contains 42 names and zero retrieval failures. Raw candidate
metadata is in outputs/nz-au-phase0/version-census.json; names alone do not identify the user's
libraries. Latest supported versus held-back classification requires actual install/API testing.
Snakemake/Polars/Arrow candidate hash resolution passed without pandas/xarray entries. Exact
candidate: Snakemake 9.27.1, Polars 2.1.0, PyArrow 26.0.1; install/execution result is separate.

Current shared checkout still has dirty docs/WORKSTREAM_SYNC.md and
scripts/verify_empirical_longitudinal.py owned by the Polars lane. No changes copied.
