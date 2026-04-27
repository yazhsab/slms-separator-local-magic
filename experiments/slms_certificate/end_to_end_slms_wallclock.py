"""Gate for end-to-end SLMS wall-clock benchmarking on real QNLP instances.

The benchmark is only meaningful for parser-generated lambeq/QDisCoCirc
instances with non-Clifford resource annotations.  If the current run only has
LinearReader graph-only instances or fallback structured instances, this script
writes an explicit blocker report and exits nonzero.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx

from certify_slms import certify_instance
from fallback_structured_instances import StructuredInstance


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent.parent
RESULTS_DIR = REPO_ROOT / "results"


def _load_real_records() -> list[dict]:
    path = RESULTS_DIR / "real_lambeq_instances.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _is_parser_resource_record(record: dict) -> bool:
    mode = str(record.get("mode", ""))
    resources = record.get("resource_locations", [])
    has_resource = bool(resources)
    return "linear_reader_not_parser" not in mode and "graph_only" not in mode and has_resource


def _record_to_instance(record: dict) -> StructuredInstance:
    graph = nx.Graph()
    graph.add_nodes_from(record["graph"]["nodes"])
    graph.add_edges_from(tuple(edge) for edge in record["graph"]["edges"])
    td = record["tree_decomposition"]
    root = td["root"]
    parent = {node: None for node in graph.nodes}
    children = {node: [] for node in graph.nodes}
    for parent_node, child in td["tree_edges"]:
        parent[child] = parent_node
        children.setdefault(parent_node, []).append(child)
        children.setdefault(child, [])
    meta = record["certificate_metadata"]
    resources = set(record.get("resource_locations", []))
    active_edge = {}
    for parent_node, active_children in meta.get("active_child_sets", {}).items():
        for child in active_children:
            active_edge[(parent_node, child)] = True
    return StructuredInstance(
        instance_id=record["id"],
        sentence=record.get("sentence", ""),
        mode=record.get("mode", ""),
        graph=graph,
        root=root,
        parent=parent,
        children=children,
        xi={node: float(meta["xi"][node]) for node in graph.nodes},
        kappa={node: float(meta["kappa"][node]) for node in graph.nodes},
        resource={node: node in resources for node in graph.nodes},
        active_edge=active_edge,
        w_eff_proxy=float(meta.get("w_eff_proxy", 1.0)),
        failure_reason=meta.get("failure_reason", ""),
    )


def run() -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    records = _load_real_records()
    selected = [record for record in records if _is_parser_resource_record(record)]
    rows = []
    status = "blocked"
    blocker = ""
    if not selected:
        blocker = (
            "No parser-generated real QNLP records with non-Clifford resource annotations were found. "
            "End-to-end SLMS wall-clock benchmarking would be misleading on fallback or LinearReader graph-only data."
        )
    else:
        status = "ok"
        for record in selected:
            instance = _record_to_instance(record)
            t0 = time.perf_counter()
            cert = certify_instance(instance)
            elapsed = time.perf_counter() - t0
            rows.append({
                "instance_id": instance.instance_id,
                "mode": instance.mode,
                "certificate_pass": cert["certificate_pass"],
                "lambda_msg": cert["lambda_msg"],
                "wallclock_certificate_seconds": elapsed,
            })

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "real_records_seen": len(records),
        "parser_resource_records": len(selected),
        "rows": rows,
        "blocker": blocker,
    }
    (RESULTS_DIR / "end_to_end_slms_wallclock.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (RESULTS_DIR / "end_to_end_slms_wallclock.md").write_text(
        "# End-to-End SLMS Wall-Clock Benchmark\n\n"
        f"Timestamp: {report['timestamp_utc']}\n\n"
        f"Status: `{status}`\n\n"
        f"Real records seen: `{len(records)}`\n\n"
        f"Parser resource records: `{len(selected)}`\n\n"
        f"Blocker: {blocker or 'none'}\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))
    return report


def main() -> int:
    report = run()
    return 0 if report["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
