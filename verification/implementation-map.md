# Authorized residual/material traceability

All configurations and symbols are those of the compositional parent. MOOSE implementation was authorized on 7 October 2026. The first table records the governing constitutive contract; the second identifies implemented objects and their verification.

| Governing family | Candidate labels | Source parents | Variables / data | Configuration / differentiation |
|---|---|---|---|---|
| Mechanics residual and traction BC | `eq:weak_momentum`, `eq:reference_momentum` | C `eq:solid_reference_overall_momentum` | u, p̄_f, φ_s, η_f, τ, electric field, P, ρ, W_f, Σ ċ_f^α, gravity, outward traction | Solid reference; include implicit roots, state-dependent Biot, Maxwell stress, reaction resistance and source derivative. |
| Nine aqueous component residuals and flux BCs | `eq:weak_fluid`, `eq:reference_fluid_mass` | C `eq:solid_reference_fluid_component_balance` | p̄_f, three φ_s, eight independent η_f; J, ρ̄_f, η_f^N, W_f, j_f,k^α, νr; prescribed outward mass flux | Solid reference; conservative storage Jφρ̄η. Do not divide residual by a variable density without differentiating the test-weight product. |
| Three pure-solid mass residuals | `eq:weak_solid`, `eq:reference_solid_mass` | C `eq:solid_reference_solid_component_balance` | φ_A,φ_B,φ_C; J, ρ̄_s, ν_sr | Solid reference; no bulk solid relative flux. Mass addition changes storage weights, not the true-mass identity. |
| Transfer residual | `eq:weak_tau`, `eq:tau_evolution` | C `eq:MC_admissible_conversion_component` | τ, v_S; compatible initial τ field | Local in solid reference; one field only, no independent flux BC or per-reaction τ. |
| Gauss residual and electrical BCs | `eq:weak_gauss` | C `eq:gauss_law`, `eq:electrostatic_boundary_conditions` | φ potential (written varphi), η_f,φ_f,ρ̄_f, ε; prescribed potential or outward electric displacement | Solid reference; charge is component-carried. Pure Neumann boundary compatibility and gauge required. |
| Elastic constitutive material/local root | `eq:solid_energy`–`eq:biot_aggregate` | C `eq:MC_solid_stress_definition`, `eq:MC_scalar_distension_stress_restriction`, `eq:MC_phase_biot_coefficient`; matched-log elastic specialization | F, J, p̄_f, φ_s, original intrinsic densities, pure-phase reference energies, elastic moduli | Differentiate off-constraint ψ first, then enforce J̄=ρ̄_0/ρ̄. AD Newton updates include the root response, following the finite-strain companion. |
| Aqueous EOS/potential material | `eq:aqueous_gibbs`–`eq:aqueous_potentials` | C `eq:MC_fluid_pressure_definition`, `eq:MC_absolute_neutral_component_potential` | ρ̄_f or p̄_f, η_f, θ, consistent chemical standard data | Algebraic state response; mass-specific μ, not unconverted molar potentials. |
| Coupled reaction/phase-flux and component-transport material | `eq:reaction_kinetics`, `eq:reaction_force`, `eq:relative_transport`, `eq:reference_flux` | C `eq:MC_onsager_reaction_rate`, `eq:MC_relative_transport_closures`, `eq:solid_reference_relative_flux` | ν,K_(m),ψ,L,τ,∇τ,v_S, phase mass sources, permeability/viscosity, reduced species mobility, electric field | Current forces with reference flux output. Rate and bulk phase flux must be solved consistently; source inversion positivity is not a proof of whole coupled-system uniqueness. |

Implemented FE spaces, time integrators and numerical fluxes are specified below. The full reacting aqueous constitutive block and phase-active-set treatment remain open. Tests of calibrated coupled chemistry and transport, drained/undrained limits and experimental behavior require those closures and separate evidence. Synthetic residual tests establish only the quantities recorded in the executable verification report.

## Implemented residual contract (7 October 2026)

