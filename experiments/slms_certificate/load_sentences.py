from __future__ import annotations

from pathlib import Path


def load_sentences(path: Path, max_sentences: int) -> list[str]:
    if not path.exists():
        return []
    sentences: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text and not text.startswith("#"):
            sentences.append(text)
        if len(sentences) >= max_sentences:
            break
    return sentences
