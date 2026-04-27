# Final Submission Readiness

Audit date: 2026-04-26.

## Current status

QPL-ready: yes, if submitted as a restricted theorem plus executable diagnostic artifact with all limitations included.

Quantum-ready: borderline, not secure. The package is technically honest and artifact-backed, but the empirical layer is still fallback structured data plus graph-only lambeq reader sidecar output.

90% Quantum-ready: no.

Reason: parser-generated lambeq/QDisCoCirc resource instances are absent; exact Sutcliffe-Kissinger ZX cutting/k-partitioning is absent; exact Masot-Llima/Nakhl STN or MAST is absent; and end-to-end SLMS wall-clock benchmarking on parser-generated QNLP circuits is blocked.

## Required next external actions

- Obtain a working Bobcat model directory, DepCCG installation/model, WebParser service path, or serialized parser-generated lambeq/QDisCoCirc diagrams with resource annotations.
- Obtain or vendor an exact Sutcliffe-Kissinger ZX partitioning/cutting implementation, then run it on the same circuit instances.
- Obtain or implement exact Masot-Llima--Garcia-Saez STN and/or Nakhl MAST/magic-state-injection STN baselines.
- Add a `LICENSE`, clean release files, publish a GitHub release, archive on Zenodo, and insert only the real minted DOI.
- If claiming separation/dominance, prove it formally against exact competitor parameters. Otherwise keep the non-dominance wording.

## Honest acceptance estimate

- QPL / categorical quantum venue: 80-88%, assuming full artifact is submitted.
- J. Phys. A / PRA-style journal: 65-78%, depending on reviewer appetite for fallback-only empirical evidence.
- Quantum: 40-60%, with full artifact; lower if the artifact is not public and DOI-backed.
- PRX Quantum / npj Quantum Information: 10-20%.

## Recommended venue path

Submit now to QPL or a specialist theory-methods venue if the goal is publication with the current evidence.

Hold for Quantum if the goal is a high-confidence journal submission. The minimum Quantum-strength upgrade is parser-generated lambeq/QDisCoCirc resource instances plus one exact serious external baseline beyond proxies.

## Final blocker statuses

- Parser-generated lambeq/QDisCoCirc resource instances: `BLOCKED`.
- Real QNLP end-to-end SLMS wall-clock benchmark: `BLOCKED`.
- Exact Sutcliffe-Kissinger ZX cutting / k-partitioning baseline: `BLOCKED`.
- Exact Masot-Llima / Nakhl STN or MAST baseline: `BLOCKED`.
- Public artifact / DOI: `PARTIALLY MITIGATED`.
- Strict separation or dominance claim against focused tree-width / ZX / STN: `BLOCKED`.
- Exact focused tree-width / focused rank-width implementation across all instances: `PARTIALLY MITIGATED`.
- Real worked certificate from parser-generated lambeq instance: `BLOCKED`.

## Bottom line

The repository is now honest enough that a hostile reviewer should not be able to say proxies were misrepresented as exact baselines. It is not 90% Quantum-ready.
