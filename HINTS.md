# Hints — open one at a time

<details>
<summary>Hint 1: inspect the input to retrieval</summary>

Read the original document, then run `python lab.py --trace`. Does each chunk still tell you which workspace it describes?

</details>

<details>
<summary>Hint 2: follow the tie</summary>

The scorer counts shared words. Without the headings, the three project paragraphs share the same question words. Document order breaks ties. Adding more random prompt instructions would not restore the missing qualifier.

</details>

<details>
<summary>Hint 3: use the existing interface</summary>

`Chunk` has both `text` and `heading`. Ranking searches both, but the selected passage is still `text`. Track the active heading while reading the document. Put it on each paragraph chunk. Do not add the heading to `text`, because the checks compare unchanged paragraph bodies.

</details>

<details>
<summary>Hint 4: avoid carrying the wrong scope forward</summary>

Flush a paragraph before changing headings. When a new heading arrives, remove earlier headings at its own level and deeper levels. Otherwise the next workspace can inherit the previous workspace's context. The reference also retains parent headings.

</details>
