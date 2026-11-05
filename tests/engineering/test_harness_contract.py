"""Static contracts are not proof that hosted tools have executed successfully."""

import ast
import json
import re
import shlex
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = (
    "engineering.yml",
    "engineering-deep.yml",
    "release-candidate.yml",
    "dependency-lock.yml",
    "linux-audit.yml",
    "package-portability.yml",
    "scientific-reproduction.yml",
    "advisory-types.yml",
)


@pytest.mark.parametrize("name", WORKFLOWS)
def test_new_workflows_are_pinned_read_only_and_bounded(name) -> None:
    data = yaml.load(
        (ROOT / ".github/workflows" / name).read_text(),
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
    text = (ROOT / ".github/workflows/release-candidate.yml").read_text()
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
        (ROOT / ".github/workflows/dependency-lock.yml").read_text(),
        Loader=yaml.BaseLoader,
    )
    job = data["jobs"]["resolve"]
    assert set(job["strategy"]["matrix"]["profile"]) == {"runtime", "audit", "voiage", "ecosystem"}
    assert data["permissions"] == {"contents": "read"}
    assert set(data["on"]) == {"workflow_dispatch"}
    assert any("scripts/lock_receipt.py generate" in step.get("run", "") for step in job["steps"])


def test_lock_candidates_use_selected_repo_local_python() -> None:
    data = yaml.load(
        (ROOT / ".github/workflows/dependency-lock.yml").read_text(),
        Loader=yaml.BaseLoader,
    )
    run = next(
        step["run"]
        for step in data["jobs"]["resolve"]["steps"]
        if "scripts/lock_receipt.py generate" in step.get("run", "")
    )
    assert "uv venv --python 3.15.1 .venv-lock" in run
    assert run.count(".venv-lock/bin/python") == 3
    assert "scripts/run_bounded.py --max-rss-mib 4096 --timeout 900" in run
    assert "assert sys.version_info[:3] == (3, 15, 1)" in run
    assert re.search(r"(?m)^\s*python(?:3)?\s", run) is None


def assert_advisory_job_guards(data) -> None:
    assert set(data["on"]) == {"pull_request", "workflow_dispatch"}
    job = data["jobs"]["advisory"]
    assert job["strategy"]["matrix"]["os"] == ["macos-latest", "ubuntu-latest", "ubuntu-24.04-arm"]
    commands = [step.get("run", "") for step in job["steps"]]
    assert any("assert sys.version_info[:3] == (3, 15, 1)" in command for command in commands)
    assert any(
        "scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400" in c and "-s advisory_types" in c
        for c in commands
    )
    assert any("scripts/install_security_tools.sh" in command for command in commands)
    assert any("scripts/publication_boundary.py export --source outputs/advisory" in c for c in commands)
    assert all("-s reproduce" not in c and "-s tests" not in c for c in commands)


def test_active_ci_uses_checked_local_python_and_platform_guards() -> None:
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        data = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        if "push" in data["on"]:
            assert data["on"]["push"]["branches"] == ["main"], path
        if path.name == "lineage-verifier.yml":
            job = data["jobs"]["runtime"]
            variants = {(entry["os"], entry["installer"]) for entry in job["strategy"]["matrix"]["include"]}
            assert variants == {
                ("macos-latest", "uv"),
                ("macos-latest", "setup-python"),
                ("ubuntu-latest", "uv"),
                ("windows-latest", "uv"),
            }
            assert job["timeout-minutes"] == "10"
            commands = [step.get("run", "") for step in job["steps"]]
            assert any("uv venv --python 3.15.1 .venv-lineage" in command for command in commands)
            assert any("-I -S scripts/hosted_lineage.py --probe" in command for command in commands)
            assert any(command.endswith("-I -S scripts/hosted_lineage.py") for command in commands)
            assert all("upload-artifact@" not in step.get("uses", "") for step in job["steps"])
            continue
        if path.name == "cross-platform.yml":
            job = data["jobs"]["tests"]
            assert job["strategy"]["matrix"]["os"] == ["ubuntu-latest", "windows-latest"]
            assert job["timeout-minutes"] == "40"
            commands = [step.get("run", "") for step in job["steps"]]
            assert any("assert sys.version_info[:3] == (3, 15, 1)" in command for command in commands)
            assert any(
                "scripts/run_bounded.py" in command and "nox -s tests" in command for command in commands
            )
            assert any("nox -s tests" in command for command in commands)
            assert all("upload-artifact@" not in step.get("uses", "") for step in job["steps"])
            continue
        if path.name in {"advisory-types.yml", "scorecard.yml"}:
            guard = {
                "advisory-types.yml": assert_advisory_job_guards,
                "scorecard.yml": assert_scorecard_job_guards,
            }
            guard[path.name](data)
            continue
        if path.name in {"package-portability.yml", "scientific-reproduction.yml"}:
            assert_portable_package_job(data, reproduce=path.name == "scientific-reproduction.yml")
            continue
        if path.name in {"release-candidate.yml", "dependency-lock.yml"}:
            assert set(data["on"]) == {"workflow_dispatch"}
            assert data["on"]["workflow_dispatch"]["inputs"]["expected_sha"]["required"] == "true"
            for job in data["jobs"].values():
                expected = "ubuntu-latest" if path.name == "release-candidate.yml" else "ubuntu-24.04"
                assert job["runs-on"] == expected
                commands = [s.get("run", "") for s in job["steps"]]
                assert any('test "$GITHUB_SHA" = "$EXPECTED_SHA"' in c for c in commands)
                assert any("scripts/run_bounded.py --max-rss-mib 4096" in c for c in commands)
                assert any("scripts/publication_boundary.py export" in c for c in commands)
            continue
        assert_reference_job_guards(data, path)
    deferred = ROOT / "conductor/roadmap/deferred-workflows"
    for name in ("release-candidate.yml", "dependency-lock.yml"):
        assert not (deferred / name).exists()
        assert (ROOT / ".github/workflows" / name).is_file()


