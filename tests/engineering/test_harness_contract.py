"""Static contracts are not proof that hosted tools have executed successfully."""

import ast
import json
import re
import tomllib
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ("engineering.yml", "engineering-deep.yml", "release-candidate.yml")


@pytest.mark.parametrize("name", WORKFLOWS)
def test_new_workflows_are_pinned_read_only_and_bounded(name) -> None:
    data = yaml.load(
        (
            ROOT
            / (
                "conductor/roadmap/deferred-workflows"
                if name == "release-candidate.yml"
                else ".github/workflows"
            )
            / name
        ).read_text(),
        Loader=yaml.BaseLoader,
    )
    assert "pull_request_target" not in data["on"]
    assert data["permissions"] == {"contents": "read"}
    assert data["concurrency"]["group"]
    for job in data["jobs"].values():
        assert 0 < int(job["timeout-minutes"]) <= 60
        assert "continue-on-error" not in job
        for step in job["steps"]:
            assert "continue-on-error" not in step
            if "uses" in step:
                assert re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+@[0-9a-f]{40}", step["uses"])
                if step["uses"].startswith("actions/checkout@"):
                    assert step["with"]["persist-credentials"] == "false"
            assert "pull_request.title" not in step.get("run", "")
            assert "secrets." not in step.get("run", "")


def test_context_profiles_are_schema_valid_and_bounded() -> None:
    schema = json.loads((ROOT / "engineering/context.schema.json").read_text())
    profiles = list((ROOT / "engineering/context").glob("*.json"))
    assert len(profiles) >= 3
    for path in profiles:
        cfg = json.loads(path.read_text())
        Draft202012Validator(schema).validate(cfg)
        assert cfg["max_bytes"] <= 100000
        assert cfg["paths"][0] == "AGENTS.md"
        assert "docs/WORKSTREAM_SYNC.md" in cfg["paths"]
        assert not any(x.startswith("outputs/") for x in cfg["paths"])


def test_conductor_is_upstream_pinned_not_copied() -> None:
    metadata = json.loads((ROOT / "engineering/upstream-pins.json").read_text())
    pin = metadata["conductor"]
    assert re.fullmatch(r"[0-9a-f]{40}", pin["commit"])
    assert pin["url"] == "https://github.com/gemini-cli-extensions/conductor.git"
    modules = (ROOT / ".gitmodules").read_text()
    assert pin["url"] in modules
    assert "vendor/conductor" in modules


def test_newest_ecosystem_is_a_separate_canary_not_a_reference_overwrite() -> None:
    code = (ROOT / "noxfile.py").read_text()
    tree = ast.parse(code)
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {
        "tests",
        "quality",
        "strict_all",
        "reproduce",
        "security",
        "lock",
        "package",
        "mutation",
        "profile",
        "canary",
    } <= names
    assert "session.python" not in code
    assert "source-only" in code
    assert "require-hashes" in code
    assert "--no-build-isolation" in code
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert config["project"]["requires-python"] == ">=3.15.1,<3.16"
    assert config["project"]["dependencies"] == ["numpy==2.5.4", "scipy==1.18.1"]
    assert "sys.version_info[:3] == (3, 15, 1)" in code
    strict = ast.parse(code)
    strict_session = next(n for n in strict.body if isinstance(n, ast.FunctionDef) and n.name == "strict_all")
    strict_source = ast.unparse(strict_session)
    assert "'engineering/ruff.toml'" in strict_source
    lint = tomllib.loads((ROOT / "ruff.toml").read_text())
    assert lint["target-version"] == "py315"
    assert "CPY001" in lint["lint"]["ignore"]
    for profile in ["basedpyright.json", "basedpyright-all.json"]:
        checker = json.loads((ROOT / "engineering" / profile).read_text())
        assert checker["pythonVersion"] == "3.15"
    all_checker = json.loads((ROOT / "engineering/basedpyright-all.json").read_text())
    assert all_checker["extraPaths"] == ["../src", "../scripts"]


