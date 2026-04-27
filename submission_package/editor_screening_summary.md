# Editor Screening Summary

## Problem

Structured compositional quantum language circuits are neither arbitrary quantum circuits nor purely tree-like tensor networks. Standard dense tensor-network bounds exploit graph width, while stabilizer/quasiprobability simulators exploit low global non-stabilizer resource. Neither parameter alone captures where magic sits relative to separators in a compositional contraction graph.

## Main Result

For locally marginalizable resource-decomposition networks, the manuscript proves the SLMS simulation theorem:

\[
\widetilde O(\mathrm{poly}(|C|)\epsilon^{-2}\log(1/\delta)
2^{O(w_{\mathrm{eff}})}
\exp(2\Lambda_{\mathrm{msg}})).
\]

Here \(w_{\mathrm{eff}}\) is stabilizer-compressed effective width and \(\Lambda_{\mathrm{msg}}\) is the message burden computed by an explicit active-child recurrence. The factor of two is displayed because the proof uses a second-moment bound \(\Gamma_b^2\).

## Novelty

The paper introduces a certified separator-local recurrence combining stabilizer compression, local free-tensor quasiprobability costs, local coefficient-map factors, and active-child marginalization. It proves separations from naive global quasiprobability burden and from dense treewidth parameter bounds for a stabilizer-compressed grid family.

## What Is Not Claimed

The manuscript does not claim unconditional quantum advantage, does not claim coverage of arbitrary lambeq/QDisCoCirc circuits, and does not prove lower bounds against all classical algorithms. The dense-grid result is a parameter separation from dense tensor-network width bounds, not a complexity-theoretic separation.
