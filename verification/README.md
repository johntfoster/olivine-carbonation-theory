# Verification of the compositional special case

This directory contains **new** consistency evidence for the source-specialized candidate. The author rejected the preceding candidate; none of its 358 checks or review votes are credited here. The preserved rejected snapshot is historical only.

## Reproduce

From repository root, with Python 3.10+ (standard library only):

```bash
python3 verification/build_equation_map.py
python3 verification/check_theory.py
make paper
```

The mapping command resolves explicit provenance comments against the exact-byte author-source snapshots in `verification/parent-sources/`. It writes `equation-map.json`, `source-equation-excerpts.json`, and `paper/source-correspondence.md`. The 18 snapshot files match hashes in `paper/source-lineage.json`; original resolved paths and Git HEAD values are retained there for provenance. The snapshots are the inspected scientific source surface, not a complete buildable distribution of each parent project. Their plastic/general multiphase sections are context only, not part of this specialization.

The scientific checks run without the original sibling repositories. When those originals are accessible, their present hashes are reported separately; their absence in an extracted package is not represented as a matching source. Snapshot-byte integrity is always checked. The source macro copy is compared byte-for-byte with the pinned compositional macro hash.

## Evidence interpretation

`analytical_report.json` records the command, Python version, all candidate/source/script hashes, individual errors/tolerances, and failures. Its current run has 52 checks: 49 synthetic algebra, conservation, dimensional, constitutive derivative, reference-transform and source-limit checks, plus 3 source/document-integrity checks. The count is not PDE verification, physical validation, or independent acceptance.

Meaningful source checks include:

- Exact atom, mass and charge cancellation for all seven mechanisms and the net carbonation reaction.
- Source material-insertion sum, reference pullback, virtual-work/traction invariance, and weak boundary signs.
- Both independent Coleman–Noll stress/trace restrictions, mineral mean-stress recovery, and constituent-mass solid insertion potential.
- One-solid elastic matched-log recovery; mineral root and fixed-pressure tangent; three-solid aggregate pressure tangent; zero-pressure and incompressible-mineral limits.
- Aqueous Gibbs/Helmholtz density transform and constituent-mass derivatives, including the solvent.
- One source-normalized exchange potential, algebraic transfer-work recovery, and nonzero fluid phase offset for phase-changing reaction power.
- Source corrected fluid resistance, insertion-force cancellation, conversion-free Darcy limit, and source reaction/diffusion/drag entropy production.

Material numbers are synthetic inputs recorded in the script/report, not empirical measurements. Chemical calibration, continuum solutions, time/mesh convergence, phase appearance, well-posedness of the coupled reaction/flow system and experimental validation are not established. The portable source map and passing tests do not replace the independent equation-by-equation source-fidelity audit.

## Future implementation

`implementation-map.md` gives the residual/material boundary and source equations. No MOOSE source or executable was created. The 17-field count applies to the three-dimensional quasi-static finite-rate branch; using four fast aqueous equilibria replaces four rate laws, not four mass balances.

## Authorized numerical implementation

MOOSE residual implementation was authorized on 7 October 2026. Run `make moose`
and `make test` in the pinned toolchain. `implementation-results.json` contains
quantitative executable checks, source hashes, commands and category-specific
errors/tolerances. The implementation map now names the actual AD residual,
material and boundary objects. The earlier future-implementation statements
above describe the preceding theory-only stage.
