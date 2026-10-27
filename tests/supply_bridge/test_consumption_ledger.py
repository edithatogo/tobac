"""Accounting invariants for the explicit lawful-consumption bridge."""

import importlib.util

import numpy as np
import pytest


@pytest.fixture
def module():
    spec = importlib.util.find_spec("tobac_supply.consumption_ledger")
    assert spec is not None, "consumption ledger implementation is missing"
    from tobac_supply import consumption_ledger  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    return consumption_ledger


def test_inventory_conservation(module) -> None:
    ledger = module.lawful_ledger([2022, 2023], [100.0, 80.0], [20.0, 10.0, 15.0], basis=module.SupplyBasis())
    np.testing.assert_allclose(ledger.consumption, [110.0, 75.0])
    assert ledger.consumption.sum() == 100 + 80 + 20 - 15


def test_visitors_and_missing_channel_are_signed_separate(module) -> None:
    x = module.lawful_ledger(
        [2023], [100.0], [0.0, 0.0], unrecorded=[5.0], net_visitors=[-8.0], basis=module.SupplyBasis()
    )
    assert x.consumption[0] == 97.0


def test_no_double_count_duty_free(module) -> None:
    with pytest.raises(ValueError, match=r"duty.free"):
        module.lawful_ledger(
            [2023], [100.0], [0.0, 0.0], duty_free_addition=[1.0], basis=module.SupplyBasis()
        )


def test_duty_free_can_be_explicitly_absent(module) -> None:
    basis = module.SupplyBasis(duty_free_included=False)
    x = module.lawful_ledger([2023], [100.0], [0.0, 0.0], duty_free_addition=[1.0], basis=basis)
    assert x.consumption[0] == 101.0


@pytest.mark.parametrize(
    "kwargs",
    [
        {"years": [2023, 2023], "releases": [1, 1], "stocks": [0, 0, 0]},
        {"years": [2021, 2023], "releases": [1, 1], "stocks": [0, 0, 0]},
        {"years": [True], "releases": [1], "stocks": [0, 0]},
        {"years": [2023], "releases": [1], "stocks": [0, -1]},
        {"years": [2023], "releases": [1], "stocks": [0, 2]},
        {"years": [2023], "releases": [float("nan")], "stocks": [0, 0]},
        {"years": [2023], "releases": [1], "stocks": [0]},
        {"years": [], "releases": [], "stocks": [0]},
    ],
)
def test_invalid_ledger_rejected(module, kwargs) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"negative\ lawful\ consumption\ in\ 2023\ \(index\ 0\):\ R=1,\ S_prev\-S="
            r"\-2,\ U=0,\ V=0,\ D=0\.\ The\ caller\ must\ supply\ a\ release/stock/adj"
            r"ustment\ set\ that\ does\ not\ imply\ negative\ consumption"
            r"|"
            r"releases\ must\ be\ finite\ and\ >=\ 0\.0"
            r"|"
            r"stocks\ must\ be\ finite\ and\ >=\ 0\.0"
            r"|"
            r"stocks\ needs\ 2\ values,\ got\ 1"
            r"|"
            r"years\ must\ be\ consecutive,\ unique\ and\ increasing"
            r"|"
            r"years\ must\ be\ nonempty\ calendar\ integers"
            r")"
        ),
    ):
        module.lawful_ledger(basis=module.SupplyBasis(), **kwargs)


def test_incompatible_mass_units_rejected(module) -> None:
    with pytest.raises(ValueError, match="unit"):
        module.SupplyBasis(unit="tonnes")


def test_annualised_period_alignment_leap_year(module) -> None:
    x = module.lawful_ledger([2023, 2024], [365.0, 732.0], [0, 0, 0], basis=module.SupplyBasis())
    y = module.annualised_supply(x, "2023-07-01", "2024-07-01")
    assert y["covered_days"] == 366
    # Window total in source annual units: 365*184/365 + 732*182/366.
    assert y["allocated_total"] == pytest.approx(184 + 182 * 2)
    assert y["annualised_per_365_days"] == pytest.approx((184 + 182 * 2) / 366 * 365)
    assert y["allocation_is_observed"] is False
    assert "value" not in y


