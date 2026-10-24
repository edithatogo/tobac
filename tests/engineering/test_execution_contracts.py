"""Nox command planning with a labelled test double, not an executed Nox environment."""
import importlib.util
from pathlib import Path
import sys
import types

import pytest

ROOT=Path(__file__).resolve().parents[2]


@pytest.fixture
def harness(monkeypatch,tmp_path):
    path=ROOT/'noxfile.py'
    assert path.is_file(), 'Nox follow-through file missing'
    nox=types.ModuleType('nox');nox.options=types.SimpleNamespace()
    nox.session=lambda f:f
    command=types.ModuleType('nox.command')
    class CommandFailed(Exception):pass
    command.CommandFailed=CommandFailed
    monkeypatch.setitem(sys.modules,'nox',nox)
    monkeypatch.setitem(sys.modules,'nox.command',command)
    spec=importlib.util.spec_from_file_location('harness_under_test',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    monkeypatch.chdir(tmp_path);monkeypatch.setattr(m,'ROOT',tmp_path)
    monkeypatch.setattr(m,'sys',types.SimpleNamespace(platform='linux'))
    class Session:
        def __init__(self):self.env={};self.posargs=[];self.calls=[];self.fail=set()
        def install(self,*args,**kwargs):self.calls.append(('install',args))
        def log(self,*args):pass
        def error(self,message):raise RuntimeError(message)
        def run(self,*args,**kwargs):
            self.calls.append(('run',args))
            if args[0] in self.fail:raise CommandFailed('fixture command failure')
            if args[:2]==('python','-c') and 'print(sys.executable)' in args[2]:return '/fixture/python\n'
            return ''
    return m,Session,tmp_path


def test_release_mode_refuses_missing_lock(harness,monkeypatch):
    m,S,_=harness;monkeypatch.setenv('TOBAC_REQUIRE_LOCK','1')
    with pytest.raises(RuntimeError,match='lock'):m.environment(S())


def test_partial_receipt_is_not_bootstrap_permission(harness):
    m,S,root=harness;p=root/'engineering';p.mkdir();(p/'requirements.lock.json').write_text('{}')
    with pytest.raises(RuntimeError,match='lock'):m.environment(S())


def test_locked_environment_verifies_before_sync_and_no_extra_tool_installs(harness):
    m,S,root=harness;p=root/'engineering';p.mkdir()
    (p/'audit.lock').write_text('fixture');(p/'audit.lock.json').write_text('{}')
    s=S();m.environment(s,profile='audit')
    run=[args for kind,args in s.calls if kind=='run']
    verify=next(i for i,args in enumerate(run) if 'scripts/lock_receipt.py' in args)
    sync=next(i for i,args in enumerate(run) if args[:3]==('uv','pip','sync'))
    assert verify<sync and '--require-hashes' in run[sync]
    installs=[args for kind,args in s.calls if kind=='install']
    assert len(installs)==1 and '--no-deps' in installs[0] and '--no-build-isolation' in installs[0]


def test_runtime_bootstrap_excludes_linux_audit_dependencies(harness):
    m,S,_=harness;s=S();m.environment(s)
    installs=[args for kind,args in s.calls if kind=='install']
    assert 'engineering/tools-requirements.txt' not in str(installs)
    assert 'engineering/build-requirements.txt' in str(installs)


def test_package_cannot_bootstrap_release(harness):
    m,S,_=harness
    with pytest.raises(RuntimeError,match='lock'):m.package(S())


def test_strict_audits_both_execute_and_fail_overall(harness):
    m,S,_=harness;s=S();s.fail={'ruff'}
    with pytest.raises(RuntimeError):m.strict_all(s)
    assert any(kind=='run' and args[0]=='basedpyright' for kind,args in s.calls)


def test_security_scans_both_execute_and_fail_overall(harness):
    m,S,_=harness;s=S();s.fail={'zizmor'}
    with pytest.raises(RuntimeError):m.security(s)
    assert any(kind=='run' and args[0]=='pip-audit' for kind,args in s.calls)


def test_quality_is_not_allowed_to_reinstall_tool_versions(harness):
    m,S,root=harness;p=root/'engineering';p.mkdir()
    (p/'audit.lock').write_text('fixture');(p/'audit.lock.json').write_text('{}')
    s=S();m.quality(s)
    installs=[args for kind,args in s.calls if kind=='install']
    assert len(installs)==1 and installs[0][-2:]==('-e','.')


def test_lock_produces_candidate_not_automatic_commit(harness):
    m,S,_=harness;s=S();m.lock(s)
    run=[args for kind,args in s.calls if kind=='run']
    assert sum('scripts/lock_receipt.py' in args and 'generate' in args for args in run)==2
    assert not any(args[0]=='git' for args in run)


def test_canary_requires_hypothesis_before_collection(harness):
    m,S,_=harness;s=S();m.canary(s)
    assert any(kind=='run' and 'import hypothesis' in str(args) for kind,args in s.calls)


def test_workflows_preserve_security_and_failure_evidence():
    import re
    import yaml
    names=('engineering.yml','engineering-deep.yml','release-candidate.yml','dependency-lock.yml')
    paths=[ROOT/'.github/workflows'/name for name in names]
    assert all(path.is_file() for path in paths)
    for path in paths:
        workflow=yaml.load(path.read_text(),Loader=yaml.BaseLoader)
        assert workflow['permissions']=={'contents':'read'}
        assert 'pull_request_target' not in workflow['on']
        for job in workflow['jobs'].values():
            assert int(job['timeout-minutes'])<=60
            assert 'continue-on-error' not in job
            for step in job['steps']:
                assert 'continue-on-error' not in step
                if 'uses' in step:
                    assert re.fullmatch(r'[\w.-]+/[\w./-]+@[0-9a-f]{40}',step['uses'])
    release=yaml.load((ROOT/'.github/workflows/release-candidate.yml').read_text(),Loader=yaml.BaseLoader)
    job=release['jobs']['qualify']
    assert job['env']['TOBAC_REQUIRE_LOCK']=='1'
    text=' '.join(s.get('run','') for s in job['steps'])
    assert 'git ls-files --error-unmatch' in text and 'strict_all' in text
    assert 'lock_receipt.py verify --profile audit' in text
    uploads=[s for s in job['steps'] if 'upload-artifact@' in s.get('uses','')]
    assert uploads[0]['if']=='always()' and uploads[1]['if']=='success()'


def test_workflow_contract_preserves_other_workstream_files(tmp_path, monkeypatch):
    import shutil
    folder=tmp_path/'.github/workflows';folder.mkdir(parents=True)
    for path in (ROOT/'.github/workflows').glob('*.yml'):
        shutil.copyfile(path,folder/path.name)
    (folder/'separate-research.yml').write_text('name: Other workstream\n')
    monkeypatch.setattr(sys.modules[__name__],'ROOT',tmp_path)
    test_workflows_preserve_security_and_failure_evidence()


def test_linux_audit_profile_is_not_portable_runtime(harness):
    m,S,_=harness;m.sys.platform='win32'
    with pytest.raises(RuntimeError,match='Linux-only'):m.environment(S(),profile='audit')
