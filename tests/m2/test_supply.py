import numpy as np
import pytest
from tobac.supply import expected_releases, release_loglikelihood

def test_supply_accounting_not_sales_equals_consumption():
    # total 100, illicit 20, lawful unrecorded 5: recorded consumption=75.
    assert expected_releases(np.array([100.]),.2,5.,10.,2.,3.)==pytest.approx([90.])

def test_stock_drawdown_and_multiplier():
    assert expected_releases(np.array([100.]),.2,5.,-10.,0.,0.,1.1)==pytest.approx([71.5])

@pytest.mark.parametrize('kwargs',[
 {'total':[-1.]},{'illicit_share':1.1},{'lawful_unrecorded':81.}, {'stock_change':-100.},
 {'reporting_multiplier':0.}, {'outbound':-1.}, {'wastage':-1.}, {'total':[np.nan]}])
def test_invalid_supply_inputs(kwargs):
    d=dict(total=np.array([100.]),illicit_share=.2,lawful_unrecorded=5.,stock_change=0.,outbound=0.,wastage=0.)
    d.update(kwargs)
    with pytest.raises(ValueError):expected_releases(**d)

def test_joint_likelihood_shared_error_and_missing_precision():
    means=np.array([[70.,80.],[90.,100.]])
    covariance=np.array([[4.,2.],[2.,4.]])
    logl=release_loglikelihood([70.,80.],means,covariance)
    assert logl[0]>logl[1]
    with pytest.raises(ValueError):release_loglikelihood([70.,80.],means,[[1.,2.],[2.,1.]])
    with pytest.raises(ValueError):release_loglikelihood([70.,80.],means,[[0.,0.],[0.,0.]])
    with pytest.raises(ValueError):release_loglikelihood([-1.,80.],means,covariance)
