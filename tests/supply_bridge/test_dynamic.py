"""Independent analytic cases for the exploratory cohort reference model.

All counts, rates and effects below are constructed fixtures, never NZ estimates.
"""

import numpy as np
import pytest

from tobac_supply.dynamic import PRODUCTS, STATES, project_cohorts, project_health_cohorts


def fixture_inputs(intervals=3, cohorts=1):
    initial = np.zeros((cohorts, 6))
    initial[:, 1] = 100
    rates = np.zeros((intervals, cohorts, 6, 2))
    rates[:, :, 1, 0] = 10
    rates[:, :, 3, 0] = 4
    rates[:, :, 2:4, 1] = 20
    return {
        "initial_population": initial,
        "transitions": np.tile(np.eye(6), (intervals, cohorts, 1, 1)),
        "boundaries_years": np.arange(intervals + 1, dtype=float),
        "consumption_rates": rates,
        "cohort_ids": tuple(f"cohort_{i}" for i in range(cohorts)),
        "product_units": ("sticks", "ml_e_liquid"),
        "policy_ids": ("synthetic_status_quo",) * intervals,
        "assumption_id": "synthetic_analytic_fixture_v1",
    }


def test_static_limit_and_opening_occupancy_exposure():
    inputs = fixture_inputs()
    inputs["boundaries_years"] = [2027, 2027.25, 2028, 2030]
    result = project_cohorts(**inputs)
    np.testing.assert_array_equal(result.population[:, 0, 1], [100] * 4)
    np.testing.assert_array_equal(result.consumption[:, 0, 0], [250, 750, 2000])
    assert not result.consumption[:, :, 1].any()
    assert result.product_units == ("sticks", "ml_e_liquid")
    assert STATES[-1] == "dead"
    assert PRODUCTS == ("smoked_tobacco", "vaping")


def test_geometric_cessation_matches_closed_form():
    inputs = fixture_inputs(intervals=10)
    inputs["transitions"][:, :, 1, 1] = 0.8
    inputs["transitions"][:, :, 1, 4] = 0.2
    result = project_cohorts(**inputs)
    expected_smokers = 100 * 0.8 ** np.arange(11)
    np.testing.assert_allclose(result.population[:, 0, 1], expected_smokers)
    np.testing.assert_allclose(result.population[:, 0, 4], 100 - expected_smokers)
    assert result.consumption[:, 0, 0].sum() == pytest.approx(1000 * (1 - 0.8**10) / (1 - 0.8))


def test_substitution_and_dual_use_preserve_people_and_separate_products():
    inputs = fixture_inputs(intervals=2)
    inputs["transitions"][0, 0, 1] = [0, 0.3, 0.2, 0.4, 0.1, 0]
    result = project_cohorts(**inputs)
    np.testing.assert_array_equal(result.population[1, 0], [0, 30, 20, 40, 10, 0])
    np.testing.assert_array_equal(result.population.sum(axis=2), [[100], [100], [100]])
    np.testing.assert_array_equal(result.consumption[:, 0], [[1000, 0], [460, 1200]])


def test_policy_timing_changes_cumulative_exposure():
    early = fixture_inputs()
    late = fixture_inputs()
    early["transitions"][0, 0, 1] = [0, 0, 0, 0, 1, 0]
    late["transitions"][1, 0, 1] = [0, 0, 0, 0, 1, 0]
    early["policy_ids"] = ("cessation", "follow_up", "follow_up")
    late["policy_ids"] = ("wait", "cessation", "follow_up")
    a, b = project_cohorts(**early), project_cohorts(**late)
    assert a.consumption[:, 0, 0].sum() == 1000
    assert b.consumption[:, 0, 0].sum() == 2000
    np.testing.assert_array_equal(a.population[-1], b.population[-1])
    assert a.policy_ids != b.policy_ids