def test_renovate_does_not_automerge_scientific_changes() -> None:
    data = json.loads((ROOT / "renovate.json").read_text())
    assert data["automerge"] is False
    assert "helpers:pinGitHubActionDigests" in data["extends"]
    assert data["minimumReleaseAge"]


def test_release_requires_reviewed_lock_and_is_not_public_publication() -> None:
    text = (ROOT / "conductor/roadmap/deferred-workflows/release-candidate.yml").read_text()
    assert "workflow_dispatch" in text
    assert "engineering/requirements.lock" in text
    assert "id-token: write" not in text
    assert "pypa/gh-action-pypi-publish" not in text
    assert "git push" not in text


def test_renovate_covers_profile_inputs_and_keeps_review_gates() -> None:
    data = json.loads((ROOT / "renovate.json").read_text())
    assert data["enabled"] is True
    assert data["dependencyDashboard"] is True
    patterns = data["pip_requirements"]["managerFilePatterns"]
    profiles = ["requirements", "audit", "voiage", "ecosystem"]
    for profile in profiles:
        path = f"engineering/{profile}.in"
        assert any(re.search(pattern[1:-1], path) for pattern in patterns)
    assert not any(re.search(pattern[1:-1], "conductor/archive/example.in") for pattern in patterns)
    assert not (ROOT / ".github/dependabot.yml").exists()
    assert not (ROOT / ".github/dependabot.yaml").exists()
    assert data["automerge"] is False
    assert all(rule.get("automerge") is not True for rule in data["packageRules"])
    assert any(
        {"polars", "pyarrow", "patito", "msgspec"} <= set(rule.get("matchPackageNames", []))
        for rule in data["packageRules"]
    )


def test_dependency_lock_candidates_cover_all_qualified_profiles() -> None:
    data = yaml.load(
        (ROOT / "conductor/roadmap/deferred-workflows/dependency-lock.yml").read_text(),
        Loader=yaml.BaseLoader,
    )
    job = data["jobs"]["resolve"]
    assert set(job["strategy"]["matrix"]["profile"]) == {"runtime", "audit", "voiage", "ecosystem"}
    assert data["permissions"] == {"contents": "read"}
    assert set(data["on"]) == {"workflow_dispatch"}
    assert any("scripts/lock_receipt.py generate" in step.get("run", "") for step in job["steps"])


def test_lock_candidates_use_selected_repo_local_python() -> None:
    data = yaml.load(
        (ROOT / "conductor/roadmap/deferred-workflows/dependency-lock.yml").read_text(),
        Loader=yaml.BaseLoader,
    )
    run = next(
        step["run"]
        for step in data["jobs"]["resolve"]["steps"]
        if "scripts/lock_receipt.py generate" in step.get("run", "")
    )
    assert "uv venv --python 3.15.1 .venv-lock" in run
    assert run.count(".venv-lock/bin/python") == 2
    assert "assert sys.version_info[:3] == (3, 15, 1)" in run
    assert re.search(r"(?m)^\s*python(?:3)?\s", run) is None


def test_active_ci_is_macos_only_with_checked_local_python_and_resource_guards() -> None:
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        data = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        if "push" in data["on"]:
            assert data["on"]["push"]["branches"] == ["main"], path
        for job in data["jobs"].values():
            runner = job["runs-on"]
            if runner == "${{ matrix.os }}":
                assert {entry["os"] for entry in job["strategy"]["matrix"]["include"]} == {"macos-latest"}
            else:
                assert runner in {"macos-latest", "macos-15-intel"}, (path, runner)
            commands = [step.get("run", "") for step in job["steps"]]
            assert any(
                ".venv-ci/bin/python -c" in command and "assert sys.version_info[:3] == (3, 15, 1)" in command
                for command in commands
            ), path
            for command in commands:
                if "uvx " in command:
                    assert ".venv-ci/bin/python scripts/run_bounded.py" in command, path
    deferred = ROOT / "conductor/roadmap/deferred-workflows"
    for name in ("release-candidate.yml", "dependency-lock.yml"):
        assert (deferred / name).is_file()
        assert not (ROOT / ".github/workflows" / name).exists()
