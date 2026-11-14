"""Build a source/estimate/target parameter-to-code and eligibility crosswalk.

Reads the Phase 1 source/model/parameter/formula matrix and maps each object
to its code location and eligibility status. No observation admission,
likelihood, posterior, or scientific acceptance is conferred by this crosswalk.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "conductor/tracks/nz_au_empirical_20261106/source-model-parameter-formula-matrix_20261114.csv"

# Object type -> responsible code module for eligibility mapping
CODE_MODULES = {
    "source": "src/tobac/evidence.py",
    "model": "src/tobac/_core.py",
    "parameter": "src/tobac/parameters.py",
    "formula": "src/tobac/partial_identification.py",
}

# Disposition -> eligibility status
# CSV values use hyphenated forms: adopted, adapted, alternative, context-only, unavailable
DISPOSITION_ELIGIBILITY = {
    "adopted": "eligible_for_use",
    "adapted": "eligible_with_documented_changes",
    "alternative": "candidate_requires_verification",
    "context-only": "informative_not_empirical_input",
    "unavailable": "not_accessible_not_verifiable",
    "excluded": "screened_out_not_eligible",
}

# Source-specific code elements for eligibility mapping
SOURCE_CODE_ELEMENTS = {
    "NZHS": "src/tobac/evidence.py::Scope",
    "MOH_RETURNS": "src/tobac/supply.py",
    "STATS_TRADE": "src/tobac/evidence.py",
    "STATS_CPI": "src/tobac/evidence.py",
    "CUSTOMS": "src/tobac/evidence.py",
    "POLICE_WBE": "src/tobac/evidence.py",
    "POLICE_CRIME": "src/tobac/evidence.py",
    "JUSTICE": "src/tobac/evidence.py",
    "WHO": "src/tobac/evidence.py",
    "ACIC": "src/tobac/evidence.py",
    "AU_WBE": "src/tobac/evidence.py",
    "ABS": "src/tobac/evidence.py",
    "AU_HEALTH": "src/tobac/evidence.py",
    "HEALTH_OUTCOMES": "src/tobac/health.py",
    "CESSATION": "src/tobac/health.py",
    "COUNCIL_FLOW": "src/tobac/evidence.py",
    "PROGRAMME_COSTS": "src/tobac/evidence.py",
}

# Model-specific code elements
MODEL_CODE_ELEMENTS = {
    "NZ_HISTORICAL_BRIDGE": "src/tobac_supply/consumption_ledger.py",
    "NZ_BODE3_SHINE": "src/tobac/m2.py",
    "AU_TOBACCO_POLICY_MODELS": "src/tobac/research/implementation.py",
}

# Parameter-specific code elements
PARAMETER_CODE_ELEMENTS = {
    "WBE_PRODUCT_ATTRIBUTION": "src/tobac/partial_identification.py::restriction_bounds",
    "WBE_COSTS": "src/tobac/parameters.py",
    "WBE_COVERAGE": "src/tobac/partial_identification.py::accounting_bounds",
    "HRQOL_TARIFF": "src/tobac/parameters.py",
    "POLICY_EFFECTS": "src/tobac/research/implementation.py",
    "SUPPLY_BASIS": "src/tobac/supply.py",
    "HISTORICAL_ASSUMPTIONS": "src/tobac/parameters.py",
    "NICOTINE_MIXTURE_ID": "src/tobac/partial_identification.py",
    "VOI_FINITE_ORACLE": "src/tobac/research/qualification.py",
}


def load_matrix(path: Path) -> list[dict[str, str]]:
    """Load the source/model/parameter/formula matrix."""
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        return list(reader)


def code_element_for(row: dict[str, str]) -> str | None:
    """Return the responsible code element for a matrix row."""
    obj_type = row["object_type"]
    obj_id = row["object_id"]

    if obj_type == "source" and obj_id in SOURCE_CODE_ELEMENTS:
        return SOURCE_CODE_ELEMENTS[obj_id]
    if obj_type == "model" and obj_id in MODEL_CODE_ELEMENTS:
        return MODEL_CODE_ELEMENTS[obj_id]
    if obj_type == "parameter" and obj_id in PARAMETER_CODE_ELEMENTS:
        return PARAMETER_CODE_ELEMENTS[obj_id]

    return CODE_MODULES.get(obj_type)


def eligibility_for(disposition: str) -> str:
    """Return the eligibility status for a disposition."""
    return DISPOSITION_ELIGIBILITY.get(disposition, "eligibility_undetermined")


def build_crosswalk(matrix: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Build the parameter-to-code and eligibility crosswalk."""
    crosswalk: list[dict[str, Any]] = []
    for row in matrix:
        entry = {
            "matrix_id": row["matrix_id"],
            "object_type": row["object_type"],
            "object_id": row["object_id"],
            "country": row["country"],
            "authority": row["authority"],
            "disposition": row["disposition"],
            "verification_status": row["verification_status"],
            "dependency_group": row["dependency_group"],
            "admission_gap": row["admission_gap"],
            "model_component": row["model_component"],
            "estimand_link": row["estimand_link"],
            "validation_split": row["validation_split"],
            "notes": row["notes"],
            "code_element": code_element_for(row),
            "eligibility": eligibility_for(row["disposition"]),
            "empirical_admission": False,
            "source_edition_required": True,
            "shared_measurement_id": None,
        }
        crosswalk.append(entry)
    return crosswalk


def write_crosswalk(path: Path, crosswalk: list[dict[str, Any]], matrix_path: Path = MATRIX) -> None:
    """Write the crosswalk as JSON."""
    resolved = matrix_path.resolve()
    source = resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else Path(matrix_path.name)
    output = {
        "schema": "tobac.parameter_code_crosswalk.v1",
        "matrix_source": str(source),
        "matrix_sha256": hashlib.sha256(matrix_path.read_bytes()).hexdigest(),
        "generated_by": "scripts/crosswalk_eligibility.py",
        "total_objects": len(crosswalk),
        "eligible_for_use": sum(1 for e in crosswalk if e["eligibility"] == "eligible_for_use"),
        "eligible_with_changes": sum(
            1 for e in crosswalk if e["eligibility"] == "eligible_with_documented_changes"
        ),
        "candidate_requires_verification": sum(
            1 for e in crosswalk if e["eligibility"] == "candidate_requires_verification"
        ),
        "informative_only": sum(
            1 for e in crosswalk if e["eligibility"] == "informative_not_empirical_input"
        ),
        "not_accessible": sum(1 for e in crosswalk if e["eligibility"] == "not_accessible_not_verifiable"),
        "screened_out": sum(1 for e in crosswalk if e["eligibility"] == "screened_out_not_eligible"),
        "crosswalk": crosswalk,
    }
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    """Build and write the parameter-to-code and eligibility crosswalk."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=MATRIX, help="Path to the matrix CSV")
    parser.add_argument("--out", type=Path, required=True, help="Output crosswalk JSON path")
    args = parser.parse_args()

    matrix = load_matrix(args.matrix)
    crosswalk = build_crosswalk(matrix)
    write_crosswalk(args.out, crosswalk, args.matrix)


if __name__ == "__main__":
    main()
