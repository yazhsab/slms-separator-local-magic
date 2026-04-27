# lambeq Parser Blocker Report

Audit date: 2026-04-26.

Final status: `BLOCKED`.

## Environment

```text
Python: 3.11.14
Executable: /tmp/slms_lambeq_py311/bin/python
lambeq: 0.5.0
discopy: 1.2.2
qdiscocirc: unavailable
qdisco_circ: unavailable
```

`check_environment.py` reports parser classes `BobcatParser`, `DepCCGParser`, `CCGParser`, and `WebParser` as importable. Importability did not translate into successful parser-generated diagrams.

## Attempts

### 1. Existing installed lambeq parser tools

Command:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
import inspect, importlib.util
import lambeq
print('lambeq', getattr(lambeq, '__version__', None))
for name in ['BobcatParser','DepCCGParser','WebParser','CCGParser',
             'PregroupTreeParser','LinearReader','TreeReader',
             'cups_reader','stairs_reader']:
    obj = getattr(lambeq, name, None)
    print(name, 'FOUND' if obj is not None else 'MISSING',
          inspect.signature(obj) if obj is not None and callable(obj) else '')
for mod in ['qdiscocirc','qdisco_circ']:
    print(mod, importlib.util.find_spec(mod))
PY
```

Result:

```text
lambeq 0.5.0
BobcatParser FOUND
DepCCGParser FOUND
WebParser FOUND
CCGParser FOUND
PregroupTreeParser MISSING
LinearReader FOUND
TreeReader FOUND
cups_reader FOUND
stairs_reader FOUND
qdiscocirc None
qdisco_circ None
```

### 2. BobcatParser with local model path

Command:

```bash
find /tmp/slms_lambeq_models /tmp/slms_lambeq_py311 -maxdepth 5 \
  \( -iname '*bobcat*' -o -iname '*model*' -o -iname '*ccg*' -o -iname '*diagram*' \) -print
find /tmp/slms_lambeq_models/lambeq/bobcat -maxdepth 3 -type f -print
```

Result: only an empty `/tmp/slms_lambeq_models/lambeq/bobcat` cache directory and installed package source paths were found; no usable local Bobcat model files were present.

### 3. BobcatParser with documented/default model URL

Command:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
from lambeq import BobcatParser
try:
    p = BobcatParser(cache_dir='/tmp/slms_lambeq_models', verbose='text')
    print('BOBCAT_INIT_OK', p)
    print(p.sentence2diagram('Alice likes Bob.'))
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
PY
```

Result:

```text
ModelDownloaderError: ModelDownloader raised error: Failed to retrieve remote version number from https://qnlp.cambridgequantum.com/models/bobcat/latest/version.txt
```

### 4. DepCCG parser

Command:

```bash
/tmp/slms_lambeq_py311/bin/python -m pip install depccg
```

Result:

```text
ERROR: Failed to build 'depccg' when getting requirements to build wheel
Could not import Cython, which is required to build depccg extension modules.
Please install cython and numpy prior to installing depccg.
```

Command:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
from lambeq import DepCCGParser
try:
    p = DepCCGParser(verbose='progress')
    print('DEPCCG_INIT_OK', p)
    print(p.sentence2diagram('Alice likes Bob.'))
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
PY
```

Result:

```text
ModuleNotFoundError: No module named 'depccg'
```

### 5. WebParser

Command:

```bash
/tmp/slms_lambeq_py311/bin/python - <<'PY'
from lambeq import WebParser
try:
    p = WebParser(verbose='suppress')
    d = p.sentence2diagram('Alice likes Bob.')
    print('WEBPARSER_OK', d)
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
PY
```

Result:

```text
WebParseError: Web parser could not parse 'Alice likes Bob.'
```

### 6. Alternative lambeq-compatible parser route

The local `cups_reader` route is available and was exercised by `run_all.py`. It produced 120 lambeq LinearReader diagrams and graph extraction records in `results/real_lambeq_instances.json`.

This does not resolve the blocker because LinearReader output is not CCG/Bobcat/DepCCG parser output and the extracted records have no non-Clifford resource annotations.

### 7. Manual import of pre-parsed diagrams

No repository-local serialized parser-generated lambeq diagrams were found. The installed lambeq package contains code and documentation references but no local Bobcat model or ready-to-import parser-output dataset suitable for this artifact.

### 8. Public notebooks or datasets

Public lambeq documentation and package metadata describe Bobcat parsing and lambeq's QNLP pipeline, but this repository does not contain downloaded serialized diagrams or a pinned dataset with parser outputs. The Quantinuum/CQCL lambeq README notes that DepCCG support requires a separately installed external parser and says DepCCG-related functionality is no longer actively supported.

References checked through web search:

- `https://github.com/CQCL/lambeq`
- `https://docs.quantinuum.com/lambeq/`
- `https://docs.quantinuum.com/lambeq/tutorials/discocirc-basics.html`

## Blocker classification

The failure is mixed environmental/upstream:

- Bobcat requires a model file not available locally and failed during remote version lookup.
- DepCCG is an external dependency and did not install/build in the audited Python 3.11 environment.
- WebParser failed remotely for the sample sentence.
- QDisCoCirc package candidates are not importable and did not resolve from PyPI.

External file/model needed: a working Bobcat model directory compatible with lambeq 0.5.0, or a working DepCCG installation plus model, or a public serialized lambeq/QDisCoCirc diagram dataset with resource annotations.

Can the paper honestly claim real lambeq parser evidence? No. It may claim lambeq imported and LinearReader graph-only sidecar extraction ran, but not parser-generated lambeq/QDisCoCirc resource evidence.
