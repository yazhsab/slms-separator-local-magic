#!/usr/bin/env python3
"""Summarize and plot synthetic burden-accounting instances.

This script does not simulate quantum circuits. It reads generated accounting
CSV files and computes the same combinatorial recurrence used by the manuscript.
"""

import argparse
import csv
import math
import os


def read_instance(path):
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    parents = {int(r["node"]): (None if r["parent"] == "" else int(r["parent"])) for r in rows}
    children = {node: [] for node in parents}
    root = None
    for node, parent in parents.items():
        if parent is None:
            root = node
        else:
            children[parent].append(node)
    if root is None:
        raise ValueError(f"{path}: missing root")
    xi = {int(r["node"]): float(r["xi"]) for r in rows}
    kappa = {int(r["node"]): float(r.get("kappa", "1.0")) for r in rows}
    resource = {int(r["node"]): bool(int(r.get("resource", "0"))) for r in rows}
    marginalizable = {int(r["node"]): bool(int(r.get("marginalizable", "0"))) for r in rows}
    w_tn = float(rows[0].get("w_tn_proxy", "0") or 0)
    w_eff = float(rows[0].get("w_eff_proxy", "0") or 0)
    return root, parents, children, xi, kappa, resource, marginalizable, w_tn, w_eff


def postorder(root, children):
    out = []

    def visit(node):
        for child in children[node]:
            visit(child)
        out.append(node)

    visit(root)
    return out


def path_burden(root, children, local_log):
    best = 0.0

    def visit(node, acc):
        nonlocal best
        acc += local_log[node]
        if not children[node]:
            best = max(best, acc)
        for child in children[node]:
            visit(child, acc)

    visit(root, 0.0)
    return best


def subtree_burden(root, children, local_log):
    sums = {}
    best = 0.0
    for node in postorder(root, children):
        total = local_log[node] + sum(sums[child] for child in children[node])
        sums[node] = total
        best = max(best, total)
    return best


def certified_lambda_msg(root, children, local_log, resource, marginalizable):
    subtree_ok = {}
    log_gamma = {}
    active_edges = 0
    for node in postorder(root, children):
        active = []
        for child in children[node]:
            if not subtree_ok[child]:
                active.append(child)
        active_edges += len(active)
        own_ok = (not resource[node]) or marginalizable[node]
        subtree_ok[node] = own_ok and all(subtree_ok[child] for child in children[node])
        log_gamma[node] = local_log[node] + sum(log_gamma[child] for child in active)
    return max(log_gamma.values()) if log_gamma else 0.0, active_edges


def summarize(path):
    root, parents, children, xi, kappa, resource, marginalizable, w_tn, w_eff = read_instance(path)
    log_xi = {node: math.log(xi[node]) for node in xi}
    log_kappa = {node: math.log(kappa[node]) for node in kappa}
    local_log = {node: log_xi[node] + log_kappa[node] for node in xi}
    lambda_msg, active_edges = certified_lambda_msg(root, children, local_log, resource, marginalizable)
    global_burden = sum(log_xi.values())
    return {
        "case": os.path.splitext(os.path.basename(path))[0],
        "nodes": len(parents),
        "resource_bags": sum(1 for val in resource.values() if val),
        "global_burden": global_burden,
        "kappa_burden": sum(log_kappa.values()),
        "max_bag_burden": max(local_log.values()) if local_log else 0.0,
        "path_burden": path_burden(root, children, local_log),
        "subtree_burden": subtree_burden(root, children, local_log),
        "lambda_msg": lambda_msg,
        "active_edges": active_edges,
        "w_tn_proxy": w_tn,
        "w_eff_proxy": w_eff,
        "slms_exponent_proxy": w_eff + 2.0 * lambda_msg,
        "dense_tn_exponent_proxy": w_tn,
        "global_sampling_exponent_proxy": global_burden,
    }


