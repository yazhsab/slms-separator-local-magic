# SciPost Submission Audit

Audit date: 2026-04-26.

Target framing: SciPost Physics Core, Quantum Physics / Mathematical Physics / Computational Physics. The paper should read as a quantum simulation and quantum tensor-network paper motivated by compositional quantum-language circuits.

## Files Present

Main manuscript:

- `main.tex`
- `macros.tex`
- `refs.bib`
- `main.pdf`

Sections:

- `sections/00_popular_summary.tex`
- `sections/01_introduction.tex`
- `sections/02_related_work.tex`
- `sections/03_model.tex`
- `sections/04_separator_local_magic.tex`
- `sections/05_algorithm.tex`
- `sections/06_main_theorem.tex`
- `sections/07_qnlp_specialization.tex`
- `sections/08_benchmarks.tex`
- `sections/09_limitations.tex`
- `sections/10_conclusion.tex`

Appendices:

- `appendices/A_tree_decompositions.tex`
- `appendices/B_stabilizer_decompositions.tex`
- `appendices/C_variance_bounds.tex`
- `appendices/D_qnlp_graph_extraction.tex`
- `appendices/E_additional_examples.tex`
- `appendices/F_certification_algorithms.tex`
- `appendices/G_worked_certificate.tex`

Experiment and artifact scripts:

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
- `experiments/slms_certificate/dense_contraction_baseline.py`
- `experiments/slms_certificate/slms_scalar_estimator.py`
- `experiments/slms_certificate/qnlp_extraction_probe.py`
- `experiments/slms_certificate/end_to_end_slms_wallclock.py`
- `experiments/slms_certificate/run_all.py`
- `experiments/slms_certificate/plot_results.py`
- `experiments/slms_certificate/tests/test_certificate.py`

Result files:

- `results/slms_certificate_results.csv`
- `results/slms_certificate_summary.json`
- `results/slms_certificate_failures.csv`
- `results/baseline_results.csv`
- `results/fallback_instances.json`
- `results/run_manifest.json`
- `results/run_log.txt`
- `results/environment_report.json`
- `results/environment_report.txt`
- `results/real_lambeq_parse_log.txt`
- `results/real_lambeq_instances.json`
- `results/real_lambeq_failure_report.md`
- `results/qnlp_extraction_probe.json`
- `results/end_to_end_slms_wallclock.json`
- `results/dense_contraction_baseline.csv`
- `results/slms_scalar_estimator_results.csv`
- `results/worked_certificate_recurrence.csv`

Figures:

- `figures/exp_lambda_msg_histogram.pdf`
- `figures/exp_w_eff_histogram.pdf`
- `figures/exp_lambda_msg_vs_lambda_glob.pdf`
- `figures/exp_exponent_proxy_comparison.pdf`
- `figures/exp_certificate_pass_rate.pdf`
- `figures/exp_focused_width_proxy_comparison.pdf`

Audit and release files:

- `README.md`
- `artifact_manifest.md`
- `build_report.md`
- `TODO_remaining.md`
- `hard_blocker_ledger.md`
- `artifact_publication_checklist.md`
- `lambeq_parser_blocker_report.md`
- `zx_baseline_blocker_report.md`
- `stn_mast_blocker_report.md`
- `zenodo_release_instructions.md`
- `final_submission_readiness.md`

## Files Missing or Not Yet Public

- `LICENSE` was missing at audit start.
- Root-level `requirements.txt` was missing at audit start.
- `parser_failure_logs/` directory was missing at audit start.
- `worked_certificate/` directory was missing at audit start.
- Public GitHub URL is not assigned.
- Zenodo DOI is not minted.

Post-audit remediation: `LICENSE`, root `requirements.txt`, `parser_failure_logs/README.md`, and `worked_certificate/README.md` have been added. The public GitHub URL and Zenodo DOI remain pending external release actions.

## Build Status

Command run:

```bash
latexmk -pdf main.tex
```

Status: success. `main.pdf` is up to date. The previous log scan found no unresolved citation, unresolved reference, or overfull-box matches in `main.log` / `main.blg`. The build uses `quantumarticle` and `bibtex` with `refs.bib`.

## Bibliography Status

`refs.bib` is present and `main.bbl` is generated. The bibliography covers tensor-network simulation, quasiprobability simulation, stabilizer-rank/magic, junction-tree inference, focused width, ZX approaches, STN/MAST, lambeq, and QDisCoCirc. No missing citation was reported in the current build.

## Figure and Result Path Status

All figure paths included in `sections/08_benchmarks.tex` exist under `figures/`.

All listed result paths in the benchmark/artifact section exist, except directory-level packaging paths requested for public release (`parser_failure_logs/`, `worked_certificate/`) which were not present at audit start and should be created as release-facing index directories.

## Artifact Result Status

Current artifact results:

- Primary fallback structured instances: 120.
- Certificate passes/failures: 105 / 15.
- Median `Lambda_msg`: 0.9244220183777844.
- Median `w_eff_proxy`: 1.0.
- Median SLMS exponent proxy: 3.574185586804947.
- Median global PWB proxy: 8.395656462959717.
- Parser-generated lambeq/QDisCoCirc resource instances: 0.
- lambeq LinearReader graph-only sidecar instances: 120.

These numbers are supported by `results/slms_certificate_summary.json`, `results/slms_certificate_results.csv`, and `results/run_manifest.json`.

## Claim Support Map

Supported by theorem:

- SLMS is a checkable sufficient certificate for additive classical simulation of locally marginalizable resource-decomposition tensor networks.
- Runtime contains `2^{O(w_eff)}` and the explicit sampling factor `exp(2 Lambda_msg)`.
- Certificate failure does not imply hardness.

Supported by artifact:

- Fallback structured corpus contains 120 instances, with 105 certificate passes and 15 failures.
- Baseline/comparator rows are generated in `results/baseline_results.csv`.
- pyzx and STN rows are proxy/heuristic diagnostics, not exact Sutcliffe-Kissinger or exact STN/MAST implementations.
- Parser-generated lambeq/QDisCoCirc resource evidence is unavailable in the executed environment.
- End-to-end real-QNLP SLMS wall-clock benchmarking is blocked because parser-generated resource instances are absent.

Supported by citations / related-work context:

- Markov--Shi treewidth simulation.
- Pashayan--Wallman--Bartlett and Pashayan--Bartlett--Gross quasiprobability simulation.
- Bravyi--Gosset / BBCCGH stabilizer-rank simulation.
- Lauritzen--Spiegelhalter / Shafer--Shenoy / Dechter message passing.
- Codsi--Laakkonen focused width.
- Kuyanov--Kissinger low-rank-width ZX.
- Sutcliffe / Sutcliffe--Kissinger ZX partitioning/cutting.
- Masot-Llima--Garcia-Saez and Nakhl et al. STN/MAST.
- lambeq and QDisCoCirc as motivating sources of structured quantum language circuits.

Unsupported and correctly not claimed:

- Generic parser-level lambeq/QDisCoCirc coverage.
- Quantum advantage.
- Dominance over focused-width, ZX, stabilizer-rank, or STN methods.
- Exact Sutcliffe-Kissinger or exact STN/MAST numerical baselines.
- Real parser-generated QNLP wall-clock benchmark.

## SciPost Risk Assessment

The main SciPost risk is not prose quality but scope clarity. The paper must foreground quantum simulation, tensor networks, stabilizer compression, magic, and quasiprobability sampling. QNLP should remain a motivating structured circuit source, not the empirical center of gravity. The hard blocker ledger already protects the manuscript from overclaiming.
