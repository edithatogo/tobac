"""Nox/uv execution with source-bound locks; configuration is not qualification."""

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from uuid import uuid4

import nox
from nox.command import CommandFailed

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["tests", "quality"]
ROOT = Path(__file__).resolve().parent
OUT = Path("outputs/engineering")
# Measured 61.7% on src/tobac/supply.py at main 5ab361b. A floor below the measured
# score converts a silent success into a regression alarm without asserting adequacy.
MUTATION_MINIMUM_PERCENT = "60"


def environment(session: nox.Session, profile: str = "runtime", *, require_lock: bool = False) -> None:
    """Exact sync when locked; explicit bootstrap only outside release qualification."""
    if profile not in {"runtime", "audit", "clustering"}:
        session.error("Unknown environment profile")
    if profile == "audit" and sys.platform != "linux":
        session.error("Audit-tool profile is Linux-only; use runtime tests on other platforms")
    session.env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONHASHSEED="0")
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    name = {"runtime": "requirements.lock", "audit": "audit.lock", "clustering": "clustering.lock"}[profile]
    lock = ROOT / "engineering" / name
    receipt = lock.with_suffix(".lock.json")
    mandatory = require_lock or os.environ.get("TOBAC_REQUIRE_LOCK") == "1"
    # A partial or stale lock is an error, never permission to silently fall back.
    if lock.exists() or receipt.exists() or mandatory:
        if not lock.is_file() or not receipt.is_file():
            session.error("Both generated lock and matching receipt are required")
        session.run(
            "python",
            "scripts/lock_receipt.py",
            "verify",
            "--profile",
            profile,
            "--path",
            f"engineering/{name}",
        )
        python = session.run("python", "-c", "import sys;print(sys.executable)", silent=True)
        if not isinstance(python, str) or not python.strip():
            session.error("Could not resolve the isolated interpreter")
        if profile == "audit":
            session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
        session.run(
            "uv", "pip", "sync", "--python", python.strip(), "--require-hashes", str(lock), external=True
        )
    else:
        session.log("BOOTSTRAP ONLY: transitive hash-lock qualification is not established")
        requirements = [
            "-r",
            "requirements.lock",
            "-r",
            "engineering/test-requirements.txt",
            "-r",
            "engineering/build-requirements.txt",
        ]
        if profile == "audit":
            requirements += ["-r", "engineering/tools-requirements.txt"]
        session.install(*requirements)
    # Never invoke an isolated floating build backend or install extra tools after the lock.
    session.install("--no-deps", "--no-build-isolation", "-e", ".")
    OUT.mkdir(parents=True, exist_ok=True)
    python = session.run("python", "-c", "import sys;print(sys.executable)", silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error("Could not resolve the isolated interpreter")
    session.run("uv", "pip", "check", "--python", python.strip(), external=True)
    session.run(
        "python",
        "-c",
        "import importlib.metadata as m,json,sys; from pathlib import Path; "
        "Path('outputs/engineering/environment.json').write_text(json.dumps("
        "{'python':sys.version,'distributions':sorted((d.metadata['Name'],d.version) "
        "for d in m.distributions())},indent=2))",
    )


def audit_lock_present() -> bool:
    """Check whether a reviewed Linux audit lock is committed and must be honoured."""
    return (ROOT / "engineering" / "audit.lock").is_file()


@nox.session(python="3.15.2")
def clustering(session: nox.Session) -> None:
    """Qualify synthetic sensitivity/clustering; never process empirical observations."""
    environment(session, profile="clustering", require_lock=True)
    session.env["OMP_NUM_THREADS"] = "1"
    packet = OUT / f"synthetic-clustering-{uuid4().hex}"
    session.run(
        "python",
        "-m",
        "pytest",
        "-q",
        "tests/engineering/test_clustering_qualification.py",
        "tests/engineering/test_clustering_packet.py",
        "tests/test_workstream_integration.py",
    )
    session.run(
        "python",
        "scripts/qualify_sensitivity_clustering.py",
        "--out",
        str(packet),
        "--lock",
        "engineering/clustering.lock",
    )
    session.run("python", "scripts/verify_sensitivity_clustering.py", "--out", str(packet))


def audit_tools(session: nox.Session) -> None:
    """Resolve audit tools for this host when the Linux audit lock is unusable.

    The Linux profile stays authoritative wherever it can be installed. On other hosts the
    reviewed tool pins are resolved natively so the same checks actually run, and the session
    says plainly that this is not the locked release profile.
    """
    if sys.platform == "linux":
        environment(session, profile="audit")
        return
    if os.environ.get("TOBAC_REQUIRE_LOCK") == "1":
        session.error("Locked qualification requires the Linux audit lock; not available here")
    session.log(
        "NATIVE AUDIT: host-resolved tools from engineering/tools-requirements.txt; "
        "NOT the Linux audit lock, hash-checked install or release qualification"
        + ("" if audit_lock_present() else "; no audit lock is committed yet")
    )
    session.env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONHASHSEED="0")
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    # The audit checks import the project and jsonschema, so the ordinary dependency set is
    # required too; installing only the tool pins leaves basedpyright unable to resolve imports.
    session.install(
        "-r",
        "requirements.lock",
        "-r",
        "engineering/test-requirements.txt",
        "-r",
        "engineering/build-requirements.txt",
        "-r",
        "engineering/tools-requirements.txt",
    )
    session.install("--no-deps", "--no-build-isolation", "-e", ".")
    OUT.mkdir(parents=True, exist_ok=True)
    return