def test_linux_audit_requires_source_bound_lock_and_actual_audits() -> None:
    data = yaml.load((ROOT / ".github/workflows/linux-audit.yml").read_text(), Loader=yaml.BaseLoader)
    job = data["jobs"]["audit-lock"]
    assert job["runs-on"] == "ubuntu-24.04"
    assert job["env"]["TOBAC_REQUIRE_LOCK"] == "1"
    assert job["timeout-minutes"] == "40"
    commands = [step.get("run", "") for step in job["steps"]]
    assert any("verify --profile audit" in command for command in commands)
    assert any("platform.machine() == 'x86_64'" in command for command in commands)
    assert any("-s strict_all security" in command for command in commands)


def assert_reference_job_guards(data, path) -> None:
    for job in data["jobs"].values():
        assert "lock" not in job.get("strategy", {}).get("matrix", {}).get("session", [])
        runner = job["runs-on"]
        if runner == "${{ matrix.os }}":
            assert {entry["os"] for entry in job["strategy"]["matrix"]["include"]} == {"macos-latest"}
        else:
            allowed = {"linux-audit.yml": {"ubuntu-24.04"}}.get(path.name, {"macos-latest", "macos-15-intel"})
            assert runner in allowed, (path, runner)
        commands = [step.get("run", "") for step in job["steps"]]
        assert any(
            ".venv-ci/bin/python -c" in command and "assert sys.version_info[:3] == (3, 15, 1)" in command
            for command in commands
        ), path
        for command in commands:
            if "uvx " in command:
                assert ".venv-ci/bin/python scripts/run_bounded.py" in command, path


def assert_portable_package_job(data, *, reproduce=False) -> None:
    job = data["jobs"]["reproduce" if reproduce else "portable"]
    assert job["strategy"]["matrix"]["os"] == ["ubuntu-latest", "windows-latest"]
    assert job["timeout-minutes"] == "40"
    assert job["env"]["TOBAC_REQUIRE_LOCK"] == "1"
    commands = [step.get("run", "") for step in job["steps"]]
    assert any("assert sys.version_info[:3] == (3, 15, 1)" in c for c in commands)
    assert any("verify --profile runtime" in c for c in commands)
    assert any("scripts/hosted_lineage.py --configure" in c for c in commands)
    sessions = "-s reproduce" if reproduce else "-s package clean_package"
    executions = [s for s in job["steps"] if sessions in s.get("run", "")]
    assert {s["if"] for s in executions} == {"runner.os == 'Linux'", "runner.os == 'Windows'"}
    linux = next(s for s in executions if s["if"] == "runner.os == 'Linux'")
    assert "--max-rss-mib 4096 --timeout 2100" in linux["run"]
    assert any("scripts/publication_boundary.py export" in c for c in commands)


