"""Emit an allowlisted delivery file to the orchestration tool, not credentials."""
import argparse
import base64
import json
from pathlib import Path
from package import ROOT, delivery_files

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--index',type=int)
parser.add_argument('--offset',type=int,default=0)
parser.add_argument('--limit',type=int)
parser.add_argument('--prepare',action='store_true')
parser.add_argument('--payload-offset',type=int)
args = parser.parse_args()
files = delivery_files() + sorted((ROOT/'releases/v0.1.0').glob('*'))
def payload(p):
    binary = p.suffix in {'.zip','.docx','.xlsx','.png'}
    data = p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob',
            'encoding':'base64' if binary else 'utf-8',
            'content':base64.b64encode(data).decode() if binary else data.decode('utf-8')}

if args.prepare:
    dest = ROOT/'work/upload-payload.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps([payload(p) for p in files],ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'files':len(files),'bytes':dest.stat().st_size}))
elif args.payload_offset is not None:
    if args.payload_offset < 0 or args.limit is None or args.limit <= 0:
        parser.error('payload offset requires a positive limit')
    data = (ROOT/'work/upload-payload.json').read_bytes()
    print(json.dumps({'total_bytes':len(data),'chunk_base64':base64.b64encode(data[args.payload_offset:args.payload_offset+args.limit]).decode()}))
elif args.index is None:
    print(json.dumps([{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,
                       'binary':p.suffix in {'.zip','.docx','.xlsx','.png'}} for p in files],ensure_ascii=False))
else:
    p = files[args.index]
    binary = p.suffix in {'.zip','.docx','.xlsx','.png'}
    data = p.read_bytes()
    if args.offset < 0 or (args.limit is not None and args.limit <= 0):
        parser.error('offset must be nonnegative and limit must be positive')
    if args.limit is not None:
        # Base64 chunks avoid accidental shell interpretation and console encoding changes.
        data = data[args.offset:args.offset+args.limit]
        print(json.dumps({'path':p.relative_to(ROOT).as_posix(),'chunk_base64':base64.b64encode(data).decode()}))
    else:
        print(json.dumps(payload(p),ensure_ascii=True))
