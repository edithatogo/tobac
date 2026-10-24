"""Verify run source/output hashes and scientific scope; not external validation."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def verify(out,root=ROOT):
    out=Path(out).resolve();root=Path(root).resolve();errors=[]
    manifest=json.loads((out/'run_manifest.json').read_text())
    for group,base in [('sources',root),('files',out)]:
        for item in manifest[group]:
            target=(base/item['path']).resolve()
            if not target.is_relative_to(base) or not target.is_file():
                errors.append(f'Invalid path: {item["path"]}');continue
            if hashlib.sha256(target.read_bytes()).hexdigest()!=item['sha256']:
                errors.append(f'Hash mismatch: {item["path"]}')
    scope=json.loads((out/'fit_scope.json').read_text())
    if manifest.get('funding_recommendation') is not False:
        errors.append('Funding readiness overstated')
    if scope.get('latest_paired_year')!=2023 or scope.get('current_joint_nz_posterior') is not False:
        errors.append('Current empirical status overstated')
    if scope.get('source_positive_gap_is_illicit') is not False:
        errors.append('Signed discrepancy relabelled illicit')
    return {'status':'fail' if errors else 'pass','sources':len(manifest['sources']),
            'artifacts':len(manifest['files']),'errors':errors,
            'scope':'Run integrity and explicit interpretation only; not independent scientific validation'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('out',type=Path)
    result=verify(parser.parse_args().out);print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='pass' else 1)
