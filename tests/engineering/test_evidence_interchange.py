"""Exercise evidence transport without changing the conditioning contract."""

import gc
import hashlib
from dataclasses import replace
from datetime import UTC, datetime

import numpy as np
import pyarrow as pa
import pytest

from tobac.evidence import EvidencePacket, Scope
from tobac.interchange import (
    from_arrow,
    from_polars,
    read_ipc,
    to_arrow,
    to_polars,
    write_ipc,
)


@pytest.fixture
def packet():
    scope = Scope("NZ", "adults", "2024-01-01", "2024-12-31", "counts")
    return EvidencePacket(
        "observed",
        ("data:1",),
        ("source:1",),
        ("a", "b"),
        np.array([0.0, -np.inf]),
        scope,
        scope,
        "joint Gaussian",
    )


@pytest.mark.parametrize("timestamp", [None, datetime(2026, 10, 26, tzinfo=UTC)])
def test_roundtrip(packet, timestamp) -> None:
    table = to_arrow(packet, captured_at=timestamp)
    recovered = from_arrow(table)
    assert recovered.state_ids == packet.state_ids
    assert recovered.source_scope == packet.source_scope
    assert recovered.data_ids == packet.data_ids
    np.testing.assert_array_equal(recovered.log_likelihood, packet.log_likelihood)
    view = to_polars(table)
    np.testing.assert_array_equal(from_polars(view).log_likelihood, packet.log_likelihood)


def test_polars_changes_rejected(packet) -> None:
    view = to_polars(to_arrow(packet))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Evidence\ values,\ order\ or\ metadata\ changed)"),
    ):
        from_polars(replace(view, frame=view.frame.reverse()))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Evidence\ metadata\ is\ missing\ or\ unrecognized)"),
    ):
        from_arrow(view.frame.to_arrow())


@pytest.mark.parametrize("values", [[None, 0.0], [np.nan, 0.0], [np.inf, 0.0], [1.0, 2.0]])
def test_corruption_rejected(packet, values) -> None:
    table = to_arrow(packet)
    changed = table.set_column(1, "log_likelihood", pa.array(values, type=pa.float64()))
    with pytest.raises(
        ValueError,
        match=(r"^(?:1\ validation\ error\ for\ _Rows|Evidence\ values,\ order\ or\ metadata\ changed)"),
    ):
        from_arrow(changed)


@pytest.mark.parametrize("dtype", [pa.float32(), pa.int64(), pa.string()])
def test_no_coercion(packet, dtype) -> None:
    table = to_arrow(packet)
    values = ["0", "1"] if pa.types.is_string(dtype) else [0, 1]
    table = table.set_column(1, "log_likelihood", pa.array(values, type=dtype))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Evidence\ requires\ the\ exact\ version\-1\ Arrow\ schema)"),
    ):
        from_arrow(table)


def test_chunking_hash_and_lifetime(packet, tmp_path) -> None:
    table = to_arrow(packet)
    chunked = pa.concat_tables([table.slice(0, 1), table.slice(1, 1)])
    np.testing.assert_array_equal(from_arrow(chunked).log_likelihood, packet.log_likelihood)
    stream = pa.RecordBatchReader.from_stream(table).read_all()
    address = table.column(1).chunk(0).buffers()[1].address
    view = to_polars(stream)
    assert view.frame.to_arrow().column(1).chunk(0).buffers()[1].address == address
    del table, stream
    gc.collect()
    assert from_polars(view).state_ids == packet.state_ids
    one, two = tmp_path / "one.arrow", tmp_path / "two.arrow"
    write_ipc(one, to_arrow(packet))
    write_ipc(two, chunked)
    assert hashlib.sha256(one.read_bytes()).digest() != hashlib.sha256(two.read_bytes()).digest()
    assert read_ipc(one).state_ids == read_ipc(two).state_ids
    with pytest.raises(FileExistsError):
        write_ipc(one, chunked)


