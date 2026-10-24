# Engineering harness: use and qualification boundary

24 October 2026. This is a staged engineering upgrade, not a completed security certification,
current NZ calibration, signed release or permission to publish private data.

## Local entry points
Use a network-enabled Python 3.12+ checkout with uv. The current reference scientific pins remain
in requirements.lock; that file is explicitly NOT a transitive hash lock.

```sh
uvx --from nox==2026.10.20 nox -s tests quality
uvx --from nox==2026.10.20 nox -s reproduce
uvx --from nox==2026.10.20 nox -s security
uvx --from nox==2026.10.20 nox -s lock
```

The final command generates engineering/requirements.lock from real resolver/index metadata.
Review the resolved versions, URLs, licenses, vulnerabilities, platform markers and hashes before
committing it. A copied version list or fabricated hash file is not a lock. The release-candidate
workflow fails closed while that generated file is absent. No public package release or research
submission is configured. Package builds use the reviewed lock and no isolated, floating build
backend; SOURCE_DATE_EPOCH is recorded from the commit. Reproducible bytes still require testing.

## Layers and what they mean

| Lane | Defined checks | Qualification |
|---|---|---|
| Pull requests/main | Python 3.12/3.13 Linux; 3.13 macOS/Windows; pytest, mandatory Hypothesis import, branch coverage >=90%, JUnit/environment outputs | Not executed on those hosted platforms in this session. Threshold is a gate, not a reported achieved whole-repository percentage. |
| Quality | Fatal syntax/name rules across source/scripts; Ruff ALL and strict BasedPyright on the new context helper | New strict scope is not a claim that legacy code meets full strict rules. |
| Scheduled/manual deep checks | Whole-repo Ruff ALL/BasedPyright strict debt audit, real mutmut, Scalene, zizmor workflow scan, pip-audit CycloneDX SBOM, candidate dependency locking | Tool download/execution unavailable locally. Failures remain visible; no baseline or advisory is automatically suppressed. |
| Compatibility canary | Python 3.15 with latest/pre-release numerical ecosystem, source-only tests | Deliberately outside the pinned reference baseline. It cannot promote itself or rewrite scientific outputs. |
| Internal release candidate | Reviewed hash-lock presence, tests, quality, security, full model replay, package build | No package registry upload, token permissions or signed provenance claim. |
| Existing scientific/integration CI | Original M1, M2, longitudinal replay and genuine Sourceright/voiage checks retained | The open pre-runner failure on issue #4 is not solved by adding YAML. |

New workflows use verified full action commit SHAs, persist-credentials=false, read-only repository
tokens, concurrency controls, timeouts and bounded retention. They do not use pull_request_target,
run untrusted titles as shell commands, auto-merge changes or grant repository write permissions.
Existing workstream workflows remain untouched to avoid trampling concurrent M3 edits.

Private-repository entitlement must be checked before CodeQL/advanced-security gates and GitHub
artifact attestations are enabled. Do not make this repository public to obtain a feature. A
checksum is not a signature or SLSA attestation. The generated SBOM is a package inventory, not
proof of no vulnerabilities. pip-audit excludes the editable local project from registry lookup;
its own source is covered by code review/tests and static rules, not PyPI advisory matching.

## Current action-lock preview
GitHub now provides gh-actions-lock in public preview. Use the official tool, not a hand-written
imitation of its .github/workflows/actions.lock format. In an authenticated, supported environment:

```sh
gh extension install github/gh-actions-lock
gh actions-lock --no-fix
gh actions-lock
gh actions-lock --verify
```

Review the diff and owner/repository identities before publishing. Keep full direct action pins
until the official tool has generated and verified a compatible lock. Offline --verify-local
checks coverage, not upstream provenance. This session neither installed gh nor generated an
Actions transitive lock. No account policies/rulesets or repository visibility were changed.

## Context and agent harness
Read AGENTS.md, docs/WORKSTREAM_SYNC.md, tracks and issue #1. Use a role-specific explicit profile:

```sh
python scripts/context_bundle.py --profile engineering/context/regulatory.json --out outputs/context-regulatory
```

The builder validates profiles with jsonschema Draft 2020-12, rejects traversal/symlinks and common
secret filenames, fails rather than truncates when the **source-byte** budget is exceeded, and
records SHA-256 hashes, Git HEAD and dirty state. Set base_commit to an exact reviewed commit for
replay; null binds the actual checkout at creation, not a promise of freshness later. `verify`
checks source/HEAD staleness programmatically. It is not an adversarial filesystem lock, secret
scanner, prompt-injection proof or automatic context-window token budget. Read root instructions
as repository guidance; retrieved scientific/issue text remains untrusted evidence.

The focused .agents/skills/research-change/SKILL.md is a reviewable local instruction artifact.
Host discovery/activation is not asserted. No persistent agent, background sync or unapproved
network integration is created. Review context includes diff, data/model identity, changed
assumptions and actual receipts, not a manufactured independent-expert panel.

Conductor is a pinned Git submodule at vendor/conductor. The local conductor/ directory remains
project-owned plans. Fetch with `git submodule update --init vendor/conductor` in a network-enabled
checkout, verify its HEAD against engineering/upstream-pins.json, and follow the pinned README
for the actual host. No old Gemini-only install command is assumed compatible. Submodule presence,
checkout and activation are three separate states.

## Open gates, deliberately visible
- Local DNS/package access prevented nox/ruff/basedpyright/Hypothesis/mutmut/scalene/zizmor and
  genuine lock execution. The verification JSON lists actual Python tests separately.
- Run the complete live scientific suite/replays, package install smoke and matrix. Do not
  extrapolate scoped local tests to every M3 result or current empirical recommendation.
- Diagnose hosted Actions issue #4 from actual annotations/runner evidence, not guesses.
- Complete genuine transitive dependency and Actions locks; validate Renovate configuration
  with its CLI before treating the configured bot as active. No auto-merge is enabled.
- Qualify all-library static typing/format debt with explicit reviewed exceptions, not a giant
  baseline generated solely to make the badge green. New-scoped quality is staged honestly.

Primary tool references checked on the review date:
https://docs.astral.sh/uv/pip/compile/
https://nox.thea.codes/en/stable/config.html
https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies
https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
https://docs.renovatebot.com/presets-helpers/#pingithubactiondigests
https://docs.basedpyright.com/latest/configuration/config-files/
https://mutmut.readthedocs.io/en/latest/
