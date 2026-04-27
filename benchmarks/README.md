# Synthetic Burden Accounting Benchmarks

These scripts do not simulate quantum circuits. They implement the combinatorial/resource accounting layer used in the manuscript and are not empirical runtime evidence.

## Run the bundled examples

```sh
bash run_examples.sh
```

This generates CSV instances, `results/summary.csv`, and two SVG plots:

- `results/burdens_global_vs_msg.svg`
- `results/burdens_dense_vs_slms.svg`

The plots are synthetic accounting diagnostics only. They are not runtime measurements.

## Generate a tree/resource instance

```sh
python3 generate_synthetic_networks.py \
  --shape balanced \
  --nodes 31 \
  --placement leaf-local \
  --xi-resource 1.3 \
  --marginalizable-mode leaves \
  --w-tn-proxy 1 \
  --w-eff-proxy 1 \
  --output tree.csv
```

Supported shapes:

- `balanced`
- `chain`
- `star`
- `random`

Supported placement modes:

- `uniform`
- `clustered`
- `leaf-local`
- `root-local`
- `path-local`
- `leaf-plus-path`

The `leaf-plus-path` mode is intended to mirror the path-active separation family in the paper: resources occur at leaves and on the leftmost root-to-leaf path.

For that case, use `--marginalizable-mode off-path` so off-path resources are locally consumed while path resources remain active:

```sh
python3 generate_synthetic_networks.py \
  --shape balanced \
  --nodes 31 \
  --placement leaf-plus-path \
  --marginalizable-mode off-path \
  --output path_active.csv

python3 certify_synthetic_lm.py --input path_active.csv
```

## Compute burdens

```sh
python3 compute_burdens.py \
  --input tree.csv \
  --active-rule none
```

`compute_burdens.py` is a compatibility wrapper for `compute_synthetic_burdens.py`. The script reports:

- global burden `sum_b log xi_b`;
- kappa burden `sum_b log kappa_b`;
- maximum bag burden;
- maximum root-to-leaf path burden;
- maximum subtree burden;
- `Lambda_msg` from the active-child recurrence in the paper.
- dense TN, SLMS, and global-sampling exponent proxies when width proxy columns are present.

`active-rule none` corresponds to complete local marginalization. `active-rule all` reproduces the global/subtree product behavior. `active-rule max-child` gives a path-like recurrence.

## Synthetic local-marginalizability certification

```sh
python3 certify_synthetic_lm.py --input tree.csv --save-csv certificate.csv
```

This script is a combinatorial stand-in for the certification algorithms in the paper. A child subtree is marked inactive when all resource-bearing nodes in that subtree are flagged `marginalizable`; otherwise the child is active. This is conservative and is not a quantum-circuit verifier.
