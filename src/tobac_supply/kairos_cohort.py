"""Read Kairos cohort and exposure IPC streams with the optional interchange extra.

Rows retain their original Arrow columns and metadata. The caller supplies the
initial cohort and interprets the stratum and state codes.
"""

from __future__ import annotations

import importlib
import math
from collections import Counter
from typing import Any, cast
lazy from collections.abc import Mapping
lazy from pathlib import Path

pa = importlib.import_module("pyarrow")

type Entity = tuple[int, int]
type State = tuple[int, int]

_ENTITY_FIELDS = [
    pa.field("entity_id_index", pa.uint64(), nullable=False),
    pa.field("entity_id_gen", pa.uint32(), nullable=False),
    pa.field("stratum_id", pa.uint32(), nullable=False),
]
_EVENT_TIME_FIELDS = [
    pa.field("event_time_hi", pa.uint64(), nullable=False),
    pa.field("event_time_lo", pa.uint64(), nullable=False),
]
_TRANSITIONS = pa.schema(
    [
        *_ENTITY_FIELDS,
        pa.field("from_state", pa.uint32(), nullable=False),
        pa.field("to_state", pa.uint32(), nullable=False),
        *_EVENT_TIME_FIELDS,
        pa.field("dwell_time_hi", pa.uint64(), nullable=False),
        pa.field("dwell_time_lo", pa.uint64(), nullable=False),
        pa.field("visit_index", pa.uint64(), nullable=False),
        pa.field("draw_slot", pa.uint32(), nullable=False),
        pa.field("rng_substream_id", pa.uint64(), nullable=False),
    ]
)
_EXPOSURES = pa.schema(
    [
        *_ENTITY_FIELDS,
        *_EVENT_TIME_FIELDS,
        pa.field("spatial_cell_id", pa.uint64(), nullable=False),
        pa.field("radius_metres", pa.float64(), nullable=False),
        pa.field("features_within_radius", pa.uint32(), nullable=False),
        pa.field("nearest_feature_metres", pa.float64(), nullable=True),
    ]
)


def _tick_unit(unit: str) -> bytes:
    if unit not in {"millisecond", "second", "minute", "hour", "day"}:
        msg = "Unknown Kairos tick unit"
        raise ValueError(msg)
    return unit.encode("ascii")


def _read_stream(path: Path, schema: object) -> object:
    with pa.memory_map(str(path), "r") as source, pa.ipc.open_stream(source) as stream:
        if not stream.schema.equals(schema, check_metadata=True):
            msg = "Kairos IPC schema, units or provenance do not match"
            raise ValueError(msg)
        table = stream.read_all()
        if source.tell() != source.size():
            msg = "Kairos IPC file contains data after the stream"
            raise ValueError(msg)
    table.validate(full=True)
    if any(not field.nullable and table[field.name].null_count for field in table.schema):
        msg = "Kairos IPC stream contains nulls in a required column"
        raise ValueError(msg)
    return table


def read_cohort_transitions(path: Path, *, tick_unit: str, run_seed: int) -> object:
    """Read a v1 Arrow transition table with the expected time and RNG metadata."""
    if type(run_seed) is not int or not 0 <= run_seed < (1 << 64):
        msg = "Kairos run seed must be an unsigned 64-bit integer"
        raise ValueError(msg)
    schema = _TRANSITIONS.with_metadata(
        {
            b"kairo_ecs.projected_schema": b"kairo_ecs.cohort_transition.v1",
            b"kairo_ecs.tick_unit": _tick_unit(tick_unit),
            b"kairo_ecs.run_seed": str(run_seed).encode("ascii"),
            b"kairo_ecs.rng_profile": b"rand_distr_0.6",
        }
    )
    return _read_stream(path, schema)


def read_spatial_exposures(path: Path, *, tick_unit: str) -> object:
    """Read a v1 Arrow exposure table with distances in metres."""
    schema = _EXPOSURES.with_metadata(
        {
            b"kairo_ecs.projected_schema": b"kairo_ecs.spatial_exposure.v1",
            b"kairo_ecs.tick_unit": _tick_unit(tick_unit),
            b"kairo_ecs.length_unit": b"metre",
        }
    )
    table = _read_stream(path, schema)
    previous: dict[Entity, int] = {}
    for batch in cast("Any", table).to_batches():
        for row in cast("list[dict[str, int | float | None]]", batch.to_pylist()):
            entity = (cast("int", row["entity_id_index"]), cast("int", row["entity_id_gen"]))
            tick = (cast("int", row["event_time_hi"]) << 64) | cast("int", row["event_time_lo"])
            radius = cast("float", row["radius_metres"])
            nearest = row["nearest_feature_metres"]
            if (
                tick < previous.get(entity, 0)
                or not math.isfinite(radius)
                or radius < 0
                or (nearest is None) != (row["features_within_radius"] == 0)
                or (nearest is not None and not (0 <= nearest <= radius))
            ):
                msg = "Invalid Kairos exposure chronology or proximity"
                raise ValueError(msg)
            previous[entity] = tick
    return table


def cohort_state_counts(
    transitions: object, initial: Mapping[Entity, State], *, at_tick: int
) -> dict[State, int]:
    """Count members by (stratum, state), applying events through the given tick.

    Pass a table from read_cohort_transitions and every initial member keyed
    by (entity index, generation), including members with no transitions.
    """
    if type(at_tick) is not int or not 0 <= at_tick < (1 << 128):
        msg = "Cohort cutoff must be an unsigned 128-bit tick"
        raise ValueError(msg)
    table = cast("Any", transitions)
    counts = Counter(initial.values())
    previous: dict[Entity, tuple[int, int]] = {}
    for batch in table.to_batches():
        for row in cast("list[dict[str, int]]", batch.to_pylist()):
            entity = (row["entity_id_index"], row["entity_id_gen"])
            stratum, origin, destination = row["stratum_id"], row["from_state"], row["to_state"]
            tick = (row["event_time_hi"] << 64) | row["event_time_lo"]
            dwell = (row["dwell_time_hi"] << 64) | row["dwell_time_lo"]
            member = initial.get(entity)
            prior = previous.get(entity)
            if (
                member is None
                or member[0] != stratum
                or origin == destination
                or dwell > tick
                or (prior is None and member[1] != origin)
                or (prior is not None and prior != (origin, tick - dwell))
            ):
                msg = "Kairos transition does not match the initial cohort or visit history"
                raise ValueError(msg)
            previous[entity] = (destination, tick)
            if tick <= at_tick:
                counts[stratum, origin] -= 1
                counts[stratum, destination] += 1
    return dict(+counts)
