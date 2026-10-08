# Numerical manuscript extension — 8 October 2026

The author requests discretization and implementation exposition, two actual
mineral reaction simulations, and the full simulated AI acceptance cycle.
Existing manuscript and review-helper changes were copied to the ignored
`numerical-extension-20261008` baseline before work began.

## Scientific contract

Use the controlling balances `eq:reference_fluid_mass`,
`eq:reference_solid_mass`, chemical potentials `eq:aqueous_potentials`,
`eq:solid_potential`, reaction law `eq:reaction_kinetics` and relative diffusion
`eq:relative_transport`. Retain three positive mineral phases and one aqueous
phase. Test mechanism (3), H4SiO4 <-> SiO2 + 2 H2O, with a binary aqueous
subsystem; the other six mechanisms are suppressed in this restricted test.
This restriction tests a mineral-forming step of carbonation, rather than
claiming simulation of the entire seven-mechanism network.

Prescribe F=I, J=1, p=p0=0, uniform tau=0, zero electric field, no body force,
and closed boundaries. All reference intrinsic densities are 1000 kg/m3,
and each aqueous molar volume is its molar mass divided by this density.
Then the fluid EOS is composition independent, mineral roots are one, and
reaction volume and total mass cancel exactly. Positive finite elastic moduli
are retained, although this unstressed branch does not discriminate mechanics.
Use ideal mixing and a chosen solid reference energy to set equilibrium.
These are synthetic parameters, not silica or olivine calibration data.

The computational transport variable is the invertible scaled potential
q=M_Si*(mu_Si-mu_water)/(R theta), not a replacement balance law. The material
recovers mass fractions from q and differences complete storage
J phi_f rhobar_f eta_Si. Aqueous silica uses P1+P0 EG in space; silica solid
fraction uses P0 because its equation has no flux. Forsterite and magnesite
fractions remain constant and positive. Solvent mass is the complementary
fluid mass, with opposite relative mass flux.

## Examples and gates fixed before runs

1. **Closed reactor, precipitation and dissolution.** Start above and below
   the same equilibrium. Compare actual MOOSE time histories to an independent
   scalar extent ODE, solved with SciPy DOP853 at tight tolerances. Verify
   Si/H/O conservation, reaction direction, approach to equilibrium, positive
   masses, nonnegative rate times affinity, and time refinement of backward
   Euler and BDF2. Require relative atom/inventory drift <1e-9, final Si error
   <1e-3 mol/m3 on the finest time step and orders >0.9 and >1.7.
2. **Spatial precipitation and dissolution.** Start with a smooth silica
   supersaturation gradient in a closed 1 m column. Solve coupled EG aqueous
   transport and P0 mineral mass equations, with counterdiffusing water.
   Compare to an independently coded conservative cell-centered finite-volume
   method-of-lines reference using the same thermodynamic potentials, not
   MOOSE residual code. Require global Si drift <1e-9 relative, decreasing
   profile error with mesh refinement, finest relative profile error <1%,
   positive participating masses, and both mineral growth and loss in space.
   Separately refine time so temporal and spatial errors are not conflated.
   Record cell mass-balance residuals from the discrete numerical facet flux.

All runs record decks, source and executable hashes, pinned framework revision,
commands, return codes, solver logs, raw CSV data, reference solver tolerances,
errors and observations. Failures remain recorded. Figures are generated from
those data. Existing finite-deformation and manufactured-solution checks remain
separate evidence. No experimental validation or full carbonation prediction
is inferred from these tests.

## Delivery gates

Update numerical exposition and actual residual/material map, reproduce the
existing executable and analytical checks, build and inspect the PDF, and
freeze all scientific payload for three independent reviewers. Resolve their
substantiated defects until at least two exact ACCEPTs apply to one snapshot.
Then perform three sequential Foster prose cycles with invariants, rebuilds
and page inspection, followed by fresh independent review if sources changed.
Deliver the PDF and evidence here. This request does not require a new Git
commit, deployment, or release.
