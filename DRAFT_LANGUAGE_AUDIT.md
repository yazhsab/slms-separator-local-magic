# Draft / Version Language Audit

## Search Scope

Checked:

- `main.tex`
- `sections/*.tex`
- `appendices/*.tex`
- `macros.tex`

## Removed Or Fixed

| Occurrence | Location | Action |
|---|---|---|
| `Anonymous` author placeholder | `main.tex` | Replaced with named author and affiliation metadata supplied in the source. |
| `\TODO` macro | `macros.tex` | Removed because it was unused and looked like draft infrastructure. |
| `future experiments` | `appendices/D_qnlp_graph_extraction.tex` | Replaced by `follow-up experiments`. |
| `future implementation` | `appendices/F_certification_algorithms.tex`, `sections/08_benchmarks.tex` | Replaced by implementation-neutral wording. |

## Clean Search Terms

No manuscript-body occurrences remain for:

- `draft`
- `v0.1`, `v0.2`, `v0.3`, `v0.4`, `v0.5`, `v0.6`, `v0`
- `scaffold`
- `proof target`
- `future version`
- `current version`
- `there should exist`
- `should`
- `future`
- `we expect`
- `intended`
- `missing proof`
- `to be completed`
- `TODO`

## Qualified Negative Claims

The manuscript still contains `quantum advantage`, `legal`, and `speedup` only in conservative or related-work contexts:

- it explicitly denies unconditional quantum-advantage claims;
- legal corpora are described only as graph-structure stress tests;
- speedup language appears in dequantization/prior-work discussion, not as a claimed result of this paper.
