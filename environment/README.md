# Reproduction requirements

## Theory and frozen reviews

- Python 3.10 or later. The analytical checker and review helpers use only the
  standard library; `requirements.txt` deliberately has no installable packages.
- GNU Make for repository convenience targets (not required for direct commands).
- `latexmk`, `pdflatex`, and BibTeX from TeX Live, including the LaTeX extra and
  recommended-font collections. On Ubuntu/Debian install
  `latexmk texlive-latex-extra texlive-fonts-recommended`.

Run from the repository or frozen snapshot root:

```sh
python3 verification/check_theory.py
python3 scripts/build_paper.py
```

A frozen snapshot is read-only. Copy it to a separate writable directory before
reproducing commands that write verification reports or build products. Compare
reported source/script hashes to its manifest; the copied result is not a new
accepted snapshot. The analytical checker does not require Git. Its report records
SHA-256 hashes for the candidate inputs and whether each original source is
available and still matches its pinned snapshot; it does not record a Git HEAD.
Numerical simulations and physical validation are not covered.

## Repository infrastructure

Git and the exact `.agent/shared` submodule revision declared in
`research-project.yml` are required by `make check`, `make site` and workflow
setup. Initialize with `git submodule update --init --recursive`. Review snapshots
intentionally exclude this submodule and harness copies; their scientific checks
and manuscript build use the direct commands above. Hosted Codespaces and live
site deployment require separate verification.

The devcontainer provides the pinned MOOSE framework and scientific Python.
A scientific TeX installation and hosted startup require separate evidence.

## MOOSE implementation and prebuilt images (authorized 7 October 2026)

`environment/toolchain.json` and `moose-linux-64.lock` pin the linux/amd64
framework and exact Conda artifacts, including archive checksums. The base
Dockerfile compiles the pinned framework once and installs NumPy, SciPy,
Matplotlib and pandas. Dispatch **Build MOOSE base image** before the first
application image build, and after deliberately changing the toolchain lock.

Every push builds the exact checked-out revision, runs the quantitative
implementation checks inside the candidate image, then publishes
`ghcr.io/johntfoster/olivine-carbonation-theory:sha-<full-commit>`.
Image evidence includes the base digest, source revision, executable digest
and exact compiled-source hashes. Failed tests prevent publication.
The `main` alias is a convenience for normal Codespaces startup; immutable
reproduction uses the digest listed in the image-evidence Actions artifact.
Set the devcontainer `image` to that digest when reproducing a fixed snapshot.

The source-matching startup guard reuses a prebuilt executable only if every
application source/header and Makefile matches its recorded SHA-256. An older
image therefore cannot silently execute an older application against a new
workspace. Edited code rebuilds locally. Run build commands through
`tools/moose-run` (or `with-moose` inside the container) so Conda activation
exports MPI, compiler and libMesh settings. Open a new terminal after setup.

```sh
make moose
make test
make site
```

Codespaces prebuild settings are configured separately in GitHub repository
settings. Enable main-branch prebuilds for this devcontainer if desired;
GHCR publication by itself is not a hosted Codespaces startup check.
The image includes numerical tooling. Install TeX separately for an explicit
`make paper`; startup never compiles or modifies the manuscript.

Application image builds also compare the source toolchain lock against the
installed base lock; a mismatch requires a new base build. Codespaces startup
rejects an image for a different workspace toolchain rather than compiling
against an outdated environment.
