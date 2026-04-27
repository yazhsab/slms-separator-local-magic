# Major Revision Changelog

## Claim Framing

- Reframed SLMS as a certificate-based separator-local dequantisation and simulation criterion for locally marginalizable resource-decomposition networks.
- Removed language suggesting a broad new general-purpose simulator.
- Made clear that dense-grid and global-magic examples are parameter/accounting examples, not state-of-the-art simulation separations.

## Runtime and Theorem

- Changed the main theorem display from `exp(O(Lambda_msg))` to the explicit scalar-sampling factor `exp(2 Lambda_msg)`.
- Clarified that the proved theorem estimates a scalar root probability.
- Separated optional message-table estimation from the scalar theorem and noted the additional table-dimension and error-propagation costs.

## Related Work

- Added explicit comparison to focused tree-width/focused rank-width, low-rank-width ZX simulation, ZX cutting and partitioning, stabilizer tensor networks, and magic-state-injection stabilizer tensor networks.
- Added references for Codsi--Laakkonen 2026, Kuyanov--Kissinger 2026, Sutcliffe/Kissinger ZX work, Masot-Llima--Garcia-Saez, and Nakhl et al.

## QNLP Positioning

- Tightened lambeq/QDisCoCirc claims to certified grammar-tree and warm-start/easy subclasses.
- Added explicit warnings that continuous trainable rotations and high-level entangling relation tensors may violate local marginalizability.

## Benchmarks and Reproducibility

- Updated synthetic accounting scripts and tables so the SLMS exponent proxy is `w_eff + 2 Lambda_msg`.
- Added a required empirical validation section specifying real lambeq/QDisCoCirc extraction, dense tensor-network, global quasiprobability, focused-width/ZX, and stabilizer tensor-network baselines.

## Appendix

- Added a fully worked two-leaf certificate example specifying `T`, `w_TN`, `w_eff`, `xi_b`, `kappa_b`, `Act(b)`, `Lambda_glob`, and `Lambda_msg`.

## 2026-04-26 baseline-implementation pass

- Implemented exact focused tree-width and focused rank-width computation per Codsi--Laakkonen Definitions 13 and 14 in `experiments/slms_certificate/focused_width.py`. Exact for `n <= 22` (focused tree-width) and `|S| <= 4` (focused rank-width); honest upper bound otherwise.
- Implemented a ZX baseline using `pyzx 0.10.0`'s `simplify.full_reduce` plus the Bravyi--Gosset stabilizer-rank exponent constant `alpha = 0.396` in `experiments/slms_certificate/zx_baseline.py`. Operates on a synthetic Clifford+T encoding of each instance.
- Implemented a stabilizer-tensor-network upper-bound proxy in `experiments/slms_certificate/stn_baseline.py` (tableau plus Bravyi--Gosset). Explicitly NOT a re-implementation of the Masot-Llima--Garcia-Saez or Nakhl algorithms.
- Wired the new comparators into `baselines.py` and `run_all.py`. Per-instance wall-clock seconds are recorded for focused widths, pyzx, the STN proxy, and the SLMS scalar estimator.
- Empirical SLMS-vs-comparator counts on the 120 fallback instances after the latest rerun: SLMS exponent strictly smaller than the Codsi--Laakkonen Theorem 8 exponent diagnostic on 101/120; smaller than pyzx full_reduce + Bravyi--Gosset on 66/120; smaller than the pyzx k-partition heuristic on 66/120; smaller than the STN-style upper bound on 69/120. Reported in Section 8 with explicit "not a separation proof" disclaimer.

## 2026-04-26 framing and documentation

- Documented the parser-level lambeq upstream block in `notes/gap1_parser_block.md`: NXDOMAIN on `qnlp.cambridgequantum.com`, lambeq GitHub issues #253, #254, #257 (all open).
- Updated Section 8 with the concrete BobcatParser/DepCCGParser/WebParser failure modes and a new "Comparison baselines" subsection covering Codsi--Laakkonen, ZX, and STN-style numerical exponents.
- Updated Section 9 with the exact upstream block details and per-baseline exactness/upper-bound flags.
- Lifted "certificate failure is sufficient-condition failure, not quantum hardness" framing into the abstract and Section 1's "What is not claimed" paragraph.
- Archived the stale Python-3.14 fallback-only manifest set to `archive/stale_run_py314/`.
