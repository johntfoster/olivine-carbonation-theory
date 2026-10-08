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
Those direct theory/build commands do not run numerical simulations; numerical reproduction is described below. Physical validation has not been performed.

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
The optional `.devcontainer/reproducible/devcontainer.json` pins the published
f2133b3 runtime snapshot by digest. Select that configuration to fix the numerical
environment. Its provenance records the exact image source revision; use that
revision in a separate checkout for the corresponding complete source tree.
The default configuration follows tested main builds. Image and hosted evidence is recorded in
`verification/environment-results.json`.

Creation and resume both run the source-matching guard. It reuses a prebuilt executable only if every
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

The base includes OpenSSH. The application entrypoint generates container host
keys and starts the listener before remote attachment. Port 22 serves the
standard Codespaces CLI; port 2222 supports private port forwarding. Concurrent
entrypoint and workspace setup share a runtime lock. Creation and resume repeat
the idempotent server start and source check; host private keys are absent from
the published image. Hosted setup can continue after the first connection, as
[GitHub documents](https://docs.github.com/en/codespaces/about-codespaces/deep-dive).

The published f2133b3 snapshot passed a full hosted Codespaces rebuild and a
stop/resume cycle through the standard CLI without manual configuration.
Creation and resume reused the source-matched executable; all 61 quantitative
checks passed, source/artifact hashes matched and manuscript bytes stayed
unchanged. The temporary verification environment is removed after evidence
archival. These numerical checks are synthetic verification, not physical
validation.

## Reproducing the numerical supplement without the workflow submodule

The numerical examples additionally require NumPy, SciPy and Matplotlib, pinned
by `toolchain.json` and the explicit Conda package lock. The theory checker
still uses only the standard library. A source supplement contains application
code rather than a prebuilt binary. In an activated environment installed from
`environment/moose-linux-64.lock`, retrieve the external MOOSE dependency at
`abafb58b67a6037c6723ffeb19647c84484466da`, including its submodules, and build the
application against that checkout. MOOSE's framework is compiled by its app
Makefile as needed. The following direct commands bypass workflow helpers:

```sh
# Activate the environment first so LIBMESH_DIR and compiler settings exist.
make -C moose_app -j2 MOOSE_DIR=/absolute/path/to/pinned/moose
python3 scripts/check_implementation.py --binary moose_app/olivine_carbonation-opt
python3 scripts/run_silica_verification.py --binary moose_app/olivine_carbonation-opt
python3 scripts/check_silica_jacobian.py --binary moose_app/olivine_carbonation-opt
python3 verification/build_equation_map.py
python3 verification/check_theory.py
make paper
```

The reproduction script expects the framework at `.agent-runtime/moose` for its
revision audit; install that checkout there (the default app Makefile location).
The numerical reference algorithms are part of the supplement. `data/silica/`
contains time histories, selected cell profiles, finite-volume references and
compressed actual solver logs. Figures are regenerated by the simulation script.
The new scientific sources require rebuilding even in a previously verified
image; historical hosted-image evidence is not an image of this extension.
