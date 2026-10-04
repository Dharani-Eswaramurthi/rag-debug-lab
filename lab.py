"""Run from any working directory. This program only reads local lab files."""

import argparse
import json
from pathlib import Path

from chunking import make_chunks
from engine import naive_chunks, rank, retrieve

ROOT = Path(__file__).resolve().parent
VERSION = "0.1.0"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--baseline", action="store_true", help="Use unchanged broken baseline")
    mode.add_argument("--reference", action="store_true", help="SPOILER: use the supplied solution")
    parser.add_argument("--trace", action="store_true", help="Print chunks and one ranking")
    parser.add_argument("--check", action="store_true", help="Exit 1 if any exercise check fails")
    args = parser.parse_args()
    splitter = make_chunks
    selected_mode = "learner"
    if args.baseline:
        splitter, selected_mode = naive_chunks, "baseline"
    elif args.reference:
        from reference import make_chunks as reference_chunks
        splitter, selected_mode = reference_chunks, "reference"
    chunks = splitter((ROOT / "data" / "workspaces.md").read_text(encoding="utf-8"))
    cases = json.loads((ROOT / "data" / "cases.json").read_text(encoding="utf-8"))
    print(f"RAG Debug Lab {VERSION} | {selected_mode}")
    print("Synthetic passage retrieval only; no LLM or network calls.\n")
    if args.trace:
        for index, chunk in enumerate(chunks, 1):
            print(f"CHUNK {index} | heading: {chunk.heading or '(missing)'}\n  {chunk.text}")
        print("\nStudio project question: ranking (larger overlap wins)")
        for score, chunk in rank(cases[1]["question"], chunks):
            print(f"  score={score} | {chunk.heading or '(missing)'} | {chunk.text}")
        print()
    passed = 0
    for case in cases:
        actual = retrieve(case["question"], chunks)
        success = actual == case["expected"]
        passed += int(success)
        print(f"{'PASS' if success else 'FAIL'} {case['id']}: {actual}")
        if not success:
            print(f"  expected: {case['expected']}")
    print(f"\nRESULT missing-heading v{VERSION} mode={selected_mode} checks={passed}/{len(cases)}")
    if passed == len(cases):
        print("These fixtures pass, not production RAG. Explain the fix and its limits.")
    else:
        print("Starter failures are intentional. Inspect --trace, then edit chunking.py.")
    print("Optional: send the RESULT line plus one useful/confusing detail.")
    print("GitHub: Issues > New issue > Tried the lab; or email dharani96556@gmail.com.")
    print("Only share if you choose. No result was uploaded. See README.md for privacy.")
    return 1 if args.check and passed != len(cases) else 0


if __name__ == "__main__":
    raise SystemExit(main())
