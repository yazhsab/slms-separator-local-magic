from __future__ import annotations

import time

import networkx as nx

from fallback_structured_instances import StructuredInstance
from focused_width import compute_focused_widths
from stn_baseline import stn_exponent
from zx_baseline import PYZX_AVAILABLE, zx_exponent
from zx_partition_baseline import zx_partition_heuristic


def dense_width_proxy(graph: nx.Graph) -> float:
    if graph.number_of_nodes() <= 1:
        return 0.0
    try:
        from networkx.algorithms.approximation import treewidth_min_fill_in

        width, _decomp = treewidth_min_fill_in(graph)
        return float(width)
    except Exception:
        return float(max(1, min(dict(graph.degree()).values() or [1])))


def _subtree_nodes(instance: StructuredInstance, root: str) -> set[str]:
    out = set()
    stack = [root]
    while stack:
        node = stack.pop()
        out.add(node)
        stack.extend(instance.children.get(node, []))
    return out


def compute_focused_width_proxy(instance: StructuredInstance) -> tuple[float, str]:
    """Best-effort focused-width proxy, not exact focused tree-width.

    Formula used here:
    max over parent-child separators of the number of resource vertices in the
    child subtree whose randomness is certified active across that separator,
    then max with the dense graph-width proxy. This is a diagnostic resource
    separator score; it is not the Codsi--Laakkonen focused tree-width.
    """

    graph = instance.graph
    resource_vertices = {node for node, flag in instance.resource.items() if flag}
    if not resource_vertices:
        return 0.0, "no_resource_vertices"
    max_active_resource_crossing = 0
    for parent, children in instance.children.items():
        for child in children:
            if not instance.active_edge.get((parent, child), False):
                continue
            subtree = _subtree_nodes(instance, child)
            max_active_resource_crossing = max(max_active_resource_crossing, len(subtree & resource_vertices))
    return float(max(dense_width_proxy(graph), max_active_resource_crossing)), "implemented_proxy_not_exact_focused_treewidth"


def exponent_proxies(row: dict, w_tn_proxy: float) -> dict:
    lambda_glob = float(row["lambda_glob"])
    lambda_msg = float(row["lambda_msg"])
    w_eff = float(row["w_eff_proxy"])
    return {
        "w_TN_proxy": w_tn_proxy,
        "dense_tn_proxy": w_tn_proxy,
        "global_pwb_proxy": 2.0 * lambda_glob,
        "naive_hybrid_proxy": w_eff + 2.0 * lambda_glob,
        "slms_proxy": w_eff + 2.0 * lambda_msg,
        "exponent_dense": w_tn_proxy,
        "exponent_global_pwb": 2.0 * lambda_glob,
        "exponent_naive_hybrid": w_eff + 2.0 * lambda_glob,
        "exponent_slms": w_eff + 2.0 * lambda_msg,
    }


def codsi_laakkonen_exponent(row: dict) -> float:
    """Codsi-Laakkonen exponent: T^{gamma * frw}, natural log.

    From Theorem 8 of arXiv:2603.06377: runtime ~ |S|^{gamma * frw_S(C)} where
    gamma = log_{3/2}(4) ~= 3.42 and S is the special (non-Clifford) set.
    Reported as natural log to be comparable with other exponent proxies.
    """
    from math import log, log2

    gamma = log(4) / log(1.5)  # ~3.42
    n_resource = float(row.get("n_resources") or row.get("resource_count") or 0)
    frw = float(row.get("focused_rankwidth", 0.0))
    if n_resource <= 1 or frw <= 0:
        return 0.0
    return gamma * frw * log(max(2, n_resource))


