"""Regression checks for the versioned Kairos streams accepted by Tobac."""

from typing import cast
lazy from pathlib import Path

import pyarrow as pa
import pytest

from tobac_supply.kairos_cohort import cohort_state_counts, read_cohort_transitions, read_spatial_exposures

_BASE = [
    pa.field("entity_id_index", pa.uint64(), nullable=False),
    pa.field("entity_id_gen", pa.uint32(), nullable=False),
    pa.field("stratum_id", pa.uint32(), nullable=False),
]
_TIME = [
    pa.field("event_time_hi", pa.uint64(), nullable=False),
    pa.field("event_time_lo", pa.uint64(), nullable=False),
]
_UNIT = {b"kairo_ecs.tick_unit": b"millisecond"}
_COHORT = pa.schema(
    [
        *_BASE,
        pa.field("from_state", pa.uint32(), nullable=False),
        pa.field("to_state", pa.uint32(), nullable=False),
        *_TIME,
        pa.field("dwell_time_hi", pa.uint64(), nullable=False),
        pa.field("dwell_time_lo", pa.uint64(), nullable=False),
        pa.field("visit_index", pa.uint64(), nullable=False),
        pa.field("draw_slot", pa.uint32(), nullable=False),
        pa.field("rng_substream_id", pa.uint64(), nullable=False),
    ],
    metadata={
        **_UNIT,
        b"kairo_ecs.projected_schema": b"kairo_ecs.cohort_transition.v1",
        b"kairo_ecs.run_seed": b"753",
        b"kairo_ecs.rng_profile": b"rand_distr_0.6",
    },
)


def _write(path: Path, table: pa.Table) -> None:
    with pa.OSFile(str(path), "w") as sink, pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table, max_chunksize=1)


def test_counts_full_width_ticks_in_stream_order(tmp_path: Path) -> None:
    """Retain both generations and apply same-tick exits across batches."""
    entity = (1 << 64) - 1
    rows = [
        (entity, 7, 5, 0, 1, 1, 4, 0, 4, 0, 0, 31),
        (entity, 7, 5, 1, 2, 1, 4, 0, 0, 0, 0, 32),
    ]
    path = tmp_path / "transitions.arrow"
    _write(path, pa.Table.from_arrays(list(zip(*rows, strict=True)), schema=_COHORT))
    table = read_cohort_transitions(path, tick_unit="millisecond", run_seed=753)
    initial = {(entity, 7): (5, 0), (entity, 8): (5, 0)}
    assert cohort_state_counts(table, initial, at_tick=(1 << 64) + 3) == {(5, 0): 2}
    assert cohort_state_counts(table, initial, at_tick=(1 << 64) + 4) == {(5, 0): 1, (5, 2): 1}
    with pytest.raises(ValueError, match="initial cohort or visit history"):
        cohort_state_counts(table, {(entity, 8): (5, 0)}, at_tick=(1 << 64) + 4)
    with pytest.raises(ValueError, match="schema, units or provenance"):
        read_cohort_transitions(path, tick_unit="day", run_seed=753)
    with pytest.raises(ValueError, match="schema, units or provenance"):
        read_cohort_transitions(path, tick_unit="millisecond", run_seed=754)
    with path.open("ab") as stream:
        stream.write(b"trailing bytes")
    with pytest.raises(ValueError, match="data after the stream"):
        read_cohort_transitions(path, tick_unit="millisecond", run_seed=753)


def test_exposure_distinguishes_missing_nearest_from_zero_metres(tmp_path: Path) -> None:
    """A point at the query origin is an observed distance."""
    schema = pa.schema(
        [
            *_BASE,
            *_TIME,
            pa.field("spatial_cell_id", pa.uint64(), nullable=False),
            pa.field("radius_metres", pa.float64(), nullable=False),
            pa.field("features_within_radius", pa.uint32(), nullable=False),
            pa.field("nearest_feature_metres", pa.float64(), nullable=True),
        ],
        metadata={
            **_UNIT,
            b"kairo_ecs.projected_schema": b"kairo_ecs.spatial_exposure.v1",
            b"kairo_ecs.length_unit": b"metre",
        },
    )
    columns = [[1, 1], [3, 3], [5, 5], [0, 0], [0, 1], [10, 11], [8.0, 8.0], [1, 0], [0.0, None]]
    path = tmp_path / "exposure.arrow"
    _write(path, pa.Table.from_arrays(columns, schema=schema))
    table = cast("pa.Table", read_spatial_exposures(path, tick_unit="millisecond"))
    assert table["nearest_feature_metres"].to_pylist() == [0.0, None]
    columns[-1] = [0.0, 1.0]
    invalid_path = tmp_path / "invalid.arrow"
    _write(invalid_path, pa.Table.from_arrays(columns, schema=schema))
    with pytest.raises(ValueError, match="Invalid Kairos exposure"):
        read_spatial_exposures(invalid_path, tick_unit="millisecond")
