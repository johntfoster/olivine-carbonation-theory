#!/usr/bin/env python3
"""Hash-guard reuse of an image's binary; never reuse it for different source bytes."""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sources(root):
 files=[root/'moose_app/Makefile']
 for surface,glob in [('src','*.C'),('include','*.h')]: files.extend((root/'moose_app'/surface).rglob(glob))
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
def artifacts(root):
 files=[root/'moose_app/olivine_carbonation-opt']
 files.extend(p for p in (root/'moose_app/lib').rglob('*.so*') if p.is_file() and not p.is_symlink())
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
def record(revision,base_image):
 binary=ROOT/'moose_app/olivine_carbonation-opt'
 if not binary.is_file(): raise RuntimeError('Compiled application absent')
 data={'source_revision':revision,'base_image':base_image,'source_hashes':sources(ROOT),'executable_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'artifact_hashes':artifacts(ROOT),'architecture':'linux/amd64'}
 (ROOT/'prebuilt-application.json').write_text(json.dumps(data,indent=2)+'\n')
def reuse(image):
 metadata=image/'prebuilt-application.json'
 if not metadata.is_file(): return False
 data=json.loads(metadata.read_text()); binary=image/'moose_app/olivine_carbonation-opt'
 if data['source_hashes']!=sources(ROOT) or data['artifact_hashes']!=artifacts(image): return False
 target=ROOT/'moose_app/olivine_carbonation-opt'
 if target.is_symlink(): target.unlink()
 if target.exists(): return False # Preserve a workspace build.
 target.symlink_to(binary)
 print('Reusing source-matched application from revision '+data['source_revision'])
 return True
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('command',choices=['record','startup']); p.add_argument('--revision'); p.add_argument('--base-image'); args=p.parse_args()
 if args.command=='record':
  if not args.revision or not args.base_image or '@sha256:' not in args.base_image: p.error('Record requires exact revision and digest-pinned base image')
  record(args.revision,args.base_image)
 else:
  image=Path(os.environ.get('OLIVINE_IMAGE_ROOT','/opt/olivine'))
  if not reuse(image):
   target=ROOT/'moose_app/olivine_carbonation-opt'
   if target.is_symlink(): target.unlink()
   subprocess.run(['with-moose','make','-C',str(ROOT/'moose_app'),'-j2'],check=True)
