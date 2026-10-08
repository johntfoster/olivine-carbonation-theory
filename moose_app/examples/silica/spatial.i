!include batch.i
[Mesh]
 nx := 32
[]
[Variables]
 [e]
  family = MONOMIAL
  order = CONSTANT
 []
[]
[Functions]
 [q_initial]
  expression := 'n:=5+4*cos(pi*x); w:=(650-0.096113*n)/0.018015; xsi:=n/(n+w); log(xsi)-(0.096113/0.018015)*log(1-xsi)'
 []
[]
[Materials]
 [chemistry]
  enrichment = e
  diffusion_mobility = 1e-6
 []
 [fluid_rate]
  type = ADReferenceStorageRate
  variable = q
  storage = fluid_mass
  rate = fluid_rate
 []
[]
[Kernels]
 inactive = 'fluid_time fluid_reaction'
 [fluid_continuous]
  type = ADEnrichedGalerkinScalarBalance
  variable = q
  enrichment = e
  reference_component_storage_rate_name = fluid_rate
  source_name = silica_fluid_source
  reference_flux_name = silica_flux
 []
 [fluid_enriched]
  type = ADEnrichedGalerkinScalarEnrichmentBalance
  variable = e
  backbone = q
  reference_component_storage_rate_name = fluid_rate
  source_name = silica_fluid_source
 []
[]
[DGKernels]
 [flux]
  type = ADEnrichedGalerkinFluxDG
  variable = e
  reference_flux_name = silica_flux
  mobility_name = silica_mobility
  sigma = 12
 []
 [symmetry]
  type = ADEnrichedGalerkinSymmetryDG
  variable = q
  enrichment = e
  mobility_name = silica_mobility
 []
[]
[BCs]
 [decomposition_gauge]
  type = DirichletBC
  variable = q
  boundary = left
  value = -8.2938839759539817
 []
[]
[AuxVariables]
 [n_si]
  family = MONOMIAL
  order = CONSTANT
 []
 [r_si]
  family = MONOMIAL
  order = CONSTANT
 []
 [q_total]
  family = MONOMIAL
  order = FIRST
 []
[]
[Materials]
 [q_reconstruction]
  type = ADOlivineReconstruction
  backbone = q
  enrichment = e
  value = q_total
  gradient = grad_q_total
 []
[]
[AuxKernels]
 [n_si]
  type = ADMaterialRealAux
  variable = n_si
  property = aqueous_silicon
  execute_on = 'INITIAL TIMESTEP_END'
 []
 [r_si]
  type = ADMaterialRealAux
  variable = r_si
  property = silica_rate
  execute_on = 'INITIAL TIMESTEP_END'
 []
 [q_total]
  type = ADMaterialRealAux
  variable = q_total
  property = q_total
  execute_on = 'INITIAL TIMESTEP_END'
 []
[]
[VectorPostprocessors]
 [nodes]
  type = NodalValueSampler
  variable = q
  sort_by = x
  execute_on = 'INITIAL TIMESTEP_END'
 []
 [profile]
  type = ElementValueSampler
  variable = 'n_si phi_C r_si q_total e'
  sort_by = x
  execute_on = 'INITIAL TIMESTEP_END'
 []
[]
[Executioner]
 dt := 0.02
 end_time := 5
[]
[Outputs]
 file_base := out_spatial
[]
