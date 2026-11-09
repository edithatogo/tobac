"""Hypothesis contracts; hardened CI requires the dependency before collecting tests."""

import numpy as np
import pytest

pytest.importorskip("hypothesis", reason="Local optional dependency unavailable; engineering CI requires it")
from hypothesis import given, settings
from hypothesis import strategies as st

from tobac._core import DecisionProblem, exact_evpi
from tobac.health import competing_mortality, exposure_health_step, illness_death_interval
from tobac.information import evaluate
from tobac.partial_identification import Interval, restriction_bounds
from tobac.supply import expected_releases
from tobac_supply.dynamic import project_cohorts, project_health_cohorts
from tobac_supply.longitudinal import continuous_correlation


@settings(max_examples=100, deadline=None, derandomize=True)
@given(st.lists(st.integers(-10000, 10000), min_size=6, max_size=6))
def test_evpi_is_nonnegative_and_invariant_to_common_value_offset(values) -> None:
    matrix = np.array(values, float).reshape(3, 2)
    a = exact_evpi(DecisionProblem(matrix, ["a", "b"], "fixture_units"))
    b = exact_evpi(DecisionProblem(matrix + 10000, ["a", "b"], "fixture_units"))
    assert a >= 0
    assert a == pytest.approx(b, abs=1e-9)


@settings(max_examples=100, deadline=None, derandomize=True)
@given(
    st.floats(1, 10000, allow_nan=False, allow_infinity=False),
    st.floats(0, 0.5, allow_nan=False, allow_infinity=False),
)
def test_observation_accounting_uses_absolute_unrecorded_amount(total, illicit) -> None:
    unrecorded = total * 0.1
    result = expected_releases(total, illicit, unrecorded)
    assert float(result) == pytest.approx(total * (1 - illicit) - unrecorded)


@settings(max_examples=60, deadline=None, derandomize=True)
@given(st.lists(st.integers(0, 365), min_size=1, max_size=12), st.floats(0.1, 365))
def test_calendar_covariance_is_psd_for_irregular_and_duplicate_days(days, half_life) -> None:
    matrix = continuous_correlation(days, half_life)
    assert np.linalg.eigvalsh(matrix).min() >= -1e-10
    np.testing.assert_allclose(np.diag(matrix), 1.0)


@settings(max_examples=60, deadline=None, derandomize=True)
@given(
    st.lists(st.floats(0.0, 0.25, allow_nan=False, allow_infinity=False), min_size=1, max_size=4),
    st.floats(0.05, 5.0, allow_nan=False, allow_infinity=False),
    st.floats(0.05, 5.0, allow_nan=False, allow_infinity=False),
    st.floats(0.01, 0.25, allow_nan=False, allow_infinity=False),
)
def test_competing_mortality_semigroup_conservation_and_hazard_monotonicity(
    hazards, years_a, years_b, extra_hazard
) -> None:
    rates = tuple(hazards)
    combined = competing_mortality(rates, years_a + years_b)
    step_a = competing_mortality(rates, years_a)
    step_b = competing_mortality(rates, years_b)

    assert combined.survival + sum(combined.death_probabilities) == pytest.approx(1.0, abs=1e-12)
    assert combined.survival == pytest.approx(step_a.survival * step_b.survival, rel=1e-12, abs=1e-12)
    assert combined.living_person_years == pytest.approx(
        step_a.living_person_years + step_a.survival * step_b.living_person_years,
        rel=1e-12,
        abs=1e-12,
    )

    elevated = (rates[0] + extra_hazard, *rates[1:])
    worse = competing_mortality(elevated, years_a)
    assert worse.survival < step_a.survival
    assert worse.living_person_years < step_a.living_person_years


