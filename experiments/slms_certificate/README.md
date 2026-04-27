# SLMS Certificate-Evidence Pipeline

This package computes SLMS certificate quantities and baseline exponent proxies for structured language-like tensor-network instances.

It has two modes:

- `real`: attempts to use `lambeq` to parse sentences. If parser execution fails but lambeq readers are available, it records LinearReader graph-only evidence with `extraction_mode=linear_reader_not_parser`.
- `fallback`: generates lambeq-compatible grammar-tree instances. These are structured sanity-check instances, not real lambeq outputs.
- `auto`: tries `real` first. If only LinearReader graph-only evidence is available, it stores that as a sidecar and uses fallback instances as the primary nontrivial certificate evidence.

Run:

```sh
python3 experiments/slms_certificate/run_all.py --mode auto
```

In this environment the verified command used the temporary dependency target:

```sh
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/run_all.py --mode auto
```

Outputs are written under the repository root:

- `results/slms_certificate_results.csv`
- `results/slms_certificate_summary.json`
- `results/slms_certificate_failures.csv`
- `results/baseline_results.csv`
- `results/real_lambeq_instances.json`
- `results/lambeq_reader_certificate_results.csv`
- `results/lambeq_reader_baseline_results.csv`
- `results/lambeq_reader_dense_contraction_baseline.csv`
- `results/qnlp_extraction_probe.json`
- `results/end_to_end_slms_wallclock.json`
- `results/run_manifest.json`
- `figures/*.pdf`
- `results/dense_contraction_baseline.csv`
- `results/slms_scalar_estimator_results.csv`

Additional microbenchmarks:

```sh
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/dense_contraction_baseline.py --run-contract
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/slms_scalar_estimator.py
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/qnlp_extraction_probe.py
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/end_to_end_slms_wallclock.py
```

The QNLP extraction and end-to-end wall-clock scripts intentionally exit nonzero when parser-generated resource instances are unavailable; their JSON/Markdown reports are the artifact output. The results are certificate-evidence diagnostics only. The dense contraction and scalar-estimator scripts are executed microbenchmarks on graph-derived data, not real parser-level QNLP simulator benchmarks. The lambeq reader sidecar verifies local lambeq diagram generation and graph extraction, but it does not establish nontrivial QNLP resource coverage. The artifact does not establish quantum advantage or dominance over focused-width, ZX, or stabilizer tensor-network simulators.