| Object | Equation | Inputs | Verification |
|---|---|---|---|
| `ADReferenceMassStorage` | `eq:weak_fluid`, `eq:weak_solid` | complete AD reference mass and old/older states | nonlinear closed-box mass; variable-step BDF2; coupled FD Jacobian |
| `ADReferenceSpeciesBalance` | `eq:weak_fluid`, `eq:weak_solid` | full reference flux and J-weighted reaction source | pure-solid conservation; EG flux balances |
| `ADCarbonationMomentum` | `eq:weak_momentum` | P, F, J, current mixture density, partial fluid density, current fluid production, W_f, gravity | finite-deformation homogeneous loading; nonzero insertion/gravity cancellation; natural and Maxwell traction; coupled FD Jacobian |
| `ADTransferPotential` | `eq:weak_tau` | AD skeleton velocity | quadratic-in-space exact transfer evolution and off-diagonal displacement derivatives |
| `ADReferenceGauss` | `eq:weak_gauss` | pulled-back dielectric and J-weighted charge | finite deformation with essential and outward-displacement boundaries |
| `ADReferenceOutwardFlux` | `eq:weak_fluid`, `eq:weak_gauss` | outward reference scalar flux | electric boundary-sign MMS |
| `ADReferenceTraction` | `eq:weak_momentum` | outward nominal traction vector | natural-boundary mechanics MMS |
| `ADReferenceMass` | `eq:densities`, `eq:reference_fluid_mass`, `eq:reference_solid_mass` | J, phi, intrinsic density, optional eta | current/old material initialization and nonlinear storage |
| `ADReferencePullback` | `eq:reference_fluid_mass`, `eq:weak_gauss` | J, F inverse, eta, W_f, component-relative current flux, production and charge | deformation-dependent Gauss and reference-source terms |
| `ADLogarithmicMinerals` | `eq:mineral_solve`, `eq:phase_biot`, `eq:total_stress` | F,J,p, phase fractions, branch constants, optional current E | author companion's Newton/AD root; three-mineral roots and Biot coefficient under compression/tension; coupled reference mass/stress Jacobian and Maxwell traction |
| `ADSolidReferenceKinematics`, `ADSkeletonVelocity` | `eq:motion`, `eq:piola_flux`, `eq:weak_tau` | displacement fields in X | coupled finite-deformation test |
| `ADOlivineReconstruction` | discretization of scalar constitutive fields | continuous backbone and optional constant MONOMIAL enrichment | total-field EG L2 error and nonlinear-storage Jacobian |
| `ADEnrichedGalerkin*` | discretization of `eq:weak_fluid` | reconstructed fields, full reference fluxes, diagonal/cross mobility blocks | 1D/2D/3D Poisson reduction; quantitative boundary conservation and L2 convergence |

All kernels assemble on the **undisplaced solid reference mesh**. Material
properties are AD throughout; explicit old states are historical values.
Backward Euler and variable-step BDF2 difference complete reference storage.
Other time integrators are rejected by `ADReferenceMassStorage`. No residual
is divided by a variable phase density or volume fraction.

Continuous scalar fields and P0 enrichment use paired copies of the same
reference storage/source term. For physical nonlinear storage, attach
`ADReferenceMassStorage` to both rows, consuming the same reconstructed mass;
attach `ADReferenceSpeciesBalance` to both rows. Reconstruction and the enrichment-row operators reject nonconstant enrichment. The P0 row has zero broken
volume gradient and obtains its flux from facets. Never replace nonlinear
reference mass with `coefficient * total_field_dot`. The inherited scalar
balance objects' constant-coefficient mode is used only in Poisson verification.

For SPD species-mobility blocks, add diagonal facet fluxes once and then the
signed cross-penalty and adjoint terms for each off-diagonal block. These are
numerical stabilization, not added physical transport laws. Dirichlet backbone
boundaries and weak enrichment boundary terms remove the constant decomposition
mode in the supplied MMS inputs. The local transfer equation uses continuous
Q2 in tests; it has no invented flux or artificial tau anchoring law.

`ADScalarDiffusionReferenceFluxMaterial` is explicitly a **verification
reduction**, not a replacement for the reacting aqueous constitutive block.
Reaction rates, the conversion-corrected fluid resistance, chemical potentials
and species mobilities must be supplied consistently by application materials.
These residual objects make that boundary explicit. They do not claim a
calibrated coupled 17-field carbonation simulation or phase-appearance solver.
