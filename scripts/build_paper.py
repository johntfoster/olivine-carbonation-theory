#!/usr/bin/env python3
"""Explicit LaTeX build with hash-bound provenance; never run by startup hooks."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess

COMMAND = ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
           '-outdir=build', 'paper/main.tex']
OUTPUTS = ('build/main.pdf', 'build/main.log', 'build/build-command.log')
SOURCE_DIRS = ('paper', 'sections', 'figures')


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(root):
    files = {}
    for directory in SOURCE_DIRS:
        base = root / directory
        if base.is_symlink():
            raise ValueError(f'build source symlink disallowed: {directory}')
        if base.exists():
            for path in sorted(base.rglob('*')):
                if path.is_symlink():
                    raise ValueError(f'build source symlink disallowed: {path.relative_to(root)}')
                if path.is_file():
                    files[path.relative_to(root).as_posix()] = sha256(path)
    for path in root.iterdir():
        if path.suffix in {'.tex', '.bib', '.sty', '.cls', '.bst'}:
            if path.is_symlink():
                raise ValueError(f'build source symlink disallowed: {path.name}')
            files[path.name] = sha256(path)
    if 'paper/main.tex' not in files:
        raise ValueError('paper/main.tex is required')
    return dict(sorted(files.items()))


def build(root):
    initial = sources(root)
    outdir = root / 'build'
    if outdir.is_symlink():
        raise ValueError('build directory cannot be a symlink')
    outdir.mkdir(exist_ok=True)
    record = outdir / 'build-provenance.json'
    if record.exists():
        record.unlink()  # A failed rebuild must not leave apparently current provenance.
    completed = subprocess.run(COMMAND, cwd=root, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, check=False)
    (outdir / 'build-command.log').write_text(completed.stdout)
    print(completed.stdout, end='')
    if completed.returncode:
        raise ValueError(f'latexmk failed with exit status {completed.returncode}')
    if initial != sources(root):
        raise ValueError('manuscript sources changed during build; no provenance recorded')
    for name in OUTPUTS:
        if not (root / name).is_file() or (root / name).is_symlink():
            raise ValueError(f'build output missing/nonregular: {name}')
    versions = {}
    for tool, argument in [('latexmk', '-v'), ('pdflatex', '--version'), ('bibtex', '--version')]:
        result = subprocess.run([tool, argument], cwd=root, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, check=True)
        versions[tool] = result.stdout.strip()
    payload = {'category': 'manuscript-build-provenance-not-scientific-validation',
               'command': COMMAND, 'python': platform.python_version(),
               'tool_versions': versions, 'sources': initial,
               'outputs': {name: sha256(root / name) for name in OUTPUTS}}
    record.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        build(args.root.resolve())
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
