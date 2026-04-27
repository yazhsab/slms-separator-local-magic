from __future__ import annotations

import argparse
import csv
from pathlib import Path


def _read_rows(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _write_pdf(path: Path, title: str, commands: list[str]) -> None:
    content = [
        "BT /F1 14 Tf 50 760 Td (" + _pdf_escape(title) + ") Tj ET",
        "0.5 w",
        *commands,
    ]
    stream = "\n".join(content).encode("ascii", "ignore")
    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream"
    )
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n".encode("ascii"))
        out.extend(obj)
        out.extend(b"\nendobj\n")
    xref = len(out)
    out.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode("ascii"))
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(bytes(out))


def _scale(value: float, lo: float, hi: float, start: float, end: float) -> float:
    if hi <= lo:
        return (start + end) / 2.0
    return start + (value - lo) * (end - start) / (hi - lo)


def _hist_commands(values: list[float], label: str) -> list[str]:
    if not values:
        return []
    lo, hi = min(values), max(values)
    bins = 12
    counts = [0] * bins
    for value in values:
        idx = 0 if hi == lo else min(bins - 1, int((value - lo) / (hi - lo) * bins))
        counts[idx] += 1
    max_count = max(counts) or 1
    cmds = ["50 90 m 560 90 l S", "50 90 m 50 700 l S"]
    width = 500 / bins
    for i, count in enumerate(counts):
        x = 55 + i * width
        h = 560 * count / max_count
        cmds.append(f"{x:.2f} 90 {width-4:.2f} {h:.2f} re S")
    cmds.append(f"BT /F1 10 Tf 50 60 Td ({_pdf_escape(label)} range {lo:.3f} to {hi:.3f}) Tj ET")
    return cmds


def _scatter_commands(xs: list[float], ys: list[float], xlabel: str, ylabel: str) -> list[str]:
    if not xs or not ys:
        return []
    xlo, xhi = min(xs), max(xs)
    ylo, yhi = min(ys), max(ys)
    cmds = ["50 90 m 560 90 l S", "50 90 m 50 700 l S"]
    for x, y in zip(xs, ys):
        px = _scale(x, xlo, xhi, 70, 550)
        py = _scale(y, ylo, yhi, 110, 690)
        cmds.append(f"{px:.2f} {py:.2f} 2 0 360 arc S")
    cmds.append(f"BT /F1 10 Tf 50 60 Td ({_pdf_escape(xlabel)} range {xlo:.3f} to {xhi:.3f}) Tj ET")
    cmds.append(f"BT /F1 10 Tf 50 45 Td ({_pdf_escape(ylabel)} range {ylo:.3f} to {yhi:.3f}) Tj ET")
    return cmds


def _line_commands(series: list[tuple[str, list[float]]]) -> list[str]:
    all_values = [v for _name, values in series for v in values]
    if not all_values:
        return []
    lo, hi = min(all_values), max(all_values)
    n = max(len(values) for _name, values in series)
    cmds = ["50 90 m 560 90 l S", "50 90 m 50 700 l S"]
    dash_patterns = ["[] 0 d", "[4 3] 0 d", "[1 3] 0 d"]
    for idx, (name, values) in enumerate(series):
        cmds.append(dash_patterns[idx % len(dash_patterns)])
        points = []
        for i, value in enumerate(values):
            x = _scale(i, 0, max(1, n - 1), 70, 550)
            y = _scale(value, lo, hi, 110, 690)
            points.append((x, y))
        if points:
            first = points[0]
            cmds.append(f"{first[0]:.2f} {first[1]:.2f} m")
            for x, y in points[1:]:
                cmds.append(f"{x:.2f} {y:.2f} l")
            cmds.append("S")
        cmds.append("[] 0 d")
        cmds.append(f"BT /F1 10 Tf 420 {720 - 14 * idx} Td ({_pdf_escape(name)}) Tj ET")
    cmds.append(f"BT /F1 10 Tf 50 60 Td (proxy range {lo:.3f} to {hi:.3f}) Tj ET")
    return cmds


