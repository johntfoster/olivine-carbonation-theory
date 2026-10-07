#!/usr/bin/env python3
"""Fresh source-specialization consistency checks; stdlib only; no PDE solver."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json,math,platform,sys
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def record(name,error=0.,tol=0.,category='algebraic-consistency',details=None):
 checks.append(dict(name=name,category=category,error=float(error),tolerance=tol,passed=math.isfinite(float(error)) and abs(error)<=tol,details=details))
def close(name,a,b,tol=1e-8,details=None):
 scale=max(1.,abs(a),abs(b));record(name,abs(a-b)/scale,tol,details=details)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def trans(a):return [list(c) for c in zip(*a)]
def mm(a,b):return [[dot(r,c) for c in zip(*b)] for r in a]
def mv(a,b):return [dot(r,b) for r in a]
def scale(a,c):return [[c*x for x in r] for r in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def ident():return [[float(i==j) for j in range(3)] for i in range(3)]
def det(a):return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def inv(a):
 d=det(a);return [[(-1)**(i+j)*det2([[a[r][c] for c in range(3) if c!=i] for r in range(3) if r!=j])/d for j in range(3)] for i in range(3)]
def det2(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def norm(a):return max(abs(v) for r in a for v in r)
def mdiff(a,b):return norm(add(a,scale(b,-1)))/max(1.,norm(a),norm(b))
def fd(fun,x,h):return (fun(x+h)-fun(x-h))/(2*h)

# Exact chemical bookkeeping: A,B,C,H+,OH-,CO2,HCO3-,CO3--,Mg++,H4SiO4,H3SiO4-,water.
elements=['Mg','Si','C','H','O']
atoms=[[2,1,0,0,4],[1,0,1,0,3],[0,1,0,0,2],[0,0,0,1,0],[0,0,0,1,1],[0,0,1,0,2],[0,0,1,1,3],[0,0,1,0,3],[1,0,0,0,0],[0,1,0,4,4],[0,1,0,3,4],[0,0,0,2,1]]
valence=[0,0,0,1,-1,0,-1,-2,2,0,-1,0]
aw=list(map(Q,['0.024305','0.028085','0.012011','0.001008','0.015999']))
mass=[dot(a,aw) for a in atoms]
stoich=[[0]*12 for _ in range(7)]
for c,entries in zip(stoich,[{0:-1,3:-4,8:2,9:1},{8:-1,6:-1,1:1,3:1},{9:-1,2:1,11:2},{11:-1,3:1,4:1},{5:-1,11:-1,3:1,6:1},{6:-1,3:1,7:1},{9:-1,3:1,10:1}]):
 for i,n in entries.items():c[i]=n
record('seven_mechanisms_exact_atom_conservation',max(abs(dot(c,[a[j] for a in atoms])) for c in stoich for j in range(5)),details={'elements':elements,'stoichiometric_columns_transposed':stoich})
record('seven_mechanisms_exact_mass_conservation',max(abs(dot(c,mass)) for c in stoich),details={'atomic_masses_kg_per_mol':list(map(str,aw))})
record('seven_mechanisms_exact_charge_conservation',max(abs(dot(c,valence)) for c in stoich))
net=[stoich[0][i]+2*stoich[1][i]+stoich[2][i]+2*stoich[4][i] for i in range(12)]
record('net_carbonation_reaction',[a-b for a,b in zip(net,[-1,2,1,0,0,-2,0,0,0,0,0,0])].count(0)-12)
rates=list(map(Q,['0.2','0.3','0.4','0.6','0.8','1.1','0.5']))
productions=[sum(mass[i]*stoich[m][i]*rates[m] for m in range(7)) for i in range(12)]
record('material_insertion_mass_sum_zero',sum(productions))
record('homogeneous_phase_offset_cancels',max(abs(dot(c[3:],mass[3:])) for c in stoich[3:]))

# Kinematics, Piola work, traction and flux maps at a nonspherical finite deformation.
F=[[1.12,0.17,-0.04],[0.03,0.91,0.08],[0.02,-0.06,1.04]];J=det(F);Fi=inv(F)
sigma=[[3.2,.5,.2],[.5,1.4,-.3],[.2,-.3,2.1]]
P=scale(mm(sigma,trans(Fi)),J)
dF=[[.01,-.02,.003],[.006,.012,-.007],[.002,.004,-.01]]
close('piola_virtual_work',sum(dot(a,b) for a,b in zip(P,dF)),J*sum(dot(a,b) for a,b in zip(sigma,mm(dF,Fi))),1e-13)
N=[.3,.4,math.sqrt(.75)];area_vec=[J*x for x in mv(trans(Fi),N)]
record('nanson_nominal_traction',max(abs(a-b) for a,b in zip(mv(P,N),mv(sigma,area_vec))),1e-13)
w=[.2,-.13,.05];W=[J*x for x in mv(Fi,w)]
close('piola_flux_surface_invariance',dot(W,N),dot(w,area_vec),1e-13)
# Variable deformation exact one-dimensional divergence: x=X+X²/10.
X=Q(2,5);x=X+X*X/10;Fx=1+X/5
record('nonuniform_piola_divergence',2*x*Fx-Fx*2*x)
record('weak_mass_outward_flux_sign',Q(14,3)-(-Q(13,3)+9))
record('weak_gauss_outward_displacement_sign',Q(1)+Q(3)-Q(4))

# Mineral equation, constitutive energy derivatives and trace restriction.
rho0=3300.;q=.6;K=4.8e9;Ks=130e9;Gs=5e9;H=(K/q)/(1-K/(q*Ks));pressure=2e8
params={'F':F,'rho0':rho0,'phi_s0':q,'K':K,'Ks':Ks,'Gs':Gs,'pressure':pressure}
def mineral(j,p,k=K,km=Ks,q0=q):
 u=k/(q0*km)*math.log(j)
 for _ in range(40):
  z=math.exp(u);res=km*u+(1-k/(q0*km))*p*z-(k/q0)*math.log(j)
  step=res/(km+(1-k/(q0*km))*p*z);u-=step
  if abs(step)<1e-15:break
 return math.exp(u)
z=mineral(J,pressure);rho=rho0/z
ph=q*z/J
shape=sum(x*x for r in F for x in r)*J**(-2/3)
def psi(f,r):
 j=det(f);zz=rho0/r
 return (Gs/2*(j**(-2/3)*sum(x*x for row in f for x in row)-3)+H/2*math.log(j/zz)**2+Ks/2*math.log(zz)**2)/rho0
close('mineral_root_residual',Ks*math.log(z)+(1-K/(q*Ks))*pressure*z,(K/q)*math.log(J),1e-12,params)
close('solid_pressure_from_helmholtz',rho*rho*fd(lambda r:psi(F,r),rho,rho*1e-5),pressure,2e-7)
Bmat=mm(F,trans(F));trB=sum(Bmat[i][i] for i in range(3));dev=add(Bmat,scale(ident(),-trB/3))
single=scale(add(scale(dev,Gs*J**(-2/3)),scale(ident(),H*math.log(J/z))),q/J)
Psingle=scale(mm(single,trans(Fi)),J)
num=[]
for i in range(3):
 row=[]
 for j in range(3):
  h=1e-6;fp=[r[:] for r in F];fm=[r[:] for r in F];fp[i][j]+=h;fm[i][j]-=h
  row.append(q*rho0*(psi(fp,rho)-psi(fm,rho))/(2*h))
 num.append(row)
record('solid_single_prime_energy_gradient',mdiff(num,Psingle),2e-8,details=params)
a=J/z
# Vary scalar a at fixed true deformation and density: F(a)=a^(1/3)*Fbar.
Fbar=scale(F,a**(-1/3))
trace=sum(single[i][i] for i in range(3))/3
trace_a=(q*rho0/J)*a*fd(lambda av:psi(scale(Fbar,av**(1/3)),rho),a,a*1e-5)
close('scalar_distention_coleman_noll_trace',trace,trace_a,2e-7)
# True deformation spherical variation at fixed distention gives same trace.
trace_true=(q*rho0/J)/3*fd(lambda h:psi(scale(F,math.exp(h)),rho),0.,1e-6)
close('true_deformation_trace_matches_distention',trace,trace_true,2e-8)
close('intrinsic_mineral_mean_stress',trace/ph-pressure,Ks*math.log(z)/z,1e-12)
bulk_mass=ph*rho
close('solid_constituent_mass_potential',fd(lambda m:m*psi(F,m/ph),bulk_mass,bulk_mass*1e-5),psi(F,rho)+pressure/rho,2e-7)
der=K*z/(q*J*(Ks+(1-K/(q*Ks))*pressure*z))
close('fixed_pressure_mineral_J_tangent',der,fd(lambda j:mineral(j,pressure),J,J*1e-5),2e-9)
B=1-ph*(J/z)*der
# The one-solid source uses K directly as the mixture-reference modulus.
Bsource=1-K*z/(J*(Ks+(1-K/(q*Ks))*pressure*z))
close('one_solid_source_biot_exact',B,Bsource,1e-14)
Wnew=q*rho0*psi(F,rho)
Wsource=q*Gs/2*(shape-3)+K/(2*(1-K/(q*Ks)))*math.log(J/z)**2+q*Ks/2*math.log(z)**2
close('one_solid_matched_log_energy_exact',Wnew,Wsource,1e-14)
z0=mineral(J,0.);Wzero=q*rho0*psi(F,rho0/z0)
Wdrained=q*Gs/2*(shape-3)+K/2*math.log(J)**2
close('drained_matched_log_energy',Wzero,Wdrained,1e-13)
# Three distinct minerals, masses frozen when differentiating.
qs=[.45,.10,.07];ks=[3.6e9,.6e9,.28e9];kms=[130e9,110e9,80e9]
def solid_mean(j,p):return sum((ki/(1-ki/(qi*kmi)))*math.log(j/mineral(j,p,ki,kmi,qi))/j for qi,ki,kmi in zip(qs,ks,kms))
zs=[mineral(J,pressure,ki,kmi,qi) for qi,ki,kmi in zip(qs,ks,kms)]
B3=1-sum(zz/J*ki/(kmi+(1-ki/(qi*kmi))*pressure*zz) for qi,zz,ki,kmi in zip(qs,zs,ks,kms))
close('three_solid_total_stress_pressure_tangent',-fd(lambda p:solid_mean(J,p)-p,pressure,1e4),B3,2e-8)
record('compressible_true_mass_distention',max(abs((J/zz)*(qi*zz/J)-qi) for qi,zz in zip(qs,zs)),1e-14)
Bsmall=1-sum(ki/kmi for ki,kmi in zip(ks,kms))
close('linearized_biot_limit',1-sum(ki/(kmi+(1-ki/(qi*kmi))*0) for qi,ki,kmi in zip(qs,ks,kms)),Bsmall,1e-14)
zi=mineral(J,pressure,K,1e18,q)
record('incompressible_mineral_limit',abs(zi-1),2e-9)

# Aqueous potential differentiation with all nine species; pure stdlib numerical derivative.
Ms=[float(m) for m in mass[3:]];masses=[.000001,.00002,.01,.003,.002,.001,.002,.001,.98]
v0=[1.8e-5,2.0e-5,3.1e-5,3.0e-5,2.9e-5,1.9e-5,4.2e-5,4.1e-5,1.8e-5]
g0=[-1000.,-2000.,-3000.,-2500.,-2300.,-1500.,-3500.,-3300.,-4000.]
R=8.314462618;theta=350.;Kf=2.2e9;p0=1e5;pf=4e7
m_tot=sum(masses);eta=[m/m_tot for m in masses]
def gibbs(p,m):
 n=[mi/Mi for mi,Mi in zip(m,Ms)];nt=sum(n);ex=math.exp(-(p-p0)/Kf)
 return sum(ni*(gi+R*theta*math.log(ni/nt)+vi*Kf*(1-ex)) for ni,gi,vi in zip(n,g0,v0))
def vol(p,m):return sum(mi/Mi*vi for mi,Mi,vi in zip(m,Ms,v0))*math.exp(-(p-p0)/Kf)
V=vol(pf,masses)
def helmholtz_at_volume(m,V):
 pref=sum(mi/Mi*vi for mi,Mi,vi in zip(m,Ms,v0));p=p0+Kf*math.log(pref/V)
 return gibbs(p,m)-p*V
close('aqueous_gibbs_density_legendre',fd(lambda p:gibbs(p,masses),pf,1e4),V,1e-10)
close('aqueous_pressure_from_volume_derivative',-fd(lambda vv:helmholtz_at_volume(masses,vv),V,V*1e-5),pf,3e-7)
n=[mi/Mi for mi,Mi in zip(masses,Ms)];nt=sum(n)
muhat=[(gi+R*theta*math.log(ni/nt)+vi*Kf*(1-math.exp(-(pf-p0)/Kf)))/Mi for gi,ni,vi,Mi in zip(g0,n,v0,Ms)]
errors=[]
for i,mi in enumerate(masses):
 h=max(mi*1e-4,1e-9);mp=masses[:];mmass=masses[:];mp[i]+=h;mmass[i]-=h
 num=(helmholtz_at_volume(mp,V)-helmholtz_at_volume(mmass,V))/(2*h)
 errors.append(abs(num-muhat[i])/max(1,abs(muhat[i])))
record('aqueous_constituent_mass_derivatives',max(errors),1e-5,details={'masses_kg':masses,'molar_volumes_m3_per_mol':v0,'pressure':pf,'temperature':theta,'component_relative_errors':errors})
close('aqueous_euler_identity',dot(masses,muhat),gibbs(pf,masses),1e-13)

# Source tau, transfer offsets and source force dissipation, not a replacement network.
vs=[.03,-.02,.01];rel=[.006,.004,-.002];gradtau=[.07,.02,-.01];vf=[a+b for a,b in zip(vs,rel)]
dtau_s=.5*dot(vs,vs);dtau_f=dtau_s+dot(rel,gradtau)
offset=dtau_f-.5*dot(vf,vf)
close('source_tau_normalization',dtau_s-.5*dot(vs,vs),0.,1e-15)
close('source_fluid_transfer_offset',offset,dot(rel,[a-b for a,b in zip(gradtau,vs)])-.5*dot(rel,rel),1e-15)
psi=[.4,.5,.3,.6];mu=[.9,1.1,.8,1.3];vel=[vs,vs,vs,vf];dtaus=[dtau_s]*3+[dtau_f]
L=[mui-ps+dt-.5*dot(v,v) for mui,ps,dt,v in zip(mu,psi,dtaus,vel)]
record('component_transfer_equations_recovered',max(abs(dt-(.5*dot(v,v)+li-(mui-ps))) for dt,v,li,mui,ps in zip(dtaus,vel,L,mu,psi)),1e-15)
nu=[-.07,.084,.061,-.075];aff=-dot(mu,nu);force=-dot([ps+li for ps,li in zip(psi,L)],nu)
close('phase_changing_reaction_retains_source_offset',force,aff-offset*nu[-1],1e-15)
record('phase_changing_bare_affinity_is_not_substituted',int(abs(force-aff)<1e-10),0.)
Krxn=.3;rr=Krxn*force/theta
close('reaction_entropy_production',force*rr/theta,rr*rr/Krxn,1e-15)
# Reduced source mobility including cross coefficients; a symmetric positive definite 2x2 block.
D=[[2.,.3],[.3,1.]];dforce=[.7,-.2];j=[-x for x in mv(D,dforce)];jref=-sum(j)
close('component_flux_zero_sum',sum(j)+jref,0.,1e-15)
record('relative_transport_nonnegative',max(0.,dot(j,dforce)),0.)
# Full source conversion-corrected flux inversion and no-conversion limit.
phi=.25;rhof=260.;visc=.001;kappa=[[2e-12,0.,0.],[0.,1e-12,0.],[0.,0.,.5e-12]];conversion=-30.
resistance=add(scale(inv(kappa),phi*phi*visc),scale(ident(),conversion))
body=[.0,-9.81,.0];gradp=[2e4,-1e4,3e3]
rhs=[rhof*g-phi*p+conversion*(gt-v) for g,p,gt,v in zip(body,gradp,gradtau,vs)]
ww=mv(inv(resistance),[rhof*x for x in rhs])
record('reacting_flux_inverts_source_phase_momentum',max(abs(a-b) for a,b in zip(mv(resistance,ww),[rhof*x for x in rhs]))/max(abs(rhof*x) for x in rhs),1e-13)
record('positive_resistance_domain',max(0.,-(phi*phi*visc/2e-12+conversion)),0.)
drag=[-phi*phi*visc*x for x in mv(inv(kappa),rel)]
record('drag_heating_nonnegative',max(0.,dot(drag,rel)),0.)
lam0=inv(scale(inv(kappa),phi*phi*visc));w0=mv(lam0,[rhof*(rhof*g-phi*p) for g,p in zip(body,gradp)])
darcy=mv(scale(kappa,1/visc),[rhof/phi*g-p for g,p in zip(body,gradp)])
record('conversion_free_source_darcy_limit',max(abs(phi*a/rhof-b) for a,b in zip(w0,darcy)),1e-14)
# Mixture insertion force cancels global gradtau but retains relative momentum.
csol=[10.,12.,8.];cf=-sum(csol)
full=[sum(c*(gt-v) for c,v in zip(csol+[cf],[vs[i]]*3+[vf[i]])) for i,gt in enumerate(gradtau)]
record('overall_insertion_force_cancellation',max(abs(a+cf*b) for a,b in zip(full,rel)),1e-15)
# Maxwell pressure bookkeeping for identical constant permittivity.
eps=.04;E=[.2,-.1,.3];omega=-eps*dot(E,E)/2;p=1.2;pE=p-omega;phases=[.5,.15,.1];Bbars=[.8,.85,.9]
Bp=1-sum(ph*(1-b) for ph,b in zip(phases,Bbars))
sp=2.;sdouble=sp-sum(ph*(1-b)*pE for ph,b in zip(phases,Bbars))
close('electrical_pressure_stress_bookkeeping',sdouble-Bp*pE,sp-p+omega,1e-15)

# Units in (kg,m,s,mol,K) exponent vectors.
kg=(1,0,0,0,0);rate=(0,-3,-1,1,0);nuunit=(1,0,0,-1,0);density=(1,-3,0,0,0);tau=(0,2,-1,0,0)
def umul(a,b):return tuple(x+y for x,y in zip(a,b))
production=umul(rate,nuunit);velocity=(0,1,-1,0,0);forcevol=(1,-2,-2,0,0)
record('mass_source_dimensions',int(production!=(1,-3,-1,0,0)),0.)
record('insertion_force_dimensions',int(umul(production,velocity)!=forcevol),0.)
record('tau_gradient_velocity_dimensions',int(umul(tau,(0,-1,0,0,0))!=velocity),0.)
record('chemical_stoichiometric_force_dimensions',int(umul((0,2,-2,0,0),nuunit)!=(1,2,-2,-1,0)),0.)

# Source contract and map integrity; does NOT substitute for scientific source-fidelity review.
manifest=json.loads((ROOT/'paper/source-lineage.json').read_text())
source_changed=[row['snapshot_path'] for row in manifest['sources'] if sha(ROOT/row['snapshot_path'])!=row['sha256']]
original_status={row['path']:('matching' if sha(Path(row['path']))==row['sha256'] else 'changed-since-snapshot') if Path(row['path']).exists() else 'not-available-in-this-environment' for row in manifest['sources']}
record('inspected_source_bytes_unchanged',len(source_changed),category='source-document-integrity',details=source_changed)
parent_defs=next(row for row in manifest['sources'] if row['source']=='C' and row['relative_path']=='defs.tex')
record('parent_macros_preserved_byte_for_byte',int(sha(ROOT/'paper/defs.tex')!=parent_defs['sha256']),category='source-document-integrity')
import re
tex=(ROOT/'paper/main.tex').read_text();labels=re.findall(r'\\label\{(eq:[^}]+)\}',tex)
mapping=json.loads((ROOT/'verification/equation-map.json').read_text())['equations']
record('complete_equation_correspondence',len(set(labels)^{r['label'] for r in mapping})+abs(len(labels)-len(mapping)),category='source-document-integrity',details={'equation_labels':len(labels)})
input_files=['paper/main.tex','paper/defs.tex','paper/references.bib','paper/source-lineage.json','paper/source-correspondence.md','verification/check_theory.py','verification/build_equation_map.py','verification/equation-map.json','verification/source-equation-excerpts.json']+[row['snapshot_path'] for row in manifest['sources']]
report={'category':'synthetic-source-specialization-consistency-not-PDE-verification','original_source_current_status':original_status,'command':'python3 verification/check_theory.py','python':platform.python_version(),'historical_rejected_checks_credited':0,'checks':checks,'summary':{'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'total':len(checks)},'inputs':{p:sha(ROOT/p) for p in input_files},'categories':{'source_fidelity':'equation map and byte identity checked; independent mathematical audit pending','constitutive_and_balance_consistency':'passed' if all(c['passed'] for c in checks) else 'failed','continuum_simulation':'not_performed','convergence':'not_performed','physical_validation':'not_performed','independent_acceptance':'pending'}}
(ROOT/'verification/analytical_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['summary']))
for c in checks:
 if not c['passed']:print('FAILED',c['name'],c['error'],'>',c['tolerance'])
sys.exit(bool(report['summary']['failed']))
