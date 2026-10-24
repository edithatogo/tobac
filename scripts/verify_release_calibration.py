"""Check release-calibration input/output hashes and scope, not scientific validity."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def verify(out,root=ROOT):
    out=Path(out).resolve();root=Path(root).resolve()
    data=json.loads((out/'run_manifest.json').read_text())
    errors=[]
    if data.get('funding_recommendation') is not False:
        errors.append('Funding status overstated')
    for group,base in [('sources',root),('files',out)]:
        for item in data[group]:
            p=(base/item['path']).resolve()
            if not p.is_relative_to(base) or not p.is_file():
                errors.append('Invalid file '+item['path']);continue
            if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
                errors.append('Hash mismatch '+item['path'])
    scope=json.loads((out/'fit_scope.json').read_text())
    if scope.get('estimand')!='reported_lawful_smoked_tobacco_releases':
        errors.append('Estimand changed')
    return {'status':'pass' if not errors else 'fail','sources':len(data['sources']),
            'artifacts':len(data['files']),'errors':errors,
            'scope':'integrity only; empirical funding remains unestablished'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('out',type=Path)
    result=verify(parser.parse_args().out);print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='pass' else 1)
