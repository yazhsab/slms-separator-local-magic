#!/usr/bin/env python3
"""Generate synthetic rooted tree/resource instances for burden accounting.

The generator emits a per-node CSV.  When ``--w-tn-proxy`` is omitted (or
negative), the dense-width column ``w_tn_proxy`` is computed from the
underlying graph using ``networkx.algorithms.approximation.treewidth_min_fill_in``
rather than a hand-set value; this is the recommended honest mode.  When
``--w-tn-proxy <value>`` is given explicitly, the supplied value is written
verbatim and the row is marked as a synthetic analogue (column
``w_tn_source``).
"""

import argparse
import csv
import math
import random

try:
    import networkx as nx
    from networkx.algorithms.approximation import treewidth_min_fill_in
    NETWORKX_AVAILABLE = True
except Exception:
    NETWORKX_AVAILABLE = False


def balanced_tree(n):
    parents = {0: None}
    next_id = 1
    queue = [0]
    while next_id < n and queue:
        node = queue.pop(0)
        for _ in range(2):
            if next_id >= n:
                break
            parents[next_id] = node
            queue.append(next_id)
            next_id += 1
    return parents


def chain_tree(n):
    return {i: (None if i == 0 else i - 1) for i in range(n)}


def star_tree(n):
    return {0: None, **{i: 0 for i in range(1, n)}}


def random_tree(n, seed):
    rng = random.Random(seed)
    parents = {0: None}
    for i in range(1, n):
        parents[i] = rng.randrange(0, i)
    return parents


def grid_graph_parents(n):
    """Approximate L*L grid as a rooted spanning tree of an L*L grid graph.

    Returns (parents, side, extra_edges) where extra_edges are the L*L grid
    edges not covered by the BFS spanning tree.  These are returned so the
    caller can compute the dense treewidth on the full grid graph rather than
    the spanning tree.
    """
    side = max(2, int(math.isqrt(n)))
    if side * side != n:
        # Round n up to the next perfect square.
        side = side + 1 if side * side < n else side
    total = side * side
    parents = {0: None}
    for r in range(side):
        for c in range(side):
            idx = r * side + c
            if idx == 0:
                continue
            # Parent is left neighbour for c>0, else top neighbour.
            parents[idx] = idx - 1 if c > 0 else idx - side
    extra_edges = []
    for r in range(side):
        for c in range(side):
            idx = r * side + c
            # Add the missing right and down edges that the spanning tree
            # didn't use, to recover the full grid graph.
            if c < side - 1 and (r > 0):  # right edge that isn't the spanning-tree parent edge
                extra_edges.append((idx, idx + 1))
            if r < side - 1:
                extra_edges.append((idx, idx + side))
    # De-duplicate edges that the spanning tree already provides.
    spanning = {(node, parent) for node, parent in parents.items() if parent is not None}
    spanning |= {(p, n) for n, p in spanning}
    extra_edges = [e for e in extra_edges if (e not in spanning and (e[1], e[0]) not in spanning)]
    return parents, side, extra_edges


def compute_treewidth_from_parents(parents, extra_edges=None) -> tuple[float, str]:
    """Compute treewidth of the graph (parent edges + extra_edges) via networkx.

    Returns (width, mode) where mode is "computed" if networkx was available,
    otherwise "spanning_tree_fallback".
    """
    if not NETWORKX_AVAILABLE:
        return 0.0, "networkx_unavailable"
    g = nx.Graph()
    for node, parent in parents.items():
        g.add_node(node)
        if parent is not None:
            g.add_edge(node, parent)
    for u, v in extra_edges or []:
        g.add_edge(u, v)
    if g.number_of_nodes() == 0:
        return 0.0, "computed"
    width, _decomp = treewidth_min_fill_in(g)
    return float(width), "computed"


def children_from_parents(parents):
    children = {i: [] for i in parents}
    for node, parent in parents.items():
        if parent is not None:
            children[parent].append(node)
    return children


def depths_from_parents(parents):
    depths = {}

    def depth(node):
        if node in depths:
            return depths[node]
        parent = parents[node]
        depths[node] = 0 if parent is None else depth(parent) + 1
        return depths[node]

    for node in parents:
        depth(node)
    return depths


def leftmost_path(children):
    path = []
    node = 0
    while True:
        path.append(node)
        if not children[node]:
            return set(path)
        node = min(children[node])


def clustered_nodes(children):
    if not children[0]:
        return {0}
    root_child = min(children[0])
    out = set()
    stack = [root_child]
    while stack:
        node = stack.pop()
        out.add(node)
        stack.extend(children[node])
    return out


