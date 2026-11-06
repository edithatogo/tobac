# Phase 0 capability and ownership inventory

Initial inspection: 6 November 2026 at adb3f8127355f210c1df959d629730873b381fc2.
The initial table is retained as baseline history; the integrated disposition follows below.

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

## Integrated disposition at de1c887

The owner's committed runner/verifier conversion, exact CSV corrections and profile
retirement are integrated. Maintained src/scripts/tests no longer import pandas/xarray.
This lane's actual default Python 3.15.1 environment is hash-synchronised, has 36 compatible
packages and cannot import either library. All six lock receipts verify. Optional analytics
is a separately closed input profile; Nox remains the engineering runner.

The bounded runtime inventory records 15 tracked CI workflows, 19 dependency/runtime
declarations and no tracked notebook or container definition. The raw inventory's former
local-environment list is historical: the four redundant inactive package/quality/test-tool/
Voiage environments were removed after qualification, preserving their receipts. Active
baseline, analytics, latest-baseline, latest-audit and forward-ecosystem environments remain.
The dated dependency census was expanded from the initial 42 to 146 identities, with zero
lookup failures; available and qualified versions remain distinct.

Existing finite calculations, evidence/state IDs and covariance/dependence guards were
retained. New workflow code wraps existing calculations; it introduces no parallel numerical
engine. Targeted and whole-source type evidence is in phase0-progress.md. Remaining defects
are the stale signed runtime/inventory acceptance, optional Innovate's pandas dependency
conflict and Apple's incompatible default Snakemake ILP solver (qualified greedy route
used). None is silently converted into successful empirical or native acceptance.
