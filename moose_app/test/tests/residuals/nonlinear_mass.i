# Synthetic closed-box reduction: M=p(1+p), dM/dt=1; no physical calibration.
[Mesh]
 type = GeneratedMesh
 dim = 1
 nx = 2
[]
[Variables]
 [p]
  initial_condition = 0.25
 []
[]
[Materials]
 [constants]
  type = ADGenericConstantMaterial
  prop_names = 'J phi source'
  prop_values = '1 1 1'
 []
 [eta]
  type = ADOlivineReconstruction
  backbone = p
  value = eta
  gradient = grad_eta
 []
 [density]
  type = ADParsedMaterial
  coupled_variables = p
  property_name = density
  expression = '1+p'
 []
 [mass]
  type = ADReferenceMass
  jacobian = J
  volume_fraction = phi
  density = density
  mass_fraction = eta
  storage = mass
 []
[]
[Kernels]
 [storage]
  type = ADReferenceMassStorage
  variable = p
  storage = mass
 []
 [source]
  type = ADReferenceSpeciesBalance
  variable = p
  source = source
 []
[]
[Postprocessors]
 [p_average]
  type = ElementAverageValue
  variable = p
 []
[]
[Executioner]
 type = Transient
 scheme = implicit-euler
 solve_type = NEWTON
 dt = 0.1
 num_steps = 5
 nl_abs_tol = 1e-12
 nl_rel_tol = 1e-12
 petsc_options_iname = '-pc_type'
 petsc_options_value = 'lu'
[]
[Outputs]
 csv = true
 file_base = out_mass
[]
