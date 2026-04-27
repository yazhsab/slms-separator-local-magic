# v0.4 Audit

Historical audit retained for provenance. It is superseded by `FINAL_ACCEPTANCE_AUDIT.md`; current proof, benchmark, and citation status should be read from the final audit and current TODO files.

## 1. Dense contraction comparison

The paper now proves a parameter separation from dense tensor-network width in Theorem `Stabilizer-compressed dense-width separation`.

Construction: an \(L\times L\) stabilizer graph-state core with a constant-size locally measured non-Clifford gadget attached at each grid site.

Scaling:

\[
w_{\mathrm{TN}}^\ast=\Theta(L),\qquad
w_{\mathrm{eff}}=O(1),\qquad
\Lambda_{\mathrm{msg}}=O(1),\qquad
\Lambda_{\mathrm{glob}}=\Theta(L^2).
\]

Assumptions and scope: this separates dense treewidth parameters from stabilizer-compressed separator-local parameters. It is not a lower bound against arbitrary classical algorithms, because stabilizer-aware simulators can also exploit the graph-state core.

## 2. Global magic comparison

The paper proves separation from naive global quasiprobability burden using non-scalar messages.

- Constant-boundary tree family: each \(|T\rangle\)-type resource is locally measured and exports a one-bit classical stabilizer message. Scaling: \(\Lambda_{\mathrm{glob}}=\Theta(n)\), \(\Lambda_{\mathrm{msg}}=O(1)\).
- Path-active tree family: resources occur at leaves and along one active path. Off-path resources are locally marginalized. Scaling: \(\Lambda_{\mathrm{glob}}=\Theta(n)\), \(\Lambda_{\mathrm{msg}}=O(\log n)\).

These are separations from global-magic sampling. Only the stabilizer-grid theorem separates from dense treewidth parameters.

## 3. QNLP instantiation

The paper now defines a certified lambeq-style locally marginalizable family:

- bounded-arity parse trees;
- bounded grammatical type dimensions;
- free/stabilizer grammatical reductions and phrase maps;
- resource lexical modules at leaves;
- each resource module is locally measured by a stabilizer instrument and exports a bounded classical stabilizer feature message;
- optionally one bounded semantic feature remains active along one root-to-leaf path.

Scaling: \(\weff=O(1)\), and \(\Lambda_{\mathrm{msg}}=O(1)\) without an active path or \(O(\log n)\) on balanced trees with one active path.

This does not cover arbitrary lambeq ansätze or general QDisCoCirc circuits.

## 4. Certification algorithms

Algorithmic sufficient checks now appear in Appendix F:

- CERTIFY-FREE-REGIONS: syntactic free-region component extraction.
- COMPUTE-WEFF-UPPER: separator active-boundary counting after tableau/affine compression.
- CERTIFY-ACTIVE-CHILDREN: bottom-up inactive-child checks.
- CERTIFY-L1-NONEXPANSIVE: local \(1\to1\) coefficient-map norm bound, producing \(\kappa_b\).

Still input promises rather than implemented backend code:

- exact tableau data structure;
- stabilizer membership checks for arbitrary boundary tensors;
- optimized resource decompositions;
- tree decompositions;
- non-stylized lambeq/QDisCoCirc extraction.

## 5. Proof status table

- Free-region compression theorem: standard stabilizer-simulation reduction, proved at theorem level.
- Local quasiprobability expansion lemma: proved.
- Constructive message burden definition with \(\kappa_b\): definition.
- Message expansion and second-moment recurrence: proved for locally marginalizable networks with certified \(\kappa_b\).
- Constructive SLMS simulation theorem: proved under local marginalizability and supplied certificates.
- Polynomial-time easy regime corollary: proved.
- Constant-boundary global-magic separation: proved example.
- Path-active global-magic separation: proved example.
- Stabilizer-compressed dense-width separation: proved parameter-separation example; not a lower bound against arbitrary stabilizer-aware algorithms.
- Non-improvement over dense treewidth in the uncompressed regime: proved.
- QNLP specialization proposition: conditional application of the main theorem.
- Certified lambeq-style locally marginalizable family: proved for the restricted family.
- Hard QDisCoCirc regimes and separator burden: conjecture.
- General separator-local factorization: conjecture.

## 6. Quantum readiness

Classification: expert-feedback-ready, not Quantum submission candidate.

The draft now has a cleaner theorem stack, non-scalar global-magic separations, a dense-treewidth parameter separation, a concrete restricted QNLP family, and reproducible synthetic accounting outputs. Remaining blockers for a Quantum submission are:

- citation verification;
- tested stabilizer/tableau backend implementation;
- actual lambeq/QDisCoCirc circuit extraction satisfying the certificates;
- replacing width proxies in synthetic benchmarks with computed treewidth/branchwidth where feasible;
- final pass to remove or downgrade claims not covered by the constructive theorem.
