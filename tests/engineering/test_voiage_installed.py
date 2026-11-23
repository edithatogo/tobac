"""Actual installed-library compatibility, separate from protocol doubles."""

import csv
import json
from importlib.util import find_spec
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.skipif(
    find_spec("voiage") is None, reason="requires the isolated Nox voiage candidate environment"
)


def test_installed_release_weighted_and_partition_parity() -> None:
    from tobac._core import DecisionProblem, exact_evpi, exact_partial_information  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from tobac.research.voiage_adapter import installed_evpi, installed_partial  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    rng = np.random.default_rng(931)
    for states, actions in [(2, 2), (5, 3), (17, 4)]:
        for _ in range(10):
            values = rng.normal(size=(states, actions)) * 100
            weights = rng.uniform(size=states)
            weights[0] = 0
            weights /= weights.sum()
            p = DecisionProblem(values, tuple(str(i) for i in range(actions)), "fixture units", weights)
            labels = np.arange(states) % 2
            assert installed_evpi(p)["value"] == pytest.approx(exact_evpi(p), abs=1e-10)
            assert installed_partial(p, labels)["value"] == pytest.approx(
                exact_partial_information(p, labels), abs=1e-10
            )


def test_installed_release_matches_frozen_m2_retail_evpi() -> None:
    from tobac._core import exact_evpi  # noqa: PLC0415 -- Import at the exercised capability boundary.
    from tobac.regulation import load_config  # noqa: PLC0415 -- Import at the exercised capability boundary.
    from tobac.retail_case import build_retail_states, retail_problem  # noqa: PLC0415 -- Import at the exercised capability boundary.

    root = Path(__file__).resolve().parents[2]
    with (root / "results/milestone2/summary.csv").open(encoding="utf-8", newline="") as stream:
        reference = next(
            row
            for row in csv.DictReader(stream)
            if row["case"] == "source_shape_partial_replacement" and row["crime_weight"] == "1.0"
        )
    specification = json.loads((root / "configs/m2_retail.json").read_text(encoding="utf-8"))
    case = next(case for case in specification["cases"] if case["id"] == reference["case"])
    states, prior, config = build_retail_states(
        load_config(root / specification["base_config"]),
        quit_points=int(reference["quit_nodes"]),
        transport=case["transport"],
        null_weight=case["null_weight"],
        source_beta=tuple(specification["source_beta"]),
    )
    problem = retail_problem(
        states, prior, config, float(reference["crime_weight"]), lawful_replacement=case["lawful_replacement"]
    )
    expected = pytest.approx(float(reference["evpi"]), rel=1e-10, abs=1e-10)
    assert len(prior) == int(reference["states"])
    assert problem.value_unit == reference["value_unit"]
    assert exact_evpi(problem) == expected
    assert exact_evpi(problem, backend="voiage") == expected


def test_actual_arrow_ipc_and_parquet_roundtrip(tmp_path) -> None:
    import pyarrow as pa  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    import pyarrow.parquet as pq  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from pyarrow import ipc  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.
    from voiage.schema import ValueArray  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    values = np.array([[1.0, 2.0], [3.0, 0.0], [-2.0, 4.0]])
    table = pa.table({"a": values[:, 0], "b": values[:, 1]})
    pq.write_table(table, tmp_path / "fixture.parquet")
    with (
        pa.OSFile(str(tmp_path / "fixture.arrow"), "wb") as stream,
        ipc.new_file(stream, table.schema) as writer,
    ):
        writer.write_table(table)
    with ipc.open_file(tmp_path / "fixture.arrow") as reader:
        restored = reader.read_all()
    assert restored.equals(table)
    assert pq.read_table(tmp_path / "fixture.parquet").equals(table)
    np.testing.assert_array_equal(ValueArray.from_numpy(values).values, values)
