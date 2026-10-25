"""Cross-workstream regression contracts; all constructed amounts are test fixtures.

Tests exercise the real tobac and tobac_supply modules together. They do not
condition the research prior or qualify the scientific meaning of an observation.
"""
from dataclasses import replace

import numpy as np
import pytest
from scipy.special import logsumexp

from tobac._core import DecisionProblem
from tobac.evidence import (
    Belief, EvidencePacket, Scope, condition, incremental_value,
    prospective_value, state_identifiers,
)
from tobac.supply import expected_releases, release_loglikelihood
from tobac_supply.consumption_ledger import SupplyBasis, annualised_supply, lawful_ledger
from tobac_supply.longitudinal import continuous_correlation


@pytest.mark.parametrize('visitors', [-9., 0., 7.])
@pytest.mark.parametrize('illicit_share', [0., .25])
@pytest.mark.parametrize('stocks', [[20., 10., 15.], [10., 15., 20.]])
def test_accounting_roundtrip_uses_common_stock_and_flow_conventions(visitors, illicit_share, stocks):
    releases = np.array([100., 90.])
    u = np.array([3., 5.])
    v = np.full(2, visitors)
    ledger = lawful_ledger([2022, 2023], releases, stocks, unrecorded=u, net_visitors=v,
                           basis=SupplyBasis())
    # Hypothetical total and illicit share are supplied, not inferred from the ledger.
    total = ledger.consumption / (1-illicit_share)
    prediction = expected_releases(
        total, illicit_share, u+np.maximum(v, 0),
        stock_change=np.diff(ledger.stocks), outbound=np.maximum(-v, 0),
    )
    np.testing.assert_allclose(prediction, releases, rtol=1e-13, atol=1e-13)
    assert ledger.consumption.sum() == pytest.approx(
        releases.sum()+stocks[0]-stocks[-1]+u.sum()+v.sum())


def test_duty_free_absent_channel_translates_only_when_explicit():
    ledger = lawful_ledger([2023], [100.], [0., 0.], unrecorded=[3.],
                           duty_free_addition=[7.], basis=SupplyBasis(duty_free_included=False))
    prediction = expected_releases(ledger.consumption, 0.,
                                   ledger.unrecorded+ledger.duty_free_addition)
    np.testing.assert_allclose(prediction, ledger.releases)
    with pytest.raises(ValueError, match='double count'):
        lawful_ledger([2023], [100.], [0., 0.], duty_free_addition=[7.],
                      basis=SupplyBasis())


def test_reporting_bias_is_not_a_second_physical_consumption_adjustment():
    ledger = lawful_ledger([2023], [100.], [10., 5.], unrecorded=[2.],
                           basis=SupplyBasis())
    mean = expected_releases(ledger.consumption, 0., ledger.unrecorded,
                             stock_change=np.diff(ledger.stocks), reporting_multiplier=1.2)
    np.testing.assert_allclose(mean, [120.])
    np.testing.assert_allclose(ledger.consumption, [107.])


def test_period_allocation_matches_explicit_overlap_not_calendar_label():
    ledger = lawful_ledger([2023, 2024], [365., 732.], [0., 0., 0.],
                           basis=SupplyBasis())
    report = annualised_supply(ledger, '2023-07-01', '2024-07-01')
    assert report['covered_days'] == 366
    assert report['allocated_total'] == pytest.approx(184+2*182)
    assert report['annualised_per_365_days'] == pytest.approx((184+2*182)*365/366)
    assert report['allocation_is_observed'] is False
    assert report['unit'] == 'cigarette_equivalents/365_day_equivalent'


def fixture():
    # Supply uncertainty is crossed with an independent causal-response parameter.
    states = {'lawful_total': np.array([100., 100., 120., 120.]),
              'policy_effect': np.array([0., 1., 0., 1.])}
    ids = state_identifiers(states)
    scope = Scope('synthetic_NZ', 'synthetic_all_ages', '2023-01-01', '2024-01-01',
                  'cigarette_equivalents/calendar_year')
    values = np.array([[0., -1.], [0., 1.], [0., -1.], [0., 1.]])
    belief = Belief(DecisionProblem(values, ('retain', 'change'), 'test_units'), ids, scope)
    observed = lawful_ledger([2023], [100.], [0., 0.], basis=SupplyBasis()).releases
    expected = expected_releases(states['lawful_total'], 0., 0.)[:, None]
    logl = release_loglikelihood(observed, expected, [[100.]])
    packet = EvidencePacket('synthetic_release', ('test:MOH:2023',), ('test:sourceA',),
        ids, logl, scope, scope, 'synthetic_gaussian_releases_sd10')
    return states, belief, packet


