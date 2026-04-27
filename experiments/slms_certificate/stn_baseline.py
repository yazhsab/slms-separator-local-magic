"""STN-style baseline: tableau + Bravyi-Gosset stabilizer rank.

The exact algorithms of Masot-Llima & Garcia-Saez (PRL 133, 230601, 2024) and
Nakhl et al. (PRL 134, 190602, 2025) are not implemented here.  Both of those
papers introduce non-trivial tensor-network architectures over a stabilizer
basis with magic-state injection, and a faithful re-implementation would
require careful coding of their tableau-update and bond-dimension rules.

What we compute is an STN-inspired *upper-bound proxy* for the synthetic
Clifford+T circuit attached to each instance:

    STN_exponent_proxy  =  alpha_bg * T_count + w_eff_extra

where T_count is the number of resource (non-Clifford) bags in the instance,
``alpha_bg = 0.396`` is the Bravyi-Gosset stabilizer rank exponent constant
for T magic states, and ``w_eff_extra`` reflects the non-Clifford bond
dimension that must be tracked when the resource bags are coupled to the
Clifford backbone.  We use ``w_eff_extra = log(max(1, n_resource_bags_active))``
as a conservative upper bound on the bond dimension, where active resource
bags are those that the SLMS certificate marks as active.

This is a comparator-grade proxy, NOT a re-implementation of the
Masot-Llima or Nakhl algorithms.  Use it to ask "is SLMS's certified
exponent below this simple stabilizer-rank-inspired comparator for the same
Clifford+T encoding?"  An honest empirical comparison against the actual
published algorithms requires an implementation of those algorithms, which is
out of scope here.
"""

from __future__ import annotations

from math import log


ALPHA_BG = 0.396  # Bravyi-Gosset stabilizer rank exponent for T magic states.


def stn_exponent(instance) -> dict:
    """STN-style exponent upper bound.

    Returns a natural-log exponent comparable to the SLMS bound
    ``w_eff + 2*Lambda_msg``.
    """
    n_resource_bags = sum(1 for flag in instance.resource.values() if flag)
    n_active = 0
    for parent, children in instance.children.items():
        for child in children:
            if instance.active_edge.get((parent, child), False):
                # Count the resource bags in the child's subtree.
                stack = [child]
                seen = set()
                while stack:
                    v = stack.pop()
                    if v in seen:
                        continue
                    seen.add(v)
                    if instance.resource.get(v, False):
                        n_active += 1
                    stack.extend(instance.children.get(v, []))
    bond_extra = log(max(1, n_active))  # bond dim contribution from active resources
    expo = ALPHA_BG * n_resource_bags * log(2) + bond_extra
    return {
        "stn_status": "upper_bound_only",
        "stn_method_label": "tableau+Bravyi-Gosset upper bound (NOT Masot-Llima or Nakhl algorithm)",
        "stn_t_count": n_resource_bags,
        "stn_active_resource_bags": n_active,
        "stn_alpha_bg": ALPHA_BG,
        "stn_bond_extra_log": bond_extra,
        "stn_exponent_proxy": expo,
    }
