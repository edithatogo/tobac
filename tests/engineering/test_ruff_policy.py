"""Exercise the pinned Ruff binary against lint and formatter counterexamples."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def ruff():
    binary = shutil.which("ruff")
    if binary is None:
        candidate = ROOT / ".nox/quality/bin/ruff"
        if candidate.is_file():
            binary = str(candidate)
    if binary is None:
        pytest.skip("Ruff is required and executed in the strict_all tool environment")
    return binary


@pytest.mark.parametrize(
    ("rule", "source"),
    [
        ("PLW1514", 'open("fixture.txt")\n'),
        ("RUF039", 'import re\nre.compile("pattern")\n'),
        ("RUF031", "values = {}\nvalues[(1, 2)]\n"),
        ("PLC1901", 'text = "value"\nif text == "":\n    pass\n'),
        ("FURB113", "values = []\nvalues.append(1)\nvalues.append(2)\n"),
        ("F821", "undefined_name\n"),
    ],
)
def test_preview_and_stable_rules_reject_counterexamples(ruff, rule, source) -> None:
    result = subprocess.run(  # noqa: S603 -- Resolved pinned Ruff; literal synthetic source, no shell.
        [
            ruff,
            "check",
            "--config",
            "engineering/ruff.toml",
            "--output-format",
            "json",
            "--stdin-filename",
            "src/probe.py",
            "-",
        ],
        input=source,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )
    assert result.returncode == 1, result.stderr
    assert rule in {item["code"] for item in json.loads(result.stdout)}


def test_formatter_gate_rejects_unformatted_source(ruff) -> None:
    result = subprocess.run(  # noqa: S603 -- Resolved pinned Ruff; literal synthetic source, no shell.
        [
            ruff,
            "format",
            "--check",
            "--config",
            "engineering/ruff.toml",
            "--stdin-filename",
            "src/probe.py",
            "-",
        ],
        input="value= [1,2]\n",
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )
    assert result.returncode == 1


def test_strict_gate_cannot_drop_tests_tooling_or_formatting() -> None:
    import ast  # noqa: PLC0415 -- Contract inspection does not load or execute Nox sessions.

    tree = ast.parse((ROOT / "noxfile.py").read_text())
    strict = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "strict_all")
    commands = [
        ast.literal_eval(node)
        for node in ast.walk(strict)
        if isinstance(node, ast.List)
        and node.elts
        and all(isinstance(item, ast.Constant) and isinstance(item.value, str) for item in node.elts)
    ]
    targets = {"src", "scripts", "tests", "noxfile.py"}
    assert any(command[:2] == ["ruff", "check"] and targets <= set(command) for command in commands)
    assert any(
        command[:3] == ["ruff", "format", "--check"] and targets <= set(command) for command in commands
    )


def test_editor_and_nox_discover_the_same_python(ruff) -> None:
    discovered = []
    for arguments in [
        [],
        ["--config", "engineering/ruff.toml", "src", "scripts", "tests", "noxfile.py", "engineering/typings"],
    ]:
        result = subprocess.run(  # noqa: S603 -- Read-only file discovery with the pinned Ruff binary.
            [ruff, "check", "--show-files", *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
            check=True,
        )
        discovered.append(
            {
                Path(line).relative_to(ROOT)
                for line in result.stdout.splitlines()
                if Path(line).suffix in {".py", ".pyi"}
            }
        )
    assert discovered[0] == discovered[1]
    assert Path("noxfile.py") in discovered[0]
    assert any(path.parts[:2] == ("engineering", "typings") for path in discovered[0])
    assert all(path.parts[0] not in {"vendor", "outputs", "evidence"} for path in discovered[0])
