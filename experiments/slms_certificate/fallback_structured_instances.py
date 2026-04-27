from __future__ import annotations

import random
from dataclasses import dataclass
from math import log

import networkx as nx


@dataclass
class StructuredInstance:
    instance_id: str
    sentence: str
    mode: str
    graph: nx.Graph
    root: str
    parent: dict[str, str | None]
    children: dict[str, list[str]]
    xi: dict[str, float]
    kappa: dict[str, float]
    resource: dict[str, bool]
    active_edge: dict[tuple[str, str], bool]
    w_eff_proxy: float
    failure_reason: str = ""


def _add_binary_tree(depth: int) -> tuple[nx.Graph, str, dict[str, str | None], dict[str, list[str]]]:
    graph = nx.Graph()
    root = "b0"
    parent: dict[str, str | None] = {root: None}
    children: dict[str, list[str]] = {root: []}
    frontier = [root]
    next_id = 1
    for _ in range(depth):
        new_frontier: list[str] = []
        for node in frontier:
            for _side in range(2):
                child = f"b{next_id}"
                next_id += 1
                graph.add_edge(node, child)
                parent[child] = node
                children.setdefault(node, []).append(child)
                children[child] = []
                new_frontier.append(child)
        frontier = new_frontier
    graph.add_node(root)
    return graph, root, parent, children


def _add_chain(length: int) -> tuple[nx.Graph, str, dict[str, str | None], dict[str, list[str]]]:
    graph = nx.Graph()
    parent: dict[str, str | None] = {}
    children: dict[str, list[str]] = {}
    last = None
    for i in range(length):
        node = f"b{i}"
        graph.add_node(node)
        parent[node] = last
        children[node] = []
        if last is not None:
            graph.add_edge(last, node)
            children[last].append(node)
        last = node
    return graph, "b0", parent, children


def _add_grid(side: int) -> tuple[nx.Graph, str, dict[str, str | None], dict[str, list[str]]]:
    raw = nx.grid_2d_graph(side, side)
    mapping = {node: f"b{i}" for i, node in enumerate(raw.nodes)}
    graph = nx.relabel_nodes(raw, mapping)
    root = mapping[(0, 0)]
    parent: dict[str, str | None] = {root: None}
    children: dict[str, list[str]] = {node: [] for node in graph.nodes}
    queue = [root]
    seen = {root}
    while queue:
        node = queue.pop(0)
        for nbr in sorted(graph.neighbors(node), key=lambda x: int(x[1:])):
            if nbr not in seen:
                seen.add(nbr)
                parent[nbr] = node
                children[node].append(nbr)
                queue.append(nbr)
    return graph, root, parent, children


def _add_complete_chain(size: int) -> tuple[nx.Graph, str, dict[str, str | None], dict[str, list[str]]]:
    graph = nx.complete_graph(size)
    mapping = {node: f"b{node}" for node in graph.nodes}
    graph = nx.relabel_nodes(graph, mapping)
    parent: dict[str, str | None] = {}
    children: dict[str, list[str]] = {}
    previous = None
    for i in range(size):
        node = f"b{i}"
        parent[node] = previous
        children[node] = []
        if previous is not None:
            children[previous].append(node)
        previous = node
    return graph, "b0", parent, children


def _leftmost_path(children: dict[str, list[str]], root: str) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    node = root
    while children.get(node):
        child = children[node][0]
        edges.add((node, child))
        node = child
    return edges


def _cluster_nodes(children: dict[str, list[str]], root: str) -> set[str]:
    if not children[root]:
        return {root}
    cluster_root = children[root][0]
    out: set[str] = set()
    stack = [cluster_root]
    while stack:
        node = stack.pop()
        out.add(node)
        stack.extend(children.get(node, []))
    return out