def test_unknown_version_rollback(packet, tmp_path) -> None:
    table = to_arrow(packet)
    path = tmp_path / "retained.arrow"
    write_ipc(path, table)
    metadata = dict(table.schema.metadata)
    metadata[b"tobac.evidence.v1"] = metadata[b"tobac.evidence.v1"].replace(b'"version":1', b'"version":2')
    with pytest.raises(
        ValueError,
        match=(r"^(?:Unsupported\ evidence\ schema\ version)"),
    ):
        from_arrow(table.replace_schema_metadata(metadata))
    assert read_ipc(path).state_ids == packet.state_ids


def test_supplied_provenance_retained(packet) -> None:
    from tobac.interchange import read_metadata  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from tobac_supply.consumption_ledger import SupplyBasis  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    basis = SupplyBasis(source_ids=("retained-source",), observation_years=(2024,))
    covariance = np.array([[2.0, 0.5], [0.5, 1.0]])
    scope = replace(packet.source_scope, unit=basis.unit, geography=basis.geography)
    packet = replace(packet, source_scope=scope, target_scope=scope)
    table = to_arrow(
        packet,
        supply_basis=basis,
        covariance=covariance,
        observation_ids=("o1", "o2"),
        covariance_unit="counts^2",
        producer_revision="7af563c8cb373057d30662650b3f332f39e05b83",
    )
    wire = read_metadata(table)
    assert wire["supply_basis"]["duty_free_included"] is True
    assert wire["supply_basis"]["source_ids"] == ("retained-source",)
    assert wire["covariance"]["values"] == tuple(map(tuple, covariance))
    covariance[0, 0] = 99.0
    assert read_metadata(table)["covariance"]["values"][0][0] == 2.0


@pytest.mark.parametrize(
    ("covariance", "ids", "unit"),
    [
        (np.array([[1]], dtype=int), ("x",), "counts^2"),
        (np.array([[np.nan]]), ("x",), "counts^2"),
        (np.array([[np.inf]]), ("x",), "counts^2"),
        (np.array([[0.0]]), ("x",), "counts^2"),
        (np.array([[1.0, 0.0], [1.0, 1.0]]), ("x", "y"), "counts^2"),
        (np.eye(2), ("x", "x"), "counts^2"),
        (np.eye(2), ("x",), "counts^2"),
        (np.eye(2), ("x", "y"), ""),
        (None, ("x",), "counts^2"),
    ],
)
def test_invalid_covariance_rejected(packet, covariance, ids, unit) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Covariance\ labels\ require\ a\ covariance\ matrix"
            r"|"
            r"Covariance\ must\ be\ explicit\ float64,\ without\ coercion"
            r"|"
            r"Covariance\ must\ be\ positive\ definite"
            r"|"
            r"Covariance\ requires\ aligned\ unique\ observations,\ units\ and\ finite"
            r"\ symmetric\ values"
            r")"
        ),
    ):
        to_arrow(packet, covariance=covariance, observation_ids=ids, covariance_unit=unit)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("role", "forecast"),
        ("state_ids", ["b", "a"]),
        ("data_ids", ["new"]),
        ("unknown", "value"),
        ("version", True),
        ("version", "1"),
        ("captured_at", "2026-10-26T00:00:00"),
        ("producer_revision", ""),
        ("digest", "bad"),
    ],
)
def test_metadata_changes_rejected(packet, field, value) -> None:
    import json  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    table = to_arrow(packet)
    wire = json.loads(table.schema.metadata[b"tobac.evidence.v1"])
    wire[field] = value
    changed = table.replace_schema_metadata({b"tobac.evidence.v1": json.dumps(wire).encode()})
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Evidence\ metadata\ must\ use\ its\ canonical\ versioned\ encoding"
            r"|"
            r"Invalid\ evidence\ metadata"
            r")"
        ),
    ):
        from_arrow(changed)