def test_supplied_joint_likelihood_updates_once_without_learning_independent_policy_effect():
    states, prior, packet = fixture()
    after = condition(prior, packet)
    logw = np.log(prior.problem.prior_weights)+packet.log_likelihood
    expected = np.exp(logw-logsumexp(logw))
    np.testing.assert_allclose(after.problem.prior_weights, expected)
    assert after.problem.prior_weights[states['lawful_total'] == 100].sum() > .5
    assert after.problem.prior_weights[states['policy_effect'] == 1].sum() == pytest.approx(.5)
    np.testing.assert_array_equal(after.problem.values, prior.problem.values)
    assert after.state_ids == prior.state_ids
    assert after.used_data_ids == ('test:MOH:2023',)
    assert prior.used_data_ids == ()


def test_new_publication_does_not_make_old_data_new():
    _, prior, packet = fixture()
    after = condition(prior, packet)
    duplicate = replace(packet, evidence_id='other_paper', source_ids=('test:sourceB',),
                        dependence_note='Same source, not independent evidence.')
    with pytest.raises(ValueError, match='Underlying data reused'):
        condition(after, duplicate)
    with pytest.raises(ValueError, match='Underlying data reused'):
        prospective_value(after, np.ones((1, 4)), packet.data_ids)


@pytest.mark.parametrize('role', ['forecast', 'posterior', 'model_projection'])
def test_generated_longitudinal_outputs_cannot_be_new_observations(role):
    _, _, packet = fixture()
    with pytest.raises(ValueError, match='observed-data'):
        replace(packet, role=role)


def test_state_reordering_cannot_silently_change_the_physical_prior():
    _, prior, packet = fixture()
    with pytest.raises(ValueError, match='identities/order'):
        condition(prior, replace(packet, state_ids=tuple(reversed(packet.state_ids))))


def test_same_row_number_with_changed_physical_values_is_not_the_same_state():
    states, prior, packet = fixture()
    altered = dict(states, lawful_total=states['lawful_total']+1)
    with pytest.raises(ValueError, match='identities/order'):
        condition(prior, replace(packet, state_ids=state_identifiers(altered)))


def test_unknown_scope_conversion_does_not_pass_without_a_transport_model():
    _, _, packet = fixture()
    with pytest.raises(ValueError, match='transport'):
        replace(packet, source_scope=replace(packet.source_scope, unit='tonnes/year'))


def test_sequential_observations_need_an_explicit_dependence_model():
    _, prior, packet = fixture()
    after = condition(prior, packet)
    second = replace(packet, evidence_id='new_release', data_ids=('test:MOH:2024',))
    with pytest.raises(ValueError, match='conditional dependence'):
        condition(after, second)


def test_interperiod_error_is_joint_not_product_of_marginal_densities():
    _, prior, _ = fixture()
    observed = [100., 110.]
    expected = np.array([[100., 110.], [100., 110.], [120., 130.], [120., 130.]])
    covariance = 100*continuous_correlation([0., 365.], 365.)
    joint = release_loglikelihood(observed, expected, covariance)
    independent = sum(release_loglikelihood([observed[j]], expected[:, j:j+1], [[100.]])
                      for j in range(2))
    assert not np.allclose(joint, independent)
    w_joint = np.exp(joint-logsumexp(joint))
    w_independent = np.exp(independent-logsumexp(independent))
    assert not np.allclose(w_joint, w_independent)
    assert len(w_joint) == len(prior.state_ids)


def test_prospective_joint_value_chain_and_duplicate_report_identity():
    _, prior, _ = fixture()
    first = np.array([[.9, .6, .4, .1], [.1, .4, .6, .9]])
    second = np.array([[.8, .2, .8, .2], [.2, .8, .2, .8]])
    result = incremental_value(prior, first, second)
    assert result['chain_error'] < 1e-12
    assert result['expected_remaining_evpi'] == pytest.approx(
        result['initial_evpi']-result['first_evsi'])
    duplicate = np.zeros((2, 2, 4))
    for outcome in range(2):
        duplicate[outcome, outcome] = first[outcome]
    repeated = incremental_value(prior, first, joint=duplicate)
    assert repeated['expected_conditional_evsi'] == pytest.approx(0., abs=1e-12)
