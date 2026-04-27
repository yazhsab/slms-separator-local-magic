"""ZX-calculus simulation baseline using pyzx.

Each StructuredInstance is converted to a synthetic Clifford+T circuit on
``len(graph.nodes)`` qubits whose graph structure mirrors the instance:
- one qubit per bag,
- a T gate placed on the qubit at every resource bag,
- a CZ entangler between every parent-child edge.

This is NOT the original quantum circuit the instance came from; the
StructuredInstance is graph+resource metadata, not a runnable circuit.  The
ZX exponent we report is therefore a *consistent synthetic comparator*:
the same graph structure and resource set are used as in SLMS, so we
compare the resulting T-count and stabilizer-rank bound to SLMS's
``w_eff + 2*Lambda_msg`` exponent.

What we compute:
- ``zx_t_count_initial``: T-count of the synthetic circuit.
- ``zx_t_count_reduced``: T-count after ``pyzx.simplify.full_reduce``.
- ``zx_alpha_bg``: the 0.396 Bravyi-Gosset stabilizer-rank exponent constant.
- ``zx_exponent_proxy``: ``alpha_bg * zx_t_count_reduced``, the Bravyi-Gosset
  stabilizer-rank cost exponent for the reduced ZX-diagram.

Reference:
- Bravyi, S. and Gosset, D., "Improved Classical Simulation of Quantum
  Circuits Dominated by Clifford Gates", PRL 116, 250501 (2016).
- Kissinger, A. and van de Wetering, J., pyzx
  (https://github.com/Quantomatic/pyzx).

Limitations explicitly recorded:
- The instances are abstract; the synthetic Clifford+T encoding is one of many
  possible reductions of a graph+resource specification to a runnable circuit.
- ``full_reduce`` does NOT achieve optimal T-count reduction; for that one would
  need cutting/partitioning routines (Sutcliffe-Kissinger 2024-2025), which we
  do not invoke here.
- This is a per-instance EXPONENT comparator, not a wall-clock benchmark of
  pyzx vs SLMS.
"""

from __future__ import annotations

from math import log

import networkx as nx

try:
    import pyzx as zx
    PYZX_AVAILABLE = True
except Exception as exc:
    zx = None
    PYZX_AVAILABLE = False
    PYZX_ERROR = f"{type(exc).__name__}: {exc}"


ALPHA_BG = 0.396  # Bravyi-Gosset stabilizer rank exponent for T magic states.


def instance_to_synthetic_circuit(instance) -> "tuple[zx.Circuit, dict] | None":
    """Build a synthetic Clifford+T circuit reflecting the instance graph+resources."""
    if not PYZX_AVAILABLE:
        return None
    nodes = list(instance.graph.nodes)
    n = len(nodes)
    if n == 0:
        return None
    idx = {v: i for i, v in enumerate(nodes)}
    c = zx.Circuit(n)
    # Initial layer: H on all qubits (so T sees a non-trivial input).
    for i in range(n):
        c.add_gate("HAD", i)
    # T at resource bags.
    t_count = 0
    for v, is_res in instance.resource.items():
        if is_res:
            c.add_gate("T", idx[v])
            t_count += 1
    # CZ across every edge.
    for u, v in instance.graph.edges:
        c.add_gate("CZ", idx[u], idx[v])
    # Final H layer for symmetry.
    for i in range(n):
        c.add_gate("HAD", i)
    return c, {"t_count_initial": t_count}


def reduce_and_count(c) -> dict:
    """Run pyzx.full_reduce and return T-count before and after."""
    g = c.to_graph()
    t_initial = sum(1 for v in g.vertices() if g.phase(v) % 1 == 0.25 or g.phase(v) % 1 == 0.75)
    try:
        zx.simplify.full_reduce(g, quiet=True)
    except Exception as exc:
        return {
            "t_count_initial": t_initial,
            "t_count_reduced": t_initial,
            "reduction_status": f"failed: {type(exc).__name__}: {exc}",
        }
    t_reduced = sum(1 for v in g.vertices() if g.phase(v) % 1 == 0.25 or g.phase(v) % 1 == 0.75)
    return {
        "t_count_initial": t_initial,
        "t_count_reduced": t_reduced,
        "reduction_status": "ok",
    }


def zx_exponent(instance) -> dict:
    """Compute ZX simulation exponent proxy for an instance."""
    if not PYZX_AVAILABLE:
        return {
            "zx_status": "pyzx_unavailable",
            "zx_error": PYZX_ERROR,
            "zx_t_count_initial": None,
            "zx_t_count_reduced": None,
            "zx_alpha_bg": ALPHA_BG,
            "zx_exponent_proxy": None,
        }
    out = instance_to_synthetic_circuit(instance)
    if out is None:
        return {
            "zx_status": "empty_instance",
            "zx_t_count_initial": 0,
            "zx_t_count_reduced": 0,
            "zx_alpha_bg": ALPHA_BG,
            "zx_exponent_proxy": 0.0,
        }
    c, meta = out
    counts = reduce_and_count(c)
    expo = ALPHA_BG * counts["t_count_reduced"] * log(2)
    # NOTE: the Codsi-Laakkonen / pyzx exponent is naturally written 2^{alpha*T},
    # i.e. base-2.  We convert to natural log so it can be compared to
    # `w_eff + 2*Lambda_msg` (which is also natural log).
    return {
        "zx_status": counts["reduction_status"],
        "zx_t_count_initial": counts["t_count_initial"],
        "zx_t_count_reduced": counts["t_count_reduced"],
        "zx_alpha_bg": ALPHA_BG,
        "zx_exponent_proxy": expo,
    }
