# Implementation status

MOOSE implementation, tests, site and container publishing were authorized on
7 October 2026. PLAN.md records the implementation and delivery plan.

| Gate | Evidence |
|---|---|
| Equation contract | Completed; actual objects mapped to labeled weak forms |
| MOOSE build and residual tests | 61 executable checks passed |
| EG tests and convergence | Scalar 1D/2D/3D and coupled cross-diffusion passed; L2 orders approximately 2 |
| Site build and source links | Local build and all generated links passed; source bytes hash checked |
| Base/application image build | SSH-ready base run 37660466019 and exact f2133b3 application run 37677303026 published immutable digests after required smoke and 61 numerical checks |
| GitHub Pages deployment | Run 37677304226 succeeded; all 102 raw sources/viewers match committed f2133b3 bytes; six main pages/assets returned HTTP 200 |
| Hosted Codespaces | Full rebuild and same-environment stop/resume passed using the published f2133b3 image without manual configuration. Standard CLI, automatic source guards, exact source/artifact integrity and all 61 numerical checks passed; paper bytes unchanged |
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
test, 61 internal checks, zero skipped/failed). The pinned framework has no
tracked local modifications. Desktop and mobile site layouts were inspected.

The copied local framework’s generated libtool paths were relocated into this
repository before the final run. The application executable now resolves its
framework libraries inside this repository. No sibling repository was modified.

`verification/environment-results.json` records the independently built base
image ID and clean-clone container results. This Docker image ID is distinct
from a registry manifest digest.

Temporal manufactured mass convergence verifies backward Euler (orders 1.012
and 1.006) and BDF2 (1.981 and 1.990) using a time-varying source and nonlinear
complete storage. The constant-source conservation test alone cannot
distinguish those methods.

## Numerical manuscript extension — 8 October 2026

The manuscript now describes actual storage discretization, AD responsibilities
and conservative EG diffusion. Two silica reaction examples use the exact
restricted binary-aqueous, unstressed, equal-density branch. Closed-reactor
precipitation/dissolution agree with independent extent histories; a coupled
EG column agrees with an independently refined finite-volume reference.
All 178 quantitative example checks pass. The coupled Jacobian discrepancy is
7.4e-11 relative; the existing 61 executable and 52 analytical checks also pass.
Raw observations, logs, source/data hashes and errors are in data/silica/ and
verification/silica-results.json. The maximum column cell mass residual is
3.16e-10 kg/(m3 s). These are numerical verification results, not measured
mineral properties or a full seven-mechanism carbonation prediction.
Historical hosted image and site evidence above concerns earlier source bytes;
this manuscript extension has not been deployed or published as an image.
