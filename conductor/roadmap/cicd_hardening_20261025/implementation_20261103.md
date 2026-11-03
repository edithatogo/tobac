# DCI2 implementation — 3 November 2026

Status: **implemented and locally verified on the DCI2 branch; hosted qualification
and publication are DCI3 and DCI4**. The DCI checkpoint was integrated onto main
`afec3a48ce7bae14f9602c48d6c30a8b3f8dab29`, preserving both histories.

- `engineering/advisory.in`, its universal hash lock and source-bound receipt
  isolate ty 0.0.95 and Pyrefly 1.4.0 with canonical runtime, Voiage dependency
  and stub pins. The advisory profile is explicitly opt-in: the pre-existing
  `PROFILES` registry and dependency snapshot retain exactly four profiles.
  The advisory lock SHA-256 is
  `82bb884b347dd2aa085ee2a150d44b08ef46f180b12133a56fdfa73ecb2128d8`.
- The `advisory_types` Nox session checks repository-local Python 3.15.1,
  verifies and hash-installs the isolated lock, fetches Voiage commit
  `7af563c8cb373057d30662650b3f332f39e05b83`, applies the existing reviewed
  Python compatibility patch, builds its wheel with constrained build dependencies,
  installs it without resolving new dependencies, checks the environment, and
  invokes the two checkers serially. It does not run a scientific workload.
- The runner preserves raw SARIF/JSON reports, exact argv and original exit
  codes, stderr bytes, tool and interpreter hashes, dependency inventory/hash,
  source/config hashes, and file/line overlap, unique findings and candidate
  stub gaps. Missing imports, syntax problems, invalid reports, crashes, timeouts
  and contradictory exit codes fail; report-bearing diagnostics remain advisory.
  The final local Nox run passed with original exits `ty=1`, `pyrefly=1` and
  30 and six findings respectively; there were zero same-file-and-line overlaps
  and four possible ty stub gaps. These are findings, not clean type results.
  Local detailed evidence is under `outputs/advisory/6bea3e426cc248f7a076148be1eef663/`;
  its seven JSON files passed the existing publication boundary and secret scan.
- The read-only pull-request/manual workflow selects macOS, Ubuntu x64 and Ubuntu
  ARM64, uses full-SHA actions, no retries or blanket failure suppression, a 4 GiB
  sampled RSS and 40-minute command ceiling, and only inspected diagnostic export.
  The ARM64 scanner archives were downloaded and their SHA-256 values matched
  the pinned publisher digests. Native ARM execution and allocation are not yet
  evidenced; the workflow fails closed on scanner or export failure.
- All eight accepted native attempts were reopened before issuing the updated
  signed orchestration capsule. Its native readback and runner records exactly
  equal the previous generation; only `noxfile.py` and the new advisory workflow
  pins changed. The prior payload and signature were byte-verified in
  `integration/archive/hosted-generation_dci2_20261103.zip`. The new signed
  verifier passes for all eight runners; no frozen verifier profile, scientific
  input, accepted runner or original object was changed.
- Local bounded checks: the full suite passed 1,238 tests, seven capability skips
  and 92% branch coverage; `strict_all` passed lint, format, Ruff fixtures and
  whole-source BasedPyright with zero diagnostics. The focused lock, inventory,
  harness, checker-failure and workstream selection passed 116 tests. The first
  full-suite attempt found an unintended fifth dependency snapshot; the opt-in
  profile change fixed it and the complete suite was rerun successfully.

DCI3 must still execute the chosen workflow on each host, check native ARM scanner
execution, qualify negative fixtures and inspected exports there, and record any
capability limits. DCI4 must publish the qualified lane with an expected-head
non-force fast-forward and verify the receiving ref. No hosted result is inferred
from this local implementation.