def test_period_total_and_rate_are_separate_keys(module) -> None:
    x = module.lawful_ledger([2023, 2024], [3650.0, 3660.0], [0, 0, 0], basis=module.SupplyBasis())
    y = module.annualised_supply(x, "2023-07-01", "2024-07-01")
    # Hand-computed daily contributions: 2023 gives 3650*184/365, 2024 3660*182/366.
    assert y["allocated_total"] == pytest.approx(3650 * 184 / 365 + 3660 * 182 / 366)
    assert y["allocated_total"] == 3660.0
    assert y["annualised_per_365_days"] == pytest.approx(y["allocated_total"] / 366 * 365)
    assert y["annualised_per_365_days"] == 3650.0
    # The overloaded key is gone; the two quantities differ by 10 here.
    assert "value" not in y
    assert y["allocated_total"] - y["annualised_per_365_days"] == pytest.approx(10.0)
    assert y["unit"] == "cigarette_equivalents/365_day_equivalent"


def test_zero_covered_days_raises_naming_window_and_days(module, monkeypatch) -> None:
    # aggregate_uniform_years already rejects end<=start, so a zero-day window has
    # to be simulated to check that annualised_supply refuses rather than dividing.
    def stub(*args, **kwargs):  # noqa: ARG001 -- Keep the injected fixture or execution-double call signature.
        return {
            "allocated_total": 0.0,
            "covered_days": 0,
            "components": [],
            "status": "uniform_within_year_allocation_assumption",
        }

    monkeypatch.setattr(module, "aggregate_uniform_years", stub)
    x = module.lawful_ledger([2023], [100.0], [0, 0], basis=module.SupplyBasis())
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Window\ 2023\-07\-01\ to\ 2023\-07\-01\ covers\ 0\ days:\ an\ annualised"
            r"\ per\-365\-day\ rate\ requires\ at\ least\ one\ covered\ day"
            r")"
        ),
    ) as excinfo:
        module.annualised_supply(x, "2023-07-01", "2023-07-01")
    message = str(excinfo.value)
    assert "2023-07-01 to 2023-07-01" in message
    assert "covers 0 days" in message


def test_no_missing_year_imputation(module) -> None:
    x = module.lawful_ledger([2023], [100.0], [0, 0], basis=module.SupplyBasis())
    with pytest.raises(ValueError, match="Missing"):
        module.annualised_supply(x, "2022-07-01", "2023-07-01")


def test_proportional_stock_scenario_telescopes(module) -> None:
    stocks = module.stock_scenario([100.0, 80.0, 60.0], 30.0)
    x = module.lawful_ledger([2021, 2022, 2023], [100.0, 80.0, 60.0], stocks, basis=module.SupplyBasis())
    assert x.consumption.sum() == pytest.approx(240 + stocks[0] - stocks[-1])


def test_stock_scenario_uses_literal_365_day_convention(module) -> None:
    # Independent oracle: one opening boundary repeating the first release rate,
    # then every release rate, all scaled by days/365 (not days/300, not 366).
    np.testing.assert_allclose(
        module.stock_scenario([100.0, 80.0, 60.0], 30.0), np.array([100, 100, 80, 60]) * 30 / 365
    )


def test_zero_stock_days_is_a_declared_no_adjustment_case(module) -> None:
    stocks = module.stock_scenario([100.0, 80.0], 0.0)
    np.testing.assert_array_equal(stocks, np.zeros(3))
    # Declared scenario, not an observed zero inventory.
    assert stocks.dtype == np.float64


def test_nonzero_stock_path_consumption_element_by_element(module) -> None:
    # Hand-computed from C=R_t+S_(t-1)-S_t with boundaries in units of days/365:
    # 12/73 = 80*30/365 - 60*30/365 on each year boundary.
    boundaries = np.array([100, 100, 80, 60]) * 30 / 365
    x = module.lawful_ledger([2021, 2022, 2023], [100.0, 80.0, 60.0], boundaries, basis=module.SupplyBasis())
    np.testing.assert_allclose(x.consumption, [100.0, 80.0 + 120 / 73, 60.0 + 120 / 73])


