# Compressible reactive poromechanics of olivine carbonation

An independent, theory-only research repository for
**Mg₂SiO₄ + 2 CO₂ → 2 MgCO₃ + SiO₂**: three compressible elastic solids
(olivine, magnesite, silica) and one CO₂ phase. Plasticity and numerical/MOOSE
implementation are outside this stage. The manuscript is an unreviewed working
formulation, not an accepted paper or completed physical validation.

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
The pinned devcontainer supports infrastructure/source inspection; a hosted
Codespace has not yet been verified. Install the scientific TeX toolchain
separately if it is absent.

- [Manuscript source](paper/main.tex)
- [Companion site](https://johntfoster.github.io/olivine-carbonation-theory/)
- [Development environment](https://codespaces.new/johntfoster/olivine-carbonation-theory)
- [Releases](https://github.com/johntfoster/olivine-carbonation-theory/releases)
- [Citation metadata](CITATION.cff)
- [Recorded status and verification categories](research-project.yml)

Code is Apache-2.0; manuscript prose and figures are CC-BY-4.0. See LICENSES.md.
Private correspondence and attachments are deliberately excluded.
