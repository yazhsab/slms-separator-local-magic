# SciPost Physics Core Criteria Alignment

Target scope: Quantum Physics / Mathematical Physics / Computational Physics.

## 1. Important Problem

The paper addresses classical simulability of structured quantum tensor networks with localized non-Clifford resource. This is a quantum simulation problem: when can output probabilities of a quantum circuit/tensor network be estimated additively with cost governed by graph width, stabilizer compression, and quasiprobability burden?

## 2. Originality

The original contribution is the certified combination of:

- junction-tree-style message passing;
- finite quasiprobability dictionaries for non-free tensors;
- local quasiprobability `l1` costs;
- stabilizer-compressed separator boundaries;
- local marginalization declarations;
- active-child recurrence certificates.

SLMS is not presented as a new tree-decomposition algorithm by itself. The originality is the checkable sufficient certificate and the explicit message-burden parameter.

## 3. Significant Advance

The main theorem gives a sufficient condition for additive classical simulation with runtime controlled by

```text
w_eff + 2 Lambda_msg
```

equivalently by a dense-boundary factor `2^{O(w_eff)}` and the explicit sampling factor `exp(2 Lambda_msg)`. The result refines global quasiprobability accounting by distinguishing globally present non-Clifford resource from resource labels that are locally consumed before loading high-level separators.

## 4. Reproducibility

The repository includes:

- theorem details and proof appendices;
- worked fallback certificate;
- executable certificate engine;
- fallback structured instances and negative controls;
- CSV outputs and summary JSON files;
- diagnostic plots;
- environment reports;
- parser-failure logs;
- hard blocker ledger separating unavailable exact baselines from implemented proxy diagnostics.

Key files:

- `experiments/slms_certificate/run_all.py`
- `experiments/slms_certificate/plot_results.py`
- `results/slms_certificate_results.csv`
- `results/baseline_results.csv`
- `results/run_manifest.json`
- `hard_blocker_ledger.md`

## 5. Literature

Representative literature covered in the manuscript:

- Markov--Shi tensor-network treewidth simulation.
- Lauritzen--Spiegelhalter, Shafer--Shenoy, and Dechter junction-tree / local computation.
- Pashayan--Wallman--Bartlett and Pashayan--Bartlett--Gross quasiprobability simulation.
- Howard--Campbell and Seddon et al. magic monotones and simulation overheads.
- Bravyi--Gosset and BBCCGH stabilizer-rank / approximate stabilizer-rank simulation.
- Codsi--Laakkonen focused tree-width and focused rank-width.
- Kuyanov--Kissinger low-rank-width ZX simulation.
- Sutcliffe and Sutcliffe--Kissinger ZX partitioning, cutting, and parametric rewriting.
- Masot-Llima--Garcia-Saez STN and Nakhl et al. MAST / magic-state-injection STN.
- lambeq and QDisCoCirc as motivating structured quantum-language circuit frameworks.

## 6. Limitations

The paper explicitly states:

- fallback structured instances are not parser-generated lambeq data;
- parser-level lambeq/QDisCoCirc resource extraction did not run in the audited environment;
- focused-width values are exact only for small cases and upper bounds otherwise;
- pyzx and STN rows are heuristic/proxy diagnostics, not exact Sutcliffe-Kissinger or exact STN/MAST baselines;
- no wall-clock benchmark on parser-generated QNLP circuits is reported;
- no dominance over focused-width, ZX, stabilizer-rank, or STN methods is claimed;
- no quantum advantage claim is made.

## Cover-Letter Use

The strongest SciPost positioning is:

> SLMS is a reproducible certificate-based sufficient condition for additive classical simulation of structured quantum tensor networks with localized non-Clifford resource, motivated by compositional quantum-language circuits.