def run_all_checks(session: nox.Session, commands: list[list[str]]) -> None:
    """Execute independent audits, preserving an overall failure if any command fails."""
    failed = []
    for command in commands:
        try:
            session.run(*command)
        except CommandFailed:
            failed.append(command[0])
    if failed:
        session.error("Failed independent checks: " + ", ".join(failed))


def verify_lineage(session: nox.Session, label: str, *names: str) -> None:
    """Verify accepted native evidence before installing or executing the workload."""
    selection = [arg for name in names for arg in ("--runner", name)]
    session.run(
        "python",
        "scripts/qualify_integrations.py",
        "--mode",
        "lineage",
        *selection,
        "--out",
        str(OUT / f"lineage-{label}-{uuid4().hex}.json"),
    )


def verify_evidence(session: nox.Session, label: str) -> None:
    """Inventory and preserved-byte gate; not source applicability or CSL validation."""
    session.run(
        "python",
        "scripts/qualify_integrations.py",
        "--mode",
        "inventory",
        "--out",
        f"outputs/engineering/evidence-{label}-{uuid4().hex}.json",
    )


@nox.session(python="3.15.2")
def evidence(session: nox.Session) -> None:
    """Offline standard-library check; no package install or empirical conditioning."""
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    verify_evidence(session, "evidence")


@nox.session(python="3.15.2")
def tests(session: nox.Session) -> None:
    """Run the full source-coverage test suite in the qualified environment."""
    verify_evidence(session, "tests")
    verify_lineage(session, "tests")
    coverage_root = OUT / "coverage-data"
    coverage_root.mkdir(parents=True, exist_ok=True)
    session.env["COVERAGE_FILE"] = str((ROOT / coverage_root / uuid4().hex).resolve())
    environment(session)
    session.run("python", "-c", 'import hypothesis, jsonschema; print("required test libraries loaded")')
    session.run(
        "python",
        "-m",
        "coverage",
        "run",
        "--branch",
        "--source=src",
        "-m",
        "pytest",
        "-q",
        "--strict-markers",
        "--junitxml=outputs/engineering/junit.xml",
        *session.posargs,
    )
    session.run("python", "-m", "coverage", "json", "-o", "outputs/engineering/coverage.json")
    session.run("python", "-m", "coverage", "report", "--fail-under=90")


