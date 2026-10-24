"""Maintained Nox/uv harness; configurations are not evidence of execution."""
from pathlib import Path

import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["tests", "quality"]
OUT = Path("outputs/engineering")


def environment(session):
    """Keep published numerical pins; capture the actually installed environment."""
    session.env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONHASHSEED="0")
    if Path("engineering/requirements.lock").is_file():
        session.install("--require-hashes", "-r", "engineering/requirements.lock")
    else:
        session.log("Reference pins only: transitive hash-lock qualification remains open")
        session.install("-r", "requirements.lock", "-r", "engineering/test-requirements.txt")
    session.install("--no-deps", "-e", ".")
    OUT.mkdir(parents=True, exist_ok=True)
    python = session.run("python", "-c", "import sys;print(sys.executable)", silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error("Could not resolve the isolated interpreter")
    session.run("uv", "pip", "check", "--python", python.strip(), external=True)


@nox.session
def tests(session):
    """Full suite, mandatory Hypothesis import, branch coverage and machine receipts."""
    environment(session)
    session.run("python", "-c", "import hypothesis, jsonschema; print('required test libraries loaded')")
    session.run("python", "-m", "coverage", "run", "--branch", "--source=src", "-m", "pytest",
                "-q", "--strict-markers", "--junitxml=outputs/engineering/junit.xml", *session.posargs)
    session.run("python", "-m", "coverage", "json", "-o", "outputs/engineering/coverage.json")
    session.run("python", "-m", "coverage", "report", "--fail-under=90")
    session.run("python", "-c", "import importlib.metadata as m,json,sys; "
                "from pathlib import Path; "
                "Path('outputs/engineering/environment.json').write_text("
                "json.dumps({'python':sys.version,'distributions':sorted("
                "(d.metadata['Name'],d.version) for d in m.distributions())},indent=2))")


@nox.session
def quality(session):
    """Strict new harness scope; fatal syntax/name rules cover all research code."""
    environment(session)
    session.install("ruff==0.16.8", "basedpyright==1.39.9")
    session.run("ruff", "check", "--isolated", "--select", "E9,F63,F7,F82", "src", "scripts")
    session.run("ruff", "check", "--config", "engineering/ruff.toml", "scripts/context_bundle.py")
    session.run("basedpyright", "--project", "engineering/basedpyright.json")


@nox.session
def strict_all(session):
    """Whole-repository strict debt audit; failures are visible, never auto-baselined."""
    environment(session)
    session.install("ruff==0.16.8", "basedpyright==1.39.9")
    session.run("ruff", "check", "--select", "ALL", "src", "scripts")
    session.run("basedpyright", "--project", "engineering/basedpyright-all.json")


@nox.session
def reproduce(session):
    """Preserve the existing full scientific runners and their own integrity checks."""
    environment(session)
    session.run("python", "scripts/verify.py")
    for module, destination in [("tobac.run", "m1"), ("tobac.m2", "m2")]:
        args = ["python", "-m", module, "--out", f"outputs/replay_{destination}"]
        if module == "tobac.m2":
            args.append("--grid-check")
        session.run(*args)
        session.run("python", "scripts/verify.py", f"outputs/replay_{destination}")
    for stem in ["release_calibration", "empirical_longitudinal"]:
        destination = f"outputs/replay_{stem}"
        session.run("python", f"scripts/run_{stem}.py", "--out", destination)
        session.run("python", f"scripts/verify_{stem}.py", destination)


@nox.session
def security(session):
    """Scan workflow security and resolved packages; no auto-fix or ignored advisories."""
    environment(session)
    session.install("pip-audit==2.10.1", "zizmor==1.31.1")
    session.run("zizmor", "--offline", ".github/workflows")
    session.run("pip-audit", "--skip-editable", "--format", "cyclonedx-json", "--output", str(OUT / "sbom.json"))


@nox.session
def lock(session):
    """Resolve a real universal hash lock; no invented hashes or automatic publication."""
    session.run("uv", "pip", "compile", "engineering/requirements.in", "--universal",
                "--generate-hashes", "--python-version", "3.12", "--output-file", "engineering/requirements.lock", external=True)


@nox.session
def package(session):
    """Internal release candidate only; fail closed without a generated hash lock."""
    if not Path("engineering/requirements.lock").is_file():
        session.error("Generate/review the hash lock with nox -s lock before release")
    python = session.run("python", "-c", "import sys;print(sys.executable)", silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error("Could not resolve the isolated interpreter")
    session.run("uv", "pip", "sync", "--python", python.strip(), "--require-hashes",
                "engineering/requirements.lock", external=True)
    session.run("uv", "build", "--python", python.strip(), "--no-build-isolation",
                "--out-dir", "outputs/release-candidate", external=True)


@nox.session
def mutation(session):
    """Focused mutation campaign using mutmut, not hand-edited production changes."""
    environment(session)
    session.install("mutmut==3.7.0")
    session.run("mutmut", "run", "tobac.supply*")
    session.run("mutmut", "results")


@nox.session
def profile(session):
    """Profile before selecting JAX/Rust acceleration; no AI optimisation service."""
    environment(session)
    session.install("scalene==2.4.0")
    session.run("scalene", "--cpu-only", "--json", "--outfile", str(OUT / "scalene.json"),
                "scripts/run_empirical_longitudinal.py", "--out", "outputs/profile_empirical", "--quick")


@nox.session
def canary(session):
    """Isolated latest/pre-release numerical ecosystem; never overwrite reference pins."""
    session.env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONPATH="src")
    session.install("--pre", "numpy", "scipy", "pandas", "matplotlib", "pytest",
                    "hypothesis", "jsonschema", "PyYAML")
    # Deliberately source-only: the installed research distribution pins the reference stack.
    session.run("python", "-m", "pytest", "-q", "--strict-markers")
