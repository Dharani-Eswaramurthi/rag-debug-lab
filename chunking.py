"""Edit this file. Preserve paragraph bodies and their qualifying context."""

from engine import Chunk, naive_chunks


def make_chunks(markdown: str) -> list[Chunk]:
    # TODO: Replace this baseline. Chunk.heading is included in retrieval scoring.
    # Use the actual document structure, not workspace names or expected answers.
    return naive_chunks(markdown)
