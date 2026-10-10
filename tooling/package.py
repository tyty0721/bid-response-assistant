"""Build reproducible archives and hashes; never include private inputs or runtime links."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ROOTS = {'skills', 'tests', 'examples', 'docs', 'tooling'}
TOP_FILES = {'README.md','LICENSE','THIRD_PARTY_NOTICES.md','requirements.txt','.gitignore'}


def delivery_files():
    files = []
    for root_name in sorted(ALLOWED_ROOTS):
        for path in sorted((ROOT / root_name).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and not path.name.endswith(('.pyc','.inspect.ndjson')):
                if path.is_symlink() or any(part in {'sources','intake','provenance'} for part in path.relative_to(ROOT).parts):
                    continue
                files.append(path)
    files += [ROOT / name for name in sorted(TOP_FILES)]
    return sorted(files)


def build_archive(target, files, prefix, base=ROOT):
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(prefix + path.relative_to(base).as_posix(), (2026,10,10,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('Archive CRC failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    files = delivery_files()
    manifest = {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out / 'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    build_archive(out / 'bid-response-assistant-delivery-v0.1.0.zip', files, 'bid-response-assistant-delivery/')
    skill_files = [p for p in files if p.relative_to(ROOT).parts[0] == 'skills']
    # Install ZIP has exactly one skill folder at archive root.
    build_archive(out / 'bid-response-assistant-skill-v0.1.0.zip', skill_files, '', ROOT / 'skills')
    hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}
    (out / 'SHA256SUMS.txt').write_text('\n'.join(f'{sha}  {name}' for name,sha in sorted(hashes.items()))+'\n',encoding='utf-8')
    print(json.dumps({'files':len(files),'archives':2,'output':str(out)},ensure_ascii=False))
