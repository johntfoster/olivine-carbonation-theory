# Response matrix — numerical-20261008-01

This is simulated AI peer review. Reports are preserved unchanged. Acceptance votes will not carry to the revised snapshot.

| Comment | Disposition and evidence | Verification |
|---|---|---|
| R1-O01 | Corrected the malformed interior-facet subscript in the new EG residual; original governing equations unchanged. | Rebuilt PDF and equation map. |
| R2-O1 | Retained the worst-cell location, time, storage histories, current backbone and all balance terms for every column mesh in the supplement. | Driver reanalysis of all actual steps; 178 checks pass. |
| R2-O2 | Added the direct Jacobian-check command to environment/README.md. | Matches the recorded successful Jacobian command. |
| R2-O3 | Shortened mineral axis labels while keeping units; per-mixture-volume convention is defined in the manuscript. | Regenerated and inspected figure PDFs. |
| R3-01 (required) | Abstract now states specialization; physical-setting paragraph cites the compositional parent and distinguishes inherited balances/reference measures/transfer work from application free energies. | Citation resolves in rebuilt PDF; source correspondence retained. |
| R3-02 | Captions identify reference markers as appearing in the aqueous panel. | Figure/caption inspection. |
| R3-03 | Reproduction paragraph points to direct extracted-supplement commands in environment/README.md. | Source command and external-dependency audit. |

The presentation/retention changes do not modify C++ sources, input decks, compiled solver artifacts or numerical tolerances. Actual completed runs were reused with matching saved fingerprints; independent reference computations and numerical analysis were rerun. The script records that reuse explicitly.
