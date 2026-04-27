# Referee Prebuttal

## "This is just Markov--Shi plus magic."

Markov--Shi controls dense tensor-network contraction by dense width. This paper studies networks with stabilizer/free structure and introduces a stabilizer-compressed effective width. The dense-grid example shows that dense treewidth and stabilizer-compressed width can separate.
The comparison is between simulation parameters and upper bounds: the paper does not claim a lower bound against all classical algorithms.

## "This is just Gottesman--Knill plus local sampling."

Pure stabilizer networks are already easy, and global quasiprobability sampling already handles local magic with global product overhead. The new theorem is the certified message recurrence proving that locally marginalized resource labels do not multiply into all ancestor separators.

## "The graph-state example is already stabilizer-simulable."

Correct. That is the point of the parameter separation. Dense treewidth sees a high-width grid, while a stabilizer-aware representation compresses the free core. The theorem does not claim a lower bound against stabilizer-aware algorithms.

## "The QNLP family is too restricted."

The restricted family is intentional. It supplies one checkable grammar-tree class satisfying local marginalizability. The paper explicitly does not claim arbitrary lambeq or QDisCoCirc circuits satisfy the theorem.

## "The theorem uses certificates; are they checkable?"

The manuscript gives sufficient certification algorithms for free-region detection, effective-width upper bounds, active-child selection, and local `1 -> 1` norm checks. These are conservative; failure of a certificate makes the theorem inapplicable or marks a child active.
Currently, the manuscript supplies the algorithms and synthetic accounting scripts. A full stabilizer/tensor backend implementation remains outside the present package.

## "Where are the experiments?"

The repository includes synthetic accounting scripts and outputs, not full runtime experiments. The paper frames them as bookkeeping diagnostics only. A full simulator backend remains open work.

## "Does this imply quantum advantage?"

No. The result is a classical simulation theorem and parameter framework. It identifies easy regimes and compares simulation upper bounds.
