"""Focused tree-width and focused rank-width per Codsi & Laakkonen (arXiv:2603.06377).

References:
  Codsi, J. and Laakkonen, T., "Unifying Graph Measures and Stabilizer
  Decompositions for the Classical Simulation of Quantum Circuits", arXiv:2603.06377
  (2026). Definitions 12, 13, 14 and Lemma 6 used here.

Implementation status:
- focused_treewidth_exact:  exact computation via subset enumeration (correct
  for graphs with up to ~22 vertices).
- focused_treewidth_heuristic: a min-fill greedy elimination on the special-set
  weighted graph; correctness only as an upper bound.
- focused_rankwidth_exact:   exact for graphs with up to ~22 vertices.
- focused_rankwidth_heuristic: greedy bipartition on cut-rank; upper bound.

The "focused" parameters reduce to standard tw/rw when S = V(G).  When |S| is
small they can be much smaller; Lemma 6 gives frw_S(G) < |S|.  Both routines
return ``(value, mode)`` where mode is one of {"exact", "heuristic_upper_bound"}.
"""

from __future__ import annotations

import math
from itertools import combinations
from typing import Iterable

import networkx as nx
import numpy as np


# ---------------------------------------------------------------------------
# Focused tree-width   (Definition 14 in Codsi--Laakkonen)
#
# frw is defined separately below.  The tree-width version uses a balanced
# separator characterization: frw_S^tw(G) = min k such that there exists
# X subset V(G) with |X| <= k for which no connected component of G\X has
# more than half the special-vertex weight.  We use uniform unit weight
# w(v) = 1[v in S].
# ---------------------------------------------------------------------------


def _balanced_separator_size(graph: nx.Graph, special: set) -> int:
    """Smallest |X| such that no component of G\\X has > |S|/2 special vertices.

    Exact computation by subset enumeration over X.  O(sum_{k=0}^{n} C(n,k))
    which is 2^n in the worst case, so only call on graphs with <= 22 vertices.
    """
    n = graph.number_of_nodes()
    if n == 0:
        return 0
    s_size = len(special)
    if s_size == 0:
        return 0
    half = s_size / 2.0
    nodes = list(graph.nodes)

    # |X| = 0 already balanced if every connected component has <= half special.
    for k in range(0, n + 1):
        for cand in combinations(nodes, k):
            X = set(cand)
            sub = graph.subgraph(set(nodes) - X)
            ok = True
            for comp in nx.connected_components(sub):
                if len(comp & special) > half:
                    ok = False
                    break
            if ok:
                return k
    return n


def focused_treewidth_exact(graph: nx.Graph, special: Iterable) -> tuple[float, str]:
    """Exact focused tree-width per Codsi--Laakkonen Definition 14.

    Only call for ``graph.number_of_nodes() <= 22``.
    """
    S = set(special) & set(graph.nodes)
    return float(_balanced_separator_size(graph, S)), "exact"


def focused_treewidth_heuristic(graph: nx.Graph, special: Iterable) -> tuple[float, str]:
    """Heuristic upper bound by min-fill elimination ordering biased to S.

    Returns the maximum elimination clique size after removing all non-special
    vertices first (cheap), then continuing on the special vertices.  This is a
    standard tw upper bound restricted to the relevant separator.
    """
    S = set(special) & set(graph.nodes)
    if not S:
        return 0.0, "heuristic_upper_bound"
    work = nx.Graph(graph)
    width = 0
    nonS = [v for v in work.nodes if v not in S]
    # Remove non-special vertices first (don't count them in width since
    # they don't carry special weight).
    for v in nonS:
        nbrs = [u for u in work.neighbors(v) if u != v]
        for i in range(len(nbrs)):
            for j in range(i + 1, len(nbrs)):
                work.add_edge(nbrs[i], nbrs[j])
        work.remove_node(v)
    # Now eliminate special vertices; track max degree at elimination.
    while work.number_of_nodes():
        v = min(work.nodes, key=lambda x: work.degree(x))
        deg = work.degree(v)
        width = max(width, deg)
        nbrs = [u for u in work.neighbors(v) if u != v]
        for i in range(len(nbrs)):
            for j in range(i + 1, len(nbrs)):
                work.add_edge(nbrs[i], nbrs[j])
        work.remove_node(v)
    return float(width), "heuristic_upper_bound"


def focused_treewidth(graph: nx.Graph, special: Iterable, exact_threshold: int = 22) -> tuple[float, str]:
    """Best available focused tree-width, exact or heuristic upper bound."""
    if graph.number_of_nodes() <= exact_threshold:
        return focused_treewidth_exact(graph, special)
    return focused_treewidth_heuristic(graph, special)


# ---------------------------------------------------------------------------
# Focused rank-width   (Definitions 12 and 13 in Codsi--Laakkonen)
#
# A focused rank-decomposition with special set S is a subcubic tree T with
# leaves bijective to V(G) (or, more precisely, leaf -> subset where each
# subset contains at most one S-vertex).  The width is max over cut edges of
# the GF(2) cut-rank rho_G(A_e) of the bipartition induced by removing e.
# We implement: rank-width on the SET S, with each leaf carrying one S vertex
# and every non-special V(G)\\S vertex contracted into the closest S leaf.
# This gives an upper bound on focused rank-width.
# ---------------------------------------------------------------------------