def generate_instances(config: dict) -> list[StructuredInstance]:
    rng = random.Random(config.get("seed", 7))
    fallback = config.get("fallback", {})
    count = int(fallback.get("num_instances", 120))
    min_depth = int(fallback.get("min_depth", 2))
    max_depth = int(fallback.get("max_depth", 6))
    xi_resource = float(fallback.get("xi_resource", 1.30))
    xi_path = float(fallback.get("xi_path", 1.18))
    kappa_default = float(fallback.get("kappa_default", 1.0))
    modes = list(
        fallback.get(
            "modes",
            [
                "leaf_local",
                "path_active",
                "chain_active",
                "clustered",
                "grid_stabilizer_compressed",
                "dense_like_active",
                "local_failure",
                "mixed",
            ],
        )
    )

    instances: list[StructuredInstance] = []
    for i in range(count):
        mode = modes[i % len(modes)]
        depth = rng.randint(min_depth, max_depth)
        if mode == "chain_active":
            graph, root, parent, children = _add_chain(2 ** min(depth, 5))
        elif mode == "grid_stabilizer_compressed":
            graph, root, parent, children = _add_grid(max(3, depth + 2))
        elif mode == "dense_like_active":
            graph, root, parent, children = _add_complete_chain(max(6, depth + 4))
        else:
            graph, root, parent, children = _add_binary_tree(depth)

        xi = {node: 1.0 for node in graph.nodes}
        kappa = {node: kappa_default for node in graph.nodes}
        resource = {node: False for node in graph.nodes}
        active_edge: dict[tuple[str, str], bool] = {}

        leaves = [node for node, ch in children.items() if not ch]
        path_edges = _leftmost_path(children, root)
        path_child_nodes = {child for _parent, child in path_edges}

        if mode == "leaf_local":
            for leaf in leaves:
                xi[leaf] = xi_resource
                resource[leaf] = True
        elif mode == "path_active":
            for leaf in leaves:
                xi[leaf] = xi_resource
                resource[leaf] = True
            for edge in path_edges:
                active_edge[edge] = True
            for node in path_child_nodes:
                xi[node] = max(xi[node], xi_path)
                resource[node] = True
        elif mode == "chain_active":
            for node in graph.nodes:
                xi[node] = xi_resource
                resource[node] = True
            for parent_node, child_list in children.items():
                for child in child_list:
                    active_edge[(parent_node, child)] = True
        elif mode == "clustered":
            cluster = _cluster_nodes(children, root)
            for node in cluster:
                xi[node] = xi_resource
                resource[node] = True
                if parent[node] is not None:
                    active_edge[(parent[node], node)] = True
        elif mode == "grid_stabilizer_compressed":
            for node in graph.nodes:
                xi[node] = xi_resource
                resource[node] = True
            for parent_node, child_list in children.items():
                for child in child_list:
                    if rng.random() < 0.35:
                        active_edge[(parent_node, child)] = True
        elif mode == "dense_like_active":
            for node in graph.nodes:
                xi[node] = xi_resource
                resource[node] = True
            for parent_node, child_list in children.items():
                for child in child_list:
                    active_edge[(parent_node, child)] = True
        elif mode == "local_failure":
            for node in graph.nodes:
                if node == root or rng.random() < 0.35:
                    xi[node] = xi_resource
                    resource[node] = True
            # Deliberately omit the active edges that would be needed to carry
            # the uncertified resource randomness across separators. These are
            # negative controls for the certificate checker.
        else:
            for leaf in leaves:
                if rng.random() < 0.7:
                    xi[leaf] = xi_resource
                    resource[leaf] = True
            for edge in path_edges:
                if rng.random() < 0.5:
                    active_edge[edge] = True
                    xi[edge[1]] = max(xi[edge[1]], xi_path)
                    resource[edge[1]] = True

        token_count = len(leaves)
        sentence = f"fallback_{mode}_sentence_with_{token_count}_word_modules"
        failure_reason = ""
        if mode == "local_failure":
            failure_reason = "local_marginalization_certificate_missing_for_separator_resource"

        if mode == "dense_like_active":
            w_eff_proxy = max(3.0, graph.number_of_nodes() / 2.0)
        elif mode == "clustered":
            w_eff_proxy = 2.0
        elif mode == "grid_stabilizer_compressed":
            w_eff_proxy = 2.0
        else:
            w_eff_proxy = 1.0

        instances.append(
            StructuredInstance(
                instance_id=f"fallback_{i:04d}",
                sentence=sentence,
                mode=mode,
                graph=graph,
                root=root,
                parent=parent,
                children=children,
                xi=xi,
                kappa=kappa,
                resource=resource,
                active_edge=active_edge,
                w_eff_proxy=w_eff_proxy,
                failure_reason=failure_reason,
            )
        )
    return instances


def leaf_count(instance: StructuredInstance) -> int:
    return sum(1 for node in instance.graph.nodes if not instance.children.get(node))


def active_depth(instance: StructuredInstance) -> int:
    children = instance.children

    def dfs(node: str) -> int:
        best = 0
        for child in children.get(node, []):
            inc = 1 if instance.active_edge.get((node, child), False) else 0
            best = max(best, inc + dfs(child))
        return best

    return dfs(instance.root)


def global_burden(instance: StructuredInstance) -> float:
    return sum(log(instance.xi[node]) for node in instance.graph.nodes if instance.xi[node] > 0)


def instance_to_record(instance: StructuredInstance) -> dict:
    nodes = sorted(instance.graph.nodes, key=lambda x: int(x[1:]) if x[1:].isdigit() else x)
    edges = sorted([list(edge) for edge in instance.graph.edges])
    tree_edges = []
    active_sets = {}
    for parent_node in nodes:
        children = instance.children.get(parent_node, [])
        active_children = [child for child in children if instance.active_edge.get((parent_node, child), False)]
        active_sets[parent_node] = active_children
        for child in children:
            tree_edges.append([parent_node, child])
    return {
        "id": instance.instance_id,
        "mode": instance.mode,
        "sentence": instance.sentence,
        "graph": {"nodes": nodes, "edges": edges},
        "tree_decomposition": {
            "root": instance.root,
            "tree_edges": tree_edges,
            "bags": {node: [node] for node in nodes},
        },
        "resource_locations": [node for node in nodes if instance.resource.get(node, False)],
        "free_stabilizer_like_regions": [node for node in nodes if not instance.resource.get(node, False)],
        "certificate_metadata": {
            "xi": {node: instance.xi[node] for node in nodes},
            "kappa": {node: instance.kappa[node] for node in nodes},
            "active_child_sets": active_sets,
            "w_eff_proxy": instance.w_eff_proxy,
            "failure_reason": instance.failure_reason,
        },
    }
