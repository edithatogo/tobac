"""Conditional M2a projections for matched inspection game scenarios."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from typing import TYPE_CHECKING, Literal, cast

from tobac.partial_identification import Interval, RatioBounds, restriction_bounds

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from pathlib import Path

    from tobac.evidence import Scope


@dataclass(frozen=True)
class InspectionObservations:
    """Matched ratio measurements and reporting-bias supports for one product."""

    scope: Scope
    product: str
    total: Interval | None
    lawful: Interval | None
    total_bias: Interval
    lawful_bias: Interval
    channel: Literal["border_seizure", "retail_inspection"] = field(kw_only=True)
    scenario_id: str = field(kw_only=True)
    calibration_sha256: str = field(kw_only=True)


@dataclass(frozen=True)
class InspectionScenario:
    """Conditional M2a bounds and the exact solver and fiscal receipt."""

    bounds: RatioBounds
    receipt: dict[str, object]
    observations: InspectionObservations
    evasion_support: tuple[Fraction, Fraction]


@dataclass(frozen=True)
class InspectionDecisionDraw:
    """One specified joint outcome and prior weight for a reviewed scenario."""

    scenario: InspectionScenario
    continuing: Fraction
    lawful: Fraction
    weight: float

    @property
    def switching(self) -> Fraction | None:
        """Return the switching share when there is continuing consumption."""
        if self.continuing:
            return 1 - self.lawful / self.continuing
        return None


@dataclass(frozen=True)
class InspectionPairedDraws:
    """Voiage long-table inputs with their original fiscal pairing evidence."""

    dataset_id: str
    strategy_ids: tuple[str, str]
    perspective: str
    subgroup_id: str
    draw_set_digest: str
    value_unit: str
    fiscal_keys: tuple[dict[str, object], ...]
    rows: list[dict[str, str | float]]


def _calibrated_ratio(observed: Interval | None, bias: Interval) -> tuple[Fraction, Fraction]:
    if bias.lower <= 0:
        msg = "A strictly positive reporting bias is required"
        raise ValueError(msg)
    if observed is None:
        return Fraction(0), Fraction(1)
    if observed.lower < 0:
        msg = "Nonnegative quantities and strictly positive calibration required"
        raise ValueError(msg)
    return Fraction(observed.lower) / Fraction(bias.upper), Fraction(observed.upper) / Fraction(bias.lower)


def _enclosing_interval(lower: Fraction, upper: Fraction) -> Interval:
    lower_float, upper_float = float(lower), float(upper)
    if Fraction(lower_float) > lower:
        lower_float = math.nextafter(lower_float, -math.inf)
    if Fraction(upper_float) < upper:
        upper_float = math.nextafter(upper_float, math.inf)
    return Interval(lower_float, upper_float)


def inspection_restriction_bounds(
    total: Interval | None,
    lawful: Interval | None,
    *,
    total_bias: Interval,
    lawful_bias: Interval,
    switching_support: Interval,
) -> RatioBounds:
    """Condition the ratio model on switching among continuing consumers.

    The support must describe the same population, product and observation
    period as the ratios. The projections are conditional on that support.
    At zero continuing consumption, switching is undefined and remains
    unrestricted in the projection.
    """
    if switching_support.lower < 0 or switching_support.upper > 1:
        msg = "Switching support must lie within [0, 1]"
        raise ValueError(msg)
    return _conditioned_restriction_bounds(
        total,
        lawful,
        total_bias=total_bias,
        lawful_bias=lawful_bias,
        switching_support=(Fraction(switching_support.lower), Fraction(switching_support.upper)),
    )


def _conditioned_restriction_bounds(
    total: Interval | None,
    lawful: Interval | None,
    *,
    total_bias: Interval,
    lawful_bias: Interval,
    switching_support: tuple[Fraction, Fraction],
) -> RatioBounds:
    if switching_support == (0, 1):
        return restriction_bounds(total, lawful, total_bias=total_bias, lawful_bias=lawful_bias)

    minimum_total, maximum_total = _calibrated_ratio(total, total_bias)
    minimum_lawful, maximum_lawful = _calibrated_ratio(lawful, lawful_bias)
    # For remaining consumption t and lawful share s, lawful use is t*s.
    # A given t admits a feasible s when t*max(s) >= min(lawful) and
    # t*min(s) <= max(lawful). Round only the final projected intervals.
    minimum_switching, maximum_switching = switching_support
    minimum_share = 1 - maximum_switching
    maximum_share = 1 - minimum_switching
    if maximum_share == 0 and minimum_lawful > 0:
        return RatioBounds(feasible=False, quitting=None, switching=None)

    maximum_total = min(Fraction(1), maximum_total)
    if maximum_share > 0:
        minimum_total = max(minimum_total, minimum_lawful / maximum_share)
    if minimum_share > 0:
        maximum_total = min(maximum_total, maximum_lawful / minimum_share)
    if minimum_total > maximum_total:
        return RatioBounds(feasible=False, quitting=None, switching=None)

    quitting = _enclosing_interval(1 - maximum_total, 1 - minimum_total)
    if minimum_total == 0:
        switching = Interval(0, 1)
    else:
        switching = _enclosing_interval(
            1 - min(maximum_share, maximum_lawful / minimum_total),
            1 - max(minimum_share, minimum_lawful / maximum_total),
        )
    return RatioBounds(feasible=True, quitting=quitting, switching=switching)


def _receipt_object(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        msg = "Native inspection receipt must contain the declared objects"
        raise TypeError(msg)
    return cast("dict[str, object]", value)


def _receipt_ratio(value: object) -> Fraction:
    fields = _receipt_object(value)
    numerator = fields.get("numerator")
    denominator = fields.get("denominator")
    if not isinstance(numerator, str) or not isinstance(denominator, str) or int(denominator) <= 0:
        msg = "Native inspection receipt must contain exact rational endpoints"
        raise ValueError(msg)
    return Fraction(int(numerator), int(denominator))


def _receipt_text(fields: dict[str, object], name: str) -> str:
    value = fields.get(name)
    if not isinstance(value, str) or not value.strip():
        msg = f"Native inspection receipt requires {name}"
        raise ValueError(msg)
    return value


def run_inspection_scenario(
    executable: Path, request: bytes, observations: InspectionObservations
) -> InspectionScenario:
    """Run the approved locked Rust executable and condition the matched M2a ratios.

    Select the expected channel, scenario and calibration independently of the
    request. The returned receipt retains exact endpoints and fiscal draw keys.
    """
    result = subprocess.run(  # noqa: S603 -- The caller selects a trusted installed binary, with no shell.
        [str(executable.resolve(strict=True))],
        input=request,
        capture_output=True,
        check=False,
        timeout=60,
        env={"LC_ALL": "C"},
    )
    if result.returncode:
        msg = f"Native inspection command exited {result.returncode}"
        raise RuntimeError(msg)
    receipt = _receipt_object(json.loads(result.stdout))
    if (
        receipt.get("schema_version") != "tobac-inspection-result/0.1"
        or receipt.get("method") != "paignia_detection_nash_projection"
        or receipt.get("input_sha256") != f"sha256:{hashlib.sha256(request).hexdigest()}"
    ):
        msg = "Native inspection receipt does not match the submitted request"
        raise ValueError(msg)
    scope = _receipt_object(receipt.get("scope"))
    if (
        scope.get("observations") != asdict(observations.scope)
        or scope.get("product") != observations.product
        or scope.get("switching_measure") != "evasion_among_continuing_consumers"
    ):
        msg = "Native switching calibration and M2a observation scopes differ"
        raise ValueError(msg)
    if (
        scope.get("channel") != observations.channel
        or scope.get("scenario_id") != observations.scenario_id
        or scope.get("calibration_sha256") != observations.calibration_sha256
    ):
        msg = "Native channel, scenario or calibration differs from the declared M2a context"
        raise ValueError(msg)

    evasion = _receipt_object(_receipt_object(receipt.get("projection")).get("evasion"))
    lower, upper = _receipt_ratio(evasion.get("lower")), _receipt_ratio(evasion.get("upper"))
    if not 0 <= lower <= upper <= 1:
        msg = "Native evasion bounds must be ordered proportions"
        raise ValueError(msg)
    bounds = _conditioned_restriction_bounds(
        observations.total,
        observations.lawful,
        total_bias=observations.total_bias,
        lawful_bias=observations.lawful_bias,
        switching_support=(lower, upper),
    )
    return InspectionScenario(bounds, receipt, observations, (lower, upper))


def _check_inspection_draw(draw: InspectionDecisionDraw) -> None:
    scenario = draw.scenario
    observations = scenario.observations
    total_lo, total_hi = _calibrated_ratio(observations.total, observations.total_bias)
    lawful_lo, lawful_hi = _calibrated_ratio(observations.lawful, observations.lawful_bias)
    evasion_lo, evasion_hi = scenario.evasion_support
    switching = draw.switching
    if (
        not scenario.bounds.feasible
        or not 0 <= draw.lawful <= draw.continuing <= 1
        or not total_lo <= draw.continuing <= total_hi
        or not lawful_lo <= draw.lawful <= lawful_hi
        or (switching is not None and not evasion_lo <= switching <= evasion_hi)
    ):
        msg = "Joint draw is outside the matched observations and native switching support"
        raise ValueError(msg)


def prepare_inspection_paired_draws(
    draws: Sequence[InspectionDecisionDraw],
    net_benefits: Callable[[InspectionDecisionDraw], tuple[float, float]],
    *,
    value_unit: str,
) -> InspectionPairedDraws:
    """Prepare one explicit joint model for Voiage's censored EVSI input.

    The caller supplies prior weights and a valuation returning the strategy
    and comparator net benefits in the stated unit. Every draw must satisfy
    the original observation and native switching constraints jointly. Keep
    candidate models separate when evaluating a set of priors or outcomes.
    """
    if not value_unit.strip():
        msg = "A declared net-benefit unit is required"
        raise ValueError(msg)
    if any(not math.isfinite(draw.weight) or draw.weight < 0 for draw in draws):
        msg = "Draw weights must be finite and nonnegative"
        raise ValueError(msg)

    context = None
    seen: set[str] = set()
    matched: list[tuple[InspectionDecisionDraw, str, dict[str, object]]] = []
    for draw in draws:
        _check_inspection_draw(draw)
        scenario = draw.scenario
        obs = scenario.observations
        fiscal = _receipt_object(scenario.receipt.get("fiscal"))
        key = _receipt_object(fiscal.get("key"))
        scenario_id = _receipt_text(key, "scenario_id")
        strategy = _receipt_text(key, "strategy_id")
        comparator = _receipt_text(fiscal, "comparator_strategy_id")
        perspective = _receipt_text(key, "perspective")
        subgroup = _receipt_text(key, "subgroup_id")
        digest = _receipt_text(fiscal, "draw_set_digest")
        draw_id = _receipt_text(key, "draw_id")
        _receipt_text(key, "replication_id")
        draw_context = (
            (scenario_id, (strategy, comparator), perspective, subgroup, digest),
            obs.scope,
            obs.product,
            obs.channel,
            obs.calibration_sha256,
            fiscal.get("currency"),
            fiscal.get("price_year"),
            fiscal.get("resource_basis"),
        )
        if (
            scenario_id != obs.scenario_id
            or strategy == comparator
            or (context is not None and context != draw_context)
        ):
            msg = "Inspection draws must share one matched fiscal and calibration scope"
            raise ValueError(msg)
        if draw_id in seen:
            msg = f"Duplicate inspection draw ID {draw_id}"
            raise ValueError(msg)
        context = draw_context
        seen.add(draw_id)
        matched.append((draw, draw_id, dict(key)))

    if context is None or not any(draw.weight > 0 for draw in draws):
        msg = "Matched draws with positive prior mass are required"
        raise ValueError(msg)
    scenario_id, strategy_ids, perspective, subgroup, digest = context[0]
    rows: list[dict[str, str | float]] = []
    for draw, draw_id, _ in matched:
        for identifier, value in zip(strategy_ids, net_benefits(draw), strict=True):
            if not math.isfinite(value):
                msg = "Inspection net benefits must be finite"
                raise ValueError(msg)
            rows.append(
                {
                    "draw_id": draw_id,
                    "strategy_id": identifier,
                    "perspective": perspective,
                    "subgroup_id": subgroup,
                    "net_benefit": value,
                    "weight": draw.weight,
                }
            )
    return InspectionPairedDraws(
        scenario_id,
        strategy_ids,
        perspective,
        subgroup,
        digest,
        value_unit,
        tuple(key for _, _, key in matched),
        rows,
    )
