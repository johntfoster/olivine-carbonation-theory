# Source contract for the foundational rebuild

Status: source contract implemented in the candidate; independent source-fidelity review and acceptance remain pending. The contract milestone was delivered before manuscript rewriting. The rejected manuscript, its transfer network, and all 358 historical checks are excluded from the scientific foundation. Source IDs below denote actual author-owned LaTeX, not summaries or imported internet formulations.

## Hierarchy and exact-byte provenance

John’s controlling clarification (Telegram 7418): this problem is a SPECIAL CASE of the compositional paper and must use its notation. C = compositional manuscript: the sole governing parent formulation for phase/component variables, variation, transfer work, stress, thermodynamic restrictions and reference balances. R = three-phase reacting mixture: originating distention construction and reacting flux. F = four-phase manuscript: supporting extension, NOT the phase inventory for this application (its gas phase is excluded). B = finite-strain Biot manuscript: elastic, isotropic matched-logarithmic mineral/skeleton energy only; no plastic flow is imported. Read root/macros and the relevant equation neighborhoods; unrelated plastic and implementation sections are not governing sources. Original paths in the manifest are resolved paths. Exact-byte copies are also provided under `verification/parent-sources/` for portable independent inspection; these are provenance snapshots, not replacement governing sources or imported implementation code. SHA-256 values identify actual inspected working-tree bytes and remain authoritative even when HEAD differs.

## Source notation retained

| Symbol | Meaning and source |
|---|---|
| `ξ ∈ S ∪ F`, `s ∈ S`, `f ∈ F`, `α` | Phase, solid, fluid, component indices; C `sec:virtual_power_derivation`. Here S={A,B,C}: forsterite, magnesite, silica; F={f}: aqueous only. The solid label C is not the source-ID C. Each solid is a pure component phase; α indexes aqueous chemical species as components of its mass balance. |
| `ρ_ξ^α`, `ρ_ξ`, `ρ̄_ξ`, `η_ξ^α`, `φ_ξ` | Partial component density, partial phase density, intrinsic phase density, mass fraction, current volume fraction; C `eq:component_partial_density_representation`, `eq:phase_partial_density_representation`, `eq:phase_mass_fraction`. All mass densities remain kg/m³; no replacement by mole inventories. |
| `F`, `J`, `X`, `v_S`, heavy dot | Common skeleton deformation, determinant, reference coordinate, velocity and skeleton rate; C `eq:common_solid_skeleton_motion`, `eq:MC_skeleton_rate_convention`. Ordinary dot follows the indexed phase. |
| `A_s`, `a_s`, `F̄_s`, `J̄_s` | Distention map/determinant and true deformation/determinant; C `eq:MC_solid_distension_decomposition`. R calls the determinant `α_s`; C's `a_s` governs here. |
| `C_ξ^α`, `ċ_ξ^α` | Reference accumulated material increment and its current-volume rate; C `eq:augmented_component_material_measure`, `eq:reference_conversion_accumulation_rate`. The increment includes relative-transport divergence; net phase sum equals conversion. R's `c_ξ^+` maps to `Σ_α ċ_ξ^α`, not to a molar rate. |
| `ν_{ξ(m)}^α`, `r_(m)` | Mass-based stoichiometric coefficient and current-volume reaction progress. With molar progress, ν includes molar mass. C `eq:unified_stoich_current`. |
| `τ`, `L_ξ^α`, `π_ξ^α`, `Π_ξ`, `λ` | One global transfer potential; mass-specific generalized transfer work; material-storage, mass-fraction, volume multipliers. C `eq:C1_def`–`eq:C4_def`, `eq:W_def`. τ is action/mass; L is energy/mass. No independent τ per reaction. |
| `ψ_ξ`, `μ̂_ξ^α`, `μ_ξ^α`, `z_ξ^α` | Specific Helmholtz, mass-specific neutral/electrochemical potentials, specific charge (C/kg, NOT charge number); C `eq:MC_absolute_neutral_component_potential`, `eq:C45_combined_def`. Molar activity formulas multiply μ̂ by species molar mass. |
| `w_f`, `W_f`, `λ̃_f`, `Λ̃_f` | Current/reference relative mass flux and corrected mobilities; C `eq:relative_mass_flux_definition`, `eq:reference_relative_mass_flux`, `eq:modified_relative_flux_permeability`, `eq:pulled_back_modified_permeability`. |
| `σ_s′`, `σ_s″`, `B̄_s`, `B` | Partial fixed-density/fixed-pressure stresses, intrinsic phase and aggregate Biot coefficient. C `eq:MC_phase_biot_split`, `eq:MC_solid_biot_rollup_coefficient`. B is not an arbitrary pressure multiplier. |