@nox.session(python="3.15.2")
def quality(session: nox.Session) -> None:
    """Run baseline lint and component typing checks."""
    audit_tools(session)
    run_all_checks(
        session,
        [
            ["ruff", "check", "--isolated", "--select", "E9,F63,F7,F82", "src", "scripts"],
            ["ruff", "check", "--config", "engineering/ruff.toml", "scripts/context_bundle.py"],
            [
                "basedpyright",
                "--pythonpath",
                str(Path(session.bin) / ("python.exe" if os.name == "nt" else "python")),
                "--project",
                "engineering/basedpyright.json",
            ],
            [
                "basedpyright",
                "--pythonpath",
                str(Path(session.bin) / ("python.exe" if os.name == "nt" else "python")),
                "--project",
                "engineering/bp_longitudinal.json",
            ],
        ],
    )


@nox.session(python="3.15.2")
def types_longitudinal(session: nox.Session) -> None:
    """Strict typing of the empirical runner using this session's interpreter."""
    audit_tools(session)
    session.run(
        "basedpyright",
        "--pythonpath",
        str(Path(session.bin) / ("python.exe" if os.name == "nt" else "python")),
        "--project",
        "engineering/bp_longitudinal.json",
    )


@nox.session(python="3.15.2")
def strict_all(session: nox.Session) -> None:
    """Lint and format all maintained Python and check whole-source typing."""
    audit_tools(session)
    session.run("python", "-m", "pytest", "-q", "tests/engineering/test_ruff_policy.py")
    run_all_checks(
        session,
        [
            [
                "ruff",
                "check",
                "--config",
                "engineering/ruff.toml",
                "src",
                "scripts",
                "tests",
                "noxfile.py",
                "engineering/typings",
            ],
            [
                "ruff",
                "format",
                "--check",
                "--config",
                "engineering/ruff.toml",
                "src",
                "scripts",
                "tests",
                "noxfile.py",
            ],
            [
                "basedpyright",
                "--pythonpath",
                str(Path(session.bin) / ("python.exe" if os.name == "nt" else "python")),
                "--project",
                "engineering/basedpyright-all.json",
            ],
        ],
    )


@nox.session(python="3.15.2")
def source_handoff(session: nox.Session) -> None:
    """Validate source/observation declarations; blocked scientific gaps remain explicit."""
    environment(session)
    session.run(
        "python",
        "scripts/source_handoff.py",
        "--out",
        str(OUT / f"source-handoff-{uuid4().hex}.json"),
        *session.posargs,
    )


@nox.session(python="3.15.2")
def reproduce(session: nox.Session) -> None:
    """Replay the numerical reference and verify its outputs."""
    verify_evidence(session, "reproduce")
    verify_lineage(session, "reproduce")
    environment(session)
    session.run(
        "python",
        "scripts/source_handoff.py",
        "--out",
        str(OUT / f"source-handoff-reproduction-{uuid4().hex}.json"),
    )
    session.run("python", "scripts/verify.py")
    replay_root = OUT / "replays" / uuid4().hex
    session.run(
        "python",
        "scripts/qualify_m2_pathway.py",
        "--out",
        str(replay_root / "m2-pathway.json"),
    )
    for module, destination in [("tobac.run", "m1"), ("tobac.m2", "m2"), ("tobac.research.runner", "m3")]:
        args = ["python", "-m", module, "--out", str(replay_root / destination)]
        if module == "tobac.m2":
            args.append("--grid-check")
        session.run(*args)
        session.run("python", "scripts/verify.py", str(replay_root / destination))
    for stem in ["release_calibration", "empirical_longitudinal"]:
        destination = str(replay_root / stem)
        session.run("python", f"scripts/run_{stem}.py", "--out", destination)
        session.run("python", f"scripts/verify_{stem}.py", destination)
    session.run(
        "python",
        "scripts/check_longitudinal_results.py",
        "--empirical",
        str(replay_root / "empirical_longitudinal"),
        "--releases",
        str(replay_root / "release_calibration"),
    )
    synthesis_view = replay_root / "synthesis-validation-view"
    session.run(
        "python",
        "scripts/prepare_synthesis_replay.py",
        "--replay",
        str(replay_root),
        "--out",
        str(synthesis_view),
    )
    session.run(
        "python",
        "scripts/qualify_m2_synthesis.py",
        "--replay",
        str(synthesis_view),
        "--out",
        str(replay_root / "m2-synthesis.json"),
    )

    publication = str(replay_root / "m2_publication")
    session.run("python", "scripts/run_m2_publication.py", "--out", publication, "--grid-check")
    session.run("python", "scripts/verify.py", publication)
    robustness = str(replay_root / "m2_robustness")
    session.run("python", "scripts/run_m2_robustness.py", "--out", robustness)
    session.run("python", "scripts/verify.py", robustness)
    session.run("python", "scripts/qualify_publication_replay.py", "--out", str(replay_root / "paper_replay"))