@settings(max_examples=60, deadline=None, derandomize=True)
@given(
    st.tuples(
        st.floats(1.0, 1000.0, allow_nan=False, allow_infinity=False),
        st.floats(1.0, 1000.0, allow_nan=False, allow_infinity=False),
    ),
    st.tuples(
        st.floats(0.0, 0.2, allow_nan=False, allow_infinity=False),
        st.floats(0.0, 0.2, allow_nan=False, allow_infinity=False),
        st.floats(0.0, 0.3, allow_nan=False, allow_infinity=False),
    ),
    st.floats(0.1, 3.0, allow_nan=False, allow_infinity=False),
    st.floats(0.1, 3.0, allow_nan=False, allow_infinity=False),
)
def test_illness_death_subdivision_semigroup_and_mass_conservation(
    counts,
    hazards,
    years_a,
    years_b,
) -> None:
    disease_free, diagnosed = counts
    incidence_hazard, free_death_hazard, diagnosed_death_hazard = hazards
    combined = illness_death_interval(
        disease_free=disease_free,
        diagnosed=diagnosed,
        incidence_hazard=incidence_hazard,
        disease_free_death_hazard=free_death_hazard,
        diagnosed_death_hazard=diagnosed_death_hazard,
        years=years_a + years_b,
    )
    first = illness_death_interval(
        disease_free=disease_free,
        diagnosed=diagnosed,
        incidence_hazard=incidence_hazard,
        disease_free_death_hazard=free_death_hazard,
        diagnosed_death_hazard=diagnosed_death_hazard,
        years=years_a,
    )
    second = illness_death_interval(
        disease_free=first.disease_free,
        diagnosed=first.diagnosed,
        incidence_hazard=incidence_hazard,
        disease_free_death_hazard=free_death_hazard,
        diagnosed_death_hazard=diagnosed_death_hazard,
        years=years_b,
    )

    total_initial = disease_free + diagnosed
    total_end = (
        combined.disease_free
        + combined.diagnosed
        + combined.deaths_before_diagnosis
        + combined.deaths_after_diagnosis
    )
    assert total_end == pytest.approx(total_initial, rel=1e-11, abs=1e-9)
    assert combined.disease_free == pytest.approx(second.disease_free, rel=1e-11, abs=1e-9)
    assert combined.diagnosed == pytest.approx(second.diagnosed, rel=1e-11, abs=1e-9)
    assert combined.disease_free_person_years == pytest.approx(
        first.disease_free_person_years + second.disease_free_person_years,
        rel=1e-11,
        abs=1e-9,
    )
    assert combined.diagnosed_person_years == pytest.approx(
        first.diagnosed_person_years + second.diagnosed_person_years,
        rel=1e-11,
        abs=1e-9,
    )


