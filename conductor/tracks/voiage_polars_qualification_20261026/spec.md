# Voiage 3.0.0 Polars consumer qualification

Qualify tobac as a consumer of Voiage when Voiage removes its xarray-backed contract and drops pandas. This track owns the qualification record and the dependency base only. It does not port tobac's longitudinal runners to Polars, and it claims no empirical, calibration or commissioning result.

The owner authorised implementation on 27 October 2026 and explicitly selected
qualification of the exact unreleased Polars candidate from upstream PR #1202,
with published-3.0 acceptance retained as an open external gate. The candidate
is pinned at 6c28ac5787dbe261dfc918eb941c0f8e65c75f4d and declares distribution
version 2.2.0; it is not a published 3.0.0 release. No upstream merge or release
is authorised or performed here.

## Measured surface

tobac's dependence on Voiage is narrow and was checked rather than assumed:

- `src/tobac/integrations.py` calls `ValueArray.from_numpy(values, strategy_names=...)` and `DecisionAnalysis(...).evpi()`, then checks the result against a NumPy reference at `rtol=1e-10, atol=1e-10`.
- `scripts/qualify_integrations.py` exercises the same entry points.
- `tests/engineering/test_voiage_installed.py` imports `voiage._core` and `ValueArray` to prove the native extension loads on 3.15.1.
- There is no `.dataset`, `.to_dataset`, `.from_dataset`, `xarray` or `xr.` reference anywhere in `src/tobac`.

The default qualified producer remains the metadata-only compatibility build
2.2.0+tobac3151.2, from upstream 7af563c8 with wheel SHA-256
dc3230ceaa66292a87d021984c210dba3ef470feef951c660e9f4c2be699eb42.
Its receipt is integration/voiage_polars2_compatibility_20261027.json.
Polars 2.1.0 is qualified as a transport dependency for the candidate's floor;
NumPy/SciPy scientific pins and the current producer selection remain unchanged.

## Acceptance criteria

### AC1: Surface freeze

Acceptance: the inventory above is re-derived by command at the qualification revision, with the command and digest recorded; an assertion confirms no removed Voiage symbol is referenced by `src/tobac`, `scripts/` or `tests/engineering/`.

### AC2: Baseline re-qualification

Acceptance: the current `2.2.0+tobac3151.2` build executes the installed Voiage probe and the EVPI parity check with the recorded tolerances; the receipt states the wheel hash, interpreter, platform and exact command.

### AC3: Candidate qualification

Acceptance: when Voiage 3.0.0 is published, the unpatched upstream wheel is installed and the same probe and parity check run. If 3.0.0 is unpublished, the task is recorded as unexecuted and no success is claimed; a patched build is not presented as upstream qualification.

### AC3c: Exact unreleased macOS candidate (owner-selected scope)

Build the immutable unpatched candidate under Python 3.15.1, enforce locked
dependency and wheel hashes without dependency bypass, prove installed member
bytes match the built wheel, load the real native extension and execute the same
consumer APIs and independent EVPI/finite-partition references at 1e-10. Retain
the default producer and record current pandas/xarray metadata. Add hosted macOS
execution with existing resource, timeout and security controls. This bounded
implementation can merge while AC3 remains explicitly unexecuted.

### AC4: Patch disposition

Acceptance: the track states whether the metadata-only patch is still required at 3.0.0, and if not, retires it explicitly with evidence that the upstream wheel installs and imports on the supported interpreter. The patch is not silently carried forward or silently dropped.

### AC5: Dependency base

Acceptance: whether `pandas` remains in tobac's declared dependency set is recorded from Voiage's actual 3.0.0 metadata, not inferred. Any removal is limited to what no other consumer needs, and the generated lock receipt is regenerated rather than edited. No pin is loosened without a recorded reason.

### AC6: Parity policy

Acceptance: the existing `1e-10` parity tolerances are unchanged. Any widening, any change to the reference calculation and any change to `ValueArray.from_numpy` usage requires separate authorisation and cannot be absorbed into a dependency refresh.

### AC7: Boundary

Acceptance: no empirical, calibration, predictive or commissioning claim is made; no hosted job is recorded as passed unless it ran; no Voiage release, issue state or visibility is changed by this track.

## Distinct from existing planning

Voiage's `tobac_consumer_qualification_20261025` (issue #1193, draft PR #1194) registers weighted and structure-only VOI capability ownership. This track is narrower: it qualifies the container break and the dependency base only. The two must not be merged into one acceptance claim.

## Verification

Freeze exact commands in the first task of each phase. Record source, environment, command, exit status, wheel and artifact digests, and stop on unresolved failure. Run the affected component tests and `tests/test_workstream_integration.py` per `AGENTS.md`. Unexecuted external gates remain open.
