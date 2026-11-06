"""Qualify maintained sensitivity/clustering libraries on synthetic cases only."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import logging
import platform
from importlib.metadata import distributions, version
from pathlib import Path
from typing import Any, cast

import numpy as np
import polars as pl
from numpy.typing import NDArray
from scipy.stats import sobol_indices, uniform
from sklearn.cluster import KMeans
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score, balanced_accuracy_score, log_loss, silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

type FloatArray = NDArray[np.float64]

LOGGER = logging.getLogger(__name__)
SEED = 20261106
FEATURE_COUNT = 2
MIN_ROWS = 12
EXPECTED_CLUSTERS = 3
VARIANCE_RTOL = 0.025
MIN_STABILITY = 0.9
MIN_ACCURACY = 0.95
MIN_SILHOUETTE = 0.25
MIN_CLUSTER_SIZE = 8


def sensitivity_check() -> dict[str, Any]:
    """Check independent Sobol effects and a separate correlated-PSA variance oracle."""

    def linear(x: FloatArray) -> FloatArray:
        return x[0] + 2 * x[1]

    result = sobol_indices(
        func=linear,
        n=4096,
        # scipy-stubs 1.18.1.1 declares ppf scalar-only; runtime supports array quantiles.
        # This narrow boundary is exercised against the analytical Sobol reference below.
        dists=[cast("Any", uniform()), cast("Any", uniform())],
        rng=np.random.default_rng(SEED),
    )
    draws = np.random.default_rng(SEED).multivariate_normal(
        [0, 0],
        [[1, 0.6], [0.6, 1]],
        size=65536,
    )
    variance = float(np.var(draws[:, 0] + 2 * draws[:, 1], ddof=1))
    return {
        "sobol_first": result.first_order.tolist(),
        "sobol_total": result.total_order.tolist(),
        "sobol_oracle": [0.2, 0.8],
        "sobol_input_assumption": "independent_uniform_fixture_only",
        "correlated_variance": variance,
        "correlated_variance_oracle": 7.4,
        "correlated_draws": len(draws),
        "correlation": 0.6,
        "correlated_case_has_no_independent_sobol_indices": True,
    }


def synthetic_features() -> tuple[FloatArray, FloatArray]:
    """Use independent train/test generators; no empirical source or posterior is read."""
    centers = np.asarray([[-5, 0], [0, 5], [5, 0]])

    def draw(seed: int, per_center: int) -> FloatArray:
        rng = np.random.default_rng(seed)
        values = np.concatenate([rng.normal(c, 0.25, (per_center, FEATURE_COUNT)) for c in centers])
        return values[rng.permutation(len(values))]

    return draw(SEED, 128), draw(SEED + 1, 64)


def cluster_check(
    train: FloatArray,
    test: FloatArray,
    train_ids: list[str],
    test_ids: list[str],
) -> dict[str, Any]:
    """Select discovery on training rows, then predict frozen pseudo-labels on holdout."""
    if (
        train.ndim != FEATURE_COUNT
        or test.ndim != FEATURE_COUNT
        or train.shape[1] != test.shape[1]
        or len(train) < MIN_ROWS
        or not len(test)
        or not np.isfinite(train).all()
        or not np.isfinite(test).all()
        or (np.std(train, axis=0) == 0).any()
        or len(train_ids) != len(train)
        or len(test_ids) != len(test)
        or len(set(train_ids)) != len(train_ids)
        or len(set(test_ids)) != len(test_ids)
        or bool(set(train_ids) & set(test_ids))
    ):
        msg = "Finite nondegenerate features and unique disjoint matching split IDs required"
        raise ValueError(msg)
    with threadpool_limits(limits=1):
        scaler = StandardScaler().fit(train)
        training = scaler.transform(train)
        models = {k: KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(training) for k in (2, 3, 4)}
        scores = {k: float(silhouette_score(training, m.labels_)) for k, m in models.items()}
        chosen = max(scores, key=lambda k: (scores[k], -k))
        discovery = models[chosen]
        labels = discovery.labels_
        rng = np.random.default_rng(SEED + 2)
        stability: list[float] = []
        for i in range(12):
            sample = train[rng.integers(0, len(train), len(train))]
            boot = make_pipeline(
                StandardScaler(),
                KMeans(n_clusters=chosen, n_init=10, random_state=SEED + i),
            ).fit(sample)
            stability.append(float(adjusted_rand_score(labels, boot.predict(train))))
        training_report: dict[str, Any] = {
            "selected_k": chosen,
            "training_silhouettes": {str(k): v for k, v in scores.items()},
            "scaler_mean": scaler.mean_.tolist(),
            "scaler_scale": scaler.scale_.tolist(),
            "cluster_centers_scaled": discovery.cluster_centers_.tolist(),
            "bootstrap_min_ari": min(stability),
            "bootstrap_ari": stability,
            "cluster_sizes": np.bincount(labels).tolist(),
            "train_rows": len(train),
            "test_rows": len(test),
        }
        if (
            scores[chosen] < MIN_SILHOUETTE
            or min(stability) < MIN_STABILITY
            or np.bincount(labels).min() < MIN_CLUSTER_SIZE
        ):
            return {**training_report, "discovery_status": "no_use", "supervised_evaluated": False}
        classifier = make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=1000, random_state=SEED)
        ).fit(train, labels)
        baseline = DummyClassifier(strategy="most_frequent").fit(train, labels)
        # Holdout is first used only after all training fitting/selection/stability work.
        target = discovery.predict(scaler.transform(test))
        if set(target) != set(labels):
            return {
                **training_report,
                "discovery_status": "holdout_lacks_clusters",
                "supervised_evaluated": False,
                "heldout_observed_clusters": np.unique(target).tolist(),
            }
        predictions = classifier.predict(test)
        return {
            **training_report,
            "discovery_status": "stable_under_fixture_rules",
            "supervised_evaluated": True,
            "classifier_coefficients": classifier.named_steps["logisticregression"].coef_.tolist(),
            "classifier_intercepts": classifier.named_steps["logisticregression"].intercept_.tolist(),
            "classifier_classes": classifier.classes_.tolist(),
            "heldout_balanced_accuracy": float(balanced_accuracy_score(target, predictions)),
            "heldout_log_loss": float(
                log_loss(target, classifier.predict_proba(test), labels=classifier.classes_)
            ),
            "majority_balanced_accuracy": float(balanced_accuracy_score(target, baseline.predict(test))),
            "majority_log_loss": float(
                log_loss(target, baseline.predict_proba(test), labels=baseline.classes_)
            ),
            "validation_scope": "imitation_of_frozen_cluster_labels_not_external_substantive_validation",
        }


def main() -> None:
    """Emit a versioned, non-overwriting qualification packet for synthetic fixtures."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--lock", required=True, type=Path)
    args = parser.parse_args()
    if platform.python_version() != "3.15.2" or any(
        importlib.util.find_spec(name) is not None for name in ("pandas", "xarray")
    ):
        msg = "Qualification requires Python 3.15.2 and no pandas/xarray"
        raise ValueError(msg)
    if args.out.exists():
        msg = "Refusing to overwrite a qualification output"
        raise ValueError(msg)
    lock_hash = hashlib.sha256(args.lock.read_bytes()).hexdigest()
    sensitivity = sensitivity_check()
    train, test = synthetic_features()
    clusters = cluster_check(
        train, test, [f"train-{i}" for i in range(len(train))], [f"test-{i}" for i in range(len(test))]
    )
    passed = (
        np.allclose(sensitivity["sobol_first"], [0.2, 0.8], atol=0.01, rtol=0)
        and np.allclose(sensitivity["sobol_total"], [0.2, 0.8], atol=0.01, rtol=0)
        and abs(sensitivity["correlated_variance"] / 7.4 - 1) <= VARIANCE_RTOL
        and clusters["selected_k"] == EXPECTED_CLUSTERS
        and clusters["supervised_evaluated"]
        and clusters["bootstrap_min_ari"] >= MIN_STABILITY
        and clusters["heldout_balanced_accuracy"] >= MIN_ACCURACY
    )
    if not passed:
        msg = "Synthetic reference qualification failed"
        raise ArithmeticError(msg)
    args.out.mkdir(parents=True)
    report = {
        "schema_version": 1,
        "success": True,
        "source": "synthetic_only",
        "empirical_qualification": False,
        "seed": SEED,
        "test_seed": SEED + 1,
        "train_features_sha256": hashlib.sha256(train.astype("<f8").tobytes()).hexdigest(),
        "test_features_sha256": hashlib.sha256(test.astype("<f8").tobytes()).hexdigest(),
        "python": platform.python_version(),
        "versions": {name: version(name) for name in ("numpy", "scipy", "polars", "scikit-learn")},
        "sensitivity": sensitivity,
        "clusters": clusters,
    }
    (args.out / "summary.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    pl.DataFrame({"bootstrap": range(12), "adjusted_rand_index": clusters["bootstrap_ari"]}).write_csv(
        args.out / "stability.csv"
    )
    manifest = {
        "formula_version": "synthetic-sensitivity-clustering-v1",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "lock_sha256": lock_hash,
        "installed_packages": dict(sorted((d.metadata["Name"], d.version) for d in distributions())),
        "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in args.out.iterdir()},
    }
    root = Path(__file__).resolve().parents[1]
    inputs = [
        root / "engineering/requirements.lock",
        root / "conductor/tracks/nz_au_empirical_20261106/phase5-qualification.in",
        root / "engineering/typings/threadpoolctl.pyi",
        *sorted((root / "engineering/typings/sklearn").glob("*.pyi")),
    ]
    manifest["qualification_inputs"] = {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    LOGGER.info("Synthetic qualification passed; empirical qualification remains false")


if __name__ == "__main__":
    main()