def _pass_commands(passed: list[bool]) -> list[str]:
    pass_count = sum(1 for p in passed if p)
    fail_count = len(passed) - pass_count
    max_count = max(1, pass_count, fail_count)
    cmds = ["50 90 m 560 90 l S", "50 90 m 50 700 l S"]
    for i, (label, count) in enumerate([("pass", pass_count), ("fail", fail_count)]):
        x = 120 + i * 180
        h = 560 * count / max_count
        cmds.append(f"{x} 90 100 {h:.2f} re S")
        cmds.append(f"BT /F1 10 Tf {x} 70 Td ({label}: {count}) Tj ET")
    return cmds


def write_plots(results_csv: Path, figures_dir: Path) -> list[str]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    failure_report = results_csv.parent / "plot_failure_report.md"
    if not results_csv.exists():
        failure_report.write_text(
            "# Plot Failure Report\n\n"
            f"Input results file not found: `{results_csv}`\n\n"
            "No plots were generated.\n",
            encoding="utf-8",
        )
        return []
    rows = _read_rows(results_csv)
    if not rows:
        failure_report.write_text(
            "# Plot Failure Report\n\n"
            f"Input results file was empty: `{results_csv}`\n\n"
            "No plots were generated.\n",
            encoding="utf-8",
        )
        return []

    lambda_msg = [float(r["lambda_msg"]) for r in rows]
    lambda_glob = [float(r["lambda_glob"]) for r in rows]
    w_eff = [float(r["w_eff_proxy"]) for r in rows]
    slms = [float(r["slms_proxy"]) for r in rows]
    dense = [float(r["dense_tn_proxy"]) for r in rows]
    global_pwb = [float(r["global_pwb_proxy"]) for r in rows]
    focused = [float(r["focused_width_proxy"]) for r in rows if str(r.get("focused_width_proxy", "")) != ""]
    passed = [r["certificate_pass"] == "True" for r in rows]

    specs = [
        ("exp_lambda_msg_histogram.pdf", "Lambda_msg histogram", _hist_commands(lambda_msg, "Lambda_msg")),
        ("exp_w_eff_histogram.pdf", "w_eff proxy histogram", _hist_commands(w_eff, "w_eff")),
        (
            "exp_lambda_msg_vs_lambda_glob.pdf",
            "Lambda_msg vs Lambda_glob",
            _scatter_commands(lambda_glob, lambda_msg, "Lambda_glob", "Lambda_msg"),
        ),
        (
            "exp_exponent_proxy_comparison.pdf",
            "Exponent proxy comparison",
            _line_commands([("SLMS", slms), ("dense TN", dense), ("global PWB", global_pwb)]),
        ),
        ("exp_certificate_pass_rate.pdf", "Certificate pass/fail breakdown", _pass_commands(passed)),
        (
            "exp_focused_width_proxy_comparison.pdf",
            "Focused-width proxy comparison",
            _line_commands([("SLMS", slms), ("focused proxy", focused), ("dense TN", dense)]),
        ),
    ]
    outputs: list[str] = []
    for filename, title, commands in specs:
        out = figures_dir / filename
        _write_pdf(out, title, commands)
        outputs.append(str(out))
    if failure_report.exists():
        failure_report.unlink()
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    default_root = Path(__file__).resolve().parent.parent.parent
    parser.add_argument("--results-csv", default=str(default_root / "results" / "slms_certificate_results.csv"))
    parser.add_argument("--figures-dir", default=str(default_root / "figures"))
    args = parser.parse_args()
    outputs = write_plots(Path(args.results_csv), Path(args.figures_dir))
    for output in outputs:
        print(output)
    return 0 if outputs else 2


if __name__ == "__main__":
    raise SystemExit(main())
