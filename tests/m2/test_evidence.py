from dataclasses import replace
import numpy as np
import pytest
from tobac._core import DecisionProblem
from tobac.evidence import Belief, EvidencePacket, Scope, condition, predictive, incremental_value

SCOPE=Scope('example catchment','adult residents','2025-01-01','2025-12-31','cigarette_equivalents/1000/day')

def belief():
    return Belief(DecisionProblem(np.array([[2.,0.],[0.,2.]]),('a','b'),'u'),('s0','s1'),SCOPE)

def packet(logl=np.log([.8,.2]), **kw):
    d=dict(evidence_id='e1',data_ids=('data1',),source_ids=('paper1',),state_ids=('s0','s1'),
           log_likelihood=logl,source_scope=SCOPE,target_scope=SCOPE,likelihood_model='binary fixture',
           role='observation',transport_note='',dependence_note='one joint observation')
    d.update(kw);return EvidencePacket(**d)

def test_update_and_predictive():
    b=condition(belief(),packet())
    assert b.problem.prior_weights==pytest.approx([.8,.2])
    assert b.used_data_ids==('data1',)
    assert predictive(b,np.array([[.8,.2],[.2,.8]]))==pytest.approx([.68,.32])
    assert b.receipts[0]['log_predictive_density']==pytest.approx(np.log(.5))

def test_reordered_states_are_rejected_not_silently_joined():
    with pytest.raises(ValueError,match='state'):condition(belief(),packet(state_ids=('s1','s0')))

def test_duplicate_underlying_data_with_new_citation_rejected():
    b=condition(belief(),packet())
    with pytest.raises(ValueError,match='reused'):condition(b,packet(evidence_id='e2',source_ids=('review',)))

@pytest.mark.parametrize('role',['forecast','posterior','scenario',''])
def test_nonobservations_rejected(role):
    with pytest.raises(ValueError):condition(belief(),packet(role=role))

@pytest.mark.parametrize('updates',[
 {'data_ids':()}, {'data_ids':('x','x')}, {'source_ids':()}, {'likelihood_model':''},
 {'log_likelihood':np.array([np.nan,0.])}, {'log_likelihood':np.array([np.inf,0.])},
 {'state_ids':('x','x')}, {'log_likelihood':np.array([0.])}])
def test_malformed_evidence_rejected(updates):
    with pytest.raises(ValueError):condition(belief(),packet(**updates))

def test_stable_underflow_and_density_above_one():
    b=condition(belief(),packet(logl=np.array([-10000.,-10001.])))
    assert b.problem.prior_weights[0]==pytest.approx(1/(1+np.exp(-1)))
    c=condition(belief(),packet(logl=np.array([3.,3.])))
    assert c.receipts[0]['log_predictive_density']==pytest.approx(3.)

def test_zero_support_evidence_rejected():
    with pytest.raises(ValueError,match='support'):condition(belief(),packet(logl=np.array([-np.inf,-np.inf])))

def test_source_context_change_requires_explicit_transport():
    old=replace(SCOPE,start='2022-01-01',end='2022-12-31')
    with pytest.raises(ValueError,match='transport'):condition(belief(),packet(source_scope=old))
    b=condition(belief(),packet(source_scope=old,transport_note='assumed stable; sensitivity required'))
    assert len(b.receipts)==1

def test_target_mismatch_rejected_even_with_transport_note():
    other=replace(SCOPE,geography='different population')
    with pytest.raises(ValueError,match='target'):condition(belief(),packet(target_scope=other,transport_note='note'))

def test_chained_updates_require_declared_conditional_dependence():
    b=condition(belief(),packet())
    with pytest.raises(ValueError,match='dependence'):
        condition(b,packet(evidence_id='e2',data_ids=('data2',),dependence_note=''))

def test_expected_increment_equals_joint_minus_first():
    b=belief();first=np.array([[.8,.2],[.2,.8]]);second=np.array([[.9,.1],[.1,.9]])
    r=incremental_value(b,first,second)
    assert r['expected_conditional_evsi']==pytest.approx(r['joint_evsi']-r['first_evsi'])
    assert r['chain_error']<1e-12
    assert r['expected_remaining_evpi']==pytest.approx(r['initial_evpi']-r['first_evsi'])

def test_realised_extra_value_need_not_equal_preposterior_increment():
    b=condition(belief(),packet(logl=np.log([.99,.01])))
    from tobac.information import evaluate
    assert evaluate(b.problem,np.array([[.8,.2],[.2,.8]]))['evsi']==pytest.approx(0,abs=1e-12)

def test_joint_conditional_input_supports_dependent_reports():
    b=belief();first=np.array([[.8,.2],[.2,.8]])
    # Re-reading the same report provides no information, unlike an independent repeat.
    joint=np.zeros((2,2,2));joint[0,0]=first[0];joint[1,1]=first[1]
    r=incremental_value(b,first,joint=joint)
    assert r['expected_conditional_evsi']==pytest.approx(0,abs=1e-12)
    with pytest.raises(ValueError):incremental_value(b,first,joint=joint*.8)

def test_scope_dates_and_fields():
    with pytest.raises(ValueError):replace(SCOPE,start='2026-02-02')
    with pytest.raises(ValueError):replace(SCOPE,unit='')

def test_state_identifiers_bind_values_not_only_row_positions():
    from tobac.evidence import state_identifiers
    a={'tobacco':np.array([1.,2.]),'share':np.array([.1,.2])}
    ids=state_identifiers(a)
    assert ids==state_identifiers(dict(reversed(list(a.items()))))
    b={k:v.copy() for k,v in a.items()};b['share'][0]=.3
    assert ids[0]!=state_identifiers(b)[0]
    with pytest.raises(ValueError):state_identifiers({'x':np.array([1.,1.])})

def test_used_data_cannot_be_resold_as_a_future_study():
    from tobac.evidence import prospective_value
    b=condition(belief(),packet())
    with pytest.raises(ValueError,match='reused'):
        prospective_value(b,np.ones((1,2)),('data1',))
    assert prospective_value(b,np.ones((1,2)),('new-data',))['evsi']==pytest.approx(0)
