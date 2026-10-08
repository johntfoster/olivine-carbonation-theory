# Source inventory and scientific scope

## Requested problem

Forsterite carbonation: Mg2SiO4 + 2 CO2 -> 2 MgCO3 + SiO2. The model treats forsterite, magnesite, and silica as distinct compressible elastic solids, sharing a skeleton, with one aqueous CO2-bearing multicomponent pore fluid. This is an idealized magnesium end-member, not a full mineralogical reconstruction of natural dunite. Plasticity and damage/fracture are excluded. MOOSE implementation was authorized on 7 October 2026; numerical manuscript examples and acceptance review were requested on 8 October 2026.

## Formulation sources

- Compositional reacting-mixture theory is the sole governing parent. The application is its special case, retaining its notation, balances, reference conventions, distention and transfer-work normalization.
- Three- and four-phase manuscripts are historical context only. Their different transfer-work prescriptions and phase inventories do not override the compositional parent.
- Isotropic finite-strain Biot poromechanics supplies the matched logarithmic constitutive specialization, restricted to elasticity and checked against the compositional constitutive restrictions. No anisotropic or plastic law is imported.
- The exact equation-level inheritance and restrictions are recorded in `docs/rebuild-source-contract.md`, `paper/source-correspondence.md`, and `verification/equation-map.json`. Exact-byte author-source snapshots support independent comparison.

Source commits, file hashes and exact equation correspondence are recorded with the theory manuscript and its supporting scientific provenance. Existing source checkouts are read-only inputs; any dirty upstream scientific file requires its own hash, not a commit-only provenance claim.

## Experimental motivation, not validation

Liu, J., Wolterbeek, T. K. T., and Spiers, C. J. (2024), *Volumetric response and permeability evolution during carbonation of crushed peridotite under controlled stress-pressure-temperature conditions*, International Journal of Rock Mechanics and Mining Sciences 182, 105886. DOI: [10.1016/j.ijrmms.2024.105886](https://doi.org/10.1016/j.ijrmms.2024.105886).

The study concerns flow-through carbonation of compacted dunite with aqueous reactive fluids, not pure CO2 gas transport. John authorized an aqueous formulation on 2026-10-06, replacing the original gas-only idealization. The study motivates the problem but is not evidence of model validation. Aqueous speciation, calibrated kinetics and a defensible treatment of grain-contact compaction remain necessary before claiming quantitative reproduction. No experimental parameter calibration has been performed. MOOSE implementation checks and the restricted numerical reaction examples are recorded separately in verification/.

The publisher-version article was retrieved from the [Utrecht institutional repository](https://research-portal.uu.nl/en/publications/volumetric-response-and-permeability-evolution-during-carbonation/). The originally supplied file with a PDF suffix was a saved HTML page rather than a PDF; its original bytes were preserved privately and a separately identified institutional PDF was acquired. Neither third-party article payload nor private correspondence is republished here.

## Private provenance

The original presentation and attachment bytes, extraction products and download hashes are retained outside this Git repository. The model specification here is a specialization of the author-owned compositional formulation, not a redistribution of private presentation content.