def resource_nodes(parents, placement, seed, fraction):
    children = children_from_parents(parents)
    nodes = set(parents)
    leaves = {node for node in nodes if not children[node]}
    if placement == "uniform":
        return nodes
    if placement == "leaf-local":
        return leaves
    if placement == "root-local":
        return {0}
    if placement == "path-local":
        return leftmost_path(children)
    if placement == "leaf-plus-path":
        return leaves | leftmost_path(children)
    if placement == "clustered":
        return clustered_nodes(children)
    if placement == "random":
        rng = random.Random(seed)
        return {node for node in nodes if rng.random() < fraction}
    raise ValueError(f"unknown placement: {placement}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=["balanced", "chain", "star", "random", "grid"], default="balanced")
    parser.add_argument("--nodes", type=int, default=31)
    parser.add_argument("--placement", choices=["uniform", "clustered", "leaf-local", "root-local", "path-local", "leaf-plus-path", "random"], default="leaf-local")
    parser.add_argument("--xi-resource", type=float, default=1.3)
    parser.add_argument("--xi-free", type=float, default=1.0)
    parser.add_argument("--kappa-resource", type=float, default=1.0)
    parser.add_argument("--kappa-free", type=float, default=1.0)
    parser.add_argument("--random-fraction", type=float, default=0.25)
    parser.add_argument("--marginalizable-mode", choices=["all", "none", "leaves", "resources", "off-path"], default="leaves")
    parser.add_argument("--boundary-dim", type=int, default=2)
    parser.add_argument("--w-tn-proxy", type=float, default=-1.0)
    parser.add_argument("--w-eff-proxy", type=float, default=-1.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", default="tree_resource_network.csv")
    args = parser.parse_args()

    if args.nodes < 1:
        raise SystemExit("--nodes must be positive")
    if args.xi_resource < 1.0 or args.xi_free < 1.0:
        raise SystemExit("xi values must be at least 1")
    if args.kappa_resource < 1.0 or args.kappa_free < 1.0:
        raise SystemExit("kappa values must be at least 1")

    extra_edges: list[tuple[int, int]] = []
    if args.shape == "balanced":
        parents = balanced_tree(args.nodes)
    elif args.shape == "chain":
        parents = chain_tree(args.nodes)
    elif args.shape == "star":
        parents = star_tree(args.nodes)
    elif args.shape == "grid":
        parents, _side, extra_edges = grid_graph_parents(args.nodes)
    else:
        parents = random_tree(args.nodes, args.seed)

    depths = depths_from_parents(parents)
    children = children_from_parents(parents)
    leaves = {node for node in parents if not children[node]}
    path = leftmost_path(children)
    resources = resource_nodes(parents, args.placement, args.seed, args.random_fraction)

    def is_marginalizable(node):
        if args.marginalizable_mode == "all":
            return True
        if args.marginalizable_mode == "none":
            return False
        if args.marginalizable_mode == "leaves":
            return node in leaves
        if args.marginalizable_mode == "resources":
            return node in resources
        if args.marginalizable_mode == "off-path":
            return node not in path
        raise ValueError(args.marginalizable_mode)

    default_w_eff = math.log(max(1, args.boundary_dim), 2)
    w_eff_proxy = args.w_eff_proxy if args.w_eff_proxy >= 0 else float(default_w_eff)
    if args.w_tn_proxy >= 0:
        w_tn_proxy = float(args.w_tn_proxy)
        w_tn_source = "synthetic_user_supplied"
    else:
        w_tn_proxy, w_tn_source = compute_treewidth_from_parents(parents, extra_edges)

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "node",
                "parent",
                "depth",
                "xi",
                "kappa",
                "resource",
                "marginalizable",
                "boundary_dim",
                "w_tn_proxy",
                "w_tn_source",
                "w_eff_proxy",
            ],
        )
        writer.writeheader()
        for node in sorted(parents):
            is_resource = node in resources
            writer.writerow({
                "node": node,
                "parent": "" if parents[node] is None else parents[node],
                "depth": depths[node],
                "xi": args.xi_resource if is_resource else args.xi_free,
                "kappa": args.kappa_resource if is_resource else args.kappa_free,
                "resource": int(is_resource),
                "marginalizable": int(is_marginalizable(node)),
                "boundary_dim": args.boundary_dim,
                "w_tn_proxy": w_tn_proxy,
                "w_tn_source": w_tn_source,
                "w_eff_proxy": w_eff_proxy,
            })

    print(f"wrote {args.output} with {len(parents)} nodes and {len(resources)} resource nodes")


if __name__ == "__main__":
    main()
