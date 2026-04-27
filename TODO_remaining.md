# TODO Remaining

Status reflects work executed in the 2026-04-26 implementation session.

## Resolved in this session

- [x] **Exact focused tree-width and focused rank-width** are now computed in
  `experiments/slms_certificate/focused_width.py` per Codsi--Laakkonen
  Definitions 13 and 14. Focused tree-width is exact via balanced-separator
  enumeration for instances with up to 22 vertices, and a heuristic upper
  bound otherwise. Focused rank-width is exact for `|S| <= 4` and a tight
  upper bound otherwise via recursive bipartition over GF(2) cut-rank.
  The Codsi--Laakkonen Theorem 8 runtime exponent
  `(log_{3/2} 4) * frw_S * log|S|` is reported per instance.
- [x] **ZX numerical baseline** implemented in
  `experiments/slms_certificate/zx_baseline.py` using `pyzx 0.10.0`'s
  `simplify.full_reduce` on a synthetic Clifford+T encoding of each instance,
  combined with the Bravyi--Gosset stabilizer-rank exponent constant
  alpha = 0.396.  The Sutcliffe--Kissinger cutting and parametric-rewriting
  baselines are NOT invoked; only `full_reduce` is run.
- [x] **ZX partition diagnostic** implemented in
  `experiments/slms_certificate/zx_partition_baseline.py`. It runs after pyzx
  `full_reduce` and reports a conservative k-partition score for `k <= 4`.
  This is a reproducible heuristic diagnostic, NOT the Sutcliffe--Kissinger
  cutting or parametric-rewriting algorithm.
- [x] **STN-style upper bound** implemented in
  `experiments/slms_certificate/stn_baseline.py` as
  `alpha_BG * T + log(active_resource_count)` natural-log exponent. Explicitly
  NOT a re-implementation of the Masot-Llima or Nakhl algorithms; it is an
  STN-inspired upper-bound proxy for the synthetic Clifford+T encoding, not a
  lower bound on all stabilizer-tensor-network simulators.
- [x] **Wall-clock microbenchmarks** for focused tree-width, focused
  rank-width, pyzx full_reduce, the STN-style proxy, and the SLMS scalar
  estimator are recorded per instance in `results/slms_certificate_results.csv`
  (columns `focused_widths_seconds`, `zx_seconds`, `stn_seconds`) and in
  `results/slms_scalar_estimator_results.csv`.
- [x] **Empirical SLMS-vs-comparator evidence** on the 120 fallback
  instances: SLMS exponent `w_eff + 2*Lambda_msg` is strictly smaller than
  the Codsi--Laakkonen Theorem 8 exponent diagnostic on 101/120 instances,
  smaller than the pyzx full_reduce + Bravyi--Gosset exponent on 66/120,
  smaller than the pyzx k-partition heuristic on 66/120, and smaller than the
  STN-style upper bound on 69/120. These are exponent-bound comparisons on a
  fixed synthetic encoding; they are NOT proofs of separation and NOT
  wall-clock simulator comparisons.
- [x] **"Certificate failure is sufficient-condition failure, not quantum
  hardness"** framing lifted into `main.tex` abstract and Section 1
  ("What is not claimed").
- [x] **Parser/QDisCoCirc and end-to-end SLMS wall-clock blockers are now
  executable checks**, not just prose. `qnlp_extraction_probe.py` writes
  `results/qnlp_extraction_probe.json`; `end_to_end_slms_wallclock.py` writes
  `results/end_to_end_slms_wallclock.json` and refuses to benchmark fallback
  or LinearReader graph-only data as real QNLP resource instances.

## Still missing or upstream-blocked

- [ ] **Parser-generated lambeq evidence is blocked.** lambeq 0.5.0 attempts
  Bobcat model retrieval from
  `https://qnlp.cambridgequantum.com/models/bobcat/latest/version.txt`, and
  the audited run failed before parser construction completed. `pip install
  depccg` failed during wheel-requirement discovery because the build requested
  Cython and NumPy before compiling extension modules, and `DepCCGParser` then
  failed with `ModuleNotFoundError: No module named 'depccg'`. WebParser failed
  against the lambeq web service in the verified run. `cups_reader` produces
  120 LinearReader graph-only diagrams that contain no non-Clifford resource
  annotations. See `lambeq_parser_blocker_report.md`.
- [ ] **Strict separation theorem against focused tree-width / ZX / STN /
  MAST is not proved.** The artifact reports empirical exponent comparisons
  on 120 fallback instances, but no family is exhibited with provably small
  `w_eff + 2 Lambda_msg` and provably large focused tw / rw / ZX-rank / STN
  bond dimension. Proving such a separation is a research project beyond
  the scope of this artifact.
- [ ] **Exact Sutcliffe--Kissinger ZX partitioning/cutting, exact STN, and
  MAST baselines are not implemented.** The pyzx full_reduce baseline, a pyzx
  k-partition heuristic, and the STN upper-bound proxy are reported. Faithful
  re-implementations of the Sutcliffe--Kissinger 2024 and 2025 algorithms,
  the Masot-Llima--Garcia-Saez 2024 STN algorithm, and the Nakhl et al.\
  2025 magic-state-injection STN algorithm are out of scope here.
- [ ] **Fallback structured instances and lambeq LinearReader graph-only
  instances do not establish parser-level QNLP or QDisCoCirc coverage.**
  The QNLP claims in the manuscript are bounded by the certified
  grammar-tree family of Proposition 13 and the synthetic transitive-sentence
  diagnostic in Section 7. Generalisation to trained QNLP ansaetze remains
  open.
- [ ] **Wall-clock benchmark on a full SLMS simulator backend on real QNLP
  circuits is not provided.** The artifact provides per-instance wall-clock
  timings for the focused-width, pyzx, STN-proxy, and signed-sampling
  microbenchmarks, but not for an end-to-end SLMS simulator on
  parser-generated lambeq circuits, which would require resolving the
  upstream parser block above.
- [ ] **Public artifact DOI pending.** The manuscript contains placeholders
  `[Zenodo DOI to be inserted after release]` and `[GitHub URL to be inserted
  after release]`. Do not replace them until a real GitHub release and Zenodo
  DOI exist.
