# Aqueous formulation: scope decision

John authorized this change on 2026-10-06, replacing the original pure-CO2 pore-fluid idealization. This document records scope, not completed derivations or validation.

## Phase and component distinction

The model has three compressible elastic solid phases (forsterite, magnesite and silica) and one aqueous fluid phase. Water, dissolved carbon, dissolved magnesium/silicon and the species needed by the selected chemical closure belong to that same fluid. A separate gas phase is deferred. Single-fluid admissibility must be stated, not assumed across gas exsolution conditions.

## Required theory revision

- Preserve finite-deformation kinematics and derive mineral/skeleton coupling from the isotropic logarithmic elastic laws, not the anisotropic coefficient formulation.
- Account for independent mineral dissolution and precipitation, dissolved storage and transport. The net carbonation stoichiometry alone does not close transient aqueous transport.
- Specify a component/species basis, charge balance, solvent accounting, chemical equilibrium/activity conventions, equation of state and kinetic laws. Clearly distinguish an idealized dilute closure from a calibrated brine model.
- Derive thermodynamically compatible transport, reaction affinities and reaction-transfer work rather than replacing gas density by water density.
- Supply implementation-ready weak forms, admissibility conditions, initial/boundary data, parameter inventory, equation correspondence and reproducible analytical consistency checks.

## Retained boundaries

Elastic constituents only: no plasticity, grain rearrangement, fracture or crushing. No MOOSE implementation before separate authorization after theory acceptance. The Liu et al. aqueous experiments motivate eventual comparison; matching their fluid category is not experimental validation or a calibrated reconstruction of natural dunite.

## Acceptance

Three independent reviewers of the same immutable scientific snapshot, at least two exact ACCEPT verdicts and resolution of substantiated defects; then three separate Foster prose-only cycles; then a fresh three-reviewer round with the same threshold. Deliver the current accepted PDF and verified repository/site links. All reviews are simulated AI reviews, not journal acceptance.
