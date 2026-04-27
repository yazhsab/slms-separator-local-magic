from __future__ import annotations

import json
import traceback
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx

from fallback_structured_instances import StructuredInstance, instance_to_record
from load_sentences import load_sentences


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent.parent
RESULTS_DIR = REPO_ROOT / "results"


def _import_lambeq():
    try:
        import lambeq  # type: ignore

        return lambeq, None
    except Exception as exc:
        return None, f"lambeq_import_failed: {exc.__class__.__name__}: {exc}"


def _choose_parser(lambeq):
    parser_names = ["BobcatParser", "DepCCGParser", "WebParser", "PregroupTreeParser"]
    available = [name for name in parser_names if hasattr(lambeq, name)]
    if not available:
        return None, None, [], "no_known_lambeq_parser_class_available"
    errors = []
    for name in available:
        cls = getattr(lambeq, name)
        attempts = [
            ({"verbose": "suppress"}, "verbose_suppress"),
            ({}, "no_args"),
        ]
        if name == "BobcatParser":
            attempts.insert(0, ({"verbose": "suppress", "cache_dir": "/tmp/slms_lambeq_models"}, "cache_dir_tmp"))
        for kwargs, label in attempts:
            try:
                return cls(**kwargs), name, available, f"initialized_with_{label}"
            except Exception as exc:
                errors.append(f"{name}({label}) failed: {exc.__class__.__name__}: {exc}")
                continue
    return None, None, available, "parser_classes_found_but_initialization_failed; " + " | ".join(errors[:6])


def _parse_sentences(parser, sentences: list[str]):
    if hasattr(parser, "sentences2diagrams"):
        return parser.sentences2diagrams(sentences)
    if hasattr(parser, "sentence2diagram"):
        return [parser.sentence2diagram(sentence) for sentence in sentences]
    if hasattr(parser, "parse_sentences"):
        return parser.parse_sentences(sentences)
    raise RuntimeError("selected parser exposes no supported sentence-to-diagram method")


def _try_lambeq_reader(lambeq, sentences: list[str], parser_failure: str, parser_name: str | None):
    readers = []
    for name in ["cups_reader", "stairs_reader"]:
        reader = getattr(lambeq, name, None)
        if reader is not None:
            readers.append((name, reader))
    errors = []
    for reader_name, reader in readers:
        try:
            diagrams = reader.sentences2diagrams(sentences)
            return diagrams, reader_name, {
                "parser_failure_reason": parser_failure,
                "parser_failure_parser_name": parser_name,
                "reader_note": "lambeq LinearReader output; not CCG/Bobcat/DepCCG parsed diagrams",
            }
        except Exception as exc:
            errors.append(f"{reader_name}: {exc.__class__.__name__}: {exc}")
    raise RuntimeError("all_lambeq_readers_failed: " + " | ".join(errors))


def _diagram_to_instance(diagram, sentence: str, index: int, parser_name: str) -> StructuredInstance:
    boxes = list(getattr(diagram, "boxes", []) or [])
    box_count = max(1, len(boxes))
    graph = nx.Graph()
    for i in range(box_count):
        graph.add_node(f"b{i}")
        if i > 0:
            graph.add_edge(f"b{i-1}", f"b{i}")

    parent = {f"b{i}": (None if i == 0 else f"b{i-1}") for i in range(box_count)}
    children = {f"b{i}": ([] if i == box_count - 1 else [f"b{i+1}"]) for i in range(box_count)}
    xi = {f"b{i}": 1.0 for i in range(box_count)}
    kappa = {f"b{i}": 1.0 for i in range(box_count)}
    resource = {f"b{i}": False for i in range(box_count)}
    active_edge = {}

    # Real lambeq grammar/reader diagrams do not by themselves identify
    # non-Clifford quantum resources. This extractor therefore records the graph
    # with no magic resources unless a downstream circuitization layer supplies
    # them.
    return StructuredInstance(
        instance_id=f"real_lambeq_{index:04d}",
        sentence=sentence,
        mode=f"real_lambeq_{parser_name}_graph_only",
        graph=graph,
        root="b0",
        parent=parent,
        children=children,
        xi=xi,
        kappa=kappa,
        resource=resource,
        active_edge=active_edge,
        w_eff_proxy=1.0,
    )


