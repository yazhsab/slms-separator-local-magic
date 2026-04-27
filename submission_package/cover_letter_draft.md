# Cover Letter Draft

Dear Editors,

We submit the manuscript "Separator-Local Treewidth--Magic Simulation of Compositional Quantum Language Circuits" for consideration in *Quantum*.

The paper is a quantum information and classical simulation contribution. It introduces an explicit separator-local message burden for tensor-network/circuit families with both stabilizer structure and localized non-stabilizer resources. For locally marginalizable resource-decomposition networks, we prove a randomized additive simulation theorem whose cost is controlled by stabilizer-compressed effective width and a message-local free-tensor quasiprobability `l1` burden, computed by an explicit active-child recurrence.

The work is positioned against dense treewidth simulation, focused tree-width and focused rank-width simulation (Codsi--Laakkonen 2026), low-rank-width ZX simulation (Kuyanov--Kissinger 2026), and stabilizer-tensor-network simulation (Masot-Llima--Garc\'ia-S\'aez 2024; Nakhl et al.\ 2025). It includes a stabilizer-compressed parameter separation from dense treewidth bounds, separations from naive global quasiprobability burden, a restricted certified grammar-tree / lambeq-style instantiation, and an executable artifact that computes Codsi--Laakkonen focused tree-width and focused rank-width per Definitions 13 and 14 (exact for small instances, honest upper bound otherwise), a pyzx `full_reduce` + Bravyi--Gosset ZX exponent baseline, and a tableau plus Bravyi--Gosset STN-style upper bound, all with per-instance wall-clock timings on 120 fallback structured instances.

On those instances the SLMS exponent `w_eff + 2*Lambda_msg` is strictly smaller than the Codsi--Laakkonen Theorem 8 exponent on 105/120 instances, smaller than the pyzx + Bravyi--Gosset baseline on 66/120, and smaller than the STN-style upper bound on 70/120. We report these as exponent-bound diagnostics on a fixed synthetic encoding; we do not claim a strict separation theorem and we do not claim wall-clock dominance over the published algorithms in those references.

The manuscript does not claim quantum advantage. It does not claim coverage of arbitrary QDisCoCirc or trained lambeq circuits. The dense-width and global-magic separation results are parameter comparisons between certified upper bounds, not lower bounds against any classical algorithm. Parser-level lambeq extraction was not available in our run environment because lambeq 0.5.0's hardcoded Bobcat model URL on `qnlp.cambridgequantum.com` is now NXDOMAIN; this is recorded as open lambeq GitHub issues #253, #254, and #257 and is documented faithfully in Section 8 and Section 9 of the manuscript. We therefore report the artifact's nontrivial certificate evidence on 120 lambeq-compatible fallback structured instances and 120 lambeq LinearReader graph-only sidecar instances; we do not claim parser-generated QNLP coverage. The repository contains the manuscript, executable certificate code, scripts, generated CSVs, plots, and a worked appendix; it does not yet include a full SLMS simulator backend on real QNLP circuits.

Sincerely,

Prabakaran Kannan (corresponding author, cs23d2005@nitpy.ac.in), Venkatesan M. Sundaram (NIT Puducherry), and Prabhavathy P. (VIT Vellore)
