"""Small deterministic reference for time-varying tobacco/nicotine cohorts.

This is an exploratory closed-cohort projection, not a fitted population model.
Rows of each supplied transition matrix are origins; columns are destinations.
The discrete reference applies transitions at the end of each interval and
consumption uses opening-state occupancy and a supplied rate per person-year.
The opt-in health projection instead integrates living person-time under
supplied origin-state hazards, then applies survivor transitions at the boundary.
Changing interval length therefore requires new transition probabilities; this
module never rescales probabilities or infers them from prevalence snapshots.

There is no evidence conditioning, policy optimisation, supply-origin inference,
birth/migration process, causal-effect estimation or health-outcome valuation.
The existing evidence interface and lawful-consumption ledger retain those roles.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum
from typing import cast

import numpy as np
from numpy.typing import ArrayLike, NDArray

from tobac.health import ExposureHealthStep, exposure_health_step

STATES = ("never_use", "smoking_only", "vaping_only", "dual_use", "former_use", "dead")
PRODUCTS = ("smoked_tobacco", "vaping")
FloatArray = NDArray[np.float64]
PROBABILITY_TOLERANCE = 1e-12


@dataclass(frozen=True)
class Projection:
    """Expected people at boundaries and product amounts within intervals.

    Shapes are (boundary, cohort, state) and (interval, cohort, product).
    Product units are deliberately separate: their amounts must not be summed
    across products without an explicit, scientifically justified conversion.
    Arrays are defensive, read-only copies; the result contains no observed data.
    """

    boundaries_years: FloatArray
    population: FloatArray
    consumption: FloatArray
    cohort_ids: tuple[str, ...]
    product_units: tuple[str, str]
    policy_ids: tuple[str, ...]
    assumption_id: str


@dataclass(frozen=True)
class HealthProjection(Projection):
    """Projection with mortality-integrated origin-state consumption.

    ``living_person_years`` has shape (interval, cohort, living state), using
    ``STATES[:-1]`` in order. ``deaths`` has shape (interval, cohort, cause),
    using ``cause_ids``. Deaths accumulate in the final boundary-population
    state and do not accrue person-time or consumption. Mortality is applied
    once, before the surviving people change exposure state at the boundary.
    Hazards and rates are supplied assumptions, not fitted tobacco effects.
    """

    living_person_years: FloatArray
    deaths: FloatArray
    cause_ids: tuple[str, ...]


def _numbers(values: ArrayLike, name: str) -> FloatArray:
    # Inspect before NumPy can silently turn mixed numeric/boolean lists into 0/1.
    if any(isinstance(value, (bool, np.bool_)) for value in np.asarray(values, dtype=object).flat):
        msg = f"{name} must contain real numeric values, not booleans or strings"
        raise ValueError(msg)
    array = np.asarray(values)
    if array.dtype.kind not in "iuf":
        msg = f"{name} must contain real numeric values, not booleans or strings"
        raise ValueError(msg)
    result = np.array(array, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(result)):
        msg = f"{name} must contain only finite values"
        raise ValueError(msg)
    return result


def _labels(values: tuple[str, ...], name: str, *, unique: bool = False) -> None:
    if not isinstance(cast("object", values), tuple) or not values:
        msg = f"{name} must be a nonempty tuple"
        raise ValueError(msg)
    if any(
        not isinstance(cast("object", value), str) or not value.strip() or value != value.strip()
        for value in values
    ):
        msg = f"{name} requires nonempty, whitespace-trimmed strings"
        raise ValueError(msg)
    if unique and len(set(values)) != len(values):
        msg = f"{name} must be unique"
        raise ValueError(msg)


def _readonly(array: FloatArray) -> FloatArray:
    array.setflags(write=False)
    return array


def _validate_transitions(transition: FloatArray) -> None:
    if np.any(transition < 0) or np.any(transition > 1):
        msg = "transitions must lie in [0, 1]"
        raise ValueError(msg)
    if not np.allclose(transition.sum(axis=-1), 1, atol=PROBABILITY_TOLERANCE, rtol=0):
        msg = "every transition row must sum to one; probabilities are never normalised"
        raise ValueError(msg)
    absorbing = np.eye(len(STATES))[-1]
    if np.any(transition[:, :, -1, :] != absorbing):
        msg = "dead must be exactly absorbing"
        raise ValueError(msg)
    if np.any(transition[:, :, 1:, 0] != 0):
        msg = "ever-users cannot transition back to never_use"
        raise ValueError(msg)


def _projection_inputs(  # noqa: PLR0913  # Shared explicit axes preserve both timing contracts.
    *,
    initial_population: ArrayLike,
    transitions: ArrayLike,
    boundaries_years: ArrayLike,
    consumption_rates: ArrayLike,
    cohort_ids: tuple[str, ...],
    product_units: tuple[str, str],
    policy_ids: tuple[str, ...],
    assumption_id: str,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Validate the common population, boundary, state and product contract."""
    _labels(cohort_ids, "cohort_ids", unique=True)
    _labels(product_units, "product_units")
    _labels(policy_ids, "policy_ids")
    _labels((assumption_id,), "assumption_id")
    if len(product_units) != len(PRODUCTS):
        msg = "product_units must declare one unit for each of smoked_tobacco and vaping"
        raise ValueError(msg)
    initial = _numbers(initial_population, "initial_population")
    transition = _numbers(transitions, "transitions")
    boundaries = _numbers(boundaries_years, "boundaries_years")
    rates = _numbers(consumption_rates, "consumption_rates")
    n_cohorts, n_states = len(cohort_ids), len(STATES)
    n_intervals = len(policy_ids)
    shapes = (
        (initial, (n_cohorts, n_states), "initial_population"),
        (transition, (n_intervals, n_cohorts, n_states, n_states), "transitions"),
        (boundaries, (n_intervals + 1,), "boundaries_years"),
        (rates, (n_intervals, n_cohorts, n_states, len(PRODUCTS)), "consumption_rates"),
    )
    for array, expected, name in shapes:
        if array.shape != expected:
            msg = f"{name} must have shape {expected}; got {array.shape}"
            raise ValueError(msg)
    durations = np.diff(boundaries)
    if not np.all(np.isfinite(durations)) or np.any(durations <= 0):
        msg = "boundaries_years must define finite, strictly positive intervals"
        raise ValueError(msg)
    if np.any(initial < 0) or np.any(rates < 0):
        msg = "initial_population and consumption_rates must be nonnegative"
        raise ValueError(msg)
    _validate_transitions(transition)
    allowed_rates = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0, 0], [0, 0]], dtype=bool)
    if np.any(rates[:, :, ~allowed_rates] != 0):
        msg = "consumption_rates conflict with the declared smoking/vaping state"
        raise ValueError(msg)
    return initial, transition, boundaries, rates


