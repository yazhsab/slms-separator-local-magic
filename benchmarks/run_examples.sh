#!/usr/bin/env bash
# Generates the synthetic accounting CSVs and plots.
#
# Dense width column "w_tn_proxy" is now COMPUTED from the underlying graph
# via networkx.treewidth_min_fill_in (heuristic upper bound).  Earlier
# revisions of this script passed --w-tn-proxy by hand; that is no longer the
# default mode.  The grid case uses --shape grid so its computed treewidth
# reflects the actual L*L grid graph rather than a balanced tree analogue.

set -euo pipefail

cd "$(dirname "$0")"
mkdir -p results

python3 generate_tree_resource_network.py \
  --shape balanced \
  --nodes 63 \
  --placement leaf-local \
  --marginalizable-mode leaves \
  --w-eff-proxy 1 \
  --output results/balanced_leaf_local.csv

python3 generate_tree_resource_network.py \
  --shape balanced \
  --nodes 63 \
  --placement leaf-plus-path \
  --marginalizable-mode off-path \
  --w-eff-proxy 1 \
  --output results/balanced_path_active.csv

python3 generate_tree_resource_network.py \
  --shape chain \
  --nodes 40 \
  --placement uniform \
  --marginalizable-mode none \
  --w-eff-proxy 1 \
  --output results/uniform_chain.csv

python3 generate_tree_resource_network.py \
  --shape balanced \
  --nodes 63 \
  --placement clustered \
  --marginalizable-mode none \
  --w-eff-proxy 2 \
  --output results/clustered_subtree.csv

python3 generate_tree_resource_network.py \
  --shape grid \
  --nodes 81 \
  --placement leaf-local \
  --marginalizable-mode leaves \
  --w-eff-proxy 1 \
  --output results/stabilizer_compressed_grid_accounting.csv

python3 plot_burdens.py \
  --inputs \
    results/balanced_leaf_local.csv \
    results/balanced_path_active.csv \
    results/uniform_chain.csv \
    results/clustered_subtree.csv \
    results/stabilizer_compressed_grid_accounting.csv \
  --output-summary results/summary.csv \
  --plot-prefix results/burdens
