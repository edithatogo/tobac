"""Cross-workstream regression contracts; all constructed amounts are test fixtures.

Tests exercise the real tobac and tobac_supply modules together. They do not
condition the research prior or qualify the scientific meaning of an observation.
"""

from dataclasses import replace
from datetime import date
from math import exp, log

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.special import logsumexp

from tobac._core import BiomarkerParameters, Catchment, DecisionProblem, Exposure, predict_signals
from tobac.evidence import (
    Belief,
    EvidencePacket,
    Scope,
    condition,
    incremental_value,
    prospective_value,
    state_identifiers,
)
from tobac.health import (
    ExposureInterval,
    IllnessDeathHazards,
    advance_exposure_states,
    aggregate_qaly_gains,
    discounted_exposure_qalys,
    discounted_illness_death_qalys,
    discounted_resource_cost,
    discounted_tax_transfer,
    equity_weighted_qaly_score,
    exposure_health_step,
    exposure_health_trajectory,
    illness_death_interval,
    illness_death_trajectory,
    incremental_exposure_qalys,
    incremental_qalys,
    mortality_trajectory,
    summarize_paired_draws,
)
from tobac.regulation import (
    cohort_initiation_response,
    cohort_restriction_applies,
    expected_enforcement_seizures,
    expected_flagged_pack_share,
    nicotine_standard_exposure,
)
from tobac.supply import expected_releases, release_loglikelihood
from tobac_supply.consumption_ledger import (
    SupplyBasis,
    annualised_supply,
    excise_price_response,
    excise_receipts,
    lawful_ledger,
)
from tobac_supply.longitudinal import continuous_correlation


@pytest.mark.parametrize("visitors", [-9.0, 0.0, 7.0])
@pytest.mark.parametrize("illicit_share", [0.0, 0.25])
@pytest.mark.parametrize("stocks", [[20.0, 10.0, 15.0], [10.0, 15.0, 20.0]])
def test_accounting_roundtrip_uses_common_stock_and_flow_conventions(visitors, illicit_share, stocks) -> None:
    releases = np.array([100.0, 90.0])
    u = np.array([3.0, 5.0])
    v = np.full(2, visitors)
    ledger = lawful_ledger([2022, 2023], releases, stocks, unrecorded=u, net_visitors=v, basis=SupplyBasis())
    # Hypothetical total and illicit share are supplied, not inferred from the ledger.
    total = ledger.consumption / (1 - illicit_share)
    prediction = expected_releases(
        total,
        illicit_share,
        u + np.maximum(v, 0),
        stock_change=np.diff(ledger.stocks),
        outbound=np.maximum(-v, 0),
    )
    np.testing.assert_allclose(prediction, releases, rtol=1e-13, atol=1e-13)
    assert ledger.consumption.sum() == pytest.approx(
        releases.sum() + stocks[0] - stocks[-1] + u.sum() + v.sum()
    )


def test_duty_free_absent_channel_translates_only_when_explicit() -> None:
    ledger = lawful_ledger(
        [2023],
        [100.0],
        [0.0, 0.0],
        unrecorded=[3.0],
        duty_free_addition=[7.0],
        basis=SupplyBasis(duty_free_included=False),
    )
    prediction = expected_releases(ledger.consumption, 0.0, ledger.unrecorded + ledger.duty_free_addition)
    np.testing.assert_allclose(prediction, ledger.releases)
    with pytest.raises(ValueError, match="double count"):
        lawful_ledger([2023], [100.0], [0.0, 0.0], duty_free_addition=[7.0], basis=SupplyBasis())


def test_reporting_bias_is_not_a_second_physical_consumption_adjustment() -> None:
    ledger = lawful_ledger([2023], [100.0], [10.0, 5.0], unrecorded=[2.0], basis=SupplyBasis())
    mean = expected_releases(
        ledger.consumption,
        0.0,
        ledger.unrecorded,
        stock_change=np.diff(ledger.stocks),
        reporting_multiplier=1.2,
    )
    np.testing.assert_allclose(mean, [120.0])
    np.testing.assert_allclose(ledger.consumption, [107.0])


