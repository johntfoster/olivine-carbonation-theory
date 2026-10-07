#!/usr/bin/env python3
"""Quantitative executable verification, with independent analytical expectations."""
import argparse, csv, hashlib, json, math, os, re, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def hashes():
 paths=[ROOT/'moose_app/Makefile']
 for folder,glob in [('moose_app/src','*.C'),('moose_app/include','*.h'),('moose_app/test/tests','*.i'),('scripts','check_implementation.py')]: paths.extend((ROOT/folder).rglob(glob))
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
def verify(binary,output):
 output.mkdir(parents=True,exist_ok=True); results=[]; commands=[]
 def check(name,error,tol,category='implementation'):
  results.append({'name':name,'category':category,'error':error,'tolerance':tol,'passed':math.isfinite(error) and error<=tol})
 def run(deck,name,extra=()):
  base=output/name
  command=[str(binary),'-i',str(ROOT/'moose_app/test/tests'/deck),'Outputs/file_base='+str(base),*extra]
  process=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
  (output/(name+'.log')).write_text(process.stdout); commands.append({'command':[os.path.relpath(binary,ROOT),'-i',str(Path('moose_app/test/tests')/deck),'Outputs/file_base='+os.path.relpath(base,ROOT),*extra],'exit_code':process.returncode})
  if process.returncode: raise RuntimeError(name+' failed:\n'+process.stdout[-5000:])
  with base.with_suffix('.csv').open() as f: rows=list(csv.DictReader(f))
  return rows,process.stdout
 for deck,name in [('residuals/nonlinear_mass.i','mass_euler'),('residuals/bdf2_mass.i','mass_bdf2')]:
  rows,_=run(deck,name)
  # Initial complete mass 0.25*(1+0.25), constant source 1, closed boundaries.
  error=max(abs(float(r['p_average'])*(1+float(r['p_average']))-0.3125-float(r['time'])) for r in rows[1:])
  check(name+'_conservation',error,1e-10)
 for deck,name in [('residuals/mechanics.i','mechanics'),('residuals/gauss_flux.i','gauss_outward'),('residuals/traction_insertion.i','traction_insertion')]:
  rows,_=run(deck,name)
  for quantity in ('u_l2','tau_l2','electric_l2'): check(name+'_'+quantity,max(float(r[quantity]) for r in rows[1:]),1e-10,'finite_deformation' if quantity=='u_l2' else 'implementation')
 for deck,name in [('residuals/nonlinear_mass.i','mass_jacobian'),('residuals/mechanics.i','coupled_jacobian'),('residuals/traction_insertion.i','insertion_jacobian'),('eg/poisson_1d.i','eg_jacobian')]:
  _,log=run(deck,name,['-snes_test_jacobian','-snes_force_iteration'])
  ratios=[float(v) for v in re.findall(r'\|\|J - Jfd\|\|_F/\|\|J\|\|_F\s*=\s*([0-9.eE+\-]+)',log)]
  if not ratios: raise RuntimeError('Missing PETSc finite-difference Jacobian evidence: '+name)
  check(name+'_relative_fd',max(ratios),2e-7)
 for dim in (1,2,3):
  sizes=(4,8,16) if dim<3 else (2,4,8); errors=[]
  for n in sizes:
   rows,_=run(f'eg/poisson_{dim}d.i',f'eg_{dim}d_{n}',[f'Mesh/n{axis}={n}' for axis in 'xyz'[:dim]])
   errors.append(float(rows[-1]['l2']))
   # Exact integral of -laplacian product(x_i(1-x_i)) over the unit cube.
   expected=2*dim*(1/6)**(dim-1)
   check(f'eg_{dim}d_{n}_boundary_conservation',abs(float(rows[-1]['outward_flux'])-expected),1e-9)
  rates=[math.log(a/b,2) for a,b in zip(errors,errors[1:])]
  check(f'eg_{dim}d_l2_order',max(0,1.7-min(rates)),0,'convergence')
  results[-1].update({'mesh_sizes':list(sizes),'l2_errors':errors,'observed_orders':rates,'minimum_order':1.7})
 rows,_=run('residuals/three_minerals.i','three_minerals')
 def mineral_root(J,p,K,Ks,phi0):
  lo,hi=-100.0,1.0
  for _ in range(150):
   y=(lo+hi)/2
   f=Ks*y+(1-K/(phi0*Ks))*p*math.exp(y)-K/phi0*math.log(J)
   if f>0: hi=y
   else: lo=y
  return math.exp((lo+hi)/2)
 for r in rows[1:]:
  J=1+0.1*float(r['time']); B=1.0
  for label,K,Ks,phi0 in [('A',0.5,20,0.15),('B',0.3,30,0.1),('C',0.1,40,0.05)]:
   b=mineral_root(J,0.2,K,Ks,phi0); b0=mineral_root(1,0.2,K,Ks,phi0)
   check('three_minerals_root_'+label+'_t'+r['time'],abs(float(r['root'+label])-b),1e-10,'finite_deformation')
   phi=phi0*b/(b0*J); B-=phi*K/phi0/(Ks+(1-K/(phi0*Ks))*0.2*b)
  check('three_minerals_biot_t'+r['time'],abs(float(r['biot'])-B),1e-10,'finite_deformation')
 cross_errors=[]
 for n in (4,8,16):
  rows,_=run('eg/cross_diffusion.i',f'cross_{n}',[f'Mesh/nx={n}'])
  cross_errors.append([float(rows[-1]['p_l2']),float(rows[-1]['q_l2'])])
 for column,label in enumerate(('p','q')):
  rates=[math.log(a[column]/b[column],2) for a,b in zip(cross_errors,cross_errors[1:])]
  check('eg_cross_'+label+'_order',max(0,1.7-min(rates)),0,'convergence')
  results[-1].update({'l2_errors':[r[column] for r in cross_errors],'observed_orders':rates})
 _,log=run('eg/cross_diffusion.i','cross_jacobian',['-snes_test_jacobian','-snes_force_iteration'])
 ratios=[float(v) for v in re.findall(r'\|\|J - Jfd\|\|_F/\|\|J\|\|_F\s*=\s*([0-9.eE+\-]+)',log)]
 if not ratios: raise RuntimeError('Missing cross-component FD evidence')
 check('eg_cross_jacobian_relative_fd',max(ratios),2e-7)
 framework=Path(os.environ.get('MOOSE_DIR', ROOT/'.agent-runtime/moose'))
 revision=subprocess.check_output(['git','-C',str(framework),'rev-parse','HEAD'],text=True).strip()
 if revision!='abafb58b67a6037c6723ffeb19647c84484466da': raise RuntimeError('Unexpected MOOSE revision '+revision)
 dirty=subprocess.check_output(['git','-C',str(framework),'diff','--name-only'],text=True).splitlines()
 report={'status':'passed' if all(r['passed'] for r in results) else 'failed','scope':'Synthetic residual, Jacobian, conservation and EG convergence verification; no calibration or physical validation.','python':sys.version.split()[0],'moose_revision':revision,'framework_modifications':dirty,'source_hashes':hashes(),'executable_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'commands':commands,'checks':results,'physical_validation':'not performed'}
 (ROOT/'verification/implementation-results.json').write_text(json.dumps(report,indent=2)+'\n')
 failures=[r for r in results if not r['passed']]
 print(json.dumps({'status':report['status'],'checks':len(results),'failures':failures},indent=2))
 return not failures
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--binary',type=Path,default=ROOT/'moose_app/olivine_carbonation-opt'); p.add_argument('--output',type=Path,default=ROOT/'.agent-runtime/implementation-tests'); a=p.parse_args()
 sys.exit(0 if verify(a.binary.resolve(),a.output.resolve()) else 1)
