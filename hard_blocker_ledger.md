# Hard Blocker Ledger

Audit date: 2026-04-26.

This ledger uses the requested statuses only: `RESOLVED`, `PARTIALLY MITIGATED`, `BLOCKED`, `NOT ATTEMPTED`. A proxy or heuristic is not counted as resolving an exact-baseline blocker.

## A. Parser-generated lambeq/QDisCoCirc resource instances

Required evidence for `RESOLVED`: at least one CCG/Bobcat/DepCCG/WebParser or QDisCoCirc-generated diagram/circuit extracted from real text, with graph structure and non-Clifford/resource annotations usable by the SLMS certificate engine.

Current repository status: no such instance exists. `results/real_lambeq_instances.json` contains 120 lambeq `cups_reader` / LinearReader graph-only sidecar diagrams. They are not parser-generated and carry no non-Clifford resource annotations. `experiments/slms_certificate/qnlp_extraction_probe.py` reports `parser_generated_lambeq_instances: 0`, `qdiscocirc_instances: 0`, `resource_instances: 0`.

Commands attempted:

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/check_environment.py
/tmp/slms_lambeq_py311/bin/python - <<'PY'
from lambeq import BobcatParser
p = BobcatParser(cache_dir='/tmp/slms_lambeq_models', verbose='text')
print(p.sentence2diagram('Alice likes Bob.'))
PY
/tmp/slms_lambeq_py311/bin/python -m pip install depccg
/tmp/slms_lambeq_py311/bin/python - <<'PY'
from lambeq import DepCCGParser
p = DepCCGParser(verbose='progress')
print(p.sentence2diagram('Alice likes Bob.'))
PY
/tmp/slms_lambeq_py311/bin/python - <<'PY'
from lambeq import WebParser
p = WebParser(verbose='suppress')
print(p.sentence2diagram('Alice likes Bob.'))
PY
/tmp/slms_lambeq_py311/bin/python -m pip install qdiscocirc
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/qnlp_extraction_probe.py
```

Exact errors or missing dependency:

```text
ModelDownloaderError: ModelDownloader raised error: Failed to retrieve remote version number from https://qnlp.cambridgequantum.com/models/bobcat/latest/version.txt
ERROR: Failed to build 'depccg' when getting requirements to build wheel
Could not import Cython, which is required to build depccg extension modules.
Please install cython and numpy prior to installing depccg.
ModuleNotFoundError: No module named 'depccg'
WebParseError: Web parser could not parse 'Alice likes Bob.'
ERROR: No matching distribution found for qdiscocirc
```

Workaround exists: fallback structured instances and lambeq LinearReader graph-only instances.

Scientifically equivalent: no. They exercise the certificate pipeline, but they do not establish parser-level QNLP/QDisCoCirc resource coverage.

Final status: `BLOCKED`.

Recommended next action: obtain a working Bobcat model directory or supported parser backend, or obtain a public QDisCoCirc/lambeq serialized diagram dataset with resource annotations. Then rerun `run_all.py --mode real` and use only parser-generated resource records for real-QNLP claims.

## B. Real QNLP end-to-end SLMS wall-clock benchmark

Required evidence for `RESOLVED`: parser-generated QNLP/QDisCoCirc resource instances, an SLMS estimator operating on those instances, recorded wall-clock runtimes, sample counts, error bars or variance diagnostics, and comparable baseline wall-clock outputs.

Current repository status: the gate script exists and refuses to benchmark fallback or LinearReader graph-only data. `results/end_to_end_slms_wallclock.json` reports `status: blocked`, `real_records_seen: 120`, `parser_resource_records: 0`.

Commands attempted:

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/end_to_end_slms_wallclock.py
```

Exact error or missing dependency:

```text
"No parser-generated real QNLP records with non-Clifford resource annotations were found. End-to-end SLMS wall-clock benchmarking would be misleading on fallback or LinearReader graph-only data."
```