def test_zero_adjustments_preserve_releases(module) -> None:
    x = module.lawful_ledger([2023], [10.0], [0, 0], basis=module.SupplyBasis())
    np.testing.assert_array_equal(x.consumption, x.releases)


def test_basis_rejects_missing_scope(module) -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:geography\ is\ required)"),
    ):
        module.SupplyBasis(geography="")
    with pytest.raises(
        ValueError,
        match=(r"^(?:duty_free_included\ must\ be\ boolean)"),
    ):
        module.SupplyBasis(duty_free_included="yes")


def test_basis_is_required_without_default(module) -> None:
    with pytest.raises(TypeError):
        module.lawful_ledger([2023], [100.0], [0.0, 0.0])


def test_ledger_does_not_validate_magnitude_only_declares_basis(module) -> None:
    # A tonne-magnitude series is accepted: the ledger records the declared basis
    # and performs no unit conversion or magnitude check, so the runner must
    # guard the unit before calling this function.
    x = module.lawful_ledger([2023], [0.075], [0.0, 0.0], basis=module.SupplyBasis())
    assert x.consumption[0] == pytest.approx(0.075)
    assert x.basis.unit == "cigarette_equivalents"
    assert x.basis.geography == "NZ_national"


def test_negative_consumption_error_names_year_index_and_components(module) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"negative\ lawful\ consumption\ in\ 2023\ \(index\ 1\):\ R=80,\ S_prev\-S"
            r"=\-200,\ U=0,\ V=0,\ D=0\.\ The\ caller\ must\ supply\ a\ release/stock/"
            r"adjustment\ set\ that\ does\ not\ imply\ negative\ consumption"
            r")"
        ),
    ) as excinfo:
        module.lawful_ledger([2022, 2023], [100.0, 80.0], [0.0, 0.0, 200.0], basis=module.SupplyBasis())
    message = str(excinfo.value)
    assert "2023" in message
    assert "index 1" in message
    assert "R=80" in message
    assert "S_prev-S=-200" in message
    assert "negative lawful consumption" in message


def test_shape_error_names_required_and_received_lengths(module) -> None:
    with pytest.raises(ValueError, match=r"unrecorded needs 2 values, got 0"):
        module.lawful_ledger(
            [2023, 2024], [100.0, 100.0], [0.0, 0.0, 0.0], unrecorded=[], basis=module.SupplyBasis()
        )


def test_ledger_arrays_are_read_only(module) -> None:
    caller_owned = np.zeros(3)
    x = module.lawful_ledger([2022, 2023], [100.0, 80.0], caller_owned, basis=module.SupplyBasis())
    for name in (
        "years",
        "releases",
        "stocks",
        "unrecorded",
        "net_visitors",
        "duty_free_addition",
        "consumption",
    ):
        with pytest.raises(ValueError, match="read-only"):
            getattr(x, name)[0] = 1
    # The frozen copy must not alias caller-owned input.
    assert not np.shares_memory(x.stocks, caller_owned)


def test_bad_adjustment_shapes_and_metadata(module) -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:unrecorded\ needs\ 1\ values,\ got\ 0)"),
    ):
        module.lawful_ledger([2023], [100], [0, 0], unrecorded=[], basis=module.SupplyBasis())
    with pytest.raises(
        ValueError,
        match=(r"^(?:releases\ must\ not\ be\ empty)"),
    ):
        module.stock_scenario([], 2)
    with pytest.raises(
        ValueError,
        match=(r"^(?:stock\ days\ must\ be\ finite\ and\ >=\ 0\.0)"),
    ):
        module.stock_scenario([1], -1)
    with pytest.raises(
        ValueError,
        match=(r"^(?:product\ basis\ is\ required)"),
    ):
        module.SupplyBasis(products="")
    with pytest.raises(
        ValueError,
        match=(r"^(?:A\ validated\ SupplyBasis\ is\ required)"),
    ):
        module.lawful_ledger([2023], [100], [0, 0], basis="tonnes")


