# v0.4 Upgrade Plan

## 1. Current theorem status

The manuscript currently proves a restricted constructive theorem for locally marginalizable resource-decomposition networks. The theorem is non-circular: the message burden is computed by the active-child recurrence

\[
\Gamma_b=\xi_b\prod_{c\in \operatorname{Act}(b)}\Gamma_c,\qquad
\Lambda_{\mathrm{msg}}=\max_b\log\Gamma_b .
\]

The proof is an induction over tree-decomposition messages, using certified free-region compression, local quasiprobability expansions, local marginalization of inactive children, and an \(\ell_1\)-nonexpansive local map assumption.

## 2. What is already proved

- Free stabilizer regions can be compressed by standard tableau/stabilizer methods, leaving only certified dense active boundary degrees of freedom.
- Bag-local resource tensors admit product quasiprobability expansions with cost \(\xi_b\), or smaller supplied joint costs.
- Locally marginalizable networks obey the message \(\ell_1\) and second-moment recurrence.
- SLMS estimates output probabilities in time controlled by \(w_{\mathrm{eff}}\) and \(\Lambda_{\mathrm{msg}}\).
- There are non-scalar tree examples separating \(\Lambda_{\mathrm{msg}}\) from the global quasiprobability burden.

## 3. What currently only beats naive global quasiprobability sampling

The existing constant-boundary and path-active tree examples have low dense treewidth. They show

\[
\Lambda_{\mathrm{glob}}=\Theta(n),\qquad
\Lambda_{\mathrm{msg}}=O(1)\ \text{or}\ O(\log n),
\]

but they do not beat Markov--Shi-style dense tensor-network contraction, because the underlying tree graphs already have small dense width.

## 4. Dense Markov--Shi comparison

The manuscript currently does not prove a dense-width separation. It states the limitation correctly: if \(w_{\mathrm{eff}}=w_{\mathrm{TN}}\), the SLMS bound is not better than dense contraction. To upgrade this, I will add a stabilizer-grid construction whose dense contraction graph has grid treewidth \(\Theta(L)\), while the whole grid is a free stabilizer region and all attached resource gadgets are locally marginalized. This gives

\[
w_{\mathrm{TN}}^\ast=\Theta(L),\qquad
w_{\mathrm{eff}}+\Lambda_{\mathrm{msg}}=O(1)
\]

for an \(L\times L\) family, with \(\Lambda_{\mathrm{glob}}=\Theta(L^2)\). The claim will be scoped carefully: it separates SLMS parameters from dense treewidth bounds, not from arbitrary classical algorithms that also exploit stabilizer structure.

## 5. v0.4 upgrade to implement

I will implement all three requested directions:

A. Dense-width separation: add a theorem for a 2D stabilizer graph-state core with locally marginalized non-Clifford leaf gadgets. Prove the dense graph has grid treewidth \(\Theta(L)\), while \(w_{\mathrm{eff}}=O(1)\) and \(\Lambda_{\mathrm{msg}}=O(1)\).

B. Concrete QNLP instantiation: replace the informal grammar-tree example with a formal certified lambeq-style family proposition: bounded-arity parse trees, free grammatical reductions, locally measured lexical resource modules, and optional path-active semantic features.

C. Synthetic benchmark scaffold: add `run_examples.sh`, `plot_burdens.py`, `results/`, and generated CSV outputs for leaf-local, path-active, chain, clustered, and high-dense-width stabilizer-compressed accounting examples. These will be labelled as accounting diagnostics, not quantum simulation data.

I will also update the recurrence to include local norm factors \(\kappa_b\):

\[
\Gamma_b=\kappa_b\xi_b\prod_{c\in\operatorname{Act}(b)}\Gamma_c .
\]

This makes the certification algorithms and theorem statement match the appendix.