def test_timestamp_precision_and_naive_input(packet) -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:captured_at\ must\ have\ an\ explicit\ UTC\ offset)"),
    ):
        to_arrow(packet, captured_at=datetime(2026, 10, 26))  # noqa: DTZ001 -- Deliberately naive datetime exercises the rejection boundary.
    table = to_arrow(packet)
    table = table.set_column(2, "captured_at", pa.array([None, None], type=pa.timestamp("ns", "UTC")))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Evidence\ requires\ the\ exact\ version\-1\ Arrow\ schema)"),
    ):
        from_arrow(table)


def test_conditioning_preserves_correlated_likelihood(packet) -> None:
    from tobac._core import DecisionProblem  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from tobac.evidence import Belief, condition  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from tobac.supply import release_loglikelihood  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    scope = packet.source_scope
    covariance = np.array([[2.0, 0.5], [0.5, 1.0]])
    logl = release_loglikelihood([3.0, 4.0], [[2.0, 4.0], [4.0, 5.0]], covariance)
    observed = replace(packet, log_likelihood=logl)
    problem = DecisionProblem(np.array([[0.0, 4.0], [3.0, 0.0]]), ("a", "b"), "score", np.array([0.75, 0.25]))
    prior = Belief(problem, packet.state_ids, scope)
    original = condition(prior, observed)
    table = to_arrow(
        observed, covariance=covariance, observation_ids=("o1", "o2"), covariance_unit="counts^2"
    )
    restored = condition(prior, from_polars(to_polars(table)))
    np.testing.assert_array_equal(original.problem.prior_weights, restored.problem.prior_weights)
    with pytest.raises(ValueError, match="reused"):
        condition(restored, from_arrow(table))


def test_real_installed_producer(packet) -> None:
    pytest.importorskip("voiage", reason="Native producer is required in the ecosystem session")
    from tobac._core import DecisionProblem, exact_evpi  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from tobac.evidence import Belief, condition  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from tobac.research.voiage_adapter import installed_evpi  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    observed = replace(packet, log_likelihood=np.array([-1.0, 0.0]))
    problem = DecisionProblem(np.array([[0.0, 4.0], [3.0, 0.0]]), ("a", "b"), "score", np.array([0.75, 0.25]))
    prior = Belief(problem, packet.state_ids, packet.source_scope)
    original = condition(prior, observed)
    restored = condition(prior, from_polars(to_polars(to_arrow(observed))))
    result = installed_evpi(restored.problem)["value"]
    assert result == installed_evpi(original.problem)["value"]
    np.testing.assert_allclose(result, exact_evpi(restored.problem), rtol=1e-12, atol=1e-12)


def test_supply_scope_mismatch_rejected(packet) -> None:
    from tobac_supply.consumption_ledger import SupplyBasis  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    with pytest.raises(ValueError, match="units/geography"):
        to_arrow(packet, supply_basis=SupplyBasis())


def test_sliced_chunk_buffers_and_caller_isolation(packet) -> None:
    table = to_arrow(packet)
    saved = table.column(1).to_pylist()
    # The original packet owns its copy; deliberately overriding NumPy's flag
    # demonstrates that the exported buffer does not alias that caller object.
    packet.log_likelihood.setflags(write=True)
    packet.log_likelihood[0] = 99.0
    assert table.column(1).to_pylist() == saved
    chunked = pa.concat_tables([table.slice(0, 1), table.slice(1, 1)])
    view = to_polars(chunked)
    actual = view.frame.to_arrow().column(1)
    assert actual.num_chunks == 2
    for left, right in zip(chunked.column(1).chunks, actual.chunks, strict=True):
        # Polars may rebase a sliced buffer, so compare the effective data
        # address including Arrow element offsets, rather than base addresses.
        assert left.buffers()[1].address + left.offset * 8 == right.buffers()[1].address + right.offset * 8
        assert len(left) == len(right)