Workaround exists: dense-contraction and signed-sampling microbenchmarks on fallback/graph-derived data.

Scientifically equivalent: no. Those are useful implementation checks, not end-to-end parser-generated QNLP simulator benchmarks.

Final status: `BLOCKED`.

Recommended next action: resolve blocker A first, then implement a real SLMS estimator on the parsed resource circuits and rerun the benchmark gate.

## C. Exact Sutcliffe-Kissinger ZX cutting / k-partitioning baseline

Required evidence for `RESOLVED`: a faithful implementation or installed package for the Sutcliffe-Kissinger cutting/k-partitioning/parametric-rewriting algorithms, run on the same circuit instances, with numerical outputs and limitations recorded.

Current repository status: not available. `pyzx 0.10.0` is installed. No local or installed `ProcOptCut`, `zxpartitioner`, Sutcliffe-Kissinger, or ZX cutting package was found. The repository implements `pyzx full_reduce` and a separate pyzx graph k-partition heuristic, explicitly labelled as heuristic.

Commands attempted:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
import pyzx, pkgutil
print('pyzx', getattr(pyzx, '__version__', None))
for m in pkgutil.walk_packages(pyzx.__path__, pyzx.__name__ + '.'):
    if any(s in m.name.lower() for s in ['cut','partition','part','sutcliffe','kissinger','hyper']):
        print(m.name)
PY
/tmp/slms_lambeq_py311/bin/python -m pip install zxpartitioner
rg -n "Sutcliffe|Kissinger|ProcOpt|zxpartition|partitioner" .
```

Exact error or missing dependency:

```text
pyzx 0.10.0
NO_MATCHING_PYZX_MODULES
ERROR: No matching distribution found for zxpartitioner
```

Workaround exists: `pyzx full_reduce + Bravyi-Gosset` and `experiments/slms_certificate/zx_partition_baseline.py`.

Scientifically equivalent: no. The heuristic is not Sutcliffe-Kissinger cutting, smart k-partitioning, or parametric rewriting.

Final status: `BLOCKED`.

Recommended next action: vendor or depend on the authors' ZX-Partitioner/ProcOptCut implementation if licensing permits, then run it on the benchmark circuits. Until then, keep all paper claims as `pyzx reduction heuristic` or `pyzx k-partition heuristic`.

## D. Exact Masot-Llima / Nakhl STN or MAST baseline

Required evidence for `RESOLVED`: a faithful stabilizer tensor-network implementation of Masot-Llima--Garcia-Saez and/or Nakhl et al. MAST/magic-state-injection STN, run on the same circuit instances with recorded outputs and wall-clock timing.

Current repository status: unavailable. No importable MAST, STN, stabilizer-tensor-network, `stim`, `quimb`, `qiskit`, `pytket`, or `cotengra` package is present in the verified venv. The current row is a tableau plus Bravyi-Gosset upper-bound proxy only.

Commands attempted:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
import importlib.util
for n in ['mast','stn','stabilizer_tensor_network','stabilizertensornetwork',
          'stabilizer_tensor_networks','stabilizer_tn','magic_state_injection',
          'quimb','stim','qiskit','pytket','cotengra']:
    print(n, importlib.util.find_spec(n))
PY
rg -n "MAST|Masot|Nakhl|stabilizer tensor|STN" .
```

Exact error or missing dependency:

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

Workaround exists: `experiments/slms_certificate/stn_baseline.py` computes a tableau plus Bravyi-Gosset upper-bound proxy for the synthetic Clifford+T encoding.

Scientifically equivalent: no. It is not a faithful STN or MAST implementation.

Final status: `BLOCKED`.

Recommended next action: obtain a public or author-provided STN/MAST implementation, or implement the published algorithms as a separate engineering project with validation tests against the papers.

## E. Public artifact / DOI

Required evidence for `RESOLVED`: public repository or archive, permanent DOI, license, clean release contents, reproducibility instructions, and expected output row counts/hashes.

