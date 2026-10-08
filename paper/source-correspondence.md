# Equation correspondence: compositional parent → restricted application

The classification is explicit: inherited, specialization, derived, or application. Application entries are constitutive/data choices admitted by the identified parent state/restriction; they are not claimed to be verbatim equations of the parent. Exact source file/line/digest and literal context are in `verification/equation-map.json` and `verification/source-equation-excerpts.json`. All citations resolve against the working-tree manifest in `paper/source-lineage.json`.

| Candidate label | Type | Parent equation labels |
|---|---|---|
| `eq:application_reaction` | application | `C:eq:unified_stoich_current` |
| `eq:densities` | inherited | `C:eq:component_partial_density_representation`, `C:eq:phase_mass_fraction`, `C:eq:volume_fraction_constraint` |
| `eq:motion` | inherited | `C:eq:common_solid_skeleton_motion`, `C:eq:MC_skeleton_rate_convention`, `C:eq:MC_phase_skeleton_transport_identity` |
| `eq:rates` | inherited | `C:eq:common_solid_skeleton_motion`, `C:eq:MC_skeleton_rate_convention`, `C:eq:MC_phase_skeleton_transport_identity` |
| `eq:material_measure` | inherited | `C:eq:augmented_component_material_measure`, `C:eq:reference_conversion_accumulation_rate` |
| `eq:material_rate` | inherited | `C:eq:augmented_component_material_measure`, `C:eq:reference_conversion_accumulation_rate` |
| `eq:zero_sum_flux` | inherited | `C:eq:separate_relative_flux_sum_closure`, `C:eq:averaged_component_spatial_mass` |
| `eq:spatial_component_balance` | inherited | `C:eq:separate_relative_flux_sum_closure`, `C:eq:averaged_component_spatial_mass` |
| `eq:distention` | inherited | `C:eq:MC_solid_distension_decomposition`, `C:eq:MC_scalar_distension_deformation`, `C:eq:MC_solid_true_mass_conservation` |
| `eq:solid_material_mass` | inherited | `C:eq:MC_solid_phase_material_mass`, `C:eq:MC_solid_distension_mass_relation`, `C:eq:MC_solid_distension_evolution` |
| `eq:distention_rate` | inherited | `C:eq:MC_solid_phase_material_mass`, `C:eq:MC_solid_distension_mass_relation`, `C:eq:MC_solid_distension_evolution` |
| `eq:variational_principle` | inherited | `C:eq:vp_principle` |
| `eq:energies` | specialization | `C:eq:T_def`, `C:eq:U_def`, `C:eq:W_def` |
| `eq:virtual_work` | specialization | `C:eq:T_def`, `C:eq:U_def`, `C:eq:W_def` |
| `eq:constraints` | inherited | `C:eq:C1_def`, `C:eq:C2_def`, `C:eq:C3_def`, `C:eq:C4_def` |
| `eq:transfer_variation` | inherited | `C:eq:el_conversion_component`, `C:eq:MC_neutral_component_euler_identity` |
| `eq:component_euler` | inherited | `C:eq:el_conversion_component`, `C:eq:MC_neutral_component_euler_identity` |
| `eq:tau_evolution` | inherited | `C:eq:MC_transfer_work_reference_normalization`, `C:eq:MC_admissible_conversion_component`, `C:eq:MC_transfer_work_full_recovery` |
| `eq:transfer_recovery` | inherited | `C:eq:MC_transfer_work_reference_normalization`, `C:eq:MC_admissible_conversion_component`, `C:eq:MC_transfer_work_full_recovery` |
| `eq:fluid_transfer_offset` | derived | `C:eq:MC_generalized_transfer_phase_offset`, `C:eq:relative_flux_velocity_reconstruction`, `C:eq:MC_admissible_conversion_component` |
| `eq:solid_restrictions` | specialization | `C:eq:MC_phase_pressure_definitions`, `C:eq:MC_scalar_distension_solid_stress`, `C:eq:MC_scalar_distension_stress_restriction` |
| `eq:solid_energy` | application | `C:eq:MC_solid_general_free_energy`, `B:eq:distention-mineral-volumetric-energy` |
| `eq:solid_pressure` | derived | `C:eq:MC_phase_pressure_definitions`, `C:eq:MC_scalar_distension_solid_stress`, `B:eq:matched-energy-density-derivative` |
| `eq:solid_single_prime` | derived | `C:eq:MC_phase_pressure_definitions`, `C:eq:MC_scalar_distension_solid_stress`, `B:eq:matched-energy-density-derivative` |
| `eq:intrinsic_mineral_mean` | derived | `C:eq:MC_solid_stress_definition`, `B:eq:matched-logarithmic-mineral-stress` |
| `eq:electric_closure` | application | `C:eq:electric_field_definitions`, `C:eq:MC_volume_fraction_restrictions`, `C:eq:gauss_law` |
| `eq:pressure_gauss` | application | `C:eq:electric_field_definitions`, `C:eq:MC_volume_fraction_restrictions`, `C:eq:gauss_law` |
| `eq:mineral_solve` | derived | `C:eq:MC_solid_volume_fraction_restriction`, `B:eq:verification-mineral-factors` |
| `eq:phase_biot` | derived | `C:eq:MC_phase_biot_coefficient`, `B:eq:solid-density-eos-tangent` |
| `eq:biot_stress` | inherited | `C:eq:MC_phase_biot_split`, `C:eq:MC_solid_biot_rollup_coefficient`, `C:eq:solid_reference_effective_piola_stress` |
| `eq:biot_aggregate` | inherited | `C:eq:MC_phase_biot_split`, `C:eq:MC_solid_biot_rollup_coefficient`, `C:eq:solid_reference_effective_piola_stress` |
| `eq:total_stress` | inherited | `C:eq:MC_phase_biot_split`, `C:eq:MC_solid_biot_rollup_coefficient`, `C:eq:solid_reference_effective_piola_stress` |
| `eq:linear_limit` | derived | `C:eq:MC_solid_biot_rollup_coefficient`, `B:eq:poroplastic-biot-correction` |
| `eq:aqueous_mole_fractions` | application | `C:eq:MC_fluid_pressure_definition`, `C:eq:MC_absolute_neutral_component_potential` |
| `eq:aqueous_gibbs` | application | `C:eq:MC_fluid_pressure_definition`, `C:eq:MC_absolute_neutral_component_potential` |
| `eq:aqueous_eos` | derived | `C:eq:MC_fluid_pressure_definition`, `C:eq:MC_absolute_neutral_component_potential` |
| `eq:aqueous_helmholtz` | derived | `C:eq:MC_fluid_pressure_definition`, `C:eq:MC_absolute_neutral_component_potential` |
| `eq:aqueous_potentials` | derived | `C:eq:MC_fluid_pressure_definition`, `C:eq:MC_absolute_neutral_component_potential` |
| `eq:solid_potential` | specialization | `C:eq:MC_neutral_component_euler_identity`, `C:eq:MC_absolute_neutral_component_potential` |
| `eq:mechanisms` | application | `C:eq:unified_stoich_current`, `C:eq:mechanism_charge_conservation` |
| `eq:mechanism_conservation` | derived | `C:eq:unified_stoich_current`, `C:eq:material_increment_insertion_constraint`, `C:eq:mechanism_charge_conservation` |
| `eq:reaction_kinetics` | specialization | `C:eq:MC_onsager_reaction_rate`, `C:eq:MC_affinity_projection`, `C:eq:MC_reaction_power_local_thermal_equilibrium` |
| `eq:affinity` | specialization | `C:eq:MC_onsager_reaction_rate`, `C:eq:MC_affinity_projection`, `C:eq:MC_reaction_power_local_thermal_equilibrium` |
| `eq:reaction_force` | specialization | `C:eq:MC_onsager_reaction_rate`, `C:eq:MC_affinity_projection`, `C:eq:MC_reaction_power_local_thermal_equilibrium` |
| `eq:speciation` | derived | `C:eq:MC_affinity_projection`, `C:eq:MC_onsager_reaction_rate` |
| `eq:relative_transport` | specialization | `C:eq:MC_diffusion_closure`, `C:eq:MC_dispersion_closure`, `C:eq:MC_relative_transport_closures` |
| `eq:charge_balance` | inherited | `C:eq:charge_current_density_definition`, `C:eq:mixture_charge_balance` |
| `eq:fluid_momentum` | specialization | `C:eq:el_mom_f_dynamic_capillary` |
| `eq:drag` | inherited | `C:eq:relative_mass_flux_definition`, `C:eq:fluid_phase_interaction_law` |
| `eq:flux_linear_system` | specialization | `C:eq:relative_flux_linear_system`, `C:eq:modified_relative_flux_permeability` |
| `eq:corrected_mobility` | specialization | `C:eq:relative_flux_linear_system`, `C:eq:modified_relative_flux_permeability` |
| `eq:resistance_domain` | inherited | `C:eq:modified_relative_flux_positive_resistance_condition` |
| `eq:darcy_limit` | specialization | `C:eq:standard_darcy_mass_flux_limit` |
| `eq:overall_momentum` | derived | `C:eq:MC_overall_momentum_nonlinear_biot`, `C:eq:material_increment_insertion_constraint` |
| `eq:dissipation` | specialization | `C:eq:MC_onsager_reaction_transport_dissipation`, `C:eq:MC_interphase_exchange_positive` |
| `eq:piola_flux` | inherited | `C:eq:reference_relative_mass_flux`, `C:eq:pulled_back_modified_permeability`, `C:eq:solid_reference_flux_divergence` |
| `eq:reference_flux` | specialization | `C:eq:solid_reference_relative_flux` |
| `eq:reference_fluid_mass` | specialization | `C:eq:solid_reference_fluid_component_balance`, `C:eq:solid_reference_solid_component_balance` |
| `eq:reference_solid_mass` | specialization | `C:eq:solid_reference_fluid_component_balance`, `C:eq:solid_reference_solid_component_balance` |
| `eq:reference_total_mass` | derived | `C:eq:solid_reference_fluid_component_balance`, `C:eq:solid_reference_solid_component_balance` |
| `eq:reference_momentum` | specialization | `C:eq:solid_reference_overall_momentum` |
| `eq:weak_fluid` | derived | `C:eq:solid_reference_fluid_component_balance` |
| `eq:weak_solid` | derived | `C:eq:solid_reference_solid_component_balance`, `C:eq:MC_admissible_conversion_component`, `C:eq:solid_reference_overall_momentum` |
| `eq:weak_tau` | derived | `C:eq:solid_reference_solid_component_balance`, `C:eq:MC_admissible_conversion_component`, `C:eq:solid_reference_overall_momentum` |
| `eq:weak_momentum` | derived | `C:eq:solid_reference_solid_component_balance`, `C:eq:MC_admissible_conversion_component`, `C:eq:solid_reference_overall_momentum` |
| `eq:weak_gauss` | derived | `C:eq:gauss_law`, `C:eq:electrostatic_boundary_conditions` |
| `eq:discrete_euler` | application | `C:eq:solid_reference_fluid_component_balance`, `C:eq:solid_reference_solid_component_balance` |
| `eq:discrete_bdf` | application | `C:eq:solid_reference_fluid_component_balance`, `C:eq:solid_reference_solid_component_balance` |
| `eq:eg_space` | application | `C:eq:solid_reference_fluid_component_balance` |
| `eq:eg_flux` | application | `C:eq:solid_reference_fluid_component_balance` |
| `eq:eg_residual` | application | `C:eq:solid_reference_fluid_component_balance` |
| `eq:silica_rate` | derived | `C:eq:MC_onsager_reaction_rate`, `C:eq:MC_affinity_projection`, `C:eq:MC_absolute_neutral_component_potential` |
| `eq:silica_coordinate` | derived | `C:eq:MC_absolute_neutral_component_potential`, `C:eq:MC_relative_transport_closures` |
| `eq:silica_diffusion` | derived | `C:eq:MC_absolute_neutral_component_potential`, `C:eq:MC_relative_transport_closures` |
| `eq:silica_extent` | derived | `C:eq:solid_reference_fluid_component_balance`, `C:eq:solid_reference_solid_component_balance` |

## Restrictions

C phase sets become S={A,B,C}, F={f}; pure solid components, one aqueous phase; common constant temperature; identity plastic and stress-free maps; scalar distention. S_f=1 and γ=0 remove interfluid capillarity/history/saturation processes. Charged aqueous components retain source electrical enthalpy, specific charge, electrochemical transport and Gauss law. C mass and charge sources, material increments, τ/L normalization, insertion force, resistance shift, pressure/volume multipliers, scalar distention restriction and Biot transforms remain. The common-permittivity and additive matched-log/ideal-mixture free energies are declared application constitutive choices. No other paper supplies a competing τ or mass/transport law.
