"""Spoiler: heading-aware splitting for the restricted fixture format."""

import re
from engine import Chunk


def make_chunks(markdown: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    headings: dict[int, str] = {}
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            context = " > ".join(headings[level] for level in sorted(headings))
            chunks.append(Chunk(" ".join(paragraph), context))
            paragraph.clear()

    for line in markdown.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            flush()  # Flush under the OLD heading, then change the scope.
            level = len(heading.group(1))
            for previous in list(headings):
                if previous >= level:
                    del headings[previous]
            headings[level] = heading.group(2)
        elif not line.strip():
            flush()
        else:
            paragraph.append(line.strip())
    flush()
    return chunks
