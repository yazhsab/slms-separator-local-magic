# Proof and Implementation TODOs

## Completed Proof Items

- [x] Choose the primary operational resource measure: certified free-tensor quasiprobability `l1` norm.
- [x] Replace the earlier `Lambda_sep` definition with the explicit `Gamma_b` recurrence and `Lambda_msg`.
- [x] Include local coefficient-map expansion factors `kappa_b` in the recurrence.
- [x] Distinguish dense tensor-network width `w_TN`, optimal dense width `w_TN^*`, and stabilizer-compressed effective width `w_eff`.
- [x] Prove free-region compression as a standard stabilizer/tableau simulation reduction.
- [x] Prove bag-local quasiprobability expansion.
- [x] Define locally marginalizable resource-decomposition networks.
- [x] Prove message `l1` and second-moment recurrence for the active-child model.
- [x] Prove the SLMS simulation theorem for locally marginalizable networks.
- [x] Prove the polynomial-time easy-regime corollary.
- [x] Prove non-scalar constant-boundary and path-active separations from naive global quasiprobability burden.
- [x] Prove the stabilizer-compressed parameter separation from dense treewidth bounds.
- [x] State the non-improvement condition for the uncompressed `w_eff = w_TN` regime.
- [x] Give a certified restricted grammar-tree / lambeq-style family satisfying local marginalizability.
- [x] Clarify the explicit runtime sampling factor `exp(2 Lambda_msg)` arising from the `Gamma_b^2` second-moment bound.
- [x] Separate root-scalar estimation from optional entrywise message-table estimation.
- [x] Add worked examples for the local coefficient expansion factor `kappa_b`.
- [x] Restrict algorithmic free-tensor representations to finite or effectively enumerable certified dictionaries.
- [x] Reframe the dense-grid result as a parameter separation rather than a computational lower bound.
- [x] Relabel the QDisCoCirc separator-burden conjecture as an open problem.
- [x] Add a synthetic lambeq-style diagnostic calculation with analytic `Lambda_glob`, `Lambda_msg`, and `w_eff`.

## Completed Repository Items

- [x] Add certification algorithms: CERTIFY-FREE-REGIONS, COMPUTE-WEFF-UPPER, CERTIFY-ACTIVE-CHILDREN, CERTIFY-L1-NONEXPANSIVE, and CERTIFY-LM.
- [x] Add a backend-specific certification appendix with tableau, classical stochastic, affine stabilizer, and local `1 -> 1` sufficient checks.
- [x] Add synthetic accounting scripts.
- [x] Generate CSV outputs and SVG accounting plots for the bundled synthetic examples.
- [x] Add referee-proof, novelty, citation, and acceptance-readiness audits.

## Still Open

- [ ] Implement a full tensor/stabilizer backend rather than only combinatorial burden accounting.
- [ ] Turn the sufficient certification algorithms into tested code for a concrete tableau/stabilizer-tensor backend.
- [ ] Give a non-stylized lambeq or QDisCoCirc instance whose extracted circuit satisfies the certificates.
- [ ] Replace dense-width proxy examples in benchmarks with computed treewidth/branchwidth values where feasible.
- [ ] Add real lambeq extraction code and diagnostic outputs if QNLP applicability is intended to be more than a certified family theorem.
- [ ] Final author-level bibliography spot-check before submission.

## Conjectural Generalization

- [ ] Prove or refute the broader separator-local factorization conjecture beyond locally marginalizable networks.
- [ ] Identify whether specific QDisCoCirc hardness constructions imply large dense width, large effective width, large message burden, or failure of local marginalizability.
- [ ] Determine whether there is a canonical separator-local magic monotone independent of a specified message-passing algorithm.

## Before Submission

- [ ] Decide whether to submit first as an arXiv preprint or proceed directly after external expert review.
- [ ] Confirm author metadata, acknowledgements, keywords, and final journal formatting.
- [ ] Keep benchmark language restricted to synthetic accounting unless a real simulator backend is added.
- [ ] Remove or downgrade every statement not covered by the main theorem or an explicitly labeled conjecture.
