"""The mutation session must fail, not pass, when mutants survive.

mutmut exits 0 whatever the score, so the Nox session only becomes a gate
through scripts/check_mutation_score.py. These tests pin that threshold behaviour
against mutmut's own ``mutants/<path>.meta`` record format.
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[2]


def load():
    path=ROOT/'scripts/check_mutation_score.py'
    assert path.is_file(), 'mutation score gate absent'
    spec=importlib.util.spec_from_file_location('check_mutation_score',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def write_meta(root: Path, exit_codes: dict[str, int | None]) -> Path:
    """Write one ``mutants/<source>.meta`` file using mutmut's own record layout."""
    meta_path=root/'mutants'/'src'/'tobac'/'supply.py.meta'
    meta_path.parent.mkdir(parents=True,exist_ok=True)
    meta_path.write_text(json.dumps({
        'exit_code_by_key':exit_codes,
        'hash_by_function_name':{},
        'type_check_error_by_key':{},
        'durations_by_key':{},
        'estimated_durations_by_key':{},
    }),encoding='utf-8')
    return meta_path


def test_survivors_below_the_floor_fail_the_gate(tmp_path,capsys):
    write_meta(tmp_path,{'f__mutmut_1':1,'f__mutmut_2':0,'f__mutmut_3':0,'f__mutmut_4':1})
    assert load().main(['--minimum','60','--mutants-dir',str(tmp_path/'mutants')])==1
    assert 'below the minimum' in capsys.readouterr().err


def test_score_at_the_floor_passes(tmp_path):
    write_meta(tmp_path,{'f__mutmut_1':1,'f__mutmut_2':1,'f__mutmut_3':1,'f__mutmut_4':0})
    assert load().main(['--minimum','75','--mutants-dir',str(tmp_path/'mutants')])==0


def test_pytest_internal_error_counts_as_a_kill(tmp_path):
    # mutmut maps exit code 3 ('internal error in pytest') to killed; treating it as a
    # survivor would understate the score and make the gate report a false regression.
    write_meta(tmp_path,{'f__mutmut_1':3})
    module=load()
    assert module.read_statuses(tmp_path/'mutants')['killed']==1
    assert module.main(['--minimum','100','--mutants-dir',str(tmp_path/'mutants')])==0


def test_missing_results_fail_rather_than_pass(tmp_path):
    (tmp_path/'mutants').mkdir()
    assert load().main(['--minimum','1','--mutants-dir',str(tmp_path/'mutants')])==1


def test_unassessable_mutants_leave_the_denominator(tmp_path):
    # Interrupted and never-checked mutants say nothing about test strength, so they must
    # not be scored as survivors.
    write_meta(tmp_path,{'f__mutmut_1':1,'f__mutmut_2':2,'f__mutmut_3':None})
    module=load()
    counts=module.read_statuses(tmp_path/'mutants')
    assert counts['killed']==1 and counts['not checked']==1
    assert module.main(['--minimum','100','--mutants-dir',str(tmp_path/'mutants')])==0


def test_unreadable_record_fails_closed(tmp_path):
    meta=write_meta(tmp_path,{'f__mutmut_1':1})
    meta.write_text('{not json',encoding='utf-8')
    with pytest.raises(SystemExit):
        load().main(['--minimum','60','--mutants-dir',str(tmp_path/'mutants')])


def test_timeout_codes_are_not_counted_as_kills(tmp_path):
    # This table previously declared -24 as killed. mutmut classes -24 as a timeout, so a
    # timed-out mutant was counted as killed; at 63 such mutants that alone moved the
    # reported score from 61.7% to well above 100%, and the gate passed on a miscount.
    write_meta(tmp_path,{'f__mutmut_1':-24,'f__mutmut_2':36,'f__mutmut_3':152})
    module=load()
    counts=module.read_statuses(tmp_path/'mutants')
    assert counts['timeout']==3 and 'killed' not in counts
    assert module.main(['--minimum','1','--mutants-dir',str(tmp_path/'mutants')])==1


@pytest.fixture
def mutmut_status_by_exit_code():
    """mutmut's own table, or a deliberate skip.

    The ``tests`` session does not install tools-requirements.txt, so these two comparisons
    cannot run there. They are paired on one deliberately environment-sensitive skip rather
    than a bare importorskip, which would report them as passing once the import succeeds but
    silently skip them in the session that runs the suite. Run them under the ``quality``
    environment (the mutation session's environment) to execute them.
    """
    stats=pytest.importorskip('mutmut.stats')
    return stats.status_by_exit_code


def test_mapping_matches_mutmut_own_table(mutmut_status_by_exit_code):
    """The recorded statuses must be mutmut's, not a hand-maintained guess."""
    for code,status in load().STATUS_BY_EXIT_CODE.items():
        assert mutmut_status_by_exit_code[code]==status, (
            f'exit code {code!r} is recorded as {status!r} here but is '
            f'{mutmut_status_by_exit_code[code]!r} in mutmut')


def test_every_killed_status_is_one_mutmut_calls_killed(mutmut_status_by_exit_code):
    """A non-kill must never enter the numerator, whatever mutmut adds later."""
    module=load()
    killed={code for code,status in mutmut_status_by_exit_code.items() if status=='killed'}
    assert module.KILLED_STATUSES=={'killed'}
    for code in module.STATUS_BY_EXIT_CODE:
        if code in killed:
            assert module.STATUS_BY_EXIT_CODE[code]=='killed'
