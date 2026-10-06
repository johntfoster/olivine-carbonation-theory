#!/usr/bin/env python3
"""Check necessary (not sufficient) conditions for a prose-only editorial change."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

MATH = re.compile(r'\\\[(.*?)\\\]|\\\((.*?)\\\)|\$\$(.*?)\$\$|(?<!\\)\$(.*?)(?<!\\)\$|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|displaymath|math)\}(.*?)\\end\{\5\}', re.S)
STRUCTURE = re.compile(r'\\(?:begin|end)\{[^}]+\}|\\(?:section|subsection|subsubsection|chapter|paragraph)\*?\b')
REFS = re.compile(r'\\(?:cite\w*|label|ref|eqref|autoref)\*?(?:\[[^]]*\])*\{[^}]*\}')
SYMBOLS = re.compile(r'\\[A-Za-z]+')
DIGITS = re.compile(r'(?<![A-Za-z])[-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_text(text):
    return '\n'.join(re.sub(r'(?<!\\)%.*$', '', line) for line in text.splitlines())


def invariants(data):
    text = source_text(data.decode('utf-8'))
    return {'structural_tokens': dict(sorted(Counter(STRUCTURE.findall(text)).items())),
            'digit_literals': dict(sorted(Counter(DIGITS.findall(text)).items())),
            'math_block_hashes': [digest(m.group(0).encode()) for m in MATH.finditer(text)],
            'citation_label_reference_tokens': dict(sorted(Counter(REFS.findall(text)).items())),
            'symbol_commands': dict(sorted(Counter(SYMBOLS.findall(text)).items()))}


def files(root):
    selected = {}
    for folder in ('paper', 'verification', 'data', 'evidence', 'parameters', 'scripts'):
        base = root / folder
        if base.exists():
            for path in sorted(base.rglob('*')):
                if path.is_symlink():
                    raise ValueError(f'symlink disallowed in editorial evidence: {path}')
                if path.is_file() and '__pycache__' not in path.parts and path.suffix not in {'.pyc', '.pyo'}:
                    selected[path.relative_to(root).as_posix()] = path.read_bytes()
    return selected


def compare(before, after):
    old, new = files(before), files(after)
    errors = []
    if 'paper/main.tex' not in old or 'paper/main.tex' not in new:
        errors.append({'missing_authority': 'paper/main.tex must exist in both trees'})
    if set(old) != set(new):
        errors.append({'file_set_changed': sorted(set(old) ^ set(new))})
    for name in sorted(set(old) & set(new)):
        if name.startswith('paper/') and name.endswith('.tex'):
            first, second = invariants(old[name]), invariants(new[name])
            changed = [key for key in first if first[key] != second[key]]
            if changed:
                errors.append({'path': name, 'changed_invariants': changed})
        elif old[name] != new[name]:
            errors.append({'path': name, 'scientific_payload_changed': True,
                           'before_sha256': digest(old[name]), 'after_sha256': digest(new[name])})
    return {'passed': not errors, 'files_compared': len(set(old) & set(new)), 'errors': errors,
            'limits': 'Necessary checks only. Manual diff audit must verify unchanged scientific claims, assumptions and meaning. Regex math detection does not implement the full TeX grammar; prose numerals and macro spelling are intentionally conservatively protected. PDF bytes are rebuilt separately, not required to remain identical.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    args = parser.parse_args()
    try:
        result = compare(args.before.resolve(), args.after.resolve())
        print(json.dumps(result, indent=2))
        return 0 if result['passed'] else 1
    except (ValueError, OSError, UnicodeError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    raise SystemExit(main())
