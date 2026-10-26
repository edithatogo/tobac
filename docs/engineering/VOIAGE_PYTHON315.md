# Voiage on Python 3.15.1

The published 2.1.0/2.2.0 dependency bounds select SciPy below 1.17, pandas below 3,
xarray before 2025, and PyArrow 25. Those bounds cannot install a consistent native
Python 3.15.1 environment. This repository builds `2.2.0+tobac3151.2` from upstream
commit `7af563c8cb373057d30662650b3f332f39e05b83`, using the reviewed patch in
`engineering/voiage-python315.patch`. The patch changes only package metadata:
the local version, Python requirement and five dependency bounds. Voiage's Python
implementation, Rust/native code and upstream licence are unchanged. It is a
consumer compatibility candidate, not an unmodified upstream release.

The independent `voiage` dependency profile uses the same scientific reference pins
as tobac, including SciPy 1.18.1 and pandas 3.1.0, together with xarray 2026.9.0 and
PyArrow 26.0.0 and Polars 2.0.0. The input-bound `engineering/voiage.lock{,.json}` records exact
transitive versions and hashes. The existing lock helper verifies it before
`uv pip sync --require-hashes`. Maturin 1.15.0 builds the candidate from a clean,
committed derived source tree. Both upstream and derived identities, patch/wheel
hashes and installed distributions are retained in each build receipt. Native
wheel hashes are observations, not a bit-reproducibility claim.

The wheel is installed with normal dependency resolution and no index access into
the hash-installed environment; no Voiage `--no-deps` override is used. `uv pip check`
must pass. The wheel's cp312-abi3 tag denotes its minimum stable native ABI; the
build, import, tests and probes actually execute on asserted Python 3.15.1.

Run from the repository with the existing Nox/uv tools:

```sh
uvx --python 3.15.1 --from nox==2026.10.20 nox -s voiage
```

An optional directory argument places fresh source/native-build outputs on another
volume. Every invocation gets a new directory; compact receipts remain beneath
`outputs/engineering/voiage-receipts-*/`. Both hosted Voiage jobs run this same
session on macOS and retain those receipts. Failures remain failures.

Executed qualification covers 63 actual installed-library/component/integration
tests, 51 equal-weight EVPI cases, weighted/zero-mass/finite-partition cases, 30
randomized weighted and partition comparisons to the independent exact oracle,
Arrow IPC/Parquet round trips and native-extension import. The reference full
suite, numerical reproductions and static checks remain separate. Local dependency
auditing found no known vulnerabilities among published distributions; the two
locally built project distributions have no PyPI advisory identity and were
explicitly reported as unauditable by that service.

These are bounded software compatibility and numerical parity checks. They do
not establish generic EVSI, structural APIs, empirical calibration, causal validity
or a full upstream Voiage test-suite qualification. No public release is made.

All 15 checks on PR #33 passed at `fe56de0`, including both formerly failing
Voiage jobs, the full engineering matrix and numerical/longitudinal checks.
Receiving commit `f06eed630a8832174328a0472bdcaf55c98a4af9` was verified on main.
The full hosted and local receipts are in
`integration/voiage_python315_compatibility_20261026.json`.

## Polars 2 qualification — 27 October 2026

PR #48 also requires a new compatibility artifact: the earlier .1 wheel declares
polars<2 and cannot resolve with Polars 2.0.0. The .2 patch changes that bound to
>=2.0.0,<3 and changes the local version; all upstream implementation/native files
remain byte-identical to the pinned revision. The new build installs with normal
dependency resolution and passes pip check on actual Python 3.15.1.

The current native run executes 99 installed-library, M3, evidence-transport and
workstream tests, plus the equal/weighted/partition probes. Separate JAX float64,
Arrow/Polars buffer ownership/lifetime and strict Patito/msgspec probes pass.
The prior .1 receipt above remains historical; the current artifact identity is
in integration/voiage_polars2_compatibility_20261027.json. No Voiage 3 migration,
scientific calibration or generic structural/EVSI certification is implied.
