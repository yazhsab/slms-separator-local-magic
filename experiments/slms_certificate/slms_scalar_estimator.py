from __future__ import annotations

import argparse
import csv
import json
import math
import time
from pathlib import Path

import numpy as np


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent.parent
RESULTS_DIR = REPO_ROOT / "results"


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _active_resource_count(row: dict) -> int:
    gamma = json.loads(row["Gamma_b_json"])
    xi = json.loads(row["xi_b_json"])
    lambda_msg = float(row["Lambda_msg"])
    threshold = math.exp(lambda_msg) + 1e-9
    active = 0
    for node, gamma_value in gamma.items():
        if float(gamma_value) <= threshold and float(xi.get(node, 1.0)) > 1.0:
            active += 1
    return max(1, min(active, int(row["n_resources"])))


def _estimate_row(row: dict, samples: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    lambda_msg = float(row["Lambda_msg"])
    bound = math.exp(2.0 * lambda_msg)
    # Synthetic signed local-factor estimator: target value is 1.0 and the
    # Bernoulli signs are scaled so the empirical second moment is controlled
    # by the certificate-visible exp(2 Lambda_msg) bound. This is a runtime and
    # variance sanity check for the sampling dependence, not a QNLP simulator.
    active = _active_resource_count(row)
    p = 0.5 + min(0.45, 0.05 / active)
    scale = math.exp(lambda_msg)
    t0 = time.perf_counter()
    signs = np.where(rng.random(samples) < p, 1.0, -1.0)
    estimates = 1.0 + (scale / max(1.0, math.sqrt(active))) * (signs - (2.0 * p - 1.0))
    elapsed = time.perf_counter() - t0
    mean = float(np.mean(estimates))
    variance = float(np.var(estimates, ddof=1)) if samples > 1 else 0.0
    stderr = math.sqrt(variance / samples) if samples else float("nan")
    return {
        "instance_id": row["instance_id"],
        "mode": row["mode"],
        "samples": samples,
        "active_resource_count_proxy": active,
        "lambda_msg": lambda_msg,
        "predicted_second_moment_bound": bound,
        "estimate_mean": mean,
        "estimate_abs_error_from_target_1": abs(mean - 1.0),
        "sample_variance": variance,
        "standard_error": stderr,
        "runtime_s": elapsed,
        "status": "microbenchmark_not_qnlp_simulator",
    }


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> int:
    rows = _read_rows(Path(args.results_csv))
    selected = [row for row in rows if row["certificate_pass"] == "True"][: args.limit]
    out = [_estimate_row(row, args.samples, args.seed + index) for index, row in enumerate(selected)]
    _write_csv(Path(args.output), out)
    print(json.dumps({"instances_selected": len(selected), "samples": args.samples, "output": args.output}, indent=2))
    return 0 if out else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-csv", default=str(RESULTS_DIR / "slms_certificate_results.csv"))
    parser.add_argument("--output", default=str(RESULTS_DIR / "slms_scalar_estimator_results.csv"))
    parser.add_argument("--limit", type=int, default=32)
    parser.add_argument("--samples", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=12345)
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
