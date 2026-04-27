# Artifact Manifest

Generated: 2026-04-26

## Reproduction Command

Verified core command:

```sh
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/run_all.py --mode auto
```

The plain `python` executable is unavailable in this environment; `python3` is Python 3.14.0.

## Mode

- Requested mode: `auto`
- Mode actually used: `fallback_with_lambeq_reader_evidence`
- Lambeq LinearReader extraction succeeded: yes
- Parser-generated lambeq extraction succeeded: no
- Real lambeq import status: success under Python 3.11
- Parser failure: Bobcat model retrieval unavailable; WebParser failed; DepCCG dependency stack did not install cleanly
- Lambeq LinearReader graph-only instances: 120
- Parser-generated real instances: 0
- Fallback instances: 120
- Certificate passes/failures: 105/15

## Scripts

- `experiments/slms_certificate/check_environment.py`
- `experiments/slms_certificate/real_lambeq_pipeline.py`
- `experiments/slms_certificate/lambeq_pipeline.py`
- `experiments/slms_certificate/fallback_structured_instances.py`
- `experiments/slms_certificate/certify_slms.py`
- `experiments/slms_certificate/baselines.py`
- `experiments/slms_certificate/run_all.py`
- `experiments/slms_certificate/plot_results.py`
- `experiments/slms_certificate/qnlp_extraction_probe.py`
- `experiments/slms_certificate/end_to_end_slms_wallclock.py`
- `experiments/slms_certificate/zx_partition_baseline.py`
- `experiments/slms_certificate/dense_contraction_baseline.py`
- `experiments/slms_certificate/slms_scalar_estimator.py`
- `experiments/slms_certificate/load_sentences.py`
- `experiments/slms_certificate/graph_extract.py`
- `experiments/slms_certificate/tree_decomp.py`
- `experiments/slms_certificate/tests/test_certificate.py`

## Inputs

- `requirements.txt`
- `experiments/slms_certificate/example_sentences.txt`
- `experiments/slms_certificate/config.yaml`
- `experiments/slms_certificate/requirements.txt`
- `LICENSE`

## Result Files

- `results/environment_report.json`
- `results/environment_report.txt`
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

## Figures

- `figures/exp_lambda_msg_histogram.pdf`
- `figures/exp_w_eff_histogram.pdf`
- `figures/exp_lambda_msg_vs_lambda_glob.pdf`
- `figures/exp_exponent_proxy_comparison.pdf`
- `figures/exp_certificate_pass_rate.pdf`
- `figures/exp_focused_width_proxy_comparison.pdf`

## Baselines

Implemented:
- dense TN proxy
- global PWB proxy
- naive hybrid proxy
- SLMS proxy
- legacy focused-width proxy, explicitly not exact focused tree-width
- Codsi--Laakkonen focused tree-width/focused rank-width diagnostics, exact for small cases and upper bounds otherwise
- pyzx `full_reduce` + Bravyi--Gosset ZX-inspired exponent proxy
- pyzx k-partition heuristic diagnostic, explicitly not Sutcliffe--Kissinger exact cutting/partitioning
- tableau + Bravyi--Gosset STN-style upper-bound proxy
- dense contraction microbenchmark on small fallback-derived tensor networks
- dense contraction sidecar on small lambeq LinearReader graph networks
- scalar-estimator microbenchmark on passing fallback certificates

Not implemented numerically:
- exact Sutcliffe--Kissinger ZX cutting/partitioning
- exact Masot-Llima / Nakhl STN or MAST algorithms
- end-to-end wall-clock simulator benchmark on parser-generated QNLP circuits
- real QNLP circuit benchmark

## Reproducibility Notes

The artifact is deterministic under `seed: 7` in `experiments/slms_certificate/config.yaml`. Fallback instances are structured sanity-check instances and negative controls; they are not empirical parser-level QNLP data. The lambeq reader instances are real lambeq-generated LinearReader diagrams, but they are graph-only and carry no non-Clifford resource annotations in this artifact.

## Release-Facing Index Files

- `parser_failure_logs/README.md`
- `worked_certificate/README.md`
- `hard_blocker_ledger.md`
- `lambeq_parser_blocker_report.md`
- `zx_baseline_blocker_report.md`
- `stn_mast_blocker_report.md`
- `scipost_submission_audit.md`
- `scipost_criteria_alignment.md`
- `claim_audit_final.md` once generated

## Public Archive Status

- GitHub URL: `[GitHub URL to be inserted after release]`
- Zenodo DOI: `[Zenodo DOI to be inserted after release]`
- DOI status: pending; no DOI has been minted in this repository.
