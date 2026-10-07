#!/usr/bin/env python3
"""Allowlisted self-contained companion site, patterned after the finite-strain Biot companion."""
import argparse, hashlib, html, json, re, shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/'.agent-runtime/site'
class Links(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.links=[]; self.ids=set(); self.feed(text)
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if 'id' in attrs: self.ids.add(attrs['id'])
  self.links.extend(attrs[a] for a in ('href','src') if a in attrs)
def published_path(path):
 # upload-pages-artifact excludes every .github directory, including raw code.
 path=Path(path)
 return Path('github',*path.parts[1:]) if path.parts[0]=='.github' else path
def source_link(path,label=None):
 path=Path(path); return f'<a href="sources/{published_path(path).as_posix()}.html">{html.escape(label or str(path))}</a>'
def input_objects(deck,seen=None):
 seen=set() if seen is None else seen
 if deck in seen: return set()
 seen.add(deck); text=deck.read_text()
 names=set(re.findall(r'^\s*type\s*(?::=|=)\s*(\w+)',text,re.M))
 for include in re.findall(r'^\s*!include\s+([^\s#]+)',text,re.M):
  parent=(deck.parent/include).resolve()
  if not parent.is_relative_to(ROOT): raise ValueError('External input include rejected')
  names.update(input_objects(parent,seen))
 return names
ROLES={
 'ADReferenceMassStorage':'Difference complete reference mass with backward Euler or variable-step BDF2.',
 'ADReferenceSpeciesBalance':'Assemble a component flux and reference reaction source; omit flux for pure solids.',
 'ADCarbonationMomentum':'Assemble nominal stress, gravity and fluid-production momentum in the solid reference.',
 'ADTransferPotential':'Advance the parent transfer-work field using the skeleton velocity.',
 'ADReferenceGauss':'Assemble electrostatics with the pulled-back dielectric and reference charge.',
 'ADReferenceOutwardFlux':'Apply prescribed outward reference mass flux or electric displacement.',
 'ADReferenceTraction':'Apply prescribed outward nominal traction.',
 'ADReferenceMass':'Form the conservative storage J phi rho-bar eta, including historical states.',
 'ADReferencePullback':'Pull current species flux, production, charge and dielectric into the solid reference.',
 'ADLogarithmicMinerals':'Solve each mineral volume by Newton in AD and assemble density, stress and the aggregate Biot coefficient.',
 'ADOlivineReconstruction':'Reconstruct a scalar from its continuous backbone and optional constant enrichment.',
 'ADSolidReferenceKinematics':'Compute finite-deformation kinematics on the undisplaced reference mesh.',
 'ADSkeletonVelocity':'Obtain skeleton velocity from the displacement time derivative.',
 'ADScalarDiffusionReferenceFluxMaterial':'Supply scalar diffusion properties for manufactured verification reductions.',
 'ADCrossDiffusionVerification':'Supply a synthetic SPD two-species mobility block for cross-diffusion verification.',
 'ADEnrichedGalerkinScalarBalance':'Assemble the continuous scalar volume row.',
 'ADEnrichedGalerkinScalarEnrichmentBalance':'Assemble the constant enrichment storage and source row.',
 'ADEnrichedGalerkinFluxDG':'Assemble conservative diagonal interior flux and penalty terms.',
 'ADEnrichedGalerkinSymmetryDG':'Assemble diagonal adjoint-consistency terms on interior faces.',
 'ADEnrichedGalerkinCrossFluxDG':'Assemble off-diagonal interior flux and penalty terms.',
 'ADEnrichedGalerkinCrossSymmetryDG':'Assemble off-diagonal adjoint-consistency terms on interior faces.',
 'ADEnrichedGalerkinPenaltyBC':'Apply weak diagonal Dirichlet data to the enrichment field.',
 'ADEnrichedGalerkinCrossPenaltyBC':'Apply weak off-diagonal Dirichlet coupling to the enrichment field.',
 'ADEnrichedGalerkinBoundaryFluxIntegral':'Measure the assembled outward numerical boundary flux.'
}
def page(title,body):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · Olivine carbonation</title><link rel="stylesheet" href="assets/style.css"></head><body><header><div class="container"><a class="brand" href="index.html">Olivine carbonation<span class="tag">Compositional finite-deformation theory · MOOSE residuals</span></a><nav><a href="index.html">Home</a><a href="model.html">Model</a><a href="kernels.html">MOOSE catalog</a><a href="verification.html">Verification</a><a href="reproduction.html">Reproduce</a></nav></div></header>{body}<footer><div class="container">John T. Foster · Code: Apache-2.0 · Manuscript: CC BY 4.0 · <a href="https://github.com/johntfoster/olivine-carbonation-theory">Repository</a></div></footer></body></html>'''
def check(output):
 count=0
 parsed_pages={p.resolve():Links(p.read_text()) for p in output.rglob('*.html')}
 for file,document in parsed_pages.items():
  for link in document.links:
   parsed=urlsplit(link)
   if parsed.scheme or parsed.netloc: continue
   target=(file.parent/unquote(parsed.path)).resolve() if parsed.path else file.resolve()
   if not target.is_relative_to(output.resolve()) or not target.is_file(): raise ValueError(f'Broken link {file}: {link}')
   if parsed.fragment and target.suffix=='.html' and unquote(parsed.fragment) not in parsed_pages[target].ids: raise ValueError(f'Broken anchor {link}')
   count+=1
 manifest=json.loads((output/'source-manifest.json').read_text())
 for path,digest in manifest.items():
  if hashlib.sha256((output/'raw'/published_path(path)).read_bytes()).hexdigest()!=digest: raise ValueError(f'Incorrect packaged bytes: {path}')
 return count
def build(output):
 if output.exists(): shutil.rmtree(output)
 output.mkdir(parents=True); shutil.copytree(ROOT/'site/assets',output/'assets'); (output/'.nojekyll').touch()
 allow=[]
 for directory,patterns in [('moose_app/src',['*.C']),('moose_app/include',['*.h']),('moose_app/test/tests',['*.i','tests']),('scripts',['*.py']),('.devcontainer',['Dockerfile*','*.json','*.sh']),('.github/workflows',['*.yml']),('environment',['*.json','*.md']),('verification',['implementation-map.md','implementation-results.json','environment-results.json','eg-source-lineage.json','mineral-source-lineage.json'])]:
  for pattern in patterns: allow.extend((ROOT/directory).rglob(pattern))
 allow.extend(ROOT/p for p in ['PLAN.md','GOAL.md','research-project.yml','paper/main.tex','paper/defs.tex','paper/references.bib','moose_app/Makefile','moose_app/run_tests','docs/implementation-status.md'])
 manifest={}
 for p in sorted(set(allow)):
  if not p.is_file(): continue
  rel=p.relative_to(ROOT)
  if not p.resolve().is_relative_to(ROOT): raise ValueError('External source rejected')
  public=published_path(rel)
  raw=output/'raw'/public; raw.parent.mkdir(parents=True,exist_ok=True); raw.write_bytes(p.read_bytes()); manifest[str(rel)]=hashlib.sha256(p.read_bytes()).hexdigest()
  dest=output/'sources'/(str(public)+'.html'); dest.parent.mkdir(parents=True,exist_ok=True)
  prefix='../'*len(dest.relative_to(output).parts[:-1])
  lines='\n'.join(f'<span class="source-line" id="L{i}"><a class="line-number" href="#L{i}">{i}</a>{html.escape(line)}</span>' for i,line in enumerate(p.read_text().splitlines(),1))
  dest.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(str(rel))}</title><link rel="stylesheet" href="{prefix}assets/style.css"></head><body><main class="container"><p><a href="{prefix}kernels.html">← Object catalog</a> · <a href="{prefix}raw/{public}">Raw source</a></p><h2>{html.escape(str(rel))}</h2><p>SHA-256: <code>{manifest[str(rel)]}</code></p><pre><code>{lines}</code></pre></main></body></html>')
 (output/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 objects={name:p for p in (ROOT/'moose_app/src').rglob('*.C') for name in re.findall(r'registerMooseObject\(\s*"OlivineCarbonationApp",\s*(\w+)\)',p.read_text())}
 catalog=['<main class="container"><h1>MOOSE object catalog</h1><p>Every local registered object links to the exact packaged source bytes. Constitutive and residual responsibilities follow the '+source_link('verification/implementation-map.md','equation contract')+'.</p><div class="grid">']
 for name,p in sorted(objects.items()):
  rel=p.relative_to(ROOT); head=Path('moose_app/include')/rel.relative_to('moose_app/src').with_suffix('.h')
  inputs=[deck for deck in sorted((ROOT/'moose_app/test/tests').rglob('*.i')) if name in input_objects(deck)]
  tests=' · '.join(source_link(deck.relative_to(ROOT),deck.name) for deck in inputs[:3])
  display_name=re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])','<wbr>',html.escape(name))
  catalog.append(f'<article class="card"><h3>{display_name}</h3><p>{html.escape(ROLES[name])}</p><p>{source_link(rel,"Implementation")} · {source_link(head,"Header")}</p><p>Verification inputs: {tests or "See the equation contract"}</p></article>')
 catalog.append('</div><h2>Inputs and test specifications</h2><ul>')
 for deck in sorted((ROOT/'moose_app/test/tests').rglob('*.i')):
  names=input_objects(deck); selected=[source_link(objects[n].relative_to(ROOT),n) for n in sorted(names) if n in objects]
  spec=deck.parent/'tests'
  if spec.exists(): selected.append(source_link(spec.relative_to(ROOT),'Test specification'))
  catalog.append('<li>'+source_link(deck.relative_to(ROOT))+'<br>'+' · '.join(selected)+'</li>')
 catalog.append('</ul></main>')
 (output/'kernels.html').write_text(page('MOOSE catalog',''.join(catalog)))
 (output/'index.html').write_text(page('Home','''<section class="hero"><div class="container"><h1>Elastic deformation, aqueous transport and mineral conversion</h1><p class="lead">Mg₂SiO₄ + 2 CO₂ → 2 MgCO₃ + SiO₂. Three compressible elastic minerals and one aqueous phase, specialized from the author's compositional reacting-mixture theory.</p><div class="cta"><a class="btn primary" href="kernels.html">Inspect the kernels</a><a class="btn" href="reproduction.html">Run the tests</a><a class="btn" href="https://codespaces.new/johntfoster/olivine-carbonation-theory">Launch Codespace</a></div></div></section><main class="container"><section class="section"><h2>From equations to residuals</h2><div class="grid"><article class="card"><h3>Conservative reference mass</h3><p>Difference the complete mass J φ ρ̄ η. Assembly retains derivatives of deformation, phase fraction, density and composition.</p></article><article class="card"><h3>Reference mechanics</h3><p>Nominal stress, gravity and material-insertion momentum use the same solid reference configuration as mass storage.</p></article><article class="card"><h3>Enriched Galerkin</h3><p>Continuous and cellwise constant fields share volume equations. Interior numerical fluxes provide opposite cell-face contributions.</p></article></div></section><p class="status">Numerical verification and deployment evidence are reported on the verification page. Material calibration and experimental validation remain open. A Codespaces launch link does not certify hosted startup.</p></main>'''))
 (output/'model.html').write_text(page('Model','<main class="container"><h1>The compositional special case</h1><p>The phases are forsterite A, magnesite B, silica C and aqueous f. The nine aqueous species share one phase; water is the dependent mass fraction. The three-dimensional quasi-static system has 17 scalar fields.</p><p>The source contract controls transfer-work normalization and all phase and component measures. Kernels consume constitutive AD properties. The logarithmic mineral material solves the positive-tangent density branch and recovers nominal stress. Reaction/flow closures must supply a consistently solved constitutive block; passing residual tests does not establish its global uniqueness.</p><ul><li>'+source_link('paper/main.tex','Manuscript source and labeled equations')+'</li><li>'+source_link('verification/implementation-map.md','Residual/material contract')+'</li><li>'+source_link('verification/eg-source-lineage.json','EG source attribution')+'</li></ul><p>Plasticity, a separate gas phase, phase nucleation and phase disappearance are outside the implemented positive-mass branch.</p></main>'))
 results=ROOT/'verification/implementation-results.json'
 if results.exists():
  report=json.loads(results.read_text()); checks=report.get('checks',[])
  evidence=f"<p><strong>{html.escape(report.get('status','pending').upper())}</strong> · {len(checks)} executable checks</p><table><thead><tr><th>Check</th><th>Error / tolerance</th><th>Result</th></tr></thead><tbody>"
  for item in checks:
   evidence+=f"<tr><td>{html.escape(item['name'])}</td><td>{item['error']:.3g} / {item['tolerance']:.3g}</td><td>{'Pass' if item['passed'] else 'Fail'}</td></tr>"
  evidence+='</tbody></table><h2>Observed convergence</h2><table><thead><tr><th>Reduction</th><th>Errors</th><th>Orders</th></tr></thead><tbody>'
  for item in checks:
   if 'observed_orders' in item:
    evidence+=f"<tr><td>{html.escape(item['name'])}</td><td>{', '.join(f'{v:.4g}' for v in item.get('l2_errors',item.get('mass_errors',[])))}</td><td>{', '.join(f'{v:.3f}' for v in item['observed_orders'])}</td></tr>"
  evidence+='</tbody></table><p>'+source_link('verification/implementation-results.json','Complete hash-bound evidence and commands')+'</p>'
 else: evidence='<p>Numerical evidence pending.</p>'
 (output/'verification.html').write_text(page('Verification','<main class="container"><h1>Recorded verification</h1><p>Assembly tests, analytical identities, discretization convergence and physical validation are distinct gates. Test parameters are synthetic.</p><p>'+source_link('docs/implementation-status.md','Current status')+'</p>'+evidence+'<p>Physical validation has not been performed.</p></main>'))
 (output/'reproduction.html').write_text(page('Reproduce','''<main class="container"><h1>Reproduce and inspect</h1><pre>git clone --recurse-submodules https://github.com/johntfoster/olivine-carbonation-theory.git
cd olivine-carbonation-theory
tools/setup-agent-workflows
make check
make moose
make test
make site</pre><p>Use the devcontainer for the pinned compiled MOOSE framework and scientific Python. Startup checks source hashes before reusing the prebuilt application. Edited source triggers a rebuild. Manuscript compilation remains explicit with <code>make paper</code>.</p><h2>Two image layers</h2><p>The manually dispatched base-image workflow builds the numerical toolchain once. Each push builds and tests an application image for that exact Git revision, then publishes its SHA tag to GitHub Container Registry. The base digest and compiled-source hashes are recorded in image provenance.</p><p>Hosted Codespaces prebuilds are configured in repository settings and are separate from GHCR publishing.</p><ul><li>'''+source_link('.devcontainer/Dockerfile.base','Base Dockerfile')+'</li><li>'+source_link('.devcontainer/Dockerfile','Application Dockerfile')+'</li><li>'+source_link('environment/README.md','Toolchain and startup instructions')+'</li><li>'+source_link('verification/environment-results.json','Recorded container and hosted-startup evidence')+'</li><li><a href="https://github.com/johntfoster/olivine-carbonation-theory/actions">GitHub Actions</a></li></ul></main>'))
 return {'objects':len(objects),'sources':len(manifest),'checked_links':check(output)}
if __name__=='__main__':
 parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=DEFAULT); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
 print(json.dumps({'checked_links':check(args.output)} if args.check else build(args.output),indent=2))
