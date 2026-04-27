from __future__ import annotations

import importlib
import importlib.util
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent.parent
RESULTS_DIR = REPO_ROOT / "results"


PACKAGES = [
    "numpy",
    "pandas",
    "networkx",
    "matplotlib",
    "yaml",
    "opt_einsum",
    "cotengra",
    "lambeq",
    "discopy",
    "qiskit",
    "pytket",
    "pytest",
    "pyzx",
    "qdiscocirc",
    "qdisco_circ",
]


def _package_status(name: str) -> dict:
    status = {"available": False, "version": None, "error": None}
    if importlib.util.find_spec(name) is None:
        return status
    try:
        module = importlib.import_module(name)
        status["available"] = True
        status["version"] = getattr(module, "__version__", None)
    except Exception as exc:
        status["error"] = f"{exc.__class__.__name__}: {exc}"
    return status


def _lambeq_parser_status() -> dict:
    if importlib.util.find_spec("lambeq") is None:
        return {
            "lambeq_available": False,
            "parser_available": False,
            "available_parser_classes": [],
            "preferred_parser": None,
            "error": "lambeq package not importable",
        }
    try:
        lambeq = importlib.import_module("lambeq")
    except Exception as exc:
        return {
            "lambeq_available": False,
            "parser_available": False,
            "available_parser_classes": [],
            "preferred_parser": None,
            "error": f"{exc.__class__.__name__}: {exc}",
        }

    names = [
        "BobcatParser",
        "DepCCGParser",
        "CCGParser",
        "WebParser",
        "PregroupTreeParser",
    ]
    available = [name for name in names if hasattr(lambeq, name)]
    return {
        "lambeq_available": True,
        "parser_available": bool(available),
        "available_parser_classes": available,
        "preferred_parser": available[0] if available else None,
        "error": None if available else "no known parser classes found on lambeq module",
    }


def build_report() -> dict:
    packages = {name: _package_status(name) for name in PACKAGES}
    parser = _lambeq_parser_status()
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": {
            "executable": sys.executable,
            "version": sys.version,
            "version_info": list(sys.version_info[:3]),
            "platform": platform.platform(),
        },
        "packages": packages,
        "core_available": all(packages[name]["available"] for name in ["numpy", "pandas", "networkx", "matplotlib", "yaml"]),
        "networkx_available": packages["networkx"]["available"],
        "plotting_available": packages["matplotlib"]["available"],
        "optional_baseline_packages": {
            "opt_einsum": packages["opt_einsum"],
            "cotengra": packages["cotengra"],
            "qiskit": packages["qiskit"],
            "pytket": packages["pytket"],
            "pyzx": packages["pyzx"],
        },
        "qdiscocirc": {
            "qdiscocirc": packages["qdiscocirc"],
            "qdisco_circ": packages["qdisco_circ"],
        },
        "lambeq": parser,
    }


def write_reports(report: dict) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "environment_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        "SLMS Environment Report",
        f"timestamp_utc: {report['timestamp_utc']}",
        f"python_executable: {report['python']['executable']}",
        f"python_version: {report['python']['version'].splitlines()[0]}",
        f"core_available: {report['core_available']}",
        f"lambeq_available: {report['lambeq']['lambeq_available']}",
        f"parser_available: {report['lambeq']['parser_available']}",
        f"preferred_parser: {report['lambeq']['preferred_parser']}",
        f"parser_error: {report['lambeq']['error']}",
        "",
        "Packages:",
    ]
    for name, status in report["packages"].items():
        lines.append(f"- {name}: available={status['available']} version={status['version']} error={status['error']}")
    (RESULTS_DIR / "environment_report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = build_report()
    write_reports(report)
    print(json.dumps(report, indent=2))
    return 0 if report["core_available"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
