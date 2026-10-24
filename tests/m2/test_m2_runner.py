from pathlib import Path
import json
import pytest
from tobac.m2 import run

ROOT=Path(__file__).parents[2]

def test_m2_quick_runner_and_nonoverwrite(tmp_path,monkeypatch):
    monkeypatch.chdir(ROOT)
    out=tmp_path/'run'
    r=run('configs/m2_retail.json',out,quick=True,quit_points=2)
    assert r['passed'] and r['designs']==15
    assert (out/'manifest.json').is_file()
    data=json.loads((out/'conditioning_fixtures.json').read_text())
    assert all('NOT an empirical' in row['qualification'] for row in data)
    with pytest.raises(FileExistsError):run('configs/m2_retail.json',out,quick=True,quit_points=2)


def test_source_shape_cannot_drift_from_record(tmp_path):
    import json
    from pathlib import Path
    cfg=json.loads(Path('configs/m2_retail.json').read_text())
    cfg['source_beta'][0]=1.0
    changed=Path.cwd()/'configs'/'_invalid_m2_test.json'
    try:
        changed.write_text(json.dumps(cfg))
        import pytest
        from tobac.m2 import run
        with pytest.raises(ValueError,match='Source-prior'):
            run(changed,tmp_path/'bad',quick=True)
    finally:
        changed.unlink(missing_ok=True)


def test_m2_uses_configured_scientific_threshold_and_confidence(tmp_path, monkeypatch):
    import tobac.m2 as module
    original_load = module.load_config
    original_evaluate = module.evaluate
    def changed_config(path):
        c=original_load(path)
        c['scientific_event']={'minimum_absolute_growth_fraction':.17,'confidence':.8}
        return c
    def checked_evaluate(*args, **kwargs):
        if kwargs.get('event') is not None:
            assert kwargs.get('confidence')==.8
        return original_evaluate(*args, **kwargs)
    monkeypatch.setattr(module,'load_config',changed_config)
    monkeypatch.setattr(module,'evaluate',checked_evaluate)
    value=module.run('configs/m2_retail.json',tmp_path/'custom',quick=True,quit_points=1)
    assert value['scientific_event']['minimum_absolute_growth_fraction']==.17
