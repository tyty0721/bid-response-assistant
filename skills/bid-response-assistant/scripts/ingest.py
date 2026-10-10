"""Local, bounded intake. Document text is data, never executable instructions."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import unicodedata
import zipfile

MAX_FILE = 25 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_FILES = 500
ALLOWED = {'.pdf', '.docx', '.txt', '.md'}


def digest(path):
    with open(path, 'rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def normalize(text):
    return unicodedata.normalize('NFKC', text)


def safe_members(archive):
    members = archive.infolist()
    if len(members) > MAX_FILES or sum(m.file_size for m in members) > MAX_TOTAL:
        raise ValueError('Archive exceeds file count or expanded size limit')
    seen = set()
    for member in members:
        name = member.filename.replace('\\', '/')
        path = PurePosixPath(name)
        mode = member.external_attr >> 16
        if (path.is_absolute() or '..' in path.parts or ':' in name or
                stat.S_ISLNK(mode) or member.flag_bits & 1 or
                any(p.rstrip(' .').upper().split('.')[0] in
                    {'CON', 'PRN', 'AUX', 'NUL', *[f'COM{i}' for i in range(1, 10)],
                     *[f'LPT{i}' for i in range(1, 10)]} for p in path.parts)):
            raise ValueError(f'Unsafe archive entry: {name}')
        key = name.casefold().rstrip('/')
        if key in seen or any(p.endswith((' ', '.')) for p in path.parts):
            raise ValueError(f'Ambiguous archive entry: {name}')
        seen.add(key)
        if member.file_size > MAX_FILE or member.file_size > max(1, member.compress_size) * 200:
            raise ValueError(f'Archive entry exceeds expansion limit: {name}')
        if not member.is_dir() and path.suffix.lower() not in ALLOWED:
            raise ValueError(f'Unsupported archive entry (not executed): {name}')
    return members


def extract_zip(path, target):
    with zipfile.ZipFile(path) as archive:
        members = safe_members(archive)  # Validate every entry before any extraction.
        for member in members:
            dest = target / member.filename.replace('\\', '/')
            if member.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as src, open(dest, 'xb') as out:
                    shutil.copyfileobj(src, out)


def parse(path, source_id):
    suffix = path.suffix.lower()
    if suffix == '.pdf':
        from pypdf import PdfReader
        reader = PdfReader(path)
        if reader.is_encrypted:
            raise ValueError('Encrypted PDF requires an authorized decrypted copy')
        blocks = []
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ''
            blocks.append({'id': f'{source_id}:p{page_num:03}', 'page': page_num,
                           'text': text, 'normalized': normalize(text),
                           'quality': 'native' if len(text.strip()) >= 30 else 'needs_review'})
        return blocks
    if suffix == '.docx':
        # OOXML is also a ZIP trust boundary. Do not resolve external links or macros.
        with zipfile.ZipFile(path) as archive:
            if sum(m.file_size for m in archive.infolist()) > MAX_TOTAL:
                raise ValueError('OOXML expanded size exceeds limit')
            if any('vbaproject' in n.lower() for n in archive.namelist()):
                raise ValueError('Macro payload is not allowed')
        from docx import Document
        from docx.oxml.ns import qn
        document = Document(path)
        blocks = []
        for idx, element in enumerate(document.element.body, 1):
            parts = [''.join(t.itertext()) for t in element.iter(qn('w:t'))]
            text = ' '.join(parts).strip()
            if text:
                blocks.append({'id': f'{source_id}:b{idx:04}', 'block': idx, 'text': text,
                               'normalized': normalize(text), 'quality': 'native'})
        return blocks
    text = path.read_text(encoding='utf-8-sig')
    return [{'id': f'{source_id}:b0001', 'block': 1, 'text': text,
             'normalized': normalize(text), 'quality': 'native'}]


def ingest(input_path, output):
    input_path, output = Path(input_path).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError('Output exists; choose a new version directory to preserve edits')
    if input_path.is_dir() and (output == input_path or input_path in output.parents):
        raise ValueError('Output must be outside the input tree')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='bid-intake-', dir=output.parent) as temp:
        stage = Path(temp) / 'project'
        stage.mkdir()
        root = input_path
        if input_path.suffix.lower() == '.zip':
            root = Path(temp) / 'unpacked'
            root.mkdir()
            extract_zip(input_path, root)
        elif input_path.suffix.lower() == '.rar':
            raise ValueError('RAR requires trusted local extraction first; pass the extracted folder')
        files = sorted(root.rglob('*')) if root.is_dir() else [root]
        files = [p for p in files if p.is_file() or p.is_symlink()]
        if not files or len(files) > MAX_FILES:
            raise ValueError('Input is empty or exceeds file count limit')
        if sum(p.stat().st_size for p in files) > MAX_TOTAL:
            raise ValueError('Input exceeds total size limit')
        sources, corpus = [], []
        for idx, path in enumerate(files, 1):
            if path.is_symlink() or path.stat().st_size > MAX_FILE:
                raise ValueError(f'Link or oversized input: {path.name}')
            relative = path.relative_to(root) if root.is_dir() else Path(path.name)
            target = stage / 'sources' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            source_id = f'S{idx:03}'
            source = {'id': source_id, 'path': target.relative_to(stage).as_posix(),
                      'sha256': digest(target), 'bytes': target.stat().st_size,
                      'parser': 'native', 'error': None}
            try:
                if path.suffix.lower() not in ALLOWED:
                    raise ValueError('Unsupported type retained as data; never opened or executed')
                blocks = parse(target, source_id)
                corpus.extend(dict(b, source_id=source_id) for b in blocks)
                if not blocks or any(b['quality'] != 'native' for b in blocks):
                    source['parser'] = 'needs_review'
            except Exception as error:
                source.update(parser='failed', error=f'{type(error).__name__}: {error}')
            sources.append(source)
        (stage / 'source_blocks.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding='utf-8')
        manifest = {'schema_version': 1, 'sources': sources, 'state': 'ingested',
                    'source_blocks_sha256': digest(stage / 'source_blocks.json')}
        (stage / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        os.rename(stage, output)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    try:
        result = ingest(args.input, args.output)
        print(json.dumps({'sources': len(result['sources']), 'state': result['state']}, ensure_ascii=False))
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        parser.exit(2, f'{error}\n')
