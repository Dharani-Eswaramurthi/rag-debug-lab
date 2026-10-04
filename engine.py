"""Small deterministic retrieval harness. No model, network, or telemetry."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Chunk:
    text: str
    heading: str = ""


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def naive_chunks(markdown: str) -> list[Chunk]:
    """Known-broken baseline: removes the scope carried by headings."""
    paragraphs: list[Chunk] = []
    lines: list[str] = []
    for line in markdown.splitlines() + [""]:
        if not line.strip() or line.lstrip().startswith("#"):
            if lines:
                paragraphs.append(Chunk(" ".join(lines)))
                lines = []
        else:
            lines.append(line.strip())
    return paragraphs


def rank(question: str, chunks: list[Chunk]) -> list[tuple[int, Chunk]]:
    query = tokens(question)
    scored = [(len(query & tokens(chunk.heading + " " + chunk.text)), chunk)
              for chunk in chunks]
    # Stable sorting makes ties follow original document order.
    return sorted(scored, key=lambda item: item[0], reverse=True)


def retrieve(question: str, chunks: list[Chunk]) -> str:
    ranked = rank(question, chunks)
    return ranked[0][1].text if ranked and ranked[0][0] > 0 else "NO MATCH"