@nox.session(python="3.15.2")
def security(session: nox.Session) -> None:
    """Run dependency and workflow security checks."""
    audit_tools(session)
    session.run("python", "scripts/check_security_findings.py")
    run_all_checks(
        session,
        [
            ["zizmor", "--offline", "--persona", "pedantic", ".github/workflows"],
            [
                "pip-audit",
                "--skip-editable",
                "--format",
                "cyclonedx-json",
                "--output",
                str(OUT / "sbom.json"),
            ],
        ],
    )


@nox.session(python="3.15.2")
def publication(session: nox.Session) -> None:
    """Qualify the public boundary and pinned native macOS scanners."""
    environment(session)
    session.run("python", "-m", "pytest", "-q", "tests/engineering/test_publication_boundary.py")
    session.run("python", "scripts/check_publication_security.py")


@nox.session(python="3.15.2")
def qualification(session: nox.Session) -> None:
    """Reopen the native evidence before running enforcement regression tests."""
    verify_lineage(session, "qualification")
    environment(session)
    session.run(
        "python",
        "-m",
        "pytest",
        "-q",
        "tests/engineering/test_qualification_check.py",
        "tests/engineering/test_lineage_gate.py",
    )


@nox.session(python="3.15.2")
def lock(session: nox.Session) -> None:
    """Produce review candidates, not automatic trusted locks or source commits."""
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    destination = session.posargs[0] if session.posargs else "outputs/engineering/lock-candidate"
    for profile in ["runtime", "audit"]:
        session.run(
            "python", "scripts/lock_receipt.py", "generate", "--profile", profile, "--path", destination
        )


@nox.session(python="3.15.2")
def package(session: nox.Session) -> None:
    """Build internal source/wheel candidates after exact locked installation."""
    verify_evidence(session, "package")
    verify_lineage(session, "package")
    environment(session, require_lock=True)
    python = session.run("python", "-c", "import sys;print(sys.executable)", silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error("Could not resolve the isolated interpreter")
    session.run(
        "uv",
        "build",
        "--no-sources",
        "--python",
        python.strip(),
        "--no-build-isolation",
        "--out-dir",
        "outputs/release-candidate",
        external=True,
    )


@nox.session(python="3.15.2")
def mutation(session: nox.Session) -> None:
    """Mutation score gate; mutmut enforces no threshold of its own."""
    audit_tools(session)
    session.run(
        "python",
        "scripts/check_mutation_score.py",
        "--prepare",
        "--receipt",
        "outputs/engineering/mutation-input.json",
    )
    session.run("mutmut", "run", "--max-children", "2", "tobac.supply*")
    session.run("mutmut", "results")
    session.run(
        "python",
        "scripts/check_mutation_score.py",
        "--minimum",
        MUTATION_MINIMUM_PERCENT,
        "--receipt",
        "outputs/engineering/mutation-input.json",
    )


@nox.session(python="3.15.2")
def profile(session: nox.Session) -> None:
    """Profile the empirical quick runner with the maintained Scalene tool."""
    audit_tools(session)
    # Scalene 2.4 replaced the flat CLI with subcommands; program arguments must follow '---'.
    session.run(
        "scalene",
        "run",
        "--cpu-only",
        "--outfile",
        str(OUT / "scalene.json"),
        "scripts/run_empirical_longitudinal.py",
        "---",
        "--out",
        "outputs/profile_empirical",
        "--quick",
    )


@nox.session(python="3.15.2")
def canary(session: nox.Session) -> None:
    """Latest/pre-release source-only experiment; cannot qualify the reference environment."""
    session.env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONPATH="src")
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    session.install(
        "--pre", "numpy", "scipy", "polars", "matplotlib", "pytest", "hypothesis", "jsonschema", "PyYAML"
    )
    session.run("python", "-c", 'import hypothesis, jsonschema; print("canary dependencies loaded")')
    session.run("python", "-m", "pytest", "-q", "--strict-markers")


