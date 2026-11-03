# Advisory CI/CD, automation, quality and security lane

Current selection is recorded below and in [the DCI1 decision](selection_20261103.md).

## Historical original proposal — superseded by DCI1

Add an advisory tooling lane beside the frozen reference qualification lane. Ancillary tools
(ruff-action, ty, pyrefly, j178/prek, gitleaks, zizmor-action, gh-action-pip-audit,
attest-build-provenance, harden-runner) run as non-required jobs that report counts and
artifacts. The reference NumPy/SciPy pins, engineering/*.lock and its receipts, strict_all
and every existing required Nox session are unchanged. Nothing in this lane may promote
itself, merge, upload a package or mutate a lock.

Report only what executed. A configured action, a resolved tag or a green lane is not hosted
execution, signed provenance, arm64 scientific qualification or independent review. No account,
billing, visibility, branch-ruleset, entitlement or security-setting changes.


## Selected scope — DCI1, 3 November 2026

The original ancillary-tool list above is a superseded proposal, not an instruction
to add every wrapper. [DCI1 selection](selection_20261103.md) chooses a bounded
ty 0.0.95/Pyrefly 1.4.0 differential diagnostic experiment and a Linux ARM64 static
diagnostic leg beside current macOS/Linux x64 evidence. Existing Ruff, workflow/
dependency/security scans, hooks, attestations, hardening and required checks stay
in their current lanes. No new action wrapper or hook migration is selected.

A separately reviewed, source-bound advisory lock may be added during DCI2;
advisory execution cannot modify/promote it or the four existing locks. Pinned
interpreter/tool behavior, dependency/stub resolution, report/exit controls and
ARM delivery/export must be qualified in DCI3. Publishing this selection does not
publish an implemented lane or complete DCI4. No scientific source/model/input,
reference pin, frozen verifier profile or native authority change is selected.
