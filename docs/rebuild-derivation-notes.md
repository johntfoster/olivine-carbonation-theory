# Candidate derivation checkpoint for source-fidelity audit

Historical checkpoint: this document records the 6 October 2026 theory rebuild. Its label/page counts and statements about future implementation describe that stage. The 8 October numerical extension is documented in `docs/implementation-status.md`, `docs/numerical-verification-plan.md`, the current manuscript and source-bound verification reports.

## Governing choice

John's clarification (Telegram 7418) selects a special case of the compositional paper in its notation. It does not authorize blending older reacting-mixture transfer prescriptions into that parent. The source contract was delivered before manuscript rewriting; the new root is a replacement of the rejected scientific content, not a notation patch.

## Concrete propagated differences from rejected candidate

1. The state is the compositional phase/component state: rho_xi^alpha=phi_xi rho-bar_xi eta_xi^alpha, C_xi^alpha, F/J, A_s/a_s/F-bar_s/J-bar_s, one tau and mass-specific L_xi^alpha. Mole fractions appear only as derived constitutive activity arguments. Mineral/aqueous mole inventories are not governing variables.
2. The tau relation is C `eq:MC_admissible_conversion_component`; all L values are recovered from C `eq:MC_transfer_work_full_recovery`. A stationary skeleton retains its initial tau. No per-reaction tau, donor normalization, or extra power-pair correction survives.
3. Phase-changing reaction force is C's full generalized supply sum. Its aqueous phase-common offset is derived explicitly in candidate `eq:fluid_transfer_offset` and retained in `eq:reaction_force`. Homogeneous aqueous reactions alone cancel that offset by phasewise mass conservation.
4. Net aqueous mass production shifts source resistance and weights the source insertion force. Both survive the specialization. The mixture gradient-tau force cancels only after summing all phases; the relative momentum source remains.
5. Mineral compressibility is not imported by changing a source incompressibility assumption in isolation. The candidate instantiates psi_s(A_s,F-bar_s,rho-bar_s) and differentiates before imposing true mass conservation. Its stress, intrinsic pressure and scalar-distention trace are mutually checked. The mineral mean logarithmic stress is explicitly recovered. Matched-log single-solid elastic energy uses the source normalization directly: K is the skeleton modulus per mixture reference volume, K_s the intrinsic mineral modulus, and G_source=phi_s0 G_s. Thus the distention factor is 1-K/(phi_s0 K_s); each solid branch has its own allocated K.
6. Biot is the parent fixed-pressure derivative and phase rollup, not a finite-pressure fitted multiplier. Electrical equivalent pressure is retained distinct from actual phase pressure; common constant permittivity permits a direct Maxwell-stress bookkeeping check.
7. Ionic aqueous species retain source specific charge, electrochemical diffusion and Gauss law. No hidden electroneutral replacement was made. Nine species enter the original mass-fraction/component balances; all seven application stoichiometric columns conserve atom, mass and charge counts.
8. Fluid density, solvent and solute component potentials come from one declared mass-specific phase potential. It is an ideal-mixture demonstration, not experimentally calibrated brine chemistry. Standard chemical energies must be supplied compatibly before predictive chemistry is claimed.
9. Reference balances and weak signs are derived from C's skeleton pullback, including the insertion force cancellation of J. The 17-scalar-field count is explicitly square for the finite-rate quasi-static branch. Four fast-equilibrium relations replace, rather than supplement, four kinetic laws.

## Evidence and review handoff

- `paper/main.tex`: 66 governing labels, each provenance-tagged.
- `paper/defs.tex`: exact copy of the compositional macro file.
- `verification/equation-map.json`: exact parent paths/lines/digests and classifications.
- `verification/source-equation-excerpts.json`: 81 literal parent/source equation contexts.
- `verification/parent-sources/`: 18 exact-byte inspected source snapshots for portable audits (not parent-project build distributions).
- `verification/analytical_report.json`: 52 passing checks, comprising 49 synthetic scientific consistency/dimension checks and 3 source/document integrity checks. No rejected evidence is credited.
- `verification/render-inspection.json`: 13-page PDF QA, zero LaTeX box/reference diagnostics; not a scientific acceptance claim.
- `verification/implementation-map.md`: future residual/material map only, no implementation.

Commands completed: `python3 verification/build_equation_map.py`; `python3 verification/check_theory.py`; `make paper`; `pdftoppm -scale-to 1400 -png build/main.pdf build/rebuild-page`; pinned derivation-surface scanner. All originals remain untouched. No commit, push, independent review, AI acceptance, numerical simulation, convergence or physical validation was performed by this writer.

## Narrow limitations, not source ambiguities

The compositional normalization is a resolved governing choice, not a question for John. Positive participating masses, scalar-mineral stable roots, positive pore volume and a nonsingular corrected resistance define the present smooth domain. Phase appearance, chemistry/material calibration, global existence/uniqueness, discretization and simulation remain outside the demonstrated result. None is concealed by an alternative governing model. The next gate is the coordinator's independent comparison to actual pinned source equations, followed by a new review cycle from zero.
