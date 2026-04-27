# Final Claim Audit

Audit date: 2026-04-26.

## Risky Phrases and Replacements

| Risky phrase | Replacement / current wording | Reason |
|---|---|---|
| `ZX baseline` | `ZX-inspired diagnostic`, `pyzx full_reduce + Bravyi--Gosset diagnostic` | Exact Sutcliffe--Kissinger ZX cutting/k-partitioning is not implemented. |
| `STN baseline` | `STN-style upper-bound proxy` | Exact Masot-Llima / Nakhl STN or MAST algorithms are not implemented. |
| `real lambeq evidence` | `lambeq LinearReader graph-only sidecar evidence` or `fallback lambeq-compatible structured evidence` | No parser-generated lambeq resource instances exist. |
| `general QNLP coverage` | `restricted QNLP-motivated structured families` | The theorem applies only to locally marginalizable resource-decomposition networks. |
| `beats focused tree-width / ZX / STN` | `SLMS exponent is smaller than the implemented diagnostic on the reported fallback instances` | Only proxy/diagnostic comparisons are reported; no dominance theorem exists. |
| `hardness` for certificate failure | `failure of this sufficient certificate` | Certificate failure does not imply classical hardness. |
| `simulator` where only an exponent is reported | `certificate framework`, `estimator`, or `diagnostic` | Many reported rows are parameter diagnostics, not full simulator implementations. |
| `AI/NLP contribution` | `quantum simulation / quantum tensor-network result motivated by compositional quantum-language circuits` | SciPost Physics Core scope is quantum physics / mathematical physics / computational physics. |

## Final Search Notes

Remaining uses of `hardness` occur in explicit limitations, QDisCoCirc related-work context, or statements that failure is not hardness. Remaining uses of `simulator` refer either to cited simulator families, actual simulation methods, or explicit non-dominance statements. Remaining uses of legal/AI language are negative-scope statements or possible graph stress-test descriptions, not claimed applications.

## Final Claim Status

- No quantum advantage claim remains.
- No generic parser-level lambeq/QDisCoCirc coverage claim remains.
- No exact Sutcliffe--Kissinger or exact STN/MAST implementation claim remains.
- No dominance claim over focused-width, ZX, stabilizer-rank, or STN methods remains.
- Fallback data is labelled as fallback structured evidence.
- lambeq LinearReader data is labelled graph-only sidecar evidence.
