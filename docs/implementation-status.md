# Implementation status

The platform goal is active. MOOSE implementation, tests, site and container
publishing were authorized on 7 October 2026. PLAN.md is the current plan.

| Gate | Evidence |
|---|---|
| Equation contract | Completed; actual objects mapped to labeled weak forms |
| MOOSE build and residual tests | 42 executable checks passed |
| EG tests and convergence | Scalar 1D/2D/3D and coupled cross-diffusion passed; L2 orders approximately 2 |
| Site build and source links | Local build and all generated links passed; source bytes hash checked |
| Base/application image build | Base toolchain installed; local framework build in progress. Workflows prepared |
| GitHub Pages deployment | Pending |
| Hosted Codespaces | Not run |
| Physical validation | Not performed |

The requested sibling `finite-deformation-biot-poromechanics` is absent. The
available `finite-strain-biot-poromechanics` supplies the design reference.
The compositional parent's enriched Galerkin objects supply the discretization
reference, with attribution and inspected-byte hashes recorded separately.

The mineral root follows the author-requested finite-strain companion Newton/AD
helper. Three mineral roots and the aggregate Biot coefficient are compared
against an independent scalar bisection calculation. Four infrastructure tests
check source-matched binary reuse and rejection of changed headers, new source
files and corrupted application shared libraries.