@settings(max_examples=60, deadline=None, derandomize=True)
@given(
    st.lists(st.floats(10.0, 500.0, allow_nan=False, allow_infinity=False), min_size=5, max_size=5),
    st.floats(0.0, 0.3, allow_nan=False, allow_infinity=False),
    st.floats(0.0, 0.3, allow_nan=False, allow_infinity=False),
    st.floats(0.25, 3.0, allow_nan=False, allow_infinity=False),
)
def test_dynamic_health_cohorts_zero_hazard_parity_and_mass_conservation(
    living_counts, quit_prob, switch_prob, duration
) -> None:
    initial = np.array([[*living_counts, 5.0]], dtype=float)
    stay = 1.0 - quit_prob - switch_prob
    transition = np.array(
        [
            [
                [1.0 - switch_prob, switch_prob, 0.0, 0.0, 0.0, 0.0],
                [0.0, stay, switch_prob, 0.0, quit_prob, 0.0],
                [0.0, 0.0, 1.0 - quit_prob, 0.0, quit_prob, 0.0],
                [0.0, switch_prob, 0.0, stay, quit_prob, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            ]
        ],
        dtype=float,
    )[None, ...]
    rates = np.array([[[[0.0, 0.0], [10.0, 0.0], [0.0, 5.0], [8.0, 3.0], [0.0, 0.0], [0.0, 0.0]]]])
    zero_hazards = np.zeros((1, 1, 5, 2), dtype=float)

    discrete = project_cohorts(
        initial_population=initial,
        transitions=transition,
        boundaries_years=[0.0, duration],
        consumption_rates=rates,
        cohort_ids=("c0",),
        product_units=("sticks", "ml"),
        policy_ids=("baseline",),
        assumption_id="zero_hazard_parity",
    )
    continuous = project_health_cohorts(
        initial_population=initial,
        survivor_transitions=transition,
        annual_hazards=zero_hazards,
        boundaries_years=[0.0, duration],
        consumption_rates=rates,
        cohort_ids=("c0",),
        product_units=("sticks", "ml"),
        policy_ids=("baseline",),
        assumption_id="zero_hazard_parity",
        cause_ids=("smoking_related", "background"),
    )

    np.testing.assert_allclose(continuous.population, discrete.population, rtol=1e-12, atol=1e-10)
    np.testing.assert_allclose(continuous.consumption, discrete.consumption, rtol=1e-12, atol=1e-10)
    assert float(continuous.population[-1].sum()) == pytest.approx(float(initial.sum()), rel=1e-12)

    survivor_matrix = {
        "smoking": {"smoking": 1.0 - quit_prob, "former": quit_prob},
        "former": {"smoking": 0.0, "former": 1.0},
    }
    positive_step = exposure_health_step(
        {"smoking": living_counts[1], "former": living_counts[4]},
        {"smoking": (0.04, 0.01), "former": (0.01, 0.01)},
        survivor_matrix,
        duration,
    )
    assert sum(positive_step.population.values()) + sum(positive_step.deaths) == pytest.approx(
        living_counts[1] + living_counts[4],
        rel=1e-12,
    )


@settings(max_examples=60, deadline=None, derandomize=True)
@given(
    st.floats(0.25, 0.45, allow_nan=False, allow_infinity=False),
    st.floats(0.65, 0.90, allow_nan=False, allow_infinity=False),
    st.floats(0.10, 0.25, allow_nan=False, allow_infinity=False),
    st.floats(0.45, 0.65, allow_nan=False, allow_infinity=False),
    st.floats(0.01, 0.04, allow_nan=False, allow_infinity=False),
)
def test_partial_identification_bounds_shrink_monotonically_under_tighter_inputs(
    total_low, total_high, lawful_low, lawful_high, shrink
) -> None:
    bias = Interval(0.95, 1.05)
    outer = restriction_bounds(
        Interval(total_low, total_high),
        Interval(lawful_low, lawful_high),
        total_bias=bias,
        lawful_bias=bias,
    )
    inner = restriction_bounds(
        Interval(total_low + shrink, total_high - shrink),
        Interval(lawful_low + shrink, lawful_high - shrink),
        total_bias=bias,
        lawful_bias=bias,
    )
    assert outer.feasible
    assert inner.feasible
    assert outer.quitting is not None
    assert inner.quitting is not None
    assert outer.switching is not None
    assert inner.switching is not None
    assert inner.quitting.lower >= outer.quitting.lower - 1e-12
    assert inner.quitting.upper <= outer.quitting.upper + 1e-12
    assert inner.switching.lower >= outer.switching.lower - 1e-12
    assert inner.switching.upper <= outer.switching.upper + 1e-12


@settings(max_examples=60, deadline=None, derandomize=True)
@given(
    st.lists(st.floats(-500.0, 500.0, allow_nan=False, allow_infinity=False), min_size=6, max_size=6),
    st.floats(0.55, 0.95, allow_nan=False, allow_infinity=False),
    st.floats(0.55, 0.95, allow_nan=False, allow_infinity=False),
)
def test_blackwell_garbling_cannot_increase_evsi_or_expected_information_gain(
    payoffs, sensitivity, garble_keep
) -> None:
    matrix = np.array(payoffs, dtype=float).reshape(3, 2)
    problem = DecisionProblem(matrix, ["status_quo", "intervene"], "nzd")
    informative = np.array(
        [
            [sensitivity, (1.0 - sensitivity) / 2.0, (1.0 - sensitivity) / 2.0],
            [(1.0 - sensitivity) / 2.0, sensitivity, (1.0 - sensitivity) / 2.0],
            [(1.0 - sensitivity) / 2.0, (1.0 - sensitivity) / 2.0, sensitivity],
        ],
        dtype=float,
    )
    garbling = np.array(
        [
            [garble_keep, (1.0 - garble_keep) / 2.0, (1.0 - garble_keep) / 2.0],
            [(1.0 - garble_keep) / 2.0, garble_keep, (1.0 - garble_keep) / 2.0],
            [(1.0 - garble_keep) / 2.0, (1.0 - garble_keep) / 2.0, garble_keep],
        ],
        dtype=float,
    )
    garbled = garbling @ informative
    targets = {"state": [0, 1, 2]}

    direct_report = evaluate(problem, informative, targets)
    garbled_report = evaluate(problem, garbled, targets)
    direct_eig = direct_report["targets"]["state"]["eig_nats"]
    garbled_eig = garbled_report["targets"]["state"]["eig_nats"]

    assert direct_report["evpi"] >= direct_report["evsi"] - 1e-12
    assert direct_report["evsi"] >= garbled_report["evsi"] - 1e-12
    assert direct_eig >= garbled_eig - 1e-12
