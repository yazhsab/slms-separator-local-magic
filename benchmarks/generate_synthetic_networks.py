#!/usr/bin/env python3
"""Compatibility wrapper for generate_tree_resource_network.py."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).with_name("generate_tree_resource_network.py")
    runpy.run_path(str(target), run_name="__main__")
