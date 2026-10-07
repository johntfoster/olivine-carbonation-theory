# Synthetic Poisson MMS in 2D: EG value = CG1 + cellwise P0.
[Mesh]
 type = GeneratedMesh
 dim = 2
 nx = 4
 ny = 4
[]
[Variables]
 [p]
 []
 [e]
  family = MONOMIAL
  order = CONSTANT
 []
[]
[AuxVariables]
 [total]
  family = MONOMIAL
  order = SECOND
 []
[]
[AuxKernels]
 [total]
  type = ADMaterialRealAux
  variable = total
  property = total
  execute_on = 'INITIAL TIMESTEP_END'
 []
[]
[Functions]
 [exact]
  type = ParsedFunction
  expression = 'x*(1-x)*y*(1-y)'
 []
 [forcing]
  type = ParsedFunction
  expression = '2*y*(1-y)+2*x*(1-x)'
 []
[]
[Materials]
 [reconstruction]
  type = ADOlivineReconstruction
  backbone = p
  enrichment = e
  value = total
  gradient = gradient
 []
 [flux]
  type = ADScalarDiffusionReferenceFluxMaterial
  backbone = p
  enrichment = e
  diffusivity = 1
  mobility_name = mobility
  reference_flux_name = flux
 []
[]
[Kernels]
 [continuous]
  type = ADEnrichedGalerkinScalarBalance
  variable = p
  enrichment = e
  time_coefficient = 0
  source_function = forcing
  reference_flux_name = flux
 []
 [enriched]
  type = ADEnrichedGalerkinScalarEnrichmentBalance
  variable = e
  backbone = p
  time_coefficient = 0
  source_function = forcing
 []
[]
[DGKernels]
 [flux]
  type = ADEnrichedGalerkinFluxDG
  variable = e
  reference_flux_name = flux
  mobility_name = mobility
  sigma = 12
 []
 [symmetry]
  type = ADEnrichedGalerkinSymmetryDG
  variable = p
  enrichment = e
  mobility_name = mobility
 []
[]
[BCs]
 [continuous]
  type = DirichletBC
  variable = p
  boundary = 'left right bottom top'
  value = 0
 []
 [enriched]
  type = ADEnrichedGalerkinPenaltyBC
  variable = e
  backbone = p
  boundary = 'left right bottom top'
  reference_flux_name = flux
  mobility_name = mobility
  sigma = 12
  value = 0
 []
[]
[Postprocessors]
 [outward_flux]
  type = ADEnrichedGalerkinBoundaryFluxIntegral
  boundary = 'left right bottom top'
  backbone = p
  enrichment = e
  reference_flux_name = flux
  mobility_name = mobility
  sigma = 12
  execute_on = TIMESTEP_END
 []
 [l2]
  type = ElementL2Error
  variable = total
  function = exact
  execute_on = TIMESTEP_END
 []
 [enrichment]
  type = ElementAverageValue
  variable = e
  execute_on = TIMESTEP_END
 []
[]
[Executioner]
 type = Transient
 dt = 1
 num_steps = 1
 solve_type = NEWTON
 nl_abs_tol = 1e-12
 nl_rel_tol = 1e-12
 petsc_options_iname = '-pc_type'
 petsc_options_value = 'lu'
[]
[Outputs]
 csv = true
 file_base = out_eg
[]
