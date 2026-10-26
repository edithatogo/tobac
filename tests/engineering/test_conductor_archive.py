"""Archived tracks remain verifiable without appearing in the active registry."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def test_archived_registry_is_part_of_name_validation(tmp_path):
    folder=tmp_path/'conductor';(folder/'archive').mkdir(parents=True)
    (folder/'tracks.md').write_text('# Active\n')
    (folder/'roadmap.md').write_text('# Deferred\n')
    (folder/'archive/index.md').write_text('## Completed example\nTrack: `conductor/archive/example/`\n')
    spec=importlib.util.spec_from_file_location('track_names',ROOT/'scripts/check_conductor_track_names.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    mapping,_=module.registry_headings(tmp_path)
    assert mapping['example']=='Completed example'
