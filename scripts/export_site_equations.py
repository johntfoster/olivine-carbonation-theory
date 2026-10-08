#!/usr/bin/env python3
"""Export numbered source displays after an explicit manuscript build.

The checked-in export lets Pages build without a TeX installation. Its source
hashes are checked by the site builder; it cannot silently outlive a paper edit.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export():
    source = (ROOT / 'paper/main.tex').read_text()
    aux = (ROOT / 'build/main.aux').read_text()
    numbers = dict(re.findall(r'\\newlabel\{(eq:[^}]+)\}\{\{(\d+)\}', aux))
    equations = []
    for match in re.finditer(r'\\begin\{(equation|align)\}(.*?)\\end\{\1\}', source, re.S):
        env, content = match.group(1, 2)
        # Split only on an actual numbered label. Leading unnumbered rows stay
        # with the following numbered row (e.g. the complete weak fluid form).
        start = 0
        for label_match in re.finditer(r'\\label\{(eq:[^}]+)\}', content):
            label = label_match.group(1)
            raw = content[start:label_match.end()]
            start = label_match.end()
            raw = re.sub(r'^\s*\\\\\s*', '', raw).strip()
            display = re.sub(r'\\label\{[^}]+\}|\\notag', '', raw).strip()
            display = re.sub(r'\\eqref\{(eq:[^}]+)\}', lambda m: '(' + numbers[m[1]] + ')', display)
            if env == 'align':
                display = r'\begin{aligned}' + display + r'\end{aligned}'
            display = r'\begin{equation}' + display + r'\tag{' + numbers[label] + r'}\end{equation}'
            line = source.count('\n', 0, match.start()) + 1
            equations.append({'label': label, 'number': int(numbers[label]),
                              'source_line': line, 'source_latex': raw,
                              'display_latex': display})
    source_labels = re.findall(r'\\label\{(eq:[^}]+)\}', source)
    assert [e['label'] for e in equations] == source_labels
    assert len(set(source_labels)) == len(equations) == 75
    assert [e['number'] for e in equations] == list(range(1, 76))
    result = {'source_hashes': {p: digest(ROOT / p) for p in ['paper/main.tex', 'paper/defs.tex']},
              'pdf_sha256': digest(ROOT / 'build/main.pdf'), 'equations': equations}
    (ROOT / 'site/manuscript-equations.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'Exported {len(equations)} exact numbered displays from the built manuscript.')


if __name__ == '__main__':
    export()
