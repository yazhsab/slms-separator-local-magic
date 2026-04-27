# Submission Package Checklist

Date: 2026-04-26

## Include in the Submission

Manuscript:
- `main.pdf`
- `main.tex`
- `macros.tex`
- `refs.bib`
- `sections/*.tex`
- `appendices/*.tex`

Artifact code:
- `experiments/slms_certificate/README.md`
- `experiments/slms_certificate/requirements.txt`
- `experiments/slms_certificate/config.yaml`
- `experiments/slms_certificate/example_sentences.txt`
- `experiments/slms_certificate/check_environment.py`
- `experiments/slms_certificate/real_lambeq_pipeline.py`
- `experiments/slms_certificate/lambeq_pipeline.py`
- `experiments/slms_certificate/fallback_structured_instances.py`
- `experiments/slms_certificate/certify_slms.py`
- `experiments/slms_certificate/baselines.py`
- `experiments/slms_certificate/focused_width.py`
- `experiments/slms_certificate/zx_baseline.py`
- `experiments/slms_certificate/zx_partition_baseline.py`
- `experiments/slms_certificate/stn_baseline.py`
- `experiments/slms_certificate/qnlp_extraction_probe.py`
- `experiments/slms_certificate/end_to_end_slms_wallclock.py`
- `experiments/slms_certificate/dense_contraction_baseline.py`
- `experiments/slms_certificate/slms_scalar_estimator.py`
- `experiments/slms_certificate/run_all.py`
- `experiments/slms_certificate/plot_results.py`
- `experiments/slms_certificate/load_sentences.py`
- `experiments/slms_certificate/graph_extract.py`
- `experiments/slms_certificate/tree_decomp.py`
- `experiments/slms_certificate/tests/test_certificate.py`

Generated evidence:
- `results/environment_report.json`
- `results/environment_report.txt`
- `results/real_lambeq_failure_report.md`
- `results/real_lambeq_parse_log.txt`
- `results/real_lambeq_instances.json`
- `results/qnlp_extraction_probe.json`
- `results/qnlp_extraction_probe.md`
- `results/end_to_end_slms_wallclock.json`
- `results/end_to_end_slms_wallclock.md`
- `results/lambeq_reader_certificate_results.csv`
- `results/lambeq_reader_certificate_failures.csv`
- `results/lambeq_reader_baseline_results.csv`
- `results/lambeq_reader_dense_contraction_baseline.csv`
- `results/lambeq_reader_worked_certificate_recurrence.csv`
- `results/fallback_instances.json`
- `results/slms_certificate_results.csv`
- `results/slms_certificate_summary.json`
- `results/slms_certificate_failures.csv`
- `results/baseline_results.csv`
- `results/dense_contraction_baseline.csv`
- `results/slms_scalar_estimator_results.csv`
- `results/worked_certificate_recurrence.csv`
- `results/run_manifest.json`
- `results/run_log.txt`
- `figures/*.pdf`

Reproducibility and review files:
- `README.md`
- `artifact_manifest.md`
- `build_report.md`
- `audit_report.md`
- `changelog.md`
- `TODO_remaining.md`
- `REVIEWER_RESPONSE_MEMO.md`
- `acceptance_readiness_score.md`
- `SUBMISSION_PACKAGE.md`
- `remaining_blockers_status.md`

Optional legacy synthetic benchmark layer:
- `benchmarks/`

## Exclude from the Submission Archive

- `.DS_Store`
- `.pytest_cache/`
- `__pycache__/`
- `*.pyc`
- transient TeX files if the venue wants source-only: `main.aux`, `main.blg`, `main.fdb_latexmk`, `main.fls`, `main.log`, `main.out`

Keep `main.bbl` if the venue requests a self-contained LaTeX source bundle.

## Current Evidence Status

- Mode used: `fallback_with_lambeq_reader_evidence`
- Lambeq LinearReader graph-only instances: 120
- Parser-generated lambeq instances: 0
- Fallback structured instances: 120
- Primary certificate passes/failures: 105/15
- Figures generated: 6
- Paper build: success, 46-page `main.pdf`

This package is honest and reproducible, but it is not a 100% strong Quantum-level package because parser-generated QNLP resource instances, Sutcliffe--Kissinger ZX cutting/partitioning, exact Masot-Llima/Nakhl STN or MAST baselines, a strict separation theorem, and real-QNLP wall-clock simulator benchmarks remain open. Focused tree-width/rank-width diagnostics are included, exact for small cases and upper bounds otherwise.
