"""Run pinned differential type checkers and retain fail-closed evidence."""

from __future__ import annotations

import base64
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, cast
from urllib.parse import unquote, urlparse
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "advisory"
VERSIONS = {"ty": "ty 0.0.95", "pyrefly": "pyrefly 1.4.0"}
REQUIRED_MODULES = (
    "numpy",
    "scipy",
    "pyarrow",
    "polars",
    "patito",
    "msgspec",
    "sklearn",
    "pydantic",
    "voiage.analysis",
    "voiage.schema",
    "voiage.methods.basic",
)
STUB_CANDIDATES = ("unresolved-attribute", "missing-attribute", "unknown-attribute", "untyped-import")


def digest(path: Path) -> str:
    """Hash an exact file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fatal_codes(codes: list[str]) -> list[str]:
    """Find errors that make the checker run unqualified rather than advisory."""
    markers = ("unresolved-import", "missing-import", "parse-error", "syntax-error", "invalid-syntax")
    return [code for code in codes if any(marker in code.lower() for marker in markers)]


def _file_location(uri: str) -> str:
    """Normalize diagnostic locations to a repo-relative path without losing spaces."""
    parsed = urlparse(uri)
    if parsed.scheme == "file" and parsed.netloc in ("", "localhost"):
        path = Path(unquote(parsed.path))
    elif not parsed.scheme:
        path = ROOT / unquote(uri)
    else:
        msg = "Unsupported diagnostic location URI"
        raise ValueError(msg)
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError as exc:
        msg = "Diagnostic location is outside the repository"
        raise ValueError(msg) from exc


def _entries(tool: str, raw: bytes) -> list[dict[str, Any]]:
    """Select the expected structured diagnostic collection."""
    decoded: object = json.loads(raw)
    if not isinstance(decoded, dict):
        msg = f"Malformed {tool} report"
        raise TypeError(msg)
    report = cast("dict[str, Any]", decoded)
    if tool == "ty":
        runs = cast("list[Any]", report["runs"])
        if report.get("version") != "2.1.0" or len(runs) != 1:
            msg = "Malformed ty SARIF report"
            raise ValueError(msg)
        entries: object = runs[0]["results"]
    elif tool == "pyrefly":
        entries = report["errors"]
    else:
        msg = "Unknown checker"
        raise ValueError(msg)
    if not isinstance(entries, list):
        msg = f"Malformed {tool} diagnostics"
        raise TypeError(msg)
    return cast("list[dict[str, Any]]", entries)


def _normalize(tool: str, entry: dict[str, Any]) -> dict[str, Any]:
    """Validate a single diagnostic and return its comparison identity."""
    if tool == "ty":
        location = entry["locations"][0]["physicalLocation"]
        path = _file_location(location["artifactLocation"]["uri"])
        line = location["region"]["startLine"]
        code, severity = entry["ruleId"], entry["level"]
    else:
        path, line = _file_location(entry["path"]), entry["line"]
        code, severity = entry["name"], entry["severity"]
    if not isinstance(code, str) or not code or not isinstance(line, int) or line < 1:
        msg = f"Malformed {tool} diagnostic fields"
        raise ValueError(msg)
    if severity not in {"error", "warning", "warn", "note", "info"}:
        msg = f"Unknown {tool} severity: {severity!r}"
        raise ValueError(msg)
    return {"path": path, "line": line, "code": code, "severity": severity}


def parse_report(tool: str, raw: bytes, exit_code: int) -> list[dict[str, Any]]:
    """Validate report shape and exit semantics; retain per-location comparison keys."""
    if exit_code not in (0, 1):
        msg = f"{tool} crashed or failed: exit {exit_code}"
        raise ValueError(msg)
    normalized = [_normalize(tool, entry) for entry in _entries(tool, raw)]
    errors = sum(item["severity"] == "error" for item in normalized)
    if bool(errors) != bool(exit_code):
        msg = f"{tool} exit code contradicts diagnostic severity"
        raise ValueError(msg)
    return normalized


def compare(reports: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Compare file/line overlap and label possible stub gaps for human inspection."""
    locations = {
        name: {(item["path"], item["line"]) for item in entries} for name, entries in reports.items()
    }
    overlap = locations["ty"] & locations["pyrefly"]
    findings = {}
    for name, entries in reports.items():
        findings[name] = {
            "count": len(entries),
            "codes": dict(sorted(Counter(item["code"] for item in entries).items())),
            "overlap_count": sum((item["path"], item["line"]) in overlap for item in entries),
            "unique_count": sum((item["path"], item["line"]) not in overlap for item in entries),
            "possible_stub_gaps": [
                item for item in entries if any(x in item["code"] for x in STUB_CANDIDATES)
            ],
        }
    return {
        "method": "same repository-relative file and line; not semantic equivalence",
        "overlap_locations": len(overlap),
        "tools": findings,
    }


