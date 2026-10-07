[Mesh]
 type = GeneratedMesh
 dim = 1
 nx = 8
[]
[Variables]
 [p]
 []
 [q]
 []
 [ep]
  family = MONOMIAL
  order = CONSTANT
 []
 [eq]
  family = MONOMIAL
  order = CONSTANT
 []
[]
[AuxVariables]
 [pt]
  family = MONOMIAL
  order = SECOND
 []
 [qt]
  family = MONOMIAL
  order = SECOND
 []
[]
[Functions]
 [p_exact]
  type = ParsedFunction
  expression = 'x*(1-x)'
 []
 [q_exact]
  type = ParsedFunction
  expression = '2*x*(1-x)'
 []
[]
[Materials]
 [flux]
  type = ADCrossDiffusionVerification
  p = p
  q = q
 []
 [p_reconstruction]
  type = ADOlivineReconstruction
  backbone = p
  enrichment = ep
  value = pt
  gradient = grad_p
 []
 [q_reconstruction]
  type = ADOlivineReconstruction
  backbone = q
  enrichment = eq
  value = qt
  gradient = grad_q
 []
[]
[AuxKernels]
 [p_total]
  type = ADMaterialRealAux
  variable = pt
  property = pt
  execute_on = TIMESTEP_END
 []
 [q_total]
  type = ADMaterialRealAux
  variable = qt
  property = qt
  execute_on = TIMESTEP_END
 []
[]
[Kernels]
 [p_continuous]
  type = ADEnrichedGalerkinScalarBalance
  variable = p
  enrichment = ep
  time_coefficient = 0
  source_function = 3
  reference_flux_name = flux_p
 []
 [p_enriched]
  type = ADEnrichedGalerkinScalarEnrichmentBalance
  variable = ep
  backbone = p
  time_coefficient = 0
  source_function = 3
 []
 [q_continuous]
  type = ADEnrichedGalerkinScalarBalance
  variable = q
  enrichment = eq
  time_coefficient = 0
  source_function = 8.5
  reference_flux_name = flux_q
 []
 [q_enriched]
  type = ADEnrichedGalerkinScalarEnrichmentBalance
  variable = eq
  backbone = q
  time_coefficient = 0
  source_function = 8.5
 []
[]
[DGKernels]
 [p_flux]
  type = ADEnrichedGalerkinFluxDG
  variable = ep
  reference_flux_name = flux_p
  mobility_name = Dpp
  sigma = 12
 []
 [p_symmetry]
  type = ADEnrichedGalerkinSymmetryDG
  variable = p
  enrichment = ep
  mobility_name = Dpp
 []
 [p_cross_flux]
  type = ADEnrichedGalerkinCrossFluxDG
  variable = ep
  column_enrichment = eq
  cross_mobility_name = Dpq
  sigma = 12
 []
 [p_cross_symmetry]
  type = ADEnrichedGalerkinCrossSymmetryDG
  variable = p
  column_enrichment = eq
  cross_mobility_name = Dpq
 []
 [q_flux]
  type = ADEnrichedGalerkinFluxDG
  variable = eq
  reference_flux_name = flux_q
  mobility_name = Dqq
  sigma = 12
 []
 [q_symmetry]
  type = ADEnrichedGalerkinSymmetryDG
  variable = q
  enrichment = eq
  mobility_name = Dqq
 []
 [q_cross_flux]
  type = ADEnrichedGalerkinCrossFluxDG
  variable = eq
  column_enrichment = ep
  cross_mobility_name = Dpq
  sigma = 12
 []
 [q_cross_symmetry]
  type = ADEnrichedGalerkinCrossSymmetryDG
  variable = q
  column_enrichment = ep
  cross_mobility_name = Dpq
 []
[]
[BCs]
 [p_continuous]
  type = DirichletBC
  variable = p
  boundary = 'left right'
  value = 0
 []
 [p_enrichment]
  type = ADEnrichedGalerkinPenaltyBC
  variable = ep
  backbone = p
  boundary = 'left right'
  reference_flux_name = flux_p
  mobility_name = Dpp
  sigma = 12
 []
 [p_cross_boundary]
  type = ADEnrichedGalerkinCrossPenaltyBC
  variable = ep
  column_backbone = q
  column_enrichment = eq
  boundary = 'left right'
  cross_mobility_name = Dpq
  sigma = 12
 []
 [q_continuous]
  type = DirichletBC
  variable = q
  boundary = 'left right'
  value = 0
 []
 [q_enrichment]
  type = ADEnrichedGalerkinPenaltyBC
  variable = eq
  backbone = q
  boundary = 'left right'
  reference_flux_name = flux_q
  mobility_name = Dqq
  sigma = 12
 []
 [q_cross_boundary]
  type = ADEnrichedGalerkinCrossPenaltyBC
  variable = eq
  column_backbone = p
  column_enrichment = ep
  boundary = 'left right'
  cross_mobility_name = Dpq
  sigma = 12
 []
[]
[Postprocessors]
 [p_l2]
  type = ElementL2Error
  variable = pt
  function = p_exact
  execute_on = TIMESTEP_END
 []
 [q_l2]
  type = ElementL2Error
  variable = qt
  function = q_exact
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
 file_base = out_cross
[]