def test_cohort_heterogeneity_and_absorbing_deaths():
    inputs = fixture_inputs(intervals=2, cohorts=2)
    inputs["initial_population"][1, 1] = 50
    inputs["transitions"][:, 0, 1] = [0, 0.5, 0, 0, 0, 0.5]
    inputs["transitions"][:, 1, 1] = [0, 0.9, 0, 0, 0, 0.1]
    result = project_cohorts(**inputs)
    np.testing.assert_allclose(result.population[-1, :, -1], [75, 9.5])
    np.testing.assert_allclose(result.population.sum(axis=2), [[100, 50]] * 3)


def test_output_owns_inputs_and_rejects_mutation():
    inputs = fixture_inputs()
    result = project_cohorts(**inputs)
    inputs["initial_population"][:] = 0
    inputs["boundaries_years"][:] = 20
    assert result.population[0, 0, 1] == 100
    assert result.boundaries_years[0] == 0
    for array in (result.population, result.consumption, result.boundaries_years):
        with pytest.raises(ValueError, match="read-only"):
            array.flat[0] = 0


@pytest.mark.parametrize(
    "field", ["initial_population", "transitions", "boundaries_years", "consumption_rates"]
)
@pytest.mark.parametrize("invalid", [np.nan, np.inf, -np.inf])
def test_nonfinite_inputs_rejected(field, invalid):
    inputs = fixture_inputs()
    inputs[field].flat[0] = invalid
    with pytest.raises(ValueError, match="finite"):
        project_cohorts(**inputs)


@pytest.mark.parametrize(
    "field", ["initial_population", "transitions", "boundaries_years", "consumption_rates"]
)
def test_shape_broadcasting_rejected(field):
    inputs = fixture_inputs()
    inputs[field] = inputs[field][0]
    with pytest.raises(ValueError, match="shape"):
        project_cohorts(**inputs)


@pytest.mark.parametrize("field", ["initial_population", "consumption_rates"])
def test_negative_counts_or_rates_rejected(field):
    inputs = fixture_inputs()
    inputs[field].flat[0] = -1
    with pytest.raises(ValueError, match="nonnegative"):
        project_cohorts(**inputs)


@pytest.mark.parametrize("row", [[0, 0.9, 0, 0, 0, 0], [0, 1.1, 0, 0, -0.1, 0]])
def test_invalid_probabilities_are_not_repaired(row):
    inputs = fixture_inputs()
    inputs["transitions"][0, 0, 1] = row
    with pytest.raises(ValueError, match=r"sum to one|\[0, 1\]"):
        project_cohorts(**inputs)


@pytest.mark.parametrize("boundaries", [[0, 1, 1, 2], [0, 1, 0.5, 2]])
def test_nonpositive_time_intervals_rejected(boundaries):
    inputs = fixture_inputs()
    inputs["boundaries_years"] = boundaries
    with pytest.raises(ValueError, match="strictly positive"):
        project_cohorts(**inputs)


def test_death_cannot_reverse_and_never_use_cannot_regain_history():
    inputs = fixture_inputs()
    inputs["transitions"][0, 0, -1] = [0, 1, 0, 0, 0, 0]
    with pytest.raises(ValueError, match="absorbing"):
        project_cohorts(**inputs)
    inputs = fixture_inputs()
    inputs["transitions"][0, 0, 4] = [1, 0, 0, 0, 0, 0]
    with pytest.raises(ValueError, match="never_use"):
        project_cohorts(**inputs)


@pytest.mark.parametrize(("state", "product"), [(0, 0), (4, 1), (5, 0), (1, 1), (2, 0)])
def test_nonuser_or_wrong_product_consumption_rejected(state, product):
    inputs = fixture_inputs()
    inputs["consumption_rates"][0, 0, state, product] = 1
    with pytest.raises(ValueError, match="conflict"):
        project_cohorts(**inputs)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("cohort_ids", ("same", "same")),
        ("cohort_ids", ("",)),
        ("product_units", ("sticks",)),
        ("policy_ids", (" ",) * 3),
        ("assumption_id", ""),
    ],
)
def test_missing_or_ambiguous_metadata_rejected(field, value):
    inputs = fixture_inputs()
    inputs[field] = value
    with pytest.raises(ValueError, match=field):
        project_cohorts(**inputs)


