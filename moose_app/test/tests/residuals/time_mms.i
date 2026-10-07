!include nonlinear_mass.i
# Independent exact mass M(t)=0.3125+exp(t)-1; nonlinear p(1+p) storage.
[Functions]
 [mass_rate]
  type = ParsedFunction
  expression = 'exp(t)'
 []
[]
[Materials]
 [constants]
  prop_names := 'J phi'
  prop_values := '1 1'
 []
 [source_function]
  type = ADGenericFunctionMaterial
  prop_names = source
  prop_values = mass_rate
 []
[]
