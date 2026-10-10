"""Save the actual unittest result as machine-readable evidence."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', required=True)
args = parser.parse_args()
output = Path(args.output)
output.mkdir(parents=True, exist_ok=False)
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
(output / 'unittest.log').write_text(stream.getvalue(), encoding='utf-8')
import pypdf, docx
report = {'tests_run':result.testsRun, 'failures':len(result.failures), 'errors':len(result.errors),
          'skipped':len(result.skipped), 'passed':result.wasSuccessful(),
          'platform':platform.platform(), 'python':platform.python_version(),
          'dependencies':{'pypdf':pypdf.__version__, 'python-docx':docx.__version__},
          'scope':'deterministic unit/integration checks, not business UAT',
          'skill_files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (ROOT / 'skills').rglob('*') if p.is_file() and '__pycache__' not in p.parts}}
(output / 'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ('tests_run','failures','errors','passed')},ensure_ascii=False))
sys.exit(0 if result.wasSuccessful() else 1)
