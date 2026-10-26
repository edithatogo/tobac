"""Independent acceptance cases for parameter identity and resumable execution."""
import copy
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

from tobac._core import DecisionProblem, exact_evpi
from tobac.regulation import build_states, load_config, make_problem

ROOT = Path(__file__).resolve().parents[2]


def test_parameter_round_trip_preserves_metadata_and_rejects_unknown_fields(tmp_path):
    from tobac.parameters import load_parameters, save_parameters
    original = load_config(ROOT / 'configs/regulatory.json')
    path = tmp_path / 'parameters.json'
    save_parameters(original, path)
    assert load_parameters(path) == original
    assert load_parameters(path)['axes'][0]['unit'] == original['axes'][0]['unit']
    with pytest.raises(FileExistsError): save_parameters(original, path)
    data = json.loads(path.read_text()); data['backend'] = 'jax'; path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='fields'): load_parameters(path)


def test_two_parameter_scenarios_are_order_independent_and_do_not_mutate():
    c = load_config(ROOT / 'configs/regulatory.json'); frozen = copy.deepcopy(c)
    def calculate(probability):
        states, weights = build_states(c, {'illicit': probability})
        return exact_evpi(make_problem(states, weights, c, 1.0))
    a, b = calculate(.2), calculate(.8)
    assert calculate(.8) == b and calculate(.2) == a
    assert c == frozen


def test_numerical_calculation_does_not_use_file_or_network(monkeypatch):
    p = DecisionProblem(np.array([[0., 4.], [3., 0.]]), ('a', 'b'), 'score', np.array([.75, .25]))
    def forbidden(*args, **kwargs): raise AssertionError('I/O in calculation')
    monkeypatch.setattr(Path, 'read_bytes', forbidden)
    assert exact_evpi(p) == .75


def test_parameter_schema_and_nonfinite_values_fail_closed(tmp_path):
    from tobac.parameters import load_parameters, save_parameters
    c = load_config(ROOT / 'configs/regulatory.json')
    c['reference_exposure'] = float('nan')
    with pytest.raises(ValueError): save_parameters(c, tmp_path / 'bad.json')
    path = tmp_path/'unknown.json'; path.write_text('{"schema":"unknown"}')
    with pytest.raises(ValueError): load_parameters(path)


def test_replay_receipt_rejects_changed_inputs_and_partial_output(tmp_path):
    from tobac.replay import identities, verify_receipt
    root = tmp_path/'root'; (root/'configs').mkdir(parents=True)
    (root/'configs/c.json').write_text('{"schema":"test"}')
    output = tmp_path/'run'; output.mkdir(); (output/'value.csv').write_text('a\n1\n')
    inputs = identities(root)
    receipt = {'schema':'tobac.replay.v1','status':'complete','identity':inputs,
               'artifacts':{'value.csv':__import__('hashlib').sha256((output/'value.csv').read_bytes()).hexdigest()}}
    assert verify_receipt(root, output, receipt) == []
    (root/'configs/c.json').write_text('{"schema":"changed"}')
    assert 'input/environment identity changed' in verify_receipt(root, output, receipt)
    receipt['status'] = 'running'
    assert 'incomplete execution' in verify_receipt(root, output, receipt)


def test_replay_verifier_rejects_missing_and_escaping_artifacts(tmp_path):
    from tobac.replay import identities, verify_receipt
    receipt = {'schema':'tobac.replay.v1','status':'complete','identity':identities(tmp_path), 'artifacts':{'../secret':'0'*64}}
    with pytest.raises(ValueError): verify_receipt(tmp_path, tmp_path, receipt)


def test_context_rejects_missing_required_contract(tmp_path):
    repo = tmp_path
    spec = importlib.util.spec_from_file_location('context_bundle', ROOT/'scripts/context_bundle.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    config = {'schema_version':1,'profile':'evidence','max_bytes':4096,'paths':['AGENTS.md'],'base_commit':None,
              'required_paths':['AGENTS.md','docs/scope.md']}
    with pytest.raises(ValueError, match='required'): module.build(repo, config)


def test_stage_boundary_interruption_resumes_without_overwriting_receipts(tmp_path, monkeypatch):
    import hashlib
    import subprocess
    from tobac import replay
    calls = []
    def execute(command, **kwargs):
        folder = Path(command[command.index('--out')+1])
        calls.append(folder.name)
        if calls == ['m1','m2']:
            raise KeyboardInterrupt('boundary interruption')
        folder.mkdir()
        (folder/'validation.json').write_text('{"synthetic_fixture":true}')
        return subprocess.CompletedProcess(command,0)
    monkeypatch.setattr(replay.subprocess,'run',execute)
    out = tmp_path/'out'
    with pytest.raises(KeyboardInterrupt): replay.execute(ROOT,out,['m1','m2'],quick=True)
    before = hashlib.sha256((out/'m1.receipt.json').read_bytes()).hexdigest()
    result = replay.execute(ROOT,out,['m1','m2'],quick=True,resume=True)
    assert result['completed'] == ['m1','m2']
    assert calls == ['m1','m2','m2']
    assert hashlib.sha256((out/'m1.receipt.json').read_bytes()).hexdigest() == before


def test_replay_rejects_changed_checkpoint_options(tmp_path):
    from tobac.replay import execute, identities
    out=tmp_path/'out';out.mkdir()
    (out/'checkpoint.json').write_text(json.dumps({'schema':'tobac.replay-checkpoint.v1', 'identity':identities(ROOT),'stages':['m1'],'quick':True,'completed':[]}))
    with pytest.raises(ValueError,match='Incompatible'):execute(ROOT,out,['m1'],quick=False,resume=True)


def test_unknown_nested_parameter_cannot_be_ignored(tmp_path):
    from tobac.parameters import save_parameters
    c=load_config(ROOT/'configs/regulatory.json')
    c['constants']['unrecognised_model_switch']=1
    with pytest.raises(ValueError,match='fields'):save_parameters(c,tmp_path/'bad.json')


def test_additional_declared_scenario_uses_existing_model_without_changing_baseline(tmp_path):
    from tobac.parameters import save_parameters,load_parameters
    c=load_config(ROOT/'configs/regulatory.json'); baseline=copy.deepcopy(c)
    c['prior_scenarios']['bounded_extension']={'illicit':.35,'diversion':.65}
    save_parameters(c,tmp_path/'extension.json'); restored=load_parameters(tmp_path/'extension.json')
    states,weights=build_states(restored,restored['prior_scenarios']['bounded_extension'])
    assert np.isclose(weights.sum(),1)
    assert np.isfinite(exact_evpi(make_problem(states,weights,restored,1.)))
    del restored['prior_scenarios']['bounded_extension']
    assert restored == baseline


def test_bounded_model_action_extension_preserves_dominated_option_result():
    values=np.array([[0.,4.],[3.,0.]])
    base=DecisionProblem(values,('a','b'),'score',np.array([.75,.25]))
    extension=DecisionProblem(np.column_stack([values,[-100.,-100.]]),('a','b','dominated'),'score',np.array([.75,.25]))
    assert exact_evpi(extension)==exact_evpi(base)
    np.testing.assert_array_equal(base.values,values)
    with pytest.raises(ValueError):DecisionProblem(values,('a','a'),'score')
