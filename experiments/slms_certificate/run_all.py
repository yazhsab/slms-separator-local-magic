from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from baselines import baseline_rows, compute_extended_baselines, compute_focused_width_proxy, dense_width_proxy, exponent_proxies
from certify_slms import certify_instance, recurrence_rows
from fallback_structured_instances import StructuredInstance, generate_instances, instance_to_record
from lambeq_pipeline import try_real_lambeq
from load_sentences import load_sentences
from plot_results import write_plots


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent.parent
RESULTS = REPO_ROOT / "results"
FIGURES = REPO_ROOT / "figures"
LOGS = PACKAGE_DIR / "logs"


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _dependency_status() -> dict:
    import importlib.util as util

    deps = ["networkx", "matplotlib", "numpy", "pandas", "yaml", "lambeq", "discopy", "opt_einsum", "cotengra"]
    status = {}
    for name in deps:
        if util.find_spec(name) is None:
            status[name] = {"available": False, "importable": False, "error": None}
            continue
        try:
            importlib.import_module(name)
            status[name] = {"available": True, "importable": True, "error": None}
        except Exception as exc:
            status[name] = {
                "available": False,
                "importable": False,
                "error": f"{exc.__class__.__name__}: {exc}",
            }
    return status


def _summary(rows: list[dict], mode_used: str, lambeq_status: dict, plots: list[str]) -> dict:
    def vals(key: str) -> list[float]:
        return [float(r[key]) for r in rows]

    def stats(key: str) -> dict:
        xs = sorted(vals(key))
        if not xs:
            return {"min": None, "median": None, "max": None}
        return {"min": xs[0], "median": xs[len(xs) // 2], "max": xs[-1]}

    pass_count = sum(1 for r in rows if str(r["certificate_pass"]) == "True")
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode_used": mode_used,
        "lambeq_status": lambeq_status,
        "instances": len(rows),
        "certificate_pass_count": pass_count,
        "certificate_fail_count": len(rows) - pass_count,
        "lambda_msg": stats("lambda_msg"),
        "lambda_glob": stats("lambda_glob"),
        "w_eff_proxy": stats("w_eff_proxy"),
        "slms_proxy": stats("slms_proxy"),
        "dense_tn_proxy": stats("dense_tn_proxy"),
        "global_pwb_proxy": stats("global_pwb_proxy"),
        "plots": plots,
    }


def _rows_for_instances(instances: list[StructuredInstance]) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    recurrence: list[dict] = []
    for inst in instances:
        row = certify_instance(inst)
        w_tn = dense_width_proxy(inst.graph)
        focused_proxy, focused_status = compute_focused_width_proxy(inst)
        row.update(exponent_proxies(row, w_tn))
        row["focused_width_proxy"] = focused_proxy
        row["focused_width_status"] = focused_status
        # Codsi-Laakkonen, ZX, STN: real numerical values + wall-clock timings.
        ext = compute_extended_baselines(inst, row)
        row.update(ext)
        rows.append(row)
        if not recurrence:
            for rec in recurrence_rows(inst):
                rec["instance_id"] = inst.instance_id
                recurrence.append(rec)
    return rows, recurrence


def run(mode: str) -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    run_log: list[str] = [
        f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}",
        f"command: {' '.join(sys.argv)}",
        f"mode_requested: {mode}",
    ]
    config = yaml.safe_load((PACKAGE_DIR / "config.yaml").read_text(encoding="utf-8"))
    sentences = load_sentences(PACKAGE_DIR / "example_sentences.txt", int(config.get("max_sentences", 120)))
    run_log.append(f"sentences_loaded: {len(sentences)}")

    lambeq_status = {
        "used_lambeq": False,
        "lambeq_available": False,
        "parser_available": False,
        "parser_name": None,
        "real_instances": 0,
        "failure_reason": "not_attempted",
    }
    instances: list[StructuredInstance] = []
    mode_used = mode
    real_instance_count = 0
    fallback_instance_count = 0
    lambeq_reader_sidecar = {}
    if mode in {"auto", "real"}:
        real_instances, lambeq_status = try_real_lambeq(sentences, RESULTS)
        instances = real_instances
        real_instance_count = len(real_instances)
        run_log.append(f"real_lambeq_status: {json.dumps(lambeq_status, sort_keys=True)}")
        if instances:
            if mode == "auto" and lambeq_status.get("extraction_mode") != "parser":
                reader_rows, reader_recurrence = _rows_for_instances(instances)
                reader_failures = [r for r in reader_rows if str(r["certificate_pass"]) != "True"]
                reader_baseline = [baseline for row in reader_rows for baseline in baseline_rows(row)]
                _write_csv(RESULTS / "lambeq_reader_certificate_results.csv", reader_rows)
                _write_csv(RESULTS / "lambeq_reader_certificate_failures.csv", reader_failures)
                _write_csv(RESULTS / "lambeq_reader_baseline_results.csv", reader_baseline)
                _write_csv(RESULTS / "lambeq_reader_worked_certificate_recurrence.csv", reader_recurrence)
                lambeq_reader_sidecar = {
                    "lambeq_reader_results_csv": str(RESULTS / "lambeq_reader_certificate_results.csv"),
                    "lambeq_reader_failures_csv": str(RESULTS / "lambeq_reader_certificate_failures.csv"),
                    "lambeq_reader_baseline_csv": str(RESULTS / "lambeq_reader_baseline_results.csv"),
                    "lambeq_reader_instances": len(reader_rows),
                    "lambeq_reader_certificate_passes": sum(1 for r in reader_rows if str(r["certificate_pass"]) == "True"),
                    "lambeq_reader_extraction_mode": lambeq_status.get("extraction_mode"),
                    "lambeq_reader_note": lambeq_status.get("reader_note", ""),
                }
                mode_used = "fallback_with_lambeq_reader_evidence"
                instances = generate_instances(config)
                fallback_instance_count = len(instances)
            else:
                mode_used = "real"
        elif mode == "real":
            mode_used = "real_failed"
        else:
            mode_used = "fallback"
            instances = generate_instances(config)
            fallback_instance_count = len(instances)
    elif mode == "fallback":
        mode_used = "fallback"
        instances = generate_instances(config)
        fallback_instance_count = len(instances)
    else:
        raise ValueError(f"unknown mode: {mode}")

    if mode_used.startswith("fallback"):
        fallback_records = [instance_to_record(instance) for instance in instances]
        (RESULTS / "fallback_instances.json").write_text(json.dumps(fallback_records, indent=2), encoding="utf-8")

    rows, recurrence = _rows_for_instances(instances)
    failures = [r for r in rows if str(r["certificate_pass"]) != "True"]
    baseline = [baseline for row in rows for baseline in baseline_rows(row)]
    results_csv = RESULTS / "slms_certificate_results.csv"
    _write_csv(results_csv, rows)
    _write_csv(RESULTS / "slms_certificate_failures.csv", failures)
    _write_csv(RESULTS / "worked_certificate_recurrence.csv", recurrence)
    _write_csv(RESULTS / "baseline_results.csv", baseline)
    plots = write_plots(results_csv, FIGURES)
    summary = _summary(rows, mode_used, lambeq_status, plots)
    (RESULTS / "slms_certificate_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    pass_count = sum(1 for r in rows if str(r["certificate_pass"]) == "True")
    warnings = []
    if not lambeq_status.get("used_lambeq"):
        warnings.append("real_lambeq_not_used")
    if mode_used.startswith("fallback"):
        warnings.append("fallback_structured_instances_are_not_real_lambeq_outputs")
    warnings.extend(
        [
            "focused_treewidth_exact_for_n<=22_else_heuristic_upper_bound",
            "focused_rankwidth_recursive_bipartition_upper_bound_NP_hard_in_general",
            "ZX_baseline_uses_pyzx_full_reduce_not_Sutcliffe_Kissinger_cutting",
            "ZX_k_partition_heuristic_is_not_Sutcliffe_Kissinger_exact_algorithm",
            "STN_proxy_is_tableau_plus_Bravyi_Gosset_upper_bound_NOT_Masot_Llima_or_Nakhl",
            "wall_clock_microbenchmarks_recorded_for_focused_widths_pyzx_and_STN_proxy",
            "parser_level_lambeq_extraction_blocked_by_dead_qnlp_cambridgequantum_com_URL",
        ]
    )
    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "commands_run": [" ".join(sys.argv)],
        "command": " ".join(sys.argv),
        "python_executable": sys.executable,
        "environment_overrides": {
            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
            "MPLCONFIGDIR": os.environ.get("MPLCONFIGDIR", ""),
        },
        "python": sys.version,
        "platform": platform.platform(),
        "dependency_status": _dependency_status(),
        "mode_requested": mode,
        "mode_actually_used": mode_used,
        "mode_used": mode_used,
        "lambeq_availability": bool(lambeq_status.get("lambeq_available")),
        "parser_availability": bool(lambeq_status.get("parser_available")),
        "lambeq_used": bool(lambeq_status.get("used_lambeq")),
        "lambeq_status": lambeq_status,
        "number_of_real_instances": real_instance_count,
        "number_of_fallback_instances": fallback_instance_count,
        "number_of_certificate_passes": pass_count,
        "number_of_failures": len(rows) - pass_count,
        "warnings": warnings,
        "instances": len(rows),
        "outputs": {
            "results_csv": str(results_csv),
            "summary_json": str(RESULTS / "slms_certificate_summary.json"),
            "failures_csv": str(RESULTS / "slms_certificate_failures.csv"),
            "baseline_csv": str(RESULTS / "baseline_results.csv"),
            "worked_recurrence_csv": str(RESULTS / "worked_certificate_recurrence.csv"),
            "figures": plots,
            **lambeq_reader_sidecar,
        },
        "limitations": [
            "certificate-evidence only; not wall-clock quantum simulation",
            "fallback mode is lambeq-compatible synthetic structure, not real parsed lambeq output",
            "focused tree-width and focused rank-width are computed exactly only for small instances (<=22 vertices); heuristic upper bound otherwise",
            "ZX baseline uses pyzx full_reduce on a synthetic Clifford+T encoding, not Sutcliffe-Kissinger cutting/parametric rewrites",
            "ZX k-partition heuristic is implemented as a reproducible pyzx graph diagnostic, but it is NOT the Sutcliffe-Kissinger algorithm",
            "STN/MAST proxy is a tableau+Bravyi-Gosset stabilizer-rank upper bound; the Masot-Llima and Nakhl algorithms are NOT implemented",
            "wall-clock timings are recorded for per-instance focused-width, pyzx and STN-proxy computation, not for a full SLMS simulator backend",
            "parser-level lambeq extraction is blocked upstream: qnlp.cambridgequantum.com is NXDOMAIN; lambeq GitHub issues #253, #254, #257 are open",
        ],
    }
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    run_log.extend(
        [
            f"mode_actually_used: {mode_used}",
            f"instances: {len(rows)}",
            f"certificate_passes: {pass_count}",
            f"certificate_failures: {len(rows) - pass_count}",
            f"warnings: {warnings}",
        ]
    )
    (RESULTS / "run_log.txt").write_text("\n".join(run_log) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if rows else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "real", "fallback"], default="auto")
    args = parser.parse_args()
    return run(args.mode)


if __name__ == "__main__":
    raise SystemExit(main())
