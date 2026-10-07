!include mechanics.i
[Functions]
 [electric_exact]
  expression := '-(1+0.1*t)^2*x*x/4'
 []
 [electric_outward]
  type := ParsedFunction
  expression := '1+0.1*t'
 []
[]
[BCs]
 [electric]
  boundary := left
 []
 [electric_outward]
  type := ADReferenceOutwardFlux
  variable := potential
  boundary := right
  function := electric_outward
 []
[]
