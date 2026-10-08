#!/usr/bin/env python3
"""Build the static equation/code/evidence review interface without network access."""
import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / '.agent-runtime/site'
sys.path.insert(0, str(ROOT / 'site/vendor/pygments-2.19.2-py3-none-any.whl'))
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.util import ClassNotFound

ESC = html.escape
REPORTS = {'analytical': 'verification/analytical_report.json',
           'residuals': 'verification/implementation-results.json',
           'silica': 'verification/silica-results.json'}


def load(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def published_path(path):
    path = Path(path)
    # Pages artifact upload excludes any .github directory.
    return Path('github', *path.parts[1:]) if path.parts[0] == '.github' else path


def source_link(path, label=None, prefix='', line=None, end=None):
    public = published_path(path).as_posix()
    query = f'?lines={line}-{end or line}' if line else ''
    anchor = f'#L{line}' if line else ''
    return f'<a href="{prefix}sources/{public}.html{query}{anchor}">{ESC(label or str(path))}</a>'


def equation_link(eq, prefix=''):
    return f'<a class="chip" href="{prefix}equations.html#{eq["label"]}">Eq. {eq["number"]}</a>'


def object_link(obj, prefix=''):
    return f'<a href="{prefix}objects/{obj["name"]}.html">{ESC(obj["title"])}</a>'


def page(title, body, prefix='', wide=False):
    nav = [('index.html', 'Overview'), ('equations.html', 'Equations'),
           ('kernels.html', 'C++ objects'), ('verification.html', 'Evidence'),
           ('reproduction.html', 'Reproduce')]
    links = ''.join(f'<a href="{prefix}{url}">{label}</a>' for url, label in nav)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ESC(title)} · Olivine carbonation</title>
