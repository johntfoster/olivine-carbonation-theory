# Implementation plan — authorized 7 October 2026

This is the durable `/plan` for the active platform goal. The author's request
explicitly lifts the earlier MOOSE deferral. The compositional special-case
source contract still controls; plasticity and a separate gas phase remain
outside scope. Existing manuscript/review changes are preserved.

1. **Authority and equation contract.** Update GOAL.md and the project manifest;
   map every residual to paper/main.tex and the compositional parent. Record
   inspected sibling revisions and changed bytes. Do not alter sibling files.
2. **MOOSE application.** Implement AD reference mass storage, component/solid
   balances, transfer evolution, momentum, Gauss law and outward-flux/traction
   boundary terms. Keep constitutive properties separate from residuals.
   Difference complete reference storage, including J, fraction and density.
   Follow the finite-strain companion’s bracketed Newton AD mineral-volume
   solver; use no separate implicit-tangent reconstruction (author clarification).
3. **Enriched Galerkin.** Adapt the compositional companion's continuous plus
   P0 reconstruction, paired volume rows, conservative interior flux, adjoint
   consistency, cross-mobility terms and weak boundary terms. Use reconstruction
   in material evaluations. Document the decomposition gauge and fluxless tau.
4. **Verification.** Build against pinned MOOSE in an isolated local checkout.
   Test conservation with nonlinear storage, boundary signs, AD off-diagonal
   derivatives, momentum insertion, dielectric pullback, transfer normalization,
   EG facet cancellation and manufactured-solution convergence. Keep numerical
   verification separate from calibration and experimental validation.
5. **Companion site.** Follow the finite-strain Biot companion's navigation,
   source viewer, object catalog and reproduction pages. Package allowlisted
   source bytes, link each object to equations and tests, and check all local
   targets. Publish through GitHub Pages and inspect the deployed output.
6. **Base image.** Provide a Dockerfile and manually dispatched Actions workflow
   for a pinned MOOSE toolchain/framework with scientific Python. Compile MOOSE
   once in the base layer; record its digest and architecture.
7. **Application image.** On every push build the exact pushed source revision,
   test before publishing to GHCR with a SHA tag and OCI provenance. Resolve the
   base by digest. Codespaces startup verifies source bytes before reusing the
   prebuilt executable, rebuilding when the workspace differs. Never execute
   an older binary as though it matches a newer checkout.
8. **Delivery.** Record real local/hosted results, image digests and site URL.
   Publish the authorized code/configuration with repository hooks. Complete
   the platform goal only after all required deliverables and checks finish.

Progress and evidence are maintained in docs/implementation-status.md. GitHub
Codespaces prebuild configuration is a separate hosted setting; a GHCR image
alone does not prove a hosted Codespace has started.

## Recorded progress

- Equation contract, kernels/materials and 61 quantitative checks complete.
- Native TestHarness and six startup-integrity tests pass.
- Companion site deployed and representative source/assets verified live.
- SSH-ready base and exact 582101c application images published from Actions
  after 61 numerical and startup checks. All 101 site source/viewer pairs
  matched committed bytes. Actual hosted creation/resume remains pending;
  an early image entrypoint is being verified after SSH RPC/port failures.
