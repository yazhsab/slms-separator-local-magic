#!/usr/bin/env python3
"""Conservative synthetic local-marginalizability certification.

This is not a quantum-circuit verifier. It mirrors the paper's certificate logic
on generated tree/resource CSV files: a child subtree is marked inactive when
all resource-bearing nodes in that subtree are flagged marginalizable.
Otherwise the child is active.
"""

import argparse
import csv
import math


def read_tree(path):
    parents = {}
    xi = {}
    kappa = {}
    resource = {}
    marginalizable = {}
    boundary_dim = {}
    w_tn_proxy = None
    w_eff_proxy = None
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            node = int(row["node"])
            parents[node] = None if row["parent"] == "" else int(row["parent"])
            xi[node] = float(row["xi"])
            kappa[node] = float(row.get("kappa", "1.0"))
            resource[node] = bool(int(row.get("resource", "0")))
            marginalizable[node] = bool(int(row.get("marginalizable", "0")))
            boundary_dim[node] = int(row.get("boundary_dim", "2"))
            if row.get("w_tn_proxy", "") != "":
                w_tn_proxy = float(row["w_tn_proxy"])
            if row.get("w_eff_proxy", "") != "":
                w_eff_proxy = float(row["w_eff_proxy"])
    children = {node: [] for node in parents}
    root = None
    for node, parent in parents.items():
        if parent is None:
            root = node
        else:
            children[parent].append(node)
    if root is None:
        raise ValueError("missing root")
    return root, parents, children, xi, kappa, resource, marginalizable, boundary_dim, w_tn_proxy, w_eff_proxy


def postorder(root, children):
    out = []

    def visit(node):
        for child in children[node]:
            visit(child)
        out.append(node)

    visit(root)
    return out


def certify(root, children, xi, kappa, resource, marginalizable, boundary_dim):
    subtree_ok = {}
    log_gamma = {}
    active = {}
    max_weff = 0.0
    for node in postorder(root, children):
        active[node] = []
        for child in children[node]:
            if not subtree_ok[child]:
                active[node].append(child)
        own_ok = (not resource[node]) or marginalizable[node]
        subtree_ok[node] = own_ok and all(subtree_ok[child] for child in children[node])
        log_gamma[node] = math.log(xi[node]) + math.log(kappa[node]) + sum(log_gamma[child] for child in active[node])
        max_weff = max(max_weff, math.log(max(1, boundary_dim[node]), 2))
    return subtree_ok, active, log_gamma, max_weff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--save-csv", default="")
    args = parser.parse_args()

    root, parents, children, xi, kappa, resource, marginalizable, boundary_dim, w_tn_proxy, w_eff_proxy = read_tree(args.input)
    subtree_ok, active, log_gamma, max_weff = certify(root, children, xi, kappa, resource, marginalizable, boundary_dim)

    log_xi = {node: math.log(val) for node, val in xi.items()}
    log_kappa = {node: math.log(val) for node, val in kappa.items()}
    global_burden = sum(log_xi.values())
    kappa_burden = sum(log_kappa.values())
    lambda_msg = max(log_gamma.values()) if log_gamma else 0.0
    if w_eff_proxy is not None:
        max_weff = w_eff_proxy
    if w_tn_proxy is None:
        w_tn_proxy = 0.0
    active_edges = sum(len(v) for v in active.values())
    failed_subtrees = sum(1 for ok in subtree_ok.values() if not ok)

    print(f"nodes,{len(parents)}")
    print(f"global_burden,{global_burden}")
    print(f"kappa_burden,{kappa_burden}")
    print(f"lambda_msg,{lambda_msg}")
    print(f"w_tn_proxy,{w_tn_proxy}")
    print(f"certified_w_eff,{max_weff}")
    print(f"slms_exponent_proxy,{max_weff + 2.0 * lambda_msg}")
    print(f"dense_tn_exponent_proxy,{w_tn_proxy}")
    print(f"global_sampling_exponent_proxy,{global_burden}")
    print(f"active_edges,{active_edges}")
    print(f"failed_subtrees,{failed_subtrees}")

    if args.save_csv:
        with open(args.save_csv, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["node", "parent", "resource", "marginalizable", "subtree_certified", "log_gamma", "active_children"],
            )
            writer.writeheader()
            for node in sorted(parents):
                writer.writerow({
                    "node": node,
                    "parent": "" if parents[node] is None else parents[node],
                    "resource": int(resource[node]),
                    "marginalizable": int(marginalizable[node]),
                    "subtree_certified": int(subtree_ok[node]),
                    "log_gamma": log_gamma[node],
                    "active_children": " ".join(str(c) for c in active[node]),
                })


if __name__ == "__main__":
    main()
