"""Probe parser-level lambeq and QDisCoCirc extraction availability.

The script is intentionally conservative.  It does not fabricate parsed
instances.  It records whether parser-generated lambeq instances and a
QDisCoCirc package are actually available in the current environment.
"""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent.parent
RESULTS_DIR = REPO_ROOT / "results"


def _module_status(name: str) -> dict:
    spec = importlib.util.find_spec(name)
    if spec is None:
        return {"available": False, "error": "module_not_found"}
    try:
        module = __import__(name)
        return {"available": True, "version": getattr(module, "__version__", None), "error": None}
    except Exception as exc:
        return {"available": False, "error": f"{type(exc).__name__}: {exc}"}


def run() -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = RESULTS_DIR / "run_manifest.json"
    real_path = RESULTS_DIR / "real_lambeq_instances.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    lambeq_status = manifest.get("lambeq_status", {"used_lambeq": False, "failure_reason": "run_manifest_missing"})
    real_records = json.loads(real_path.read_text(encoding="utf-8")) if real_path.exists() else []
    parser_instances = real_records if lambeq_status.get("extraction_mode") == "parser" else []
    qdiscocirc_candidates = {
        "qdiscocirc": _module_status("qdiscocirc"),
        "qdisco_circ": _module_status("qdisco_circ"),
    }
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_manifest": str(manifest_path),
        "lambeq_status": lambeq_status,
        "lambeq_instances_total": len(real_records),
        "parser_generated_lambeq_instances": len(parser_instances),
        "qdiscocirc_candidates": qdiscocirc_candidates,
        "qdiscocirc_instances": 0,
        "resource_instances": 0,
        "status": "blocked" if not parser_instances else "parser_instances_available",
        "blocker": (
            "No parser-generated lambeq/QDisCoCirc resource instances are available in this environment. "
            "lambeq reader instances, when present, are graph-only and carry no non-Clifford resource annotations."
        ),
    }
    (RESULTS_DIR / "qnlp_extraction_probe.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (RESULTS_DIR / "qnlp_extraction_probe.md").write_text(
        "# QNLP Extraction Probe\n\n"
        f"Timestamp: {report['timestamp_utc']}\n\n"
        f"Parser-generated lambeq instances: `{report['parser_generated_lambeq_instances']}`\n\n"
        f"QDisCoCirc package candidates: `{json.dumps(qdiscocirc_candidates, sort_keys=True)}`\n\n"
        f"Status: `{report['status']}`\n\n"
        f"Blocker: {report['blocker']}\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    report = run()
    print(json.dumps(report, indent=2))
    return 0 if report["status"] != "blocked" else 2


if __name__ == "__main__":
    raise SystemExit(main())
