# Citation Audit

This audit checks manuscript citations against `refs.bib`. Entries marked `VERIFIED` were checked against publisher, arXiv, PubMed, dblp, or institutional pages during this pass. Any later unresolved entries must be marked `VERIFY`.

## Used Citations

| Key | Used in manuscript? | Status | Notes |
|---|---:|---|---|
| `AaronsonGottesman2004` | yes | VERIFIED | Physical Review A 70, 052328 (2004), DOI `10.1103/PhysRevA.70.052328`; publisher page confirms title and metadata. |
| `MarkovShi2008` | yes | VERIFIED | SIAM Journal on Computing 38(3), 963--981 (2008), DOI `10.1137/050644756`; checked against SIAM/CiNii metadata. |
| `Vidal2003` | yes | VERIFIED | Physical Review Letters 91, 147902 (2003), DOI `10.1103/PhysRevLett.91.147902`; APS and PubMed metadata confirm. |
| `Schollwoeck2011` | yes | VERIFIED | Annals of Physics 326(1), 96--192 (2011), DOI `10.1016/j.aop.2010.09.012`; ScienceDirect/CiNii metadata confirm. |
| `TindallEtAl2024` | yes | VERIFIED | PRX Quantum 5, 010308 (2024), DOI `10.1103/PRXQuantum.5.010308`; APS page confirms title, authors, journal, and publication date. |
| `CodsiLaakkonen2026` | yes | VERIFIED | arXiv `2603.06377`; public arXiv-index pages confirm title, authors, and abstract. |
| `KuyanovKissinger2026` | yes | VERIFIED | arXiv `2603.06764`; ZX-calculus publication page and arXiv-index pages confirm title, authors, and abstract. |
| `Sutcliffe2024KPartition` | yes | VERIFIED | arXiv `2409.00828`; ZX-calculus publication page and public preprint metadata confirm title and author. |
| `SutcliffeKissinger2024Cutting` | yes | VERIFIED | EPTCS 406, 63--78 (2024), DOI `10.4204/EPTCS.406.3`; ZX-calculus publication metadata confirm. |
| `SutcliffeKissinger2025Parametric` | yes | VERIFIED | EPTCS 426, 247--269 (2025), DOI `10.4204/EPTCS.426.10`; dblp/EPTCS metadata confirm. |
| `MasotLlimaGarciaSaez2024` | yes | VERIFIED | Physical Review Letters 133, 230601 (2024), DOI `10.1103/PhysRevLett.133.230601`; APS/PubMed metadata confirm. |
| `NakhlEtAl2025` | yes | VERIFIED | Physical Review Letters 134, 190602 (2025), DOI `10.1103/PhysRevLett.134.190602`; APS metadata confirm. |
| `PashayanWallmanBartlett2015` | yes | VERIFIED | Physical Review Letters 115, 070501 (2015), DOI `10.1103/PhysRevLett.115.070501`; APS page confirms. |
| `BravyiGosset2016` | yes | VERIFIED | Physical Review Letters 116, 250501 (2016), DOI `10.1103/PhysRevLett.116.250501`; PubMed/APS metadata confirm. |
| `BravyiEtAl2019` | yes | VERIFIED | Quantum 3, 181 (2019), DOI `10.22331/q-2019-09-02-181`; publisher/IBM metadata confirm. |
| `HowardCampbell2017` | yes | VERIFIED | Physical Review Letters 118, 090501 (2017), DOI `10.1103/PhysRevLett.118.090501`; APS page confirms. |
| `SeddonEtAl2021` | yes | VERIFIED | PRX Quantum 2, 010345 (2021), DOI `10.1103/PRXQuantum.2.010345`; APS page confirms. |
| `LeoneOlivieroHamma2022` | yes | VERIFIED | Physical Review Letters 128, 050402 (2022), DOI `10.1103/PhysRevLett.128.050402`; APS page confirms. |
| `HaugPiroli2023` | yes | VERIFIED | Quantum 7, 1092 (2023), DOI `10.22331/q-2023-08-28-1092`; public metadata confirm. |
| `LeoneBittel2024` | yes | VERIFIED | Physical Review A 110, L040403 (2024), DOI `10.1103/PhysRevA.110.L040403`; APS page confirms. |
| `CoeckeSadrzadehClark2010` | yes | VERIFIED | Linguistic Analysis 36(1--4), 345--384 (2010), arXiv `1003.4394`; public metadata confirm. |
| `ZengCoecke2016` | yes | VERIFIED | EPTCS 221, 67--75 (2016), DOI `10.4204/EPTCS.221.8`; public metadata confirm. |
| `MeichanetzidisEtAl2020` | yes | VERIFIED | EPTCS 340, 213--229, DOI `10.4204/EPTCS.340.11`; arXiv `2005.04147`; public metadata confirm. |
| `KartsaklisEtAl2021` | yes | VERIFIED | arXiv `2110.04236`; public arXiv-index pages confirm title/authors. Check whether final proceedings metadata is preferable before submission. |
| `LaakkonenMeichanetzidisCoecke2024` | yes | VERIFIED | EPTCS 406, 162--196 (2024), DOI `10.4204/EPTCS.406.8`; arXiv `2408.06061`; checked against dblp/EPTCS-indexed metadata. |
| `HarveyYeungMeichanetzidis2025` | yes | VERIFIED | Scientific Reports 15, article 7155 (2025), DOI `10.1038/s41598-024-84295-2`; Nature/PubMed metadata confirm. |
| `Tang2019` | yes | VERIFIED | STOC 2019, pages 217--228, DOI `10.1145/3313276.3316310`; standard ACM metadata. |
| `ChiaEtAl2020` | yes | VERIFIED | Journal of the ACM 69(5), 1--72 (2022), DOI `10.1145/3549524`; arXiv `1910.06151`; checked against ACM-indexed metadata. |
| `Tang2022` | yes | VERIFIED | Nature Reviews Physics 4, 692--693 (2022), DOI `10.1038/s42254-022-00511-w`; Nature page confirms. |
| `ShinTeoJeong2024` | yes | VERIFIED | Physical Review Research 6, 023218 (2024), DOI `10.1103/PhysRevResearch.6.023218`; APS page confirms. |

