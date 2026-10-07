# Implementation goal — 7 October 2026

The author explicitly authorizes MOOSE kernels and tests, enriched Galerkin as needed, a completed companion website, a manually triggered base MOOSE/scientific-Python image and exact-revision application images on every push for Codespaces. This supersedes every earlier implementation deferral below. Plasticity remains excluded. The current manuscript and compositional source contract control implementation. See PLAN.md and docs/implementation-status.md. The platform goal records the full author request. Implementation and hosted verification evidence is recorded in verification/environment-results.json. Historical platform/tool and scope statements below describe earlier work only.

# Durable goal: olivine carbonation theory

## Controlling clarification — compositional special case (Telegram 7418)

John explicitly states that olivine carbonation is a **special case of the compositional paper**, not a new theory or a synthesis of competing frameworks. This clarification controls all rebuild work. Use the compositional paper's existing notation, macros, state variables, governing equations, variational/transfer-work conventions, and reference configurations. Present each general source equation, the phase/component/reaction substitutions and restrictions, and the resulting specialized equation. Identify retained and vanishing terms. Do not reinvent balances, transfer potentials, or a new primary-inventory formulation. Other author papers are supporting constitutive references only where consistent with the compositional parent; do not import their different normalizations or governing laws over it. The source contract and independent audit must test **special-case equivalence**, not merely self-consistency or loose provenance.

## Active reset — John rejected the delivered manuscript, 2026-10-06 16:50 CDT

This instruction supersedes previous scientific acceptance and candidate-development choices. The delivered aqueous manuscript is **rejected by the author** because it departs from his theory and notation. Redo the complete scientific manuscript and dependent derivations/checks from the author-owned reacting-mixture and compositional theory. This is a foundational rebuild, not a symbol-renaming exercise or an edit of a substitute reactive-transport model. Earlier reviewer votes and Foster cycles apply only to rejected historical snapshots; none count toward this rebuild.

### Controlling source hierarchy and invariants

1. Read actual author-owned LaTeX and macros, not workspace summaries or the rejected candidate's paraphrases: `/home/jfoster/projects/research/reactive_transport/multicomponent_reactive_flow` (primary compositional framework), `/home/jfoster/Documents/LaTeX/ReactingMixture`, `/home/jfoster/Documents/LaTeX/FourPhaseReactingMixture`, and `/home/jfoster/projects/research/reactive_transport/finite-strain-biot-poromechanics` (elastic isotropic logarithmic specialization only). Resolve symlinks and record actual inspected file hashes including dirty bytes. Sources are read-only.
2. Preserve the source phase/component indices, density distinction, volume fractions, reference/current configuration notation, distention/true-deformation split, mass production, transfer-work fields, variational structure, pressure and stress definitions. Reuse source macros where appropriate. New problem-specific indices must be explicitly mapped, never replace the primary framework with mole-inventory notation.
3. Derive every balance, constitutive specialization, transfer law, and weak form from exact source labels and definitions. Show intermediate specialization steps and units/reference transformations. Do not introduce independent network tau laws, donor normalizations, paired-power replacements, or a generic geochemical framework in place of the source theory. Source discrepancies must be resolved by derivation or recorded as specific blockers, not covered by a new constitutive model.
4. Existing reaction application scope remains: forsterite, magnesite, silica as three compressible elastic solids; one aqueous CO2-bearing multicomponent fluid; isotropic logarithmic mineral/skeleton laws; no separate gas phase, plasticity, or MOOSE implementation. John's present request authorizes a scientific rebuild; it does not explicitly lift the earlier implementation deferral.
5. External chemistry can supply clearly separated application closure/data only where needed and compatible with the source theory. It cannot replace mechanical or transfer foundations. Do not fetch generic reactive-transport theory as the basis. No claims of universal source correctness without checking derivations; concrete ambiguities are surfaced honestly.

### Rebuild milestones and completion gates

- Preserve rejected source/PDF/reports/checkpoint and hashes under `.agent-runtime/baselines/rejected-aqueous-20261006/`; retain old reports as historical evidence, not current approval.
- First produce `docs/rebuild-source-contract.md`: exact authoritative labels, source symbols and meanings, problem-specific specialization, and explicit discarded departures. Provide a comprehensive equation-to-source correspondence, not bibliography-only provenance.
- Rewrite the manuscript and dependent verification/weak-form maps from that contract. Every substantive displayed governing equation must be mapped as inherited, derived specialization, or necessary application closure with derivation. Check source limits, dimensions, conservation, reference pullbacks, thermodynamics, and source-faithful transfer structure.
- An independent source-fidelity audit must compare actual pinned author sources to the new candidate before ordinary scientific acceptance. Mathematical self-consistency of a different model is not sufficient.
- Start the three-independent-reviewer, three Foster editorial cycles, and fresh final review gates below from zero on new snapshots. Reviewers must receive the actual controlling source excerpts/macros and correspondence, not only the candidate's restatement. Source-theory/notation departures are required corrections.
- Build and inspect the new PDF, verify packaging and hashes, deliver it to John here. Distinguish AI review from John's approval. Do not call the goal complete while the rebuild, verification, review, or delivery is pending.

