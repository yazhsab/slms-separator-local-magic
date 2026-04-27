# Final Acceptance Audit

## 1. Main Theorem

Statement: For locally marginalizable resource-decomposition networks with certified free-tensor quasiprobability costs `xi_b`, local coefficient factors `kappa_b`, active-child sets, and stabilizer-compressed width `w_eff`, SLMS estimates output probabilities with runtime

\[
\widetilde O(\mathrm{poly}(|C|)\epsilon^{-2}\log(1/\delta)
2^{O(w_{\mathrm{eff}})}
\exp(2\Lambda_{\mathrm{msg}})).
\]

With `Lambda_msg = max_b log Gamma_b`, the explicit Monte Carlo sampling term is `epsilon^{-2} exp(2 Lambda_msg) log(1/delta)`. The manuscript now displays this factor explicitly rather than hiding it in big-O notation.

Proof status: fully proved for the restricted locally marginalizable class.

Remaining assumptions: supplied or certified tree decomposition, resource assignment, local expansions, active-child/local marginalization certificates, coefficient-norm bounds, and polynomially describable certificates.

## 2. Novelty

Genuinely new:

- explicit message burden `Lambda_msg` defined by an active-child recurrence;
- active-child recurrence for locally marginalizable networks;
- combination of stabilizer-compressed effective width and message-local quasiprobability burden;
- pedagogical examples separating global magic burden and message burden;
- stabilizer-compressed parameter separation from dense treewidth bounds.

Standard and cited:

- Markov--Shi dense treewidth simulation;
- Gottesman--Knill/tableau stabilizer simulation;
- stabilizer-rank, robustness, and quasiprobability simulation;
- QNLP/DisCoCat/lambeq/QDisCoCirc background;
- dequantization/QML simulability context.

## 3. Dense-Width Separation

Exact result: Proposition `thm:dense-width-separation` gives an \(L\times L\) stabilizer graph-state core with locally marginalized non-Clifford leaf gadgets and

\[
w_{\mathrm{TN}}^\ast=\Theta(L),\qquad
w_{\mathrm{eff}}=O(1),\qquad
\Lambda_{\mathrm{msg}}=O(1).
\]

What it proves: a parameter separation between dense tensor-network width bounds and stabilizer-compressed separator-local simulation bounds.

What it does not prove: no lower bound against all classical algorithms; no lower bound against stabilizer-aware simulators; no complexity-theoretic separation.

## 4. QNLP Specialization

Covered family: bounded-arity grammar-tree / lambeq-style circuits with bounded type dimension, free grammatical reductions and relation maps, constant-size local resource modules, local consumption or bounded stabilizer-frame/classical message export, and optional one active semantic path.

Additional diagnostic: the manuscript includes a synthetic lambeq-style transitive sentence calculation with free noun/evaluation tensors, constant-size adverb and verb resource modules, and analytic values for `Lambda_glob`, `Lambda_msg`, and `w_eff`. It is explicitly not empirical lambeq data.

Not covered: arbitrary lambeq ansaetze, arbitrary trained QNLP circuits, general QDisCoCirc circuits, or QDisCoCirc hardness constructions.

## 5. Benchmarks

Status: scripts plus outputs for synthetic accounting. Plot generation support is included; generated plots are treated as optional diagnostics.

The manuscript claims match the repository:

- scripts exist;
- `run_examples.sh` regenerates CSV outputs;
- `summary.csv` matches the manuscript table;
- SVG plots exist;
- the manuscript labels all outputs as synthetic accounting diagnostics, not empirical runtime data.

## 6. Citation Status

Status: verified for the present bibliography using publisher, arXiv, dblp, PubMed, or institutional metadata where available. The referee-hardening pass added modern tensor-network comparators: Vidal 2003, Schollwoeck 2011, and Tindall--Fishman--Stoudenmire--Sels 2024.

No entries are currently marked `VERIFY` in `CITATION_AUDIT.md`. A final author-level spot-check is still recommended before submission.

## 7. Source Package Status

Status: compiles.

Command tested:

```sh
latexmk -pdf -interaction=nonstopmode main.tex
```

The final log scan found no undefined references, no undefined citations, no overfull boxes, and no LaTeX errors.

## 8. Overclaim Audit

Confirmed no unsupported:

- quantum advantage claim;
- legal AI benefit claim;
- all-QNLP applicability claim;
- lower bound against all classical algorithms;
- empirical performance claim.

Remaining uses of `advantage`, `speedup`, and `legal` are negative claims or prior-work/benchmark-context statements.

## 9. Submission Readiness Classification

expert-review ready.

The package is not marked as a Quantum submission candidate because a full stabilizer/tensor backend implementation, external expert review, and a non-stylized extracted lambeq/QDisCoCirc certificate example would materially strengthen the journal case. It is close to arXiv-ready pending final author-level citation spot-check and release decision.

## 10. Remaining Blockers

- Confirm final author names, affiliations, acknowledgements, and funding statements.
- Perform final author-level citation spot-check.
- Decide whether to submit to arXiv before journal review.
- Implement at least one concrete stabilizer/tensor backend certificate checker for stronger Quantum submission readiness.
- Add a non-stylized extracted lambeq or QDisCoCirc example satisfying the certificates if QNLP relevance is to carry more weight.
- Replace synthetic width proxies with computed graph-width values where feasible.
