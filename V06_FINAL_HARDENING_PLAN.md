# V06 Final Hardening Plan

## 1. Source Tree Completeness

The current source tree is complete for the existing structure. `main.tex` inputs all files that exist under `sections/` and `appendices/`, and `refs.bib` is present. The current structure differs from the target example in file names, but it is internally clean and should be preserved rather than mechanically renamed.

## 2. Compile Status

The previous build using `pdflatex`, `bibtex`, and repeated `pdflatex` succeeded. This pass will test `latexmk -pdf main.tex` if available. If `latexmk` is unavailable, the README and `COMPILE_AUDIT.md` will document the manual build.

## 3. Draft / Version Language

The manuscript body does not contain `v0.*`, `proof target`, or explicit development-log language. Remaining language to check includes conservative negative claims such as "quantum advantage" and "legal AI benefits"; these are intentional denials, not overclaims. I will produce `DRAFT_LANGUAGE_AUDIT.md` with all findings.

## 4. TODO File Status

`TODO_proofs.md` and `TODO_submission.md` are mostly current. Historical versioned audit files remain, but they are audit records rather than manuscript body. I will add `archive/old_TODOs/README.md` documenting that no stale TODO files remain to archive.

## 5. Benchmark Claims

Benchmark scripts and outputs exist. The manuscript table matches `benchmarks/results/summary.csv`. The script names are currently `generate_tree_resource_network.py` and `compute_synthetic_burdens.py`, while the requested submission package names are `generate_synthetic_networks.py` and `compute_burdens.py`. I will add compatibility wrappers and update README language.

## 6. Bibliography Status

`refs.bib` exists and covers the cited works. `CITATION_AUDIT.md` still marks Laakkonen--Meichanetzidis--Coecke and Chia et al. as `VERIFY`. I will use web metadata checks where possible, update entries conservatively, and keep any unresolved items marked `VERIFY`.

## 7. Theorem Support

The theorem stack is supported for locally marginalizable resource-decomposition networks. General separator-local factorization and hard QDisCoCirc regimes are labeled as conjectures. I will create `THEOREM_PROOF_AUDIT.md` and weaken any statement that reads broader than its proof.

## 8. Exact Edits Planned

1. Run or document `latexmk -pdf main.tex`; create `COMPILE_AUDIT.md`.
2. Create `DRAFT_LANGUAGE_AUDIT.md`.
3. Create `THEOREM_PROOF_AUDIT.md`.
4. Update `CITATION_AUDIT.md` and `refs.bib` if metadata checks resolve remaining `VERIFY` items.
5. Add benchmark compatibility wrappers and create `BENCHMARK_AUDIT.md`.
6. Update `README.md` with repository structure, citation status, code availability, limitations, and contact placeholder.
7. Add `cover_letter_draft.md` and `suggested_editors_reviewers_template.md` to `submission_package/`; keep or supersede the older reviewer-template file.
8. Create `FINAL_ACCEPTANCE_AUDIT.md`.
9. Run final benchmark and LaTeX checks.