### Current ownership

The current coordinator owns goal/checkpoint and status metadata. Assign one new native sole theory writer after checking no prior writer is active. Old runtime handles are historical, not live assignments. Native owned child completion is the immediate continuation route; record its receipt before yielding. A disk checkpoint alone is not active execution.

## Original authorization and scope
John authorized steps 1 and 2 on 2026-10-06: standalone repository scaffold and problem-specific theory development through acceptance. **Do not implement MOOSE** until separately authorized after theory acceptance. Compressible elastic constituents only; no plasticity; use isotropic logarithmic mineral/skeleton Biot laws, not anisotropic Biot formulation.

## Objective
Develop an implementation-ready finite-deformation theory for Mg2SiO4 + 2 CO2 -> 2 MgCO3 + SiO2, treating forsterite, magnesite, and silica as separately compressible elastic solids with one aqueous CO2-bearing multicomponent pore fluid (water, dissolved carbon and reaction species), without a separate gas phase. Specialize the compositional parent equations and exact notation, with explicit provenance and thermodynamically admissible application constitutive choices.

## Deliverables
- Independent Git repository, GitHub remote, exact-pinned shared workflows, local agent authority and applicable skill activation, reproducible manuscript build, CI and companion website.
- Source/provenance inventory and model specification; private correspondence and third-party attachment payloads excluded from published tree.
- Theory manuscript, PDF, constitutive derivations, balances, closures, weak forms, limiting-case/analytic checks, future equation-to-MOOSE map. No MOOSE application or simulation.
- Development website with evidence status honestly distinguishing theory checks from deferred numerical implementation and experimental validation.

## Acceptance gates
1. Build a reproducible candidate and freeze scientific sources, supporting evidence, bibliography and PDF with a SHA-256 manifest.
2. Three fresh independent simulated AI reviewers, at least two exact ACCEPT on the same snapshot; all substantiated correctness defects resolved. Preserve reports and response matrices; no cross-review exposure.
3. Three separate Foster engineering/prose/narrative review/edit cycles, each with memo, disposition, prose-only invariants, rebuild and page-image inspection.
4. Fresh three-reviewer round on the final post-Foster snapshot; at least two exact ACCEPT and no unresolved substantiated major issue. Acceptance does not carry between changed snapshots.
5. Verify final build, repository push and live site, deliver artifact and links, then mark complete. Simulated review is not journal acceptance.

## Ownership and resumption
Parent coordinator owns this goal and `.agent-runtime/goal-checkpoint.json`; current worker assignments are recorded in the checkpoint and supersede historical assignments. One writer per surface. Reviewer seats write only their own reports against immutable snapshots. Check existing worker deliverables before retrying; never duplicate a writer.

## Platform goal status
Native get_goal/create_goal/update_goal tools are not exposed in this Codex runtime. Installed OpenClaw documentation says native-Codex Goal start is unavailable. This version-controlled goal plus on-disk checkpoint provides durability, but is **not claimed to be an active platform /goal**. Do not edit OpenClaw state stores to emulate one.

## Scientific boundary
On 2026-10-06 John explicitly authorized replacing the gas-only idealization with one aqueous CO2-bearing multicomponent fluid. The phase count remains four: forsterite, magnesite, silica, and an aqueous phase; dissolved species remain within the same aqueous phase. Derive component conservation, speciation/activity closure, fluid EOS and dissolution/precipitation kinetics consistently with compressible elastic mechanics and isotropic logarithmic mineral/skeleton Biot laws. No separate gas phase or capillarity is required within the declared single-aqueous-phase domain.

Liu et al. (2024) provides aqueous experimental motivation, not achieved validation. Natural mineralogy, grain rearrangement, irreversible compaction, kinetic calibration and permeability closure still limit direct quantitative reproduction. No plasticity or MOOSE implementation is authorized.

## Scope-change baseline
The recovered, uncommitted gas-only candidate and its analytical evidence are preserved under ignored `.agent-runtime/baselines/gas-only-20261006/` with file hashes. They are superseded development artifacts, not accepted theory. Earlier runtime-local worker handles are not addressable in the current native tree; recover artifacts before assigning a new sole writer and do not count missing completion events as reviews.
