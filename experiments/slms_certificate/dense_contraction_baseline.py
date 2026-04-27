from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import networkx as nx
import numpy as np


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent.parent
RESULTS_DIR = REPO_ROOT / "results"


def _read_instances(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def _graph_from_record(record: dict) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(record["graph"]["nodes"])
    graph.add_edges_from(tuple(edge) for edge in record["graph"]["edges"])
    return graph


def _make_tensor_network(graph: nx.Graph, seed: int, bond_dim: int) -> tuple[list[np.ndarray], list[list[str]]]:
    rng = np.random.default_rng(seed)
    edge_labels = {tuple(sorted(edge)): f"e{i}" for i, edge in enumerate(sorted(tuple(sorted(e)) for e in graph.edges()))}
    tensors = []
    labels = []
    for node in sorted(graph.nodes()):
        incident = []
        for nbr in sorted(graph.neighbors(node)):
            incident.append(edge_labels[tuple(sorted((node, nbr)))])
        shape = (bond_dim,) * len(incident)
        if not shape:
            tensor = np.asarray(rng.normal(), dtype=np.float64)
        else:
            tensor = rng.normal(size=shape).astype(np.float64) / np.sqrt(max(1, bond_dim ** len(incident)))
        tensors.append(tensor)
        labels.append(incident)
    return tensors, labels


def _contract_instance(record: dict, bond_dim: int, run_contract: bool, seed: int) -> dict:
    try:
        import opt_einsum as oe
    except Exception as exc:
        return {
            "instance_id": record["id"],
            "mode": record["mode"],
            "status": "opt_einsum_unavailable",
            "error": f"{exc.__class__.__name__}: {exc}",
        }

    graph = _graph_from_record(record)
    tensors, labels = _make_tensor_network(graph, seed, bond_dim)
    args = []
    for tensor, inds in zip(tensors, labels):
        args.extend([tensor, inds])
    args.append([])

    out = {
        "instance_id": record["id"],
        "mode": record["mode"],
        "n_vertices": graph.number_of_nodes(),
        "n_edges": graph.number_of_edges(),
        "bond_dim": bond_dim,
        "status": "planned",
        "path_time_s": "",
        "contract_time_s": "",
        "optimized_flops": "",
        "largest_intermediate": "",
        "contraction_value": "",
        "error": "",
    }
    try:
        t0 = time.perf_counter()
        _path, info = oe.contract_path(*args, optimize="greedy")
        out["path_time_s"] = time.perf_counter() - t0
        out["optimized_flops"] = float(info.opt_cost)
        out["largest_intermediate"] = float(info.largest_intermediate)
        if run_contract:
            t1 = time.perf_counter()
            value = oe.contract(*args, optimize="greedy")
            out["contract_time_s"] = time.perf_counter() - t1
            out["contraction_value"] = float(value)
            out["status"] = "contracted"
    except Exception as exc:
        out["status"] = "failed"
        out["error"] = f"{exc.__class__.__name__}: {exc}"
    return out


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> int:
    records = _read_instances(Path(args.instances))
    selected = []
    for record in records:
        graph = _graph_from_record(record)
        if graph.number_of_nodes() <= args.max_vertices and graph.number_of_edges() <= args.max_edges:
            selected.append(record)
        if len(selected) >= args.limit:
            break
    rows = [
        _contract_instance(record, args.bond_dim, args.run_contract, args.seed + index)
        for index, record in enumerate(selected)
    ]
    _write_csv(Path(args.output), rows)
    print(json.dumps({"instances_selected": len(selected), "output": args.output}, indent=2))
    return 0 if rows else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instances", default=str(RESULTS_DIR / "fallback_instances.json"))
    parser.add_argument("--output", default=str(RESULTS_DIR / "dense_contraction_baseline.csv"))
    parser.add_argument("--limit", type=int, default=24)
    parser.add_argument("--max-vertices", type=int, default=18)
    parser.add_argument("--max-edges", type=int, default=24)
    parser.add_argument("--bond-dim", type=int, default=2)
    parser.add_argument("--run-contract", action="store_true")
    parser.add_argument("--seed", type=int, default=2026)
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
