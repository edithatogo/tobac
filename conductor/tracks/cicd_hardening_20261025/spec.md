# Bleeding-edge CI/CD, automation, quality and security lane

Add an advisory tooling lane beside the frozen reference qualification lane. Ancillary tools
(ruff-action, ty, pyrefly, j178/prek, gitleaks, zizmor-action, gh-action-pip-audit,
attest-build-provenance, harden-runner) run as non-required jobs that report counts and
artifacts. The reference NumPy/SciPy pins, engineering/*.lock and its receipts, strict_all
and every existing required Nox session are unchanged. Nothing in this lane may promote
itself, merge, upload a package or mutate a lock.

Report only what executed. A configured action, a resolved tag or a green lane is not hosted
execution, signed provenance, arm64 scientific qualification or independent review. No account,
billing, visibility, branch-ruleset, entitlement or security-setting changes.
