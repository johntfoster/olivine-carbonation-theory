# Companion site: independent equation/code review

The companion site is a static GitHub Pages publication built by
`scripts/build_site.py`. The manuscript and recorded scientific results remain
its authority. The user authorized updating and deploying the site on
8 October 2026.

## Review structure

- **Equation browser:** all 75 numbered displays, generated from `paper/main.tex`
  and the explicitly built `build/main.aux`; numbering matches the accepted PDF.
  Search covers source labels, formulas and implementing responsibilities.
- **Object reviews:** all 26 local registered objects. Each page pairs the
  rendered equations and assembly responsibility with the actual highlighted
  C++ function. Property definitions state notation, units and measures. Direct
  source-line links identify the implemented terms; input decks and report rows
  connect them to executable checks.
- **Bidirectional contract:** `site/implementation-contract.json` generates both
  indexes and the reverse evidence links. Partial residuals, synthetic fixtures,
  restricted chemistry and weak-Dirichlet extensions are explicitly identified.
  A mapped source must be registered; every registered object must be mapped.
  Named properties must occur in its code/header. Curated line ranges have a
  source digest, preventing silently shifted anchors.
- **Evidence:** analytical/source checks, residual/MMS checks, nonlinear silica
  simulations, convergence, the coupled FD Jacobian and physical validation are
  distinct categories. CSVs, compressed solver logs, saved worst-cell histories,
  input decks and independent-reference generators are available. Acceptance
  applies to the immutable numerical snapshot, not to later presentation edits.
- **Downloads:** the exact accepted PDF and supplement are publication assets
  under `site/publication/`. The manuscript build directory remains ignored.

## Presentation and accessibility

A restrained light background, generous spacing and clear typography emphasize
formulas and evidence. Desktop object reviews place equations beside C++; mobile
reviews stack them. Math and code scroll within their own containers. Overflowing
formulas have a visible scroll hint and keyboard focus. Filters have labels,
live counts and an explicit empty state. Navigation and all links work without
JavaScript; raw LaTeX remains available when the math renderer is disabled.
C++ highlighting is generated on the server; line numbers are stable anchors.

## Source fidelity and dependencies

`export_site_equations.py` is run after an explicit `make paper`. It splits
numbered displays on source labels, retaining preceding unnumbered align rows,
and binds the export to the manuscript/macros and accepted PDF hashes. Browser
rendering adapts only the parent macros to MathJax syntax; the heavy material-rate
bullet is retained. The exact original LaTeX is exposed beside each display.

MathJax 3.2.2's complete TeX/SVG component and the pure-Python Pygments 2.19.2 wheel
are pinned with source URLs, hashes and licenses. Builds require no dependency
installation or network. Math, fonts and interaction scripts are served by the
site. Figure SVGs are direct `pdftocairo -svg` conversions of the accepted PDF
figures, with their source and asset hashes in `site/figure-provenance.json`.

The builder rejects stale evidence, failed report checks, source drift, missing
object mappings, missing input decks, broken links or anchors, and incorrect raw
source bytes. It verifies all 278 supplement payload entries and the immutable
manifest ID, then binds current manuscript/code/data/figure/report sources to
that accepted scientific payload. Compiled executable/library hashes are checked
when those local artifacts exist; a source-only clean clone does not claim a new
compiled or hosted run. The accepted artifact remains fully self-contained.

## Verification record

Local and deployed browser checks cover rendering, syntax highlighting, filters,
source-line selection and desktop/mobile layout. The publication audit records
its exact commit and Pages run, plus the deployed artifact digests. Historical
Codespaces evidence concerns the older f2133b3 application revision; the website
states that limitation instead of extending that evidence to the silica work.
