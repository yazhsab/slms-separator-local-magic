# Reviewer Response Memo

## Criticism: Active-child recurrence is just junction-tree DP.

Response: The paper now states this directly. The contribution is clarified as a checkable sufficient certificate that lifts a junction-tree-style collect recurrence with quasiprobability sampling, stabilizer compression, local norm factors, and local marginalization semantics.

## Criticism: No real QNLP evidence.

Response: A real lambeq pipeline, environment checker, and QNLP extraction probe were added. A Python 3.11 environment now imports lambeq. Parser execution still failed: Bobcat model retrieval failed, WebParser failed on the sample corpus, and DepCCG dependencies did not install cleanly. QDisCoCirc package candidates are also unavailable in this environment. The pipeline records 120 lambeq LinearReader graph-only diagrams from `cups_reader`, but labels them as reader sidecar/plumbing evidence rather than parser-level QNLP evidence. The nontrivial resource evidence remains fallback structured instances.

## Criticism: Synthetic accounting only.

Response: The repository now includes an executable certificate pipeline, environment reports, fallback instance JSON, result CSVs, plots, tests, run manifest, failure report, a worked certificate appendix, a dense contraction microbenchmark, and a scalar-estimator microbenchmark.

## Criticism: No baseline comparison.

Response: Implemented baseline rows now include dense TN, global PWB, naive hybrid, SLMS, a legacy focused-width proxy, Codsi--Laakkonen focused tree-width/rank-width diagnostics, a pyzx `full_reduce` + Bravyi--Gosset ZX-inspired exponent proxy, a pyzx k-partition heuristic, and a tableau + Bravyi--Gosset STN-style upper-bound proxy. Exact Sutcliffe--Kissinger ZX cutting/partitioning and exact Masot-Llima/Nakhl STN or MAST baselines remain non-implemented rows with limitations.

## Criticism: Focused-width may dominate.

Response: The paper now explicitly avoids dominance claims. The artifact computes focused tree-width/rank-width diagnostics exactly only for small cases and reports upper bounds otherwise; the text frames comparisons as diagnostics, not separations or dominance over focused-width simulation.

## Criticism: No artifact.

Response: Added a reproducibility package under `experiments/slms_certificate/`, root-level `results/` and `figures/`, `artifact_manifest.md`, `build_report.md`, tests, and exact run logs.
