# Gap 1: Parser-Level lambeq Extraction — Upstream Block

## Status

**Cannot be resolved in this session.** All three parser paths in lambeq 0.5.0 (latest pip release) fail with errors that have no current upstream fix.

## Concrete failure modes (verified 2026-04-26)

### BobcatParser
- Hardcoded model URL: `https://qnlp.cambridgequantum.com/models/bobcat/latest/version.txt`
  (verified in `/tmp/slms_lambeq_py311/lib/python3.11/site-packages/lambeq/text2diagram/model_based_reader/model_downloader.py` line 41:
  `MODELS_URL = 'https://qnlp.cambridgequantum.com/models'`)
- `nslookup qnlp.cambridgequantum.com` returns **NXDOMAIN**. Cambridge Quantum was acquired by Quantinuum in 2021; the domain is retired.
- `qnlp.quantinuum.com/models/bobcat/latest/version.txt` returns HTTP 404; `qnlp.quantinuum.com/models/` returns HTTP 403.
- The Bobcat model is **not** mirrored on Hugging Face (searched 2026-04-26: 0 results for "lambeq", "ccg-parser", "discocat"; the 10 "bobcat" hits are unrelated Qwen-Swarm naming).
- Wayback Machine has **no archived snapshot** of the Bobcat model files (`archive.org/wayback/available` returned `{archived_snapshots: {}}` for the version.txt and model.tar.gz URLs).
- This is a known, **open upstream issue** in the Quantinuum/lambeq GitHub repository:
  - Issue [#253](https://github.com/CQCL/lambeq/issues/253) "Unable to reach URL https://qnlp.cambridgequantum.com/" (opened 2025-12-02)
  - Issue [#254](https://github.com/CQCL/lambeq/issues/254) "BobcatParser fails: ModelDownloaderError" (opened 2025-12-03)
  - Issue [#257](https://github.com/CQCL/lambeq/issues/257) "BobcatParser model download fails due to unreachable qnlp.cambridgequantum.com (DNS resolution error)" (opened 2026-02-14)
  - All three issues are still **open** as of 2026-04-26.

### DepCCGParser
- Requires the `depccg` PyPI package, which is no longer maintained.
- `pip install depccg` fails: `depccg`'s build chain pulls `spacy` whose setup script imports `distutils.msvccompiler`, which was removed from setuptools >=72.
- Per the lambeq 0.5.0 documentation, "DepCCG-related functionality is no longer actively supported in lambeq, and may not work as expected."

### WebParser
- Calls `https://api.qnlp.cambridgequantum.com/...` (or similar). The service returns empty JSON, causing
  `requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.
- This is the failure recorded in the current `results/real_lambeq_parse_log.txt`.

### PregroupTreeParser
- Does not exist in lambeq 0.5.0 (`ImportError: cannot import name 'PregroupTreeParser' from 'lambeq'`).

## What the artifact actually has

`lambeq.cups_reader` (a LinearReader) does work and produces 120 real lambeq-generated diagrams from the
sample sentences. These are real lambeq output, but they are **not** CCG-parsed; they are linear cup/cap
structures derived directly from sentence token sequences, with no grammatical category information.

## Implication for the paper

Sections 8.3 and 9.4 must continue to label the cups_reader output as **non-parser lambeq diagrams**
(plumbing/import evidence) and add an explicit pointer to the upstream blockers above. Parser-level QNLP
coverage on real CCG-parsed lambeq circuits is not currently obtainable from any pip-installable
lambeq release; this is an external dependency status, not a property of the SLMS framework or the
manuscript's claims.
