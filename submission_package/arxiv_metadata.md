# arXiv Metadata

## Title

Separator-Local Treewidth--Magic Simulation of Compositional Quantum Language Circuits

## Abstract

Structured quantum language circuits are often neither arbitrary quantum circuits nor purely tree-shaped tensor networks. They arise from grammatical, discourse, or document-level composition procedures that impose a contraction graph, while local word or relation ansatz choices may introduce non-Clifford resources. This paper develops SLMS as a certificate-based separator-local dequantisation criterion for a restricted class of tensor networks, not as a general-purpose simulator. The operational primitive is a finite certified free-tensor quasiprobability `l1` representation. For a rooted tree decomposition, local costs `xi_b`, certified local norm factors `kappa_b`, and certified active-child sets define a message burden `Lambda_msg(C, T)` by an explicit recurrence for message `l1` norms. We prove the resulting scalar-estimator simulation theorem only for locally marginalizable resource-decomposition networks, where inactive child subtrees are compressed or marginalized before their resource randomness crosses the parent separator. For such certified inputs, SLMS contracts stabilizer components using an effective stabilizer-compressed boundary width `w_eff` and samples only active quasiprobability variables. Output probabilities can be estimated to additive error `epsilon` and failure probability `delta` in time `poly(|C|) epsilon^{-2} log(1/delta) 2^{O(w_eff)} exp(2 Lambda_msg(C, T))`. We also give pedagogical examples separating `Lambda_msg` from global quasiprobability burden and a stabilizer-compressed grid example separating the certified SLMS parameter from dense treewidth bounds. These are parameter separations, not lower bounds against focused tree-width, ZX-calculus, stabilizer-rank, or stabilizer tensor-network simulators. A certified grammar-tree family is discussed as a restricted QNLP instantiation. No unconditional quantum advantage or general lambeq/QDisCoCirc coverage is claimed.

This abstract is synced from `main.tex` (no-macro rendering). Re-sync if `main.tex` is edited.

## Suggested Categories

- Primary: `quant-ph`
- Optional cross-list: `cs.CL` only if the authors want to emphasize the restricted compositional-language instantiation; otherwise use `quant-ph` only.

## Keywords

classical simulation; tensor networks; treewidth; stabilizer simulation; quasiprobability; magic resource theory; quantum natural language processing; compositional circuits

## Author Metadata

- Prabakaran Kannan (corresponding author), Department of Computer Science and Engineering, National Institute of Technology Puducherry, Karaikal 609609, India. Email: cs23d2005@nitpy.ac.in. ORCID: 0009-0008-0487-3825.
- Venkatesan M. Sundaram, Department of Computer Science and Engineering, National Institute of Technology Puducherry, Karaikal 609609, India. ORCID: 0000-0002-1651-7093.
- Prabhavathy P., School of Computer Science and Engineering, Vellore Institute of Technology, Vellore 632014, India. ORCID: 0000-0002-5982-8983.

Equal-contribution notes, acknowledgements, and funding statements: to be supplied by the authors before public release if desired.

## Code Availability

The repository contains synthetic burden-accounting scripts but not a full quantum-circuit simulator. State this explicitly if submitting with code.
