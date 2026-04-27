"""Best-effort ZX k-partition heuristic baseline.

This is not a reimplementation of the Sutcliffe--Kissinger cutting or
parametric-rewriting algorithms.  It is a local, reproducible diagnostic that
uses pyzx's graph representation after ``full_reduce`` and then estimates a
partitioned stabilizer-rank exponent:

    min_k max_part(alpha_BG * T_part * ln 2) + cut_edges * ln 2 + ln k.

The cut term is deliberately conservative and easy to audit.  It lets the
artifact report a numerical partition-style comparator without pretending to
match the published ZX simulators.
"""

from __future__ import annotations

from math import log

import networkx as nx

from zx_baseline import ALPHA_BG, PYZX_AVAILABLE, instance_to_synthetic_circuit
import zx_baseline

if PYZX_AVAILABLE:
    import pyzx as zx
else:  # pragma: no cover - exercised only when pyzx is missing.
    zx = None


def _is_t_phase(phase) -> bool:
    try:
        value = float(phase % 1)
    except Exception:
        return False
    return abs(value - 0.25) < 1e-9 or abs(value - 0.75) < 1e-9


def _reduced_nx_graph(instance) -> tuple[nx.Graph, int, str]:
    out = instance_to_synthetic_circuit(instance)
    if out is None:
        return nx.Graph(), 0, "empty_instance"
    circuit, _meta = out
    graph = circuit.to_graph()
    try:
        zx.simplify.full_reduce(graph, quiet=True)
        status = "ok"
    except Exception as exc:
        status = f"full_reduce_failed: {type(exc).__name__}: {exc}"

    nx_graph = nx.Graph()
    t_count = 0
    for vertex in graph.vertices():
        is_t = _is_t_phase(graph.phase(vertex))
        if is_t:
            t_count += 1
        nx_graph.add_node(vertex, is_t=is_t)
    for edge in graph.edges():
        try:
            u, v = graph.edge_st(edge)
        except Exception:
            u, v = edge
        if u != v:
            nx_graph.add_edge(u, v)
    return nx_graph, t_count, status


def _recursive_bisection(graph: nx.Graph, k: int) -> list[set]:
    parts = [set(graph.nodes())]
    while len(parts) < k:
        largest = max(parts, key=len)
        parts.remove(largest)
        if len(largest) <= 1:
            parts.append(largest)
            break
        subgraph = graph.subgraph(largest)
        try:
            left, right = nx.algorithms.community.kernighan_lin_bisection(subgraph)
        except Exception:
            ordered = sorted(largest)
            mid = max(1, len(ordered) // 2)
            left, right = set(ordered[:mid]), set(ordered[mid:])
        if not left or not right:
            ordered = sorted(largest)
            mid = max(1, len(ordered) // 2)
            left, right = set(ordered[:mid]), set(ordered[mid:])
        parts.extend([set(left), set(right)])
    return parts[:k]


def _partition_score(graph: nx.Graph, parts: list[set]) -> dict:
    index = {}
    for part_id, part in enumerate(parts):
        for vertex in part:
            index[vertex] = part_id
    t_by_part = []
    for part in parts:
        t_by_part.append(sum(1 for vertex in part if graph.nodes[vertex].get("is_t", False)))
    cut_edges = sum(1 for u, v in graph.edges() if index.get(u) != index.get(v))
    max_part_exponent = ALPHA_BG * max(t_by_part or [0]) * log(2)
    exponent = max_part_exponent + cut_edges * log(2) + log(max(1, len(parts)))
    return {
        "k": len(parts),
        "cut_edges": cut_edges,
        "max_t_part": max(t_by_part or [0]),
        "partition_exponent": exponent,
    }


def zx_partition_heuristic(instance, max_k: int = 4) -> dict:
    if not PYZX_AVAILABLE:
        return {
            "zx_partition_status": "pyzx_unavailable",
            "zx_partition_error": getattr(zx_baseline, "PYZX_ERROR", "pyzx unavailable"),
            "zx_partition_best_k": None,
            "zx_partition_cut_edges": None,
            "zx_partition_max_t_part": None,
            "zx_partition_exponent_proxy": None,
        }

    graph, t_count, reduce_status = _reduced_nx_graph(instance)
    if graph.number_of_nodes() == 0:
        return {
            "zx_partition_status": "empty_instance",
            "zx_partition_error": "",
            "zx_partition_best_k": 1,
            "zx_partition_cut_edges": 0,
            "zx_partition_max_t_part": 0,
            "zx_partition_exponent_proxy": 0.0,
        }

    candidates = []
    max_candidate_k = max(1, min(max_k, graph.number_of_nodes()))
    for k in range(1, max_candidate_k + 1):
        parts = [set(graph.nodes())] if k == 1 else _recursive_bisection(graph, k)
        candidates.append(_partition_score(graph, parts))
    best = min(candidates, key=lambda item: item["partition_exponent"])
    return {
        "zx_partition_status": f"heuristic_after_full_reduce:{reduce_status}",
        "zx_partition_error": "",
        "zx_partition_t_count_reduced": t_count,
        "zx_partition_best_k": best["k"],
        "zx_partition_cut_edges": best["cut_edges"],
        "zx_partition_max_t_part": best["max_t_part"],
        "zx_partition_exponent_proxy": best["partition_exponent"],
    }
