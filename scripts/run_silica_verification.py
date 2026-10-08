#!/usr/bin/env python3
"""Run mineral PDEs in MOOSE and compare to independent extent/FV references.

Requires the pinned MOOSE executable plus numpy, scipy and matplotlib. The
reference uses molar diagnostics internally; MOOSE differences mass storage.
"""
import argparse
import csv
import gzip
import hashlib
import json
import math
import platform
import shutil
import subprocess
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.sparse import lil_matrix

ROOT = Path(__file__).resolve().parents[1]
MS, MW, MC, RHO, RT = .096113, .018015, .060083, 1000., 8.31446261815324*298.15
INERT, PHI0, RATE, L = .3, .05, 1., 1e-6
NW0 = (650.-MS*5)/MW
XEQ = 5/(5+NW0)
QEQ = XEQ/(1-XEQ)**2


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open() as stream:
        return {k: np.array([float(r[k]) for r in rows])
                for rows in [list(csv.DictReader(stream))] for k in rows[0]}


def chemistry(n, c):
    """Reference chemistry written from conserved mole amounts, not C++ code."""
    phi = MC*c/RHO
    water = (RHO*(1-INERT-phi)-MS*n)/MW
    x = n/(n+water)
    q = np.log(x)-(MS/MW)*np.log1p(-x)
    force = np.log(x)-2*np.log1p(-x)-math.log(QEQ)
    return q, RATE*force, water


def extent_reference(n0, times):
    c0 = RHO*PHI0/MC
    def rhs(t, extent):
        return [chemistry(n0-extent[0], c0+extent[0])[1]]
    sol = solve_ivp(rhs, (0., float(times[-1])), [0.], method='DOP853',
                    rtol=2e-12, atol=1e-13, t_eval=times)
    if not sol.success:
        raise RuntimeError(sol.message)
    return n0-sol.y[0], c0+sol.y[0]


