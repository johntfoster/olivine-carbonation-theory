# Independent simulated AI peer review — reviewer 3

Round: numerical-20261008-01  
Snapshot ID: c0e4d11ef2e69cdf9aba1150cbf5b2c0c48122afc73876ab686fddd1ff858c0a  
Seat: exposition, notation, claim accuracy and engineering usefulness  
Review status: fresh independent simulated AI review; no previous votes or other reviewer reports were inspected or credited.

## Independent snapshot verification

I independently computed SHA-256 of the exact MANIFEST.json bytes and obtained c0e4d11ef2e69cdf9aba1150cbf5b2c0c48122afc73876ab686fddd1ff858c0a. It matches both the assigned ID and the exact value in SNAPSHOT_ID. I read and hashed all 261 listed payload files and checked their declared byte counts: zero missing files, zero size differences and zero hash differences. The compositional macros in paper/defs.tex are byte-identical to verification/parent-sources/C/defs.tex.

I additionally checked the evidence-to-payload bindings: all 62 silica report source hashes, all 103 silica data hashes, all 61 Jacobian report source hashes and all 70 implementation report source hashes match the included files. The cited executable and shared-library bytes are recorded evidence, not bundled runnable artifacts; I did not assert their independent reproduction.

## Review coverage and limits

I read the snapshot AGENTS.md, GOAL.md, research-project.yml, agent-profile.json, scientific source contract/correspondence, the complete application manuscript and its definitions, and relevant actual pinned compositional source passages/macros. I compared material increments, constituent potentials, transfer normalization, reaction rates, scalar-distention restrictions and solid-reference balances directly with the included parent source. I examined the actual silica chemistry/storage/facet code, input decks, independent reference driver, implementation map, recorded numerical reports and selected compressed solver logs. I read the 19-page PDF and visually inspected the implementation table, both numerical figures and the spatial error table on pages 14, 15 and 17.

The exact workflow revision is declared as 74309a56c009d65aa83f7729e6775fb8fea340ce in research-project.yml. The workflow catalog itself is deliberately excluded from snapshots by docs/review-workflow.md. I respected the immutable-snapshot restriction and did not substitute the live workflow catalog, manuscript, sibling sources, framework or reviewer reports. This review is not a clean-environment MOOSE rerun or physical validation.

## Assessment

The numerical extension is technically useful and substantially well explained. The distinction between partial current density and intrinsic phase density is explicit at paper/main.tex:35. The phase-attached increment and skeleton-reference storage are distinguished at paper/main.tex:56 and paper/main.tex:528. The transfer offset and production-dependent fluid resistance are retained, rather than replaced by a separate reaction-transfer construction. Their zero values in the examples follow from the stated branch.

The binary silica restriction is convincing. At paper/main.tex:657 the other components and reactions are excluded from the test subsystem, without claiming that the full ideal nine-component equations admit zero concentrations. At paper/main.tex:659 the equal reference densities, zero pressure and identity deformation make the mineral roots one, the stress zero and the fluid bulk flux zero. At paper/main.tex:661 reaction mass transfer therefore gives compensating phase-volume changes. This is an exact synthetic unstressed branch, not an approximation to measured silica densities. The mineral equations still carry positive phases, and the mechanical/electrical equations are explicitly acknowledged to be satisfied trivially rather than verified by these examples.

The change to q at paper/main.tex:673 is an invertible constitutive coordinate. Its derivative is positive, and the implemented inversion reconstructs mass fractions before evaluating complete storage and mass-based reaction sources. It does not replace the parent balances by independent mole inventories. The solvent source follows from total fluid storage and the silicic-acid balance because M7 = MC + 2 MN and the relative mass flux is zero sum. The extent ODE and finite-volume reference instead use mole diagnostics consistently; they import no MOOSE residual implementation.

The storage formulas, facet signs and residual responsibilities are understandable and match the inspected code. The complete reference mass is differenced, the BDF2 coefficients include the time-step ratio, and the EG cell tests expose equal-and-opposite facet fluxes. The representation anchor does not prescribe the reconstructed physical boundary value. The manuscript explicitly limits its displayed EG method to diffusion and does not claim stabilization for the full advective system. The 17-field count at paper/main.tex:577 is consistent with the stated independent fields and nine aqueous balances.

