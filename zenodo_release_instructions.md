# Zenodo Release Instructions

Do not invent a DOI. Use these steps to create the real one.

1. Repository name suggestion: `slms-separator-local-magic`.
2. Recommended release tag: `v1.0-scipost-core-submission`.
3. Confirm the `LICENSE` file with all authors. The current draft uses MIT for code and CC-BY-4.0 for text, figures, and generated data.
4. Remove or exclude unwanted files: `.DS_Store`, `.pytest_cache/`, `__pycache__/`, stale `submission_package/*.zip`, stale `submission_package/*.tar.gz`, and temporary TeX aux files unless intentionally released.
5. Create a clean release archive containing:
   - `main.tex`, `macros.tex`, `refs.bib`, `sections/`, `appendices/`, `figures/`
   - `experiments/slms_certificate/`
   - `results/`
   - `parser_failure_logs/`, `worked_certificate/`
   - `README.md`, `LICENSE`, `requirements.txt`, `artifact_manifest.md`, `build_report.md`, `TODO_remaining.md`
   - blocker reports and readiness reports
   - `main.pdf`
6. Create a GitHub repository or release tag.
7. Connect the GitHub repository to Zenodo.
8. In Zenodo metadata, use:
   - Title: `Separator-Local Treewidth--Magic Simulation Artifact`
   - Authors: `[Authors]`
   - Description: executable certificate evidence for SLMS, a sufficient certificate for additive classical simulation of structured quantum tensor networks with localized non-Clifford resource
   - Keywords: `quantum simulation`, `quantum tensor networks`, `stabilizer`, `magic`, `quasiprobability`, `treewidth`, `QNLP`, `lambeq`
   - Related identifier: arXiv DOI/ID if available
   - License: MIT for code and CC-BY-4.0 for text/data, pending author confirmation
9. Upload or archive the GitHub release.
10. Let Zenodo mint the DOI.
11. Only after DOI minting, update the manuscript and `artifact_manifest.md` with the actual DOI.
12. Rebuild `main.pdf` and record the final DOI-backed artifact hash.

Citation placeholder:

```text
[Authors], Separator-Local Treewidth--Magic Simulation Artifact,
Zenodo, [Zenodo DOI to be inserted after release].
```

Minimum release note:

```text
This artifact contains executable SLMS certificate diagnostics, fallback structured lambeq-compatible instances, lambeq LinearReader graph-only sidecar extraction, baseline proxy/comparator diagnostics, plots, environment reports, and hard-blocker reports. It does not contain parser-generated lambeq/QDisCoCirc resource instances, exact Sutcliffe-Kissinger ZX cutting/k-partitioning, or exact Masot-Llima/Nakhl STN/MAST implementations.
```