The author’s C `defs.tex` will be copied without modifications and used by the new root; only problem-specific symbols are declared separately. All reference/current mass factors and held-fixed derivatives are explicit.

## General compositional equation → restrictions → specialized equation

Apply `S={A,B,C}`, `F={f}`, one component in each solid, nine aqueous species, `S_f=1`, `γ=0`, common constant `θ`, all plastic/stress-free factors equal to identity. Capillary, saturation-rate, thermal-gradient and plastic terms vanish; material insertion, τ, L, component diffusion, compressible true-solid volumes and pressure transformations remain. For ionic chemistry, retain the parent electrical fields and Gauss law rather than silently discarding charge coupling.

## Equation inheritance and specialization contract

| New block | Exact source labels | Category / required operation |
|---|---|---|
| Densities, fractions, phase material increment | C `eq:phase_mass_fraction`, `eq:component_partial_density_representation`, `eq:augmented_component_material_measure` | Inherited; retain phase reference J_ξ distinct from common solid J. |
| Component balances and zero-sum relative transport | C `eq:averaged_component_spatial_mass`, `eq:reference_conversion_accumulation_rate`, `eq:separate_relative_flux_sum_closure` | Inherited; pure solids have no component-relative flux. |
| Mass production and atom/charge conservation | C `eq:unified_stoich_current`, `eq:material_increment_insertion_constraint`; `sections/conservation_of_charge.tex` | Derived application stoichiometry in kg/mol times current molar progress; preserve total mass and charge identities. |
| Distention and reacted material amount | C `eq:MC_solid_phase_material_mass`, `eq:MC_solid_true_mass_conservation`, `eq:MC_solid_distension_mass_relation`, `eq:MC_solid_distension_evolution` | Inherited, compressible solids; a_s is not J and J̄_s not 1. |
| Hamilton–d’Alembert statement and insertion coefficient | C `eq:vp_principle`, `eq:W_def`, `eq:C1_def`–`eq:C4_def`, `eq:deltaT_app`, `eq:el_conversion_component` | Inherited; show cancellation of recipient ψ storage against insertion supply ψ+L, leaving L in variation. |
| Component potential and transfer closure | C `eq:MC_neutral_component_euler_identity`, `eq:MC_transfer_work_component_difference`, `eq:MC_transfer_work_full_recovery`, `eq:MC_transfer_work_reference_normalization`, `eq:MC_admissible_conversion_component` | Inherited current compositional normalization; discrepancy with R/F explicitly recorded below. |
| Constitutive pressure, stress and scalar distention trace | C `eq:MC_phase_pressure_definitions`, `eq:MC_solid_stress_definition`, `eq:MC_scalar_distension_stress_restriction`, `eq:MC_volume_fraction_restrictions` | Inherited one-fluid mechanically nonpolar specialization; scalar energy must satisfy BOTH stress and distention trace restrictions. |
| Logarithmic mineral/skeleton energy | B `eq:distention-mineral-volumetric-energy`, `eq:verification-mineral-factors`, `eq:matched-logarithmic-mineral-stress` | Derived additive three-solid specialization, weighted by current reacted reference masses; single-solid nonreacting reduction must be exact. Species mechanical allocation is an application closure, not a source theorem. |
| Biot derivative and pressure split | C `eq:MC_phase_biot_coefficient`, `eq:MC_phase_biot_split`, `eq:MC_solid_biot_rollup_coefficient`; B `eq:solid-density-eos-tangent`, `eq:poroplastic-biot-correction` (elastic only) | Derived local scalar roots/tangents; fixed current solid masses. Do not identify drained finite-pressure multiplier with B. |
| Phase insertion momentum and bulk fluid flux | C `eq:el_mom_f_dynamic_capillary`, `eq:relative_flux_linear_system`, `eq:generalized_fluid_darcy_mass_flux`, `eq:modified_relative_flux_positive_resistance_condition`; R `eq:fluid_momentum`, `eq:reacting_flux`; F `eq:darcy_flux` | Inherited single-fluid zero-capillarity specialization, including electrical terms for ionic aqueous species. Retain both ċ_f ∇τ and ċ_f I in resistance. No donor normalization. |
| Overall momentum | C `eq:MC_overall_momentum_nonlinear_biot`, `eq:solid_reference_overall_momentum` | Derived single fluid: global ∇τ term cancels by total mass balance; residual −ċ_f(v_f−v_S) remains. |
| Reference species and solid balances | C `eq:solid_reference_fluid_component_balance`, `eq:solid_reference_solid_component_balance`, `eq:solid_reference_flux_divergence` | Inherited; weak forms derived by integration by parts, including outward-flux and traction signs. |
| Reaction dissipation and kinetics | C `eq:MC_reaction_power_local_thermal_equilibrium`, `eq:MC_onsager_reaction_rate`, `eq:MC_onsager_reaction_transport_dissipation` | Inherited; phase-changing reactions keep transfer-work offsets and cannot replace source force by bare affinity without proof. |
| Molecular diffusion/dispersion | C `eq:MC_dispersion_closure`, `eq:MC_diffusion_closure`, `eq:MC_relative_transport_closures` | Isothermal reduction, N−1 mass-fraction directions, separate zero sum. Electrical enthalpy, Gauss law and charge-force terms retained if ions are tracked; electroneutrality is not silently imposed. |
| Aqueous chemistry and fluid density | C `eq:MC_fluid_pressure_definition`, `eq:MC_absolute_neutral_component_potential`, `eq:MC_affinity_projection` | Application-only integrable aqueous free energy: specific ψ_f supplies both EOS and mass-specific component potentials. Activities/speciation and equilibrium constants never replace mixture mechanics. |
| Weak forms / future implementation map | C reference balance labels above; R `eq:weak_mom` as ancestry only | Derived residuals; no implementation, numerical solution or convergence claim. |