## Unused Entries In `refs.bib`

No unused entries remain after this pass.

## Missing Or Added Core Citations

- Added `AaronsonGottesman2004` for tableau/stabilizer simulation.
- Added `Vidal2003` and `Schollwoeck2011` for MPS/bond-dimension simulation comparators.
- Added `TindallEtAl2024` for modern tensor-network simulation practice and approximate contraction comparators.
- Added `CodsiLaakkonen2026` and `KuyanovKissinger2026` for focused tree-width/focused rank-width and low-rank-width ZX simulation comparators.
- Added Sutcliffe/Kissinger ZX cutting, partitioning, and parametric rewriting references.
- Added stabilizer tensor-network references `MasotLlimaGarciaSaez2024` and `NakhlEtAl2025`.
- No citation to Gottesman's thesis is strictly necessary because the manuscript cites Aaronson--Gottesman for the simulation data structure.
- Current QNLP citations cover DisCoCat, early QNLP algorithms, near-term QNLP, lambeq, QDisCoCirc, and sequence-processing tensor networks.

## Sources Checked

- APS pages for Aaronson--Gottesman, Pashayan--Wallman--Bartlett, Howard--Campbell, Seddon et al., Leone--Oliviero--Hamma, Leone--Bittel, and Shin--Teo--Jeong.
- APS pages for Vidal 2003 and Tindall--Fishman--Stoudenmire--Sels 2024.
- APS pages for Masot-Llima--Garcia-Saez 2024 and Nakhl et al. 2025.
- arXiv-index and ZX-calculus publication pages for Codsi--Laakkonen 2026, Kuyanov--Kissinger 2026, and Sutcliffe/Kissinger ZX simulation references.
- ScienceDirect/CiNii metadata for Schollwoeck 2011.
- SIAM/CiNii metadata for Markov--Shi.
- Nature/PubMed metadata for Harvey--Yeung--Meichanetzidis and Tang 2022.
- arXiv-index, dblp, and proceedings metadata pages for QNLP references where available.
- ACM-indexed metadata for Chia et al. final journal version.