The reported numerical results are supported by inspectable observations. I independently recalculated from the shipped CSVs:

- Reactor maximum aqueous trajectory errors: 8.0660504551e-6 and 1.6918756589e-4 mol/m3.
- Reactor mineral changes: +4.9996515781 and -4.0009844412 mol/m3; final absolute rates are below 0.002 mol/(m3 s).
- Reactor Si/H/O relative inventory drift is below 5.0e-13, comfortably below the manuscript's stated 1e-9 bound.
- Aqueous column RMS errors on 16, 32, 64 and 128 cells: 2.8756414603e-3, 7.2183587355e-4, 1.8122196246e-4 and 4.5933179098e-5 mol/m3. Corresponding mineral errors reproduce the spatial table as well.

The temporal table agrees with the detailed report, and the reference-refinement comparison is appropriately described as comparison against a refined independent discretization, not a known continuum exact solution. The cellwise maximum residual is recorded with a source-bound reconstruction algorithm; only selected spatial profiles are shipped, so I did not independently recalculate its maximum over all elements and time steps. The data README explicitly discloses this storage choice and says a rerun regenerates the intermediate profiles. Compressed batch and finest-column logs show the expected 3200 and 1000 converged steps. The recorded Jacobian discrepancies are supported by the included Jacobian log.

The physical limitations are convincing and repeated where needed: paper/main.tex:654, paper/main.tex:659, paper/main.tex:761 and paper/main.tex:763 distinguish actual reaction solves, synthetic residual verification, calibration and experimental validation. The manuscript does not claim a solved calibrated seven-mechanism carbonation network, active-phase treatment, scalable solver performance or deployment of this extension.

## Required correction

**R3-01 — Minor: identify and cite the controlling compositional parent in the rendered manuscript.** Locations: paper/main.tex:17, paper/main.tex:21, paper/main.tex:97, paper/main.tex:601; bibliography entry at paper/references.bib:7. The supplement carefully establishes that this application specializes the existing compositional framework, but the rendered paper never cites `compositional` or explicitly states that relationship. The abstract says “We develop” and the physical-setting introduction cites only the elastic companion. The only prose mention of the compositional companion is for EG operators. Consequently, a reader of the PDF cannot distinguish inherited governing theory from application constitutive choices and the new numerical implementation. This matters particularly because GOAL.md makes special-case equivalence, rather than a replacement theory, the controlling scientific claim.

Required action: add a concise statement near the start of the paper identifying the formulation as a specialization of the compositional parent and cite its existing bibliography entry. Identify the inherited balances/transfer normalization and the application-specific elastic/aqueous closures at a useful level; refer readers to the equation correspondence in the supplement for exact provenance. Adjust the abstract's attribution if necessary. No new governing equations or numerical runs are requested by this finding.

## Optional improvements

**R3-02 — Optional: specify which figure panel contains reference markers.** Locations: paper/main.tex:700, paper/main.tex:734; scripts/run_silica_verification.py:255 and scripts/run_silica_verification.py:265. Both figures plot independent reference markers only on the aqueous panel. Their captions can be read as describing markers for both panels. State “open markers in the aqueous panel” or add reference markers to the mineral panel. The existing tables and stored data do support mineral agreement, so this is a presentation improvement rather than a numerical defect.

**R3-03 — Optional: point directly to the extracted-supplement reproduction instructions.** Locations: paper/main.tex:761; environment/README.md:101; tools/moose-run:6. The main-text `make moose`, `make test` and `make verification-examples` commands depend on an activated environment with `with-moose` or the shared workflow checkout. The extracted snapshot intentionally omits that checkout. The environment README already provides direct commands and explains the external framework placement. A short pointer from the main-text reproduction paragraph would prevent a reader from treating the listed convenience targets as immediately runnable in the extracted supplement.

I found no required correction to the presented density distinction, restricted mass balances, reaction signs, numerical results or stated validation limits. The one required correction concerns attribution and the main scientific claim visible in the PDF.

MINOR REVISION
