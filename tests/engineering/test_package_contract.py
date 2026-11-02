"""Reject packages whose paths or dependency metadata are not portable."""

import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def contract(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return importlib.import_module("package_contract")


@pytest.mark.parametrize("names", [("CON.txt",), ("a/../b",), ("a\\b",), ("a.",), ("A.py", "a.py")])
def test_reject_windows_incompatible_archive_names(contract, names) -> None:
    with pytest.raises(ValueError, match="portable"):
        contract.portable_members(names)


def test_accept_unicode_and_spaces_without_loss(contract) -> None:
    contract.portable_members(("tobac/Māori values.py", "tobac/py.typed"))


def metadata(*requirements: str) -> bytes:
    lines = ["Metadata-Version: 2.4", "Requires-Python: >=3.15.1,<3.16", "Provides-Extra: transport"]
    return ("\n".join(lines + [f"Requires-Dist: {r}" for r in requirements]) + "\n\n").encode()


def project() -> dict:
    return {
        "requires-python": ">=3.15.1,<3.16",
        "dependencies": ["numpy==2.5.4"],
        "optional-dependencies": {"transport": ["pyarrow==26.0.0"]},
    }


def test_accept_declared_extras_on_both_platforms(contract) -> None:
    result = contract.dependency_contract(
        metadata("numpy==2.5.4", "pyarrow==26.0.0; extra == 'transport'"), project()
    )
    assert result["Windows:transport"] == ["numpy==2.5.4", "pyarrow==26.0.0"]
    assert result["Linux:none"] == ["numpy==2.5.4"]


@pytest.mark.parametrize(
    "requirements",
    [
        ("numpy==2.5.4; sys_platform == 'linux'", "pyarrow==26.0.0; extra == 'transport'"),
        ("numpy==2.5.4", "pyarrow==25.0.0; extra == 'transport'"),
        ("numpy==2.5.4", "pyarrow==26.0.0"),
    ],
)
def test_reject_missing_windows_dependency_wrong_version_and_extra_leak(contract, requirements) -> None:
    with pytest.raises(ValueError, match="dependencies"):
        contract.dependency_contract(metadata(*requirements), project())
