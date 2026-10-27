"""Versioned, integrity-checked transport of the existing evidence contract.

Requires the optional ``interchange`` dependencies. Digests detect corruption,
not authenticity or scientific validity. Export and reconstruction copy numeric
values; only the Arrow/C-stream/Polars float64 view can share buffers.
"""

from __future__ import annotations

import hashlib
import importlib
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, cast
lazy from pathlib import Path

import msgspec
import numpy as np

from tobac_supply.consumption_ledger import SupplyBasis

from .evidence import EvidencePacket, Scope

pa = importlib.import_module("pyarrow")
pl = importlib.import_module("polars")
pt = importlib.import_module("patito")
_KEY = b"tobac.evidence.v1"


class _Scope(msgspec.Struct, forbid_unknown_fields=True):
    geography: str
    population: str
    start: str
    end: str
    unit: str


class _Basis(msgspec.Struct, forbid_unknown_fields=True):
    unit: str
    geography: str
    products: str
    duty_free_included: bool
    source_ids: tuple[str, ...]
    observation_years: tuple[int, ...]


class _Covariance(msgspec.Struct, forbid_unknown_fields=True):
    observation_ids: tuple[str, ...]
    unit: str
    values: tuple[tuple[float, ...], ...]


class _Envelope(msgspec.Struct, forbid_unknown_fields=True):
    version: int
    evidence_id: str
    data_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    state_ids: tuple[str, ...]
    source_scope: _Scope
    target_scope: _Scope
    likelihood_model: str
    role: str
    transport_note: str
    dependence_note: str
    captured_at: str | None
    digest: str
    supply_basis: _Basis | None
    covariance: _Covariance | None
    producer_revision: str | None


class _Rows(pt.Model):
    state_id: str
    log_likelihood: float
    captured_at: datetime | None = pt.Field(dtype=pl.Datetime("us", "UTC"))


@dataclass(frozen=True)
class PolarsView:
    """A frame plus its mandatory immutable scientific metadata sidecar.

    Polars does not preserve Arrow schema metadata. The sidecar is deliberately
    explicit; restoration validates both values and metadata before use.
    """

    frame: object
    metadata: bytes


def _hash(envelope: object, values: object) -> str:
    wire = cast("Any", envelope)
    numeric = np.array(values, dtype="<f8", copy=True)
    numeric[numeric == 0] = 0.0
    unsigned = msgspec.structs.replace(wire, digest="")
    return hashlib.sha256(msgspec.json.encode(unsigned) + b"\0" + numeric.tobytes()).hexdigest()


def to_arrow(  # noqa: PLR0913  # Explicit supplied provenance is never inferred from packet identifiers.
    packet: EvidencePacket,
    *,
    captured_at: datetime | None = None,
    supply_basis: SupplyBasis | None = None,
    covariance: object | None = None,
    observation_ids: tuple[str, ...] = (),
    covariance_unit: str = "",
    producer_revision: str | None = None,
) -> object:
    """Export an owned Arrow table; missing capture time remains null."""
    if captured_at is not None and (
        captured_at.tzinfo is None or captured_at.utcoffset() != UTC.utcoffset(captured_at)
    ):
        msg = "captured_at must have an explicit UTC offset"
        raise ValueError(msg)
    covariance_wire = None
    if covariance is not None:
        matrix = np.asarray(covariance)
        if matrix.dtype != np.float64:
            msg = "Covariance must be explicit float64, without coercion"
            raise ValueError(msg)
        covariance_wire = {
            "observation_ids": observation_ids,
            "unit": covariance_unit,
            "values": matrix.tolist(),
        }
    elif observation_ids or covariance_unit:
        msg = "Covariance labels require a covariance matrix"
        raise ValueError(msg)
    timestamp = None if captured_at is None else captured_at.isoformat()
    fields = asdict(packet)
    del fields["log_likelihood"]
    envelope = msgspec.convert(
        {
            "version": 1,
            **fields,
            "captured_at": timestamp,
            "digest": "",
            "supply_basis": None if supply_basis is None else asdict(supply_basis),
            "covariance": covariance_wire,
            "producer_revision": producer_revision,
        },
        type=_Envelope,
        strict=True,
    )
    _validate_provenance(envelope)
    envelope = msgspec.structs.replace(envelope, digest=_hash(envelope, packet.log_likelihood))
    values = np.array(packet.log_likelihood, dtype="<f8", copy=True)
    values.setflags(write=False)
    table = pa.table(
        {
            "state_id": pa.array(packet.state_ids, type=pa.large_string()),
            "log_likelihood": pa.array(values, type=pa.float64()),
            "captured_at": pa.array([captured_at] * len(values), type=pa.timestamp("us", "UTC")),
        }
    ).replace_schema_metadata({_KEY: msgspec.json.encode(envelope)})
    from_arrow(table)
    return table


