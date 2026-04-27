# Manuscript Claim Audit

## Classification Key

- **Proved in paper**: statement follows from theorem, lemma, proposition, example, or appendix proof.
- **Supported by experiment**: statement is supported by generated files in `experiments/slms_certificate/` or `benchmarks/`.
- **Supported by citation**: statement is background or comparison supported by cited literature.
- **Speculative / conjectural**: statement is labelled as conjecture or open problem.
- **Needs qualification**: statement remains acceptable only with a stated caveat.
- **Too strong / revised**: statement was or will be weakened.

## Major Claims

| Claim | Classification | Action |
|---|---|---|
| SLMS is a certificate-based separator-local dequantisation/simulation criterion. | Proved in paper as a sufficient criterion. | Keep. |
| SLMS is a general-purpose simulator. | Too strong / revised. | The manuscript explicitly says this is not claimed. |
| The theorem applies to locally marginalizable resource-decomposition networks. | Proved in paper. | Keep and emphasize. |
| The scalar estimator has sampling dependence `exp(2 Lambda_msg)`. | Proved in paper. | Keep explicit everywhere. |
| Message-table estimation is optional and incurs table/error-propagation costs. | Proved/qualified in paper. | Keep separate from scalar theorem. |
| Active-child recurrence is new dynamic programming. | Too strong / revised. | Reframe as junction-tree-style collect recurrence lifted to stabilizer-compressed quasiprobability networks. |
| SLMS combines stabilizer compression, local quasiprobability costs, and active-child marginalization. | Proved in paper. | Keep as central contribution. |
| SLMS beats dense tensor-network contraction in general. | Too strong / revised. | Keep only dense-treewidth parameter separation and non-improvement caveat. |
| SLMS beats focused tree-width, focused rank-width, ZX partitioning, or stabilizer tensor-network simulators. | Too strong / revised. | Explicitly not claimed. |
| Dense-grid example separates dense treewidth bounds from stabilizer-compressed SLMS parameters. | Proved parameter separation. | Keep with caveat: not a computational lower bound. |
| Pedagogical examples separate `Lambda_msg` from global magic burden. | Proved examples. | Keep as examples, not novelty claims. |
| Certified grammar-tree family satisfies local marginalizability. | Proved for specified restricted family. | Keep with restriction. |
| General lambeq/QDisCoCirc circuits satisfy local marginalizability. | Too strong / revised. | Explicitly denied. |
| Real lambeq/QDisCoCirc experiments are reported. | Not supported. | Do not claim. The new artifact attempts real mode and falls back because `lambeq` is unavailable here. |
| Fallback structured instances give certificate-evidence diagnostics. | Supported by experiment. | Add with clear fallback label. |
| Synthetic/fallback outputs are empirical quantum runtime benchmarks. | Too strong / revised. | Explicitly deny; they are certificate-evidence and accounting diagnostics. |
| Focused-width, ZX, and STN comparisons are implemented. | Not supported. | Provide hooks/table only; mark not implemented. |
| Failure of SLMS certificate implies hardness. | Too strong / revised. | Explicitly deny. |
| Quantum advantage or legal-AI benefit. | Too strong / revised. | Explicitly deny. |

## Sensitive Terms

- `new`: Allowed only for the named SLMS certificate object or parameter combination; avoid implying new junction-tree dynamic programming.
- `novel`: Avoid unless tied to the specific certified integration of local quasiprobability burden, stabilizer-compressed width, and local marginalizability.
- `first`: Avoid.
- `efficient`: Use only under theorem hypotheses or in describing cited prior work.
- `state-of-the-art`: Use only in negative comparison statements; SLMS is not claimed to be state of the art.
- `separation`: Use as parameter/accounting separation, not complexity separation.
- `QDisCoCirc` / `lambeq`: Always restrict to certified subclasses or artifact attempts.
- `practical`: Avoid for performance; use `checkable` or `executable artifact` instead.
- `simulator`: Prefer `certificate-based criterion` unless referring to the theorem under its hypotheses.
- `advantage`: Only in explicit negative claims or cited dequantization context.

## Replacement Central Claim

The manuscript should use the following framing:

> SLMS provides a checkable sufficient certificate combining junction-tree-style message passing, stabilizer compression, and local quasiprobability sampling for locally marginalizable structured tensor networks.

This statement is supported by the theorem, certification algorithms, worked certificate, and reproducible fallback artifact. It does not claim dominance over focused-width, ZX, or stabilizer tensor-network simulators.
