# Olivine carbonation theory — local authority

Read GOAL.md, research-project.yml, agent-profile.json and the exact pinned
.agent/shared workflow catalog. This independent repository owns its theory in
paper/main.tex. The reaction is Mg2SiO4 + 2 CO2 -> 2 MgCO3 + SiO2.
Three compressible elastic solid phases and one aqueous CO2-bearing multicomponent fluid are in scope. Dissolved species remain within the same aqueous phase; no separate gas phase.
MOOSE implementation and tests are authorized by the 7 October 2026 request and PLAN.md.
Plasticity is NOT authorized.

Derive theory explicitly; distinguish assumptions, formal derivations and verified
results. Cite specific equations. No simulation, convergence, physical validation,
review acceptance or publication claim is valid without recorded evidence.
Never publish private email, attachments or credentials. Public research sources
must be traced in the bibliography. Do not modify sibling research repositories.

## Workflow

All pinned shared skills are installed for Codex, Claude, Copilot and OpenCode.
Their presence does not widen task authorization. After cloning run
`tools/setup-agent-workflows`; hook installation and startup never build or
modify a manuscript automatically. Build explicitly with `make paper`.
Source paths are root-relative; manuscript output goes to ignored build/.
Freeze is enabled by setup. For explicitly authorized theory commits use the
supported `git config research.manuscriptFreeze false`, then restore true.
Commit messages follow the six-section process-log contract including AI model
and session provenance. Parent GOAL.md remains the active task authority.

## Mandatory scientific reset (2026-10-06)
John rejected the delivered aqueous candidate. Follow the Active reset in GOAL.md.
The author-owned compositional/reacting-mixture theory and notation are controlling;
no substitute reactive-transport formulation or ad hoc transfer law is authorized.
Read original sources and macros, build an equation-by-equation source contract,
then rederive the application. Earlier candidate acceptance does not carry forward.

John's controlling clarification (Telegram 7418): this application is a SPECIAL
CASE of the compositional paper. Use its exact notation and specialize its
existing governing equations. Do not synthesize a replacement theory from
other papers; source differences do not justify overriding the compositional
parent's transfer-work normalization or variable conventions.
