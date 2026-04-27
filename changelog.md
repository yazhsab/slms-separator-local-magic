# Changelog

## 2026-04-26

- Added `experiments/slms_certificate/check_environment.py`.
- Added `experiments/slms_certificate/real_lambeq_pipeline.py`.
- Expanded `experiments/slms_certificate/example_sentences.txt` to 120 sentences.
- Updated `experiments/slms_certificate/requirements.txt` with core, optional parser, and optional baseline dependencies.
- Updated fallback generation to include balanced, path-active, chain-active, clustered, grid-like, dense-like, mixed, and deliberate failure modes.
- Updated certificate computation with `Lambda_msg`, `Lambda_glob`, `Lambda_kappa`, `2 Lambda_msg`, active-child JSON, gamma JSON, pass/fail reasons, and exponent fields.
- Implemented dense TN, global PWB, naive hybrid, SLMS, and focused-width proxy baseline rows.
- Added tests in `experiments/slms_certificate/tests/test_certificate.py`.
- Updated `run_all.py` to write root-level `results/` and `figures/` artifacts plus manifest and logs.
- Generated 120 fallback instances: 105 certificate passes and 15 certificate failures.
- Generated six PDF figures.
- Revised the manuscript to report fallback structured evidence, lambeq LinearReader sidecar evidence, and exact limitations.
- Created a Python 3.11 lambeq environment in `/tmp/slms_lambeq_py311`; lambeq imports there, but parser-generated extraction still failed.
- Added a lambeq `cups_reader` fallback path that produces 120 LinearReader graph-only diagrams and labels them as non-parser sidecar evidence.
- Added `experiments/slms_certificate/dense_contraction_baseline.py` and generated `results/dense_contraction_baseline.csv`.
- Generated `results/lambeq_reader_dense_contraction_baseline.csv` for the lambeq reader sidecar graphs.
- Added `experiments/slms_certificate/slms_scalar_estimator.py` and generated `results/slms_scalar_estimator_results.csv`.
- Added `experiments/slms_certificate/zx_partition_baseline.py`, a pyzx k-partition heuristic diagnostic that is explicitly not the Sutcliffe--Kissinger algorithm.
- Added `experiments/slms_certificate/qnlp_extraction_probe.py` and `experiments/slms_certificate/end_to_end_slms_wallclock.py` to turn the parser/QDisCoCirc and real-QNLP wall-clock blockers into executable reports.
