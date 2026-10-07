> **Scientific status (2026-10-06):** The author rejected the delivered manuscript for departure from the source theory and notation. A rebuilt compositional special-case candidate is undergoing independent source-fidelity audit under GOAL.md. Prior candidate reviews and checks do not establish acceptance of the rebuild.

# Compressible reactive poromechanics of olivine carbonation

An independent theory and MOOSE implementation repository for
**Mg₂SiO₄ + 2 CO₂ → 2 MgCO₃ + SiO₂**: three compressible elastic solids
(forsterite, magnesite, silica) and one aqueous CO₂-bearing multicomponent fluid
(water, dissolved carbon and reaction species). Dissolved species belong to one aqueous phase; nine aqueous species use the compositional parent’s component densities and mass fractions. No separate gas phase is modeled. Plasticity is outside scope. MOOSE kernels and tests were authorized on 7 October 2026; see [the implementation plan](PLAN.md). The manuscript is a theory candidate. Simulated AI review records are kept in
`reviews/`; they do not constitute journal acceptance or physical validation.

## Reproduce and inspect

```sh
git clone --recurse-submodules https://github.com/johntfoster/olivine-carbonation-theory.git
cd olivine-carbonation-theory
tools/setup-agent-workflows
make check
make paper
```

`make paper` requires latexmk and a TeX Live installation (recommended packages:
texlive-latex-extra, texlive-fonts-recommended). It explicitly builds
paper/main.tex into build/. Startup installs hooks and agent skills only.
The devcontainer is configured for a compiled MOOSE framework and scientific Python; hosted startup evidence is recorded separately. Install the scientific TeX toolchain
separately if it is absent.
See [reproduction requirements](environment/README.md) for Python and TeX tooling.
The analytical helper uses Python's standard library; no third-party Python
packages are required. Run its theory-only checks explicitly:

```sh
python3 verification/check_theory.py
```

These checks are analytical identities/limiting cases, not a MOOSE simulation or
experimental validation. The fluid chemistry, compressible elastic mechanics,
isotropic logarithmic mineral/skeleton Biot laws and closures must be assessed
against the current manuscript and [equation map](verification/equation-map.json).

## Immutable review inputs

Freeze only after the sole scientific writer has stopped, completed the checks,
and explicitly rebuilt the candidate PDF. The freeze helper never builds a paper
or manufactures absent scientific inputs:

```sh
python3 scripts/freeze_review.py --round round-01
python3 scripts/freeze_review.py --verify .agent-runtime/review-snapshots/round-01
python3 scripts/check_editorial_invariants.py .agent-runtime/review-snapshots/round-01 .
```

The payload includes scientific sources/bibliography, analytical evidence,
equation mapping, provenance, environment requirements, full license texts and
`build/main.pdf` plus `build/main.log`. Required inputs and supporting-science
paths are declared in [snapshot policy](scripts/review_snapshot_policy.json).
Every payload file is hash-manifested; files/directories are read-only. Permissions
prevent accidental changes, not changes by their filesystem owner. The verifier
checks hashes, sizes, exact file coverage, snapshot ID and read-only permissions.
`make paper` also writes the captured build command log and hash-bound build
provenance with tool versions. Freezing rejects stale recorded source/output
hashes or an analytical report that does not match the manuscript and checker.

Public source exports already present in this repository can be appended with
`--public-input-manifest path/to/manifest.json`. Its JSON `inputs` array declares
each root-relative `path`, exact `sha256`, `public: true`, HTTPS `source_url` and
`license`; the manifest is included too. Files under `source-snapshots/` require
this declaration. No sibling or missing source is copied or bootstrapped. Audit
the allowlist and contents for private material and prior review text before
freezing; filename guards cannot classify all content.

The optional repeated `--include` replaces the default allowlist, but cannot omit
required inputs or existing supporting science. Review snapshots deliberately
exclude `.agent/shared`, harness copies, Git state, private attachment paths and
earlier reviews. To reproduce a frozen candidate, first copy it to a writable
directory and use direct Python/`latexmk` commands from the environment guide;
`make check` and `make site` require the full clone's pinned shared submodule.

The editorial checker protects equation hashes, labels/references/citations,
symbol-command and digit multisets, macro definitions, and supporting-science
bytes. It is a conservative guard, not proof that scientific meaning stayed
unchanged; every prose cycle also requires a manual scientific diff audit.

- [Manuscript source](paper/main.tex)
- [Companion site](https://johntfoster.github.io/olivine-carbonation-theory/)
- [Development environment](https://codespaces.new/johntfoster/olivine-carbonation-theory)
- [Releases](https://github.com/johntfoster/olivine-carbonation-theory/releases)
- [Citation metadata](CITATION.cff)
- [Recorded status and verification categories](research-project.yml)

The companion website workflow is pinned to the shared infrastructure revision
and publishes default-branch pushes once GitHub Pages is enabled with the
**GitHub Actions** build type. A site URL is not deployment evidence. Live site
deployment and hosted Codespace verification remain pending until separately
recorded; do not publish a moving theory as accepted.

Code is Apache-2.0; manuscript prose and figures are CC-BY-4.0. See LICENSES.md.
Private correspondence and attachments are deliberately excluded.

## MOOSE kernels and companion website

Run `make moose`, `make test`, and `make site` in the numerical toolchain.
The [implementation map](verification/implementation-map.md) connects residuals
to labeled manuscript equations and quantitative tests. The companion site
packages source viewers for every local object and test input.
See [PLAN.md](PLAN.md) and [implementation status](docs/implementation-status.md).

Dispatch the base-image Actions workflow to build pinned MOOSE and scientific
Python once. Every push builds and tests a SHA-tagged application image in GHCR.
Codespaces startup compares complete application source hashes before reusing
its binary. The [environment guide](environment/README.md) explains immutable
image reproduction and the separate Codespaces prebuild setting.