def project_cohorts(  # noqa: PLR0913  # Explicit axes and units prevent silent scope assumptions.
    *,
    initial_population: ArrayLike,
    transitions: ArrayLike,
    boundaries_years: ArrayLike,
    consumption_rates: ArrayLike,
    cohort_ids: tuple[str, ...],
    product_units: tuple[str, str],
    policy_ids: tuple[str, ...],
    assumption_id: str,
) -> Projection:
    """Project supplied policy schedules without fitting or conditioning evidence.

    ``initial_population`` has shape (cohort, 6); ``transitions`` has shape
    (interval, cohort, 6, 6). Every row is a probability distribution. Cohorts
    must be mutually exclusive; overlapping NZHS ethnicity aggregates cannot
    be used as an additive population partition. Death is absorbing and people
    who have used a product cannot return to the never-use state.

    ``boundaries_years`` gives strictly increasing elapsed/calendar year values.
    ``consumption_rates`` has shape (interval, cohort, 6, 2) in the declared
    product units per person-year. Only smoking-only/dual-use states can consume
    smoked tobacco and only vaping-only/dual-use states can consume vaping.
    Consumption uses opening occupancy for the entire interval, including for
    people whose supplied transition leads to death at the interval boundary.
    No broadcasting, probability normalisation or unit conversion is implicit.
    Policy labels record supplied scenarios; they do not establish causal effects.
    """
    initial, transition, boundaries, rates = _projection_inputs(
        initial_population=initial_population,
        transitions=transitions,
        boundaries_years=boundaries_years,
        consumption_rates=consumption_rates,
        cohort_ids=cohort_ids,
        product_units=product_units,
        policy_ids=policy_ids,
        assumption_id=assumption_id,
    )
    n_intervals, n_cohorts, n_states = transition.shape[:3]
    durations = np.diff(boundaries)

    population = np.empty((n_intervals + 1, n_cohorts, n_states), dtype=np.float64)
    consumption = np.empty((n_intervals, n_cohorts, len(PRODUCTS)), dtype=np.float64)
    population[0] = initial
    try:
        with np.errstate(over="raise", invalid="raise"):
            for interval, duration in enumerate(durations):
                consumption[interval] = (
                    np.einsum("cs,csp->cp", population[interval], rates[interval]) * duration
                )
                population[interval + 1] = np.einsum("cs,csd->cd", population[interval], transition[interval])
    except FloatingPointError as exc:
        msg = "projection overflowed; inputs must produce finite population and consumption"
        raise ValueError(msg) from exc
    if not np.all(np.isfinite(population)) or not np.all(np.isfinite(consumption)):
        msg = "projection overflowed; inputs must produce finite population and consumption"
        raise ValueError(msg)
    return Projection(
        _readonly(boundaries),
        _readonly(population),
        _readonly(consumption),
        cohort_ids,
        product_units,
        policy_ids,
        assumption_id,
    )