@pytest.mark.parametrize("value", [True, "100"])
def test_nonnumeric_population_rejected(value):
    inputs = fixture_inputs()
    inputs["initial_population"] = [[value] * 6]
    with pytest.raises(ValueError, match="numeric"):
        project_cohorts(**inputs)


def test_projection_rejects_numerical_overflow():
    inputs = fixture_inputs()
    inputs["initial_population"][0, 1] = 1e308
    with pytest.raises(ValueError, match="overflowed"):
        project_cohorts(**inputs)


def test_mixed_numeric_boolean_input_is_not_silently_coerced():
    inputs = fixture_inputs()
    inputs["initial_population"] = [[0, 100, True, 0, 0, 0]]
    with pytest.raises(ValueError, match="numeric"):
        project_cohorts(**inputs)


def health_fixture_inputs(intervals=2, cohorts=1):
    inputs = fixture_inputs(intervals=intervals, cohorts=cohorts)
    inputs["survivor_transitions"] = inputs.pop("transitions")
    inputs["annual_hazards"] = np.zeros((intervals, cohorts, 5, 2))
    inputs["cause_ids"] = ("synthetic_cause_a", "synthetic_cause_b")
    return inputs


def test_health_projection_integrates_person_time_and_accumulates_deaths():
    inputs = health_fixture_inputs()
    inputs["initial_population"][0, -1] = 5
    inputs["boundaries_years"] = [2027, 2028, 2030]
    inputs["annual_hazards"][0, 0, 1, 0] = np.log(2)
    inputs["annual_hazards"][1, 0, 1, 1] = np.log(2) / 2
    result = project_health_cohorts(**inputs)

    np.testing.assert_allclose(result.population[:, 0, 1], [100, 50, 25])
    np.testing.assert_allclose(result.population[:, 0, -1], [5, 55, 80])
    np.testing.assert_allclose(result.population.sum(axis=2), 105)
    np.testing.assert_allclose(result.living_person_years[:, 0, 1], [50 / np.log(2)] * 2)
    np.testing.assert_allclose(result.consumption[:, 0, 0], [500 / np.log(2)] * 2)
    np.testing.assert_allclose(result.deaths[:, 0], [[50, 0], [0, 25]])
    assert result.cause_ids == inputs["cause_ids"]


def test_health_projection_zero_hazard_matches_discrete_reference():
    inputs = health_fixture_inputs(intervals=3, cohorts=2)
    inputs["boundaries_years"] = [0, 0.25, 1.5, 3]
    inputs["initial_population"][1] = [0, 0, 60, 20, 10, 7]
    inputs["survivor_transitions"][:, 0, 1, 1] = 0.8
    inputs["survivor_transitions"][:, 0, 1, 4] = 0.2
    inputs["survivor_transitions"][:, 1, 3] = [0, 0.2, 0.3, 0.4, 0.1, 0]
    reference = {key: value for key, value in inputs.items() if key not in ("annual_hazards", "cause_ids")}
    reference["transitions"] = reference.pop("survivor_transitions")
    discrete = project_cohorts(**reference)
    health = project_health_cohorts(**inputs)

    np.testing.assert_allclose(health.population, discrete.population, atol=1e-12)
    np.testing.assert_allclose(health.consumption, discrete.consumption, atol=1e-12)
    np.testing.assert_allclose(
        health.living_person_years,
        discrete.population[:-1, :, :-1] * np.diff(discrete.boundaries_years)[:, None, None],
    )
    assert not health.deaths.any()


