"""Verify extracted-core provenance and saved numerical-input/output hashes."""
from pathlib import Path
import ast, hashlib, json, sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'integration/baseline.json').read_text())
text=(root/manifest['published_core']).read_text();lines=text.splitlines(keepends=True)
nodes={n.name:n for n in ast.parse(text).body if hasattr(n,'name')}
for item in manifest['extracted_definitions']:
    n=nodes[item['name']];start=min([n.lineno]+[d.lineno for d in getattr(n,'decorator_list',[])])-1
    actual=hashlib.sha256(''.join(lines[start:n.end_lineno]).encode()).hexdigest()
    if actual!=item['sha256_of_extracted_source']:raise SystemExit('Changed inherited definition: '+item['name'])
if len(sys.argv)>1:
    directory=root/sys.argv[1];run=json.loads((directory/'manifest.json').read_text())
    for path,digest in run['inputs'].items():
        if hashlib.sha256((root/path).read_bytes()).hexdigest()!=digest:raise SystemExit('Changed input: '+path)
    for path,digest in run['outputs'].items():
        if hashlib.sha256((directory/path).read_bytes()).hexdigest()!=digest:raise SystemExit('Changed output: '+path)
print(json.dumps({'verified_core_definitions':len(manifest['extracted_definitions']),'run_verified':len(sys.argv)>1}))
