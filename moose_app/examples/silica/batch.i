# Synthetic exact mechanism-(3) reduction; see docs/numerical-verification-plan.md.
[Mesh]
 type = GeneratedMesh
 dim = 1
 nx = 2
[]
[Variables]
 [q]
 []
 [phi_C]
  family = MONOMIAL
  order = CONSTANT
  initial_condition = 0.05
 []
[]
[Functions]
 [q_initial]
  type = ParsedFunction
  expression = '-8.1882549288578215'
 []
[]
[ICs]
 [potential]
  type = FunctionIC
  variable = q
  function = q_initial
 []
[]
[Materials]
 [chemistry]
  type = ADSilicaVerificationChemistry
  potential = q
  solid_fraction = phi_C
  rate_coefficient = 1
  equilibrium_quotient = 0.00013869868505433515
 []
 [constants]
  type = ADGenericConstantMaterial
  prop_names = 'J rho'
  prop_values = '1 1000'
 []
 [fluid_storage]
  type = ADReferenceMass
  jacobian = J
  density = rho
  volume_fraction = fluid_phi
  mass_fraction = silica_eta
  storage = fluid_mass
 []
 [solid_storage]
  type = ADReferenceMass
  jacobian = J
  density = rho
  volume_fraction = silica_phi
  storage = solid_mass
 []
[]
[Kernels]
 [fluid_time]
  type = ADReferenceMassStorage
  variable = q
  storage = fluid_mass
 []
 [fluid_reaction]
  type = ADReferenceSpeciesBalance
  variable = q
  source = silica_fluid_source
 []
 [solid_time]
  type = ADReferenceMassStorage
  variable = phi_C
  storage = solid_mass
 []
 [solid_reaction]
  type = ADReferenceSpeciesBalance
  variable = phi_C
  source = silica_solid_source
 []
[]
[Postprocessors]
 [aq_si]
  type = ADElementIntegralMaterialProperty
  execute_on = 'INITIAL TIMESTEP_END'
  mat_prop = aqueous_silicon
 []
 [solid_mass]
  type = ADElementIntegralMaterialProperty
  execute_on = 'INITIAL TIMESTEP_END'
  mat_prop = solid_mass
 []
 [water]
  type = ADElementIntegralMaterialProperty
  execute_on = 'INITIAL TIMESTEP_END'
  mat_prop = water_moles
 []
 [power]
  type = ADElementIntegralMaterialProperty
  execute_on = 'INITIAL TIMESTEP_END'
  mat_prop = reaction_power
 []
 [rate]
  type = ADElementIntegralMaterialProperty
  execute_on = 'INITIAL TIMESTEP_END'
  mat_prop = silica_rate
 []
 [phi_min]
  type = ADElementExtremeMaterialProperty
  execute_on = 'INITIAL TIMESTEP_END'
  mat_prop = silica_phi
  value_type = min
 []
 [fluid_min]
  type = ADElementExtremeMaterialProperty
  execute_on = 'INITIAL TIMESTEP_END'
  mat_prop = fluid_phi
  value_type = min
 []
[]
[Executioner]
 type = Transient
 scheme = bdf2
 solve_type = NEWTON
 dt = 0.05
 end_time = 40
 nl_abs_tol = 1e-11
 nl_rel_tol = 1e-11
 l_tol = 1e-12
 petsc_options_iname = '-pc_type -snes_linesearch_type'
 petsc_options_value = 'lu bt'
[]
[Outputs]
 csv = true
 file_base = out_batch
[]
