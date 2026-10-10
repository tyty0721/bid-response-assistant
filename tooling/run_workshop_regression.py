"""Replay selected source anchors and checks. This is NOT model extraction accuracy."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/bid-response-assistant/scripts'))
import bid
import ingest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--materials', required=True)
parser.add_argument('--workspace', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
workspace, output = Path(args.workspace), Path(args.output)
ingest.ingest(args.materials, workspace)
manifest = bid.load(workspace / 'manifest.json')
blocks = bid.load(workspace / 'source_blocks.json')
main = next(s for s in manifest['sources'] if s['path'].endswith('.pdf') and 'N5100012026002044' in s['path'])
pages = {b['page']: b for b in blocks if b['source_id'] == main['id']}
gold = bid.load(ROOT / 'tests/gold/workshop-key-clauses.json')
expected = gold['expected']
requirements, responses = [], []
for item in gold['clauses']:
    block = pages[item['page']]
    match = re.search(item['pattern'], block['normalized'])
    if not match:
        raise AssertionError(f'Expected anchor missing on page {item["page"]}: {item["id"]}')
    requirement = {'id': item['id'], 'text': item['text'], 'kind': item['kind'],
                   'mandatory': item['kind'] != 'scoring', 'phase': 'contract_performance' if item['kind'] == 'contract' else 'response_preparation',
                   'response_required_now': item['proof'] != 'none', 'proof_type': item['proof'],
                   'sources': [{'source_id': main['id'], 'block_id': block['id'], 'quote': match.group()}]}
    requirements.append(requirement)
    if item['proof'] != 'none':
        responses.append({'requirement_id': item['id'], 'text': None,
                          'status': 'needs_confirmation' if item['proof'] == 'promise' else 'missing_evidence', 'evidence_ids': []})
record = {'schema_version': 1, 'project': {'id': gold['project_id'], 'name': 'AI赋能铁道移动通信课程建设及智能体开发与应用课程资源建设(二次)',
          'package': '1', 'version': gold['version'], 'method': 'competitive_consultation', 'category': 'services',
          'jurisdiction': 'CN-government-procurement', 'company': None, 'deadline': None,
          'rules': {k: v for k, v in expected.items() if k not in {'deadline','company','quote','state'}},
          'sources': [{'source_id':main['id'], 'block_id':pages[2]['id'], 'quote':'N5100012026002044'}]},
          'procurement_source_ids':[main['id']],
          'reviewed_blocks': [pages[p]['id'] for p in sorted({2,3,5,6,15,23,24,27,28,30,33,34,35,36,42})],
          'requirements':requirements, 'responses':responses, 'evidence':[], 'quote':None, 'approval':None,
          'conflicts':[{'description':'p24达到付款条件后30个工作日与p42满足条件收到发票后10个工作日的起算和期限需澄清',
                        'sources':[{'source_id':main['id'],'block_id':pages[42]['id'],'quote':'10\n个工作日'}], 'resolution':None}],
          'analysis_scope':'selected_key_clause_regression_not_full_requirement_extraction'}
checks = bid.check(record, workspace, date(2026, 10, 10))
assert checks['state'] == expected['state']
assert not any(i['code'] in {'CITATION_INVALID','CITATION_QUOTE','SOURCE_CHANGED','CORPUS_CHANGED'} for i in checks['issues'])
output.mkdir(parents=True, exist_ok=False)
bid.save(output / 'record.json', record)
bid.export(record, checks, output / 'draft')
# Publish metadata, not the raw customer package or full corpus.
bid.save(output / 'materials-manifest.json', manifest)
bid.save(output / 'regression-result.json', {'scope':gold['scope'], 'sources':len(manifest['sources']),
          'pdf_pages':sum(1 for b in blocks if 'page' in b), 'anchors_checked':len(requirements),
          'citation_errors':0, 'state':checks['state'], 'issues':len(checks['issues']),
          'complete_semantic_extraction':False, 'business_acceptance':False, 'submission':'not_performed'})
print(json.dumps(bid.load(output / 'regression-result.json'), ensure_ascii=False))