## Actual source differences that cannot be hidden by notation

1. **Transfer-work normalization differs materially.** C `eq:MC_transfer_work_reference_normalization` sets ψ_s*+L_s*^N=μ̂_s*^N. Combined with its Euler identity this gives D_S τ/Dt=|v_S|²/2 (`eq:MC_admissible_conversion_component`). R `eq:LA` instead specifies L_A=φ_A ∂ψ_A^dis/∂φ−ψ_A, leading to `eq:tau_final`; F `eq:tau_evolution` has the corresponding law. Even with porosity-independent energy, R/F give D_S τ/Dt=|v_S|²/2−ψ_A−p/ρ̄_A, not the C normalization. These are different transfer-work prescriptions, not constant gauges: their difference can vary in space. The rebuild follows the explicitly primary C normalization and carries its L offsets into reaction dissipation. It must not claim spatial chemistry generates τ under stationary-skeleton C normalization, or claim the full R/F τ evolution as a limit. The author has unequivocally selected the compositional parent; the older normalization is therefore NOT imported and no author choice or interpolating law is needed.
2. **Volume-multiplier sign.** R uses λ=+p+p_φ* and −λ/ρ̄_A in τ; F uses λ=−p−P_φ* and +λ/ρ̄_A. Both give −p/ρ̄_A in the porosity-independent limit. C uses λ=−p in the neutral one-fluid limit. Symbols must be mapped by physical pressure rather than copied with a changed sign.
3. **A Piola typo in R is not inherited.** Immediately following R `eqn:final_momentum` an unnumbered display prints P′=Jσ′F^T. The flux/traction transformation and C `eq:solid_reference_effective_piola_stress` require F^(−T). The rebuild uses the latter and checks virtual work and Nanson traction.
4. **Constitutive scope.** R/F assume incompressible solids and some porosity-dependent distention examples. The current scope is compressible solids using B's matched logarithmic law. The general C kinematics/pressure derivative permit this; one cannot append old porosity-conjugate stress terms when the selected ψ has no independent φ argument.
5. **Phase count.** F's four phases are two solids plus liquid plus gas. The application has three solids plus a single multicomponent aqueous fluid. Only its variational lineage is inherited, not gas saturation or capillary closures.

## Discarded deviations from rejected candidate

Delete the governing mole-inventory replacement (`n_i`, `a_α`, `q_i`, `z_i` as primary phase variables), independently postulated network τ fields, donor-weighted/normalized transfer terms, and artificial paired-power reaction corrections. Do not preserve their purported verification by translating variable names. Existing chemical reaction stoichiometry can be independently rechecked but must enter C's ν r mass sources. The source corrected resistance and insertion force, material increment, L potentials, pressure multipliers and fixed-pressure Biot definition must be explicit, not bibliography-only ancestry.

## Execution and honest verification

Following the contract checkpoint, the root and source correspondence were rewritten from scratch and C macros imported byte-for-byte. The following completion requirements govern the candidate. Derive three pure-solid matched-log energies by specialization of C constitutive state, preserving true mass identity and scalar-distention trace; derive current/reference mechanics and species balance residuals. Derive chemistry from one phase potential and keep application assumptions separate. Run new exact conservation, unit, stress/pressure derivative, Piola, transfer normalization/offset, source-limit and dissipation checks. Record run command, source hashes, tolerances and observed residuals. No historical 358 checks, source manuscript benchmark result, or reviewer acceptance is a result for this rebuild. PDF build/render inspection is document QA only.

## Exact inspected source hashes

