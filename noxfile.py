"""Nox/uv execution with source-bound locks; configuration is not qualification."""
import os
from pathlib import Path
import sys

import nox
from nox.command import CommandFailed

nox.options.default_venv_backend = 'uv'
nox.options.sessions = ['tests', 'quality']
ROOT = Path(__file__).resolve().parent
OUT = Path('outputs/engineering')


def environment(session, profile='runtime', require_lock=False):
    """Exact sync when locked; explicit bootstrap only outside release qualification."""
    if profile not in {'runtime', 'audit'}:
        session.error('Unknown environment profile')
    if profile == 'audit' and sys.platform != 'linux':
        session.error('Audit-tool profile is Linux-only; use runtime tests on other platforms')
    session.env.update(OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg', PYTHONHASHSEED='0')
    name = 'requirements.lock' if profile == 'runtime' else 'audit.lock'
    lock = ROOT / 'engineering' / name
    receipt = lock.with_suffix('.lock.json')
    mandatory = require_lock or os.environ.get('TOBAC_REQUIRE_LOCK') == '1'
    # A partial or stale lock is an error, never permission to silently fall back.
    if lock.exists() or receipt.exists() or mandatory:
        if not lock.is_file() or not receipt.is_file():
            session.error('Both generated lock and matching receipt are required')
        session.run('python', 'scripts/lock_receipt.py', 'verify', '--profile', profile,
                    '--path', f'engineering/{name}')
        python = session.run('python', '-c', 'import sys;print(sys.executable)', silent=True)
        if not isinstance(python, str) or not python.strip():
            session.error('Could not resolve the isolated interpreter')
        if profile == 'audit':
            session.run('python', '-c', 'import sys; assert sys.version_info[:2] == (3, 13)')
        session.run('uv', 'pip', 'sync', '--python', python.strip(), '--require-hashes',
                    str(lock), external=True)
    else:
        session.log('BOOTSTRAP ONLY: transitive hash-lock qualification is not established')
        requirements = ['-r', 'requirements.lock', '-r', 'engineering/test-requirements.txt',
                        '-r', 'engineering/build-requirements.txt']
        if profile == 'audit':
            requirements += ['-r', 'engineering/tools-requirements.txt']
        session.install(*requirements)
    # Never invoke an isolated floating build backend or install extra tools after the lock.
    session.install('--no-deps', '--no-build-isolation', '-e', '.')
    OUT.mkdir(parents=True, exist_ok=True)
    python = session.run('python', '-c', 'import sys;print(sys.executable)', silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error('Could not resolve the isolated interpreter')
    session.run('uv', 'pip', 'check', '--python', python.strip(), external=True)
    session.run('python', '-c', "import importlib.metadata as m,json,sys; from pathlib import Path; "
                "Path('outputs/engineering/environment.json').write_text(json.dumps("
                "{'python':sys.version,'distributions':sorted((d.metadata['Name'],d.version) "
                "for d in m.distributions())},indent=2))")


def run_all_checks(session, commands):
    """Execute independent audits, preserving an overall failure if any command fails."""
    failed = []
    for command in commands:
        try:
            session.run(*command)
        except CommandFailed:
            failed.append(command[0])
    if failed:
        session.error('Failed independent checks: ' + ', '.join(failed))


@nox.session
def tests(session):
    environment(session)
    session.run('python', '-c', 'import hypothesis, jsonschema; print("required test libraries loaded")')
    session.run('python', '-m', 'coverage', 'run', '--branch', '--source=src', '-m', 'pytest',
                '-q', '--strict-markers', '--junitxml=outputs/engineering/junit.xml', *session.posargs)
    session.run('python', '-m', 'coverage', 'json', '-o', 'outputs/engineering/coverage.json')
    session.run('python', '-m', 'coverage', 'report', '--fail-under=90')


@nox.session
def quality(session):
    environment(session, profile='audit')
    run_all_checks(session, [
        ['ruff', 'check', '--isolated', '--select', 'E9,F63,F7,F82', 'src', 'scripts'],
        ['ruff', 'check', '--config', 'engineering/ruff.toml', 'scripts/context_bundle.py'],
        ['basedpyright', '--project', 'engineering/basedpyright.json'],
    ])


@nox.session
def strict_all(session):
    environment(session, profile='audit')
    run_all_checks(session, [
        ['ruff', 'check', '--select', 'ALL', 'src', 'scripts'],
        ['basedpyright', '--project', 'engineering/basedpyright-all.json'],
    ])


@nox.session
def reproduce(session):
    environment(session)
    session.run('python', 'scripts/verify.py')
    for module, destination in [('tobac.run', 'm1'), ('tobac.m2', 'm2')]:
        args = ['python', '-m', module, '--out', f'outputs/replay_{destination}']
        if module == 'tobac.m2':
            args.append('--grid-check')
        session.run(*args)
        session.run('python', 'scripts/verify.py', f'outputs/replay_{destination}')
    for stem in ['release_calibration', 'empirical_longitudinal']:
        destination = f'outputs/replay_{stem}'
        session.run('python', f'scripts/run_{stem}.py', '--out', destination)
        session.run('python', f'scripts/verify_{stem}.py', destination)


@nox.session
def security(session):
    environment(session, profile='audit')
    run_all_checks(session, [
        ['zizmor', '--offline', '.github/workflows'],
        ['pip-audit', '--skip-editable', '--format', 'cyclonedx-json', '--output', str(OUT / 'sbom.json')],
    ])


@nox.session
def lock(session):
    """Produce review candidates, not automatic trusted locks or source commits."""
    for profile in ['runtime', 'audit']:
        session.run('python', 'scripts/lock_receipt.py', 'generate', '--profile', profile,
                    '--path', 'outputs/engineering/lock-candidate')


@nox.session
def package(session):
    """Build an internal candidate only after exact locked installation."""
    environment(session, require_lock=True)
    python = session.run('python', '-c', 'import sys;print(sys.executable)', silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error('Could not resolve the isolated interpreter')
    session.run('uv', 'build', '--python', python.strip(), '--no-build-isolation',
                '--out-dir', 'outputs/release-candidate', external=True)


@nox.session
def mutation(session):
    environment(session, profile='audit')
    session.run('mutmut', 'run', 'tobac.supply*')
    session.run('mutmut', 'results')


@nox.session
def profile(session):
    environment(session, profile='audit')
    session.run('scalene', '--cpu-only', '--json', '--outfile', str(OUT / 'scalene.json'),
                'scripts/run_empirical_longitudinal.py', '--out', 'outputs/profile_empirical', '--quick')


@nox.session
def canary(session):
    """Latest/pre-release source-only experiment; cannot qualify the reference environment."""
    session.env.update(OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg', PYTHONPATH='src')
    session.install('--pre', 'numpy', 'scipy', 'pandas', 'matplotlib', 'pytest',
                    'hypothesis', 'jsonschema', 'PyYAML')
    session.run('python', '-c', 'import hypothesis, jsonschema; print("canary dependencies loaded")')
    session.run('python', '-m', 'pytest', '-q', '--strict-markers')
