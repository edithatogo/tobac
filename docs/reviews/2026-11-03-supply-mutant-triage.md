# Supply mutation triage — 3 November 2026

The [receiving-main macOS qualification run](https://github.com/edithatogo/tobac/actions/runs/40436389773/job/121965933410) for PR #51 reported 119/131 detected and 12 survivors. Its mutation input receipt identifies `src/tobac/supply.py` SHA-256 `45261897fd11636492186c070fc6b0a77caf7dae3d9345ef2dec495ca169acfb` and mutmut 3.8.0. The current source has the same hash, and the retained local 3.8.1 record lists the identical twelve IDs. Patches below were reconstructed with 3.8.1; the hosted 3.8.0 log contains identities and counts, not patch bytes, so identity alone does not prove generated patches were byte-identical across tool versions.

| Survivor IDs (prefix `tobac.supply.x_`) | Triage and evidence |
| --- | --- |
| `expected_releases__mutmut_7`, `_9` | Remove floating conversion across the accounting inputs. Numeric strings accepted by the existing conversion then fail validation/arithmetic. A focused accounting test detects both in the fresh run. |
| `release_loglikelihood__mutmut_3`, `_5` | Remove observed-value floating conversion. Numeric string input exposes the difference; both detected. |
| `release_loglikelihood__mutmut_8`, `_10` | Remove expected-value conversion. Numeric string input exposes the difference; both detected. |
| `release_loglikelihood__mutmut_13`, `_15` | Remove covariance conversion. Numeric string input exposes the difference; both detected. |
| `release_loglikelihood__mutmut_21` | Combines independent wrong-width and empty-hypothesis guards with `and`. Previous shape test also supplied invalid covariance, so that separate guard masked the omission. New tests hold covariance valid and detect the mutant. |
| `release_loglikelihood__mutmut_47` | Removes the explicit `1e-12` symmetry tolerance and accepts differences under NumPy's looser default. A positive-definite near-symmetric covariance with `1e-9` disagreement detects it. |
| `release_loglikelihood__mutmut_67`, `_70` | Replace explicit zero mean with `None` or omit it. Equivalent for this call with installed SciPy 1.18.1: its `Covariance` processing maps `None` to zero and broadcasts to covariance dimension. They remain survivors rather than being excluded or counted as detected. Direct checks also returned identical values for explicit, `None` and omitted means in dimensions 1, 2 and 5. This equivalence is scoped to the qualified backend and current call. |

A fresh bounded macOS mutation session using Python 3.15.1 and mutmut 3.8.1 detected **129/131 (98.5%)**, with only `_67` and `_70` surviving; no incomplete, suspicious or timeout statuses were reported. Its source-bound receipt is `outputs/engineering/mutation-input.json`; the run log is `/tmp/tobac-dh1-final-mutation.log`. The focused supply and workstream integration selection passed 108 tests. This is a local fresh result and does not replace or retroactively alter the hosted PR #51 result.
