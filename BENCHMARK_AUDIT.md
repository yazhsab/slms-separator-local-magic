# Benchmark Audit

## Scripts Found

- `benchmarks/generate_tree_resource_network.py`
- `benchmarks/generate_synthetic_networks.py` compatibility wrapper
- `benchmarks/compute_synthetic_burdens.py`
- `benchmarks/compute_burdens.py` compatibility wrapper
- `benchmarks/certify_synthetic_lm.py`
- `benchmarks/plot_burdens.py`
- `benchmarks/run_examples.sh`
- `benchmarks/README.md`

## Scripts Created In This Pass

- `generate_synthetic_networks.py`
- `compute_burdens.py`

These wrappers preserve the existing implementation while matching the expected submission-package names.

## Outputs Generated

Running:

```sh
cd benchmarks
bash run_examples.sh
```

was rerun successfully during the referee-hardening pass and generated:

- `results/balanced_leaf_local.csv`
- `results/balanced_path_active.csv`
- `results/uniform_chain.csv`
- `results/clustered_subtree.csv`
- `results/stabilizer_compressed_grid_accounting.csv`
- `results/summary.csv`
- `results/burdens_global_vs_msg.svg`
- `results/burdens_dense_vs_slms.svg`

The compatibility wrappers were also smoke-tested on a three-node chain.

## Manuscript Table Check

The table in Section 8 matches `benchmarks/results/summary.csv` to three decimal places:

- balanced leaf-local: global 8.396, `Lambda_msg` 0.262, SLMS exponent `w_eff + 2 Lambda_msg` = 1.525;
- balanced path-active: global 9.707, `Lambda_msg` 1.574, SLMS exponent `w_eff + 2 Lambda_msg` = 4.148;
- uniform chain: global 10.495, `Lambda_msg` 10.495, SLMS exponent `w_eff + 2 Lambda_msg` = 21.989;
- clustered subtree: global 8.133, `Lambda_msg` 8.133, SLMS exponent `w_eff + 2 Lambda_msg` = 18.267;
- stabilizer-compressed grid accounting: global 10.757, `Lambda_msg` 0.262, SLMS exponent `w_eff + 2 Lambda_msg` = 1.525.

## Limitations

The benchmark layer is synthetic accounting only:

- it does not simulate quantum circuits;
- width values are proxies, not computed treewidth/branchwidth;
- runtime values are exponent proxies, not measured simulator runtimes;
- no lambeq or QDisCoCirc extraction backend is implemented.
