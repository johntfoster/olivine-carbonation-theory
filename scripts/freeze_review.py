#!/usr/bin/env python3
"""Create a new read-only self-contained review snapshot from an explicit allowlist."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

DEFAULT_INCLUDE = ('paper', 'verification', 'scripts', 'docs', 'GOAL.md', 'README.md',
                   'LICENSES.md', 'CITATION.cff', 'research-project.yml', 'Makefile', 'build/main.pdf')
EXCLUDED = {'.git', '.agent-runtime', 'reviews', '.agent', '.agents', '.claude', '.opencode'}


def payload(root, includes):
    files = {}
    for item in includes:
        rel = Path(item)
        if rel.is_absolute() or '..' in rel.parts or any(p in EXCLUDED for p in rel.parts):
            raise ValueError(f'forbidden include: {item}')
        source = root / rel
        if not source.exists():
            raise ValueError(f'required review input missing: {item}')
        candidates = sorted(source.rglob('*')) if source.is_dir() else [source]
        for path in candidates:
            name = path.relative_to(root)
            if any(p in EXCLUDED or p == '__pycache__' for p in name.parts):
                continue
            if path.is_symlink():
                raise ValueError(f'symlinks cannot enter an independent snapshot: {name}')
            if path.is_file():
                if path.suffix in {'.pyc', '.pyo'}:
                    continue
                files[name.as_posix()] = path
    for required in ('paper/main.tex', 'build/main.pdf'):
        if required not in files:
            raise ValueError(f'self-contained review requires {required}')
    return files


def freeze(root, round_name, includes):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', round_name):
        raise ValueError('round must be a simple identifier')
    base = root / '.agent-runtime/review-snapshots'
    dest = base / round_name
    if dest.exists():
        raise ValueError(f'round already exists; never replace immutable evidence: {dest}')
    files = payload(root, includes)
    base.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.new-', dir=base))
    try:
        records = []
        for rel, source in sorted(files.items()):
            target = staging / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            records.append({'path': rel, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        manifest = (json.dumps(records, indent=2, sort_keys=True) + '\n').encode()
        (staging / 'MANIFEST.json').write_bytes(manifest)
        snapshot_id = hashlib.sha256(manifest).hexdigest()
        (staging / 'SNAPSHOT_ID').write_text(snapshot_id + '\n')
        for entry in staging.rglob('*'):
            entry.chmod(0o555 if entry.is_dir() else 0o444)
        staging.chmod(0o555)
        staging.rename(dest)
    except Exception:
        for entry in staging.rglob('*'):
            entry.chmod(0o755 if entry.is_dir() else 0o644)
        staging.chmod(0o755)
        shutil.rmtree(staging)
        raise
    return {'round': round_name, 'snapshot': str(dest), 'snapshot_id': snapshot_id,
            'files': len(records), 'report_paths': [f'reviews/{round_name}/reviewer-{n}.md' for n in (1, 2, 3)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--round', required=True)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--include', action='append', help='Explicit complete replacement allowlist; repeat per path')
    args = parser.parse_args()
    try:
        print(json.dumps(freeze(args.root.resolve(), args.round, args.include or DEFAULT_INCLUDE), indent=2))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
