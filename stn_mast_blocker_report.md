# STN / MAST Baseline Blocker Report

Audit date: 2026-04-26.

Final status: `BLOCKED` for exact Masot-Llima / Nakhl STN or MAST; `PARTIALLY MITIGATED` by a labelled upper-bound proxy.

## Required exact baseline

The requested resolved baseline is a faithful implementation of the stabilizer tensor-network algorithm of Masot-Llima--Garcia-Saez and/or the magic-state-injection STN/MAST algorithm of Nakhl et al., run on the same circuit instances with numerical outputs and wall-clock timings.

## Package search

Command:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
import importlib.util
names = [
    'mast', 'stn', 'stabilizer_tensor_network',
    'stabilizertensornetwork', 'stabilizer_tensor_networks',
    'stabilizer_tn', 'magic_state_injection',
    'quimb', 'stim', 'qiskit', 'pytket', 'cotengra',
]
for n in names:
    print(n, importlib.util.find_spec(n))
PY
```

Result:

```text
mast None
stn None
stabilizer_tensor_network None
stabilizertensornetwork None
stabilizer_tensor_networks None
stabilizer_tn None
magic_state_injection None
quimb None
stim None
qiskit None
pytket None
cotengra None
```

Repository search:

```bash
rg -n "MAST|Masot|Nakhl|stabilizer tensor|STN" .
```

Result: paper references, limitations, and `experiments/slms_certificate/stn_baseline.py` were found; no exact external implementation is vendored.

## What was attempted and run

The implemented script `experiments/slms_certificate/stn_baseline.py` computes:

```text
STN-style exponent upper bound = alpha_BG * T_count + log(max(1, active_resource_count))
```

for the synthetic Clifford+T encoding used by the artifact. This is recorded as `STN-style upper bound` in `results/baseline_results.csv`.

## Does this resolve the requested blocker?

No. The current tableau plus Bravyi-Gosset row is only a proxy / upper-bound diagnostic. It does not simulate with stabilizer tensor-network states, does not implement magic-state injection STN, and does not reproduce Masot-Llima or Nakhl algorithms.

Safe paper wording:

- Allowed: "STN-style upper-bound proxy", "tableau plus Bravyi-Gosset upper-bound diagnostic".
- Not allowed: "STN baseline implemented", "MAST implemented", "Masot-Llima/Nakhl comparison implemented", "runtime exponent of any STN simulator".

## Remaining missing item

Acquire a public or author-provided implementation, or undertake a separate faithful implementation project with validation against published random Clifford+T benchmarks. Until then the exact STN/MAST blocker remains `BLOCKED`.
