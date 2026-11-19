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

The new `properties` Nox session in `nox_properties.py` imports the existing
environment helper and uses its source-bound runtime lock and exact Python 3.15.2.
The signed main `noxfile.py` remains byte-for-byte unchanged. This is a scalar
synthetic test session, not native-producer
lineage qualification. The scoped workflow runs 100 examples per property on PRs
and 1,000 weekly/manual, through the existing macOS process-group monitor at
4 GiB RSS and a ten-minute wall limit. Public artifacts pass the existing export
scanner; no raw source inputs or synthetic example database are exported directly.
The run seed and Hypothesis minimal examples remain in the job log.

## Executed evidence and remaining gates

`TOBAC_PROPERTY_EXAMPLES=1000 .venv/bin/python -m nox -f nox_properties.py -s properties -- --hypothesis-seed=20261121`
selects the four properties using the verified existing runtime lock on Python
3.15.2. Its final execution result is recorded below. The new test and Nox entry
point pass pinned Ruff check and formatting.

The required full `nox -s tests` was attempted. Its evidence inventory passed,
then native lineage preflight failed because `TOBAC_LINEAGE_PYTHON` was absent.
The full suite, workstream integration, coverage and numerical reproduction were
therefore not executed through their qualified route. No substitute lineage,
private binding, skipped preflight or gate waiver was introduced. Existing native
owner and empirical acceptance work remains open. The PR records the candidate
commit, receiving-ref verification and actual hosted results.

The first hosted candidate `0c972b99c3cb498c2165e48002de00b42b2b1976` passed its
new property job but exposed two introduced integration defects: the initial
session addition changed signed `noxfile.py` bytes, and the pedantic workflow audit
required a job display name. The next candidate restores the original Nox file,
uses the separate Nox entry point above and names the job. No native acceptance
pin, signature or verifier is changed; final hosted status remains in the PR.

The final separate-entry-point command above passed all four properties in
5.20 seconds (Nox session 27 seconds, including its clean locked installation).
All 43 file hashes in the committed native acceptance capsule match their original
pins. Pinned zizmor 1.32.0, offline/pedantic, reports no workflow findings. These
checks do not substitute for hosted native signature/interpreter qualification.
