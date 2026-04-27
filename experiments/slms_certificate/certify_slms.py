from __future__ import annotations

import json
from math import isfinite, log

from fallback_structured_instances import StructuredInstance, active_depth, global_burden, leaf_count


def compute_gamma(instance: StructuredInstance) -> tuple[dict[str, float], dict[str, float]]:
    gamma: dict[str, float] = {}
    log_gamma: dict[str, float] = {}

    def visit(node: str) -> float:
        value = instance.kappa[node] * instance.xi[node]
        for child in instance.children.get(node, []):
            if instance.active_edge.get((node, child), False):
                value *= visit(child)
            else:
                visit(child)
        gamma[node] = value
        log_gamma[node] = log(value) if value > 0 else float("inf")
        return value

    visit(instance.root)
    return gamma, log_gamma


def certify_instance(instance: StructuredInstance) -> dict:
    gamma, log_gamma = compute_gamma(instance)
    lambda_msg = max(log_gamma.values()) if log_gamma else 0.0
    lambda_glob = global_burden(instance)
    kappa_logs = [log(k) for k in instance.kappa.values() if k > 0]
    xi_values = [instance.xi[node] for node in instance.graph.nodes]
    active_edges = [edge for edge, active in instance.active_edge.items() if active]
    resource_bags = [node for node, flag in instance.resource.items() if flag]
    active_child_sets = {
        node: [child for child in instance.children.get(node, []) if instance.active_edge.get((node, child), False)]
        for node in instance.graph.nodes
    }
    finite_nonnegative = all(isfinite(v) and v >= 0.0 for v in log_gamma.values())
    pass_certificate = (
        finite_nonnegative
        and lambda_glob >= 0.0
        and all(k >= 1.0 for k in instance.kappa.values())
        and not instance.failure_reason
    )
    reason = "" if pass_certificate else instance.failure_reason or "nonfinite_gamma_or_invalid_kappa"
    lambda_kappa = sum(kappa_logs)
    two_lambda_msg = 2.0 * lambda_msg
    return {
        "instance_id": instance.instance_id,
        "mode": instance.mode,
        "sentence": instance.sentence,
        "tokens": leaf_count(instance),
        "n_vertices": instance.graph.number_of_nodes(),
        "n_edges": instance.graph.number_of_edges(),
        "n_resources": len(resource_bags),
        "vertices": instance.graph.number_of_nodes(),
        "edges": instance.graph.number_of_edges(),
        "resource_count": len(resource_bags),
        "Lambda_glob": lambda_glob,
        "Lambda_msg": lambda_msg,
        "Lambda_kappa": lambda_kappa,
        "two_Lambda_msg": two_lambda_msg,
        "lambda_glob": lambda_glob,
        "lambda_msg": lambda_msg,
        "lambda_kappa": lambda_kappa,
        "two_lambda_msg": two_lambda_msg,
        "kappa_min": min(instance.kappa.values()) if instance.kappa else 1.0,
        "kappa_max": max(instance.kappa.values()) if instance.kappa else 1.0,
        "xi_min": min(xi_values) if xi_values else 1.0,
        "xi_max": max(xi_values) if xi_values else 1.0,
        "active_children": len(active_edges),
        "Act_b_json": json.dumps(active_child_sets, sort_keys=True),
        "xi_b_json": json.dumps(instance.xi, sort_keys=True),
        "kappa_b_json": json.dumps(instance.kappa, sort_keys=True),
        "Gamma_b_json": json.dumps(gamma, sort_keys=True),
        "active_child_depth": active_depth(instance),
        "certificate_pass": pass_certificate,
        "failure_reason": reason,
        "w_eff_proxy": instance.w_eff_proxy,
        "gamma_root": gamma.get(instance.root, 1.0),
        "gamma_max": max(gamma.values()) if gamma else 1.0,
    }


def recurrence_rows(instance: StructuredInstance) -> list[dict]:
    gamma, log_gamma = compute_gamma(instance)
    rows = []
    for node in sorted(instance.graph.nodes, key=lambda x: int(x[1:]) if x[1:].isdigit() else x):
        active = [child for child in instance.children.get(node, []) if instance.active_edge.get((node, child), False)]
        rows.append(
            {
                "bag": node,
                "resources": "yes" if instance.resource.get(node, False) else "no",
                "xi_b": instance.xi[node],
                "kappa_b": instance.kappa[node],
                "active_children": " ".join(active) if active else "-",
                "Gamma_b": gamma[node],
                "log_Gamma_b": log_gamma[node],
            }
        )
    return rows
