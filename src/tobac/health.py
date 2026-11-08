"""Health accounting primitives for conditional policy scenarios."""

from math import exp, expm1, fsum, isclose, isfinite, log1p
from statistics import stdev
from typing import NamedTuple
lazy from collections.abc import Mapping

from scipy.linalg import expm


class IllnessDeathInterval(NamedTuple):
    """Expected counts and person-years for an irreversible diagnosis."""

    disease_free: float
    diagnosed: float
    disease_free_person_years: float
    diagnosed_person_years: float
    first_diagnoses: float
    deaths_before_diagnosis: float
    deaths_after_diagnosis: float
    surviving_first_diagnoses: float


def illness_death_interval(  # noqa: PLR0913 -- Keep each initial count, hazard and interval explicit.
    *,
    disease_free: float,
    diagnosed: float,
    incidence_hazard: float,
    disease_free_death_hazard: float,
    diagnosed_death_hazard: float,
    years: float,
) -> IllnessDeathInterval:
    """Advance living cohorts under constant annual hazards and no recovery."""
    inputs = (
        disease_free,
        diagnosed,
        incidence_hazard,
        disease_free_death_hazard,
        diagnosed_death_hazard,
        years,
    )
    if any(not isfinite(value) or value < 0 for value in inputs):
        msg = "Counts, hazards and years must be finite and nonnegative"
        raise ValueError(msg)

    # The last two rows integrate occupancy alongside the living states.
    generator = [
        [-(incidence_hazard + disease_free_death_hazard), 0, 0, 0],
        [incidence_hazard, -diagnosed_death_hazard, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    transition = expm([[rate * years for rate in row] for row in generator])
    free_end, diagnosed_end, free_years, diagnosed_years = map(
        float, transition @ [disease_free, diagnosed, 0, 0]
    )
    return IllnessDeathInterval(
        free_end,
        diagnosed_end,
        free_years,
        diagnosed_years,
        incidence_hazard * free_years,
        disease_free_death_hazard * free_years,
        diagnosed_death_hazard * diagnosed_years,
        float(transition[1, 0] * disease_free),
    )


class IllnessDeathHazards(NamedTuple):
    """Constant annual hazards and duration for one trajectory interval."""

    incidence: float
    disease_free_death: float
    diagnosed_death: float
    years: float


def illness_death_trajectory(
    disease_free: float,
    diagnosed: float,
    intervals: tuple[IllnessDeathHazards, ...],
) -> tuple[IllnessDeathInterval, ...]:
    """Carry the surviving cohort through successive hazard intervals."""
    trajectory: list[IllnessDeathInterval] = []
    for hazards in intervals:
        step = illness_death_interval(
            disease_free=disease_free,
            diagnosed=diagnosed,
            incidence_hazard=hazards.incidence,
            disease_free_death_hazard=hazards.disease_free_death,
            diagnosed_death_hazard=hazards.diagnosed_death,
            years=hazards.years,
        )
        trajectory.append(step)
        disease_free, diagnosed = step.disease_free, step.diagnosed
    return tuple(trajectory)


class MortalityInterval(NamedTuple):
    """Outcomes per entrant, with death probabilities in input cause order."""

    survival: float
    living_person_years: float
    death_probabilities: tuple[float, ...]


def competing_mortality(annual_hazards: tuple[float, ...], years: float) -> MortalityInterval:
    """Integrate constant, mutually exclusive cause hazards over an interval.

    Hazards are per living person-year. The caller supplies the cause
    partition and is responsible for its empirical qualification.
    """
    if not isfinite(years) or years < 0:
        msg = "Interval length must be finite and nonnegative"
        raise ValueError(msg)
    if any(not isfinite(rate) or rate < 0 for rate in annual_hazards):
        msg = "Annual hazards must be finite and nonnegative"
        raise ValueError(msg)

    total = fsum(annual_hazards)
    exposure = total * years
    if exposure == 0:
        return MortalityInterval(1.0, years, (0.0,) * len(annual_hazards))

    deaths = -expm1(-exposure)
    return MortalityInterval(
        exp(-exposure),
        deaths / total,
        tuple(deaths * (rate / total) for rate in annual_hazards),
    )


def mortality_trajectory(
    intervals: tuple[tuple[tuple[float, ...], float], ...],
) -> tuple[MortalityInterval, ...]:
    """Return interval outcomes per original entrant.

    Each input is a pair of annual cause hazards and interval duration.
    Supply the same causes in the same order in every interval. Each
    output contains end-of-interval survival, person-time accrued in
    that interval and cause-specific deaths during that interval.
    """
    if not intervals:
        return ()

    cause_count = len(intervals[0][0])
    entering = 1.0
    trajectory: list[MortalityInterval] = []
    for hazards, years in intervals:
        if len(hazards) != cause_count:
            msg = "Cause count must be consistent across intervals"
            raise ValueError(msg)
        result = competing_mortality(hazards, years)
        remaining = entering * result.survival
        trajectory.append(
            MortalityInterval(
                remaining,
                entering * result.living_person_years,
                tuple(entering * probability for probability in result.death_probabilities),
            )
        )
        entering = remaining
    return tuple(trajectory)


def discounted_qalys(
    trajectory: tuple[MortalityInterval, ...],
    utilities: tuple[float, ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> float:
    """Value living person-time per original entrant at supplied interval times.

    Utilities may be negative. The caller supplies the verified tariff
    and valuation timing relative to the analysis origin.
    """
    if not isfinite(annual_discount_rate) or annual_discount_rate < 0:
        msg = "Discount rate must be finite and nonnegative"
        raise ValueError(msg)

    terms: list[float] = []
    for interval, utility, year in zip(trajectory, utilities, valuation_years, strict=True):
        if not isfinite(utility):
            msg = "Utility must be finite"
            raise ValueError(msg)
        if not isfinite(year) or year < 0:
            msg = "Valuation year must be finite and nonnegative"
            raise ValueError(msg)
        person_years = interval.living_person_years
        if not isfinite(person_years) or person_years < 0:
            msg = "Living person-years must be finite and nonnegative"
            raise ValueError(msg)
        terms.append(person_years * utility * exp(-year * log1p(annual_discount_rate)))
    return fsum(terms)


def discounted_illness_death_qalys(
    trajectory: tuple[IllnessDeathInterval, ...],
    utilities: tuple[tuple[float, float], ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> float:
    """Value cohort person-time with disease-free and diagnosed utility pairs."""
    flows: list[float] = []
    for interval, (free_utility, diagnosed_utility) in zip(trajectory, utilities, strict=True):
        person_years = (interval.disease_free_person_years, interval.diagnosed_person_years)
        if any(not isfinite(years) or years < 0 for years in person_years):
            msg = "Living person-years must be finite and nonnegative"
            raise ValueError(msg)
        flows.append(person_years[0] * free_utility + person_years[1] * diagnosed_utility)
    return _discounted_flows(tuple(flows), valuation_years, annual_discount_rate)


def incremental_qalys(  # noqa: PLR0913, PLR0917 -- Preserve the paired scenario call signature.
    action_hazards: tuple[tuple[float, ...], ...],
    reference_hazards: tuple[tuple[float, ...], ...],
    interval_years: tuple[float, ...],
    action_utilities: tuple[float, ...],
    reference_utilities: tuple[float, ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> float:
    """Compare QALYs per entrant on a shared interval and valuation grid."""
    action = mortality_trajectory(tuple(zip(action_hazards, interval_years, strict=True)))
    reference = mortality_trajectory(tuple(zip(reference_hazards, interval_years, strict=True)))
    return discounted_qalys(
        action, action_utilities, valuation_years, annual_discount_rate
    ) - discounted_qalys(reference, reference_utilities, valuation_years, annual_discount_rate)


class PopulationQalyGain(NamedTuple):
    """Subgroup totals and their unweighted sum in QALYs."""

    by_group: dict[str, float]
    total: float


def aggregate_qaly_gains(
    per_entrant: Mapping[str, float],
    subgroup_sizes: Mapping[str, int],
    population_size: int,
) -> PopulationQalyGain:
    """Aggregate one caller-verified disjoint partition of the entrant population."""
    if per_entrant.keys() != subgroup_sizes.keys():
        msg = "Every population subgroup must have a QALY gain"
        raise ValueError(msg)
    if any(size < 0 for size in subgroup_sizes.values()) or (sum(subgroup_sizes.values()) != population_size):
        msg = "Subgroup sizes must reconcile to the entrant population"
        raise ValueError(msg)
    if any(not isfinite(gain) for gain in per_entrant.values()):
        msg = "Every subgroup QALY gain must be finite"
        raise ValueError(msg)

    totals = {group: per_entrant[group] * size for group, size in subgroup_sizes.items()}
    return PopulationQalyGain(totals, fsum(totals.values()))


def equity_weighted_qaly_score(
    gains: PopulationQalyGain,
    weights: Mapping[str, float],
) -> float:
    """Apply explicit normative weights to subgroup gains without rescaling them."""
    if gains.by_group.keys() != weights.keys():
        msg = "Equity weights must cover exactly the reported subgroups"
        raise ValueError(msg)
    if any(not isfinite(weight) or weight < 0 for weight in weights.values()):
        msg = "Equity weights must be finite and nonnegative"
        raise ValueError(msg)
    return fsum(gain * weights[group] for group, gain in gains.by_group.items())


def discounted_resource_cost(
    incremental_costs: tuple[float, ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> float:
    """Value incremental resource flows in one declared currency and price year.

    Supply resource costs for a single perspective. Track tax and other
    transfers in the fiscal accounts before constructing these inputs.
    """
    return _discounted_flows(incremental_costs, valuation_years, annual_discount_rate)


def _discounted_flows(
    flows: tuple[float, ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> float:
    if not isfinite(annual_discount_rate) or annual_discount_rate < 0:
        msg = "Discount rate must be finite and nonnegative"
        raise ValueError(msg)

    log_discount = log1p(annual_discount_rate)
    terms: list[float] = []
    for value, year in zip(flows, valuation_years, strict=True):
        if not isfinite(value):
            msg = "Discounted flow inputs must be finite"
            raise ValueError(msg)
        if not isfinite(year) or year < 0:
            msg = "Valuation year must be finite and nonnegative"
            raise ValueError(msg)
        terms.append(value * exp(-year * log_discount))
    return fsum(terms)


def discounted_tax_transfer(
    incremental_revenue: tuple[float, ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> tuple[float, float]:
    """Return government receipts and payer outflows as signed cash flows.

    Positive revenue is a government inflow and a payer outflow. Use
    one currency and price year. This identity leaves incidence and
    any collection costs to the caller.
    """
    receipts = discounted_resource_cost(incremental_revenue, valuation_years, annual_discount_rate)
    return receipts, -receipts


def _validate_state_population(population: Mapping[str, float]) -> None:
    if any(not isfinite(count) or count < 0 for count in population.values()):
        msg = "State populations must be finite and nonnegative"
        raise ValueError(msg)


def advance_exposure_states(
    population: Mapping[str, float],
    transitions: Mapping[str, Mapping[str, float]],
) -> dict[str, float]:
    """Move people between explicitly disjoint exposure states for one interval.

    Represent dual use as its own state. Each origin has a probability
    distribution over the same named destination states. Population
    entry, exit and mortality are outside this closed transition.
    """
    states = population.keys()
    if states != transitions.keys():
        msg = "Transition origins must match the population states"
        raise ValueError(msg)
    _validate_state_population(population)
    for row in transitions.values():
        if states != row.keys():
            msg = "Every transition row must cover the same destination states"
            raise ValueError(msg)
        if any(not isfinite(probability) or not 0 <= probability <= 1 for probability in row.values()):
            msg = "Transition probabilities must be finite and in [0, 1]"
            raise ValueError(msg)
        if not isclose(fsum(row.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
            msg = "Each origin's transition probabilities must sum to one"
            raise ValueError(msg)
    return {
        destination: fsum(count * transitions[origin][destination] for origin, count in population.items())
        for destination in states
    }


class ExposureHealthStep(NamedTuple):
    """End populations, living person-years by origin, and deaths by cause."""

    population: dict[str, float]
    living_person_years: dict[str, float]
    deaths: tuple[float, ...]


def exposure_health_step(
    population: Mapping[str, float],
    annual_hazards: Mapping[str, tuple[float, ...]],
    survivor_transitions: Mapping[str, Mapping[str, float]],
    years: float,
) -> ExposureHealthStep:
    """Apply origin-state mortality before survivors change state at the boundary."""
    if not population or population.keys() != annual_hazards.keys():
        msg = "Hazards must cover exactly the nonempty exposure partition"
        raise ValueError(msg)
    _validate_state_population(population)
    cause_count = len(next(iter(annual_hazards.values())))
    if any(len(hazards) != cause_count for hazards in annual_hazards.values()):
        msg = "Cause count must be consistent across exposure states"
        raise ValueError(msg)

    outcomes = {state: competing_mortality(hazards, years) for state, hazards in annual_hazards.items()}
    survivors = {state: count * outcomes[state].survival for state, count in population.items()}
    ending = advance_exposure_states(survivors, survivor_transitions)
    person_time = {state: count * outcomes[state].living_person_years for state, count in population.items()}
    deaths = tuple(
        fsum(count * outcomes[state].death_probabilities[cause] for state, count in population.items())
        for cause in range(cause_count)
    )
    return ExposureHealthStep(ending, person_time, deaths)


class ExposureInterval(NamedTuple):
    """Inputs to one interval with a common cause order across the schedule."""

    years: float
    annual_hazards: Mapping[str, tuple[float, ...]]
    survivor_transitions: Mapping[str, Mapping[str, float]]


def exposure_health_trajectory(
    initial_population: Mapping[str, float],
    intervals: tuple[ExposureInterval, ...],
) -> tuple[ExposureHealthStep, ...]:
    """Propagate only survivors across a closed cohort's exposure schedule."""
    _validate_state_population(initial_population)
    population = initial_population
    results: list[ExposureHealthStep] = []
    for interval in intervals:
        result = exposure_health_step(
            population, interval.annual_hazards, interval.survivor_transitions, interval.years
        )
        if results and len(result.deaths) != len(results[0].deaths):
            msg = "Cause count must be consistent across the exposure schedule"
            raise ValueError(msg)
        results.append(result)
        population = result.population
    return tuple(results)


def discounted_exposure_qalys(
    trajectory: tuple[ExposureHealthStep, ...],
    utilities: tuple[Mapping[str, float], ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> float:
    """Value total living person-time using the utility of each origin state."""
    interval_values: list[float] = []
    for step, state_utilities in zip(trajectory, utilities, strict=True):
        if step.living_person_years.keys() != state_utilities.keys():
            msg = "Utility inputs must match the origin states in each interval"
            raise ValueError(msg)
        if any(not isfinite(utility) for utility in state_utilities.values()):
            msg = "Utility must be finite"
            raise ValueError(msg)
        _validate_state_population(step.living_person_years)
        interval_values.append(
            fsum(years * state_utilities[state] for state, years in step.living_person_years.items())
        )
    return _discounted_flows(tuple(interval_values), valuation_years, annual_discount_rate)


def incremental_exposure_qalys(  # noqa: PLR0913, PLR0917 -- Preserve the paired scenario call signature.
    initial_population: Mapping[str, float],
    action: tuple[ExposureInterval, ...],
    reference: tuple[ExposureInterval, ...],
    utilities: tuple[Mapping[str, float], ...],
    valuation_years: tuple[float, ...],
    annual_discount_rate: float,
) -> float:
    """Compare exposure policies under a common state utility and time schedule."""
    if tuple(step.years for step in action) != tuple(step.years for step in reference):
        msg = "Action and reference must have the same interval durations"
        raise ValueError(msg)
    action_qalys = discounted_exposure_qalys(
        exposure_health_trajectory(initial_population, action),
        utilities,
        valuation_years,
        annual_discount_rate,
    )
    reference_qalys = discounted_exposure_qalys(
        exposure_health_trajectory(initial_population, reference),
        utilities,
        valuation_years,
        annual_discount_rate,
    )
    return action_qalys - reference_qalys


class PairedDrawSummary(NamedTuple):
    """Mean incremental outcome and simulation error on that mean."""

    draws: int
    mean_increment: float
    monte_carlo_standard_error: float


def summarize_paired_draws(
    action: Mapping[str, float],
    reference: Mapping[str, float],
) -> PairedDrawSummary:
    """Summarize equally weighted independent draws matched by shared draw ID."""
    minimum_draws = 2
    if action.keys() != reference.keys() or len(action) < minimum_draws:
        msg = "At least two matched action and reference draw IDs are required"
        raise ValueError(msg)
    differences = tuple(action[key] - reference[key] for key in sorted(action))
    if any(not isfinite(delta) for delta in differences):
        msg = "Paired outcome differences must be finite"
        raise ValueError(msg)
    count = len(differences)
    return PairedDrawSummary(count, fsum(differences) / count, stdev(differences) / count**0.5)
