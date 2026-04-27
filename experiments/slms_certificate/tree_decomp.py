from __future__ import annotations

from fallback_structured_instances import StructuredInstance


def rooted_tree_decomposition_certificate(instance: StructuredInstance) -> dict:
    """Return the explicit tree decomposition used by the fallback instances.

    For fallback grammar trees, every graph node is already a bag and every tree
    edge is a decomposition edge. This is a certificate format, not an optimizer.
    """

    return {
        "root": instance.root,
        "bags": sorted(instance.graph.nodes),
        "parent": instance.parent,
        "children": instance.children,
    }