- C `main.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/main.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `c3851aeb803b6171213975cdf5370c7a06fe74d53f91fa1b04bfeb14becbc2fc`
- C `defs.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/defs.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `eb99bfa85b9d27aa952c0c9b5a380a0dc8d4f99c44ba4e83a3cc2b42ae707130`
- C `sections/material_mass.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/sections/material_mass.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `181a44f957610a03dc89935a61bc11f062b71ba0c120e1e993d29340340b45db`
- C `sections/virtual_power_derivation.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/sections/virtual_power_derivation.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `af58b4477c4beb49f80ab168711f20be7d65f91b97c5e9ece3cfae878cc59dcb`
- C `sections/multicomponent_solids.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/sections/multicomponent_solids.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `c98ca183efbbac67ea25ccc273e9847f4eb78528ec32ebe8f60a2d761d79fb6f`
- C `sections/pulled_back_solid_skeleton.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/sections/pulled_back_solid_skeleton.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `2c57eace708a0a5ac69d9ec1970a38d7645a21e2db34e73ffaa8b73d0034bddd`
- C `sections/technical_setting.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/sections/technical_setting.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `e763dc62db966281517c860381b5e5005269695f43cccfc89ea6159d0d393868`
- C `sections/appendix_component_potential_derivation.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/sections/appendix_component_potential_derivation.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `788a8a1c2265dd9d5018d302ad67c5cb065e0e23019c6a03b8e1a14293e3508c`
- C `sections/conservation_of_charge.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow/sections/conservation_of_charge.tex`
  - HEAD: `ae51da21b52ffc2ec382dcc286f7a1b2bfdf9c92`
  - SHA-256: `f3b8e13e1bec27b205a3104db818870dc763c5780aa62c1fd26246c725b44d3b`
- R `main.tex`
  - Resolved: `/home/jfoster/Documents/LaTeX/ReactingMixture/main.tex`
  - HEAD: `b60e73b3437e3140e1011c4b19e1c6e30575831f`
  - SHA-256: `89007bd26a8b842deaad873a2d8b3a472ad620c77b62a3b5686325cf2bc5ad29`
- R `defs.tex`
  - Resolved: `/home/jfoster/Documents/LaTeX/ReactingMixture/defs.tex`
  - HEAD: `b60e73b3437e3140e1011c4b19e1c6e30575831f`
  - SHA-256: `55f0e9e3a9d93c65fb19af3a2989088c74904eb9ef6653a1558dd5e1601276dc`
- F `main.tex`
  - Resolved: `/home/jfoster/Documents/LaTeX/FourPhaseReactingMixture/main.tex`
  - HEAD: `549f1c92b56976288ac08719c58e3660e97cdb85`
  - SHA-256: `6592f68c358edeaa6f853695af57ad555c4fa467376168727ec6469844239204`
- F `defs.tex`
  - Resolved: `/home/jfoster/Documents/LaTeX/FourPhaseReactingMixture/defs.tex`
  - HEAD: `549f1c92b56976288ac08719c58e3660e97cdb85`
  - SHA-256: `2f1fff9e1224ea8460c0e43f923238092aebe88b436d725461bc88248097ab88`
- F `variational_principle_appendix.tex`
  - Resolved: `/home/jfoster/Documents/LaTeX/FourPhaseReactingMixture/variational_principle_appendix.tex`
  - HEAD: `549f1c92b56976288ac08719c58e3660e97cdb85`
  - SHA-256: `8be4af7ad016377b329548835dc4998f1a9b8d1c52fdd15d4bbe533082d6bcb4`
- F `coleman_noll_appendix.tex`
  - Resolved: `/home/jfoster/Documents/LaTeX/FourPhaseReactingMixture/coleman_noll_appendix.tex`
  - HEAD: `549f1c92b56976288ac08719c58e3660e97cdb85`
  - SHA-256: `5d86733ed7f5d3f4954851c3e25e481ec254cd70798e23679722ab6842d8c6f1`
- B `paper/main.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/finite-strain-biot-poromechanics/paper/main.tex`
  - HEAD: `9e469c871ccf833287771e447b90761cc5c5ab03`
  - SHA-256: `345ab5bd044c15db36405eeafcafa09202bb0ea2ff05c18d96406e9c447f6c3b`
- B `paper/defs.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/finite-strain-biot-poromechanics/paper/defs.tex`
  - HEAD: `9e469c871ccf833287771e447b90761cc5c5ab03`
  - SHA-256: `2ce1a86d727aa30144fa7fa620c6cabd15d0663d5c7a6e66e839055fbe085ab4`
- B `paper/sections/finite_deformation_biot.tex`
  - Resolved: `/home/jfoster/projects/research/reactive_transport/finite-strain-biot-poromechanics/paper/sections/finite_deformation_biot.tex`
  - HEAD: `9e469c871ccf833287771e447b90761cc5c5ab03`
  - SHA-256: `95d84b7a27bc9d151f384e059dd4dd52a4bedb467b42b106165ba5f38d922bce`
