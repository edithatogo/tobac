"""Reconciliation guards preserve source conflicts and physical measurement units."""
import copy
import importlib.util
import json
from decimal import Decimal
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def module():
    spec = importlib.util.spec_from_file_location('reconcile_products_2025', ROOT / 'scripts/reconcile_products_2025.py')
    assert spec and spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


@pytest.mark.parametrize('unit,value,expected,canonical', [('sticks','12','12','sticks'),('thousand_sticks','12','12000','sticks'),('kg','12','0.012','tonnes'),('tonnes','12','12','tonnes')])
def test_units_are_converted_without_mixing_count_and_mass(unit,value,expected,canonical):
    assert module().normalize(value,unit) == (Decimal(expected),canonical)


@pytest.mark.parametrize('value', ['NaN','Infinity','-Infinity','bad'])
def test_nonfinite_or_invalid_quantities_fail_closed(value):
    with pytest.raises(ValueError): module().normalize(value,'tonnes')


def test_signed_corrections_are_preserved():
    assert module().normalize('-3.22','thousand_sticks') == (Decimal('-3220'),'sticks')


def test_unknown_units_cannot_be_guessed():
    with pytest.raises(ValueError): module().normalize('12','packs')


def test_current_sources_are_accounted_for_without_claiming_national_closure():
    result = module().build_report(ROOT)
    assert result['source_asset_count'] == 9
    assert result['issuer_count'] == 8
    assert result['aggregate_reference_tonnes'] == '755'
    assert result['reconstructed_national_mass_tonnes'] is None
    assert result['aggregate_residual_tonnes'] is None
    assert result['national_cigarette_equivalents'] is None
    assert result['automatically_conditions_live_model'] is False
    assert result['measurement_parameters_changed'] is False
    rows = {r['id']:r for r in result['rows']}
    assert 'period_conflict' in rows['BAT-ryo-domestic']['issues']
    assert rows['BAT-ryo-domestic']['included_in_subtotals'] is False
    assert rows['BAT-ryo-domestic']['data_ids'] == []
    assert 'quantity_conflict' in rows['RS-cigarettes-table']['issues']
    assert rows['RS-cigarettes-table']['included_in_subtotals'] is False
    assert rows['PM-cigarettes-domestic']['normalized_quantity'] == '186440785'
    assert rows['PM-ryo-domestic']['normalized_quantity'] == '34.69953'
    assert rows['PM-ryo-domestic']['cigarette_equivalents'] is None
    assert rows['BAT-cigarettes-domestic']['cigarette_equivalents'] == '323408565'
    assert set(rows['BAT-cigarettes-domestic']['data_ids']) == set(rows['PM-ryo-domestic']['data_ids'])


def test_duplicate_rows_cannot_double_count_a_report():
    data=json.loads((ROOT/'integration/reconciliation_2025/product-extractions.json').read_text())
    data['rows'].append(copy.deepcopy(data['rows'][0]))
    with pytest.raises(ValueError,match='Duplicate'): module().reconcile(data)


def test_different_labels_do_not_allow_same_measure_twice():
    data=json.loads((ROOT/'integration/reconciliation_2025/product-extractions.json').read_text())
    extra=copy.deepcopy(data['rows'][0]);extra['id']='different-citation';data['rows'].append(extra)
    with pytest.raises(ValueError,match='Overlapping'): module().reconcile(data)


def test_absent_channel_or_quantity_is_not_zero():
    report=module().build_report(ROOT)
    row=next(r for r in report['rows'] if r['id']=='PM-ryo-duty-free')
    assert row['quantity'] is None and row['normalized_quantity'] is None
    assert not row['included_in_subtotals']


def test_ingredient_and_sales_mass_are_not_added_as_independent_supply():
    report=module().build_report(ROOT)
    for subtotal in report['subtotals']:
        assert subtotal['measure'] in {'sales_volume','ingredient_mass','additive_mass','all_product_mass'}
    assert report['cross_checks']['PM_RYO_gross_minus_additives_matches_sales'] is True


def test_unspecified_channels_cannot_be_added_beside_explicit_channel():
    data=json.loads((ROOT/'integration/reconciliation_2025/product-extractions.json').read_text())
    extra=copy.deepcopy(data['rows'][0]);extra.update(id='unlabelled-other-copy',channel='unspecified');data['rows'].append(extra)
    with pytest.raises(ValueError,match='Overlapping'): module().reconcile(data)


def test_source_asset_drift_fails_before_reconciliation(tmp_path):
    import shutil
    folder=tmp_path/'integration/reconciliation_2025';folder.mkdir(parents=True)
    shutil.copyfile(ROOT/'integration/reconciliation_2025/extraction-receipt.json',folder/'extraction-receipt.json')
    for name in ('product-extractions.json','source-assets.json','tobac-products-2025.yml'):
        shutil.copyfile(ROOT/'integration/reconciliation_2025'/name,folder/name)
    (folder/'product-extractions.json').write_text('{}')
    with pytest.raises(ValueError,match='hash mismatch'): module().build_report(tmp_path)


def test_reported_quantities_are_not_changed_by_rounding_or_component_errors():
    data=json.loads((ROOT/'integration/reconciliation_2025/product-extractions.json').read_text())
    data['rows'][0]['quantity']='323408566'
    with pytest.raises(ValueError,match='component sum'): module().reconcile(data)
