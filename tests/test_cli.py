from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import lab
import reference

ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "lab.py"), *args],
                              cwd=ROOT.parent, capture_output=True, text=True,
                              timeout=10, check=False)

    def test_baseline_check_fails_from_different_directory(self):
        result = self.run_cli("--baseline", "--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("mode=baseline checks=2/6", result.stdout)

    def test_reference_check_passes(self):
        result = self.run_cli("--reference", "--trace", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("mode=reference checks=6/6", result.stdout)
        self.assertIn("Northstar workspace handbook > Studio", result.stdout)

    def test_demo_does_not_exit_with_error_for_intentional_failure(self):
        result = self.run_cli("--baseline")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("checks=2/6", result.stdout)

    def test_mode_flags_mutually_exclusive(self):
        result = self.run_cli("--baseline", "--reference")
        self.assertEqual(result.returncode, 2)

    def test_fixed_learner_slot(self):
        output = io.StringIO()
        with patch.object(lab, "make_chunks", reference.make_chunks), \
                patch.object(sys, "argv", ["lab.py", "--check"]), redirect_stdout(output):
            self.assertEqual(lab.main(), 0)
        self.assertIn("mode=learner checks=6/6", output.getvalue())


if __name__ == "__main__":
    unittest.main()
