"""Startup guard rejects changed source and changed shared libraries."""
import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('prebuilt',Path(__file__).resolve().parents[1]/'prebuilt_app.py')
prebuilt=importlib.util.module_from_spec(spec); spec.loader.exec_module(prebuilt)
class GuardTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
  base=Path(self.temp.name); self.image=base/'image'; self.workspace=base/'workspace'
  for root in (self.image,self.workspace):
   (root/'moose_app/src').mkdir(parents=True); (root/'moose_app/include').mkdir()
   (root/'moose_app/Makefile').write_text('build rules\n')
   (root/'moose_app/src/a.C').write_text('source\n')
   (root/'moose_app/include/a.h').write_text('header\n')
   (root/'environment').mkdir(); (root/'environment/moose-linux-64.lock').write_text('locked toolchain\n')
  (self.image/'moose_app/lib').mkdir(); (self.image/'moose_app/lib/libapp.so').write_bytes(b'library')
  (self.image/'moose_app/test/lib').mkdir(parents=True); (self.image/'moose_app/test/lib/libtest.so').write_bytes(b'test library')
  (self.image/'moose_app/olivine_carbonation-opt').write_bytes(b'executable')
  prebuilt.BASE_LOCK=self.image/'environment/moose-linux-64.lock'
  prebuilt.ROOT=self.image; prebuilt.record('a'*40,'ghcr.io/example/base@sha256:'+'b'*64)
  prebuilt.ROOT=self.workspace
 def test_matching_source_reuses_image_binary(self):
  self.assertTrue(prebuilt.reuse(self.image)); self.assertTrue((self.workspace/'moose_app/olivine_carbonation-opt').is_symlink())
 def test_changed_header_rejects_binary(self):
  (self.workspace/'moose_app/include/a.h').write_text('different header\n')
  self.assertFalse(prebuilt.reuse(self.image)); self.assertFalse((self.workspace/'moose_app/olivine_carbonation-opt').exists())
 def test_new_source_rejects_binary(self):
  (self.workspace/'moose_app/src/new.C').write_text('new object\n')
  self.assertFalse(prebuilt.reuse(self.image))
 def test_changed_toolchain_rejects_old_image(self):
  (self.workspace/'environment/moose-linux-64.lock').write_text('new toolchain\n')
  with self.assertRaises(RuntimeError): prebuilt.reuse(self.image)
 def test_changed_shared_library_rejects_binary(self):
  (self.image/'moose_app/lib/libapp.so').write_bytes(b'corrupt library')
  self.assertFalse(prebuilt.reuse(self.image))
 def test_changed_test_library_rejects_binary(self):
  (self.image/'moose_app/test/lib/libtest.so').write_bytes(b'corrupt test library')
  self.assertFalse(prebuilt.reuse(self.image))
if __name__=='__main__': unittest.main()