def attempt_real_lambeq(sentences: list[str], results_dir: Path = RESULTS_DIR) -> tuple[list[StructuredInstance], dict]:
    results_dir.mkdir(parents=True, exist_ok=True)
    log_lines = [f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}", f"sentences_requested: {len(sentences)}"]
    lambeq, import_error = _import_lambeq()
    if import_error:
        status = {
            "used_lambeq": False,
            "lambeq_available": False,
            "parser_available": False,
            "parser_name": None,
            "real_instances": 0,
            "failure_reason": import_error,
        }
        _write_failure(results_dir, status, log_lines)
        return [], status

    parser, parser_name, available, parser_note = _choose_parser(lambeq)
    log_lines.append(f"available_parser_classes: {available}")
    log_lines.append(f"parser_selection_note: {parser_note}")
    if parser is None or parser_name is None:
        status = {
            "used_lambeq": False,
            "lambeq_available": True,
            "parser_available": False,
            "parser_name": parser_name,
            "real_instances": 0,
            "failure_reason": parser_note,
        }
        _write_failure(results_dir, status, log_lines)
        return [], status

    extraction_mode = "parser"
    extra_status = {}
    try:
        diagrams = _parse_sentences(parser, sentences)
    except Exception as exc:
        parser_failure = f"real_lambeq_parser_failed: {exc.__class__.__name__}: {exc}"
        log_lines.append(traceback.format_exc())
        try:
            diagrams, reader_name, extra_status = _try_lambeq_reader(lambeq, sentences, parser_failure, parser_name)
            parser_name = reader_name
            extraction_mode = "linear_reader_not_parser"
            log_lines.append(f"parser_fallback_to_lambeq_reader: {reader_name}")
            log_lines.append(parser_failure)
        except Exception as reader_exc:
            status = {
                "used_lambeq": False,
                "lambeq_available": True,
                "parser_available": True,
                "parser_name": parser_name,
                "real_instances": 0,
                "extraction_mode": "failed",
                "failure_reason": (
                    f"real_lambeq_parse_or_extract_failed: {exc.__class__.__name__}: {exc}; "
                    f"reader_fallback_failed: {reader_exc.__class__.__name__}: {reader_exc}"
                ),
            }
            log_lines.append(traceback.format_exc())
            _write_failure(results_dir, status, log_lines)
            return [], status

    try:
        instances = [
            _diagram_to_instance(diagram, sentence, idx, str(parser_name))
            for idx, (diagram, sentence) in enumerate(zip(diagrams, sentences))
            if diagram is not None
        ]
    except Exception as exc:
        status = {
            "used_lambeq": False,
            "lambeq_available": True,
            "parser_available": True,
            "parser_name": parser_name,
            "real_instances": 0,
            "extraction_mode": extraction_mode,
            "failure_reason": f"real_lambeq_extract_failed: {exc.__class__.__name__}: {exc}",
        }
        log_lines.append(traceback.format_exc())
        _write_failure(results_dir, status, log_lines)
        return [], status

    records = [instance_to_record(instance) for instance in instances]
    (results_dir / "real_lambeq_instances.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    log_lines.append(f"real_instances_extracted: {len(instances)}")
    log_lines.append(f"extraction_mode: {extraction_mode}")
    log_lines.append("resource_note: extracted lambeq graphs contain no non-Clifford resources unless downstream circuitization supplies them")
    (results_dir / "real_lambeq_parse_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    if extraction_mode == "linear_reader_not_parser":
        _write_parser_fallback_report(results_dir, status_context={
            "parser_name": parser_name,
            "real_instances": len(instances),
            **extra_status,
        })
    status = {
        "used_lambeq": True,
        "lambeq_available": True,
        "parser_available": True,
        "parser_name": parser_name,
        "real_instances": len(instances),
        "extraction_mode": extraction_mode,
        "failure_reason": "",
        **extra_status,
    }
    return instances, status


def _write_parser_fallback_report(results_dir: Path, status_context: dict) -> None:
    (results_dir / "real_lambeq_failure_report.md").write_text(
        "# Parser-Level lambeq Failure and Reader Fallback Report\n\n"
        f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n\n"
        "lambeq imported successfully and a local LinearReader path produced graph-only diagrams.\n\n"
        "Parser-generated Bobcat/DepCCG/CCG-style extraction did not succeed in this run.\n\n"
        f"Parser failure: `{status_context.get('parser_failure_reason', '')}`\n\n"
        f"Reader used: `{status_context.get('parser_name', '')}`\n\n"
        f"Reader instances extracted: `{status_context.get('real_instances', 0)}`\n\n"
        "These reader outputs are not claimed as parser-level QNLP evidence and carry no non-Clifford resource annotations in this artifact.\n",
        encoding="utf-8",
    )


def _write_failure(results_dir: Path, status: dict, log_lines: list[str]) -> None:
    (results_dir / "real_lambeq_parse_log.txt").write_text("\n".join(log_lines + [json.dumps(status, indent=2)]) + "\n", encoding="utf-8")
    (results_dir / "real_lambeq_failure_report.md").write_text(
        "# Real lambeq Failure Report\n\n"
        f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n\n"
        "The real lambeq pipeline did not produce parsed instances.\n\n"
        f"Failure reason: `{status['failure_reason']}`\n\n"
        "No real lambeq results are claimed from this run.\n",
        encoding="utf-8",
    )


def main() -> int:
    sentences = load_sentences(PACKAGE_DIR / "example_sentences.txt", 500)
    instances, status = attempt_real_lambeq(sentences, RESULTS_DIR)
    print(json.dumps(status, indent=2))
    return 0 if instances else 2


if __name__ == "__main__":
    raise SystemExit(main())
