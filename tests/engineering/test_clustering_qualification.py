"""Synthetic qualification rejects leakage and preserves training-only discovery."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("sklearn", reason="Requires the isolated phase5 scikit-learn qualification profile")
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def qualifier():
    spec = importlib.util.spec_from_file_location(
        "cluster_qualifier", ROOT / "scripts/qualify_sensitivity_clustering.py"
    )
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_synthetic_references(qualifier) -> None:
    result = qualifier.sensitivity_check()
    assert result["sobol_first"] == pytest.approx([0.2, 0.8], abs=0.01)
    assert result["correlated_variance"] == pytest.approx(7.4, rel=0.025)


def test_cluster_training_is_unchanged_by_holdout(qualifier) -> None:
    train, test = qualifier.synthetic_features()
    ids = ([f"train-{i}" for i in range(len(train))], [f"test-{i}" for i in range(len(test))])
    first = qualifier.cluster_check(train, test, *ids)
    changed = qualifier.cluster_check(train, test + 0.25, *ids)
    assert first["selected_k"] == 3
    assert first["scaler_mean"] == changed["scaler_mean"]
    assert first["training_silhouettes"] == changed["training_silhouettes"]
    assert first["bootstrap_min_ari"] >= 0.9
    assert first["heldout_balanced_accuracy"] >= 0.95
    assert first["heldout_balanced_accuracy"] > first["majority_balanced_accuracy"]


@pytest.mark.parametrize("case", ["overlap", "nonfinite", "constant", "duplicate_id"])
def test_invalid_split_is_rejected(qualifier, case: str) -> None:
    train, test = qualifier.synthetic_features()
    train_ids = [f"train-{i}" for i in range(len(train))]
    test_ids = [f"test-{i}" for i in range(len(test))]
    if case == "overlap":
        test_ids[0] = train_ids[0]
    elif case == "nonfinite":
        train[0, 0] = np.nan
    elif case == "constant":
        train[:, 0] = 1
    else:
        train_ids[0] = train_ids[1]
    with pytest.raises(ValueError, match="Finite nondegenerate features"):
        qualifier.cluster_check(train, test, train_ids, test_ids)


def test_no_structure_yields_no_use(qualifier) -> None:
    rng = np.random.default_rng(20261109)
    train = rng.normal(size=(384, 12))
    test = rng.normal(size=(192, 12))
    result = qualifier.cluster_check(
        train, test, [f"train-{i}" for i in range(len(train))], [f"test-{i}" for i in range(len(test))]
    )
    assert result["discovery_status"] == "no_use"
    assert result["supervised_evaluated"] is False


def test_holdout_with_missing_clusters_is_not_scored(qualifier) -> None:
    train, test = qualifier.synthetic_features()
    result = qualifier.cluster_check(
        train,
        test + 100,
        [f"train-{i}" for i in range(len(train))],
        [f"test-{i}" for i in range(len(test))],
    )
    assert result["discovery_status"] == "holdout_lacks_clusters"
    assert result["supervised_evaluated"] is False


def test_existing_output_is_preserved(qualifier, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output = tmp_path / "completed"
    output.mkdir()
    preserved_file = output / "preserve.txt"
    preserved_file.write_text("retained")
    monkeypatch.setattr(sys, "argv", ["qualify", "--out", str(output), "--lock", "unused.lock"])
    with pytest.raises(ValueError, match="Refusing to overwrite"):
        qualifier.main()
    assert preserved_file.read_text() == "retained"
