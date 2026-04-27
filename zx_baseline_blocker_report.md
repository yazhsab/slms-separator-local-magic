# ZX Baseline Blocker Report

Audit date: 2026-04-26.

Final status: `BLOCKED` for the exact Sutcliffe-Kissinger baseline; `PARTIALLY MITIGATED` by pyzx reduction and a labelled heuristic diagnostic.

## Required exact baseline

The requested resolved baseline is Sutcliffe-Kissinger-style ZX cutting, smart k-partitioning, or parametric rewriting, run on the same instances with recorded numerical outputs.

## Repository and installed-package search

Command:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
import pyzx, pkgutil
print('pyzx', getattr(pyzx, '__version__', None))
mods = []
for m in pkgutil.walk_packages(pyzx.__path__, pyzx.__name__ + '.'):
    low = m.name.lower()
    if any(s in low for s in ['cut','partition','part','sutcliffe','kissinger','hyper']):
        mods.append(m.name)
print('\n'.join(mods) if mods else 'NO_MATCHING_PYZX_MODULES')
PY
```

Result:

```text
pyzx 0.10.0
NO_MATCHING_PYZX_MODULES
```

Command:

```bash
/tmp/slms_lambeq_py311/bin/python -m pip install zxpartitioner
```

Result:

```text
ERROR: Could not find a version that satisfies the requirement zxpartitioner (from versions: none)
ERROR: No matching distribution found for zxpartitioner
```

Command:

```bash
rg -n "Sutcliffe|Kissinger|ProcOpt|zxpartition|partitioner" .
```

Result: no vendored exact implementation was found. References and paper text exist; exact algorithm code does not.

## What was run

The repository currently runs:

- `pyzx.simplify.full_reduce` on a synthetic Clifford+T circuit derived from each instance, with a Bravyi-Gosset stabilizer-rank exponent proxy.
- `experiments/slms_certificate/zx_partition_baseline.py`, a simple pyzx graph k-partition heuristic after `full_reduce`.

These outputs are recorded in `results/baseline_results.csv`.

## Does this resolve the requested blocker?

No. The implemented rows are useful comparator diagnostics, but they are not Sutcliffe-Kissinger cutting, smart k-partitioning, or parametric rewriting.

Safe paper wording:

- Allowed: "pyzx reduction heuristic", "pyzx k-partition heuristic", "not Sutcliffe-Kissinger".
- Not allowed: "Sutcliffe-Kissinger baseline implemented", "exact ZX partitioning baseline", "ZX cutting comparison".

## Remaining missing item

Obtain and validate the exact ZX-Partitioner / ProcOptCut implementation, or faithfully reimplement it with tests against the published examples. Until then this blocker remains `BLOCKED`.