def from_arrow(table: object) -> EvidencePacket:
    """Validate exact schema, order, metadata and digest; never cast or reorder."""
    value = cast("Any", table)
    expected = [pa.large_string(), pa.float64(), pa.timestamp("us", "UTC")]
    if (
        not isinstance(value, pa.Table)
        or value.column_names
        != [
            "state_id",
            "log_likelihood",
            "captured_at",
        ]
        or value.schema.types != expected
    ):
        msg = "Evidence requires the exact version-1 Arrow schema"
        raise ValueError(msg)
    metadata = value.schema.metadata
    if metadata is None or set(metadata) != {_KEY}:
        msg = "Evidence metadata is missing or unrecognized"
        raise ValueError(msg)
    try:
        envelope = msgspec.json.decode(metadata[_KEY], type=_Envelope, strict=True)
    except msgspec.ValidationError as exc:
        msg = "Invalid evidence metadata"
        raise ValueError(msg) from exc
    if msgspec.json.encode(envelope) != metadata[_KEY]:
        msg = "Evidence metadata must use its canonical versioned encoding"
        raise ValueError(msg)
    if envelope.version != 1:
        msg = "Unsupported evidence schema version"
        raise ValueError(msg)
    _validate_provenance(envelope)
    _Rows.validate(pl.from_arrow(value, rechunk=False))
    ids = tuple(value.column(0).to_pylist())
    values = np.array(value.column(1).to_pylist(), dtype=np.float64)
    times = value.column(2).to_pylist()
    timestamp = envelope.captured_at
    expected_time = None if timestamp is None else datetime.fromisoformat(timestamp)
    if expected_time is not None and (
        expected_time.tzinfo is None or expected_time.utcoffset() != UTC.utcoffset(expected_time)
    ):
        msg = "Capture metadata requires UTC"
        raise ValueError(msg)
    if (
        value.column(0).null_count
        or value.column(1).null_count
        or ids != envelope.state_ids
        or any(t != expected_time for t in times)
        or _hash(envelope, values) != envelope.digest
    ):
        msg = "Evidence values, order or metadata changed"
        raise ValueError(msg)
    fields = msgspec.to_builtins(envelope)
    for key in ("version", "digest", "captured_at", "supply_basis", "covariance", "producer_revision"):
        del fields[key]
    for key in ("source_scope", "target_scope"):
        fields[key] = Scope(**fields[key])
    return EvidencePacket(log_likelihood=values, **fields)


def to_polars(table: object) -> PolarsView:
    """Preserve metadata explicitly while exposing a non-rechunked frame."""
    from_arrow(table)
    value = cast("Any", table)
    return PolarsView(pl.from_arrow(value, rechunk=False), value.schema.metadata[_KEY])


def from_polars(view: PolarsView) -> EvidencePacket:
    """Restore only a complete view with unchanged values and metadata."""
    frame = cast("Any", view.frame)
    return from_arrow(frame.to_arrow().replace_schema_metadata({_KEY: view.metadata}))


def write_ipc(path: Path, table: object) -> None:
    """Create an immutable IPC file; never overwrite a retained edition."""
    from_arrow(table)
    value = cast("Any", table)
    with path.open("xb") as destination, pa.ipc.new_file(destination, value.schema) as writer:
        writer.write_table(value)


def read_ipc(path: Path) -> EvidencePacket:
    """Read and validate a retained IPC edition before reconstructing evidence."""
    with path.open("rb") as source, pa.ipc.open_file(source) as reader:
        return from_arrow(reader.read_all())


def _validate_provenance(envelope: _Envelope) -> None:
    if envelope.producer_revision is not None and not envelope.producer_revision.strip():
        msg = "Producer revision must be declared or null"
        raise ValueError(msg)
    if envelope.supply_basis is not None:
        wire = msgspec.to_builtins(envelope.supply_basis)
        wire["source_ids"] = tuple(wire["source_ids"])
        wire["observation_years"] = tuple(wire["observation_years"])
        basis = SupplyBasis(**wire)
        if basis.unit != envelope.source_scope.unit or basis.geography != envelope.source_scope.geography:
            msg = "Supply basis units/geography must match the declared source scope"
            raise ValueError(msg)
        if asdict(basis) != wire:
            msg = "Supply basis must not require normalization"
            raise ValueError(msg)
    covariance = envelope.covariance
    if covariance is not None:
        ids = covariance.observation_ids
        matrix = np.array(covariance.values, dtype=np.float64)
        if (
            not ids
            or any(not name.strip() for name in ids)
            or len(set(ids)) != len(ids)
            or not covariance.unit.strip()
            or matrix.shape != (len(ids), len(ids))
            or not np.isfinite(matrix).all()
            or not np.array_equal(matrix, matrix.T)
        ):
            msg = "Covariance requires aligned unique observations, units and finite symmetric values"
            raise ValueError(msg)
        try:
            np.linalg.cholesky(matrix)
        except np.linalg.LinAlgError as exc:
            msg = "Covariance must be positive definite"
            raise ValueError(msg) from exc


def read_metadata(table: object) -> dict[str, Any]:
    """Return validated declared provenance; it does not establish calibration.

    Supply basis and covariance belong to the supplied likelihood provenance,
    not additional observations or an alternative EvidencePacket contract.
    """
    from_arrow(table)
    value = cast("Any", table)
    return cast(
        "dict[str, Any]",
        msgspec.to_builtins(
            msgspec.json.decode(value.schema.metadata[_KEY], type=_Envelope, strict=True),
        ),
    )
