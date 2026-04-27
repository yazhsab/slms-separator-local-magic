#!/usr/bin/env python3
"""Compatibility wrapper for compute_synthetic_burdens.py."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).with_name("compute_synthetic_burdens.py")
    runpy.run_path(str(target), run_name="__main__")
