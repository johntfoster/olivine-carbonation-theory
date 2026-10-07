# Implementation status

The platform goal is active. MOOSE implementation, tests, site and container
publishing were authorized on 7 October 2026. PLAN.md is the current plan.

| Gate | Evidence |
|---|---|
| Equation contract | Completed; actual objects mapped to labeled weak forms |
| MOOSE build and residual tests | 59 executable checks passed |
| EG tests and convergence | Scalar 1D/2D/3D and coupled cross-diffusion passed; L2 orders approximately 2 |
| Site build and source links | Local build and all generated links passed; source bytes hash checked |
| Base/application image build | Local base and independent clean-clone application build/test passed. Actions base run 37649110949 is in progress; application publication awaits the base |
| GitHub Pages deployment | Actions run 37649097662 succeeded; seven deployed pages/assets/source targets returned HTTP 200, packaged kernel bytes matched |
| Hosted Codespaces | Not run |
| Physical validation | Not performed |

The requested sibling `finite-deformation-biot-poromechanics` is absent. The
available `finite-strain-biot-poromechanics` supplies the design reference.
The compositional parent's enriched Galerkin objects supply the discretization
reference, with attribution and inspected-byte hashes recorded separately.

The mineral root follows the author-requested finite-strain companion Newton/AD
helper. Three mineral roots and the aggregate Biot coefficient are compared
against an independent scalar bisection calculation under compression and tension. A uniform-field Maxwell traction case verifies the optional electrical stress. Six infrastructure tests
check source-matched binary reuse and rejection of changed headers, new source
files, corrupted application and test shared libraries and a changed toolchain lock.

The native MOOSE TestHarness ran the quantitative suite successfully (1 harness
test, 59 internal checks, zero skipped/failed). The pinned framework has no
tracked local modifications. Desktop and mobile site layouts were inspected.

The copied local framework’s generated libtool paths were relocated into this
repository before the final run. The application executable now resolves its
framework libraries inside this repository. No sibling repository was modified.

`verification/environment-results.json` records the independently built base
image ID and clean-clone container results. This Docker image ID is distinct
from a registry manifest digest.
