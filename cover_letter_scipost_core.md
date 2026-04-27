Dear SciPost Physics Core Editorial College,

We submit "Separator-Local Treewidth--Magic Simulation of Compositional Quantum Language Circuits" for consideration in SciPost Physics Core under the Quantum Physics / Mathematical Physics / Computational Physics scope.

The manuscript develops SLMS, a certificate-based sufficient condition for additive classical simulation of a restricted class of structured quantum tensor networks. The method combines junction-tree-style message passing, stabilizer-compressed separator boundaries, and local quasiprobability `l1` costs into an explicit message-burden parameter `Lambda_msg`. The main theorem gives a runtime controlled by `w_eff` and the explicit sampling factor `exp(2 Lambda_msg)`.

The work is motivated by compositional quantum-language circuits, but its primary contribution is in quantum circuit simulation and dequantisation. The paper makes no quantum-advantage claim and no general-purpose simulator claim. The accompanying artifact provides certificate-evidence diagnostics, fallback structured quantum-language instances, negative controls, and comparison diagnostics against dense tensor-network, global quasiprobability, focused-width, ZX-inspired, and stabilizer-tensor-network-inspired proxies.

We believe the manuscript fits SciPost Physics Core because it addresses classical simulability of structured quantum tensor networks, provides a new checkable sufficient certificate, includes reproducible derivations and artifacts, cites representative literature, and gives a transparent account of its assumptions and limitations.

SciPost Physics Core criteria alignment:

- Important problem: additive classical simulation of structured quantum tensor networks with localized non-Clifford resource.
- Originality: a checkable certificate combining local quasiprobability costs, stabilizer-compressed boundaries, local marginalization, and junction-tree-style message passing.
- Significant advance: an auditable runtime parameter `w_eff + 2 Lambda_msg` and explicit sampling factor `exp(2 Lambda_msg)`.
- Reproducibility: proof details, worked certificate, executable scripts, CSV outputs, plots, environment logs, and hard blocker ledger.
- Literature: representative comparison to tensor-network treewidth, quasiprobability simulation, stabilizer rank, focused width, ZX simulation, STN/MAST, lambeq, and QDisCoCirc.
- Limitations: fallback-only nontrivial artifact evidence, parser-level lambeq unavailable, exact ZX/STN baselines unavailable, no dominance or quantum-advantage claim.

Sincerely,

[Authors]
