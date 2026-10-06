# Durable goal: olivine carbonation theory

## Authorization and scope
John authorized steps 1 and 2 on 2026-10-06: standalone repository scaffold and problem-specific theory development through acceptance. **Do not implement MOOSE** until separately authorized after theory acceptance. Compressible elastic constituents only; no plasticity; use isotropic logarithmic mineral/skeleton Biot laws, not anisotropic Biot formulation.

## Objective
Develop an implementation-ready finite-deformation theory for Mg2SiO4 + 2 CO2 -> 2 MgCO3 + SiO2, treating forsterite, magnesite, and silica as separately compressible elastic solids with a CO2 pore phase. Synthesize the three-/four-phase and compositional sources with explicit provenance and thermodynamic consistency.

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
Parent coordinator owns this goal and `.agent-runtime/goal-checkpoint.json`; 6.1 Sol infrastructure agent owns scaffold, Astra author owns theory. One writer per surface. Reviewer seats write only their own reports against immutable snapshots. Check existing worker deliverables before retrying; never duplicate a writer.

## Platform goal status
Native get_goal/create_goal/update_goal tools are not exposed in this Codex runtime. Installed OpenClaw documentation says native-Codex Goal start is unavailable. This version-controlled goal plus on-disk checkpoint provides durability, but is **not claimed to be an active platform /goal**. Do not edit OpenClaw state stores to emulate one.

## Scientific boundary
The proposed Liu et al. (2024) experiment uses aqueous CO2-rich water/brine, not a pure CO2 gas pore phase. The initial gas-only elastic theory must not be labeled a quantitatively validated reproduction of that experiment. Its eventual aqueous extension and any inelastic compaction mechanisms must be identified explicitly.