def test_all_eight_scientific_variants_are_compared_after_native_gated_nox() -> None:
    data = yaml.load(
        (ROOT / ".github/workflows/scientific-reproduction.yml").read_text(), Loader=yaml.BaseLoader
    )
    commands = [s.get("run", "") for s in data["jobs"]["reproduce"]["steps"]]
    assert any(
        "scripts/run_m2_publication.py --out outputs/engineering/reproduction-no-grid" in c for c in commands
    )
    assert any("scripts/check_scientific_reproduction.py" in c for c in commands)


def test_manual_release_keeps_complete_gates_and_inspected_failure_evidence() -> None:
    data = yaml.load((ROOT / ".github/workflows/release-candidate.yml").read_text(), Loader=yaml.BaseLoader)
    job = data["jobs"]["qualify"]
    assert job["if"] == "github.ref == 'refs/heads/main'"
    commands = [s.get("run", "") for s in job["steps"]]
    assert any("-s tests quality strict_all security reproduce package clean_package" in c for c in commands)
    assert any("scripts/hosted_lineage.py --configure" in c for c in commands)
    assert any("scripts/check_scientific_reproduction.py" in c for c in commands)
    assert any("git ls-remote origin refs/heads/main" in c for c in commands)
    uploads = [s for s in job["steps"] if "upload-artifact@" in s.get("uses", "")]
    assert all(s["with"]["path"].startswith("artifact-exports/") for s in uploads)
    assert uploads[0]["if"] == "always() && steps.evidence.outcome == 'success'"
    assert uploads[1]["if"] == "success()"


def test_manual_candidates_install_hashes_without_promoting_locks() -> None:
    text = (ROOT / ".github/workflows/dependency-lock.yml").read_text()
    assert "uv pip sync --python .venv-candidate/bin/python --require-hashes" in text
    assert "uv pip check --python .venv-candidate/bin/python" in text
    assert "scripts/lock_receipt.py verify" in text
    assert "outputs/engineering/lock-candidate/" in text
    assert "git push" not in text
    data = yaml.load(text, Loader=yaml.BaseLoader)
    uploads = [s for s in data["jobs"]["resolve"]["steps"] if "upload-artifact@" in s.get("uses", "")]
    assert all(s["with"]["path"].startswith("artifact-exports/") for s in uploads)


@pytest.mark.skipif(
    sys.platform == "win32", reason="Manual Linux release uses POSIX executable bash fixtures"
)
@pytest.mark.parametrize("status", [0, 2])
def test_release_preserves_actual_preflight_status_and_json_evidence(tmp_path, status) -> None:
    data = yaml.load((ROOT / ".github/workflows/release-candidate.yml").read_text(), Loader=yaml.BaseLoader)
    run = next(s["run"] for s in data["jobs"]["qualify"]["steps"] if "lineage_status=$?" in s.get("run", ""))
    capture = run[run.index("mkdir -p outputs/engineering") :]
    interpreter = tmp_path / ".venv-ci/bin/python"
    interpreter.parent.mkdir(parents=True)
    interpreter.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + ' "$@"\n')
    interpreter.chmod(0o755)
    script = tmp_path / "scripts/hosted_lineage.py"
    script.parent.mkdir()
    script.write_text(
        'import json\nprint(json.dumps({"runtime_probe": {}}))\n'
        f'print(json.dumps({{"success": {status == 0}}}))\nraise SystemExit({status})\n'
    )
    bash = shutil.which("bash") or "/bin/bash"
    result = subprocess.run(  # noqa: S603 -- Execute the owned workflow capture against isolated synthetic receipts.
        [bash, "-e", "-c", capture], cwd=tmp_path, capture_output=True, check=False, timeout=30
    )
    assert result.returncode == status
    evidence = json.loads((tmp_path / "outputs/engineering/lineage-preflight.json").read_text())
    assert evidence == [{"runtime_probe": {}}, {"success": status == 0}]


def assert_scorecard_job_guards(data) -> None:
    """Keep the non-Python assessment bounded and restricted to pinned actions."""
    job = data["jobs"]["analysis"]
    assert job["runs-on"] == "ubuntu-latest"
    assert job["timeout-minutes"] == "20"
    assert job["permissions"] == {
        "contents": "read",
        "security-events": "write",
        "id-token": "write",
        "actions": "read",
    }
    assert all("run" not in step for step in job["steps"])
    assert job["steps"][0]["with"]["persist-credentials"] == "false"
    analysis = job["steps"][1]
    assert analysis["uses"] == "ossf/scorecard-action@fa7117db83c52d787ae5a89f350999701505d78e"
    assert analysis["with"]["results_format"] == "sarif"
    assert "github.event_name == 'push'" in analysis["with"]["publish_results"]
