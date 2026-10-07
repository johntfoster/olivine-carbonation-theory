# Homogeneous finite-deformation elastic branch; synthetic constants.
[Mesh]
 type = GeneratedMesh
 dim = 1
 nx = 4
 elem_type = EDGE3
[]
[Variables]
 [u]
  order = SECOND
 []
 [p]
  initial_condition = 0.2
 []
 [phi]
  initial_condition = 0.3
 []
 [tau]
  order = SECOND
 []
 [potential]
  order = SECOND
 []
[]
[Functions]
 [motion]
  type = ParsedFunction
  expression = '0.1*t*x'
 []
 [tau_exact]
  type = ParsedFunction
  expression = '0.005*t*x*x'
 []
 [electric_exact]
  type = ParsedFunction
  expression = '(1+0.1*t)^2*x*(1-x)/4'
 []
[]
[Materials]
 [kinematics]
  type = ADSolidReferenceKinematics
  displacements = u
 []
 [velocity]
  type = ADSkeletonVelocity
  displacements = u
  velocity = velocity
 []
 [pressure]
  type = ADOlivineReconstruction
  backbone = p
  value = pressure
  gradient = grad_pressure
 []
 [constants]
  type = ADGenericConstantMaterial
  prop_names = 'rho_f rho source eta charge'
  prop_values = '1 1 0 1 1'
 []
 [vectors]
  type = ADGenericConstantVectorMaterial
  prop_names = 'W j traction'
  prop_values = '0 0 0 0 0 0 0 0 0'
 []
 [solid_fraction]
  type = ADOlivineReconstruction
  backbone = phi
  value = solid_phi
  gradient = grad_solid_phi
 []
 [mass]
  type = ADReferenceMass
  jacobian = solid_reference_J
  volume_fraction = solid_phi
  density = density
  storage = solid_mass
 []
 [mineral]
  type = ADLogarithmicMinerals
  deformation_gradient = solid_reference_F
  jacobian = solid_reference_J
  pressure = pressure
  volume_fractions = solid_phi
  reference_fractions = 0.3
  reference_densities = 3
  allocated_bulk_moduli = 1
  mineral_bulk_moduli = 20
  shear_moduli = 2
  densities = density
  mineral_jacobians = mineral_J
  stress = P
  biot = B
 []
 [pullback]
  type = ADReferencePullback
  jacobian = solid_reference_J
  inverse_deformation_gradient = solid_reference_F_inv
  mass_fraction = eta
  current_source = source
  current_charge = charge
  bulk_reference_flux = W
  relative_current_flux = j
  permittivity = 2
  reference_flux = species_flux
  reference_source = reference_source
  reference_charge = reference_charge
  dielectric = dielectric
 []
[]
[Kernels]
 [solid_storage]
  type = ADReferenceMassStorage
  variable = phi
  storage = solid_mass
 []
 [solid_source]
  type = ADReferenceSpeciesBalance
  variable = phi
  source = reference_source
 []
 [momentum]
  type = ADCarbonationMomentum
  variable = u
  component = 0
  stress = P
  deformation_gradient = solid_reference_F
  jacobian = solid_reference_J
  density = rho
  fluid_density = rho_f
  fluid_production = source
  relative_flux = W
 []
 [pressure]
  type = ADTimeDerivative
  variable = p
 []
 [tau]
  type = ADTransferPotential
  variable = tau
  skeleton_velocity = velocity
 []
 [gauss]
  type = ADReferenceGauss
  variable = potential
  dielectric = dielectric
  charge = reference_charge
 []
[]
[BCs]
 [motion]
  type = FunctionDirichletBC
  variable = u
  boundary = 'left right'
  function = motion
 []
 [electric]
  type = DirichletBC
  variable = potential
  boundary = 'left right'
  value = 0
 []
[]
[Postprocessors]
 [u_l2]
  type = ElementL2Error
  variable = u
  function = motion
  execute_on = TIMESTEP_END
 []
 [tau_l2]
  type = ElementL2Error
  variable = tau
  function = tau_exact
  execute_on = TIMESTEP_END
 []
 [electric_l2]
  type = ElementL2Error
  variable = potential
  function = electric_exact
  execute_on = TIMESTEP_END
 []
[]
[Executioner]
 type = Transient
 scheme = implicit-euler
 dt = 0.1
 num_steps = 3
 solve_type = NEWTON
 nl_abs_tol = 1e-12
 nl_rel_tol = 1e-12
 petsc_options_iname = '-pc_type'
 petsc_options_value = 'lu'
[]
[Outputs]
 csv = true
 file_base = out_mechanics
[]
