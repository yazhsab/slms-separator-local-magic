# Artifact Publication Checklist

Audit date: 2026-04-26.

Final status: `PARTIALLY MITIGATED`. The local artifact is reproducible, but it is not yet a public DOI-backed artifact.

## Present files

Ready / present:

- `experiments/slms_certificate/`
- `experiments/slms_certificate/requirements.txt`
- `experiments/slms_certificate/check_environment.py`
- `experiments/slms_certificate/run_all.py`
- `experiments/slms_certificate/qnlp_extraction_probe.py`
- `experiments/slms_certificate/end_to_end_slms_wallclock.py`
- `results/environment_report.json`
- `results/environment_report.txt`
- `results/run_manifest.json`
- `results/run_log.txt`
- `results/slms_certificate_results.csv`
- `results/slms_certificate_summary.json`
- `results/slms_certificate_failures.csv`
- `results/baseline_results.csv`
- `results/fallback_instances.json`
- `results/real_lambeq_instances.json`
- `results/qnlp_extraction_probe.json`
- `results/end_to_end_slms_wallclock.json`
- `figures/exp_lambda_msg_histogram.pdf`
- `figures/exp_w_eff_histogram.pdf`
- `figures/exp_lambda_msg_vs_lambda_glob.pdf`
- `figures/exp_exponent_proxy_comparison.pdf`
- `figures/exp_certificate_pass_rate.pdf`
- `figures/exp_focused_width_proxy_comparison.pdf`
- `README.md`
- `artifact_manifest.md`
- `build_report.md`
- `REVIEWER_RESPONSE_MEMO.md`
- `TODO_remaining.md`
- `hard_blocker_ledger.md`
- `lambeq_parser_blocker_report.md`
- `zx_baseline_blocker_report.md`
- `stn_mast_blocker_report.md`

Missing for public release:

- `LICENSE`
- Public URL
- Zenodo DOI
- Release tag

## Sensitive or unwanted release files

Exclude from release archives:

- `.DS_Store`
- `.pytest_cache/`
- `__pycache__/`
- `main.aux`, `main.log`, `main.fls`, `main.fdb_latexmk`, `main.out`, unless intentionally included as build evidence
- stale archives in `submission_package/*.zip` and `submission_package/*.tar.gz`
- `archive/stale_run_py314/` unless deliberately retained as provenance

## Reproducibility commands

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/check_environment.py
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/run_all.py --mode auto
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/qnlp_extraction_probe.py
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/end_to_end_slms_wallclock.py
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/dense_contraction_baseline.py --run-contract --limit 24 --max-vertices 18 --max-edges 24
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/slms_scalar_estimator.py --limit 32 --samples 20000
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/plot_results.py
pytest experiments/slms_certificate/tests
latexmk -pdf main.tex
```

Expected nonzero exit codes:

- `qnlp_extraction_probe.py` exits with status 2 when parser-generated resource instances remain unavailable.
- `end_to_end_slms_wallclock.py` exits with status 2 when no parser-generated resource records exist.

## Expected row counts and hashes

```text
results/slms_certificate_results.csv 120 sha256 159e03c89f623543d22c881b581c0ed61b61f271cad178c3f4521b43b2eb5463
results/slms_certificate_failures.csv 15 sha256 d594c0d993648c97f2c33f21b33af22080642d4c1a1ce1d05de5949250aef6e5
results/baseline_results.csv 1680 sha256 ee2a5c09323b9e97f60e3e4d9ab5c086daf3cb89a4c1deec8f2610a88e169413
results/fallback_instances.json 120 sha256 7ce663cf36cbc42aa7630a44c4f102d0fbcac2eee36f981c385326f63c87020a
results/real_lambeq_instances.json 120 sha256 23dcdc864967c174fb4eb8bf9ec9773717c19ae9ac12cab695b38e6c529606e0
results/lambeq_reader_certificate_results.csv 120 sha256 30aca56bd12838357fc976e78bdabc91526ef544cc99b5661285dd1d9dbf36a7
results/dense_contraction_baseline.csv 24 sha256 a9730eb430b67e9a2befa5312ec0e692d6ff0703e50e7bb58789770f1ae45083
results/slms_scalar_estimator_results.csv 32 sha256 f2a86524e6b02959628de96af5f8cea24a4ba686eaa2ffef661e46beb71d9a1d
main.pdf sha256 4b99995ffc23cc979e8718975b2f9567194ac28d8357024e799b2d77dd96979f
```

Figure hashes:

```text
figures/exp_certificate_pass_rate.pdf da33e19b8e3be71d9375520b6b972586ceeb13948f9c8b25a445b0d29f5f555d
figures/exp_exponent_proxy_comparison.pdf f163a54de221d201b778a55c1b09e1f171820f14be21de67e155b98d246f7991
figures/exp_focused_width_proxy_comparison.pdf fab11ff993ea6b27997eae6bea02b5451f1599ede8b8c08cfb297553570db64e
figures/exp_lambda_msg_histogram.pdf 9d85703b99e4ce9e0ec254cbf31b6b7b3c269396514dad75a62d12b72f439c2d
figures/exp_lambda_msg_vs_lambda_glob.pdf b81f72c4b498f120e7ba682ff55d4f9552b6d18db3f8e43bafec8fafcdf5b588
figures/exp_w_eff_histogram.pdf 3d82e0035afee03a6d3dae00d1015124620fe0a14531654cb7fc785503effa3c
```

## Ready for GitHub?

Partially. Add `LICENSE`, remove generated caches and stale archives, and tag a clean release.

## Ready for Zenodo?

Not yet. A GitHub release or clean ZIP must be prepared first, and Zenodo must mint the DOI. Do not write a DOI into the paper until it exists.
