# v0.5 Acceptance Hardening Plan

## 1. Current main theorem

The main theorem is the constructive SLMS simulation theorem for locally marginalizable resource-decomposition networks. Given a rooted tree decomposition, certified local free-tensor quasiprobability costs \(\xi_b\), certified local coefficient-map factors \(\kappa_b\), active-child certificates \(\operatorname{Act}(b)\), and stabilizer-compressed effective width \(w_{\mathrm{eff}}\), the message recurrence is

\[
\Gamma_b=\kappa_b\xi_b\prod_{c\in\operatorname{Act}(b)}\Gamma_c,
\qquad
\Lambda_{\mathrm{msg}}=\max_b\log\Gamma_b.
\]

The theorem estimates output probabilities with runtime

\[
\widetilde O(\operatorname{poly}(|C|)\epsilon^{-2}\log(1/\delta)
2^{O(w_{\mathrm{eff}})}\exp(O(\Lambda_{\mathrm{msg}}))).
\]

## 2. Current novelty claim

The novelty is not a new stabilizer simulator or a new tensor-network contraction theorem. It is a certified tree-decomposition message recurrence that combines:

- stabilizer/free-region compression;
- local quasiprobability costs;
- local norm factors;
- active-child marginalization certificates.

The paper separates global non-stabilizer burden from message-local burden and dense treewidth parameters from stabilizer-compressed effective width.

## 3. Current dense-width separation claim

The manuscript includes a stabilizer-grid parameter separation. An \(L\times L\) graph-state core has dense treewidth \(\Theta(L)\). Attached local resource gadgets are marginalized before entering grid separators. The certified parameters satisfy

\[
w_{\mathrm{eff}}=O(1),\qquad \Lambda_{\mathrm{msg}}=O(1),\qquad
\Lambda_{\mathrm{glob}}=\Theta(L^2).
\]

This is a separation from dense treewidth bounds, not a lower bound against all classical algorithms.

## 4. Current QNLP/lambeq instantiation claim

The manuscript defines a restricted certified lambeq-style family: bounded-arity parse trees, bounded type dimensions, free grammatical reductions, local resource word modules, local stabilizer measurement/export of feature messages, and optional one-path active semantic features. It does not cover arbitrary lambeq ansätze or general QDisCoCirc circuits.

## 5. Current benchmark/code claims

The repository contains synthetic accounting scripts, generated CSV outputs, and SVG plots under `benchmarks/results/`. These are not runtime experiments or quantum-circuit simulations. They compute burden and exponent proxies for five synthetic cases.

## 6. Known weaknesses a Quantum referee may attack

- The free-region compression theorem is standard Gottesman--Knill/tableau simulation and must be framed as such.
- The main theorem is certificate-based; optimal certificate generation is not implemented.
- The dense-width separation uses a graph-state stabilizer core, which is already stabilizer-simulable. This must be framed as the point of the parameter separation, not hidden.
- The QNLP family is restricted and stylized; the paper must not imply broad lambeq or QDisCoCirc coverage.
- Synthetic benchmarks use width proxies, not measured runtime or computed treewidth.
- Citations have not yet been fully verified.
- README and TODO files still contain older version language that may contradict the current manuscript status.

## 7. Exact hardening edits

I will:

1. Create `REFEREE_PROOF_AUDIT.md` and update theorem/proof wording where needed.
2. Create `NOVELTY_POSITIONING.md` and insert a concise "not just Gottesman--Knill plus local sampling" subsection.
3. Rename/soften the dense-width theorem title to emphasize parameter separation, add a caveat paragraph, and add a corollary about superpolynomial dense-width upper bounds versus polynomial SLMS bounds.
4. Tighten the certified lambeq-style proposition and its limitations.
5. Verify benchmark scripts run and align manuscript language with existing outputs.
6. Remove manuscript-body version/development-log language and update TODO/README consistency.
7. Create `CITATION_AUDIT.md`; verify what can be verified locally and mark uncertain items `VERIFY`.
8. Create `TODO_submission.md`.
9. Create `submission_package/` with editor/referee/arXiv support files.
10. Create `V05_ACCEPTANCE_AUDIT.md`.
11. Run `bash benchmarks/run_examples.sh`, LaTeX compilation, and overclaim/version-language audits.
