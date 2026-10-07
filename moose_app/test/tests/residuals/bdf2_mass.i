!include nonlinear_mass.i
[Executioner]
 scheme := bdf2
 num_steps := 3
 [TimeStepper]
  type := TimeSequenceStepper
  time_sequence := '0 0.1 0.25 0.5'
 []
[]