def test_period_allocation_matches_explicit_overlap_not_calendar_label() -> None:
    ledger = lawful_ledger([2023, 2024], [365.0, 732.0], [0.0, 0.0, 0.0], basis=SupplyBasis())
    report = annualised_supply(ledger, "2023-07-01", "2024-07-01")
    assert report["covered_days"] == 366
    assert report["allocated_total"] == pytest.approx(184 + 2 * 182)
    assert report["annualised_per_365_days"] == pytest.approx((184 + 2 * 182) * 365 / 366)
    assert report["allocation_is_observed"] is False
    assert report["unit"] == "cigarette_equivalents/365_day_equivalent"


def fixture():
    # Supply uncertainty is crossed with an independent causal-response parameter.
    states = {
        "lawful_total": np.array([100.0, 100.0, 120.0, 120.0]),
        "policy_effect": np.array([0.0, 1.0, 0.0, 1.0]),
    }
    ids = state_identifiers(states)
    scope = Scope(
        "synthetic_NZ",
        "synthetic_all_ages",
        "2023-01-01",
        "2024-01-01",
        "cigarette_equivalents/calendar_year",
    )
    values = np.array([[0.0, -1.0], [0.0, 1.0], [0.0, -1.0], [0.0, 1.0]])
    belief = Belief(DecisionProblem(values, ("retain", "change"), "test_units"), ids, scope)
    observed = lawful_ledger([2023], [100.0], [0.0, 0.0], basis=SupplyBasis()).releases
    expected = expected_releases(states["lawful_total"], 0.0, 0.0)[:, None]
    logl = release_loglikelihood(observed, expected, [[100.0]])
    packet = EvidencePacket(
        "synthetic_release",
        ("test:MOH:2023",),
        ("test:sourceA",),
        ids,
        logl,
        scope,
        scope,
        "synthetic_gaussian_releases_sd10",
    )
    return states, belief, packet


def test_supplied_joint_likelihood_updates_once_without_learning_independent_policy_effect() -> None:
    states, prior, packet = fixture()
    after = condition(prior, packet)
    logw = np.log(prior.problem.prior_weights) + packet.log_likelihood
    expected = np.exp(logw - logsumexp(logw))
    np.testing.assert_allclose(after.problem.prior_weights, expected)
    assert after.problem.prior_weights[states["lawful_total"] == 100].sum() > 0.5
    assert after.problem.prior_weights[states["policy_effect"] == 1].sum() == pytest.approx(0.5)
    np.testing.assert_array_equal(after.problem.values, prior.problem.values)
    assert after.state_ids == prior.state_ids
    assert after.used_data_ids == ("test:MOH:2023",)
    assert prior.used_data_ids == ()


def test_new_publication_does_not_make_old_data_new() -> None:
    _, prior, packet = fixture()
    after = condition(prior, packet)
    duplicate = replace(
        packet,
        evidence_id="other_paper",
        source_ids=("test:sourceB",),
        dependence_note="Same source, not independent evidence.",
    )
    with pytest.raises(ValueError, match="Underlying data reused"):
        condition(after, duplicate)
    with pytest.raises(ValueError, match="Underlying data reused"):
        prospective_value(after, np.ones((1, 4)), packet.data_ids)


@pytest.mark.parametrize("role", ["forecast", "posterior", "model_projection"])
def test_generated_longitudinal_outputs_cannot_be_new_observations(role) -> None:
    _, _, packet = fixture()
    with pytest.raises(ValueError, match="observed-data"):
        replace(packet, role=role)


def test_state_reordering_cannot_silently_change_the_physical_prior() -> None:
    _, prior, packet = fixture()
    with pytest.raises(ValueError, match="identities/order"):
        condition(prior, replace(packet, state_ids=tuple(reversed(packet.state_ids))))


def test_same_row_number_with_changed_physical_values_is_not_the_same_state() -> None:
    states, prior, packet = fixture()
    altered = dict(states, lawful_total=states["lawful_total"] + 1)
    with pytest.raises(ValueError, match="identities/order"):
        condition(prior, replace(packet, state_ids=state_identifiers(altered)))


