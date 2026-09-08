#!/usr/bin/env python3
"""you_decide_gauntlet — never Confirm; first FAIL is iterate."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from look_verify import REFUSE_SERIAL  # noqa: E402
from you_decide_gauntlet import STEPS, EXIT_REFUSE, main, render, row  # noqa: E402


class TestGauntlet(unittest.TestCase):
    def test_steps(self) -> None:
        self.assertEqual(len(STEPS), 11)
        self.assertEqual(STEPS[0], "G0-launch")
        self.assertEqual(STEPS[-1], "G10-relaunch")

    def test_refuse_a33(self) -> None:
        self.assertEqual(main(["--serial", REFUSE_SERIAL]), EXIT_REFUSE)

    def test_render_first_fail(self) -> None:
        rows = [row("G0-launch", True, "sit"), row("G1-bound", False, "miss")]
        md = render(rows)
        self.assertIn("G1-bound", md)
        self.assertIn("FAIL", md)
        self.assertIn("SKIP", md)
        self.assertIn("First FAIL is the next patch", md)


if __name__ == "__main__":
    unittest.main()
