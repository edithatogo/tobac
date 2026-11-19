# Bounded synthetic accounting properties

Baseline: `891f79e07292b7754f78d7193130623bd5f9e243`. This isolated assurance leaf
adds four properties for the existing rectangular `accounting_bounds` contract.
No scientific input, production function, shared evidence contract or M3-owned
interface is changed. These supports are synthetic mathematical inputs, not
measurements, fitted posteriors or confidence intervals.

The independent oracle enumerates all 64 corners using exact rational arithmetic
and compares the attainable extrema with the floating-point interval output.
Additional properties check signed stock translations, containment under widening
stock uncertainty, and rejection of a calibration support that touches zero.
The oracle names every component explicitly; generated dictionary insertion order
exposed and corrected an initial test-oracle defect before publication.

The new `properties` Nox session uses the existing source-bound runtime lock and
exact Python 3.15.2. It is a scalar synthetic test session, not native-producer
lineage qualification. The scoped workflow runs 100 examples per property on PRs
and 1,000 weekly/manual, through the existing macOS process-group monitor at
4 GiB RSS and a ten-minute wall limit. Public artifacts pass the existing export
scanner; no raw source inputs or synthetic example database are exported directly.
The run seed and Hypothesis minimal examples remain in the job log.

## Executed evidence and remaining gates

`TOBAC_PROPERTY_EXAMPLES=1000 .venv/bin/nox -s properties -- --hypothesis-seed=20261121`
passed all four properties in 6.74 seconds (Nox session 12 seconds), with the
verified existing runtime lock on Python 3.15.2. The new test and Nox changes pass
Ruff check and formatting.

The required full `nox -s tests` was attempted. Its evidence inventory passed,
then native lineage preflight failed because `TOBAC_LINEAGE_PYTHON` was absent.
The full suite, workstream integration, coverage and numerical reproduction were
therefore not executed through their qualified route. No substitute lineage,
private binding, skipped preflight or gate waiver was introduced. Existing native
owner and empirical acceptance work remains open. The PR records the candidate
commit, receiving-ref verification and actual hosted results.
