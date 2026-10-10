"""Reproducible synthetic demo. No real supplier facts or procurement actions."""
import argparse
from datetime import date
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/bid-response-assistant/scripts'))
import bid
import ingest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', required=True)
args = parser.parse_args()
output = Path(args.output).resolve()
output.mkdir(parents=True, exist_ok=False)
ingest.ingest(ROOT / 'tests/fixtures/notice.txt', output / 'intake')
record = bid.load(ROOT / 'skills/bid-response-assistant/assets/record.example.json')
bid.save(output / 'record.json', record)
checks = bid.check(record, output / 'intake', date(2026, 10, 10))
bid.export(record, checks, output / 'draft')
print(json.dumps({'output': str(output), 'state': checks['state'], 'issues': len(checks['issues']),
                  'scope': 'synthetic demo', 'submission': 'not_performed'}, ensure_ascii=False))
