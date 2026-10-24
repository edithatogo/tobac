import numpy as np
import pytest
from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
from tobac.information import evaluate, joint_likelihood, lognormal_bins, scalar_oracle, same_data_robustness


def problem():
    return DecisionProblem(np.array([[0., 2.], [2., 0.]]), ('a','b'), 'illustrative loss units')


def test_perfect_and_uninformative():
    p=problem()
    assert evaluate(p,np.eye(2),{'truth':[0,1]})['evsi']==pytest.approx(1)
    r=evaluate(p,np.ones((1,2)),{'truth':[0,1]})
    assert r['evsi']==pytest.approx(0)
    assert r['targets']['truth']['eig_nats']==pytest.approx(0)
    assert r['posterior_martingale_max_error'] < 1e-12


def test_exact_noisy_binary():
    p=problem();l=np.array([[.8,.2],[.2,.8]])
    r=evaluate(p,l,{'truth':[0,1]},event=np.array([False,True]),confidence=.75)
    assert r['evsi']==pytest.approx(.6)
    assert r['probability_action_changes']==pytest.approx(.5)
    assert r['targets']['truth']['eig_nats']==pytest.approx(np.log(2)+.8*np.log(.8)+.2*np.log(.2))
    assert r['resolution_probability']==pytest.approx(1)
    assert r['correct_resolution_probability']==pytest.approx(.8)
    assert r['event_brier_risk']==pytest.approx(.16)
    assert scalar_oracle(p,l)==pytest.approx(r['evsi'])


def test_scientific_gain_without_decision_value():
    p=DecisionProblem(np.array([[1.,0.],[1.,0.]]),('a','b'),'units')
    r=evaluate(p,np.eye(2),{'truth':[0,1]})
    assert r['evsi']==pytest.approx(0)
    assert r['targets']['truth']['eig_nats']==pytest.approx(np.log(2))


def test_cross_targets_do_not_receive_independent_information():
    p=DecisionProblem(np.array([[0.,2.],[2.,0.],[0.,2.],[2.,0.]]),('a','b'),'units')
    l=np.array([[.9,.9,.1,.1],[.1,.1,.9,.9]])
    r=evaluate(p,l,{'signal':[0,0,1,1],'unrelated':[0,1,0,1]})
    assert r['evsi']==pytest.approx(0)
    assert r['targets']['unrelated']['eig_nats']==pytest.approx(0,abs=1e-12)
    assert r['targets']['signal']['eig_nats']>0


def test_zero_mass_states_and_impossible_outcomes():
    p=DecisionProblem(np.array([[0.,2.],[2.,0.]]),('a','b'),'units',np.array([1.,0.]))
    l=np.array([[1.,0.],[0.,1.],[0.,0.]])
    r=evaluate(p,l,{'truth':[0,1]})
    assert r['evsi']==pytest.approx(0)
    assert r['targets']['truth']['eig_nats']==pytest.approx(0)


@pytest.mark.parametrize('l',[np.array([[1.,.8]]),np.array([[1.,-1.],[0.,2.]]),np.array([[1.,np.nan]]),np.ones((2,3))])
def test_invalid_likelihood_rejected(l):
    with pytest.raises(ValueError):evaluate(problem(),l)


def test_joint_likelihood_and_diminishing_uncertainty():
    l=np.array([[.8,.2],[.2,.8]])
    joined=joint_likelihood(l,l)
    assert joined.shape==(4,2)
    assert np.allclose(joined.sum(0),1)
    assert evaluate(problem(),joined)['evsi']>=evaluate(problem(),l)['evsi']-1e-12
    assert evaluate(problem(),joined)['evsi']<=exact_evpi(problem())+1e-12


def test_lognormal_bins_censoring_and_refinement():
    med=np.array([1.,3.,9.])
    coarse=lognormal_bins(med,.3,[3.,6.])
    fine=lognormal_bins(med,.3,[1.,3.,6.])
    assert np.allclose(fine[:2].sum(0),coarse[0])
    assert np.allclose(fine.sum(0),1)
    p=DecisionProblem(np.array([[0.,1.],[0.,.5],[1.,0.]]),('a','b'),'u')
    assert evaluate(p,fine)['evsi']>=evaluate(p,coarse)['evsi']-1e-12


@pytest.mark.parametrize('sd,cuts',[(0,[1]),(.2,[0]),(.2,[2,1]),(.2,[1,1])])
def test_invalid_bins_rejected(sd,cuts):
    with pytest.raises(ValueError):lognormal_bins(np.array([1.,2.]),sd,cuts)


def test_shift_and_uniform_replication_invariance():
    p=problem();l=np.array([[.8,.2],[.2,.8]])
    expected=evaluate(p,l)['evsi']
    shift=DecisionProblem(p.values+1e10,p.action_names,p.value_unit)
    assert evaluate(shift,l)['evsi']==pytest.approx(expected)
    duplicate=DecisionProblem(np.repeat(p.values,2,axis=0),p.action_names,p.value_unit)
    assert evaluate(duplicate,np.repeat(l,2,axis=1))['evsi']==pytest.approx(expected)


def test_grouped_partial_information():
    p=DecisionProblem(np.array([[0.,1.],[0.,1.],[1.,0.],[1.,0.]]),('a','b'),'u')
    assert exact_partial_information(p,[0,0,1,1])==pytest.approx(.5)
    assert exact_partial_information(p,[0,1,0,1])==pytest.approx(0)


def test_same_data_robustness_uses_common_reference_distribution():
    l=np.eye(2)
    r=same_data_robustness(problem().values,[np.array([.2,.8]),np.array([.8,.2])],np.array([.5,.5]),l,np.array([0,1],bool))
    assert r['expected_probability_range']==pytest.approx(0)
    assert r['decision_agreement_probability']==pytest.approx(1)
    assert r['confident_agreement_probability']==pytest.approx(1)
