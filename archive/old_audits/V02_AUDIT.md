# v0.2 Audit

Historical audit retained for provenance. It is superseded by `FINAL_ACCEPTANCE_AUDIT.md`; current proof, benchmark, and citation status should be read from the final audit and current TODO files.

## 1. Non-circularity audit

`Lambda_msg` is non-circular in v0.2. It is computed from:

- the rooted tree decomposition;
- local bag costs `xi_b`;
- active-child sets `Act(b)`;
- the explicit recurrence `Gamma_b = xi_b * product_{c in Act(b)} Gamma_c`.

The definition no longer refers to "valid message support sets" or to the existence of an estimator with the desired runtime. The theorem separately assumes/checks local marginalizability: inactive children must be locally compressed or marginalized, and local contraction maps must be `l1`-nonexpansive on normalized free representatives.

## 2. Markov--Shi audit

The paper now distinguishes ordinary dense tensor-network width `w_TN` from stabilizer-compressed effective width `w_eff`. It explicitly states that if `w_eff = w_TN` and `Lambda_msg > 0`, SLMS is not an asymptotic improvement over ordinary dense treewidth contraction. The result is positioned as useful when stabilizer compression gives `w_eff << w_TN`, when global magic is high but message burden is low, or when the goal is diagnostic resource localization rather than beating every tensor-network contraction method.

## 3. Proof audit

- Theorem 1, Free-region compression: standard reduction, proved.
- Lemma 2, Local quasiprobability expansion: proved.
- Definition 3, Constructive message burden: definition, non-circular recurrence.
- Lemma 4, Message expansion and second-moment recurrence: proved for locally marginalizable networks.
- Theorem 5, Constructive SLMS simulation theorem: proved under the locally marginalizable input promises.
- Corollary 6, Polynomial-time easy regime: proved.
- Proposition 7, Separation from naive global-magic sampling: proved for a simple locally measured leaf-resource family.
- Proposition 8, Non-improvement over dense treewidth in the uncompressed regime: proved.
- Conjecture 1, General separator-local factorization: conjecture.
- Proposition 9, QNLP specialization: proved as an application of Theorem 5 under local marginalizability.
- Conjecture 2, Hard QDisCoCirc regimes and separator burden: conjecture.

## 4. Novelty audit

The v0.2 contribution differs from Markov--Shi treewidth contraction by separating dense contraction width from stabilizer-compressed effective width. Markov--Shi treats the network as dense tensors and gives a cost exponential in dense contraction width. SLMS is not claimed to improve that theorem in general; it applies when free stabilizer structure reduces the active boundary dimension or when resource localization gives a better diagnostic parameter.

The contribution differs from global stabilizer-rank, stabilizer-extent, and quasiprobability simulation by replacing a global product of all local magic costs with a certified message recurrence. In locally marginalizable networks, resource costs from inactive child subtrees are paid locally and do not multiply into every ancestor message. The toy separation demonstrates this restricted but concrete advantage over naive global sampling.

The contribution is orthogonal to Laakkonen--Meichanetzidis--Coecke QDisCoCirc hardness. LMC gives conditional qualitative hardness for certain compositional text-processing tasks. This paper proves an easy-regime simulation theorem under explicit local marginalizability promises and does not claim a hardness dichotomy.

The contribution also differs from standard dequantization papers. It does not dequantize a proposed application by exposing low rank or sampling assumptions. It provides a resource-localized simulation parameter for a structured circuit family and states when this parameter is, and is not, better than existing simulation baselines.

## 5. Submission readiness

Status: ready for internal review, not ready for Quantum submission.

The restricted theorem is now defensible, but the paper still needs stronger examples, concrete certification algorithms for `w_eff` and active-child conditions, a final operational magic measure, and manual citation verification. It is closer to an arXiv preprint candidate than v0.1, but it should not be submitted to *Quantum* until the examples and certification layer are substantially strengthened.