def test_unknown_scope_conversion_does_not_pass_without_a_transport_model() -> None:
    _, _, packet = fixture()
    with pytest.raises(ValueError, match="transport"):
        replace(packet, source_scope=replace(packet.source_scope, unit="tonnes/year"))


def test_sequential_observations_need_an_explicit_dependence_model() -> None:
    _, prior, packet = fixture()
    after = condition(prior, packet)
    second = replace(packet, evidence_id="new_release", data_ids=("test:MOH:2024",))
    with pytest.raises(ValueError, match="conditional dependence"):
        condition(after, second)


def test_interperiod_error_is_joint_not_product_of_marginal_densities() -> None:
    _, prior, _ = fixture()
    observed = [100.0, 110.0]
    expected = np.array([[100.0, 110.0], [100.0, 110.0], [120.0, 130.0], [120.0, 130.0]])
    covariance = 100 * continuous_correlation([0.0, 365.0], 365.0)
    joint = release_loglikelihood(observed, expected, covariance)
    independent = sum(
        release_loglikelihood([observed[j]], expected[:, j : j + 1], [[100.0]]) for j in range(2)
    )
    assert not np.allclose(joint, independent)
    w_joint = np.exp(joint - logsumexp(joint))
    w_independent = np.exp(independent - logsumexp(independent))
    assert not np.allclose(w_joint, w_independent)
    assert len(w_joint) == len(prior.state_ids)


def test_prospective_joint_value_chain_and_duplicate_report_identity() -> None:
    _, prior, _ = fixture()
    first = np.array([[0.9, 0.6, 0.4, 0.1], [0.1, 0.4, 0.6, 0.9]])
    second = np.array([[0.8, 0.2, 0.8, 0.2], [0.2, 0.8, 0.2, 0.8]])
    result = incremental_value(prior, first, second)
    assert result["chain_error"] < 1e-12
    assert result["expected_remaining_evpi"] == pytest.approx(result["initial_evpi"] - result["first_evsi"])
    duplicate = np.zeros((2, 2, 4))
    for outcome in range(2):
        duplicate[outcome, outcome] = first[outcome]
    repeated = incremental_value(prior, first, joint=duplicate)
    assert repeated["expected_conditional_evsi"] == pytest.approx(0.0, abs=1e-12)


def test_health_comparison_accrues_only_surviving_person_time() -> None:
    action = ((0.0, 0.0), (0.0, 0.0))
    reference = ((log(2), 0.0), (0.0, log(2) / 2))
    durations = (1.0, 2.0)
    first, second = mortality_trajectory(tuple(zip(reference, durations, strict=True)))

    assert first.death_probabilities == pytest.approx((0.5, 0.0))
    assert second.death_probabilities == pytest.approx((0.0, 0.25))
    assert second.survival == pytest.approx(0.25)

    # Half of the initial cohort enters the second interval. Both
    # intervals halve their entrants, and the second lasts twice as long.
    utility = (1.0, -0.5)
    reference_value = 0.5 / log(2) - 0.25 / (log(2) * 1.05)
    action_value = 1.0 - 1.0 / 1.05
    assert incremental_qalys(
        action, reference, durations, utility, utility, (0.0, 1.0), 0.05
    ) == pytest.approx(action_value - reference_value)


def test_equity_weights_apply_to_subgroup_totals_and_preserve_losses() -> None:
    gains = aggregate_qaly_gains({"a": 0.5, "b": -0.25}, {"a": 10, "b": 8}, 18)

    assert gains.by_group == {"a": 5.0, "b": -2.0}
    assert equity_weighted_qaly_score(gains, {"a": 1.0, "b": 1.0}) == gains.total
    assert equity_weighted_qaly_score(gains, {"a": 1.0, "b": 3.0}) == -1.0
    with pytest.raises(ValueError, match="exactly"):
        equity_weighted_qaly_score(gains, {"a": 1.0})


def test_tax_transfer_cancels_without_erasing_resource_cost() -> None:
    years = (0.0, 1.0)
    discount = 0.10
    resource_cost = discounted_resource_cost((100.0, -55.0), years, discount)
    government_receipts, payer_flow = discounted_tax_transfer((66.0, 22.0), years, discount)

    assert resource_cost == pytest.approx(50.0)
    assert government_receipts == pytest.approx(86.0)
    assert payer_flow == pytest.approx(-86.0)
    assert resource_cost - government_receipts - payer_flow == pytest.approx(50.0)