def test_basis_empty_identity_defaults_are_unattributed(module) -> None:
    basis = module.SupplyBasis()
    assert basis.source_ids == ()
    assert basis.observation_years == ()
    x = module.lawful_ledger([2023], [100.0], [0.0, 0.0], basis=basis)
    assert x.basis.source_ids == ()
    assert x.basis.observation_years == ()


@pytest.mark.parametrize(
    ("kwargs", "field", "rule"),
    [
        ({"source_ids": ("s1", "s1")}, "source_ids", "unique"),
        ({"source_ids": ("s1", "")}, "source_ids", "non-empty"),
        ({"source_ids": (" s1 ", "s1")}, "source_ids", "unique"),
        ({"source_ids": ("s1", 1)}, "source_ids", "strings"),
        ({"source_ids": ["s1"]}, "source_ids", "tuple"),
        ({"observation_years": (2023, 2021)}, "observation_years", "strictly increasing"),
        ({"observation_years": (2020, 2020)}, "observation_years", "unique"),
        ({"observation_years": (2023.0,)}, "observation_years", "integer"),
        ({"observation_years": (0,)}, "observation_years", "calendar"),
    ],
)
def test_basis_rejects_malformed_identity_declarations(module, kwargs, field, rule) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"observation_years\ contains\ duplicate\ year\ 2020;\ calendar\ years\ mu"
            r"st\ be\ unique"
            r"|"
            r"observation_years\ is\ not\ strictly\ increasing:\ 2021\ follows\ 2023;"
            r"\ calendar\ years\ must\ be\ strictly\ increasing"
            r"|"
            r"observation_years\ must\ contain\ integer\ calendar\ years;\ got\ 2023\."
            r"0"
            r"|"
            r"observation_years\ value\ 0\ is\ not\ a\ calendar\ year\ \(must\ be\ 1\."
            r"\.9998\)"
            r"|"
            r"source_ids\ contains\ an\ empty\ source\ id;\ each\ source\ id\ must\ be"
            r"\ non\-empty\ after\ stripping\ whitespace"
            r"|"
            r"source_ids\ contains\ duplicate\ source\ id\ 's1';\ source\ ids\ must\ b"
            r"e\ unique"
            r"|"
            r"source_ids\ must\ be\ a\ tuple\ of\ strings;\ got\ list"
            r"|"
            r"source_ids\ must\ contain\ strings;\ got\ int\ 1"
            r")"
        ),
    ) as excinfo:
        module.SupplyBasis(**kwargs)
    message = str(excinfo.value)
    assert field in message
    assert rule in message


def test_basis_canonicalises_the_declared_identity(module) -> None:
    basis = module.SupplyBasis(source_ids=(" parallel-S08 ",), observation_years=(2012, 2013, 2023))
    assert basis.source_ids == ("parallel-S08",)
    assert basis.observation_years == (2012, 2013, 2023)
    x = module.lawful_ledger([2023], [100.0], [0.0, 0.0], basis=basis)
    assert x.basis.source_ids == ("parallel-S08",)
    assert x.basis.observation_years == (2012, 2013, 2023)


def test_ledger_basis_distinguishes_sources_conditioning_same_observations(module) -> None:
    # Declared source identity without observation years is documented, not rejected.
    unattributed_years = module.SupplyBasis(source_ids=("parallel-S08",))
    assert unattributed_years.observation_years == ()
    assert unattributed_years.source_ids == ("parallel-S08",)
    # Same numbers from the same observation years, different declared source: the
    # duplicate-conditioning question is now answerable at the ledger layer.
    a = module.lawful_ledger(
        [2023],
        [100.0],
        [0.0, 0.0],
        basis=module.SupplyBasis(source_ids=("parallel-S08",), observation_years=(2023,)),
    )
    b = module.lawful_ledger(
        [2023],
        [100.0],
        [0.0, 0.0],
        basis=module.SupplyBasis(source_ids=("forced_other_source",), observation_years=(2023,)),
    )
    np.testing.assert_array_equal(a.consumption, b.consumption)
    assert a.basis != b.basis
    assert a.basis.source_ids != b.basis.source_ids