<link rel="stylesheet" href="{prefix}assets/style.css">
<script defer src="{prefix}assets/site.js"></script>
<script defer src="{prefix}assets/math-config.js"></script>
<script defer src="{prefix}assets/vendor/mathjax/tex-svg-full.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header><div class="container masthead">
<a class="brand" href="{prefix}index.html">Olivine carbonation<span>Compositional theory · numerical verification</span></a>
<nav aria-label="Main navigation">{links}</nav></div></header>
<main id="main" class="container{' wide' if wide else ''}">{body}</main>
<footer class="container"><p>John T. Foster · Code Apache-2.0 · Manuscript CC BY 4.0</p>
<p><a href="https://github.com/johntfoster/olivine-carbonation-theory">Repository</a> ·
<a href="{prefix}source-manifest.json">Packaged source hashes</a> ·
<a href="{prefix}site-provenance.json">Site provenance</a> ·
<a href="{prefix}assets/vendor/mathjax/LICENSE">Math renderer license</a> ·
<a href="{prefix}assets/vendor/PYGMENTS-LICENSE">Highlighter license</a></p></footer></body></html>'''


def highlighted_lines(path):
    source = (ROOT / path).read_text()
    try:
        lexer = get_lexer_for_filename(str(path), stripnl=False, ensurenl=False)
    except ClassNotFound:
        lexer = TextLexer(stripnl=False, ensurenl=False)
    rendered = highlight(source, lexer, HtmlFormatter(nowrap=True)).splitlines()
    assert len(rendered) == len(source.splitlines()), path
    return rendered


def code_block(path, start=1, end=None, prefix='', full=False):
    lines = highlighted_lines(path)
    end = end or len(lines)
    items = []
    for i in range(start, end + 1):
        url = f'#L{i}' if full else f'{prefix}sources/{published_path(path)}.html#L{i}'
        items.append(f'<span class="source-line" id="L{i}"><a class="line-number" href="{url}" aria-label="Source line {i}">{i}</a>{lines[i-1]}</span>')
    return '<pre class="code"><code>' + '\n'.join(items) + '</code></pre>'


def function_span(obj):
    source = (ROOT / obj['source']).read_text()
    marker = obj['name'] + '::' + obj['function']
    position = source.index(marker)
    start = source.count('\n', 0, position) + 1
    opening = source.index('{', position)
    depth = 1
    position = opening + 1
    # This source subset has no unmatched braces in strings/comments in these
    # functions. Check that the extracted closing brace ends a complete line.
    while depth:
        depth += (source[position] == '{') - (source[position] == '}')
        position += 1
    assert not source[position:source.find('\n', position)].strip()
    return start, source.count('\n', 0, position) + 1


def math(eq):
    return '<div class="math" data-equation="' + eq['label'] + '">' + ESC(eq['display_latex']) + '</div>'


def input_objects(deck, seen=None):
    seen = set() if seen is None else seen
    if deck in seen:
        return set()
    seen.add(deck)
    source = deck.read_text()
    names = set(re.findall(r'^\s*type\s*(?::=|=)\s*(\w+)', source, re.M))
    for include in re.findall(r'^\s*!include\s+([^\s#]+)', source, re.M):
        path = (deck.parent / include).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError('External input include rejected')
        names.update(input_objects(path, seen))
    return names


def evidence_table(checks, category, reverse=None, prefix='', ids=True):
    rows = []
    for item in checks:
        name = item['name']
        target = f'{category}-{name}'
        ident = f' id="{target}"' if ids else ''
        link = ESC(name) if ids else f'<a href="{prefix}verification.html#{target}">{ESC(name)}</a>'
        related = ' · '.join(object_link(o, prefix) for o in (reverse or {}).get((category, name), []))
        error = item.get('error')
        tolerance = item.get('tolerance')
        number = f'{error:.6g} / {tolerance:.6g}' if error is not None and tolerance is not None else 'See report'
        detail = ''
        if 'observed_orders' in item:
            detail = '<br>Orders: ' + ', '.join(f'{v:.3f}' for v in item['observed_orders'])
        rows.append(f'<tr{ident}><td>{link}{detail}<small>{related}</small></td><td>{number}</td><td>{"Pass" if item["passed"] else "FAIL"}</td></tr>')
    return '<div class="table-scroll"><table><thead><tr><th scope="col">Recorded check / implementing objects</th><th scope="col">Error / tolerance</th><th scope="col">Result</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'


def authoritative_evidence(equations, objects, reports):
    bindings = {}
    def bind(path, expected):
        p = ROOT / path
        if p.is_file():
            if sha(p) != expected:
                raise ValueError(f'Stale recorded evidence: {path}')
            bindings[str(path)] = expected
        elif str(path).startswith('moose_app/') and (
                str(path).startswith(('moose_app/olivine_carbonation-', 'moose_app/lib/'))
                or ('.libs' in Path(path).parts and Path(path).suffix in {'.o', '.so', '.a'})
                or str(path).endswith(('.lo', '.lo.d'))):
            return  # Compiled outputs are not required by a clean-clone site build.
        else:
            raise ValueError(f'Missing bound evidence: {path}')
    for path, value in equations['source_hashes'].items():
        bind(path, value)
    for category, report in reports.items():
        assert report['checks'] and all(c['passed'] for c in report['checks']), category
        for key in ('inputs', 'source_hashes', 'sources', 'data_hashes', 'solver_fingerprint'):
            for path, value in report.get(key, {}).items():
                bind(path, value)
    jac = load('verification/silica-jacobian-results.json')
    assert jac['status'] == 'passed' and jac['exit_code'] == 0
    assert all(v <= jac['tolerance'] for v in jac['relative_fd_differences'])
    for path, value in jac['source_hashes'].items():
        bind(path, value)
    acceptance = load('reviews/numerical-20261008-final/acceptance-record.json')
    assert acceptance['status'] == 'complete'
    for reviewer in acceptance['reviewers']:
        bind(reviewer['report'], reviewer['sha256'])
        assert reviewer['verdict'] == 'ACCEPT' and reviewer['required_revisions'] == 0
    bind('site/publication/manuscript.pdf', acceptance['pdf_sha256'])
    assert equations['pdf_sha256'] == acceptance['pdf_sha256']
    bind('site/publication/numerical-supplement.zip', acceptance['archive_sha256'])
    with zipfile.ZipFile(ROOT / 'site/publication/numerical-supplement.zip') as archive:
        manifest_name = next(n for n in archive.namelist() if n.endswith('/MANIFEST.json'))
        prefix = manifest_name[:-len('MANIFEST.json')]
        manifest_bytes = archive.read(manifest_name)
        assert hashlib.sha256(manifest_bytes).hexdigest() == acceptance['snapshot_id']
        for entry in json.loads(manifest_bytes):
            payload = archive.read(prefix + entry['path'])
            assert len(payload) == entry['bytes'] and hashlib.sha256(payload).hexdigest() == entry['sha256']
            # Scientific pages display the accepted scientific bytes. Site and
            # publication metadata may evolve after the frozen review snapshot.
            if entry['path'].startswith(('paper/', 'moose_app/', 'data/', 'figures/', 'verification/')):
                bind(entry['path'], entry['sha256'])
    dependencies = load('site/vendor/dependencies.json')
    bind('site/vendor/' + dependencies['filename'], dependencies['sha256'])
    bind('site/assets/vendor/mathjax/tex-svg-full.js', dependencies['mathjax']['sha256'])
    for path, figure in load('site/figure-provenance.json').items():
        bind(path, figure['asset_sha256'])
        bind(figure['source'], figure['source_sha256'])
    names = {o['name'] for o in objects}
    registered = {n for p in (ROOT / 'moose_app/src').rglob('*.C') for n in re.findall(r'registerMooseObject\(\s*"OlivineCarbonationApp",\s*(\w+)\)', p.read_text())}
    assert names == registered and len(names) == len(objects), (names ^ registered)
    labels = {e['label'] for e in equations['equations']}
    for obj in objects:
        assert obj['equations'] and set(obj['equations']) <= labels, obj['name']
        assert (ROOT / obj['header']).is_file()
        function_span(obj)
        if obj.get('equation_line_ranges'):
            assert sha(ROOT / obj['source']) == obj['line_range_source_sha256'], obj['name']
            assert set(obj['equation_line_ranges']) <= set(obj['equations'])
            a, b = function_span(obj)
            assert all(a <= span[0] <= span[1] <= b for span in obj['equation_line_ranges'].values())
        for alias in obj['aliases']:
            # Document aliases must actually occur in the implementation or its
            # header; descriptive expressions are checked one token at a time.
            tokens = re.findall(r'\b_[A-Za-z]\w*', alias)
            source = (ROOT / obj['source']).read_text() + (ROOT / obj['header']).read_text()
            assert all(re.search(r'\b' + re.escape(t) + r'\b', source) for t in tokens), (obj['name'], alias)
    return bindings, acceptance, jac


class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, attrs['id']
            self.ids.add(attrs['id'])
        self.links.extend(attrs[a] for a in ('href', 'src') if a in attrs)


def check(output):
    pages = {p.resolve(): Links(p.read_text()) for p in output.rglob('*.html')}
    count = 0
    for file, document in pages.items():
        for link in document.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file
            if not target.is_relative_to(output.resolve()) or not target.is_file():
                raise ValueError(f'Broken link {file}: {link}')
            if parsed.fragment and target.suffix == '.html' and unquote(parsed.fragment) not in pages[target].ids:
                raise ValueError(f'Broken anchor {file}: {link}')
            count += 1
    for path, value in json.loads((output / 'source-manifest.json').read_text()).items():
        assert sha(output / 'raw' / published_path(path)) == value, path
    provenance = json.loads((output / 'site-provenance.json').read_text())
    assert len(pages) == provenance['html_pages']
    return count


def build(output):
    output = output.resolve()
    if output == ROOT or not output.is_relative_to(ROOT / '.agent-runtime'):
        raise ValueError('Site output must be a dedicated directory under .agent-runtime')
    equation_export = load('site/manuscript-equations.json')
    equations = {e['label']: e for e in equation_export['equations']}
    objects = load('site/implementation-contract.json')['objects']
    reports = {c: load(p) for c, p in REPORTS.items()}
    bindings, acceptance, jac = authoritative_evidence(equation_export, objects, reports)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(ROOT / 'site/assets', output / 'assets')
    shutil.copytree(ROOT / 'site/publication', output / 'downloads')
    (output / '.nojekyll').touch()
    pygments_css = HtmlFormatter(style='monokai').get_style_defs('.code')
    (output / 'assets/highlight.css').write_text(pygments_css)

    decks = sorted(list((ROOT / 'moose_app/test/tests').rglob('*.i')) + list((ROOT / 'moose_app/examples').rglob('*.i')))
    deck_objects = {p: input_objects(p) for p in decks}
    reverse, by_source = {}, {}
    for obj in objects:
        by_source.setdefault(obj['source'], []).append(obj)
        by_source.setdefault(obj['header'], []).append(obj)
        obj['checks'] = [(category, item) for category, report in reports.items() for item in report['checks']
                         if any(item['name'].startswith(p) for p in obj['check_prefixes'])]
        assert obj['checks'], obj['name']
        for category, item in obj['checks']:
            reverse.setdefault((category, item['name']), []).append(obj)
    allow = []
    for directory, patterns in [('moose_app/src', ['*.C']), ('moose_app/include', ['*.h']),
                               ('moose_app/test/tests', ['*.i', 'tests']), ('moose_app/examples', ['*.i']),
                               ('scripts', ['*.py']), ('.devcontainer', ['Dockerfile*', '*.json', '*.sh']),
                               ('.github/workflows', ['*.yml']), ('environment', ['*.json', '*.md']),
                               ('verification', ['*.json', '*.md']), ('data/silica', ['*.csv', '*.md', '*.gz']),
                               ('reviews/numerical-20261008-final', ['*.json', '*.md'])]:
        for pattern in patterns:
            allow.extend((ROOT / directory).rglob(pattern))
    allow.extend(ROOT / p for p in ['PLAN.md', 'GOAL.md', 'research-project.yml', 'paper/main.tex',
                 'paper/defs.tex', 'paper/references.bib', 'paper/source-correspondence.md',
                 'moose_app/Makefile', 'moose_app/run_tests', 'docs/implementation-status.md',
                 'docs/numerical-verification-plan.md', 'site/implementation-contract.json',
                 'site/manuscript-equations.json', 'site/vendor/dependencies.json',
                 'site/figure-provenance.json', 'docs/companion-site-design.md'])
    manifest = {}
    for p in sorted(set(allow)):
        assert p.resolve().is_relative_to(ROOT) and p.is_file(), p
        rel = p.relative_to(ROOT)
        public = published_path(rel)
        dest = output / 'raw' / public
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dest)
        manifest[str(rel)] = sha(p)
        if p.suffix == '.gz':
            continue
        dest = output / 'sources' / (str(public) + '.html')
        dest.parent.mkdir(parents=True, exist_ok=True)
        prefix = '../' * len(dest.relative_to(output).parts[:-1])
        related = ' · '.join(object_link(o, prefix) for o in by_source.get(str(rel), []))
        body = f'<p class="eyebrow">Packaged source · immutable bytes</p><h1 class="source-title">{ESC(str(rel))}</h1><p>{related}</p><p><a href="{prefix}raw/{public}">Download raw source</a> · <button type="button" data-copy-url>Copy page link</button></p><details><summary>SHA-256</summary><code class="hash">{manifest[str(rel)]}</code></details>'
        if p == ROOT / 'moose_app/include/utils/MatchedLogMineralState.h':
            body += f'<p>Called by {object_link(next(o for o in objects if o["name"] == "ADLogarithmicMinerals"), prefix)} to select the admissible mineral root and propagate its AD tangent.</p>'
        body += code_block(rel, prefix=prefix, full=True)
        dest.write_text(page(str(rel), body, prefix, True))
    (output / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    def write(name, title, body, prefix='', wide=False):
        p = output / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(page(title, body, prefix, wide))

    totals = {c: len(r['checks']) for c, r in reports.items()}
    cards = ''.join(f'<a class="stat" href="verification.html#{c}"><strong>{totals[c]}</strong><span>{label}</span><small>Recorded checks · all pass</small></a>' for c, label in [('analytical', 'Analytical and source checks'), ('residuals', 'Residual and manufactured tests'), ('silica', 'Reaction and transport checks')])
    hero = '''<section class="hero"><p class="eyebrow">Theory → implementation → evidence</p><h1>A model you can inspect,<br>a result you can trace.</h1><p class="lead">Elastic deformation, aqueous transport and mineral conversion in the author's compositional reacting-mixture framework.</p><p class="reaction">Mg₂SiO₄ + 2 CO₂ → 2 MgCO₃ + SiO₂</p><div class="actions"><a class="button primary" href="equations.html">Explore the equations</a><a class="button" href="downloads/manuscript.pdf">Read the accepted manuscript ↗</a></div></section>'''
    start = '<section><h2>Start with an implementation</h2><p>Each review page places the rendered manuscript equation beside its exact, highlighted C++ function. Follow the source lines to inspect parameters and the recorded tests to check the result.</p><div class="grid">'
    for name in ['ADReferenceMassStorage', 'ADSilicaVerificationChemistry', 'ADEnrichedGalerkinFluxDG']:
        obj = next(o for o in objects if o['name'] == name)
        start += f'<article class="card"><p class="eyebrow">{ESC(obj["group"])}</p><h3>{object_link(obj)}</h3><p>{ESC(next(iter(obj["equations"].values())))}</p></article>'
    start += '</div></section>'
    figures = '''<section><h2>Two numerical verification examples</h2><p>The nonlinear silica/water subsystem exercises precipitation, dissolution and conservative diffusion. Parameters are synthetic; these tests do not establish a calibrated carbonation prediction.</p><div class="grid two"><a class="figure-card" href="verification.html#batch"><img src="assets/silica-batch.svg" alt="Closed-reactor aqueous trajectories and mineral changes for precipitation and dissolution"><h3>Closed reactor</h3><p>Opposite reaction directions agree with an independent extent ODE.</p></a><a class="figure-card" href="verification.html#column"><img src="assets/silica-column.svg" alt="Silica transport and mineral change profiles in a closed column"><h3>Closed column</h3><p>Precipitation and dissolution coexist; compare a separate finite-volume solve and inspect cell mass balances.</p></a></div></section>'''
    write('index.html', 'Overview', hero + '<div class="stats">' + cards + '</div>' + start + figures + '<aside class="note"><strong>Evidence scope.</strong> Three elastic solids and one aqueous phase. The full nine-species reacting constitutive material and experimental calibration remain open. <a href="model.html">Read the model scope</a>.</aside>')

    body = '<p class="eyebrow">Equation browser</p><h1>The manuscript, connected to code.</h1><p>All 75 numbered equations are exported from the built LaTeX manuscript. Numbering matches the downloadable PDF. An object link identifies its exact assembly responsibility; an equation without a mapped object is not a claim of implementation.</p><label class="filter-label" for="equation-filter">Find an equation, symbol label or implementing object</label><input id="equation-filter" type="search" data-filter="equation-list" placeholder="Try: mass, silica, EG, weak_momentum…"><p class="filter-status" aria-live="polite" data-status="equation-list"></p><div id="equation-list">'
    for eq in equations.values():
        related = [o for o in objects if eq['label'] in o['equations']]
        title = eq['label'][3:].replace('_', ' ').capitalize()
        body += f'<article class="equation-card filter-item" id="{eq["label"]}"><div class="section-heading"><h2>{eq["number"]}. {ESC(title)}</h2>{source_link("paper/main.tex", "Canonical LaTeX ↗", line=eq["source_line"])}</div>{math(eq)}<code class="equation-label">{eq["label"]}</code>'
        if related:
            body += '<ul class="responsibilities">' + ''.join(f'<li>{object_link(o)}<span>{ESC(o["equations"][eq["label"]])}</span></li>' for o in related) + '</ul>'
        else:
            body += '<p class="scope">No separate local object mapped. This display supplies theory, a definition or a derived consequence; inspect neighboring residual and material contracts before inferring implementation.</p>'
        body += f'<details><summary>Exact equation LaTeX</summary><pre class="latex">{ESC(eq["source_latex"])}</pre></details></article>'
    body += '</div><p class="empty" data-empty="equation-list" hidden>No matching equations. Clear the search to show all displays.</p>'
    write('equations.html', 'Equations', body, wide=True)

    body = '<p class="eyebrow">26 registered local objects</p><h1>Inspect an assembly responsibility.</h1><p>Open an object to compare the equations, C++ lines, material-property definitions, input decks and checks in one place. Generic MOOSE infrastructure remains in the <a href="sources/moose_app/src/base/OlivineCarbonationApp.C.html">application registration</a>.</p><label class="filter-label" for="object-filter">Find an object, responsibility or equation</label><input id="object-filter" type="search" data-filter="object-list" placeholder="Try: storage, traction, silica, cross…"><p class="filter-status" aria-live="polite" data-status="object-list"></p><div id="object-list" class="grid">'
    for obj in objects:
        chips = ''.join(equation_link(equations[e]) for e in obj['equations'])
        body += f'<article class="card filter-item"><p class="eyebrow">{ESC(obj["group"])}</p><h2>{object_link(obj)}</h2><code class="object-name">{obj["name"]}</code><p class="scope">{ESC(obj["scope"])}</p><p>{ESC(next(iter(obj["equations"].values())))}</p><div class="chips">{chips}</div></article>'
    write('kernels.html', 'C++ objects', body + '</div><p class="empty" data-empty="object-list" hidden>No matching objects.</p>')

    for obj in objects:
        start, end = function_span(obj)
        prefix = '../'
        body = f'<p class="eyebrow">{ESC(obj["group"])} · {ESC(obj["scope"])}</p><h1>{ESC(obj["title"])}</h1><p><code class="object-name">{obj["name"]}</code></p><p class="review-intro">Compare the formula with the implementation, then follow the test evidence below. All snippets are extracted from the packaged source, without edits.</p><div class="review-layout"><section class="equation-pane"><h2>Manuscript equations</h2>'
        for label, role in obj['equations'].items():
            eq = equations[label]
            a, b = obj.get('equation_line_ranges', {}).get(label, (start, end))
            body += f'<article class="equation-card"><div class="section-heading"><h3>Equation {eq["number"]}</h3>{equation_link(eq, prefix)}</div>{math(eq)}<p class="term-role">{ESC(role)}</p><p>{source_link("paper/main.tex", "LaTeX source ↗", prefix, eq["source_line"])} · {source_link(obj["source"], f"C++ lines {a}–{b} ↗", prefix, a, b)}</p></article>'
        body += f'</section><section class="code-pane"><h2>C++ implementation</h2><p>{source_link(obj["source"], "Full source and parameters ↗", prefix, start, end)} · {source_link(obj["header"], "Header", prefix)}</p>{code_block(obj["source"], start, end, prefix)}<details><summary>Source SHA-256</summary><code class="hash">{manifest[obj["source"]]}</code></details>'
        if obj['name'] == 'ADLogarithmicMinerals':
            body += '<aside class="note">The root solve is in ' + source_link('moose_app/include/utils/MatchedLogMineralState.h', 'matchedLogMineralVolume helper ↗', prefix) + '. Inspect it to verify branch selection and AD Newton; the displayed material calls it.</aside>'
        body += '</section></div><section><h2>Read the symbols in the code</h2><p>The formulas use the manuscript notation. The following properties show how that notation enters this object; all assembly uses the solid reference mesh.</p><div class="table-scroll"><table><thead><tr><th>Code property or expression</th><th>Meaning / measure</th></tr></thead><tbody>'
        body += ''.join(f'<tr><td><code>{ESC(alias)}</code></td><td>{ESC(meaning)}</td></tr>' for alias, meaning in obj['aliases'].items())
        body += '</tbody></table></div></section><section><h2>Input decks that instantiate this object</h2><ul class="deck-list">'
        selected = [p for p in decks if obj['name'] in deck_objects[p]]
        assert selected, obj['name']
        for deck in selected:
            spec = deck.parent / 'tests'
            body += '<li>' + source_link(deck.relative_to(ROOT), str(deck.relative_to(ROOT)), prefix)
            if spec.is_file():
                body += ' · ' + source_link(spec.relative_to(ROOT), 'Test specification', prefix)
            body += '</li>'
        body += '</ul></section><section><h2>Recorded verification linked to this responsibility</h2><p>These are relevant checks from the distinct evidence categories, not independent pass counts for this object. A check may exercise several objects together. Follow a row for the full report and all related objects.</p>'
        for category in REPORTS:
            checks = [c for cat, c in obj['checks'] if cat == category]
            if checks:
                body += f'<details class="check-group"><summary>{category.capitalize()} · {len(checks)} related checks</summary>{evidence_table(checks, category, prefix=prefix, ids=False)}</details>'
        if obj['name'] == 'ADSilicaVerificationChemistry':
            body += '<p><a href="../verification.html#jacobian">Coupled silica finite-difference Jacobian check ↗</a></p>'
        body += '</section><p><a href="../kernels.html">← All objects</a> · <a href="../equations.html">All equations →</a></p>'
        write('objects/' + obj['name'] + '.html', obj['title'], body, prefix, True)

    body = '<p class="eyebrow">Recorded scientific evidence · 8 October 2026</p><h1>What has been checked.</h1><p>Analytical consistency, executable residual tests, convergence, nonlinear reaction simulations and experimental validation are separate claims. Every number below comes from a hash-bound report included with the site.</p><div class="stats">' + cards + '</div><p class="jump-links"><a href="#batch">Reactor</a> · <a href="#column">Column</a> · <a href="#jacobian">Jacobian</a> · <a href="#analytical">Analytical</a> · <a href="#residuals">Residuals</a> · <a href="#silica">All reaction checks</a> · <a href="#acceptance">Review snapshot</a></p>'
    silica = reports['silica']
    body += '<section id="batch"><p class="eyebrow">Example 1 · reaction and time integration</p><h2>Closed reactor: precipitation and dissolution.</h2><p>Two actual MOOSE simulations start above or below the silica equilibrium quotient. Each solves complete aqueous and mineral mass residuals. An independently coded DOP853 extent equation supplies the reference trajectory.</p><img class="plot" src="assets/silica-batch.svg" alt="Recorded closed-reactor aqueous trajectories and mineral changes"><div class="table-scroll"><table><thead><tr><th>Initial direction</th><th>Initial aqueous Si</th><th>Final aqueous Si</th><th>Mineral change</th><th>Maximum trajectory error</th></tr></thead><tbody>'
    for case, item in silica['batch'].items():
        body += f'<tr><td>{case.capitalize()}</td><td>{item["initial_aqueous_si"]:.6g}</td><td>{item["final_aqueous_si"]:.9g}</td><td>{item["mineral_change_mol"]:+.9g}</td><td>{item["max_trajectory_error"]:.6g}</td></tr>'
    body += '</tbody></table></div><p>Amounts and trajectory errors are in mol/m³ of mixture. Final time 40 s; BDF2 step 0.0125 s. Both mineral and aqueous phases stay positive; elemental inventories and reaction power are checked.</p><h3>Time refinement against the independent extent ODE</h3><div class="table-scroll"><table><thead><tr><th>Case / scheme</th><th>Time steps (s)</th><th>Errors at 5 s (mol/m³)</th><th>Successive orders</th></tr></thead><tbody>'
    for key, item in silica['time_convergence'].items():
        body += f'<tr><td>{ESC(key)}</td><td>{", ".join(f"{v:g}" for v in item["steps"])}</td><td>{", ".join(f"{v:.4g}" for v in item["errors"])}</td><td>{", ".join(f"{v:.3f}" for v in item["orders"])}</td></tr>'
    body += '</tbody></table></div><p>Inspect ' + source_link('moose_app/examples/silica/batch.i', 'precipitation input') + ' · ' + source_link('moose_app/examples/silica/dissolution.i', 'dissolution input') + ' · <a href="raw/data/silica/precipitation.csv">precipitation CSV</a> · <a href="raw/data/silica/dissolution.csv">dissolution CSV</a> · <a href="objects/ADSilicaVerificationChemistry.html">implemented rate and potential equations</a>.</p></section>'
    body += '<section id="column"><p class="eyebrow">Example 2 · transport and element conservation</p><h2>Closed column: both reaction directions in one domain.</h2><p>A 1 m closed column starts with n₇ = 5 + 4 cos(πX) mol/m³. The continuous plus P0 potential drives diffusion; the mineral changes locally with reaction. A separately coded 1024-cell finite-volume BDF calculation supplies the comparison.</p><img class="plot" src="assets/silica-column.svg" alt="Recorded closed-column aqueous and mineral change profiles"><div class="table-scroll"><table><thead><tr><th>EG cells</th><th>Aqueous RMS error (mol/m³)</th><th>Mineral RMS error (mol/m³)</th><th>Max. cell mass residual (kg/m³/s)</th><th>Saved worst cell</th></tr></thead><tbody>'
    for row in silica['spatial_convergence']:
        audit = row['worst_cell_audit']
        links = ' · '.join(f'<a href="raw/data/silica/{filename}">{"nodes" if "nodes" in filename else "profile " + filename[-8:-4]}</a>' for filename in audit['files'])
        body += f'<tr><td>{row["cells"]}</td><td>{row["aqueous_l2_error"]:.7g}</td><td>{row["mineral_l2_error"]:.7g}</td><td>{row["max_cell_mass_residual"]:.7g}</td><td>Cell {audit["cell_zero_based"]} at {audit["time"]:g} s<br>{links}</td></tr>'
    global_drift = max(c['error'] for c in silica['checks'] if re.search(r'(Si|H|O)_conservation$', c['name']))
    body += f'</tbody></table></div><p>Fixed time step 0.005 s; final time 5 s. The independently coded FV references at 512 and 1024 cells differ by {silica["fv_reference_difference"]:.6g} mol/m³. A separate fixed-mesh time study gives order {silica["spatial_time_order"]:.4f}. Maximum recorded global elemental drift across the reaction suite is {global_drift:.6g} (relative).</p><aside class="note">The saved worst-cell profiles include the three BDF2 histories and the current nodal field. They support the displayed cell balance. Complete intermediate profiles require rerunning the simulations; see the data README.</aside><p>' + source_link('moose_app/examples/silica/spatial.i', 'Column input') + ' · ' + source_link('data/silica/README.md', 'Data and solver-log index') + ' · ' + source_link('scripts/run_silica_verification.py', 'Independent ODE/FV references and cell-balance audit') + ' · <a href="objects/ADEnrichedGalerkinFluxDG.html">Implemented element-face flux</a>.</p></section>'
    body += '<section id="jacobian"><h2>Coupled nonlinear Jacobian</h2><p>PETSc finite-difference comparison for the coupled 8-cell silica system, one time step. The four matrix comparisons are ' + ', '.join(f'{v:.6g}' for v in jac['relative_fd_differences']) + f'; tolerance {jac["tolerance"]:g}. All pass; command exit code {jac["exit_code"]}.</p><p>' + source_link('verification/silica-jacobian-results.json', 'Exact command, source hashes and output artifacts') + ' · ' + source_link('scripts/check_silica_jacobian.py', 'Check generator') + '</p></section>'
    for category, report in reports.items():
        desc = {'analytical': '49 analytical consistency checks and 3 source/document integrity checks. These do not constitute PDE verification.', 'residuals': 'Actual residual, finite-deformation, Jacobian, boundary-sign and manufactured-solution checks, including 1D/2D/3D and cross-diffusion refinement.', 'silica': '178 checks from 33 actual MOOSE reaction/transport solves. The latest report reanalyzes completed solves with saved source and linked-artifact fingerprints; this site build does not rerun them.'}[category]
        body += f'<section id="{category}"><h2>{category.capitalize()} · {len(report["checks"])} checks</h2><p>{desc}</p><p>{source_link(REPORTS[category], "Full report, provenance and commands")}</p>{evidence_table(report["checks"], category, reverse)}</section>'
    body += f'<section id="acceptance"><h2>Review acceptance belongs to an immutable snapshot.</h2><p>Three independent final reports give exact ACCEPT for the numerical manuscript snapshot, after three Foster prose cycles. The website is a later presentation of that evidence; the frozen supplement identifies exactly what was reviewed.</p><p>Snapshot SHA-256: <code class="hash">{acceptance["snapshot_id"]}</code></p><ul>'
    for reviewer in acceptance['reviewers']:
        body += '<li>' + source_link(reviewer['report'], f'Reviewer {reviewer["seat"]}: ACCEPT') + '</li>'
    body += '</ul><p><a href="downloads/manuscript.pdf">Accepted PDF</a> · <a href="downloads/numerical-supplement.zip">Hash-verified numerical supplement</a> · ' + source_link('reviews/numerical-20261008-final/acceptance-record.json', 'Acceptance record') + '</p></section><aside class="note"><strong>Physical validation has not been performed.</strong> Test constants are synthetic. The full carbonation network, calibrated material response and disappearance/nucleation of phases are not verified by these examples.</aside>'
    write('verification.html', 'Evidence', body, wide=True)

    write('model.html', 'Model scope', '<p class="eyebrow">Scientific scope</p><h1>A compositional special case.</h1><p>Forsterite A, magnesite B and silica C are compressible elastic solids. All nine aqueous species belong to one fluid phase, with dependent water mass fraction. The theory uses the author’s existing compositional notation and transfer-work normalization.</p><p>The implemented residuals and mineral constitutive law are separately verified. The nonlinear examples restrict chemistry to mechanism (3), H₄SiO₄ ⇌ SiO₂ + 2 H₂O, with positive inert A and B. They retain complete mass storage but set F=I, J=1, p=0 and electric field, bulk flow and transfer-work field to zero. The other reactions and aqueous species are excluded from this test subsystem.</p><p>The full reacting nine-species constitutive material and its calibrated response remain open. Phase disappearance, nucleation, plasticity and a separate gas phase are outside this implementation.</p><p><a href="equations.html">Read all numbered equations</a> · <a href="downloads/manuscript.pdf">Read the manuscript</a> · ' + source_link('paper/source-correspondence.md', 'Parent-source correspondence') + ' · ' + source_link('verification/implementation-map.md', 'Theory/code contract') + '</p>')
    write('reproduction.html', 'Reproduce', '''<p class="eyebrow">Reproduction and provenance</p><h1>Inspect the inputs. Rebuild the evidence.</h1><p>Use the repository’s pinned MOOSE environment. The commands below compile and run explicitly; opening this website does not run a simulation.</p><pre class="commands">git clone --recurse-submodules https://github.com/johntfoster/olivine-carbonation-theory.git
cd olivine-carbonation-theory
tools/setup-agent-workflows
make check
make moose
make test
make verification-examples
tools/moose-run python3 scripts/check_silica_jacobian.py
make paper
python3 scripts/export_site_equations.py
make site</pre><p>See each generator’s arguments before running. The silica script can reanalyze saved completed solves when their solver fingerprint matches; omit <code>--reuse-completed</code> to generate new trajectories. Numerical reports record commands, framework revision, executable and linked-library hashes, data hashes, tolerances and reference methods.</p><h2>Accepted publication artifacts</h2><p><a href="downloads/manuscript.pdf">19-page accepted PDF</a> · <a href="downloads/numerical-supplement.zip">Frozen numerical supplement</a>. The site checks the archive’s 278 payload entries and manifest ID, the PDF digest, and the current scientific sources against that frozen evidence.</p><h2>Environment evidence has a revision scope</h2><p>Recorded hosted startup and published image checks concern the earlier f2133b3 application revision and its 61-test suite. They do not certify a new hosted run of the later silica extension. The launcher uses the repository’s current application image; inspect Actions and the image’s exact revision before reuse.</p><p><a class="button" href="https://codespaces.new/johntfoster/olivine-carbonation-theory">Launch a Codespace ↗</a> <a href="https://github.com/johntfoster/olivine-carbonation-theory/actions">Inspect GitHub Actions ↗</a></p><ul><li>''' + source_link('environment/README.md', 'Environment and image instructions') + '</li><li>' + source_link('verification/environment-results.json', 'Historical environment and hosted-startup evidence') + '</li><li>' + source_link('.devcontainer/Dockerfile', 'Application Dockerfile') + '</li><li>' + source_link('scripts/run_silica_verification.py', 'Simulation/reference generator') + '</li><li>' + source_link('verification/silica-results.json', 'Reaction/transport report') + '</li><li>' + source_link('site/implementation-contract.json', 'Machine-readable equation/object responsibilities') + '</li></ul>')
    revision = None
    try:
        top = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', '--show-toplevel'], text=True).strip()
        if Path(top).resolve() == ROOT:
            revision = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    provenance = {'site_source_revision': revision,
                  'scientific_snapshot_id': acceptance['snapshot_id'], 'pdf_sha256': acceptance['pdf_sha256'],
                  'supplement_sha256': acceptance['archive_sha256'], 'objects': len(objects),
                  'equations': len(equations), 'recorded_checks': totals, 'source_files': len(manifest),
                  'html_pages': len(list(output.rglob('*.html'))), 'verified_evidence_bindings': bindings,
                  'report_hashes': {path: sha(ROOT / path) for path in REPORTS.values()},
                  'publication_scope': 'Presentation of the accepted numerical scientific payload; hosted environment evidence is historical.',
                  'asset_hashes': {str(p.relative_to(output)): sha(p) for p in (output / 'assets').rglob('*') if p.is_file()}}
    (output / 'site-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    return {'objects': len(objects), 'equations': len(equations), 'sources': len(manifest),
            'evidence_bindings': len(bindings), 'html_pages': provenance['html_pages'], 'checked_links': check(output)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(json.dumps({'checked_links': check(args.output)} if args.check else build(args.output), indent=2))
