# SciPost Submission Readiness

Generated: 2026-04-26.

## Readiness Verdict

SciPost Physics Core ready: yes, pending author confirmation of license and public artifact URL/DOI.

The manuscript is now framed as a quantum simulation / quantum tensor-network paper, with QNLP as motivating structured circuit context. The central claim is:

> SLMS is a reproducible certificate-based sufficient condition for additive classical simulation of structured quantum tensor networks with localized non-Clifford resource.

## What Is Ready

- Revised abstract foregrounds quantum tensor-network simulation.
- Introduction states that QNLP/QDisCoCirc are motivating structured families, not the central empirical claim.
- Core novelty paragraph added after the contribution list.
- Related work covers tensor-network treewidth, quasiprobability simulation, stabilizer-rank/magic, junction-tree inference, focused width, ZX, STN/MAST, lambeq, and QDisCoCirc.
- Reproducibility appendix added.
- Code/data availability placeholder added.
- Artifact manifest, hard blocker ledger, parser/ZX/STN blocker reports, and release instructions are present.
- `LICENSE` and root `requirements.txt` are present.
- `parser_failure_logs/` and `worked_certificate/` release-facing index directories are present.
- LaTeX build succeeds.
- Artifact run and plot generation succeed.
- Tests pass.

## Remaining Blockers

- Zenodo DOI is pending.
- GitHub release URL is pending.
- Parser-generated lambeq/QDisCoCirc resource instances remain unavailable.
- Exact Sutcliffe--Kissinger ZX cutting/k-partitioning is not implemented.
- Exact Masot-Llima / Nakhl STN or MAST is not implemented.
- No end-to-end wall-clock SLMS benchmark on parser-generated QNLP circuits exists.

These blockers are now explicitly documented and not represented as solved.

## Artifact DOI Status

Current manuscript placeholders:

- `[Zenodo DOI to be inserted after release]`
- `https://github.com/yazhsab/slms-separator-local-magic`

Do not submit a final archival version until these placeholders are either replaced by real public links or explicitly allowed by the submission workflow as "artifact forthcoming."

## Estimated Readiness Grade

SciPost Physics Core readiness: 82/100.

Rationale: the theory, framing, reproducibility, and limitation disclosure are strong for SciPost Core. The main remaining weakness is empirical external dependency coverage: parser-level QNLP instances and exact external ZX/STN baselines are still absent.

## Recommendation

Submit to SciPost Physics Core after creating the public GitHub/Zenodo artifact release and replacing the placeholders. The submission should be under Quantum Physics / Mathematical Physics / Computational Physics, not AI/NLP.
