#!/usr/bin/env python3
"""Compute synthetic global/path/subtree/message burdens from a generated tree."""

import argparse
import csv
import math


def read_tree(path):
    parents = {}
    xi = {}
    kappa = {}
    w_tn_proxy = None
    w_eff_proxy = None
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            node = int(row["node"])
            parent = None if row["parent"] == "" else int(row["parent"])
            parents[node] = parent
            xi[node] = float(row["xi"])
            kappa[node] = float(row.get("kappa", "1.0"))
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
        raise ValueError("tree has no root")
    return root, parents, children, xi, kappa, w_tn_proxy, w_eff_proxy


def postorder(root, children):
    out = []

    def visit(node):
        for child in children[node]:
            visit(child)
        out.append(node)

    visit(root)
    return out


def path_burden(root, children, log_xi):
    best = 0.0

    def visit(node, acc):
        nonlocal best
        acc += log_xi[node]
        if not children[node]:
            best = max(best, acc)
        for child in children[node]:
            visit(child, acc)

    visit(root, 0.0)
    return best


def subtree_burden(root, children, log_xi):
    sums = {}
    best = 0.0
    for node in postorder(root, children):
        total = log_xi[node] + sum(sums[child] for child in children[node])
        sums[node] = total
        best = max(best, total)
    return best


def lambda_msg(root, children, log_xi, active_rule):
    log_gamma = {}
    active_children = {}
    for node in postorder(root, children):
        child_values = [(child, log_gamma[child]) for child in children[node]]
        if active_rule == "all":
            active = [child for child, _ in child_values]
        elif active_rule == "none":
            active = []
        elif active_rule == "max-child":
            active = [max(child_values, key=lambda item: item[1])[0]] if child_values else []
        elif active_rule == "positive":
            active = [child for child, val in child_values if val > 0.0]
        else:
            raise ValueError(f"unknown active rule: {active_rule}")
        active_children[node] = active
        log_gamma[node] = log_xi[node] + sum(log_gamma[child] for child in active)
    return max(log_gamma.values()), log_gamma, active_children


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--active-rule", choices=["all", "none", "max-child", "positive"], default="max-child")
    parser.add_argument("--save-csv", default="")
    args = parser.parse_args()

    root, parents, children, xi, kappa, w_tn_proxy, w_eff_proxy = read_tree(args.input)
    log_xi = {node: math.log(val) for node, val in xi.items()}
    log_kappa = {node: math.log(val) for node, val in kappa.items()}
    local_log = {node: log_xi[node] + log_kappa[node] for node in xi}
    global_b = sum(log_xi.values())
    kappa_b = sum(log_kappa.values())
    max_bag = max(local_log.values()) if local_log else 0.0
    path_b = path_burden(root, children, local_log)
    subtree_b = subtree_burden(root, children, local_log)
    msg_b, log_gamma, active_children = lambda_msg(root, children, local_log, args.active_rule)
    if w_tn_proxy is None:
        w_tn_proxy = path_b
    if w_eff_proxy is None:
        w_eff_proxy = 0.0

    rows = [
        ("nodes", len(parents)),
        ("active_rule", args.active_rule),
        ("global_burden", global_b),
        ("kappa_burden", kappa_b),
        ("max_bag_burden", max_bag),
        ("path_burden", path_b),
        ("subtree_burden", subtree_b),
        ("lambda_msg", msg_b),
        ("w_tn_proxy", w_tn_proxy),
        ("w_eff_proxy", w_eff_proxy),
        ("slms_exponent_proxy", w_eff_proxy + 2.0 * msg_b),
        ("dense_tn_exponent_proxy", w_tn_proxy),
        ("global_sampling_exponent_proxy", global_b),
    ]
    for key, value in rows:
        print(f"{key},{value}")

    if args.save_csv:
        with open(args.save_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["node", "parent", "log_xi", "log_kappa", "log_gamma", "active_children"])
            writer.writeheader()
            for node in sorted(parents):
                writer.writerow({
                    "node": node,
                    "parent": "" if parents[node] is None else parents[node],
                    "log_xi": log_xi[node],
                    "log_kappa": log_kappa[node],
                    "log_gamma": log_gamma[node],
                    "active_children": " ".join(str(c) for c in active_children[node]),
                })


if __name__ == "__main__":
    main()