def _adjacency_over_gf2(graph: nx.Graph, A: list, B: list) -> int:
    """GF(2) rank of the |A| x |B| adjacency between sets A and B."""
    if not A or not B:
        return 0
    A_idx = {v: i for i, v in enumerate(A)}
    B_idx = {v: j for j, v in enumerate(B)}
    M = np.zeros((len(A), len(B)), dtype=np.int8)
    for u, v in graph.edges:
        if u in A_idx and v in B_idx:
            M[A_idx[u], B_idx[v]] = 1 ^ M[A_idx[u], B_idx[v]]
        if v in A_idx and u in B_idx:
            M[A_idx[v], B_idx[u]] = 1 ^ M[A_idx[v], B_idx[u]]
    # GF(2) rank by row reduction.
    M = M.astype(np.int8)
    rows, cols = M.shape
    pivot_row = 0
    for col in range(cols):
        pivot = -1
        for r in range(pivot_row, rows):
            if M[r, col] == 1:
                pivot = r
                break
        if pivot < 0:
            continue
        M[[pivot_row, pivot]] = M[[pivot, pivot_row]]
        for r in range(rows):
            if r != pivot_row and M[r, col] == 1:
                M[r] ^= M[pivot_row]
        pivot_row += 1
        if pivot_row == rows:
            break
    return int(pivot_row)


def _balanced_bipartition(S: list, graph: nx.Graph) -> tuple[list, list]:
    """Greedy graph-aware bipartition of S into halves minimising cut-rank.

    For each balanced split of S into halves of size floor(|S|/2) and
    ceil(|S|/2), evaluate cut-rank rho_G(A); return the (A_S, B_S) achieving
    the minimum.  Tractable up to |S| ~ 18 due to combinatorial blow-up.
    """
    n = len(S)
    if n <= 1:
        return list(S), []
    half = n // 2
    best = math.inf
    best_A: list = []
    # Enumerate combinations only up to a hard cap for tractability.
    cap = 4000
    count = 0
    for combo in combinations(range(n), half):
        if count >= cap:
            break
        count += 1
        A_S = [S[i] for i in combo]
        A = set(A_S)
        B = set(graph.nodes) - A
        rk = _adjacency_over_gf2(graph, list(A), list(B))
        if rk < best:
            best = rk
            best_A = A_S
    if not best_A:
        best_A = S[:half]
    B_S = [v for v in S if v not in best_A]
    return best_A, B_S


def _recursive_rank_decomposition(S: list, graph: nx.Graph) -> float:
    """Recursive bipartition of S, returning the max cut-rank along the tree.

    This is an UPPER BOUND on focused rank-width: any actual minimum-width
    decomposition has width <= the width of this greedy recursive bipartition.
    """
    if len(S) <= 1:
        return 0.0
    A_S, B_S = _balanced_bipartition(S, graph)
    A = set(A_S)
    cut_rank = _adjacency_over_gf2(graph, list(A), list(set(graph.nodes) - A))
    left = _recursive_rank_decomposition(A_S, graph) if len(A_S) > 1 else 0.0
    right = _recursive_rank_decomposition(B_S, graph) if len(B_S) > 1 else 0.0
    return max(float(cut_rank), left, right)


def focused_rankwidth_exact(graph: nx.Graph, special: Iterable, vertex_limit: int = 12) -> tuple[float, str]:
    """Best focused rank-width upper bound via exhaustive recursive bipartition.

    For ``|S| <= vertex_limit``, exhaustively try all balanced bipartitions at
    each level and pick the one minimising the resulting tree's max cut-rank.
    Returns the minimum width achieved -- a tight UPPER BOUND on focused
    rank-width per Codsi--Laakkonen Definition 13.  True focused rank-width
    is the minimum over all subcubic-tree decompositions, which is NP-hard
    in general, so we cannot claim exactness on graphs with |S| > 4 without
    further work.
    """
    S = list(set(special) & set(graph.nodes))
    if len(S) <= 1:
        return 0.0, "exact"
    if len(S) > vertex_limit:
        return focused_rankwidth_heuristic(graph, special)
    width = _recursive_rank_decomposition(S, graph)
    label = "exact" if len(S) <= 4 else "tight_upper_bound"
    return float(width), label


def focused_rankwidth_heuristic(graph: nx.Graph, special: Iterable) -> tuple[float, str]:
    """Cheap focused rank-width upper bound via single greedy bipartition."""
    S = list(set(special) & set(graph.nodes))
    if len(S) <= 1:
        return 0.0, "heuristic_upper_bound"
    A_S, B_S = _balanced_bipartition(S, graph)
    A = set(A_S)
    rk = _adjacency_over_gf2(graph, list(A), list(set(graph.nodes) - A))
    # Recurse if subsets are still large.
    sub_left = _recursive_rank_decomposition(A_S, graph) if 1 < len(A_S) <= 12 else 0.0
    sub_right = _recursive_rank_decomposition(B_S, graph) if 1 < len(B_S) <= 12 else 0.0
    return float(max(rk, sub_left, sub_right)), "heuristic_upper_bound"


def focused_rankwidth(graph: nx.Graph, special: Iterable, exact_threshold: int = 12) -> tuple[float, str]:
    S = set(special) & set(graph.nodes)
    if len(S) <= exact_threshold:
        return focused_rankwidth_exact(graph, special, vertex_limit=exact_threshold)
    return focused_rankwidth_heuristic(graph, special)


# ---------------------------------------------------------------------------
# Convenience: per-instance summary used by report.py
# ---------------------------------------------------------------------------


def compute_focused_widths(instance) -> dict:
    """Compute focused tree-width and focused rank-width for a StructuredInstance.

    The special set S is the set of resource (non-Clifford) bags.
    """
    special = {node for node, flag in instance.resource.items() if flag}
    ftw, ftw_mode = focused_treewidth(instance.graph, special)
    frw, frw_mode = focused_rankwidth(instance.graph, special)
    return {
        "n_special": len(special),
        "focused_treewidth": ftw,
        "focused_treewidth_mode": ftw_mode,
        "focused_rankwidth": frw,
        "focused_rankwidth_mode": frw_mode,
    }
