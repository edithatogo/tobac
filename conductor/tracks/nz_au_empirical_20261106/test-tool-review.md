# Test-tool review — 6 November 2026

Current required Nox tests already use coverage.py 7.17.0 with branch coverage and a 90%
source threshold. Keep that working gate. Targeted selectors and pytest cache remain enabled;
partial tests/coverage never count as full integration or scientific acceptance.

| Tool | Disposition | Evidence / rationale |
|---|---|---|
| pytest-xdist 3.8.0 | Optional candidate, not default | Isolated Python 3.15.1 two-worker trial passed 30 pure information/regulation tests; 6.17 s / 293.8 MiB versus serial 1.57 s / 106.7 MiB. No speed benefit on this selection. Reassess only a demonstrably expensive independent test group; never -n auto or parallel native mutations. |
| pytest-cov 7.1.0 | Compatible optional companion to xdist | Same trial produced matching serial/distributed executed/missing lines and branches for the selected module. Existing coverage.py gate is sufficient; no duplicate production reporter added. |
| pytest-newer | Unresolved identity | Exact PyPI JSON endpoint returned HTTP 404. Do not install a similarly named substitute; exact source needed for reconsideration. |
| pytest-changed 0.1.1 | Defer default/hook adoption | Maintainer description says filename conventions, not impact analysis; no-match can exit 0. Existing explicit selectors/workstream tests are safer until mapping coverage and non-Python input changes have real qualification. |
| unittest.mock | Use at I/O/API failure boundaries | Standard library, no dependency. Added autospecced PermissionError test proving failed context reads remove stale success and log failure. Scientific arithmetic and native receipts remain real. |
| pytest-mock 3.17.0 | Defer until fixture need | Wrapper around unittest.mock; current monkeypatch and patch already meet needs. No rewrite or dependency solely for stylistic convenience. |

Trial environment .venv-test-tools was separately hash-synced from the existing baseline,
then received pinned xdist/cov for this experiment. It is not a fully locked promoted test
environment. No global pytest addopts, hook installation, retry policy or CI parallelism changed.
Reported timings are one bounded comparison, not a statistically established performance claim.

Adoption gates: source identity, Python/pytest compatibility, reviewed hash lock, deterministic
collection, no shared writes, fixed worker budget, same selected test IDs and comparable
coverage, measured resource/time benefit. Native/scientific mutation and provenance gates
remain serial. Selection must always include relevant contracts/workstream tests and fall
back to full milestone checks for uncertain dependencies, configs/data/schema/environment
changes or unknown mappings. Preserve failure-only cache semantics and zero blind retries.

Primary references:
- https://pytest-xdist.readthedocs.io/en/stable/known-limitations.html
- https://pytest-cov.readthedocs.io/en/latest/readme.html
- https://pypi.org/project/pytest-changed/
- https://pytest-mock.readthedocs.io/en/latest/usage.html
