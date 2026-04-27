# Build Report

Generated: 2026-04-26.

## LaTeX Build

Command:

```bash
latexmk -pdf main.tex
```

Status: success.

Output:

- `main.pdf`
- 47 pages
- sha256 `7d00ce8b3d6b78bb26b8f1509b06199fd614ccee8468708958ec9445de68c6cd`

Log audit:

```bash
rg -n "undefined|Undefined|Citation|Reference|Overfull" main.log main.blg
```

Status: no matches. No unresolved citations, unresolved references, or overfull boxes were found by this scan.

Warnings remaining:

- `quantumarticle` warning about replacing `\today` before arXiv upload.
- `hyperref` warnings removing `\thanks` from PDF strings.
- `caption` package warning about unknown document class defaults.
- underfull hbox warnings in title/monospace-heavy artifact paragraphs.

## Artifact Environment Check

Command:

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/check_environment.py
```

Status: success.

Key environment facts:

- Python 3.11.14 in `/tmp/slms_lambeq_py311`.
- `lambeq 0.5.0` available.
- `discopy 1.2.2` available.
- `pyzx 0.10.0` available.
- `qdiscocirc` and `qdisco_circ` unavailable.
- `cotengra`, `qiskit`, and `pytket` unavailable in the verified venv.

## Artifact Run

Command:

```bash
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/run_all.py --mode auto
```

Status: success.

Mode used: `fallback_with_lambeq_reader_evidence`.

Result summary from `results/slms_certificate_summary.json`:

- Primary fallback instances: 120.
- Certificate passes/failures: 105 / 15.
- Parser-generated lambeq instances: 0.
- lambeq LinearReader graph-only sidecar instances: 120.
- Median `Lambda_msg`: 0.9244220183777844.
- Median `w_eff_proxy`: 1.0.
- Median SLMS exponent proxy: 3.574185586804947.
- Median global PWB proxy: 8.395656462959717.

## Plot Generation

Command:

```bash
MPLCONFIGDIR=/tmp/slms_mplconfig /tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/plot_results.py
```

Status: success.

Generated figures:

- `figures/exp_lambda_msg_histogram.pdf`
- `figures/exp_w_eff_histogram.pdf`
- `figures/exp_lambda_msg_vs_lambda_glob.pdf`
- `figures/exp_exponent_proxy_comparison.pdf`
- `figures/exp_certificate_pass_rate.pdf`
- `figures/exp_focused_width_proxy_comparison.pdf`

## Tests

Command:

```bash
pytest experiments/slms_certificate/tests
```

Status: success, 5 passed.

## Expected Blocker-Probe Failures

Command:

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/qnlp_extraction_probe.py
```

Status: expected exit code 2. The probe reports:

- parser-generated lambeq instances: 0.
- QDisCoCirc instances: 0.
- resource instances: 0.
- blocker: no parser-generated lambeq/QDisCoCirc resource instances are available.

Command:

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/end_to_end_slms_wallclock.py
```

Status: expected exit code 2. The probe reports:

- real records seen: 120.
- parser resource records: 0.
- blocker: no parser-generated real QNLP records with non-Clifford resource annotations.

## Generated File Hashes

```text
main.pdf 7d00ce8b3d6b78bb26b8f1509b06199fd614ccee8468708958ec9445de68c6cd
results/slms_certificate_results.csv 159e03c89f623543d22c881b581c0ed61b61f271cad178c3f4521b43b2eb5463
results/slms_certificate_failures.csv d594c0d993648c97f2c33f21b33af22080642d4c1a1ce1d05de5949250aef6e5
results/baseline_results.csv ee2a5c09323b9e97f60e3e4d9ab5c086daf3cb89a4c1deec8f2610a88e169413
results/fallback_instances.json 7ce663cf36cbc42aa7630a44c4f102d0fbcac2eee36f981c385326f63c87020a
results/real_lambeq_instances.json 23dcdc864967c174fb4eb8bf9ec9773717c19ae9ac12cab695b38e6c529606e0
results/run_manifest.json 8280cb3b3272482c8acc71a6d387a3e461ad2c9774e398ede5ae18c1b9b23365
results/slms_certificate_summary.json 6d2d24fad8560845d0f14e19f5f34951be1eb074e24dcc150ba024291413f989
```

Figure hashes:

```text
figures/exp_certificate_pass_rate.pdf da33e19b8e3be71d9375520b6b972586ceeb13948f9c8b25a445b0d29f5f555d
figures/exp_exponent_proxy_comparison.pdf f163a54de221d201b778a55c1b09e1f171820f14be21de67e155b98d246f7991
figures/exp_focused_width_proxy_comparison.pdf fab11ff993ea6b27997eae6bea02b5451f1599ede8b8c08cfb297553570db64e
figures/exp_lambda_msg_histogram.pdf 9d85703b99e4ce9e0ec254cbf31b6b7b3c269396514dad75a62d12b72f439c2d
figures/exp_lambda_msg_vs_lambda_glob.pdf b81f72c4b498f120e7ba682ff55d4f9552b6d18db3f8e43bafec8fafcdf5b588
figures/exp_w_eff_histogram.pdf 3d82e0035afee03a6d3dae00d1015124620fe0a14531654cb7fc785503effa3c
```

## Known Warnings

- The artifact does not contain parser-generated lambeq/QDisCoCirc resource instances.
- Exact Sutcliffe--Kissinger ZX cutting/k-partitioning is not implemented.
- Exact Masot-Llima / Nakhl STN or MAST is not implemented.
- Zenodo DOI is minted: `10.5281/zenodo.19805000`; GitHub URL is `https://github.com/yazhsab/slms-separator-local-magic`.