@nox.session(python="3.15.2")
def research_m3(session: nox.Session) -> None:
    """M3 uses the existing reference environment and preserves its lock gates."""
    verify_evidence(session, "research_m3")
    verify_lineage(session, "research_m3", "m3")
    environment(session)
    session.run("python", "-m", "pytest", "-q", "tests/m3", "tests/test_workstream_integration.py")
    destination = "outputs/replay_m3"
    if Path(destination).exists():
        destination = str(OUT / "m3-runs" / uuid4().hex)
    session.run("python", "-m", "tobac.research.runner", "--out", destination)
    session.run("python", "scripts/verify.py", destination)


@nox.session(python="3.15.2")
def voiage(session: nox.Session) -> None:
    """Qualify the released Polars producer against all existing reference oracles."""
    session.env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONHASHSEED="0")
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    session.run(
        "python",
        "scripts/lock_receipt.py",
        "verify",
        "--profile",
        "voiage",
        "--path",
        "engineering/voiage.lock",
    )
    python = str(Path(session.bin).resolve() / "python")
    session.run(
        "uv", "pip", "sync", "--python", python, "--require-hashes", "engineering/voiage.lock", external=True
    )
    session.install("--no-deps", "--no-build-isolation", "-e", ".")
    session.run("uv", "pip", "check", "--python", python, external=True)
    session.run(
        "python",
        "-c",
        "from importlib.metadata import version; "
        "from importlib.util import find_spec; assert version('voiage') == '3.1.0'; "
        "assert find_spec('pandas') is None and find_spec('xarray') is None",
    )
    default_folder = "voiage-polars-candidate" if session.name == "voiage_polars_candidate" else "voiage"
    base = Path(session.posargs[0]).resolve() if session.posargs else (ROOT / OUT / default_folder).resolve()
    run = base / uuid4().hex
    run.mkdir(parents=True)
    session.run(
        "python",
        "-m",
        "pytest",
        "-q",
        "tests/m3",
        "tests/engineering/test_voiage_installed.py",
        "tests/test_workstream_integration.py",
        "tests/engineering/test_evidence_interchange.py",
    )
    session.run("python", "scripts/qualify_interchange.py", "--out", str(run / "interchange"))
    session.run(
        "python",
        "scripts/qualify_integrations.py",
        "--mode",
        "voiage",
        "--out",
        str(run / "equal-weight.json"),
    )
    session.run("python", "-m", "tobac.research.qualification", "--out", str(run / "weighted.json"))
    record = {
        "version": "3.1.0",
        "dependency_lock_sha256": hashlib.sha256((ROOT / "engineering/voiage.lock").read_bytes()).hexdigest(),
        "scope": "Published Polars producer; original numerical and interchange oracles retained",
        "environment": session.run("uv", "pip", "freeze", "--python", python, silent=True, external=True),
    }
    (run / "build-receipt.json").write_text(json.dumps(record, indent=2) + "\n")
    receipt_dir = ROOT / OUT / ("voiage-receipts-" + run.name)
    receipt_dir.mkdir(parents=True)
    for name in ["build-receipt.json", "equal-weight.json", "weighted.json"]:
        shutil.copyfile(run / name, receipt_dir / name)
    shutil.copytree(run / "interchange", receipt_dir / "interchange")


