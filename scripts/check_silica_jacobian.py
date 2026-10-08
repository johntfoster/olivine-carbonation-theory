#!/usr/bin/env python3
"""Compare the coupled mineral/EG AD Jacobian to PETSc finite differences."""
import gzip
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    command=['moose_app/olivine_carbonation-opt','-i','moose_app/examples/silica/spatial.i',
             'Mesh/nx=8','Executioner/end_time=0.02',
             'Outputs/file_base=.agent-runtime/silica-jacobian',
             '-snes_test_jacobian','-snes_force_iteration']
    result=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    log=ROOT/'data/silica/jacobian.log.gz';log.parent.mkdir(parents=True,exist_ok=True)
    with gzip.open(log,'wb') as stream: stream.write(result.stdout.encode())
    ratios=[float(v) for v in re.findall(r'\|\|J - Jfd\|\|_F/\|\|J\|\|_F\s*=\s*([0-9.eE+\-]+)',result.stdout)]
    passed=result.returncode==0 and bool(ratios) and max(ratios)<2e-7
    paths=[Path(__file__).resolve(),ROOT/'moose_app/Makefile']
    for folder,suffix in [('src','*.C'),('include','*.h'),('examples','*.i')]:
        paths.extend((ROOT/'moose_app'/folder).rglob(suffix))
    report={'status':'passed' if passed else 'failed','category':'coupled-AD-implementation-verification',
            'command':command,'exit_code':result.returncode,'relative_fd_differences':ratios,'tolerance':2e-7,
            'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},
            'artifacts':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'moose_app/olivine_carbonation-opt',
                ROOT/'moose_app/lib/.libs/libolivine_carbonation-opt.so',log]}}
    (ROOT/'verification/silica-jacobian-results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'relative_fd_differences':ratios}))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
