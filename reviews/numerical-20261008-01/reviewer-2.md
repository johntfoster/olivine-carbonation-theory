# Independent simulated AI peer review — reviewer 2

Round: `numerical-20261008-01`  
Seat: numerical verification, implementation fidelity and reproduction  
Candidate: `.agent-runtime/review-snapshots/numerical-20261008-01`  
Declared manifest ID: `c0e4d11ef2e69cdf9aba1150cbf5b2c0c48122afc73876ab686fddd1ff858c0a`

## Snapshot integrity and review boundary

I independently hashed the exact bytes of `MANIFEST.json`; the result is `c0e4d11ef2e69cdf9aba1150cbf5b2c0c48122afc73876ab686fddd1ff858c0a`, equal to the declared ID and `SNAPSHOT_ID`. All 261 listed files exist, and every listed byte count and SHA-256 matches. There are no missing files, size errors or digest mismatches.

I reviewed the frozen authorities, manuscript, source correspondence and actual exported compositional-parent equations/macros, implementation map, chemistry/storage/EG sources and headers, three example decks, simulation/reference/Jacobian scripts, numerical reports, archived CSV files, compressed solve logs, failure explanations and environment/reproduction instructions. I inspected both numerical figure PDFs as rendered images. I did not consult other reviewer reports or prior acceptance counts and did not use live manuscript/application sources. The review credits no earlier acceptance.

Independent Python computations used `/home/jfoster/miniconda3/envs/moose/bin/python`. I wrote separate extent and finite-volume calculations from the stated balances and thermodynamics rather than importing the supplied reference implementation. I did not rebuild or rerun the MOOSE application: the supplement deliberately excludes its executable and linked library, and a build requires the separately installed pinned framework. This review combines source inspection, independent reference computation and checks of the recorded actual-solve evidence; it does not claim a fresh clean-environment MOOSE reproduction.

## Scientific and implementation audit

The restricted problem is adequately identified in `paper/main.tex:654`–`686`. It keeps all three mineral phases positive, with forsterite and magnesite fixed at 0.2 and 0.1; the chemistry material uses their fixed sum, 0.3. Its binary aqueous phase and mechanism (3) are an explicitly restricted subsystem. The text does not assert that the entire nine-species/seven-mechanism system preserves absent species. These examples provide synthetic verification of a mineral-forming reaction and diffusion, without physical calibration or a full carbonation prediction.

The reduction follows the exported compositional source: `C:eq:MC_onsager_reaction_rate`, `C:eq:MC_affinity_projection`, `C:eq:MC_absolute_neutral_component_potential`, `C:eq:MC_relative_transport_closures`, and the two solid-reference component balances. With the prescribed stationary skeleton, uniform zero transfer potential and zero bulk fluid flux, the parent's transfer offset vanishes without changing its normalization. The chosen reference mineral energy gives the stated affinity `R theta ln[x/((1-x)^2 Qeq)]`; the original rate normalization becomes `k = K_(3) R`. The mass sources are `-M7 r`, `MC r` and the complementary solvent source `2 MN r`, with `M7 = MC + 2 MN`. Equal densities make the reaction volume consistent with `phi_f = 0.7 - phi_C`. Zero-sum counterdiffusion preserves that closure. Current and reference measures coincide here because `J = 1`; the general implemented storage still retains the complete `J phi rhobar eta` measure.

`ADSilicaVerificationChemistry.C:40`–`77` inverts the monotone potential coordinate in AD, evaluates a solution-dependent rate, and constructs the correct source signs and scaled-potential mobility. The actual decks solve coupled fluid and mineral residuals; they do not impose a reaction history or manufactured chemical source. `ADReferenceMassStorage.C:27` and `ADReferenceStorageRate.C:24` difference complete mass, including variable-step BDF2 and its Euler startup. Both EG rows consume the same complete mass rate and reaction source. The P0 row and shared facet flux supply element conservation. The backbone boundary gauge fixes only the constant decomposition ambiguity because enrichment remains free; zero physical boundary flux is retained. Diagonal/cross facet and adjoint terms inspected are consistent with the stated diffusion form and its separate MMS scope.

## Independent numerical checks

The following results were reconstructed from raw data and independent calculations, not copied from the pass flags:

