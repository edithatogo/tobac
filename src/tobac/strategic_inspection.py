"""Conditional M2a projections for matched inspection game scenarios."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import TYPE_CHECKING, cast

from tobac.partial_identification import Interval, RatioBounds, _ratio, restriction_bounds

if TYPE_CHECKING:
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


@dataclass(frozen=True)
class InspectionScenario:
    """Conditional M2a bounds and the exact solver and fiscal receipt."""

    bounds: RatioBounds
    receipt: dict[str, object]


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
    if switching_support == Interval(0, 1):
        return restriction_bounds(total, lawful, total_bias=total_bias, lawful_bias=lawful_bias)
    total_ratio, lawful_ratio = _ratio(total, total_bias), _ratio(lawful, lawful_bias)
    if total_ratio is None or lawful_ratio is None:
        return RatioBounds(feasible=False, quitting=None, switching=None)
    # For remaining consumption t and lawful share s, lawful use is t*s.
    # A given t admits a feasible s when t*max(s) >= min(lawful) and
    # t*min(s) <= max(lawful). Keep these comparisons exact at point boundaries.
    minimum_lawful, maximum_lawful = Fraction(lawful_ratio.lower), Fraction(lawful_ratio.upper)
    minimum_share = 1 - Fraction(switching_support.upper)
    maximum_share = 1 - Fraction(switching_support.lower)
    if maximum_share == 0 and minimum_lawful > 0:
        return RatioBounds(feasible=False, quitting=None, switching=None)

    minimum_total, maximum_total = Fraction(total_ratio.lower), Fraction(total_ratio.upper)
    if maximum_share > 0:
        minimum_total = max(minimum_total, minimum_lawful / maximum_share)
    if minimum_share > 0:
        maximum_total = min(maximum_total, maximum_lawful / minimum_share)
    if minimum_total > maximum_total:
        return RatioBounds(feasible=False, quitting=None, switching=None)

    quitting = Interval(float(1 - maximum_total), float(1 - minimum_total))
    if minimum_total == 0:
        switching = Interval(0, 1)
    else:
        switching = Interval(
            float(1 - min(maximum_share, maximum_lawful / minimum_total)),
            float(1 - max(minimum_share, minimum_lawful / maximum_total)),
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


def run_inspection_scenario(
    executable: Path, request: bytes, observations: InspectionObservations
) -> InspectionScenario:
    """Run the approved locked Rust executable and condition the matched M2a ratios.

    The request carries an explicit switching measure and calibration digest.
    The returned receipt retains exact native endpoints, valuations and draw keys.
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

    evasion = _receipt_object(_receipt_object(receipt.get("projection")).get("evasion"))
    lower, upper = _receipt_ratio(evasion.get("lower")), _receipt_ratio(evasion.get("upper"))
    if not 0 <= lower <= upper <= 1:
        msg = "Native evasion bounds must be ordered proportions"
        raise ValueError(msg)
    lower_float, upper_float = float(lower), float(upper)
    if Fraction(lower_float) > lower:
        lower_float = math.nextafter(lower_float, -math.inf)
    if Fraction(upper_float) < upper:
        upper_float = math.nextafter(upper_float, math.inf)
    bounds = inspection_restriction_bounds(
        observations.total,
        observations.lawful,
        total_bias=observations.total_bias,
        lawful_bias=observations.lawful_bias,
        switching_support=Interval(lower_float, upper_float),
    )
    return InspectionScenario(bounds=bounds, receipt=receipt)
