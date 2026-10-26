"""Gate tests use labelled fixture locks; they are not a resolver qualification."""
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load():
    path = ROOT / 'scripts/lock_receipt.py'
    assert path.is_file(), 'lock receipt implementation missing'
    spec = importlib.util.spec_from_file_location('lock_receipt', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inputs(root):
    files = ['pyproject.toml', 'requirements.lock', 'engineering/requirements.in',
             'engineering/test-requirements.txt', 'engineering/build-requirements.txt',
             'engineering/audit.in', 'engineering/tools-requirements.txt']
    for name in files:
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('# fixture dependency input\n')


def fixture(root, profile='runtime'):
    m = load(); inputs(root)
    name = 'requirements.lock' if profile == 'runtime' else 'audit.lock'
    lock = root / 'engineering' / name
    lock.write_text('# fixture only, not a usable distribution\nexample==1 --hash=sha256:' + 'a'*64 + '\n')
    receipt = {'schema': 'tobac.lock-receipt.v1', 'profile': profile,
               'resolver': 'uv fixture', 'command': ['uv', 'pip', 'compile'],
               'resolver_exit_code': 0, 'lock_sha256': m.digest(lock),
               'inputs': m.input_hashes(root, profile),
               'qualification': 'resolver receipt is not approval or signed provenance'}
    lock.with_suffix('.lock.json').write_text(json.dumps(receipt))
    return m, lock


@pytest.mark.parametrize('profile', ['runtime', 'audit'])
def test_valid_receipt_binds_exact_inputs_and_lock(tmp_path, profile):
    m, lock = fixture(tmp_path, profile)
    assert m.verify(tmp_path, lock, profile)['status'] == 'pass'


@pytest.mark.parametrize('target', ['pyproject.toml', 'requirements.lock',
    'engineering/requirements.in', 'engineering/test-requirements.txt',
    'engineering/build-requirements.txt'])
def test_input_change_invalidates_lock(tmp_path, target):
    m, lock = fixture(tmp_path)
    (tmp_path / target).write_text('changed')
    with pytest.raises(ValueError, match='input'): m.verify(tmp_path, lock, 'runtime')


def test_missing_and_changed_receipts_fail_closed(tmp_path):
    m, lock = fixture(tmp_path)
    receipt = lock.with_suffix('.lock.json')
    receipt.unlink()
    with pytest.raises(ValueError): m.verify(tmp_path, lock, 'runtime')
    m, lock = fixture(tmp_path)
    lock.write_text('modified')
    with pytest.raises(ValueError, match='hash'): m.verify(tmp_path, lock, 'runtime')


@pytest.mark.parametrize('change', [
    {'profile': 'audit'}, {'resolver_exit_code': 1}, {'schema': 'wrong'},
    {'inputs': {}}, {'lock_sha256': '0'*64}, {'command': []}])
def test_malformed_or_failed_receipt_rejected(tmp_path, change):
    m, lock = fixture(tmp_path)
    path = lock.with_suffix('.lock.json')
    receipt = json.loads(path.read_text()); receipt.update(change)
    path.write_text(json.dumps(receipt))
    with pytest.raises(ValueError): m.verify(tmp_path, lock, 'runtime')


def test_unexpected_profile_and_path_escape_rejected(tmp_path):
    m, lock = fixture(tmp_path)
    with pytest.raises(ValueError): m.input_hashes(tmp_path, 'anything')
    with pytest.raises(ValueError): m.verify(tmp_path, tmp_path.parent/'outside.lock', 'runtime')


def test_symlinked_input_rejected(tmp_path):
    m, lock = fixture(tmp_path)
    source = tmp_path/'requirements.lock'; source.unlink()
    try:source.symlink_to(tmp_path/'pyproject.toml')
    except OSError:pytest.skip('Host cannot create test symlinks')
    with pytest.raises(ValueError, match='symlink'): m.verify(tmp_path, lock, 'runtime')


def test_audit_inputs_not_silently_ignored(tmp_path):
    m, lock = fixture(tmp_path, 'audit')
    (tmp_path/'engineering/tools-requirements.txt').write_text('changed')
    with pytest.raises(ValueError, match='input'): m.verify(tmp_path, lock, 'audit')


def test_failed_resolver_does_not_create_success_receipt(tmp_path, monkeypatch):
    m = load(); inputs(tmp_path)
    monkeypatch.setattr(m.shutil, 'which', lambda _: '/bin/uv')
    def fail(command, **kwargs):
        if '--version' in command: return subprocess.CompletedProcess(command, 0, 'uv fixture\n')
        output = Path(command[command.index('--output-file')+1]); output.write_text('partial')
        raise subprocess.CalledProcessError(1, command)
    monkeypatch.setattr(m.subprocess, 'run', fail)
    with pytest.raises(subprocess.CalledProcessError):
        m.generate(tmp_path, tmp_path/'outputs/candidate', 'runtime')
    assert not list((tmp_path/'outputs/candidate').glob('*.json'))
    assert not list((tmp_path/'outputs/candidate').glob('*.lock'))


def test_generation_requires_real_uv_and_refuses_overwrite(tmp_path, monkeypatch):
    m = load(); inputs(tmp_path)
    monkeypatch.setattr(m.shutil, 'which', lambda _: None)
    with pytest.raises(ValueError, match='uv'): m.generate(tmp_path,tmp_path/'outputs/candidate','runtime')
    m, lock = fixture(tmp_path)
    monkeypatch.setattr(m.shutil, 'which', lambda _: '/bin/uv')
    with pytest.raises(ValueError, match='overwrite'): m.generate(tmp_path, lock.parent, 'runtime')


def test_command_contract_uses_real_resolver_and_records_scope(tmp_path, monkeypatch):
    m = load(); inputs(tmp_path); calls=[]
    monkeypatch.setattr(m.shutil, 'which', lambda _: '/bin/uv')
    def simulated(command, **kwargs):
        calls.append(command)
        if '--version' in command: return subprocess.CompletedProcess(command, 0, 'uv fixture\n')
        Path(command[command.index('--output-file')+1]).write_text('example==1 --hash=sha256:'+'a'*64+'\n')
        return subprocess.CompletedProcess(command, 0)
    monkeypatch.setattr(m.subprocess, 'run', simulated)
    lock = m.generate(tmp_path, tmp_path/'outputs/candidate', 'runtime')
    assert '--generate-hashes' in calls[-1] and '--universal' in calls[-1]
    assert m.verify(tmp_path, lock, 'runtime')['status']=='pass'
    assert not (tmp_path/'engineering/requirements.lock.json').exists()


def test_recorded_command_is_repo_relative(tmp_path, monkeypatch):
    """A receipt must not embed the absolute path of the machine that resolved it."""
    m = load(); inputs(tmp_path); monkeypatch.setattr(m.shutil, 'which', lambda _: '/bin/uv')
    def simulated(command, **kwargs):
        if '--version' in command: return subprocess.CompletedProcess(command, 0, 'uv fixture\n')
        Path(command[command.index('--output-file')+1]).write_text('example==1 --hash=sha256:'+'a'*64+'\n')
        return subprocess.CompletedProcess(command, 0)
    monkeypatch.setattr(m.subprocess, 'run', simulated)
    lock = m.generate(tmp_path, tmp_path/'outputs/candidate', 'runtime')
    recorded = json.loads(lock.with_suffix('.lock.json').read_text())['command']
    assert 'engineering/requirements.in' in recorded
    assert not [item for item in recorded if str(tmp_path) in item]


def test_duplicate_json_keys_rejected(tmp_path):
    m, lock=fixture(tmp_path)
    receipt=lock.with_suffix('.lock.json')
    receipt.write_text('{"schema":"wrong","schema":"tobac.lock-receipt.v1"}')
    with pytest.raises(ValueError, match='Duplicate'): m.verify(tmp_path,lock,'runtime')


def test_untracked_requirement_include_fails_closed(tmp_path):
    m, lock=fixture(tmp_path)
    (tmp_path/'engineering/requirements.in').write_text('-r extra.txt\n')
    (tmp_path/'engineering/extra.txt').write_text('something==1\n')
    with pytest.raises(ValueError,match='include'):m.input_hashes(tmp_path,'runtime')


def test_bool_exit_code_is_not_success_metadata(tmp_path):
    m,lock=fixture(tmp_path)
    path=lock.with_suffix('.lock.json');data=json.loads(path.read_text())
    data['resolver_exit_code']=False;path.write_text(json.dumps(data))
    with pytest.raises(ValueError):m.verify(tmp_path,lock,'runtime')


@pytest.mark.parametrize('include',['--requirement=test-requirements.txt','-rtest-requirements.txt',
    '--constraint test-requirements.txt','-c test-requirements.txt'])
def test_supported_local_include_spellings(tmp_path,include):
    m=load();inputs(tmp_path)
    (tmp_path/'engineering/requirements.in').write_text(include+'\n')
    assert len(m.input_hashes(tmp_path,'runtime'))==5


def test_malformed_includes_and_missing_inputs_fail(tmp_path):
    m=load();inputs(tmp_path)
    (tmp_path/'engineering/requirements.in').write_text('-r\n')
    with pytest.raises(ValueError,match='include'):m.input_hashes(tmp_path,'runtime')
    (tmp_path/'engineering/requirements.in').unlink()
    with pytest.raises(ValueError,match='missing'):m.input_hashes(tmp_path,'runtime')


def test_output_symlink_and_escape_rejected(tmp_path,monkeypatch):
    m=load();inputs(tmp_path)
    monkeypatch.setattr(m.shutil,'which',lambda _:'/fixture/uv')
    with pytest.raises(ValueError):m.generate(tmp_path,tmp_path.parent/'escape','runtime')
    try:(tmp_path/'output').symlink_to(tmp_path/'engineering',target_is_directory=True)
    except OSError:pytest.skip('Host cannot create test symlinks')
    with pytest.raises(ValueError,match='symlink'):m.generate(tmp_path,tmp_path/'output','runtime')


def test_source_change_during_resolve_removes_candidate(tmp_path,monkeypatch):
    m=load();inputs(tmp_path)
    monkeypatch.setattr(m.shutil,'which',lambda _:'/fixture/uv')
    def simulated(command,**kwargs):
        if '--version' in command:return subprocess.CompletedProcess(command,0,'uv fixture\n')
        Path(command[command.index('--output-file')+1]).write_text('x==1 --hash=sha256:'+'a'*64)
        (tmp_path/'pyproject.toml').write_text('changed during solve')
        return subprocess.CompletedProcess(command,0)
    monkeypatch.setattr(m.subprocess,'run',simulated)
    with pytest.raises(ValueError,match='changed during'):m.generate(tmp_path,tmp_path/'candidate','audit')
    assert not list((tmp_path/'candidate').iterdir())


def test_unhashed_resolver_output_cannot_get_receipt(tmp_path,monkeypatch):
    m=load();inputs(tmp_path)
    monkeypatch.setattr(m.shutil,'which',lambda _:'/fixture/uv')
    def simulated(command,**kwargs):
        if '--version' in command:return subprocess.CompletedProcess(command,0,'uv fixture\n')
        Path(command[command.index('--output-file')+1]).write_text('x==1')
        return subprocess.CompletedProcess(command,0)
    monkeypatch.setattr(m.subprocess,'run',simulated)
    with pytest.raises(ValueError,match='hashed'):m.generate(tmp_path,tmp_path/'candidate','runtime')
    assert not list((tmp_path/'candidate').iterdir())


@pytest.mark.parametrize('profile', ['runtime', 'audit'])
def test_verify_rejects_an_unhashed_candidate_with_a_matching_receipt(tmp_path, profile):
    # The generate path refuses unhashed resolver output (above); the verify path
    # must enforce the same trust boundary. A lock whose lines carry no
    # --hash=sha256: fragment must fail even when a receipt is present and
    # byte-consistent, so a manually-edited candidate cannot be promoted as
    # locked by a self-consistent receipt.
    m, lock = fixture(tmp_path, profile)
    lock.write_text(lock.read_text().replace(' --hash=sha256:', ''))
    receipt_path = lock.with_suffix('.lock.json')
    receipt = json.loads(receipt_path.read_text())
    receipt['lock_sha256'] = m.digest(lock)
    receipt_path.write_text(json.dumps(receipt))
    with pytest.raises(ValueError, match='unhashed'):
        m.verify(tmp_path, lock, profile)


def test_cli_verify_uses_real_byte_checks(tmp_path,monkeypatch,capsys):
    import sys
    m,path=fixture(tmp_path)
    monkeypatch.setattr(sys,'argv',['lock_receipt','verify','--profile','runtime','--root',str(tmp_path),'--path',str(path)])
    m.main()
    assert json.loads(capsys.readouterr().out)['status']=='pass'