Current repository status: local artifact is mostly ready, but no public DOI can be created from this local session. A release-facing `LICENSE` file is now present. Local stale archives and generated cache files should be excluded from release.

Commands attempted:

```bash
rg --files
find . -maxdepth 3 \( -iname '*license*' -o -iname '.DS_Store' -o -path '*/__pycache__' -o -path '*/.pytest_cache' -o -iname '*.zip' -o -iname '*.tar.gz' \) -print
shasum -a 256 main.pdf figures/*.pdf
```

Exact error or missing dependency: no DOI or public archive exists.

Workaround exists: local `README.md`, `artifact_manifest.md`, `build_report.md`, generated results, and release instructions.

Scientifically equivalent: no. Local readiness is not the same as a public citable artifact.

Final status: `PARTIALLY MITIGATED`.

Recommended next action: clean release exclusions, create a GitHub release, archive it on Zenodo, and insert the real DOI only after Zenodo mints it.

## F. Strict separation or dominance claim against focused tree-width / ZX / STN

Required evidence for `RESOLVED`: a theorem or validated empirical claim showing separation/dominance against the exact competing methods under stated assumptions.

Current repository status: no such theorem is proved, and the paper now avoids dominance claims. This blocker is not resolved; it is defused by honest non-claiming.

Commands attempted: manuscript and claim audit search.

```bash
rg -n "dominance|dominate|supersede|lower bound|Sutcliffe|STN|focused tree-width" main.tex sections appendices
```

Exact error or missing dependency: missing theorem/implementation evidence, not a software error.

Workaround exists: conservative framing that SLMS is a sufficient certificate and diagnostic.

Scientifically equivalent: no. Removing overclaims is not a separation result.

Final status: `BLOCKED`.

Recommended next action: either prove a formal separation from exact competitor parameters on an explicit family, or continue to make no dominance/separation claim.

## G. Exact focused tree-width / focused rank-width implementation rather than proxy

Required evidence for `RESOLVED`: exact focused tree-width and exact focused rank-width computation for all reported instances, or a proof that the algorithm returns exact values on the whole corpus.

Current repository status: partially implemented. The current code computes exact values only on small cases and honest upper bounds otherwise. The legacy focused-width proxy remains separate and labelled as a proxy.

Commands attempted:

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/run_all.py --mode auto
rg -n "focused tree-width|focused rank-width|upper bound|proxy" experiments/slms_certificate sections
```

Exact error or missing dependency: no package error; exact computation is computationally hard at larger sizes and not proven exact for all reported instances.

Workaround exists: exact-small / upper-bound-large diagnostic.

Scientifically equivalent: partially. It is useful comparator evidence, but not exact focused-width evidence across the corpus.

Final status: `PARTIALLY MITIGATED`.

Recommended next action: restrict exact claims to instances within the exact threshold or implement a certified exact solver with branch-and-bound/ILP and proof certificates for larger cases.

## H. Real worked certificate from parser-generated lambeq instance

Required evidence for `RESOLVED`: a worked certificate table from a parser-generated lambeq/QDisCoCirc resource instance, including bags, active-child sets, `xi_b`, `kappa_b`, `Gamma_b`, `Lambda_msg`, and baseline exponents.

Current repository status: absent. Appendix G uses `fallback_0000` and labels it as fallback. There is no parser-generated resource instance to use.

Commands attempted:

```bash
/tmp/slms_lambeq_py311/bin/python experiments/slms_certificate/qnlp_extraction_probe.py
rg -n "Worked certificate|fallback_0000|parser-generated" appendices/G_worked_certificate.tex results
```

Exact error or missing dependency: same as blocker A: parser-generated resource records are zero.

Workaround exists: worked fallback certificate.

Scientifically equivalent: no. The fallback worked certificate validates the recurrence but not real parser-generated QNLP extraction.

Final status: `BLOCKED`.

Recommended next action: resolve blocker A, select the smallest passing parser-generated resource instance, and regenerate Appendix G from that instance.
