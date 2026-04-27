from __future__ import annotations

from fallback_structured_instances import StructuredInstance


def resource_vertices(instance: StructuredInstance) -> set[str]:
    return {node for node, flag in instance.resource.items() if flag}


def graph_summary(instance: StructuredInstance) -> dict:
    return {
        "vertices": instance.graph.number_of_nodes(),
        "edges": instance.graph.number_of_edges(),
        "root": instance.root,
    }