def test_excise_change_uses_scenario_taxable_releases() -> None:
    reference = excise_receipts(100.0, 2.0)
    action = excise_receipts(70.0, 2.5)
    assert discounted_tax_transfer((action - reference,), (0.0,), 0.0) == (-25.0, 25.0)
    assert excise_receipts(0.0, 2.5) == 0.0
    with pytest.raises(ValueError, match="Taxable releases"):
        excise_receipts(-1.0, 2.5)


@pytest.mark.parametrize(
    ("pass_through", "expected_price", "expected_quantity"),
    [
        (0.0, 10.0, 100.0),
        (1.5, 20.0, 50.0),
    ],
)
def test_excise_price_response_supports_null_and_overshifting(
    pass_through: float, expected_price: float, expected_quantity: float
) -> None:
    assert excise_price_response(
        baseline_price=10.0,
        baseline_consumption=100.0,
        duty_change_per_unit=20.0 / 3,
        pass_through=pass_through,
        own_price_elasticity=-1.0,
    ) == pytest.approx((expected_price, expected_quantity))


def test_excise_cross_price_effect_can_offset_own_price_response() -> None:
    assert excise_price_response(
        baseline_price=10.0,
        baseline_consumption=100.0,
        duty_change_per_unit=10.0,
        pass_through=1.0,
        own_price_elasticity=-1.0,
        cross_price_changes=((5.0, 20.0, 0.5),),
    ) == pytest.approx((20.0, 100.0))


def test_exposure_transition_keeps_dual_users_and_relapse_in_the_partition() -> None:
    population = {"smoking": 80.0, "dual": 10.0, "former": 10.0}
    transitions = {
        "former": {"former": 0.5, "dual": 0.0, "smoking": 0.5},
        "dual": {"former": 0.0, "dual": 1.0, "smoking": 0.0},
        "smoking": {"former": 0.125, "dual": 0.125, "smoking": 0.75},
    }
    result = advance_exposure_states(population, transitions)
    assert result == {"smoking": 65.0, "dual": 20.0, "former": 15.0}
    with pytest.raises(ValueError, match="sum to one"):
        advance_exposure_states(population, transitions | {"former": transitions["former"] | {"former": 0.0}})


def test_exposure_health_step_switches_survivors_only() -> None:
    result = exposure_health_step(
        {"smoking": 100.0, "former": 10.0},
        {"smoking": (log(2),), "former": (0.0,)},
        {
            "smoking": {"smoking": 0.0, "former": 1.0},
            "former": {"smoking": 0.0, "former": 1.0},
        },
        1.0,
    )
    assert result.population == {"smoking": 0.0, "former": 60.0}
    assert result.deaths == (50.0,)
    assert result.living_person_years == pytest.approx({"smoking": 50.0 / log(2), "former": 10.0})


def test_exposure_health_step_rejects_invalid_counts_before_mortality() -> None:
    with pytest.raises(ValueError, match="State populations"):
        exposure_health_step(
            {"smoking": -1.0},
            {"smoking": (1_000.0,)},
            {"smoking": {"smoking": 1.0}},
            1.0,
        )


def test_exposure_trajectory_uses_destination_hazards_in_next_interval() -> None:
    quit_at_boundary = {
        "smoking": {"smoking": 0.0, "former": 1.0},
        "former": {"smoking": 0.0, "former": 1.0},
    }
    hazards = {"smoking": (log(2), 0.0), "former": (0.0, log(2) / 2)}
    first, second = exposure_health_trajectory(
        {"smoking": 100.0, "former": 0.0},
        (
            ExposureInterval(1.0, hazards, quit_at_boundary),
            ExposureInterval(2.0, hazards, quit_at_boundary),
        ),
    )
    assert first.deaths == pytest.approx((50.0, 0.0))
    assert second.deaths == pytest.approx((0.0, 25.0))
    assert second.population == pytest.approx({"smoking": 0.0, "former": 25.0})
    assert second.living_person_years["former"] == pytest.approx(50.0 / log(2))