def fv_reference(cells, times):
    """Conservative cell-centered MOL, zero boundary flux, sparse BDF solve."""
    h = 1/cells
    xc = (np.arange(cells)+.5)*h
    # Exact cell averages of the cosine initial inventory.
    n0 = 5+4*np.sin(np.pi*h/2)/(np.pi*h/2)*np.cos(np.pi*xc)
    c0 = np.full(cells, RHO*PHI0/MC)
    def rhs(t, state):
        n, c = state[:cells], state[cells:]
        q, rate, _ = chemistry(n, c)
        flux = np.zeros(cells+1)
        flux[1:-1] = -(L*RT/MS**2)*np.diff(q)/h
        return np.r_[-np.diff(flux)/h-rate, rate]
    sparsity = lil_matrix((2*cells, 2*cells), dtype=int)
    for k in range(cells):
        for j in range(max(0,k-1), min(cells,k+2)):
            sparsity[k,j] = sparsity[k,cells+j] = 1
        sparsity[cells+k,k] = sparsity[cells+k,cells+k] = 1
    sol = solve_ivp(rhs, (0., float(times[-1])), np.r_[n0,c0], method='BDF',
                    rtol=2e-10, atol=1e-11, jac_sparsity=sparsity.tocsr(), t_eval=times)
    if not sol.success:
        raise RuntimeError(sol.message)
    return xc, sol.y[:cells].T, sol.y[cells:].T, {'nfev':sol.nfev,'njev':sol.njev,
            'relative_silicon_drift': float(np.max(np.abs(np.mean(sol.y[:cells]+sol.y[cells:],axis=0)-np.mean(n0+c0)))/np.mean(n0+c0))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary',type=Path,default=ROOT/'moose_app/olivine_carbonation-opt')
    parser.add_argument('--output',type=Path,default=ROOT/'data/silica')
    parser.add_argument('--reuse-completed',action='store_true',
                        help='Reuse completed solver outputs only after checking the saved solver fingerprint and requested time grid')
    args=parser.parse_args()
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    runtime=ROOT/'.agent-runtime/silica-verification'; runtime.mkdir(parents=True,exist_ok=True)
    commands=[]; checks=[]; batches={}; convergence={}; spatial=[]
    solver_files=[args.binary.resolve(),ROOT/'moose_app/lib/.libs/libolivine_carbonation-opt.so']
    for folder,pattern in [('moose_app/src','*.C'),('moose_app/include','*.h'),('moose_app/examples/silica','*.i')]:
        solver_files.extend((ROOT/folder).rglob(pattern))
    fingerprint={str(p.relative_to(ROOT)):sha(p) for p in sorted(solver_files)}
    saved_path=runtime/'solver-fingerprint.json'
    saved=json.loads(saved_path.read_text()) if saved_path.exists() else {}
    reuse_allowed=args.reuse_completed and saved.get('source_fingerprint')==fingerprint
    def check(name,error,tolerance,category,**details):
        checks.append(dict(name=name,error=float(error),tolerance=tolerance,
                           passed=bool(np.isfinite(error) and error<=tolerance),category=category,**details))
    def run(deck,name,overrides):
        base=runtime/name
        command=[str(args.binary.resolve()),'-i',str(ROOT/'moose_app/examples/silica'/deck),
                 'Outputs/file_base='+str(base),*overrides]
        csv_path=Path(str(base)+'.csv');log_path=runtime/(name+'.log')
        reused=False
        if reuse_allowed and csv_path.exists() and log_path.exists():
            prior=read_csv(csv_path)
            options=dict(v.split('=',1) for v in overrides if '=' in v)
            expected_end=float(options.get('Executioner/end_time',5 if deck=='spatial.i' else 40))
            expected_dt=float(options.get('Executioner/dt',.02 if deck=='spatial.i' else .05))
            reused=(abs(prior['time'][-1]-expected_end)<1e-8 and
                    abs(prior['time'][1]-expected_dt)<1e-10 and 'Solve Converged!' in log_path.read_text())
        if reused:
            result=subprocess.CompletedProcess(command,0,stdout=log_path.read_text())
        else:
            result=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
            log_path.write_text(result.stdout)
        with gzip.open(out/(name+'.log.gz'),'wb') as stream:
            stream.write(result.stdout.encode())
        commands.append({'name':name,'command':[str(Path(v).relative_to(ROOT)) if v.startswith(str(ROOT)+'/') else v for v in command],
                         'exit_code':result.returncode,'log':str((out/(name+'.log.gz')).relative_to(ROOT)),
                         'execution':'reused completed actual solve' if reused else 'new actual solve'})
        if result.returncode:
            raise RuntimeError(name+' failed: '+result.stdout[-4000:])
        shutil.copyfile(Path(str(base)+'.csv'),out/(name+'.csv'))
        print(('reused completed ' if reused else 'completed ')+name,flush=True)
        return read_csv(Path(str(base)+'.csv')), base
    def invariants(rows,name):
        n,c,w=rows['aq_si'],rows['solid_mass']/MC,rows['water']
        for element,amount in [('Si',n+c),('H',4*n+2*w),('O',4*n+2*c+w)]:
            check(name+'_'+element+'_conservation',np.max(np.abs(amount-amount[0]))/abs(amount[0]),1e-9,'implementation')
        check(name+'_positive_phases',max(0.,-min(rows['phi_min'].min(),rows['fluid_min'].min())),0.,'implementation')
        check(name+'_nonnegative_reaction_power',max(0.,-rows['power'].min()),0.,'analytical')
    for deck,label,n0 in [('batch.i','precipitation',10.),('dissolution.i','dissolution',1.)]:
        rows,_=run(deck,label,['Executioner/dt=0.0125']); invariants(rows,label)
        nr,cr=extent_reference(n0,rows['time'])
        np.savetxt(out/(label+'_reference.csv'),np.c_[rows['time'],nr,cr],delimiter=',',header='time,aq_si,solid_si',comments='')
        check(label+'_trajectory',np.max(np.abs(rows['aq_si']-nr)),.001,'analytical')
        check(label+'_direction',max(0.,-(rows['solid_mass'][-1]-rows['solid_mass'][0])*(1 if n0>5 else -1)),0.,'implementation')
        check(label+'_equilibrium',abs(rows['rate'][-1]),.002,'analytical')
        batches[label]={'initial_aqueous_si':n0,'final_aqueous_si':float(rows['aq_si'][-1]),
                        'mineral_change_mol':float((rows['solid_mass'][-1]-rows['solid_mass'][0])/MC),
                        'max_trajectory_error':float(np.max(np.abs(rows['aq_si']-nr)))}
        for scheme,minimum in [('implicit-euler',.9),('bdf2',1.7)]:
            errors=[]
            steps=[.1,.05,.025,.0125,.00625,.003125]
            for dt in steps:
                rr,_=run(deck,f'{label}_{scheme}_{dt:g}',[f'Executioner/scheme={scheme}',f'Executioner/dt={dt}','Executioner/end_time=5'])
                ref,_=extent_reference(n0,rr['time'])
                errors.append(float(abs(rr['aq_si'][-1]-ref[-1])))
                invariants(rr,f'{label}_{scheme}_{dt:g}')
            orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist()
            check(label+'_'+scheme+'_order',max(0.,minimum-min(orders)),0.,'convergence',errors=errors,orders=orders,steps=steps)
            check(label+'_'+scheme+'_fine_error',errors[-1],.001,'convergence')
            convergence[label+'_'+scheme]={'steps':steps,'errors':errors,'orders':orders}
    reference_times=np.array([0.,1.,5.])
    refs={}
    for cells in (512,1024):
        xc,n,c,meta=fv_reference(cells,reference_times); refs[cells]=(xc,n,c)
        for i,t in enumerate(reference_times):
            np.savetxt(out/f'fv_{cells}_t{t:g}.csv',np.c_[xc,n[i],c[i]],delimiter=',',header='x,aq_si,solid_si',comments='')
        check('fv_'+str(cells)+'_conservation',meta['relative_silicon_drift'],1e-10,'analytical',**{'solver':meta})
    ref_error=float(np.sqrt(np.mean((refs[512][1][-1]-refs[1024][1][-1].reshape(512,2).mean(axis=1))**2)))
    check('fv_reference_refinement',ref_error,.0001,'convergence')
    for cells in (16,32,64,128):
        rows,base=run('spatial.i',f'spatial_{cells}',[f'Mesh/nx={cells}','Executioner/dt=0.005'])
        invariants(rows,'spatial_'+str(cells))
        final_step=len(rows['time'])-1
        profiles={}
        max_cell=0.; previous=[]; worst=None
        for k,t in enumerate(rows['time']):
            prof=read_csv(Path(f'{base}_profile_{k:04d}.csv'))
            nodes=read_csv(Path(f'{base}_nodes_{k:04d}.csv'))
            previous.append(prof)
            if k:
                h=1/cells; dt=rows['time'][k]-rows['time'][k-1]
                n=prof['n_si']; old=previous[k-1]['n_si']
                derivative=(n-old)/dt if k==1 else (1.5*n-2*old+.5*previous[k-2]['n_si'])/dt
                flux_cell=-(L*RT/MS)*np.diff(nodes['q'])/h
                flux=np.zeros(cells+1)
                flux[1:-1]=.5*(flux_cell[:-1]+flux_cell[1:])+12*(L*RT/MS)/h*np.diff(-prof['e'])
                balance=MS*derivative+MS*prof['r_si']+np.diff(flux)/h
                local_max=float(np.max(np.abs(balance)))
                if local_max > max_cell:
                    cell=int(np.argmax(np.abs(balance)))
                    max_cell=local_max
                    worst={'time':float(t),'step':k,'cell_zero_based':cell,'x':float(prof['x'][cell]),
                           'dt':float(dt),'scheme':'implicit-euler' if k==1 else 'bdf2',
                           'storage_rate':float(MS*derivative[cell]),'reaction_loss':float(MS*prof['r_si'][cell]),
                           'left_flux':float(flux[cell]),'right_flux':float(flux[cell+1]),
                           'cell_width':h,'signed_residual':float(balance[cell])}
            if any(abs(t-v)<1e-8 for v in reference_times):
                profiles[float(reference_times[np.argmin(abs(reference_times-t))])]=prof
                shutil.copyfile(Path(f'{base}_profile_{k:04d}.csv'),out/f'spatial_{cells}_t{t:g}.csv')
                shutil.copyfile(Path(f'{base}_nodes_{k:04d}.csv'),out/f'spatial_{cells}_nodes_t{t:g}.csv')
        worst['files']=[]
        for step in range(max(0,worst['step']-2),worst['step']+1):
            name=f'spatial_{cells}_worst_profile_{step:04d}.csv'
            shutil.copyfile(Path(f'{base}_profile_{step:04d}.csv'),out/name)
            worst['files'].append(name)
        name=f"spatial_{cells}_worst_nodes_{worst['step']:04d}.csv"
        shutil.copyfile(Path(f"{base}_nodes_{worst['step']:04d}.csv"),out/name)
        worst['files'].append(name)
        reference_n=refs[1024][1][-1].reshape(cells,1024//cells).mean(axis=1)
        reference_c=refs[1024][2][-1].reshape(cells,1024//cells).mean(axis=1)
        final=profiles[5.]
        n_error=float(np.sqrt(np.mean((final['n_si']-reference_n)**2)))
        c_error=float(np.sqrt(np.mean((RHO*final['phi_C']/MC-reference_c)**2)))
        change=RHO*(final['phi_C']-PHI0)/MC
        check('spatial_'+str(cells)+'_both_directions',max(0.,-change.max(),change.min()),0.,'implementation')
        check('spatial_'+str(cells)+'_cell_balance',max_cell,1e-7,'implementation')
        spatial.append({'cells':cells,'dt':.005,'aqueous_l2_error':n_error,'mineral_l2_error':c_error,
                        'max_cell_mass_residual':max_cell,'worst_cell_audit':worst,'mineral_gain_mol':float(change.max()),'mineral_loss_mol':float(change.min())})
    n_errors=[s['aqueous_l2_error'] for s in spatial]
    check('spatial_monotone_refinement',max(0.,max(b-a for a,b in zip(n_errors,n_errors[1:]))),0.,'convergence')
    check('spatial_fine_relative_profile_error',n_errors[-1]/np.sqrt(np.mean(refs[1024][1][-1]**2)),.01,'convergence')
    # Independent temporal refinement on one fixed mesh, measured at the same time.
    time_profiles=[]
    for dt in (.04,.02,.01):
        rr,base=run('spatial.i',f'spatial_time_{dt:g}',['Mesh/nx=64',f'Executioner/dt={dt}'])
        pp=read_csv(Path(f'{base}_profile_{len(rr["time"])-1:04d}.csv'))
        time_profiles.append(pp['n_si'])
        shutil.copyfile(Path(f'{base}_profile_{len(rr["time"])-1:04d}.csv'),out/f'spatial_time_{dt:g}_final.csv')
    differences=[float(np.sqrt(np.mean((a-b)**2))) for a,b in zip(time_profiles,time_profiles[1:])]
    time_order=math.log2(differences[0]/differences[1])
    check('spatial_time_self_convergence',max(0.,1.7-time_order),0.,'convergence',differences=differences,order=time_order)
    scientific=[]
    for folder,pattern in [('moose_app/src','*.C'),('moose_app/include','*.h'),('moose_app/examples/silica','*.i')]:
        scientific.extend((ROOT/folder).rglob(pattern))
    scientific.extend([Path(__file__).resolve(),ROOT/'environment/toolchain.json',ROOT/'environment/moose-linux-64.lock'])
    report={'status':'passed' if all(c['passed'] for c in checks) else 'failed',
            'scope':'Actual MOOSE mineral precipitation/dissolution PDE and ODE verification on an exact synthetic silica reduction; no physical validation or full carbonation-network simulation.',
            'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
            'moose_revision':subprocess.check_output(['git','-C',str(ROOT/'.agent-runtime/moose'),'rev-parse','HEAD'],text=True).strip(),
            'framework_modifications':subprocess.check_output(['git','-C',str(ROOT/'.agent-runtime/moose'),'status','--porcelain','--untracked-files=no'],text=True).strip(),
            'executable_sha256':sha(args.binary.resolve()),'sources':{str(p.relative_to(ROOT)):sha(p) for p in sorted(scientific)},
            'parameters':{'rho':RHO,'phi_A':.2,'phi_B':.1,'phi_C_initial':PHI0,'M_Si':MS,'M_water':MW,'M_C':MC,
                          'RT':RT,'Qeq':QEQ,'rate_coefficient':RATE,'mobility':L,'spatial_length':1.,'sigma':12},
            'reference_methods':{'batch':'scalar extent, DOP853, rtol=2e-12 atol=1e-13',
                                 'spatial':'cell-centered conservative MOL, BDF, rtol=2e-10 atol=1e-11, 512/1024 cells'},
            'commands':commands,'checks':checks,'batch':batches,'time_convergence':convergence,
            'spatial_convergence':spatial,'fv_reference_difference':ref_error,'spatial_time_order':time_order}
    report['data_hashes']={str(p.relative_to(ROOT)):sha(p) for p in sorted(out.glob('*')) if p.is_file()}
    report['solver_fingerprint']=fingerprint
    report['reuse_basis']=saved.get('reuse_basis') if any(c['execution'].startswith('reused') for c in commands) else None
    saved_path.write_text(json.dumps({'source_fingerprint':fingerprint,'reuse_basis':'Saved source and linked-artifact fingerprint from completed solver suite.'},indent=2)+'\n')
    (ROOT/'verification/silica-results.json').write_text(json.dumps(report,indent=2)+'\n')
    plot(out,report)
    print(json.dumps({'status':report['status'],'checks':len(checks),'failures':[c for c in checks if not c['passed']]},indent=2))
    return 0 if report['status']=='passed' else 1


def plot(out,report):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    figs=ROOT/'figures';figs.mkdir(exist_ok=True)
    fig,axes=plt.subplots(1,2,figsize=(8,3),constrained_layout=True)
    for label,color in [('precipitation','#1864ab'),('dissolution','#d9480f')]:
        rows=read_csv(out/(label+'.csv'));ref=read_csv(out/(label+'_reference.csv'))
        axes[0].plot(rows['time'],rows['aq_si'],color=color,label=label.title())
        axes[0].plot(ref['time'][::40],ref['aq_si'][::40],'o',ms=3,mfc='none',color=color)
        axes[1].plot(rows['time'],(rows['solid_mass']-rows['solid_mass'][0])/MC,color=color)
    axes[0].set(xlabel='Time (s)',ylabel='Aqueous Si (mol / mixture m³)');axes[0].legend(frameon=False)
    axes[1].set(xlabel='Time (s)',ylabel='Mineral Si change (mol m$^{-3}$)');axes[1].axhline(0,color='.5',lw=.6)
    fig.savefig(figs/'silica-batch.pdf');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(8,3),constrained_layout=True)
    for t,color in [(0.,'.5'),(1.,'#1864ab'),(5.,'#d9480f')]:
        rows=read_csv(out/f'spatial_128_t{t:g}.csv')
        axes[0].plot(rows['x'],rows['n_si'],color=color,label=f'{t:g} s')
        if t:
            ref=read_csv(out/f'fv_1024_t{t:g}.csv');axes[0].plot(ref['x'][::40],ref['aq_si'][::40],'o',ms=3,mfc='none',color=color)
            axes[1].plot(rows['x'],RHO*(rows['phi_C']-PHI0)/MC,color=color,label=f'{t:g} s')
    axes[0].set(xlabel='Position (m)',ylabel='Aqueous Si (mol / mixture m³)');axes[0].legend(frameon=False)
    axes[1].set(xlabel='Position (m)',ylabel='Mineral Si change (mol m$^{-3}$)');axes[1].axhline(0,color='.5',lw=.6)
    fig.savefig(figs/'silica-column.pdf');plt.close(fig)


if __name__=='__main__':
    raise SystemExit(main())
