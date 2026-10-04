import json
from pathlib import Path
import unittest

from engine import Chunk, naive_chunks, rank, retrieve, tokens
from reference import make_chunks

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = (ROOT / "data" / "workspaces.md").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "data" / "cases.json").read_text(encoding="utf-8"))


class LabTests(unittest.TestCase):
    def test_known_failure_is_reproducible(self):
        chunks = naive_chunks(DOCUMENT)
        self.assertEqual(sum(retrieve(c["question"], chunks) == c["expected"] for c in CASES), 2)
        self.assertEqual(retrieve(CASES[1]["question"], chunks), CASES[0]["expected"])

    def test_reference_passes_all_cases(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.assertEqual(retrieve(case["question"], make_chunks(DOCUMENT)), case["expected"])

    def test_reference_not_dependent_on_document_order(self):
        chunks = list(reversed(make_chunks(DOCUMENT)))
        for case in CASES:
            self.assertEqual(retrieve(case["question"], chunks), case["expected"])

    def test_reference_is_not_hardcoded_to_workspace_names(self):
        document = DOCUMENT.replace("Basic", "Cedar").replace("Studio", "Maple").replace("Enterprise", "Birch")
        for case in CASES:
            query = case["question"].replace("Basic", "Cedar").replace("Studio", "Maple").replace("Enterprise", "Birch")
            self.assertEqual(retrieve(query, make_chunks(document)), case["expected"])

    def test_paragraph_bodies_preserved(self):
        self.assertEqual([c.text for c in make_chunks(DOCUMENT)], [c.text for c in naive_chunks(DOCUMENT)])

    def test_heading_scope_resets_and_flushes(self):
        chunks = make_chunks("# Root\n## First\n### Child\nold body\n## Second\nnew body\n# Other\nlast body")
        self.assertEqual([c.heading for c in chunks], ["Root > First > Child", "Root > Second", "Other"])
        self.assertEqual([c.text for c in chunks], ["old body", "new body", "last body"])

    def test_empty_document(self):
        self.assertEqual(make_chunks(""), [])
        self.assertEqual(naive_chunks("# Heading only"), [])
        self.assertEqual(retrieve("projects", []), "NO MATCH")

    def test_multiline_and_unheaded_paragraph(self):
        self.assertEqual(make_chunks("first line\nsecond line\n\n# Next\nbody"),
                         [Chunk("first line second line"), Chunk("body", "Next")])

    def test_windows_newlines(self):
        self.assertEqual(make_chunks(DOCUMENT.replace("\n", "\r\n")), make_chunks(DOCUMENT))

    def test_tokens_and_case(self):
        self.assertEqual(tokens("Studio: PROJECTS! 50"), {"studio", "projects", "50"})

    def test_stable_ties_and_no_overlap(self):
        chunks = [Chunk("projects one"), Chunk("projects two")]
        self.assertEqual(rank("projects", chunks)[0][1], chunks[0])
        self.assertEqual(retrieve("unrelated", chunks), "NO MATCH")

    def test_metadata_is_actually_searched(self):
        chunks = [Chunk("projects five", "Basic"), Chunk("projects fifty", "Studio")]
        self.assertEqual(retrieve("Studio projects", chunks), "projects fifty")


if __name__ == "__main__":
    unittest.main()
