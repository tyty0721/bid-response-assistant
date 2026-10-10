import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package', ROOT / 'tooling/package.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def test_archive_is_reproducible_and_omits_private_materials(self):
        temp_root = ROOT / 'work/tests'
        temp_root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as temp:
            files = package.delivery_files()
            for file in files:
                self.assertFalse(any(p in file.relative_to(ROOT).parts for p in ('node_modules','sources','intake','private-materials')))
            a,b = Path(temp)/'a.zip',Path(temp)/'b.zip'
            package.build_archive(a,files,'delivery/')
            package.build_archive(b,files,'delivery/')
            self.assertEqual(a.read_bytes(),b.read_bytes())
            with zipfile.ZipFile(a) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('delivery/skills/bid-response-assistant/SKILL.md',archive.namelist())


if __name__ == '__main__':
    unittest.main()
