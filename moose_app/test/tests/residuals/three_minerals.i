!include mechanics.i
[Variables]
 [phi]
  initial_condition := 0.15
 []
 [phi_B]
  initial_condition = 0.1
 []
 [phi_C]
  initial_condition = 0.05
 []
[]
[Materials]
 [mineral]
  volume_fractions := 'solid_phi phiB phiC'
  reference_fractions := '0.15 0.1 0.05'
  reference_densities := '3 4 5'
  allocated_bulk_moduli := '0.5 0.3 0.1'
  mineral_bulk_moduli := '20 30 40'
  shear_moduli := '2 3 4'
  densities := 'density densityB densityC'
  mineral_jacobians := 'mineral_J bB bC'
 []
 [fraction_B]
  type = ADOlivineReconstruction
  backbone = phi_B
  value = phiB
  gradient = grad_phiB
 []
 [mass_B]
  type = ADReferenceMass
  jacobian = solid_reference_J
  volume_fraction = phiB
  density = densityB
  storage = massB
 []
 [fraction_C]
  type = ADOlivineReconstruction
  backbone = phi_C
  value = phiC
  gradient = grad_phiC
 []
 [mass_C]
  type = ADReferenceMass
  jacobian = solid_reference_J
  volume_fraction = phiC
  density = densityC
  storage = massC
 []
[]
[Kernels]
 [storage_B]
  type = ADReferenceMassStorage
  variable = phi_B
  storage = massB
 []
 [source_B]
  type = ADReferenceSpeciesBalance
  variable = phi_B
  source = reference_source
 []
 [storage_C]
  type = ADReferenceMassStorage
  variable = phi_C
  storage = massC
 []
 [source_C]
  type = ADReferenceSpeciesBalance
  variable = phi_C
  source = reference_source
 []
[]
[AuxVariables]
 [rootA]
  family = MONOMIAL
  order = CONSTANT
 []
 [rootB]
  family = MONOMIAL
  order = CONSTANT
 []
 [rootC]
  family = MONOMIAL
  order = CONSTANT
 []
 [biot]
  family = MONOMIAL
  order = CONSTANT
 []
[]
[AuxKernels]
 [rootA]
  type = ADMaterialRealAux
  variable = rootA
  property = mineral_J
  execute_on = TIMESTEP_END
 []
 [rootB]
  type = ADMaterialRealAux
  variable = rootB
  property = bB
  execute_on = TIMESTEP_END
 []
 [rootC]
  type = ADMaterialRealAux
  variable = rootC
  property = bC
  execute_on = TIMESTEP_END
 []
 [biot]
  type = ADMaterialRealAux
  variable = biot
  property = B
  execute_on = TIMESTEP_END
 []
[]
[Postprocessors]
 [rootA]
  type = ElementAverageValue
  variable = rootA
  execute_on = TIMESTEP_END
 []
 [rootB]
  type = ElementAverageValue
  variable = rootB
  execute_on = TIMESTEP_END
 []
 [rootC]
  type = ElementAverageValue
  variable = rootC
  execute_on = TIMESTEP_END
 []
 [biot]
  type = ElementAverageValue
  variable = biot
  execute_on = TIMESTEP_END
 []
[]
