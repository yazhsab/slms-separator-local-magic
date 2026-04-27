from __future__ import annotations

import math
import sys
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from baselines import dense_width_proxy, exponent_proxies
from certify_slms import certify_instance
from fallback_structured_instances import generate_instances


CONFIG = {
    "seed": 11,
    "fallback": {
        "num_instances": 16,
        "min_depth": 3,
        "max_depth": 3,
        "xi_resource": 1.30,
        "xi_path": 1.18,
        "kappa_default": 1.0,
        "modes": [
            "leaf_local",
            "path_active",
            "chain_active",
            "clustered",
            "grid_stabilizer_compressed",
            "dense_like_active",
            "local_failure",
            "mixed",
        ],
    },
}


def _by_mode(mode: str):
    return next(instance for instance in generate_instances(CONFIG) if instance.mode == mode)


def test_all_children_active_matches_global_behavior():
    row = certify_instance(_by_mode("chain_active"))
    assert math.isclose(row["Lambda_msg"], row["Lambda_glob"], rel_tol=1e-9, abs_tol=1e-9)
    assert row["certificate_pass"] is True


def test_leaf_resources_remain_separator_local():
    row = certify_instance(_by_mode("leaf_local"))
    assert row["Lambda_msg"] < row["Lambda_glob"]
    assert row["certificate_pass"] is True


def test_local_marginalization_failure_is_rejected():
    row = certify_instance(_by_mode("local_failure"))
    assert row["certificate_pass"] is False
    assert "local_marginalization" in row["failure_reason"]


def test_burdens_are_finite_and_nonnegative():
    for instance in generate_instances(CONFIG):
        row = certify_instance(instance)
        assert math.isfinite(row["Lambda_msg"])
        assert math.isfinite(row["Lambda_glob"])
        assert row["Lambda_msg"] >= 0.0
        assert row["Lambda_glob"] >= 0.0


def test_slms_exponent_uses_two_lambda_msg():
    instance = _by_mode("path_active")
    row = certify_instance(instance)
    proxies = exponent_proxies(row, dense_width_proxy(instance.graph))
    assert math.isclose(
        proxies["exponent_slms"],
        row["w_eff_proxy"] + 2.0 * row["Lambda_msg"],
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
