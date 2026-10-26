# Evidence interchange v1

Install `tobac-regulatory-research[interchange]` to use
`tobac.interchange`. The numerical runtime remains NumPy/SciPy; this optional
boundary transports the existing `EvidencePacket`, `Scope` and `SupplyBasis`.
It does not replace them, fit a likelihood or create an observation.

```python
from pathlib import Path
from tobac.interchange import to_arrow, to_polars, from_polars, write_ipc, read_ipc

# packet is an already validated EvidencePacket from an identified producer.
table = to_arrow(packet)  # capture time is unknown: null, never the current time
view = to_polars(table)   # preserves mandatory schema metadata explicitly
restored = from_polars(view)
write_ipc(Path("evidence-v1.arrow"), table)  # exclusive creation, no overwrite
retained = read_ipc(Path("evidence-v1.arrow"))
```

Arrow fields, in order, are `state_id: large_string`,
`log_likelihood: float64`, and `captured_at: timestamp[us, UTC]`.
State IDs and likelihoods cannot be null. Capture time is either null throughout
or the same explicitly supplied UTC time throughout. No casts, state sorting,
null filling, precision changes or timezone inference are performed. Likelihoods
may include negative infinity, preserving impossible states; NaN and positive
infinity are rejected by the existing evidence constructor.

The sole Arrow schema metadata key is `tobac.evidence.v1`. Its canonical msgspec
encoding binds the existing packet fields, both scopes, exact state order, role,
model, transport/dependence notes, capture time and optional supplied provenance:

- `supply_basis`: all existing product coverage, duty-free, observation-year,
  source-ID, geography and unit declarations. Unit/geography must match source
  scope. Reconstructing it must not silently normalize IDs.
- `covariance`: explicit observation IDs, declared covariance unit and a finite,
  symmetric, positive-definite float64 matrix. The boundary preserves a supplied
  covariance; it neither estimates it nor proves that it generated the likelihood.
- `producer_revision`: explicitly supplied source/extraction revision or null.

Nested wire structures reject unknown fields. Missing or changed metadata,
unknown versions and duplicate/noncanonical encodings fail closed. Polars drops
Arrow schema metadata, so `PolarsView` carries an immutable byte sidecar; passing
a bare Polars-exported Arrow table is rejected. Deliberately changing a scientific
packet requires explicit construction of a new packet, rather than editing the
view and restoring it under an old identity. Normal data-once and target-scope
checks still run when `condition` consumes the reconstructed packet.

The logical SHA-256 v1 covers canonical metadata with an empty digest, a null
separator and ordered little-endian float64 likelihood bytes, canonicalizing
signed zero. It is independent of Arrow chunk boundaries. IPC file SHA-256 covers
physical file bytes and can differ for logically identical chunked content.
These checks detect corruption, not authenticity, source validity or permission.

Export owns a copied likelihood buffer; reconstruction also copies. The measured
zero-copy claim covers only the float64 Arrow/C-stream/Polars view, checked by
buffer address, length/offset and survival after releasing source objects.
Strings and other allocators may allocate. Arrow memory-pool counters do not
measure all Python, NumPy, Polars or process memory. Run
`scripts/qualify_interchange.py --out <new-directory>` in the qualified native
producer environment for a fresh measurement and an installed Voiage EVPI check.
The `ecosystem` Nox session executes this and the consumer/M3 tests using the
hash-bound current Voiage wheel. Voiage 3.0 qualification remains a separate track.

There is no earlier persisted domain format to migrate. A future version needs
an explicit converter and compatibility tests; v1 readers reject it. Exclusive
IPC creation and retained-v1 readback provide rollback without replacing an
existing edition. Interrupted or invalid files must pass full validation before
use. The clean-package gate exercises the API and IPC round-trip from the built
wheel outside this checkout, with source overrides disabled.

All qualification fixtures are synthetic. No national posterior, source
calibration, forecast, covariance estimate or published numerical output changes.
