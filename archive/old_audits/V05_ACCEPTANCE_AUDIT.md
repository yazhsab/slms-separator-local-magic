# V05 Acceptance Audit

Historical audit retained for provenance. It is superseded by `FINAL_ACCEPTANCE_AUDIT.md`; current proof, benchmark, and citation status should be read from the final audit and current TODO files.

## 1. Main Theorem Status

The main SLMS theorem is fully proved for locally marginalizable resource-decomposition networks with supplied or certified:

- rooted tree decomposition;
- local free-tensor quasiprobability `l1` costs `xi_b`;
- local coefficient-map factors `kappa_b`;
- active-child sets `Act(b)`;
- stabilizer-compressed effective width `w_eff`;
- polynomially describable local certificates.

The theorem is not a theorem for arbitrary compositional tensor networks.

## 2. Novelty Status

Genuinely new in this manuscript:

- the constructive separator-local message burden `Lambda_msg`;
- the active-child recurrence for locally marginalizable networks;
- the combined use of stabilizer-compressed width and message-local quasiprobability burden;
- parameter separations between global burden and message burden;
- a dense-treewidth versus stabilizer-compressed-width parameter separation.

Standard and cited:

- dense tensor-network width simulation;
- stabilizer/tableau simulation;
- stabilizer-rank, stabilizer-extent, robustness, and quasiprobability simulation;
- QNLP/DisCoCat/lambeq/QDisCoCirc background.

## 3. Dense-Width Comparison

The manuscript proves a parameter separation for a stabilizer graph-state grid with locally marginalized resource gadgets:

\[
w_{\mathrm{TN}}^*=\Theta(L),\qquad
w_{\mathrm{eff}}=O(1),\qquad
\Lambda_{\mathrm{msg}}=O(1).
\]

This is a separation from dense tensor-network width bounds and their cost expression. It is not a lower bound against all classical algorithms and not a lower bound against stabilizer-aware simulators.

## 4. QNLP Specialization

The manuscript covers a restricted certified grammar-tree family:

- bounded-arity parse trees;
- bounded type dimension and bounded feature wires;
- free grammatical reductions, cups, parity/copying maps, Clifford relation tensors, and certified classical stochastic maps;
- constant-size word or phrase resource modules with certified local `l1` costs;
- local consumption or bounded stabilizer-frame/classical message export;
- optional one active root-to-leaf semantic feature path.

It does not cover arbitrary lambeq ansaetze, arbitrary trained circuits, or general QDisCoCirc instances.

## 5. Benchmark Status

Status: scripts plus outputs for synthetic accounting only.

Implemented:

- `benchmarks/generate_tree_resource_network.py`;
- `benchmarks/compute_synthetic_burdens.py`;
- `benchmarks/certify_synthetic_lm.py`;
- `benchmarks/plot_burdens.py`;
- `benchmarks/run_examples.sh`;
- CSV outputs and SVG plots under `benchmarks/results/`.

Not implemented:

- full quantum-circuit simulation;
- real lambeq circuit extraction;
- measured runtime comparison;
- computed treewidth/branchwidth for all synthetic examples.

## 6. Overclaim Audit

Confirmed unsupported claims are not present in the manuscript:

- no unconditional quantum advantage claim;
- no legal-AI benefit claim;
- no all-QNLP or all-lambeq applicability claim;
- no lower bound against all classical algorithms;
- no empirical performance claim from the synthetic accounting scripts.

Negative statements denying these claims remain in the manuscript intentionally.

## 7. Quantum-Readiness Classification

Classification at that pass: expert-feedback-ready / possible arXiv-ready after final citation cleanup.

The current citation status has since been updated in `CITATION_AUDIT.md`. The remaining blockers are tracked in `FINAL_ACCEPTANCE_AUDIT.md`.

## 8. Remaining Blockers

- Implement at least one concrete stabilizer/tensor backend certificate check, or state certificate generation more clearly as input data.
- Add one non-stylized extracted lambeq or QDisCoCirc circuit satisfying the certificates, if QNLP relevance is to be strengthened before journal submission.
- Replace dense-width proxies in benchmarks with computed graph-width values where feasible.
