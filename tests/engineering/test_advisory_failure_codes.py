"""The advisory lane must not downgrade unresolved imports or syntax errors."""

import importlib.util
from pathlib import Path


def test_observed_checker_failure_codes_are_fatal() -> None:
    path = Path(__file__).resolve().parents[2] / "scripts" / "advisory_types.py"
    spec = importlib.util.spec_from_file_location("advisory_types", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    codes = ["unresolved-import", "missing-import", "invalid-syntax", "parse-error"]
    assert module.fatal_codes([*codes, "invalid-assignment"]) == codes
