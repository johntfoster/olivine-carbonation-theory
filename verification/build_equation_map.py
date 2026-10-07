#!/usr/bin/env python3
"""Build literal equation-to-parent map from explicit authoring provenance tags."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'paper/source-lineage.json').read_text())
sourcefiles={}
for row in manifest['sources']:
 sourcefiles.setdefault(row['source'],[]).append(row)
tex=(root/'paper/main.tex').read_text()
records=[]; excerpts={}
for match in re.finditer(r'% provenance: ([^\n]+)\n\\begin\{(equation|align)\}(.*?)\\end\{\2\}',tex,re.S):
 kind,refs=match[1].split('|',1)
 labels=re.findall(r'\\label\{(eq:[^}]+)\}',match[3])
 mapped=[]
 for ref in refs.strip().split(','):
  sid,label=ref.split(':',1);hits=[]
  for row in sourcefiles[sid]:
   p=root/row['snapshot_path'];content=p.read_text()
   loc=content.find('\\label{'+label+'}')
   if loc>=0:
    # Include local equation and explanatory context; immutable digest gives full-file authority.
    lines=content.splitlines();ln=content[:loc].count('\n')+1
    start=max(0,ln-45);end=min(len(lines),ln+12)
    hit={'source':sid,'label':label,'path':row['snapshot_path'],'original_path':row['path'],'line':ln,'sha256':row['sha256']}
    hits.append(hit);excerpts[ref]={**hit,'excerpt_start_line':start+1,'excerpt':'\n'.join(lines[start:end])}
  if len(hits)!=1:raise RuntimeError(f'{ref}: expected one exact label, found {len(hits)}')
  mapped.append(hits[0])
 for label in labels:
  records.append({'label':label,'classification':kind.strip(),'line':tex[:match.start()].count('\n')+1,'parents':mapped})
labels=re.findall(r'\\label\{(eq:[^}]+)\}',tex)
if set(labels)!={r['label'] for r in records} or len(labels)!=len(records):raise RuntimeError('Missing or duplicate provenance')
payload={'status':'unreviewed-source-specialization','governing_parent':'C: compositional manuscript; other sources are constitutive/historical only','equations':records}
(root/'verification/equation-map.json').write_text(json.dumps(payload,indent=2)+'\n')
(root/'verification/source-equation-excerpts.json').write_text(json.dumps(excerpts,indent=2)+'\n')
md='# Equation correspondence: compositional parent → restricted application\n\nThe classification is explicit: inherited, specialization, derived, or application. Application entries are constitutive/data choices admitted by the identified parent state/restriction; they are not claimed to be verbatim equations of the parent. Exact source file/line/digest and literal context are in `verification/equation-map.json` and `verification/source-equation-excerpts.json`. All citations resolve against the working-tree manifest in `paper/source-lineage.json`.\n\n| Candidate label | Type | Parent equation labels |\n|---|---|---|\n'
for r in records:
 md+='| `'+r['label']+'` | '+r['classification']+' | '+', '.join('`'+p['source']+':'+p['label']+'`' for p in r['parents'])+' |\n'
md+='\n## Restrictions\n\nC phase sets become S={A,B,C}, F={f}; pure solid components, one aqueous phase; common constant temperature; identity plastic and stress-free maps; scalar distention. S_f=1 and γ=0 remove interfluid capillarity/history/saturation processes. Charged aqueous components retain source electrical enthalpy, specific charge, electrochemical transport and Gauss law. C mass and charge sources, material increments, τ/L normalization, insertion force, resistance shift, pressure/volume multipliers, scalar distention restriction and Biot transforms remain. The common-permittivity and additive matched-log/ideal-mixture free energies are declared application constitutive choices. No other paper supplies a competing τ or mass/transport law.\n'
(root/'paper/source-correspondence.md').write_text(md)
print(f'{len(records)} candidate equation labels mapped; {len(excerpts)} literal source contexts')