def test_health_projection_cessation_changes_hazards_only_after_boundary():
    early = health_fixture_inputs()
    late = health_fixture_inputs()
    for inputs in (early, late):
        inputs["annual_hazards"][:, :, 1, 0] = np.log(2)
    early["survivor_transitions"][0, 0, 1] = [0, 0, 0, 0, 1, 0]
    late["survivor_transitions"][1, 0, 1] = [0, 0, 0, 0, 1, 0]
    a, b = project_health_cohorts(**early), project_health_cohorts(**late)

    assert a.population[-1, 0, 4] == pytest.approx(50)
    assert b.population[-1, 0, 4] == pytest.approx(25)
    assert a.consumption[:, 0, 0].sum() == pytest.approx(500 / np.log(2))
    assert b.consumption[:, 0, 0].sum() == pytest.approx(750 / np.log(2))
    assert a.living_person_years[1, 0, 4] == pytest.approx(50)
    assert a.living_person_years[1, 0, 1] == 0


def test_health_projection_keeps_causes_cohorts_and_products_separate():
    inputs = health_fixture_inputs(intervals=1, cohorts=2)
    inputs["initial_population"][1] = [0, 0, 50, 0, 0, 0]
    inputs["annual_hazards"][0, 0, 1] = [np.log(2), np.log(2)]
    result = project_health_cohorts(**inputs)

    np.testing.assert_allclose(result.deaths[0], [[37.5, 37.5], [0, 0]])
    np.testing.assert_allclose(result.population[-1, :, -1], [75, 0])
    np.testing.assert_allclose(result.consumption[0], [[750 / (2 * np.log(2)), 0], [0, 1000]])
    np.testing.assert_allclose(result.population.sum(axis=2), [[100, 50], [100, 50]])


def test_health_projection_rejects_duplicate_mortality_in_survivor_matrix():
    inputs = health_fixture_inputs()
    inputs["survivor_transitions"][0, 0, 1] = [0, 0.9, 0, 0, 0, 0.1]
    with pytest.raises(ValueError, match=r"mortality.*hazards"):
        project_health_cohorts(**inputs)


@pytest.mark.parametrize("invalid", [np.nan, np.inf, -np.inf, -0.1])
def test_health_projection_rejects_invalid_hazards(invalid):
    inputs = health_fixture_inputs()
    inputs["annual_hazards"][0, 0, 1, 0] = invalid
    with pytest.raises(ValueError, match=r"finite|nonnegative"):
        project_health_cohorts(**inputs)


@pytest.mark.parametrize("value", [True, "0"])
def test_health_projection_rejects_nonnumeric_hazards(value):
    inputs = health_fixture_inputs()
    inputs["annual_hazards"] = [[[[value, 0] for _ in range(5)]]] * 2
    with pytest.raises(ValueError, match="numeric"):
        project_health_cohorts(**inputs)


def test_health_projection_does_not_broadcast_hazards():
    inputs = health_fixture_inputs()
    inputs["annual_hazards"] = inputs["annual_hazards"][0]
    with pytest.raises(ValueError, match=r"annual_hazards.*shape"):
        project_health_cohorts(**inputs)


@pytest.mark.parametrize("cause_ids", [(), ("same", "same"), ("", "second"), ("first", " second")])
def test_health_projection_requires_named_unique_causes(cause_ids):
    inputs = health_fixture_inputs()
    inputs["cause_ids"] = cause_ids
    with pytest.raises(ValueError, match="cause_ids"):
        project_health_cohorts(**inputs)


def test_health_projection_owns_its_outputs():
    inputs = health_fixture_inputs()
    result = project_health_cohorts(**inputs)
    inputs["initial_population"][:] = 0
    inputs["boundaries_years"][:] = 20
    assert result.population[0, 0, 1] == 100
    assert result.boundaries_years[0] == 0
    for array in (
        result.population,
        result.consumption,
        result.boundaries_years,
        result.living_person_years,
        result.deaths,
    ):
        with pytest.raises(ValueError, match="read-only"):
            array.flat[0] = 0


@pytest.mark.parametrize("field", ["initial_population", "annual_hazards"])
def test_health_projection_rejects_overflow(field):
    inputs = health_fixture_inputs()
    inputs[field][:] = 1e308
    with pytest.raises(ValueError, match="overflowed"):
        project_health_cohorts(**inputs)
