# DCI3 local qualification checkpoint — 3 November 2026

Status: **partial; hosted and end-to-end qualification remain open**. This is a
local dirty-checkout observation, not acceptance of a commit or hosted run.

- Repository-local CPython 3.15.1, ty 0.0.95 and Pyrefly 1.4.0 were executed.
  `engineering/advisory.lock` was regenerated including canonical Voiage
  dependencies, verified against its inputs and installed with hashes.
- The existing bounded `nox -s voiage` session fetched source revision
  `7af563c8cb373057d30662650b3f332f39e05b83`, applied the existing Python 3.15
  compatibility patch, built a wheel and completed its checks: 99 tests passed,
  interchange and numerical qualification passed, with 1123.4 MiB peak sampled
  group RSS. The wheel SHA-256 was
  `93f617c7f7f941c6c8392358ddb755c309ab4b68f850c32485f82823b81f9564`.
  Build evidence: `outputs/engineering/voiage-receipts-06ef395d680442578bed8144a56f2d2b/`.
- Installing that wheel without dependency changes into the advisory environment
  passed `uv pip check`. The bounded prototype run wrote structured reports and
  a source/environment receipt to `outputs/advisory/`; ty returned 30 diagnostic
  entries, Pyrefly 6, and both original exit codes were 1. Neither reported a
  missing import on this run. The wrapper returned 0 for these advisory findings;
  its sampled peak was 209.5 MiB. This is not a clean type-check result.
- Small direct-checker fixtures established good and Python 3.15 lazy-import
  cases exit 0, while deliberate type error, missing import and invalid syntax
  each exit 1 with structured diagnostics for both tools. Ty's observed syntax
  code is `invalid-syntax`; the prototype now treats it as fatal, alongside the
  observed missing-import and Pyrefly parse codes. The focused regression and
  lock/workstream tests passed (70); affected Ruff and format checks passed.
  Raw fixture evidence is retained under `outputs/dci3-fixtures/`.
- The local prototype does not yet qualify report overlap/unique/stub-gap
  classification, crash/malformed-report handling and all negative cases as an
  integrated Nox lane. Its Voiage wheel must be built and verified as part of
  the repeatable lane, rather than relying on this local environment.
- GitHub workflow inventory contained no advisory workflow on this checkout's
  receiving repository. No hosted macOS, Linux x64 or Linux ARM diagnostic job
  was dispatched or qualified; ARM scanner archive execution is also unverified.
  DCI2 still requires its Nox/workflow implementation and native lineage capsule
  renewal before DCI3 hosted acceptance; DCI4 publication remains pending.
