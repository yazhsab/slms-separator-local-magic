# Remaining Blockers Status

Date: 2026-04-26

## Parser-generated lambeq / QDisCoCirc resource instances

Status: still blocked, now executable.

Actions taken:
- `experiments/slms_certificate/qnlp_extraction_probe.py` added.
- `results/qnlp_extraction_probe.json` and `.md` generated.
- Existing lambeq 0.5.0 environment imports successfully.
- lambeq LinearReader still produces 120 graph-only diagrams.
- Parser-generated lambeq instances: 0.
- QDisCoCirc package candidates `qdiscocirc` and `qdisco_circ`: unavailable.
- `pip install qdiscocirc` was attempted and returned no matching distribution.

Reason this remains a blocker:
- The available lambeq parser paths do not produce parsed CCG diagrams in this environment.
- The LinearReader diagrams do not carry non-Clifford resource annotations.

## Sutcliffe--Kissinger ZX cutting / partitioning

Status: partially improved, exact blocker remains.

Actions taken:
- `experiments/slms_certificate/zx_partition_baseline.py` added.
- The artifact now reports a pyzx k-partition heuristic after `full_reduce`.
- `results/baseline_results.csv` now contains the row `ZX k-partition heuristic (pyzx)`.

Reason this remains a blocker:
- The heuristic is not the Sutcliffe--Kissinger cutting, k-partitioning, or parametric rewriting algorithm.

## Exact Masot-Llima / Nakhl STN or MAST baselines

Status: not resolved.

Actions taken:
- STN wording was tightened to "STN-style upper-bound proxy."
- No claim is made that this is a faithful implementation of Masot-Llima, Nakhl, or MAST.

Reason this remains a blocker:
- No public implementation is present in the environment, and a faithful reimplementation is beyond this artifact pass.

## End-to-end SLMS wall-clock benchmark on parser-generated QNLP circuits

Status: still blocked, now executable.

Actions taken:
- `experiments/slms_certificate/end_to_end_slms_wallclock.py` added.
- `results/end_to_end_slms_wallclock.json` and `.md` generated.

Reason this remains a blocker:
- The script refuses to benchmark fallback or LinearReader graph-only data as real QNLP evidence.
- Parser-generated resource records found: 0.

## Net effect

The artifact is stronger because two former prose-only blockers are now executable checks, and the ZX comparison has a concrete partition-style heuristic. The package is still not a 90% Quantum-ready empirical package because the real parser-level QNLP and exact external-baseline blockers remain unresolved.
