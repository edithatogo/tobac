# Bounded lane implementation and verification

- [x] Read main, issue #1, existing workflows, Nox sessions, locks and engineering policy.
- [x] Verify every proposed action and tool ref against real tag reads; record tag+commit.
- [x] Record the drop-in misidentifications (prek != pre-commit; ty, pyrefly and basedpyright
      are separate checkers; helpers:pinGitHubActionDigests is a Renovate preset).
- [ ] Announce the base commit and bounded file scope on issue #1 (not yet posted).
- [ ] Add additive pins to engineering/upstream-pins.json and a lane requirements file.
- [ ] Add a fail-open, self-labelling `automation` Nox session; keep required sessions untouched.
- [ ] Add .github/workflows/ci-cd-lane.yml with harden-runner (egress audit), ruff-action,
      ty/pyrefly diagnostics, zizmor-action, gh-action-pip-audit, prek-action, gitleaks and an
      ubuntu-24.04-arm diagnostic leg. Dispatch-only attestation job.
- [ ] Validate .pre-commit-config.yaml with prek and add the Renovate SHA-pinning preset.
- [ ] Execute what the local host supports; record unexecuted jobs explicitly.
- [ ] Publish with an expected-head check, then verify the receiving commit on issue #1.

strict_all (4,168 ruff, 3,584 basedpyright-all errors at the original measurement; 4,861 and
2,456 at the 26 October 2026 macOS/Python 3.15 re-measurement) remains measured-not-fixed. Attestation
entitlements, harden-runner egress blocking, the arm64 leg and all hosted jobs remain open until
an actual run is recorded.
