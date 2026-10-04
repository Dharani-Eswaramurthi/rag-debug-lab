# RAG Debug Lab: the missing heading

Your document contains the right answer. Your retrieval code still selects the wrong one. Can you find where the context disappeared?

A free, small Python exercise for people who have built a first document chatbot. It isolates **one retrieval failure**: splitting paragraphs away from their headings. Designed for about 15–20 minutes; that timing has not yet been tested with learners.

**Python 3.10+ · standard library only · no API keys · no signup · no telemetry**

This is a deterministic teaching simulation, **not a complete RAG chatbot**. It uses word overlap instead of embeddings and prints a retrieved passage instead of calling an LLM. All company names, documents, and questions are fictional. Passing its tests is not proof that a production chatbot is reliable.

## Start here

On the GitHub repository page, choose **Code → Download ZIP**, extract it, and open a terminal inside the extracted folder. Cloning works too. **You do not need to fork or star the repository.**

Run:

```sh
python lab.py
python lab.py --trace
python lab.py --check
```

On Windows, try `py` if `python` is unavailable. On macOS/Linux, try `python3`. Check your version with `python --version`. If Python is missing, use the [official Python downloads](https://www.python.org/downloads/), or start with the no-install walkthrough below.

The starter passes **2 of 6** checks. Four failures are intentional. `--check` exits with code 1 until all six checks pass; that alone is not an installation error.

## Your mission

1. Read [the source document](data/workspaces.md). For a Studio workspace, how many projects are allowed?
2. Compare it with the chunks printed by `--trace`. What information is missing?
3. Change **only `chunking.py`** to preserve the relevant context. Do not change the source, questions, expected answers, or ranking function.
4. Run `python lab.py --check` again. Explain why the fix helps, not just why the checks are green.

Stuck? Open [progressive hints](HINTS.md). Want to compare? Read [the explanation](SOLUTION.md) and run `python lab.py --reference --check`. That runs the supplied solution, not your own fix.

One extra question: would this fix make a question about a nonexistent workspace safe to answer? **No.** Explain what else would be needed.

## No-install preview

In [the document](data/workspaces.md), the `Studio` heading qualifies the paragraph that allows 50 projects. The starter strips headings before ranking. All project-limit paragraphs then contain the same query words, so the first one wins: the Basic limit of 5. Read the document and [starter function](chunking.py), predict the fix, then inspect the [solution](SOLUTION.md).

Reading is welcome. When sending feedback, please distinguish reading from actually running the code.

## Finished, or got stuck? Send one short result

Run `python lab.py --check` and copy the `RESULT` line. Then choose **one** route:

- **Public:** this repository's **Issues → New issue → Tried the lab**. GitHub sign-in required. Please do not include email addresses, credentials, private code, or customer data.
- **Private:** [email Dharani](mailto:dharani96556@gmail.com?subject=RAG%20lab%20feedback). No GitHub account required; your email address will be visible to me.

Send: **“I ran it / only read it / got stuck. My result was ____. The confusing or useful part was ____.”** A failure report is just as useful as a successful result. You do not have to return to Medium or write a review. Neither route is anonymous; nothing is submitted automatically.

If you want one email when a proposed **US$19 three-exercise pack** is available, separately say **“Notify me once about the $19 pack.”** It is not currently available, and this is not a preorder or a subscription. Sending ordinary feedback does not opt you in. The free exercise and solution remain free.

Optional: star this repository to find it later. Fork only if you want your own GitHub copy or want to propose a change. Neither is required to unlock anything.

## What this does and does not demonstrate

- Six synthetic checks measure exact passage selection for three named workspace types and two topics.
- The reference preserves heading context and makes it searchable. Metadata that is merely stored but never used in retrieval would not fix this example.
- Word overlap is intentionally simple; it does not understand synonyms, negation, authority, permissions, or unsupported questions. Tie-breaking is document order.
- The reference parser supports plain ATX Markdown headings and paragraphs in these fixtures, not the full Markdown specification, tables, code fences, PDFs, or HTML.
- Do not use this as a production retriever, security control, or benchmark. Real systems need representative data, appropriate retrieval, answer grounding, and abstention tests.

## Maintainer checks

```sh
python -m unittest discover -s tests -v
python lab.py --baseline --check
python lab.py --reference --check
```

The second command intentionally exits 1 with 2/6. The last should exit 0 with 6/6. Harness tests check the reference and known failure independently of your editable function.

Version: `0.1.0`. Created with AI assistance by Dharani Eswaramurthi. Automated checks are included; independent expert review and learner testing are still pending. [MIT license](LICENSE).
