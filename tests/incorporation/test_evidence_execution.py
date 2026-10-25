"""Real snapshot checks plus labelled tool doubles; no empirical or external qualification."""
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/qualify_integrations.py'


def load():
    spec = importlib.util.spec_from_file_location('integration_qualification', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(tmp_path):
    root = tmp_path/'repo'
    shutil.copytree(ROOT/'evidence', root/'evidence')
    (root/'integration').mkdir()
    shutil.copyfile(ROOT/'integration/prior_work_manifest.json',root/'integration/prior_work_manifest.json')
    return root


def test_inventory_cli_checks_actual_preserved_bytes_without_external_tools(tmp_path):
    out = tmp_path/'inventory.json'
    result = subprocess.run([sys.executable, str(SCRIPT), '--mode', 'inventory', '--root', str(ROOT),
                             '--out', str(out)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    receipt = json.loads(out.read_text())
    assert receipt['success'] is True
    assert receipt['preservation']['files'] == 19
    assert receipt['preservation']['csv_rows'] == 298
    assert receipt['collection_count'] >= 4
    assert receipt['record_occurrences'] >= 43
    assert receipt['external_tool_executed'] is False
    assert receipt['live_model_conditioned'] is False
    assert receipt['scientific_applicability_validated'] is False


def test_all_collections_are_inventory_occurrences_not_independent_observations():
    report = load().inventory(ROOT)
    assert report['record_occurrences'] > report['distinct_literal_ids']
    assert 'parallel-S08' in report['repeated_literal_ids']
    assert {c['role'] for c in report['collections']} == {
        'active_bibliography_not_observations', 'preserved_reference_only'}


@pytest.mark.parametrize('name', ['evidence/references.csl.json','evidence/m2/references.csl.json',
    'evidence/longitudinal/references.csl.json','evidence/prior_work/v2.9.0/references.csl.json'])
def test_missing_required_collection_fails(tmp_path, name):
    root = snapshot(tmp_path);(root/name).unlink()
    with pytest.raises(ValueError):load().inventory(root)


@pytest.mark.parametrize('name', ['evidence/references.csl.json','evidence/m2/references.csl.json',
    'evidence/longitudinal/references.csl.json','evidence/prior_work/v2.9.0/references.csl.json'])
def test_stored_dois_are_canonical(name):
    """Sourceright rejects non-canonical DOIs; check locally without the external binary."""
    text=(ROOT/name).read_text(encoding='utf-8')
    try:records=json.loads(text)
    except json.JSONDecodeError:records=[json.loads(l) for l in text.splitlines() if l.strip()]
    assert records
    assert not [r['DOI'] for r in records if r.get('DOI') and r['DOI']!=r['DOI'].lower()]


def test_changed_preserved_parameters_fail_before_any_tool(tmp_path, monkeypatch):
    root = snapshot(tmp_path)
    next((root/'evidence/prior_work').rglob('parameter_estimates*.csv')).write_text('changed')
    mod = load();calls=[]
    monkeypatch.setattr(mod.subprocess,'run',lambda *a, **k:calls.append(a))
    with pytest.raises(ValueError):mod.qualify_sourceright(root, all_csl=True)
    assert not calls


def test_additional_bibliography_is_discovered_not_ignored(tmp_path):
    root = snapshot(tmp_path);before=load().inventory(root);path=root/'evidence/future_fixture/references.csl.json'
    path.parent.mkdir();path.write_text('[{"id":"future-fixture","type":"article-journal"}]')
    report = load().inventory(root)
    assert report['collection_count']==before['collection_count']+1
    assert report['record_occurrences']==before['record_occurrences']+1
    assert 'evidence/future_fixture/references.csl.json' in [r['path'] for r in report['collections']]


@pytest.mark.parametrize('text',['{}','[]','[{"id":"x"},{"id":"x"}]',
    '[{"id":"x","id":"y"}]','[{"id":false}]','[{}]'])
def test_invalid_bibliography_identity_fails(tmp_path,text):
    root = snapshot(tmp_path);(root/'evidence/references.csl.json').write_text(text)
    with pytest.raises(ValueError):load().inventory(root)


def test_symlinked_collection_is_not_followed(tmp_path):
    root = snapshot(tmp_path);p=root/'evidence/linked.csl.json'
    try:p.symlink_to(root/'evidence/references.csl.json')
    except OSError:pytest.skip('Host cannot create symlink fixture')
    with pytest.raises(ValueError,match='symlink'):load().inventory(root)


def test_symlinked_collection_directory_is_not_silently_omitted(tmp_path):
    root=snapshot(tmp_path)
    try:(root/'evidence/linked').symlink_to(root/'evidence/m2',target_is_directory=True)
    except OSError:pytest.skip('Host cannot create symlink fixture')
    with pytest.raises(ValueError,match='symlink'):load().inventory(root)


def tool_double(mod, tmp_path, monkeypatch, codes=None, timeout_index=None):
    """A labelled execution double: never used to assert real Sourceright qualification."""
    exe=tmp_path/'not-a-real-sourceright';exe.write_text('fixture only')
    calls=[]
    monkeypatch.setattr(mod.shutil,'which',lambda name:str(exe))
    def run(command,**kwargs):
        calls.append(command)
        assert command[1:3]==['validate-csl','--json'] and kwargs['timeout']==120
        if len(calls)==timeout_index:raise subprocess.TimeoutExpired(command,120)
        code=0 if codes is None else codes[len(calls)-1]
        return subprocess.CompletedProcess(command,code,'fixture stdout','fixture stderr' if code else '')
    monkeypatch.setattr(mod.subprocess,'run',run)
    return calls


def test_external_all_csl_calls_real_command_contract_for_each_collection(tmp_path,monkeypatch):
    mod=load();calls=tool_double(mod,tmp_path,monkeypatch)
    result=mod.qualify_sourceright(ROOT,all_csl=True)
    assert len(calls)==len(mod.inventory(ROOT)['collections']) and result['success'] is True and result['external_tool_executed'] is True
    assert len(result['results'])==len(calls) and len(result['executable_sha256'])==64
    assert all(len(r['sha256'])==64 for r in result['results'])
    assert result['scientific_applicability_validated'] is False


def test_failed_collection_does_not_hide_later_checks(tmp_path,monkeypatch):
    mod=load();n=mod.inventory(ROOT)['collection_count']
    calls=tool_double(mod,tmp_path,monkeypatch,codes=[1]+[0]*(n-1))
    result=mod.qualify_sourceright(ROOT,all_csl=True)
    assert len(calls)==mod.inventory(ROOT)['collection_count'] and result['success'] is False
    assert result['results'][0]['exit_code']==1
    assert result['results'][-1]['success'] is True


def test_timeout_does_not_hide_other_collection_results(tmp_path,monkeypatch):
    mod=load();calls=tool_double(mod,tmp_path,monkeypatch,timeout_index=2)
    result=mod.qualify_sourceright(ROOT,all_csl=True)
    assert len(calls)==mod.inventory(ROOT)['collection_count'] and result['success'] is False
    assert result['results'][1]['error']=='timeout'


def test_default_external_mode_retains_single_collection_compatibility(tmp_path,monkeypatch):
    mod=load();calls=tool_double(mod,tmp_path,monkeypatch)
    result=mod.qualify_sourceright(ROOT,all_csl=False)
    assert len(calls)==1 and result['results'][0]['path']=='evidence/references.csl.json'
    assert result['scope_selection']=='single_legacy_collection'


def test_missing_library_is_failure_not_inventory_success(monkeypatch):
    mod=load();monkeypatch.setattr(mod.shutil,'which',lambda _:None)
    result=mod.qualify_sourceright(ROOT,all_csl=True)
    assert result['success'] is False and result['external_tool_executed'] is False
    assert result['inventory']['success'] is True


def test_changes_during_external_check_invalidate_receipt(tmp_path,monkeypatch):
    root=snapshot(tmp_path);mod=load()
    calls=tool_double(mod,tmp_path,monkeypatch)
    original=mod.subprocess.run
    def mutate(command,**kwargs):
        result=original(command,**kwargs)
        if len(calls)==1:
            with (root/'evidence/references.csl.json').open('a') as f:f.write('\n')
        return result
    monkeypatch.setattr(mod.subprocess,'run',mutate)
    result=mod.qualify_sourceright(root,all_csl=True)
    assert result['success'] is False and result['inputs_unchanged'] is False


def test_cli_refuses_receipt_overwrite_before_external_call(tmp_path):
    out=tmp_path/'receipt.json';out.write_text('previous')
    result=subprocess.run([sys.executable,str(SCRIPT),'--mode','inventory','--root',str(ROOT),
        '--out',str(out)],capture_output=True,text=True)
    assert result.returncode!=0 and out.read_text()=='previous'


def test_inventory_success_does_not_fill_in_current_quotes_or_raw_observations():
    report=load().inventory(ROOT)
    assert report['new_raw_assays']==0
    assert report['supplier_quotes_received']==0
    assert report['bibliographic_validation_performed'] is False


@pytest.mark.parametrize('name', ['tests', 'reproduce', 'package', 'evidence'])
def test_nox_paths_run_evidence_gate_first_and_stop_on_failure(monkeypatch, name):
    import types
    nox = types.ModuleType('nox');nox.options=types.SimpleNamespace();nox.session=lambda f:f
    command=types.ModuleType('nox.command')
    class CommandFailed(Exception):pass
    command.CommandFailed=CommandFailed
    monkeypatch.setitem(sys.modules,'nox',nox);monkeypatch.setitem(sys.modules,'nox.command',command)
    spec=importlib.util.spec_from_file_location('nox_integration',ROOT/'noxfile.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    def unexpected_environment(*a,**k):raise AssertionError('environment ran before evidence integrity')
    monkeypatch.setattr(mod,'environment',unexpected_environment)
    calls=[]
    class Session:
        def run(self,*args,**kwargs):
            calls.append(args)
            raise CommandFailed('fixture inventory failure')
    with pytest.raises(CommandFailed):getattr(mod,name)(Session())
    assert calls[0][:4]==('python','scripts/qualify_integrations.py','--mode','inventory')
    assert calls[0][-1]==f'outputs/engineering/evidence-{name}.json'


def test_scientific_workflows_gate_preservation_and_cover_every_citation_collection():
    import yaml
    root_workflow=yaml.load((ROOT/'.github/workflows/ci.yml').read_text(),Loader=yaml.BaseLoader)
    long_workflow=yaml.load((ROOT/'.github/workflows/longitudinal.yml').read_text(),Loader=yaml.BaseLoader)
    for workflow,name in [(root_workflow,'numerical'),(long_workflow,'longitudinal')]:
        commands=[s['run'] for s in workflow['jobs'][name]['steps'] if 'run' in s]
        assert 'qualify_integrations.py --mode inventory' in commands[0]
        assert any('pytest' in c for c in commands)
        assert not any('continue-on-error' in s for s in workflow['jobs'][name]['steps'])
    commands=[s.get('run','') for s in root_workflow['jobs']['sourceright']['steps']]
    assert sum('--mode sourceright --all-csl' in c for c in commands)==1
    assert not any('validate-csl --json evidence/m2/' in c for c in commands)


def test_bounded_evidence_context_uses_existing_schema():
    from jsonschema import Draft202012Validator
    schema=json.loads((ROOT/'engineering/context.schema.json').read_text())
    profile=json.loads((ROOT/'engineering/context/evidence.json').read_text())
    Draft202012Validator(schema).validate(profile)
    assert 'integration/prior_work_manifest.json' in profile['paths']
    assert 'docs/EVIDENCE_INTEGRATION.md' in profile['paths']
    assert profile['base_commit'] is None
    assert profile['max_bytes'] <= 80000


def voiage_double(mod, monkeypatch, bad=None):
    """Only checks the adapter contract; not an installed voiage qualification."""
    import types
    import numpy as np
    package=types.ModuleType('voiage');analysis=types.ModuleType('voiage.analysis')
    schema=types.ModuleType('voiage.schema');seen=[]
    class ValueArray:
        @staticmethod
        def from_numpy(values):return values
    class DecisionAnalysis:
        def __init__(self,values):self.values=values
        def evpi(self):
            seen.append(self.values.copy())
            if len(seen)==2 and bad is not None:return bad
            v=self.values
            return float(np.max(v,axis=1).mean()-np.max(v.mean(axis=0)))
    schema.ValueArray=ValueArray;analysis.DecisionAnalysis=DecisionAnalysis
    for name,item in [('voiage',package),('voiage.analysis',analysis),('voiage.schema',schema)]:
        monkeypatch.setitem(sys.modules,name,item)
    monkeypatch.setattr(mod.importlib.metadata,'version',lambda _:'fixture-not-installed')
    return seen


def test_existing_voiage_equal_weight_probe_retains_51_cases(monkeypatch):
    mod=load();seen=voiage_double(mod,monkeypatch)
    report=mod.qualify_voiage()
    assert len(seen)==51 and report['cases']==51
    assert report['max_absolute_error']==0 and report['success'] is True
    assert report['version']=='fixture-not-installed'


@pytest.mark.parametrize('bad',[float('nan'),float('inf'),-float('inf')])
def test_nonfinite_external_evpi_cannot_be_hidden_by_max_error(monkeypatch,bad):
    mod=load();voiage_double(mod,monkeypatch,bad)
    with pytest.raises(ValueError,match='Nonfinite'):mod.qualify_voiage()


def test_wrong_external_evpi_fails_parity(monkeypatch):
    mod=load();voiage_double(mod,monkeypatch,100.)
    report=mod.qualify_voiage()
    assert report['success'] is False


def test_external_executable_change_invalidates_validation(tmp_path,monkeypatch):
    mod=load();calls=tool_double(mod,tmp_path,monkeypatch)
    original=mod.subprocess.run
    def mutate(command,**kwargs):
        result=original(command,**kwargs)
        if len(calls)==1:Path(command[0]).write_text('changed executable fixture')
        return result
    monkeypatch.setattr(mod.subprocess,'run',mutate)
    result=mod.qualify_sourceright(ROOT,all_csl=True)
    assert result['success'] is False and result['executable_unchanged'] is False


def test_invalid_mode_combination_fails_before_receipt(tmp_path):
    out=tmp_path/'bad.json'
    result=subprocess.run([sys.executable,str(SCRIPT),'--mode','inventory','--all-csl',
                           '--out',str(out)],capture_output=True,text=True)
    assert result.returncode!=0 and not out.exists()