def test_exposure_qalys_follow_utility_of_state_when_person_time_accrues() -> None:
    transition = {"smoking": {"smoking": 0.0, "former": 1.0}, "former": {"smoking": 0.0, "former": 1.0}}
    hazards = {"smoking": (log(2),), "former": (0.0,)}
    schedule = (ExposureInterval(1.0, hazards, transition),) * 2
    trajectory = exposure_health_trajectory({"smoking": 100.0, "former": 0.0}, schedule)
    utilities = ({"smoking": -0.5, "former": 1.0},) * 2

    assert discounted_exposure_qalys(trajectory, utilities, (0.0, 1.0), 0.25) == pytest.approx(
        -25.0 / log(2) + 40.0
    )
    with pytest.raises(ValueError, match="origin states"):
        discounted_exposure_qalys(trajectory, ({"former": 1.0},) * 2, (0.0, 1.0), 0.25)


def test_paired_exposure_qalys_compare_quitting_with_persistent_smoking() -> None:
    population = {"smoking": 100.0, "former": 0.0}
    hazards = {"smoking": (log(2),), "former": (0.0,)}
    stay = {"smoking": {"smoking": 1.0, "former": 0.0}, "former": {"smoking": 0.0, "former": 1.0}}
    quit_smoking = stay | {"smoking": {"smoking": 0.0, "former": 1.0}}
    interval = ExposureInterval(1.0, hazards, stay)
    reference = (interval, interval)
    action = (ExposureInterval(1.0, hazards, quit_smoking), interval)
    utilities = ({"smoking": 0.8, "former": 1.0},) * 2

    expected_gain = (50.0 - 20.0 / log(2)) / 1.05
    assert incremental_exposure_qalys(
        population, action, reference, utilities, (0.0, 1.0), 0.05
    ) == pytest.approx(expected_gain)
    with pytest.raises(ValueError, match="same interval durations"):
        incremental_exposure_qalys(
            population, action, (interval, interval._replace(years=2.0)), utilities, (0.0, 1.0), 0.05
        )


def test_paired_exposure_policy_reconciles_subgroup_and_population_qalys() -> None:
    hazards = {"smoking": (0.0,), "former": (0.0,)}
    stay = {
        "smoking": {"smoking": 1.0, "former": 0.0},
        "former": {"smoking": 0.0, "former": 1.0},
    }
    quit_half = stay | {"smoking": {"smoking": 0.5, "former": 0.5}}
    baseline = ExposureInterval(1.0, hazards, stay)
    reference = (baseline, baseline)
    action = (ExposureInterval(1.0, hazards, quit_half), baseline)
    utilities = ({"smoking": 0.5, "former": 1.0},) * 2

    subgroup_sizes = {"a": 20, "b": 80}
    population = {"a": {"smoking": 1.0, "former": 0.0}, "b": {"smoking": 0.25, "former": 0.75}}
    per_entrant = {
        group: incremental_exposure_qalys(entrants, action, reference, utilities, (0.0, 1.0), 0.0)
        for group, entrants in population.items()
    }
    gains = aggregate_qaly_gains(per_entrant, subgroup_sizes, 100)
    pooled = incremental_exposure_qalys(
        {"smoking": 40.0, "former": 60.0}, action, reference, utilities, (0.0, 1.0), 0.0
    )

    assert gains.by_group == {"a": 5.0, "b": 5.0}
    assert gains.total == pooled == 10.0
    assert equity_weighted_qaly_score(gains, {"a": 2.0, "b": 1.0}) == 15.0


def test_cohort_restriction_checks_birth_and_commencement_boundaries() -> None:
    rule = {
        "first_covered_birth_date": date(2010, 1, 1),
        "commencement_date": date(2030, 1, 1),
    }
    assert cohort_restriction_applies(birth_date=date(2010, 1, 1), observation_date=date(2030, 1, 1), **rule)
    assert not cohort_restriction_applies(
        birth_date=date(2009, 12, 31), observation_date=date(2030, 1, 1), **rule
    )
    assert not cohort_restriction_applies(
        birth_date=date(2010, 1, 1), observation_date=date(2029, 12, 31), **rule
    )