def write_summary(rows, path):
    fieldnames = [
        "case",
        "nodes",
        "resource_bags",
        "global_burden",
        "kappa_burden",
        "max_bag_burden",
        "path_burden",
        "subtree_burden",
        "lambda_msg",
        "active_edges",
        "w_tn_proxy",
        "w_eff_proxy",
        "slms_exponent_proxy",
        "dense_tn_exponent_proxy",
        "global_sampling_exponent_proxy",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_grouped_bar_svg(rows, series, labels, colors, path, title):
    width = 980
    height = 460
    margin_left = 70
    margin_bottom = 130
    margin_top = 45
    plot_w = width - margin_left - 30
    plot_h = height - margin_top - margin_bottom
    max_val = max([0.0] + [float(row[key]) for row in rows for key in series])
    max_val = max(max_val, 1.0)
    group_w = plot_w / max(len(rows), 1)
    bar_w = group_w / (len(series) + 1)

    def x_for(i, j):
        return margin_left + i * group_w + (j + 0.5) * bar_w

    def y_for(val):
        return margin_top + plot_h - (float(val) / max_val) * plot_h

    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n')
        f.write('<rect width="100%" height="100%" fill="white"/>\n')
        f.write(f'<text x="{width/2}" y="24" text-anchor="middle" font-family="Arial" font-size="16">{title}</text>\n')
        f.write(f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{width - 20}" y2="{margin_top + plot_h}" stroke="#333"/>\n')
        f.write(f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#333"/>\n')
        for tick in range(5):
            val = max_val * tick / 4
            y = y_for(val)
            f.write(f'<line x1="{margin_left-4}" y1="{y:.2f}" x2="{width-20}" y2="{y:.2f}" stroke="#ddd"/>\n')
            f.write(f'<text x="{margin_left-8}" y="{y+4:.2f}" text-anchor="end" font-family="Arial" font-size="11">{val:.1f}</text>\n')
        for i, row in enumerate(rows):
            for j, key in enumerate(series):
                val = float(row[key])
                x = x_for(i, j)
                y = y_for(val)
                h = margin_top + plot_h - y
                f.write(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w*0.85:.2f}" height="{h:.2f}" fill="{colors[j]}"/>\n')
            label_x = margin_left + i * group_w + group_w / 2
            f.write(f'<text x="{label_x:.2f}" y="{height-88}" text-anchor="end" transform="rotate(-35 {label_x:.2f},{height-88})" font-family="Arial" font-size="11">{row["case"]}</text>\n')
        legend_x = margin_left
        for j, label in enumerate(labels):
            x = legend_x + j * 210
            f.write(f'<rect x="{x}" y="{height-35}" width="14" height="14" fill="{colors[j]}"/>\n')
            f.write(f'<text x="{x+20}" y="{height-23}" font-family="Arial" font-size="12">{label}</text>\n')
        f.write("</svg>\n")


def write_plots(rows, prefix):
    write_grouped_bar_svg(
        rows,
        ["global_burden", "lambda_msg"],
        ["global burden", "Lambda_msg"],
        ["#4c78a8", "#f58518"],
        prefix + "_global_vs_msg.svg",
        "Synthetic accounting: global burden vs Lambda_msg",
    )
    write_grouped_bar_svg(
        rows,
        ["dense_tn_exponent_proxy", "slms_exponent_proxy"],
        ["dense TN exponent", "SLMS exponent"],
        ["#54a24b", "#e45756"],
        prefix + "_dense_vs_slms.svg",
        "Synthetic accounting: dense TN exponent vs SLMS exponent",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--output-summary", default="results/summary.csv")
    parser.add_argument("--plot-prefix", default="results/burdens")
    args = parser.parse_args()

    rows = [summarize(path) for path in args.inputs]
    os.makedirs(os.path.dirname(args.output_summary) or ".", exist_ok=True)
    write_summary(rows, args.output_summary)
    write_plots(rows, args.plot_prefix)
    for row in rows:
        print(
            f"{row['case']}: global={row['global_burden']:.3f}, "
            f"lambda_msg={row['lambda_msg']:.3f}, "
            f"dense={row['dense_tn_exponent_proxy']:.3f}, "
            f"slms={row['slms_exponent_proxy']:.3f}"
        )


if __name__ == "__main__":
    main()
