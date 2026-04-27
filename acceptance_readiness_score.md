# Acceptance Readiness Score

Date: 2026-04-26 (post baseline-implementation pass).

## Scores

1. Theorem correctness: 82/100
2. Novelty after prior art: 72/100
3. Real evidence: 50/100  *(unchanged: parser-level lambeq still upstream-blocked)*
4. Artifact completeness: 91/100  *(+1: QNLP blocker probe and wall-clock gate are executable)*
5. Baseline comparison: 84/100  *(+2: pyzx k-partition heuristic added; exact Sutcliffe--Kissinger still missing)*
6. QNLP relevance: 52/100
7. Clarity and honesty: 90/100  *(+2: failure-not-hardness lifted into intro/abstract; parser and exact-baseline blockers now documented without converting proxies into resolved evidence)*
8. Venue fit: 72/100

Overall current grade: 77/100.

## Current Grade

Improved post-revision: the artifact now computes Codsi--Laakkonen focused tree-width and focused rank-width per Definitions 13/14 (exact for small instances, honest upper bound otherwise), runs a pyzx `full_reduce` ZX baseline with Bravyi--Gosset stabilizer-rank exponent, adds a pyzx k-partition heuristic, reports a tableau-plus-Bravyi--Gosset STN-style upper bound (explicitly NOT the Masot-Llima or Nakhl algorithm), and records per-instance wall-clock timings for each. On the 120 fallback instances the SLMS exponent `w_eff + 2*Lambda_msg` is strictly smaller than the Codsi--Laakkonen Theorem 8 exponent diagnostic on 101/120, smaller than pyzx + Bravyi--Gosset on 66/120, smaller than the pyzx k-partition heuristic on 66/120, and smaller than the STN-style upper bound on 69/120. These are exponent-bound diagnostics; no separation theorem is proved.

The remaining low score on "real evidence" is dominated by the parser-level lambeq block: Bobcat model retrieval failed, DepCCG did not build/install in the audited Python 3.11 environment, WebParser did not parse the sample sentence, and no QDisCoCirc package candidate was importable. The artifact cannot extract CCG-parsed sentence circuits until a working parser/model or serialized parser-output dataset is supplied.

## Best Venue Target

QPL-ready, possibly TQC-ready as a theory-plus-artifact submission. Quantum-journal submission is plausible but borderline: a referee can object that the empirical comparator evidence is on synthetic Clifford+T encodings of fallback graph structures, not on parser-generated QNLP circuits. The honest framing in Sections 8, 9, and the abstract makes that objection straightforward to address in a revise-and-resubmit.

## Remaining Blockers to 90% Acceptance Probability

- Resolve the parser/model block so that real CCG-parsed lambeq circuits can be extracted with non-Clifford resource annotations.
- Implement the exact Sutcliffe--Kissinger ZX cutting/parametric algorithms, or arrange access to a public reference implementation.
- Implement the Masot-Llima and Nakhl STN algorithms, or arrange a faithful comparison.
- Provide a strict separation theorem (a circuit family with provably small `w_eff + 2 Lambda_msg` and provably large focused tw / rw / ZX-rank / STN bond dimension).
- Provide stronger evidence that natural QNLP circuits satisfy nontrivial local marginalization certificates.
