# Source inventory and scientific scope

## Requested problem

Forsterite carbonation: Mg2SiO4 + 2 CO2 -> 2 MgCO3 + SiO2. The model treats forsterite, magnesite, and silica as distinct compressible elastic solids, sharing a skeleton, with a CO2 pore phase. This is an idealized magnesium end-member, not a full mineralogical reconstruction of natural dunite. Plasticity, damage/fracture, and MOOSE implementation are excluded from the present authorized phase.

## Formulation sources

- Three-phase finite-deformation reacting-porous-media formulation: trace balances, reference conventions, distention and transfer-work structure to the actual source equations.
- Four-phase extension: use its balance/variational structure, but distinguish its two-solid/liquid/trapped-gas phase inventory from the present three-solid/reactive-CO2 inventory.
- Compositional reacting-mixture theory: source for compressible solid constituents and reaction-dependent coupling.
- Isotropic finite-strain Biot poromechanics: logarithmic mineral and skeleton laws, specialized to elasticity only. The anisotropic-Biot paper is not the constitutive source.

Source commits, file hashes and exact equation correspondence are recorded with the theory manuscript and its supporting scientific provenance. Existing source checkouts are read-only inputs; any dirty upstream scientific file requires its own hash, not a commit-only provenance claim.

## Experimental motivation, not validation

Liu, J., Wolterbeek, T. K. T., and Spiers, C. J. (2024), *Volumetric response and permeability evolution during carbonation of crushed peridotite under controlled stress-pressure-temperature conditions*, International Journal of Rock Mechanics and Mining Sciences 182, 105886. DOI: [10.1016/j.ijrmms.2024.105886](https://doi.org/10.1016/j.ijrmms.2024.105886).

The study concerns flow-through carbonation of compacted dunite with aqueous reactive fluids, not pure CO2 gas transport. It therefore motivates the problem but does not by itself validate the requested gas-phase elastic idealization. An aqueous/speciation model and a defensible treatment of grain-contact compaction would be needed before claiming quantitative reproduction. No experimental parameter calibration or MOOSE verification has been performed in this project.

The publisher-version article was retrieved from the [Utrecht institutional repository](https://research-portal.uu.nl/en/publications/volumetric-response-and-permeability-evolution-during-carbonation/). The originally supplied file with a PDF suffix was a saved HTML page rather than a PDF; its original bytes were preserved privately and a separately identified institutional PDF was acquired. Neither third-party article payload nor private correspondence is republished here.

## Private provenance

The original presentation and attachment bytes, extraction products and download hashes are retained outside this Git repository. The model specification here is an original synthesis of the authorized research problem, not a redistribution of private presentation content.
