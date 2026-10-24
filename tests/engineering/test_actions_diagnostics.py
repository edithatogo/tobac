"""Read-only hosted diagnostic contracts; fixtures are not actual remote executions."""
import importlib.util
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[2]

def load():
    path=ROOT/'scripts/actions_diagnostics.py'
    assert path.is_file(), 'Actions diagnostic implementation missing'
    spec=importlib.util.spec_from_file_location('actions_diagnostics',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


def test_pre_runner_failure_not_mislabelled_numerical_failure():
    m=load()
    result=m.summarise({'id':1,'head_sha':'a'*40},[
        {'id':2,'name':'tests','conclusion':'failure','runner_id':0,'steps':[]}],{})
    assert result['jobs'][0]['execution']=='not_started'
    assert result['root_cause']=='not_established'
    assert result['qualification_pass'] is False


def test_executed_failed_step_is_distinguished():
    m=load()
    result=m.summarise({'id':1,'head_sha':'a'*40},[
        {'id':2,'conclusion':'failure','runner_id':5,'steps':[{'name':'pytest','conclusion':'failure'}]}],{})
    assert result['jobs'][0]['execution']=='steps_reported'
    assert result['jobs'][0]['failed_steps']==['pytest']


def test_success_requires_all_jobs_and_actual_steps():
    m=load();run={'id':1,'head_sha':'a'*40,'status':'completed','conclusion':'success'}
    assert not m.summarise(run,[],{})['qualification_pass']
    assert not m.summarise(run,[{'id':2,'conclusion':'success','steps':[]}],{})['qualification_pass']
    jobs=[{'id':2,'conclusion':'success','runner_id':5,'steps':[{'name':'test','conclusion':'success'}]}]
    assert m.summarise(run,jobs,{})['qualification_pass'] is True


def test_annotations_preserved_as_messages_not_guessed_fixes():
    m=load()
    data=m.summarise({'id':1,'head_sha':'a'*40},[{'id':2,'conclusion':'failure','runner_id':0,'steps':[]}],
        {'2':[{'message':'example upstream scheduling annotation','annotation_level':'failure'}]})
    assert data['jobs'][0]['annotations'][0]['message'].startswith('example')
    assert data['root_cause']=='inspect_recorded_annotations'
    assert 'billing' not in str(data)


@pytest.mark.parametrize('repository',['../x','a/b/c','-X POST','https://github.com/a/b','a b/c'])
def test_non_repository_input_rejected(repository):
    with pytest.raises(ValueError):load().validate_repository(repository)


def test_paginated_payload_is_flattened_not_truncated():
    m=load()
    assert m.flatten_jobs([{'total_count':2,'jobs':[{'id':1}]},{'total_count':2,'jobs':[{'id':2}]}])==[{'id':1},{'id':2}]
    with pytest.raises(ValueError):m.flatten_jobs([{'total_count':2,'jobs':[{'id':1}]}])


def test_missing_gh_does_not_become_pass(monkeypatch):
    m=load();monkeypatch.setattr(m.shutil,'which',lambda _:None)
    with pytest.raises(ValueError,match='gh'):m.get_json('repos/a/b/actions/runs/1')


def test_incomplete_parent_run_cannot_qualify_from_current_job_list():
    m=load()
    jobs=[{'id':2,'conclusion':'success','runner_id':5,'steps':[{'name':'test','conclusion':'success'}]}]
    assert not m.summarise({'id':1,'head_sha':'a'*40,'status':'in_progress'},jobs,{})['qualification_pass']


def test_collect_uses_returned_check_id_and_records_missing_annotation(monkeypatch):
    m=load();calls=[]
    def api(endpoint,*,paginate=False):
        calls.append((endpoint,paginate))
        if endpoint.endswith('/runs/7'):return {'id':7,'head_sha':'a'*40,'status':'completed','conclusion':'failure'}
        if '/jobs?' in endpoint:return [{'total_count':1,'jobs':[{'id':8,'conclusion':'failure','runner_id':0,'steps':[],
            'check_run_url':'https://api.github.com/repos/a/b/check-runs/9'}]}]
        raise ValueError('annotation unavailable fixture')
    monkeypatch.setattr(m,'get_json',api)
    result=m.collect('a/b',7)
    assert result['annotation_errors']==[{'job_id':8,'error':'annotations_unavailable'}]
    assert any('/check-runs/9/' in endpoint for endpoint,_ in calls)
    assert result['qualification_pass'] is False


def test_collect_does_not_follow_foreign_check_url(monkeypatch):
    m=load()
    def api(endpoint,*,paginate=False):
        if endpoint.endswith('/runs/7'):return {'id':7,'head_sha':'a'*40}
        return [{'total_count':1,'jobs':[{'id':8,'conclusion':'failure','runner_id':0,'steps':[],
            'check_run_url':'https://untrusted.example/check-runs/9'}]}]
    monkeypatch.setattr(m,'get_json',api)
    assert m.collect('a/b',7)['annotation_errors'][0]['error']=='check_run_url_missing_or_mismatched'


def test_official_cli_is_get_only_and_paginates(monkeypatch):
    import subprocess
    m=load();seen=[]
    monkeypatch.setattr(m.shutil,'which',lambda _: '/fixture/gh')
    def run(command,**kwargs):
        seen.append(command);assert kwargs['check'] is True
        return subprocess.CompletedProcess(command,0,'[{"jobs": [], "total_count": 0}]')
    monkeypatch.setattr(m.subprocess,'run',run)
    assert m.get_json('repos/a/b/actions/runs/1/jobs',paginate=True)[0]['total_count']==0
    assert '--method' in seen[0] and 'GET' in seen[0] and '--hostname' in seen[0]
    assert '--paginate' in seen[0] and '--slurp' in seen[0]


@pytest.mark.parametrize('run_id',[0,-1,True,1.5])
def test_invalid_run_id_does_not_call_api(run_id):
    with pytest.raises(ValueError):load().collect('a/b',run_id)


def test_annotations_returned_from_all_pages(monkeypatch):
    m=load()
    def api(endpoint,*,paginate=False):
        if endpoint.endswith('/runs/7'):return {'id':7,'head_sha':'a'*40,'status':'completed','conclusion':'failure'}
        if '/jobs?' in endpoint:return [{'total_count':1,'jobs':[{'id':8,'conclusion':'failure','runner_id':0,'steps':[],
            'check_run_url':'https://api.github.com/repos/a/b/check-runs/9'}]}]
        return [[{'message':'first','annotation_level':'failure'}],[{'message':'second','annotation_level':'warning'}]]
    monkeypatch.setattr(m,'get_json',api)
    result=m.collect('a/b',7)
    assert len(result['jobs'][0]['annotations'])==2 and not result['annotation_errors']


def test_cli_failure_writes_diagnostic_but_not_success(tmp_path,monkeypatch):
    import sys,json
    m=load();path=tmp_path/'diagnostic.json'
    monkeypatch.setattr(sys,'argv',['diagnose','--run','7','--out',str(path)])
    monkeypatch.setattr(m,'collect',lambda *a:{'qualification_pass':False,'root_cause':'not_established'})
    with pytest.raises(SystemExit) as error:m.main()
    assert error.value.code==1 and json.loads(path.read_text())['qualification_pass'] is False
    with pytest.raises(ValueError,match='overwrite'):m.main()


def test_cli_success_keeps_precise_scope(tmp_path,monkeypatch):
    import sys
    m=load();path=tmp_path/'success.json'
    monkeypatch.setattr(sys,'argv',['diagnose','--run','7','--out',str(path)])
    monkeypatch.setattr(m,'collect',lambda *a:{'qualification_pass':True,'scope':'fixture only'})
    with pytest.raises(SystemExit) as error:m.main()
    assert error.value.code==0


def test_malformed_job_pages_fail():
    for pages in [[],[{}],[{'total_count':2,'jobs':[{'id':1},{'id':1}]}]]:
        with pytest.raises(ValueError):load().flatten_jobs(pages)
