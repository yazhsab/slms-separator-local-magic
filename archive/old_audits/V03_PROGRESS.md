# v0.3 Work-in-Progress Notes

## Completed in this pass

- Fixed the theorem-level operational magic measure to the certified free-tensor quasiprobability `l1` norm.
- Added certification procedures to the SLMS algorithm section:
  - free-region detection;
  - effective-width upper bound;
  - inactive-child marginalization check;
  - local `1 -> 1` norm check;
  - greedy active-child selection.
- Replaced the scalar separation with a non-scalar constant-boundary family:
  - each leaf consumes a `|T>` resource by Pauli measurement;
  - the leaf exports a one-bit classical stabilizer boundary message;
  - internal nodes combine messages by Clifford XOR maps;
  - `Lambda_glob = Theta(n)` but `Lambda_msg = O(1)`.
- Added `benchmarks/certify_synthetic_lm.py` to mirror active-child certification on synthetic tree/resource instances.
- Added a path-active separation family: leaf resources give \(\Lambda_{\mathrm{glob}}=\Theta(n)\), while one unresolved path gives \(\Lammsg=O(\log n)\).
- Added a stylized grammar-tree QNLP example with locally measured lexical resources and Clifford phrase composition.
- Added Appendix F with backend-specific sufficient certification checks for tableau, classical stochastic, affine stabilizer, and local \(1\to1\) norm cases.
- Extended the synthetic generator with `leaf-plus-path` placement and `off-path` marginalization mode.

## Still pending

- Actual tensor/stabilizer runtime experiments.
- Turning the certificate algorithms into executable tableau/stabilizer-tensor code.
- A non-stylized lambeq/QDisCoCirc extracted example satisfying the certificates.

## Current readiness

The manuscript is stronger than v0.2 but remains an internal-review draft. The main theorem is cleaner, and the separation example is less trivial, but the paper is still not ready for *Quantum* without backend-specific certificates and at least one QNLP-shaped worked example.
