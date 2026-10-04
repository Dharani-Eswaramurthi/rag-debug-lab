# Why the heading mattered

The source says Studio allows 50 projects. The broken output selects the Basic paragraph allowing 5. That is not an LLM hallucination in this exercise: no LLM is used. It is incorrect evidence selection before generation would start.

## Reproduce both versions

```sh
python lab.py --baseline --trace --check
python lab.py --reference --trace --check
```

The first intentionally exits 1 with 2/6 checks. The second exits 0 with 6/6. Those are fixture results, not measured production accuracy improvements.

## Trace the cause

1. The source associates paragraphs with workspace headings.
2. The naive splitter discards those headings.
3. The scorer sees indistinguishable query-word overlap for the three project paragraphs.
4. Stable sorting selects the first paragraph: Basic.

The reference keeps parent and section headings in `Chunk.heading`. Crucially, the scoring function already includes this field in the searched text. The matching workspace now contributes an extra relevant token, breaking the tie for these queries. Storing metadata without consulting it would not help.

Read [reference.py](reference.py), then implement your own version in [chunking.py](chunking.py). Try changing the workspace names and reordering sections: a general fix should not depend on names or file order.

## What did we not fix?

The retriever can still return the wrong passage for unknown workspaces, synonyms, ambiguous requests, and conflicting statements. It does not validate authority or access permissions. A heading can also be wrong. Correct evidence does not guarantee a model will use it correctly.

Real projects may use heading-aware splitting, metadata filtering, hybrid retrieval, reranking, and answer-grounding checks. Select and evaluate techniques against your own queries; this exercise does not establish which configuration wins in your system.

For a real library example, see LangChain's [MarkdownHeaderTextSplitter reference](https://reference.langchain.com/python/langchain-text-splitters/markdown/MarkdownHeaderTextSplitter). The implementation and fictional data here are original, small teaching examples, not copied library code.

## Check your understanding

- Why would merely increasing the number of retrieved chunks not necessarily identify the correct workspace?
- Why is `6/6` not evidence that unknown-workspace queries are safe?
- If an assistant generated your fix, can you explain where it flushes paragraphs and resets heading scope?

Before closing the terminal, use the feedback instructions in [README.md](README.md). Saying you only read the solution is useful too; this is not an exam.
