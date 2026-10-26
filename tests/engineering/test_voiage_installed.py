"""Actual installed-library compatibility, separate from protocol doubles."""
from importlib.util import find_spec

import numpy as np
import pytest

pytestmark = pytest.mark.skipif(find_spec('voiage') is None,
                               reason='requires the isolated Nox voiage candidate environment')


def test_installed_release_weighted_and_partition_parity():
    from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
    from tobac.research.voiage_adapter import installed_evpi, installed_partial
    rng = np.random.default_rng(931)
    for states, actions in [(2, 2), (5, 3), (17, 4)]:
        for _ in range(10):
            values = rng.normal(size=(states, actions)) * 100
            weights = rng.uniform(size=states)
            weights[0] = 0
            weights /= weights.sum()
            p = DecisionProblem(values, tuple(str(i) for i in range(actions)), 'fixture units', weights)
            labels = np.arange(states) % 2
            assert installed_evpi(p)['value'] == pytest.approx(exact_evpi(p), abs=1e-10)
            assert installed_partial(p, labels)['value'] == pytest.approx(
                exact_partial_information(p, labels), abs=1e-10)


def test_actual_arrow_ipc_and_parquet_roundtrip(tmp_path):
    import pyarrow as pa
    import pyarrow.ipc as ipc
    import pyarrow.parquet as pq
    import voiage._core  # The genuine native extension must import on 3.15.1.
    from voiage.schema import ValueArray
    values = np.array([[1., 2.], [3., 0.], [-2., 4.]])
    table = pa.table({'a': values[:, 0], 'b': values[:, 1]})
    pq.write_table(table, tmp_path / 'fixture.parquet')
    with pa.OSFile(str(tmp_path / 'fixture.arrow'), 'wb') as stream:
        with ipc.new_file(stream, table.schema) as writer:
            writer.write_table(table)
    with ipc.open_file(tmp_path / 'fixture.arrow') as reader:
        restored = reader.read_all()
    assert restored.equals(table)
    assert pq.read_table(tmp_path / 'fixture.parquet').equals(table)
    np.testing.assert_array_equal(ValueArray.from_numpy(values).values, values)