@nox.session(python="3.15.2")
def moh_workbook(session: nox.Session) -> None:
    """Explicit local native-producer verification; no acquisition or source mutation."""
    environment(session)
    session.run("python", "scripts/qualify_moh_workbook.py", *session.posargs)


@nox.session(python="3.15.2")
def native_moh_lineage(session: nox.Session) -> None:
    """Consume an explicit repo-local installed producer; never mutate its live estate."""
    if not session.posargs:
        session.error("Supply the consumer-owned producer Python followed by extraction arguments")
    selected = Path(session.posargs[0]).absolute()
    if not selected.is_relative_to(ROOT):
        session.error("Select a consumer-owned repo-local producer environment")
    session.env["PYTHONPATH"] = str(ROOT / "src")
    session.run(str(selected), "scripts/extract_moh_lineage.py", *session.posargs[1:], external=True)


@nox.session(python="3.15.2")
def native_shine_lineage(session: nox.Session) -> None:
    """Consume an explicit repo-local installed producer; never mutate its live estate."""
    if not session.posargs:
        session.error("Supply the consumer-owned producer Python followed by extraction arguments")
    selected = Path(session.posargs[0]).absolute()
    if not selected.is_relative_to(ROOT):
        session.error("Select a consumer-owned repo-local producer environment")
    session.env["PYTHONPATH"] = str(ROOT / "src")
    session.run(str(selected), "scripts/extract_shine_lineage.py", *session.posargs[1:], external=True)


@nox.session(python="3.15.2")
def product_reconciliation(session: nox.Session) -> None:
    """Recompute dated source-bound product tables; no source acquisition or conditioning."""
    environment(session)
    session.run(
        "python",
        "scripts/reconcile_products_2025.py",
        "--out",
        "outputs/engineering/product-reconciliation",
        *session.posargs,
    )


@nox.session(python="3.15.2")
def clean_package(session: nox.Session) -> None:
    """Real artifact execution outside source and sibling checkouts."""
    verify_lineage(session, "clean_package")
    environment(session, require_lock=True)
    destination = str(OUT / "clean-package" / uuid4().hex)
    session.run("python", "scripts/qualify_clean_package.py", "--out", destination)


@nox.session(python="3.15.2")
def ecosystem(session: nox.Session) -> None:
    """Probe natively with a hash-bound, already qualified macOS Voiage wheel."""
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    if len(session.posargs) != 1:
        session.error("Supply the qualified published macOS Voiage wheel path")
    wheel = Path(session.posargs[0]).resolve()
    expected = json.loads((ROOT / "integration/voiage_published_20261106.json").read_text())["wheel_sha256"]
    if not wheel.is_file() or hashlib.sha256(wheel.read_bytes()).hexdigest() != expected:
        session.error("Voiage wheel differs from the qualified artifact")
    session.run(
        "python",
        "scripts/lock_receipt.py",
        "verify",
        "--profile",
        "ecosystem",
        "--path",
        "engineering/ecosystem.lock",
    )
    python = str(Path(session.bin).resolve() / "python")
    session.env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONHASHSEED="0")
    session.run(
        "uv",
        "pip",
        "sync",
        "--python",
        python,
        "--require-hashes",
        "engineering/ecosystem.lock",
        external=True,
    )
    session.install("--no-deps", "--no-build-isolation", "-e", ".")
    session.run(
        "uv",
        "pip",
        "install",
        "--python",
        python,
        "--no-index",
        "--require-hashes",
        "-r",
        "engineering/ecosystem.lock",
        "voiage @ " + wheel.as_uri() + "#sha256=" + expected,
        external=True,
    )
    session.run("uv", "pip", "check", "--python", python, external=True)
    destination = str(OUT / "ecosystem" / ("native-" + uuid4().hex + ".json"))
    session.run("python", "scripts/qualify_ecosystem.py", "--out", destination)
    session.run("python", "scripts/qualify_interchange.py", "--out", str(OUT / "interchange" / uuid4().hex))
    session.run(
        "python",
        "-m",
        "pytest",
        "tests/engineering/test_evidence_interchange.py",
        "tests/test_workstream_integration.py",
        "tests/m3",
    )


