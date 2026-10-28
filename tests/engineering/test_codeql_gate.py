"""Native analysis is separate; these checks prevent false acceptance of its reports."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from run_codeql import validate_sarif


@pytest.mark.parametrize(
    "run",
    [
        {"results": [{"level": "warning"}]},
        {"invocations": [{"executionSuccessful": False}]},
        {"invocations": [{"toolExecutionNotifications": [{"level": "error"}]}]},
        {"invocations": [{"toolExecutionNotifications": [{"level": "warning"}]}]},
    ],
)
def test_findings_or_incomplete_analysis_fail(run) -> None:
    with pytest.raises(ValueError, match="CodeQL"):
        validate_sarif({"runs": [run]})


def test_no_analysis_is_not_a_clean_result() -> None:
    with pytest.raises(ValueError, match="Missing CodeQL"):
        validate_sarif({"runs": []})
    with pytest.raises(ValueError, match="Missing CodeQL execution"):
        validate_sarif({"runs": [{}]})


def test_clean_executed_analysis_accepted() -> None:
    validate_sarif({"runs": [{"results": [], "invocations": [{"executionSuccessful": True}]}]})
