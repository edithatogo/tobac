"""Record actual library execution, not a substitute labelled as that library."""
import argparse, importlib.metadata, json, shutil, subprocess
from pathlib import Path
import numpy as np

p=argparse.ArgumentParser();p.add_argument('--mode',choices=['voiage','sourceright'],required=True);p.add_argument('--out',required=True)
a=p.parse_args();receipt={'tool':a.mode,'success':False}
try:
    if a.mode=='voiage':
        from voiage.analysis import DecisionAnalysis
        from voiage.schema import ValueArray
        rng=np.random.default_rng(20261024);errors=[]
        for i in range(51):
            v=np.array([[0.,2.],[2.,0.]]) if i==0 else rng.normal(size=(37,4))
            got=float(DecisionAnalysis(ValueArray.from_numpy(v)).evpi())
            expected=float(v.max(axis=1).mean()-v.mean(axis=0).max())
            errors.append(abs(got-expected))
        receipt.update(version=importlib.metadata.version('voiage'),cases=51,max_absolute_error=max(errors),scope='equal-weight EVPI only; not EVPPI/EVSI or empirical validation',success=max(errors)<1e-9)
    else:
        exe=shutil.which('sourceright')
        if not exe:raise FileNotFoundError('sourceright not installed')
        r=subprocess.run([exe,'validate-csl','--json','evidence/references.csl.json'],capture_output=True,text=True,timeout=120)
        receipt.update(exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr,scope='CSL structural validation only, not provider-backed numerical/applicability verification',success=r.returncode==0)
except Exception as e:receipt['error']=repr(e)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
raise SystemExit(0 if receipt['success'] else 2)
