# v0.2 Upgrade Plan

## 1. What is currently proved

- The free-region compression / Clifford absorption statement is a standard stabilizer-simulation reduction once the free tensor class and boundary convention are fixed.
- The bag-local quasiprobability expansion lemma is proved by tensoring local decompositions and multiplying their `l1` costs.
- The variance lemma is a standard Monte Carlo concentration statement conditional on an unbiased estimator with the asserted second-moment bound.

## 2. What is conditional

- The current main theorem is conditional on the separator-factorization lemma.
- The QDisCoCirc specialization is conditional on the same separator-factorization hypothesis.
- The improvement-over-global-magic proposition is only a proof target, not an explicit construction.

## 3. What risks circularity

- `Lambda_sep` is currently defined using "valid message support sets."
- Validity is defined by the existence of a message estimator whose overhead is already controlled by the product of costs in the chosen support set.
- This makes the parameter nonconstructive and close to circular: the theorem assumes the same property it wants to prove.

## 4. What risks being subsumed by ordinary tensor-network contraction

- The current width parameter `w` is essentially an ordinary dense separator width.
- If `w = w_TN`, Markov--Shi-style tensor-network contraction gives `poly(|C|) 2^{O(w_TN)}` without an extra magic factor.
- Therefore the paper must distinguish ordinary dense width `w_TN` from stabilizer-compressed effective width `w_eff`, and must state that improvement over ordinary contraction requires `w_eff + Lambda_msg << w_TN` or a different comparison target such as global-magic sampling.

## 5. The theorem to prove in v0.2

I will prove a restricted constructive theorem for normalized locally marginalizable resource-decomposition networks.

The new theorem will use:

- a rooted tree decomposition;
- local bag quasiprobability costs `xi_b`;
- certified active-child sets `A_b`;
- a constructive recurrence

  `Gamma_b = xi_b * product_{c in A_b} Gamma_c`

  with inactive children required to be locally marginalized into normalized free or dense boundary messages before reaching `b`;

- `Lambda_msg(C,T) = max_b log Gamma_b`;
- a stabilizer-compressed boundary width `w_eff`, distinct from ordinary dense width `w_TN`.

This theorem is narrower than the original conjectural separator-local theorem, but it is non-circular and provable. It yields the path-local bound as the special case `|A_b| <= 1`, and the global product bound as the special case where all children are active.