def input_hashes() -> dict[str, str]:
    """Bind complete checked source and the settings governing this run."""
    files = {p for base in (ROOT / "src", ROOT / "scripts") for p in base.rglob("*.py")}
    files.update(p for base in (ROOT / "src", ROOT / "scripts") for p in base.rglob("*.pyi"))
    files.update((ROOT / "engineering" / "typings").rglob("*.pyi"))
    files.update(
        ROOT / name
        for name in (
            "pyproject.toml",
            "noxfile.py",
            "engineering/advisory.in",
            "engineering/advisory.lock",
            "engineering/advisory.lock.json",
            "engineering/voiage.in",
            "engineering/voiage-build-requirements.txt",
            ".github/workflows/advisory-types.yml",
        )
    )
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(files)}


def execute_checker(
    name: str, command: list[str], output: Path, environment: dict[str, str]
) -> dict[str, Any]:
    """Preserve original status and output even when the checker crashes or times out."""
    try:
        process = subprocess.run(  # noqa: S603 -- Fixed checker executable/argv, no shell.
            command, cwd=ROOT, capture_output=True, timeout=2100, check=False, env=environment
        )
        stdout, stderr, code, timeout = process.stdout, process.stderr, process.returncode, False
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, code, timeout = exc.stdout or b"", exc.stderr or b"", None, True
    (output / f"{name}.json").write_bytes(stdout)
    (output / f"{name}-stderr.json").write_text(
        json.dumps({"encoding": "base64", "bytes": base64.b64encode(stderr).decode("ascii")}) + "\n",
        encoding="utf-8",
    )
    result = {
        "command": command,
        "exit_code": code,
        "timed_out": timeout,
        "report_sha256": digest(output / f"{name}.json"),
        "executable_sha256": digest(Path(command[0])),
    }
    (output / f"{name}-execution.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if timeout:
        msg = f"{name} timed out"
        raise TimeoutError(msg)
    return result


def qualify_fixtures(
    commands: dict[str, list[str]], output: Path, environment: dict[str, str]
) -> dict[str, Any]:
    """Exercise each real checker against Python 3.15 positive and negative fixtures."""
    fixtures = {
        "good": ("type Pair[T] = tuple[T, T]\nvalue: int = 1\n", 0, None),
        "bad": ("value: int = 'bad'\n", 1, "assignment"),
        "missing": ("import dci3_deliberately_missing_module\n", 1, "import"),
        "invalid": ("def broken(:\n    pass\n", 1, "parse-error|invalid-syntax"),
        "lazy": ("lazy import json\nvalue: str = json.dumps({'x': 1})\n", 0, None),
    }
    folder = output / "fixtures"
    folder.mkdir()
    results: dict[str, Any] = {}
    for case, (source, expected_exit, required) in fixtures.items():
        path = folder / f"{case}.py"
        path.write_text(source, encoding="utf-8")
        if case != "invalid":
            compile(source, str(path), "exec")
        for name, command in commands.items():
            fixture_command = [*command[:-2], str(path)]
            result = execute_checker(f"{name}-{case}", fixture_command, folder, environment)
            entries = parse_report(
                name, (folder / f"{name}-{case}.json").read_bytes(), cast("int", result["exit_code"])
            )
            codes = [item["code"] for item in entries]
            if result["exit_code"] != expected_exit or (
                required is not None
                and not any(marker in code for marker in required.split("|") for code in codes)
            ):
                msg = f"{name} fixture {case} failed: exit {result['exit_code']}, codes {codes}"
                raise RuntimeError(msg)
            results[f"{name}-{case}"] = {
                "source_sha256": digest(path),
                "exit_code": result["exit_code"],
                "codes": codes,
                "command": fixture_command,
            }
    crash_exit = 7
    crash_command = [sys.executable, "-c", f"import sys; sys.exit({crash_exit})"]
    crash = execute_checker("forced-crash", crash_command, folder, environment)
    if crash["exit_code"] != crash_exit:
        msg = "Controlled crash did not preserve its exit code"
        raise RuntimeError(msg)
    results["forced-crash"] = {"exit_code": crash["exit_code"], "command": crash_command}
    # A checker crash and a malformed/missing report must never count as diagnostics.
    for raw, code in ((b"{}", 2), (b"", 1), (b"{", 1)):
        try:
            parse_report("ty", raw, code)
        except ValueError, KeyError, IndexError, TypeError:
            continue
        msg = "Crash or malformed report was accepted"
        raise RuntimeError(msg)
    (folder / "qualification.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return results


def record_help(name: str, binary: Path, output: Path, checker_env: dict[str, str]) -> None:
    """Retain and validate each pinned checker's actual help output."""
    help_command = [str(binary / name), "check", "--help"]
    help_result = subprocess.run(  # noqa: S603 -- Fixed pinned checker help command.
        help_command, cwd=ROOT, capture_output=True, timeout=30, check=False, env=checker_env
    )
    (output / f"{name}-help.json").write_text(
        json.dumps(
            {
                "command": help_command,
                "exit_code": help_result.returncode,
                "stdout_base64": base64.b64encode(help_result.stdout).decode("ascii"),
                "stderr_base64": base64.b64encode(help_result.stderr).decode("ascii"),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    if help_result.returncode:
        msg = f"{name} help failed: {help_result.returncode}"
        raise RuntimeError(msg)


def run() -> None:
    """Run both tools serially and write raw diagnostics, exit codes and comparison."""
    if sys.version_info[:3] != (3, 15, 1) or not Path(sys.executable).absolute().is_relative_to(ROOT):
        msg = "A repo-local Python 3.15.1 is required"
        raise RuntimeError(msg)
    if importlib.metadata.version("voiage") != "3.1.0":
        msg = "Wrong published Polars producer"
        raise RuntimeError(msg)
    if any(importlib.util.find_spec(name) is not None for name in ("pandas", "xarray")):
        msg = "Retired dataframe dependency remains installed"
        raise RuntimeError(msg)
    missing = [name for name in REQUIRED_MODULES if importlib.util.find_spec(name) is None]
    if missing:
        msg = f"Required imports missing: {missing}"
        raise RuntimeError(msg)
    output = OUT / uuid4().hex
    output.mkdir(parents=True)
    config = output / "pyrefly.toml"
    config.write_text(
        f'python-version = "3.15.1"\npython-interpreter = {json.dumps(sys.executable)}\n'
        f"search-path = [{json.dumps(str(ROOT / 'src'))}, {json.dumps(str(ROOT / 'scripts'))}]\n",
        encoding="utf-8",
    )
    binary = Path(sys.executable).parent
    commands = {
        "ty": [
            str(binary / "ty"),
            "check",
            "--python",
            sys.executable,
            "--python-version",
            "3.15",
            "--output-format",
            "sarif",
            "src",
            "scripts",
        ],
        "pyrefly": [
            str(binary / "pyrefly"),
            "check",
            "--config",
            str(config),
            "--output-format",
            "json",
            "src",
            "scripts",
        ],
    }
    before = input_hashes()
    checker_env = {k: v for k, v in os.environ.items() if not k.startswith(("TY_", "PYREFLY_"))}
    checker_env.pop("PYTHONPATH", None)
    fixture_results = qualify_fixtures(commands, output, checker_env)
    versions: dict[str, str] = {}
    results: dict[str, dict[str, Any]] = {}
    reports: dict[str, list[dict[str, Any]]] = {}
    for name, command in commands.items():
        version = subprocess.run(  # noqa: S603 -- Fixed interpreter-local executable and argv.
            [str(binary / name), "--version"], capture_output=True, text=True, check=True, timeout=30
        ).stdout.strip()
        if version.split()[:2] != VERSIONS[name].split():
            msg = f"Unexpected {name} version: {version}"
            raise RuntimeError(msg)
        versions[name] = version
        record_help(name, binary, output, checker_env)
        results[name] = execute_checker(name, command, output, checker_env)
        reports[name] = parse_report(
            name, (output / f"{name}.json").read_bytes(), cast("int", results[name]["exit_code"])
        )
    if input_hashes() != before:
        msg = "Source or configuration changed during advisory run"
        raise RuntimeError(msg)
    comparison = compare(reports)
    environment = sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions())
    environment_bytes = json.dumps(environment, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    record = {
        "schema": "tobac.advisory-types.v1",
        "python": sys.version,
        "interpreter": sys.executable,
        "interpreter_sha256": digest(Path(sys.executable)),
        "platform": platform.platform(),
        "versions": versions,
        "results": results,
        "environment": environment,
        "environment_sha256": hashlib.sha256(environment_bytes).hexdigest(),
        "runtime_settings": {
            name: os.environ.get(name)
            for name in (
                "OPENBLAS_NUM_THREADS",
                "RAYON_NUM_THREADS",
                "CARGO_BUILD_JOBS",
                "PYTHONHASHSEED",
                "PYTHONNOUSERSITE",
            )
        },
        "inputs": before,
        "config_sha256": digest(config),
        "config": config.read_text(encoding="utf-8"),
        "checker_environment": "TY_ and PYREFLY_ overrides and PYTHONPATH removed",
        "voiage": {"version": "3.1.0", "dependency_lock_sha256": digest(ROOT / "engineering/advisory.lock")},
        "comparison": comparison,
        "fixtures": fixture_results,
    }
    (output / "receipt.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    failures = {name: fatal_codes([item["code"] for item in entries]) for name, entries in reports.items()}
    if any(failures.values()):
        msg = f"Required imports or syntax could not be resolved: {failures}"
        raise RuntimeError(msg)
    print(f"Advisory reports: {output.relative_to(ROOT)}")  # noqa: T201 -- CLI receipt location.


if __name__ == "__main__":
    run()
