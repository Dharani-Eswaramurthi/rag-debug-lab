# RAG Debug Lab — a Python retrieval debugging exercise

[![Lab checks](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/actions/workflows/checks.yml)

**The answer is in the document. Why does retrieval select the wrong passage?**

Practise RAG debugging in a free, offline Python exercise: inspect a retrieval trace, find context lost during document chunking, and repair the splitter. Built for people who have tried a first retrieval-augmented generation (RAG) demo and want to understand its retrieval behaviour.

**Python 3.10+ · standard library only · no API keys · no signup · MIT license**

[Start the exercise](#quick-start) · [Read without installing](#the-retrieval-failure-in-one-example) · [Hints](HINTS.md) · [Solution (spoiler)](SOLUTION.md) · [Contribute](CONTRIBUTING.md)

This is **one deterministic retrieval exercise**, not a complete RAG chatbot. It uses word overlap instead of embeddings and prints a passage instead of calling an LLM. All documents, company names and questions are fictional. It makes no network calls and collects no telemetry.

## Quick start

You need Python 3.10 or newer and a terminal. Basic familiarity with Python functions and lists will help; no RAG framework or vector database is required.

**Download:** [Download the source ZIP](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/archive/refs/heads/main.zip), extract it, and open a terminal inside the extracted `rag-debug-lab-main` folder. You can also use **Code → Download ZIP** on this page.

**Or clone with Git:**

```sh
git clone https://github.com/Dharani-Eswaramurthi/rag-debug-lab.git
cd rag-debug-lab
```

Then run:

```sh
python lab.py
python lab.py --trace
python lab.py --check
```

On Windows, try `py` if `python` is unavailable. On macOS/Linux, try `python3`. Check your version with `python --version`. If needed, [install Python from its official website](https://www.python.org/downloads/), or use the reading-only example below.

**Expected starter result:**

```text
RESULT missing-heading v0.1.0 mode=learner checks=2/6
```

Four failed exercise checks are intentional. `--check` exits with code **1** until all six checks pass; this result alone is not an installation error. You do not need to install packages, create an account, fork the repository, or star it to participate.

## Your debugging task

1. Read [the source document](data/workspaces.md). For a Studio workspace, how many projects are allowed?
2. Compare the document with the chunks and ranking printed by `--trace`. What context disappeared?
3. Change **only [`chunking.py`](chunking.py)** to preserve that context. Keep the source document, questions, expected answers and ranking function unchanged.
4. Run `python lab.py --check` again. Explain why the selected passage changes.

The exercise is designed to take about 15–20 minutes; this timing has **not** been tested with learners. Take the time you need.

Stuck? Open the [progressive hints](HINTS.md) one at a time. When ready to compare, read [the solution explanation](SOLUTION.md) or run:

```sh
python lab.py --reference --check
```

That runs the **supplied solution**, not your own fix:

```text
RESULT missing-heading v0.1.0 mode=reference checks=6/6
```

## The retrieval failure in one example

You can follow this example without installing anything.

| Step | What happens |
|---|---|
| Source document | `Basic` allows **5** projects; `Studio` allows **50**. |
| Question | “How many projects can a Studio workspace contain?” |
| Broken chunking | The paragraph bodies survive, but their workspace headings are discarded. |
| Word-overlap ranking | All three project-limit passages tie. Document order selects Basic's **5**. |
| Reference | The headings become part of the searched context, so Studio's **50** wins for this question. |

Read the [document](data/workspaces.md), inspect the [starter](chunking.py), predict a fix, then compare with the [explanation](SOLUTION.md). Storing heading metadata without searching it would not fix this example.

The programme has returned a real passage from the source, but it belongs to the wrong workspace. There is no LLM in this exercise: the failure occurs in selecting evidence.

**Check your understanding:** would preserving headings make a question about a nonexistent workspace safe to answer? No. The retriever can still return an inappropriate passage. Explain what else would need to be checked before trusting an answer.

## What you can practise

- Following a question from the source document through chunks to ranked passages.
- Recognising how lost heading context changes retrieval.
- Making one targeted repair and checking its effect.
- Distinguishing passing fixture checks from reliable behaviour on new questions.

These are the intended activities, not measured learning outcomes. Independent expert review and learner testing are still pending.

## Files to explore

| File | Purpose |
|---|---|
| [`lab.py`](lab.py) | Run the exercise, print a trace and check the six cases. |
| [`chunking.py`](chunking.py) | Your editable, deliberately broken starter. |
| [`engine.py`](engine.py) | Chunk structure, word-overlap scoring and stable tie-breaking. |
| [`data/workspaces.md`](data/workspaces.md) | Small fictional source document. |
| [`data/cases.json`](data/cases.json) | Six questions and expected passages. |
| [`HINTS.md`](HINTS.md) | Progressive hints. |
| [`reference.py`](reference.py) and [`SOLUTION.md`](SOLUTION.md) | Supplied repair and its limits; spoilers. |
| [`tests/`](tests/) | Automated harness and command-line tests. |

## Share a result or get help

Run `python lab.py --check` and copy the `RESULT` line, if available. Choose one route:

- **Public:** [open the “Tried the lab” feedback form](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/issues/new?template=tried-the-lab.yml). GitHub sign-in is required. Do not include email addresses, credentials, private code or customer data.
- **Private:** [email Dharani](mailto:dharani96556@gmail.com?subject=RAG%20lab%20feedback). No GitHub account is required; your email address will be visible to me.

Send: **“I ran it / only read it / got stuck. My result was ____. The confusing or useful part was ____.”** Please distinguish your own repair from running the reference solution. Reading-only and failure reports are useful too. Neither route is anonymous; nothing is submitted automatically.

For an unexpected crash or incorrect documentation, [report a bug](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/issues/new?template=bug-report.yml). See [CONTRIBUTING.md](CONTRIBUTING.md) for small ways to help. A star is optional if you want to find the lab later.

<details>
<summary>Optional: hear about a future exercise pack</summary>

If you want one email when a proposed **US$19 three-exercise pack** is available, separately say **“Notify me once about the $19 pack.”** It is not currently available, and this is not a preorder or subscription. Ordinary feedback does not opt you in. The free exercise and solution remain free.

</details>

## Scope and limitations

- Six synthetic checks measure exact passage selection for three workspace types and two topics.
- Word overlap does not understand synonyms, negation, authority, permissions or unsupported questions. Ties follow document order.
- The reference parser handles plain ATX Markdown headings and paragraphs in these fixtures, not the full Markdown specification, tables, code fences, PDFs or HTML.
- This is not a production retriever, security control, chatbot reliability benchmark or evidence of improved learner performance.
- Real systems need representative evaluation data, suitable retrieval, answer-grounding checks and tests for declining unsupported questions.

## Maintainer checks

```sh
python -m unittest discover -s tests -v
python lab.py --baseline --check
python lab.py --reference --check
```

The **17 harness tests** are separate from the **six exercise checks**. The baseline command intentionally exits **1** with 2/6; the reference exits **0** with 6/6. Harness tests check the reference and known failure independently of your editable starter.

The [Lab checks workflow](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/actions/workflows/checks.yml) runs the harness on its configured Python/OS combinations. Its badge reports the workflow result; it does not measure learner understanding or production reliability.

Version **0.1.0**. Created with AI assistance by **Dharani Eswaramurthi**. Code and fictional fixtures are available under the [MIT license](LICENSE).
