# Actual silica reaction simulations

The numerical script and three decks generate these observations. Parameters
are synthetic. These are actual MOOSE mass/reaction/EG solves, with independent
extent and finite-volume comparisons; they are not physical validation or a
calibrated full carbonation calculation.

- `precipitation.csv` and `dissolution.csv`: complete closed-reactor histories.
- `*_reference.csv`: independently integrated scalar extent references.
- `*_implicit-euler_*.csv`, `*_bdf2_*.csv`: temporal refinement observations.
- `spatial_N.csv`: integrated column observables at every timestep.
- `spatial_N_tT.csv`: cell averages, P0 mineral fractions and enrichments at
  selected times; `*_nodes_tT.csv` records the continuous backbone values.
- `spatial_N_worst_*`: storage histories and current backbone values for the
  worst cell balance on each mesh; location, time and balance terms are recorded
  under `worst_cell_audit` in the numerical report.
- `fv_N_tT.csv`: independently coded conservative finite-volume references.
- `spatial_time_*_final.csv`: final profiles for fixed-mesh time refinement.
- `*.log.gz`: compressed actual solver stdout and convergence histories.
- `failures/`: preserved driver/deck failures, corrected without relaxing tests.

Reproduce with `make moose`, `make test`, `make verification-examples`, and
`tools/moose-run python3 scripts/check_silica_jacobian.py`. For an extracted
supplement, use the direct activated-environment commands in
`environment/README.md`. Complete per-element sampled histories remain in the
ignored runtime directory during a run; the driver evaluates the exact
BDF2/source/numerical-facet mass residual on every element at every timestep,
and retains the maximum in `verification/silica-results.json`. The supplement
ships complete integrated histories and selected spatial profiles; rerunning
regenerates every intermediate profile.

Original numerical data are licensed CC-BY-4.0, copyright 2026 John T. Foster.
Application and reference solver code use Apache-2.0. External dependencies
retain their own licenses. No experimental observations are included.