@nox.session(python="3.15.2")
def recovery(session: nox.Session) -> None:
    """Actual runner interruption/resume and immutable-receipt comparison."""
    environment(session)
    session.run("python", "scripts/qualify_recovery.py", "--out", str(OUT / "recovery" / uuid4().hex))


@nox.session(python="3.15.2")
def voiage_polars_candidate(session: nox.Session) -> None:
    """Retain the command name while qualifying the now-published Polars producer."""
    # The unpublished 2.2 container build and its patched predecessor are historical.
    voiage(session)


@nox.session(python="3.15.2")
def voiage_published(session: nox.Session) -> None:
    """Qualify the hash-pinned published wheel with its genuine runtime dependencies."""
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    python = session.run("python", "-c", "import sys; print(sys.executable)", silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error("Cannot resolve selected interpreter")
    pin = json.loads((ROOT / "integration/voiage_published_20261106.json").read_text())
    wheel = (ROOT / OUT / "voiage-published" / pin["wheel"]).resolve()
    wheel.parent.mkdir(parents=True, exist_ok=True)
    session.run("curl", "--fail", "--location", "--output", str(wheel), pin["wheel_url"], external=True)
    if hashlib.sha256(wheel.read_bytes()).hexdigest() != pin["wheel_sha256"]:
        session.error("Published wheel checksum differs")
    lock = wheel.parent / "local-requirements.txt"
    lock.write_text(
        (ROOT / "engineering/voiage-published-requirements.txt")
        .read_text()
        .replace(pin["wheel_url"], wheel.as_uri()),
        encoding="utf-8",
    )
    session.run(
        "uv",
        "pip",
        "sync",
        "--python",
        python.strip(),
        "--require-hashes",
        str(lock),
        external=True,
    )
    session.run("uv", "pip", "check", "--python", python.strip(), external=True)
    session.env["PYTHONPATH"] = str(ROOT / "src")
    session.run(
        "python",
        "scripts/qualify_voiage_consumer.py",
        "--wheel",
        str(wheel),
        "--expected-version",
        "3.1.0",
        "--buffer-ownership",
        "--out",
        str(wheel.parent / ("qualification-" + uuid4().hex + ".json")),
    )


@nox.session(python="3.15.2")
def advisory_types(session: nox.Session) -> None:
    """Run isolated differential diagnostics with a pinned Voiage interface build."""
    OUT.mkdir(parents=True, exist_ok=True)
    session.env.update(
        OPENBLAS_NUM_THREADS="1",
        RAYON_NUM_THREADS="2",
        CARGO_BUILD_JOBS="2",
        PYTHONHASHSEED="0",
        PYTHONPATH="",
        PYTHONNOUSERSITE="1",
    )
    session.run("python", "-c", "import sys; assert sys.version_info[:3] == (3, 15, 2)")
    session.run(
        "python",
        "scripts/lock_receipt.py",
        "verify",
        "--profile",
        "advisory",
        "--path",
        "engineering/advisory.lock",
    )
    python = str(Path(session.bin) / "python")
    session.run(
        "uv",
        "pip",
        "sync",
        "--python",
        python,
        "--require-hashes",
        "engineering/advisory.lock",
        external=True,
    )
    session.install("--no-deps", "--no-build-isolation", "-e", ".")
    session.run("uv", "pip", "check", "--python", python, external=True)
    session.run("python", "scripts/advisory_types.py")
