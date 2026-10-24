"""Accounting invariants for the explicit lawful-consumption bridge."""
import importlib.util
import numpy as np
import pytest

@pytest.fixture
def module():
    spec=importlib.util.find_spec('tobac_supply.consumption_ledger')
    assert spec is not None, 'consumption ledger implementation is missing'
    from tobac_supply import consumption_ledger
    return consumption_ledger


def test_inventory_conservation(module):
    ledger=module.lawful_ledger([2022,2023],[100.,80.],[20.,10.,15.])
    np.testing.assert_allclose(ledger.consumption,[110.,75.])
    assert ledger.consumption.sum()==100+80+20-15


def test_visitors_and_missing_channel_are_signed_separate(module):
    x=module.lawful_ledger([2023],[100.],[0.,0.],unrecorded=[5.],net_visitors=[-8.])
    assert x.consumption[0]==97.


def test_no_double_count_duty_free(module):
    with pytest.raises(ValueError,match='duty.free'):
        module.lawful_ledger([2023],[100.],[0.,0.],duty_free_addition=[1.])


def test_duty_free_can_be_explicitly_absent(module):
    basis=module.SupplyBasis(duty_free_included=False)
    x=module.lawful_ledger([2023],[100.],[0.,0.],duty_free_addition=[1.],basis=basis)
    assert x.consumption[0]==101.

@pytest.mark.parametrize('kwargs',[
 {'years':[2023,2023], 'releases':[1,1], 'stocks':[0,0,0]},
 {'years':[2021,2023], 'releases':[1,1], 'stocks':[0,0,0]},
 {'years':[True], 'releases':[1], 'stocks':[0,0]},
 {'years':[2023], 'releases':[1], 'stocks':[0,-1]},
 {'years':[2023], 'releases':[1], 'stocks':[0,2]},
 {'years':[2023], 'releases':[float('nan')], 'stocks':[0,0]},
 {'years':[2023], 'releases':[1], 'stocks':[0]},
 {'years':[], 'releases':[], 'stocks':[0]},
])
def test_invalid_ledger_rejected(module,kwargs):
    with pytest.raises(ValueError): module.lawful_ledger(**kwargs)


def test_incompatible_mass_units_rejected(module):
    with pytest.raises(ValueError,match='unit'):
        module.SupplyBasis(unit='tonnes')


def test_annualised_period_alignment_leap_year(module):
    x=module.lawful_ledger([2023,2024],[365.,732.],[0,0,0])
    y=module.annualised_supply(x,'2023-07-01','2024-07-01')
    assert y['covered_days']==366
    assert y['value']==pytest.approx((184+182*2)/366*365)
    assert y['allocation_is_observed'] is False


def test_no_missing_year_imputation(module):
    x=module.lawful_ledger([2023],[100.],[0,0])
    with pytest.raises(ValueError,match='Missing'):
        module.annualised_supply(x,'2022-07-01','2023-07-01')


def test_proportional_stock_scenario_telescopes(module):
    stocks=module.stock_scenario([100.,80.,60.],30.)
    x=module.lawful_ledger([2021,2022,2023],[100.,80.,60.],stocks)
    assert x.consumption.sum()==pytest.approx(240+stocks[0]-stocks[-1])


def test_zero_adjustments_preserve_releases(module):
    x=module.lawful_ledger([2023],[10.],[0,0])
    np.testing.assert_array_equal(x.consumption,x.releases)


def test_basis_rejects_missing_scope(module):
    with pytest.raises(ValueError): module.SupplyBasis(geography='')
    with pytest.raises(ValueError): module.SupplyBasis(duty_free_included='yes')


def test_bad_adjustment_shapes_and_metadata(module):
    with pytest.raises(ValueError):module.lawful_ledger([2023],[100],[0,0],unrecorded=[])
    with pytest.raises(ValueError):module.stock_scenario([],2)
    with pytest.raises(ValueError):module.stock_scenario([1],-1)
    with pytest.raises(ValueError):module.SupplyBasis(products='')
    with pytest.raises(ValueError):module.lawful_ledger([2023],[100],[0,0],basis='tonnes')
