!include traction_insertion.i
# Uniform prescribed current field: epsilon=2, E=(1,0,0).
# The reference traction adds sigma_Maxwell_xx = epsilon |E|^2/2 = 1.
[Functions]
 [traction_exact]
  expression := '0.3/(1+0.1*t)*(4/3*(1+0.1*t)^(-2/3)*((1+0.1*t)^2-1)+10/3*log(1+0.1*t))+1'
 []
[]
[Materials]
 [electric_field]
  type = ADGenericConstantVectorMaterial
  prop_names = prescribed_E
  prop_values = '1 0 0'
 []
 [mineral]
  electric_field = prescribed_E
  permittivity = 2
 []
[]
