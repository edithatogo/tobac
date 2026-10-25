"""Execute genuine installed-Voiage parity. No unavailable-package fallback."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import platform
import numpy as np
from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
from .voiage_adapter import installed_evpi, installed_partial, partition_problem


def qualify(path) -> dict:
    destination=Path(path)
    if destination.exists():raise FileExistsError('Use a new qualification receipt')
    receipt={'schema':'tobac.voiage-qualification.v1','expected_version':'2.2.0',
             'success':False,'installed_library_executed':False,'python':platform.python_version(),
             'status':'blocked','checks':[],
             'scope':'released EVPI on exact weighted and finite-partition transforms only; no generic EVSI or structural API certification'}
    cases=[('uniform',[.5,.5]),('unequal',[.9,.1]),('zero_mass',[1.,0.]),('small_mass',[1e-8,1-1e-8])]
    try:
        for name,weights in cases:
            p=DecisionProblem([[10.,0.],[0.,10.]],('a','b'),'normalised fixture units',weights)
            actual=installed_evpi(p);receipt['installed_library_executed']=True
            error=abs(actual['value']-exact_evpi(p))
            receipt['checks'].append({'case':name,'error':error,'value':actual['value'],'unit':actual['value_unit']})
            if error>1e-11 or actual['value_unit']!=p.value_unit:raise ArithmeticError('Weighted Voiage parity failed')
        p=DecisionProblem([[10,0],[0,10],[10,0],[0,10]],('a','b'),'normalised fixture units',[.15,.15,.35,.35])
        labels=['first','first','second','second']
        actual=installed_partial(p,labels)
        expected=exact_partial_information(p,labels)
        if abs(actual['value']-expected)>1e-11 or expected!=0:raise ArithmeticError('Structure-only counterexample failed')
        receipt['checks'].append({'case':'identical_structure_only','value':actual['value'],'joint_perfect':exact_evpi(p),'expected_structure_only':0.})
        receipt.update(success=True,status='passed',version=actual['voiage_version'])
    except Exception as exc:
        receipt.update(error=repr(exc),status='failed' if receipt['installed_library_executed'] else 'blocked')
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    return receipt


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
    result=qualify(a.out);print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['success'] else 2)

if __name__=='__main__':main()
