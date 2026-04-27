from __future__ import annotations

from pathlib import Path

from real_lambeq_pipeline import attempt_real_lambeq


def try_real_lambeq(sentences: list[str], results_dir: Path | None = None) -> tuple[list, dict]:
    """Attempt real lambeq parsing and record exact failures.

    The repository does not vendor lambeq or parser models. If lambeq is
    unavailable, parser initialization fails, or parsing fails, this returns an
    empty instance list and writes a failure report instead of fabricating data.
    """

    return attempt_real_lambeq(sentences, results_dir) if results_dir is not None else attempt_real_lambeq(sentences)
