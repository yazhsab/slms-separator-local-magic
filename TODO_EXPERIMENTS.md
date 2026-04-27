# Experiment TODOs Not Completed From Current Source Package

- [ ] Extract real lambeq sentence circuits with recorded parser, rewrite rules, ansatz, and simplification settings.
- [ ] Extract at least one QDisCoCirc-style discourse circuit with documented entity/discourse update structure.
- [ ] Export full SLMS certificates for real instances: tree decomposition `T`, dense width `w_TN`, effective width `w_eff`, local costs `xi_b`, local norm factors `kappa_b`, active-child sets `Act(b)`, `Lambda_glob`, and `Lambda_msg`.
- [ ] Run dense tensor-network contraction baselines with recorded contraction orders and memory estimates.
- [ ] Run global quasiprobability or stabilizer-decomposition baselines using the same local resource dictionary.
- [ ] Compute focused tree-width and focused rank-width when public implementations or reproducible heuristics are available.
- [ ] Run low-rank-width ZX or ZX partitioning/cutting baselines for compatible Clifford+T or graph-like ZX instances.
- [ ] Run stabilizer tensor-network and magic-state-injection stabilizer tensor-network baselines if implementations are available.
- [ ] Replace synthetic width proxies in the current benchmark table with computed treewidth/rank-width/focused-width values where feasible.
- [ ] Measure actual runtime, memory, estimator variance, and confidence intervals rather than only exponent proxies.
- [ ] Report failure cases where local marginalizability cannot be certified.