- A tighter scalar-extent DOP853 solve using water from conserved hydrogen reproduces maximum precipitation/dissolution trajectory errors of `8.06605045e-6` and `1.69187566e-4` mol/m³. Its values differ from the archived reference by at most `3.79e-11` and `5.44e-12` mol/m³.
- Recomputed reactor errors and halving orders agree with Table `tab:silica_time`. Finest-pair Euler orders are `0.999740` and `0.999351`; BDF2 orders are `2.000452` and approximately `1.992686`.
- Across all archived reactor and column integrated histories, maximum relative Si/H/O drifts are respectively `4.99e-13`, `6.05e-14` and `3.74e-14`. Minimum sampled silica and fluid fractions are `0.0497596089` and `0.649699606`; sampled reaction power is positive. The two inert phases remain positive by prescription.
- Direct Euler/BDF2 fluid, mineral and complementary-water mass residual reconstruction from representative reactor histories gives maxima below `2.55e-10` kg/(m³ s), including CSV roundoff. This checks rate signs and conservative storage against raw histories.
- Independently aggregated raw reference profiles give the reported 512/1024-cell difference `4.58767696e-7` mol/m³. EG aqueous RMS errors are `2.87564146e-3`, `7.21835874e-4`, `1.81221962e-4` and `4.59331791e-5` mol/m³. Mineral errors and aqueous orders `1.994141`, `1.993913`, `1.980149` agree with Table `tab:silica_space`.
- A separately written 1024-cell conservative BDF reference, at tighter tolerances `rtol=2e-11`, `atol=1e-12`, differs from the archived final aqueous/mineral references by at most `5.65e-9` and `2.46e-9` mol/m³. Reference integration error is consequently small relative to the finest EG error.
- Recomputed fixed-64-cell final-profile differences are `3.03920111e-5` and `8.31881998e-6` mol/m³, giving time self-order `1.86924134`. This is a distinct temporal study; the mesh table remains a comparison at a fixed small timestep, as stated.
- From archived nodal backbone/enrichment profiles, I independently reconstructed facet fluxes and cell chemistry by two-point quadrature. At 16 and 128 cells, computed cell aqueous inventories and rates match the archived samples within `8.0e-12` mol/m³ and `1.6e-12` mol/(m³ s). The shared fluxes cancel globally to roundoff. For example, at final time on 128 cells, zero-based cell 64 has left/right mass fluxes `0.001674632108` and `0.001672730743` kg/(m² s), reaction sink `0.0008545321045` kg/(m³ s), and implied mass rate `-0.0006111573841` kg/(m³ s).

The archived selected column profiles do not contain consecutive timesteps, so they alone cannot independently regenerate the reported maximum full BDF2 cell residual `3.157e-10`. The supplied driver computes that quantity over the complete regenerated runtime profiles with the correct flux, source, startup and constant-step BDF2 formulas. This limitation is explicitly documented in `data/silica/README.md:22` and is compatible with the stated source-reproduction supplement.

## Evidence and reproduction bindings

All 224 available source/data/fingerprint bindings in `silica-results.json`, all 62 available Jacobian source/log bindings, and all 70 implementation-report source bindings match the frozen files. The deliberately excluded executable/library are the only unavailable artifact hashes in the silica reports. The two silica reports identify the same executable digest; the solver fingerprint matches the scientific application sources. Build provenance also matches its source and output files. The original parent-source lineage hashes match the exported source files.

The 33 archived example solve logs have the requested final times, expected timestep counts and converged steps, with no recorded failed solve in those completed logs. Reused actual solves are explicitly distinguished from new solves and accompanied by the source/linked-artifact fingerprint and reuse explanation. Separate failed driver/deck attempts remain recorded. No tolerance relaxation is needed to explain the passing evidence. The raw PETSc Jacobian ratios are `4.51699e-11`, `4.76791e-11`, `7.39325e-11`, and `4.98475e-11`, supporting the manuscript's rounded maximum. All 178 example checks and 61 separate existing checks are recorded as passed, with their distinct evidence categories retained.

Figures use the archived actual and independent-reference series through the supplied plot function, and their visible trends agree with those series. Tables and numerical prose are traceable to the raw computations above. `environment/toolchain.json` pins MOOSE to `abafb58b67a6037c6723ffeb19647c84484466da`, and the explicit Conda lock supplies the scientific toolchain. The extracted-supplement instructions explain the external framework checkout, activation and default audit path. Historical hosted-image evidence is expressly separated from this extension. No deployment is needed for this review.

## Required changes

None. I found no demonstrated numerical, conservation, source-normalization or scope defect requiring revision for the declared restricted verification examples.

## Optional comments

- **R2-O1 — Retain a compact worst-cell audit record.** `scripts/run_silica_verification.py:203`; `data/silica/README.md:22`. For easier verification of the archived maximum cell residual without a full rebuild, record its cell/time location and retain the corresponding three storage snapshots plus current nodal/enrichment/source profile. The existing transparent regeneration route is adequate; this would strengthen convenient evidence inspection.
- **R2-O2 — Include the independent Jacobian command in the extracted-supplement sequence.** `environment/README.md:116`. Add `python3 scripts/check_silica_jacobian.py` alongside the direct commands so readers following only this block also regenerate the new coupled-Jacobian report. The command already appears elsewhere.
- **R2-O3 — Shorten the mineral-axis label.** `scripts/run_silica_verification.py:258` and `scripts/run_silica_verification.py:268`. The long vertical mineral-change label is clipped at the top in the standalone figures. A shorter label or taller figure would improve presentation without altering the numerical evidence.

ACCEPT