def compute_extended_baselines(instance, row: dict) -> dict:
    """Run focused tree-width, focused rank-width, ZX, STN baselines on an instance.

    Returns wall-clock timings as well as the exponent proxies.
    """
    out: dict = {}

    t0 = time.perf_counter()
    fw = compute_focused_widths(instance)
    out["focused_treewidth"] = fw["focused_treewidth"]
    out["focused_treewidth_mode"] = fw["focused_treewidth_mode"]
    out["focused_rankwidth"] = fw["focused_rankwidth"]
    out["focused_rankwidth_mode"] = fw["focused_rankwidth_mode"]
    out["focused_widths_seconds"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    zr = zx_exponent(instance)
    out.update(zr)
    out["zx_seconds"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    zpart = zx_partition_heuristic(instance)
    out.update(zpart)
    out["zx_partition_seconds"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    sr = stn_exponent(instance)
    out.update(sr)
    out["stn_seconds"] = time.perf_counter() - t0

    out["codsi_laakkonen_exponent"] = codsi_laakkonen_exponent({**row, **out})
    return out


def baseline_rows(row: dict) -> list[dict]:
    common = {
        "instance_id": row["instance_id"],
        "mode": row["mode"],
        "certificate_pass": row["certificate_pass"],
    }
    return [
        {
            **common,
            "method": "dense TN proxy",
            "implemented_here": True,
            "parameter": "w_TN_proxy",
            "exponent_proxy": row["exponent_dense"],
            "limitation": "graph treewidth proxy only; no tensor-value contraction timing",
        },
        {
            **common,
            "method": "global PWB proxy",
            "implemented_here": True,
            "parameter": "2 Lambda_glob",
            "exponent_proxy": row["exponent_global_pwb"],
            "limitation": "quasiprobability burden proxy; not a simulator timing",
        },
        {
            **common,
            "method": "naive hybrid proxy",
            "implemented_here": True,
            "parameter": "w_eff_proxy + 2 Lambda_glob",
            "exponent_proxy": row["exponent_naive_hybrid"],
            "limitation": "uses global resource burden without local marginalization",
        },
        {
            **common,
            "method": "SLMS proxy",
            "implemented_here": True,
            "parameter": "w_eff_proxy + 2 Lambda_msg",
            "exponent_proxy": row["exponent_slms"],
            "limitation": "certificate exponent proxy; no wall-clock simulator benchmark",
        },
        {
            **common,
            "method": "focused-width proxy (legacy)",
            "implemented_here": True,
            "parameter": "max(dense width proxy, active resource subtree score)",
            "exponent_proxy": row["focused_width_proxy"],
            "limitation": row["focused_width_status"],
        },
        {
            **common,
            "method": "Codsi-Laakkonen focused tree-width",
            "implemented_here": True,
            "parameter": "frw_S balanced-separator size, Definition 14",
            "exponent_proxy": row.get("focused_treewidth", ""),
            "limitation": row.get("focused_treewidth_mode", "") + "; per arXiv:2603.06377",
        },
        {
            **common,
            "method": "Codsi-Laakkonen focused rank-width",
            "implemented_here": True,
            "parameter": "frw_S recursive-bipartition GF(2) cut-rank, Definition 13",
            "exponent_proxy": row.get("focused_rankwidth", ""),
            "limitation": row.get("focused_rankwidth_mode", "") + "; per arXiv:2603.06377",
        },
        {
            **common,
            "method": "Codsi-Laakkonen runtime exponent",
            "implemented_here": True,
            "parameter": "(log_{3/2} 4) * frw_S * log|S|, ln-scale",
            "exponent_proxy": row.get("codsi_laakkonen_exponent", ""),
            "limitation": "Theorem 8 of arXiv:2603.06377; uses our frw upper bound",
        },
        {
            **common,
            "method": "ZX (pyzx full_reduce + Bravyi-Gosset)",
            "implemented_here": bool(PYZX_AVAILABLE),
            "parameter": "alpha_BG * T_count_after_reduction, ln-scale",
            "exponent_proxy": row.get("zx_exponent_proxy", ""),
            "limitation": "synthetic Clifford+T circuit derived from instance; pyzx full_reduce; not Sutcliffe-Kissinger cutting/parametric rewrites",
        },
        {
            **common,
            "method": "STN-style upper bound",
            "implemented_here": True,
            "parameter": "alpha_BG * T_count + ln(active_resource_count), ln-scale",
            "exponent_proxy": row.get("stn_exponent_proxy", ""),
            "limitation": "tableau+Bravyi-Gosset upper bound; NOT the Masot-Llima or Nakhl algorithm",
        },
        {
            **common,
            "method": "opt_einsum/cotengra dense contraction",
            "implemented_here": False,
            "parameter": "not available for graph-only instances",
            "exponent_proxy": "",
            "limitation": "tensor entries are not generated; width proxy reported instead",
        },
        {
            **common,
            "method": "ZX k-partition heuristic (pyzx)",
            "implemented_here": bool(PYZX_AVAILABLE),
            "parameter": "min_k max_part(alpha_BG*T_part*ln2)+cut_edges*ln2+ln(k)",
            "exponent_proxy": row.get("zx_partition_exponent_proxy", ""),
            "limitation": "best-effort pyzx graph partition diagnostic; NOT Sutcliffe-Kissinger cutting/parametric rewrites",
        },
        {
            **common,
            "method": "ZX partitioning (Sutcliffe-Kissinger exact)",
            "implemented_here": False,
            "parameter": "not computed",
            "exponent_proxy": "",
            "limitation": "published Sutcliffe-Kissinger 2024-2025 algorithms not reimplemented; heuristic pyzx partition row is separate",
        },
        {
            **common,
            "method": "STN / MAST exact",
            "implemented_here": False,
            "parameter": "not computed",
            "exponent_proxy": "",
            "limitation": "Masot-Llima and Nakhl tensor-network algorithms not implemented; only an upper-bound proxy reported",
        },
    ]