def test_cohort_initiation_response_retains_prevented_initiators() -> None:
    applies = cohort_restriction_applies(
        birth_date=date(2010, 1, 1),
        observation_date=date(2030, 1, 1),
        first_covered_birth_date=date(2010, 1, 1),
        commencement_date=date(2030, 1, 1),
    )
    initiation, stay = cohort_initiation_response(
        baseline_initiation=0.2,
        baseline_stay_never=0.7,
        prevented_fraction=0.5,
        restriction_applies=applies,
    )
    result = advance_exposure_states(
        {"never": 100.0, "smoking": 20.0, "other": 0.0},
        {
            "never": {"never": stay, "smoking": initiation, "other": 0.1},
            "smoking": {"never": 0.0, "smoking": 1.0, "other": 0.0},
            "other": {"never": 0.0, "smoking": 0.0, "other": 1.0},
        },
    )
    assert result == pytest.approx({"never": 80.0, "smoking": 30.0, "other": 10.0})


def test_nicotine_standard_changes_nicotine_signal_at_fixed_consumption() -> None:
    exposure = Exposure(100.0, 0.2, 0.0, 0.0, nicotine_dose_mg_per_cigarette=1.0)
    scenario = nicotine_standard_exposure(exposure, compliant_consumption_share=0.5, compliant_dose_mg=0.2)
    catchment = Catchment(1_000.0, 100_000.0)
    parameters = BiomarkerParameters()
    baseline = predict_signals(exposure, catchment, parameters)
    outcome = predict_signals(scenario, catchment, parameters)
    assert outcome["nicotine_equivalent_ng_l"] == pytest.approx(0.6 * baseline["nicotine_equivalent_ng_l"])
    assert {k: v for k, v in outcome.items() if k != "nicotine_equivalent_ng_l"} == {
        k: v for k, v in baseline.items() if k != "nicotine_equivalent_ng_l"
    }


def test_seizures_can_rise_when_attempted_supply_falls() -> None:
    reference = expected_enforcement_seizures(1_000.0, 0.1, 0.5)
    action = expected_enforcement_seizures(500.0, 0.4, 0.5)
    assert reference == 50.0
    assert action == 100.0
    assert expected_enforcement_seizures(500.0, 0.0, 0.5) == 0.0
    with pytest.raises(ValueError, match="probabilities"):
        expected_enforcement_seizures(500.0, 0.4, 1.1)


def test_paired_draw_summary_removes_shared_variation_before_estimating_error() -> None:
    summary = summarize_paired_draws({"a": 1.0, "b": 103.0}, {"b": 100.0, "a": 0.0})
    assert summary == pytest.approx((2, 2.0, 1.0))
    with pytest.raises(ValueError, match="matched"):
        summarize_paired_draws({"a": 1.0, "b": 2.0}, {"a": 1.0, "c": 2.0})


def test_paired_exposure_draws_recover_analytic_mean_and_simulation_error() -> None:
    population = {"smoking": 100.0, "former": 0.0}
    hazards = {"smoking": (0.0,), "former": (0.0,)}
    stay = {
        "smoking": {"smoking": 1.0, "former": 0.0},
        "former": {"smoking": 0.0, "former": 1.0},
    }
    baseline = ExposureInterval(1.0, hazards, stay)
    utilities = ({"smoking": 0.5, "former": 1.0},) * 2
    reference = discounted_exposure_qalys(
        exposure_health_trajectory(population, (baseline, baseline)), utilities, (0.0, 1.0), 0.0
    )
    actions = {}
    for draw, quit_share in (("a", 0.0), ("b", 0.5), ("c", 1.0)):
        transition = stay | {"smoking": {"smoking": 1.0 - quit_share, "former": quit_share}}
        schedule = (ExposureInterval(1.0, hazards, transition), baseline)
        actions[draw] = discounted_exposure_qalys(
            exposure_health_trajectory(population, schedule), utilities, (0.0, 1.0), 0.0
        )

    assert summarize_paired_draws(actions, dict.fromkeys(actions, reference)) == pytest.approx(
        (3, 25.0, 25.0 / 3**0.5)
    )


