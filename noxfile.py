"""Nox/uv execution with source-bound locks; configuration is not qualification."""
import os
from pathlib import Path
from uuid import uuid4
import sys

import nox
from nox.command import CommandFailed

nox.options.default_venv_backend = 'uv'
nox.options.sessions = ['tests', 'quality']
ROOT = Path(__file__).resolve().parent
OUT = Path('outputs/engineering')
# Measured 61.7% on src/tobac/supply.py at main 5ab361b. A floor below the measured
# score converts a silent success into a regression alarm without asserting adequacy.
MUTATION_MINIMUM_PERCENT = '60'


def environment(session, profile='runtime', require_lock=False):
    """Exact sync when locked; explicit bootstrap only outside release qualification."""
    if profile not in {'runtime', 'audit'}:
        session.error('Unknown environment profile')
    if profile == 'audit' and sys.platform != 'linux':
        session.error('Audit-tool profile is Linux-only; use runtime tests on other platforms')
    session.env.update(OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg', PYTHONHASHSEED='0')
    session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
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
            session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
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


def audit_lock_present():
    """True when a reviewed Linux audit lock is committed (then it must be honoured)."""
    return (ROOT / 'engineering' / 'audit.lock').is_file()


def audit_tools(session):
    """Resolve audit tools for this host when the Linux audit lock is unusable.

    The Linux profile stays authoritative wherever it can be installed. On other hosts the
    reviewed tool pins are resolved natively so the same checks actually run, and the session
    says plainly that this is not the locked release profile.
    """
    if sys.platform == 'linux':
        environment(session, profile='audit')
        return None
    if os.environ.get('TOBAC_REQUIRE_LOCK') == '1':
        session.error('Locked qualification requires the Linux audit lock; not available here')
    session.log('NATIVE AUDIT: host-resolved tools from engineering/tools-requirements.txt; '
                'NOT the Linux audit lock, hash-checked install or release qualification'
                + ('' if audit_lock_present() else '; no audit lock is committed yet'))
    session.env.update(OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg', PYTHONHASHSEED='0')
    session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
    # The audit checks import the project and jsonschema, so the ordinary dependency set is
    # required too; installing only the tool pins leaves basedpyright unable to resolve imports.
    session.install('-r', 'requirements.lock', '-r', 'engineering/test-requirements.txt',
                    '-r', 'engineering/build-requirements.txt',
                    '-r', 'engineering/tools-requirements.txt')
    session.install('--no-deps', '--no-build-isolation', '-e', '.')
    OUT.mkdir(parents=True, exist_ok=True)
    return None


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


def verify_evidence(session, label):
    """Inventory and preserved-byte gate; not source applicability or CSL validation."""
    session.run('python', 'scripts/qualify_integrations.py', '--mode', 'inventory',
                '--out', f'outputs/engineering/evidence-{label}-{uuid4().hex}.json')


@nox.session(python='3.15.1')
def evidence(session):
    """Offline standard-library check; no package install or empirical conditioning."""
    session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
    verify_evidence(session, 'evidence')


@nox.session(python='3.15.1')
def tests(session):
    verify_evidence(session, 'tests')
    coverage_root = OUT / 'coverage-data'
    coverage_root.mkdir(parents=True, exist_ok=True)
    session.env['COVERAGE_FILE'] = str((ROOT / coverage_root / uuid4().hex).resolve())
    environment(session)
    session.run('python', '-c', 'import hypothesis, jsonschema; print("required test libraries loaded")')
    session.run('python', '-m', 'coverage', 'run', '--branch', '--source=src', '-m', 'pytest',
                '-q', '--strict-markers', '--junitxml=outputs/engineering/junit.xml', *session.posargs)
    session.run('python', '-m', 'coverage', 'json', '-o', 'outputs/engineering/coverage.json')
    session.run('python', '-m', 'coverage', 'report', '--fail-under=90')


@nox.session(python='3.15.1')
def quality(session):
    audit_tools(session)
    run_all_checks(session, [
        ['ruff', 'check', '--isolated', '--select', 'E9,F63,F7,F82', 'src', 'scripts'],
        ['ruff', 'check', '--config', 'engineering/ruff.toml', 'scripts/context_bundle.py'],
        ['basedpyright', '--pythonpath', str(Path(session.bin) / ('python.exe' if os.name == 'nt' else 'python')), '--project', 'engineering/basedpyright.json'],
        ['basedpyright', '--pythonpath', str(Path(session.bin) / ('python.exe' if os.name == 'nt' else 'python')), '--project', 'engineering/bp_longitudinal.json'],
    ])


@nox.session(python='3.15.1')
def types_longitudinal(session):
    """Strict typing of the empirical runner using this session's interpreter."""
    audit_tools(session)
    session.run('basedpyright', '--pythonpath', str(Path(session.bin) / ('python.exe' if os.name == 'nt' else 'python')), '--project', 'engineering/bp_longitudinal.json')


@nox.session(python='3.15.1')
def strict_all(session):
    audit_tools(session)
    run_all_checks(session, [
        ['ruff', 'check', '--config', 'engineering/ruff.toml', 'src', 'scripts'],
        ['basedpyright', '--pythonpath', str(Path(session.bin) / ('python.exe' if os.name == 'nt' else 'python')), '--project', 'engineering/basedpyright-all.json'],
    ])


@nox.session(python='3.15.1')
def source_handoff(session):
    """Validate source/observation declarations; blocked scientific gaps remain explicit."""
    environment(session)
    session.run('python', 'scripts/source_handoff.py', '--out',
                'outputs/engineering/source-handoff.json', *session.posargs)


@nox.session(python='3.15.1')
def reproduce(session):
    verify_evidence(session, 'reproduce')
    environment(session)
    session.run('python', 'scripts/source_handoff.py', '--out',
                'outputs/engineering/source-handoff-reproduction.json')
    session.run('python', 'scripts/verify.py')
    replay_root = OUT / 'replays' / uuid4().hex
    for module, destination in [('tobac.run', 'm1'), ('tobac.m2', 'm2'), ('tobac.research.runner', 'm3')]:
        args = ['python', '-m', module, '--out', str(replay_root / destination)]
        if module == 'tobac.m2':
            args.append('--grid-check')
        session.run(*args)
        session.run('python', 'scripts/verify.py', str(replay_root / destination))
    for stem in ['release_calibration', 'empirical_longitudinal']:
        destination = str(replay_root / stem)
        session.run('python', f'scripts/run_{stem}.py', '--out', destination)
        session.run('python', f'scripts/verify_{stem}.py', destination)
    session.run('python', 'scripts/check_longitudinal_results.py',
                '--empirical', str(replay_root / 'empirical_longitudinal'),
                '--releases', str(replay_root / 'release_calibration'))


@nox.session(python='3.15.1')
def security(session):
    audit_tools(session)
    session.run('python', 'scripts/check_security_findings.py')
    run_all_checks(session, [
        ['zizmor', '--offline', '.github/workflows'],
        ['pip-audit', '--skip-editable', '--format', 'cyclonedx-json', '--output', str(OUT / 'sbom.json')],
    ])


@nox.session(python='3.15.1')
def lock(session):
    """Produce review candidates, not automatic trusted locks or source commits."""
    session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
    destination = session.posargs[0] if session.posargs else 'outputs/engineering/lock-candidate'
    for profile in ['runtime', 'audit']:
        session.run('python', 'scripts/lock_receipt.py', 'generate', '--profile', profile,
                    '--path', destination)


@nox.session(python='3.15.1')
def package(session):
    """Build an internal candidate only after exact locked installation."""
    verify_evidence(session, 'package')
    environment(session, require_lock=True)
    python = session.run('python', '-c', 'import sys;print(sys.executable)', silent=True)
    if not isinstance(python, str) or not python.strip():
        session.error('Could not resolve the isolated interpreter')
    session.run('uv', 'build', '--no-sources', '--python', python.strip(), '--no-build-isolation',
                '--out-dir', 'outputs/release-candidate', external=True)


@nox.session(python='3.15.1')
def mutation(session):
    """Mutation score gate; mutmut enforces no threshold of its own."""
    audit_tools(session)
    session.run('python', 'scripts/check_mutation_score.py', '--prepare',
                '--receipt', 'outputs/engineering/mutation-input.json')
    session.run('mutmut', 'run', 'tobac.supply*')
    session.run('mutmut', 'results')
    session.run('python', 'scripts/check_mutation_score.py',
                '--minimum', MUTATION_MINIMUM_PERCENT,
                '--receipt', 'outputs/engineering/mutation-input.json')


@nox.session(python='3.15.1')
def profile(session):
    audit_tools(session)
    # Scalene 2.4 replaced the flat CLI with subcommands; program arguments must follow '---'.
    session.run('scalene', 'run', '--cpu-only', '--outfile', str(OUT / 'scalene.json'),
                'scripts/run_empirical_longitudinal.py', '---',
                '--out', 'outputs/profile_empirical', '--quick')


@nox.session(python='3.15.1')
def canary(session):
    """Latest/pre-release source-only experiment; cannot qualify the reference environment."""
    session.env.update(OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg', PYTHONPATH='src')
    session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
    session.install('--pre', 'numpy', 'scipy', 'pandas', 'matplotlib', 'pytest',
                    'hypothesis', 'jsonschema', 'PyYAML')
    session.run('python', '-c', 'import hypothesis, jsonschema; print("canary dependencies loaded")')
    session.run('python', '-m', 'pytest', '-q', '--strict-markers')


@nox.session(python='3.15.1')
def research_m3(session):
    """M3 uses the existing reference environment and preserves its lock gates."""
    verify_evidence(session, 'research_m3')
    environment(session)
    session.run('python', '-m', 'pytest', '-q', 'tests/m3', 'tests/test_workstream_integration.py')
    session.run('python', '-m', 'tobac.research.runner', '--out', 'outputs/replay_m3')
    session.run('python', 'scripts/verify.py', 'outputs/replay_m3')


@nox.session(python='3.15.1')
def voiage(session):
    """Build a pinned, explicitly local-versioned Voiage compatibility candidate."""
    import hashlib
    import json
    import subprocess

    session.env.update(OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg', PYTHONHASHSEED='0')
    session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
    # Independent, input-bound dependency lock; the wheel still resolves its dependencies normally.
    session.run('python', 'scripts/lock_receipt.py', 'verify', '--profile', 'voiage',
                '--path', 'engineering/voiage.lock')
    python = str(Path(session.bin).resolve() / 'python')
    session.run('uv', 'pip', 'sync', '--python', python, '--require-hashes',
                'engineering/voiage.lock', external=True)
    session.install('--no-deps', '--no-build-isolation', '-e', '.')
    base = Path(session.posargs[0]).resolve() if session.posargs else (ROOT / OUT / 'voiage').resolve()
    run = base / uuid4().hex
    source, wheels = run / 'source', run / 'wheels'
    run.mkdir(parents=True)
    revision = '7af563c8cb373057d30662650b3f332f39e05b83'
    patch = ROOT / 'engineering/voiage-python315.patch'
    session.run('git', 'init', str(source), external=True)
    session.run('git', '-C', str(source), '-c', 'credential.helper=', 'fetch', '--depth=1',
                'https://github.com/edithatogo/voiage.git', revision, external=True)
    session.run('git', '-C', str(source), 'checkout', '--detach', 'FETCH_HEAD', external=True)
    fetched = session.run('git', '-C', str(source), 'rev-parse', 'HEAD', silent=True, external=True)
    if not isinstance(fetched, str) or fetched.strip() != revision:
        session.error('Fetched Voiage source does not match the reviewed revision')
    session.run('git', '-C', str(source), 'apply', '--check', str(patch), external=True)
    session.run('git', '-C', str(source), 'apply', str(patch), external=True)
    session.run('git', '-C', str(source), 'add', 'pyproject.toml', external=True)
    session.run('git', '-C', str(source), '-c', 'user.name=Tobac compatibility build',
                '-c', 'user.email=voiage-compatibility@users.noreply.github.com',
                'commit', '-m', 'Qualify Voiage metadata for tobac Python 3.15.1', external=True,
                env={'GIT_AUTHOR_DATE': '2026-10-26T00:00:00+00:00',
                     'GIT_COMMITTER_DATE': '2026-10-26T00:00:00+00:00'})
    python = str(Path(session.bin).resolve() / 'python')
    session.env['CARGO_TARGET_DIR'] = str(run / 'cargo-target')
    session.run('uv', 'build', '--python', python, '--build-constraint',
                str(ROOT / 'engineering/voiage-build-requirements.txt'),
                '--wheel', '--out-dir', str(wheels), str(source), external=True)
    wheel, = wheels.glob('*.whl')
    session.run('uv', 'pip', 'install', '--python', python, '--no-index', str(wheel), external=True)
    session.run('uv', 'pip', 'check', '--python', python, external=True)
    session.run('python', '-m', 'pytest', '-q', 'tests/m3', 'tests/engineering/test_voiage_installed.py',
                'tests/test_workstream_integration.py', 'tests/engineering/test_evidence_interchange.py')
    session.run('python', 'scripts/qualify_interchange.py', '--out', str(run / 'interchange'))
    session.run('python', 'scripts/qualify_integrations.py', '--mode', 'voiage',
                '--out', str(run / 'equal-weight.json'))
    session.run('python', '-m', 'tobac.research.qualification', '--out', str(run / 'weighted.json'))
    derived = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    record = {'upstream_revision': revision, 'patch_sha256': hashlib.sha256(patch.read_bytes()).hexdigest(),
              'derived_revision': derived, 'wheel': wheel.name,
              'wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
              'scope': 'Metadata-only compatibility build; unchanged Voiage implementation and native code'}
    record['environment'] = session.run('uv', 'pip', 'freeze', '--python', python, silent=True, external=True)
    (run / 'build-receipt.json').write_text(json.dumps(record, indent=2) + '\n')
    OUT.mkdir(parents=True, exist_ok=True)
    # Keep compact receipts without uploading a complete upstream checkout or native target tree.
    import shutil
    receipt_dir = OUT / ('voiage-receipts-' + run.name)
    receipt_dir.mkdir()
    for name in ['build-receipt.json', 'equal-weight.json', 'weighted.json']:
        shutil.copyfile(run / name, receipt_dir / name)
    shutil.copytree(run / 'interchange', receipt_dir / 'interchange')
    session.log(f'Voiage receipt: {receipt_dir}')


@nox.session(python='3.15.1')
def moh_workbook(session):
    """Explicit local native-producer verification; no acquisition or source mutation."""
    environment(session)
    session.run('python', 'scripts/qualify_moh_workbook.py', *session.posargs)


@nox.session(python='3.15.1')
def product_reconciliation(session):
    """Recompute dated source-bound product tables; no source acquisition or conditioning."""
    environment(session)
    session.run('python', 'scripts/reconcile_products_2025.py', '--out',
                'outputs/engineering/product-reconciliation', *session.posargs)


@nox.session(python='3.15.1')
def clean_package(session):
    """Real artifact execution outside source and sibling checkouts."""
    environment(session, require_lock=True)
    destination = str(OUT / 'clean-package' / uuid4().hex)
    session.run('python', 'scripts/qualify_clean_package.py', '--out', destination)


@nox.session(python='3.15.1')
def ecosystem(session):
    """Optional native probe with a hash-bound, already qualified macOS Voiage wheel."""
    import hashlib
    import json
    session.run('python', '-c', 'import sys; assert sys.version_info[:3] == (3, 15, 1)')
    if len(session.posargs) != 1:
        session.error('Supply the qualified macOS Voiage compatibility wheel path')
    wheel = Path(session.posargs[0]).resolve()
    expected = json.loads((ROOT / 'integration/voiage_python315_compatibility_20261026.json').read_text())['build']['wheel_sha256']
    if not wheel.is_file() or hashlib.sha256(wheel.read_bytes()).hexdigest() != expected:
        session.error('Voiage wheel differs from the qualified artifact')
    session.run('python', 'scripts/lock_receipt.py', 'verify', '--profile', 'ecosystem',
                '--path', 'engineering/ecosystem.lock')
    python = str(Path(session.bin).resolve() / 'python')
    session.env.update(OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg', PYTHONHASHSEED='0')
    session.run('uv', 'pip', 'sync', '--python', python, '--require-hashes',
                'engineering/ecosystem.lock', external=True)
    session.install('--no-deps', '--no-build-isolation', '-e', '.')
    session.run('uv', 'pip', 'install', '--python', python, '--no-index', str(wheel), external=True)
    session.run('uv', 'pip', 'check', '--python', python, external=True)
    destination = str(OUT / 'ecosystem' / ('native-' + uuid4().hex + '.json'))
    session.run('python', 'scripts/qualify_ecosystem.py', '--out', destination)
    session.run('python', 'scripts/qualify_interchange.py', '--out',
                str(OUT / 'interchange' / uuid4().hex))
    session.run('python', '-m', 'pytest', 'tests/engineering/test_evidence_interchange.py',
                'tests/test_workstream_integration.py', 'tests/m3')


@nox.session(python='3.15.1')
def recovery(session):
    """Actual runner interruption/resume and immutable-receipt comparison."""
    environment(session)
    session.run('python', 'scripts/qualify_recovery.py', '--out',
                str(OUT / 'recovery' / uuid4().hex))