def _health_step(
    population: FloatArray, hazards: FloatArray, transition: FloatArray, years: float
) -> ExposureHealthStep:
    """Use the shared health primitive with the explicit living-state partition."""
    living_states = STATES[:-1]
    return exposure_health_step(
        {state: float(population[index]) for index, state in enumerate(living_states)},
        {state: tuple(map(float, hazards[index])) for index, state in enumerate(living_states)},
        {
            state: {
                destination: float(transition[origin, target])
                for target, destination in enumerate(living_states)
            }
            for origin, state in enumerate(living_states)
        },
        years,
    )


def project_health_cohorts(  # noqa: PLR0913  # Explicit hazards, identities and units prevent silent conversions.
    *,
    initial_population: ArrayLike,
    survivor_transitions: ArrayLike,
    annual_hazards: ArrayLike,
    boundaries_years: ArrayLike,
    consumption_rates: ArrayLike,
    cohort_ids: tuple[str, ...],
    product_units: tuple[str, str],
    policy_ids: tuple[str, ...],
    assumption_id: str,
    cause_ids: tuple[str, ...],
) -> HealthProjection:
    """Integrate mortality and consumption before boundary exposure transitions.

    Population, boundaries, product rates and metadata follow ``project_cohorts``.
    ``survivor_transitions`` has shape (interval, cohort, 6, 6), with no living
    state transitioning to death: mortality is supplied only through hazards.
    ``annual_hazards`` has shape (interval, cohort, 5, cause), in the living-state
    order ``STATES[:-1]`` and the explicit, unique ``cause_ids`` order. Causes
    must be mutually exclusive. Each hazard is constant within its interval,
    per living person-year; it is not an interval probability.

    Origin-state living person-time determines product amounts. Only survivors
    switch at the boundary, so a new state's hazard and rate apply next interval.
    Initially dead people remain dead. Under zero hazards this agrees with the
    original discrete reference when its matrices have no transitions to death.
    A discrete projection that already applies death must not be used as this
    function's transition schedule. Neither method infers hazards or effects
    from prevalence; disease history, utility and valuation remain separate.
    """
    initial, transition, boundaries, rates = _projection_inputs(
        initial_population=initial_population,
        transitions=survivor_transitions,
        boundaries_years=boundaries_years,
        consumption_rates=consumption_rates,
        cohort_ids=cohort_ids,
        product_units=product_units,
        policy_ids=policy_ids,
        assumption_id=assumption_id,
    )
    _labels(cause_ids, "cause_ids", unique=True)
    hazards = _numbers(annual_hazards, "annual_hazards")
    n_intervals, n_cohorts, n_states = transition.shape[:3]
    expected = (n_intervals, n_cohorts, n_states - 1, len(cause_ids))
    if hazards.shape != expected:
        msg = f"annual_hazards must have shape {expected}; got {hazards.shape}"
        raise ValueError(msg)
    if np.any(hazards < 0):
        msg = "annual_hazards must be nonnegative"
        raise ValueError(msg)
    if np.any(transition[:, :, :-1, -1] != 0):
        msg = "mortality must be supplied only through hazards, not survivor_transitions"
        raise ValueError(msg)

    population = np.empty((n_intervals + 1, n_cohorts, n_states), dtype=np.float64)
    consumption = np.empty((n_intervals, n_cohorts, len(PRODUCTS)), dtype=np.float64)
    person_time = np.empty((n_intervals, n_cohorts, n_states - 1), dtype=np.float64)
    deaths = np.empty((n_intervals, n_cohorts, len(cause_ids)), dtype=np.float64)
    population[0] = initial
    try:
        with np.errstate(over="raise", invalid="raise"):
            for interval, duration in enumerate(np.diff(boundaries)):
                for cohort in range(n_cohorts):
                    step = _health_step(
                        population[interval, cohort],
                        hazards[interval, cohort],
                        transition[interval, cohort],
                        float(duration),
                    )
                    population[interval + 1, cohort, :-1] = [step.population[state] for state in STATES[:-1]]
                    population[interval + 1, cohort, -1] = population[interval, cohort, -1] + fsum(
                        step.deaths
                    )
                    person_time[interval, cohort] = [step.living_person_years[state] for state in STATES[:-1]]
                    deaths[interval, cohort] = step.deaths
                    consumption[interval, cohort] = np.einsum(
                        "s,sp->p", person_time[interval, cohort], rates[interval, cohort, :-1]
                    )
    except (FloatingPointError, OverflowError) as exc:
        msg = "health projection overflowed; inputs must produce finite outcomes"
        raise ValueError(msg) from exc
    if any(not np.all(np.isfinite(array)) for array in (population, consumption, person_time, deaths)):
        msg = "health projection overflowed; inputs must produce finite outcomes"
        raise ValueError(msg)
    return HealthProjection(
        _readonly(boundaries),
        _readonly(population),
        _readonly(consumption),
        cohort_ids,
        product_units,
        policy_ids,
        assumption_id,
        _readonly(person_time),
        _readonly(deaths),
        cause_ids,
    )