def test_illness_death_counts_diagnosis_followed_by_death_in_same_interval():
    hazard = log(2)
    result = illness_death_interval(
        disease_free=100,
        diagnosed=20,
        incidence_hazard=hazard,
        disease_free_death_hazard=0,
        diagnosed_death_hazard=hazard,
        years=1,
    )
    assert result.disease_free == pytest.approx(50)
    assert result.diagnosed == pytest.approx(10 + 50 * hazard)
    assert result.surviving_first_diagnoses == pytest.approx(50 * hazard)
    assert result.first_diagnoses == pytest.approx(50)
    assert result.deaths_before_diagnosis == 0
    assert result.deaths_after_diagnosis == pytest.approx(10 + 50 * (1 - hazard))
    assert result.disease_free_person_years == pytest.approx(50 / hazard)
    assert result.diagnosed_person_years == pytest.approx((10 + 50 * (1 - hazard)) / hazard)


def test_illness_death_matches_integrated_incidence_with_unequal_hazards():
    result = illness_death_interval(
        disease_free=120,
        diagnosed=30,
        incidence_hazard=0.15,
        disease_free_death_hazard=0.04,
        diagnosed_death_hazard=0.29,
        years=3,
    )

    def surviving_incident_cases(time):
        return quad(
            lambda diagnosis_time: 18 * exp(-0.19 * diagnosis_time) * exp(-0.29 * (time - diagnosis_time)),
            0,
            time,
        )[0]

    expected_diagnosed_years = quad(
        lambda time: 30 * exp(-0.29 * time) + surviving_incident_cases(time),
        0,
        3,
    )[0]
    assert result.surviving_first_diagnoses == pytest.approx(surviving_incident_cases(3))
    assert result.diagnosed_person_years == pytest.approx(expected_diagnosed_years)
    assert (
        result.disease_free
        + result.diagnosed
        + result.deaths_before_diagnosis
        + result.deaths_after_diagnosis
    ) == pytest.approx(150)


def test_excise_price_response_applies_cumulative_share_of_eventual_pass_through():
    parameters = {
        "baseline_price": 10,
        "baseline_consumption": 100,
        "duty_change_per_unit": 2,
        "pass_through": 1.5,
        "own_price_elasticity": -1,
    }
    assert excise_price_response(**parameters, realised_share=0) == (10, 100)
    assert excise_price_response(**parameters, realised_share=0.5) == pytest.approx((11.5, 1000 / 11.5))
    assert excise_price_response(**parameters) == pytest.approx((13, 1000 / 13))
    with pytest.raises(ValueError, match="Realised pass-through share"):
        excise_price_response(**parameters, realised_share=1.01)


def test_illness_death_qalys_value_each_living_state_at_the_supplied_year():
    result = illness_death_interval(
        disease_free=120,
        diagnosed=30,
        incidence_hazard=0,
        disease_free_death_hazard=0,
        diagnosed_death_hazard=0,
        years=2,
    )
    assert discounted_illness_death_qalys((result,), ((0.8, -0.1),), (1,), 0.05) == pytest.approx(
        (240 * 0.8 - 60 * 0.1) / 1.05
    )


def test_illness_death_trajectory_carries_diagnoses_into_later_mortality():
    first, second = illness_death_trajectory(
        100,
        0,
        (IllnessDeathHazards(log(2), 0, 0, 1), IllnessDeathHazards(0, 0, log(2), 1)),
    )
    assert first.first_diagnoses == pytest.approx(50)
    assert second.first_diagnoses == 0
    assert second.disease_free == pytest.approx(50)
    assert second.diagnosed == pytest.approx(25)
    assert second.deaths_after_diagnosis == pytest.approx(25)


def test_pack_observation_separates_sampling_from_classification():
    assert expected_flagged_pack_share(
        illicit_pack_share=0.2,
        illicit_sampling_probability=0.5,
        legal_sampling_probability=0.25,
        sensitivity=0.9,
        specificity=0.95,
    ) == pytest.approx(1 / 3)
    with pytest.raises(ValueError, match="positive sampling probability"):
        expected_flagged_pack_share(
            illicit_pack_share=0,
            illicit_sampling_probability=1,
            legal_sampling_probability=0,
            sensitivity=1,
            specificity=1,
        )
