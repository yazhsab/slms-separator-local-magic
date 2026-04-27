# SLMS Paper and Certificate Artifact

This repository contains the manuscript and executable certificate-evidence artifact for:

Separator-Local Treewidth--Magic Simulation of Compositional Quantum Language Circuits.

The paper is framed as a quantum simulation / quantum tensor-network result: SLMS is a checkable sufficient certificate for additive classical simulation of structured quantum tensor networks with localized non-Clifford resource. Compositional quantum-language circuits are the motivating structured family, not the central empirical claim.

## Build

```sh
latexmk -pdf main.tex
```

The current build succeeds and writes `main.pdf`.

## Artifact Run

The environment has no `python` executable, so the verified commands used `python3`.

Standard commands:

```sh
python experiments/slms_certificate/run_all.py --mode auto
python experiments/slms_certificate/plot_results.py
pytest experiments/slms_certificate/tests
```

Verified commands in the audited local environment:

```sh
python3 experiments/slms_certificate/check_environment.py
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/run_all.py --mode auto
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/plot_results.py
pytest experiments/slms_certificate/tests
```

The blocker probes are expected to exit with status 2 while parser-generated resource instances remain unavailable:

```sh
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/qnlp_extraction_probe.py
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/end_to_end_slms_wallclock.py
```

Parser-level lambeq extraction did not run successfully. The first Python 3.14 attempt failed at import time. A clean Python 3.11 venv was then created at `/tmp/slms_lambeq_py311`; in that environment `lambeq 0.5.0` imported and exposed parser classes, but Bobcat/DepCCG/CCG-style parser extraction did not produce diagrams for the sample corpus. The pipeline then used lambeq's local `cups_reader`, which produced 120 LinearReader graph-only diagrams. These are real lambeq-generated diagrams, but not parser-generated QNLP diagrams and not nontrivial resource instances.

```text
extraction_mode: linear_reader_not_parser
```

Auto mode therefore used fallback lambeq-compatible structured instances as the primary nontrivial certificate evidence, while preserving the lambeq reader outputs as sidecar plumbing evidence.

## Current Results

- Mode used: fallback_with_lambeq_reader_evidence
- Lambeq LinearReader graph-only instances: 120
- Parser-generated lambeq instances: 0
- Fallback instances: 120
- Certificate passes: 105
- Certificate failures: 15
- Median `Lambda_msg`: 0.9244220183777844
- Median SLMS exponent proxy: 3.574185586804947
- Median global PWB proxy: 8.395656462959714
- Dense contraction microbenchmark: 24 small fallback-derived tensor networks and 24 lambeq-reader graph networks contracted with `opt_einsum`
- SLMS scalar-estimator microbenchmark: 32 passing fallback certificates, 20,000 samples each

Primary outputs are in `results/`; generated plots are in `figures/`.

Expected row counts:

- `results/slms_certificate_results.csv`: 120 rows
- `results/slms_certificate_failures.csv`: 15 rows
- `results/baseline_results.csv`: 1680 rows
- `results/dense_contraction_baseline.csv`: 24 rows
- `results/slms_scalar_estimator_results.csv`: 32 rows

## Scope

The artifact implements dense TN, global PWB, naive hybrid, SLMS, the legacy focused-width proxy, exact Codsi--Laakkonen focused tree-width and focused rank-width per arXiv:2603.06377 Definitions 13/14 (exact for small instances; honest upper bound otherwise), a ZX-inspired diagnostic using `pyzx 0.10.0`'s `simplify.full_reduce` plus a Bravyi--Gosset stabilizer-rank exponent, a pyzx k-partition heuristic diagnostic, and a stabilizer-tensor-network upper-bound proxy (tableau plus Bravyi--Gosset). It does not implement the exact Sutcliffe--Kissinger ZX cutting/parametric algorithms, the Masot-Llima--Garcia-Saez STN algorithm, or the Nakhl et al. magic-state-injection STN algorithm. A small dense-contraction microbenchmark and a signed-sampling scalar-estimator microbenchmark are included with wall-clock timings. The end-to-end SLMS wall-clock benchmark gate is implemented, but it reports blocked because parser-generated lambeq/QDisCoCirc resource instances are unavailable.

## Reproducibility

Random seeds are pinned in every randomised script via `--seed` CLI flags with stable defaults:
- `experiments/slms_certificate/fallback_structured_instances.generate_instances`: seed `7` (overridable in `config.yaml`).
- `experiments/slms_certificate/dense_contraction_baseline.py`: `--seed 2026`.
- `experiments/slms_certificate/slms_scalar_estimator.py`: `--seed 12345`.
- `benchmarks/generate_tree_resource_network.py`: `--seed 0`.
- `benchmarks/run_examples.sh`: does not override seeds, so uses each script's pinned default.

To reproduce the reported numbers:

```sh
latexmk -pdf main.tex
cd benchmarks && bash run_examples.sh && cd ..   # synthetic accounting CSVs
MPLCONFIGDIR=/tmp/slms_mplconfig \\
  /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/run_all.py --mode auto
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/slms_scalar_estimator.py
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/dense_contraction_baseline.py
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/plot_results.py
```

The Python 3.11 venv at `/tmp/slms_lambeq_py311` is created with `python3.11 -m venv /tmp/slms_lambeq_py311 && /tmp/slms_lambeq_py311/bin/pip install -r experiments/slms_certificate/requirements.txt pyzx`.

## Known Limitations

- Fallback structured instances are not parser-generated lambeq data.
- lambeq LinearReader sidecar diagrams are graph-only and carry no non-Clifford resource annotations.
- Exact Sutcliffe--Kissinger ZX cutting/k-partitioning is not implemented.
- Exact Masot-Llima / Nakhl STN or MAST is not implemented.
- The public Zenodo DOI is pending: `[Zenodo DOI to be inserted after release]`.
