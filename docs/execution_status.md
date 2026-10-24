# Execution qualification — 24 October 2026

The numerical screening ran locally. **31 tests passed**, including two final runner regressions. The full nine-case run passed 974 invariants. Source-preserved core hashes and input/output manifests verified. An offline wheel was built, installed into a separate target directory, and its CLI/hash verification passed against the repository. This uses existing dependencies, not a fresh online dependency installation.

Final review corrected two issues with regression tests first: installed-package runs must hash the executed package and selected configuration; configured scientific-resolution confidence must reach all analysis paths. The reference confidence is 90%, so existing published numerical results are unchanged.

The workflow was actually triggered and retried: [run 40056832485](https://github.com/edithatogo/tobac/actions/runs/40056832485). All three intended jobs failed before job steps, with no runner assigned in the first attempt and no downloadable numerical logs. Available output does not establish the underlying scheduling/account/permission cause. Local success is not substituted for hosted success.

Sourceright and voiage remain unexecuted. The jobs request genuine binaries/packages and have non-silent failure receipts. A successful Sourceright CSL job would validate structure only, not numerical extraction or source applicability; voiage parity qualifies equal-weight EVPI only. The automatic dependency-graph job is not a model test.

The earlier 29-test figure in the milestone report describes its initial verification; the final suite adds the two regression cases. No current NZ data fit, continuous posterior convergence, external policy validation, independent human review or unseen parallel-branch merge is claimed.

Run commands from the repository root with the selected config inside it. Use a new output directory. Resolve hosted execution before marking the external integration track complete; do not weaken assertions to obtain a green badge.
