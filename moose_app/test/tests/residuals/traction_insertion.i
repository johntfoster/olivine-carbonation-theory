!include mechanics.i
# Nonzero insertion and gravity cancel analytically: rho*g := cdot_f W/rho_f.
# Natural traction is independently derived at p=0, phi=phi0*b/J.
[Variables]
 [p]
  initial_condition := 0
 []
[]
[Functions]
 [traction_exact]
  type := ParsedFunction
  expression = '0.3/(1+0.1*t)*(4/3*(1+0.1*t)^(-2/3)*((1+0.1*t)^2-1)+10/3*log(1+0.1*t))'
 []
[]
[Materials]
 [constants]
  prop_names := 'rho_f rho source eta charge conversion'
  prop_values := '1 0.06 0 1 1 0.3'
 []
 [vectors]
  prop_names := 'W j'
  prop_values := '0.2 0 0 0 0 0'
 []
 [traction_function]
  type := ADGenericFunctionVectorMaterial
  prop_names := traction
  prop_values := 'traction_exact 0 0'
 []
[]
[Kernels]
 [momentum]
  fluid_production := conversion
  gravity := '1 0 0'
 []
[]
[BCs]
 [motion]
  boundary := left
 []
 [traction]
  type := ADReferenceTraction
  variable := u
  component := 0
  traction := traction
  boundary := right
 []
[]
