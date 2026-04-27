# SLMS Repository Audit

Audit date: 2026-04-26

## Repository Structure Found

Main manuscript:
- `main.tex`
- `macros.tex`
- `refs.bib`

Included section files:
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

Existing experiment folders:
- `benchmarks/`
- `benchmarks/results/`
- `experiments/slms_certificate/`
- `experiments/slms_certificate/results/`
- `experiments/slms_certificate/figures/`
- `experiments/slms_certificate/logs/`

Existing experiment scripts:
- `benchmarks/certify_synthetic_lm.py`
- `benchmarks/compute_burdens.py`
- `benchmarks/compute_synthetic_burdens.py`
- `benchmarks/generate_synthetic_networks.py`
- `benchmarks/generate_tree_resource_network.py`
- `benchmarks/plot_burdens.py`
- `benchmarks/run_examples.sh`
- `experiments/slms_certificate/baselines.py`
- `experiments/slms_certificate/certify_slms.py`
- `experiments/slms_certificate/fallback_structured_instances.py`
- `experiments/slms_certificate/graph_extract.py`
- `experiments/slms_certificate/lambeq_pipeline.py`
- `experiments/slms_certificate/load_sentences.py`
- `experiments/slms_certificate/plot_results.py`
- `experiments/slms_certificate/run_all.py`
- `experiments/slms_certificate/tree_decomp.py`

Existing result files:
- `benchmarks/results/*.csv`
- `benchmarks/results/*.svg`
- `experiments/slms_certificate/results/slms_certificate_results.csv`
- `experiments/slms_certificate/results/slms_certificate_summary.json`
- `experiments/slms_certificate/results/slms_certificate_failures.csv`
- `experiments/slms_certificate/results/worked_certificate_recurrence.csv`
- `experiments/slms_certificate/results/run_manifest.json`

Existing figures:
- `experiments/slms_certificate/figures/exp_certificate_pass_rate.pdf`
- `experiments/slms_certificate/figures/exp_exponent_proxy_comparison.pdf`
- `experiments/slms_certificate/figures/exp_lambda_msg_histogram.pdf`
- `experiments/slms_certificate/figures/exp_lambda_msg_vs_lambda_glob.pdf`
- `experiments/slms_certificate/figures/exp_w_eff_histogram.pdf`
- `benchmarks/results/burdens_dense_vs_slms.svg`
- `benchmarks/results/burdens_global_vs_msg.svg`

README and meta files:
- `README.md`
- `experiments/slms_certificate/README.md`
- `benchmarks/README.md`
- `artifact_manifest.md`
- `build_report.md`
- `changelog.md`
- `TODO_remaining.md`
- `REVIEWER_RESPONSE_MEMO.md`
- several prior audit and planning files.

Dependency files:
- `experiments/slms_certificate/requirements.txt`

## LaTeX Build Status

Command run:

```sh
latexmk -pdf main.tex
```

Result: success. `latexmk` reported that `main.pdf` is up to date.

## Bibliography Status

Files found:
- `refs.bib`
- `main.bbl`
- `main.blg`

The current build log search found no unresolved citation warnings.

## Reference Status

The current build log search found no unresolved reference warnings.

## Experiment Package Status Before This Upgrade

An experiment package exists under `experiments/slms_certificate/`, but it is incomplete relative to the requested A-level artifact.

Present:
- fallback-oriented certificate pipeline,
- sentence file,
- requirements file,
- baseline script,
- plot script,
- existing generated CSV/JSON/PDF outputs under `experiments/slms_certificate/`.

Missing or insufficient before this upgrade:
- `experiments/slms_certificate/check_environment.py`
- `experiments/slms_certificate/real_lambeq_pipeline.py`
- `experiments/slms_certificate/tests/test_certificate.py`
- explicit root-level `results/` outputs requested by the mission,
- explicit root-level `figures/` outputs requested by the mission,
- `results/environment_report.json`
- `results/environment_report.txt`
- `results/real_lambeq_instances.json`
- `results/real_lambeq_parse_log.txt`
- `results/real_lambeq_failure_report.md`
- `results/fallback_instances.json`
- `results/baseline_results.csv`
- `results/run_log.txt`
- `results/plot_failure_report.md` when plotting fails,
- `figures/exp_focused_width_proxy_comparison.pdf`.

## Static vs Generated Figures

Existing experiment figures are static files already present in the repository. At audit time, the repository did not yet contain a complete script-and-manifest trail proving that all required figures were regenerated in the requested output locations.

## Described But Not Fully Present Before This Upgrade

The paper describes an executable certificate-evidence artifact, but the repository did not yet contain all scripts, root-level outputs, environment reports, tests, and manifest fields required for a complete reproducibility package. Real lambeq execution had not been established by this audit. The existing package described fallback structured instances, but it did not yet include a complete honest failure report path for unavailable lambeq parsing in the requested filenames.
