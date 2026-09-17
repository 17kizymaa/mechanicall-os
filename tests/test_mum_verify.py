#!/usr/bin/env python3
"""mum_verify — benchmark statements. Never Confirm."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from mum_verify import M_ROWS, REFUSE_SERIAL, main, parse_gauntlet, score  # noqa: E402


class TestMumVerify(unittest.TestCase):
    def test_ids(self) -> None:
        rows = score()
        self.assertEqual([r["id"] for r in rows], list(M_ROWS))
        self.assertTrue(all(r.get("statement") for r in rows))

    def test_protocol_pass_language_flag(self) -> None:
        rows = {r["id"]: r for r in score()}
        for mid in M_ROWS:
            if mid == "M9-casual-language":
                continue
            self.assertEqual(rows[mid]["verdict"], "PASS", rows[mid])
        self.assertEqual(rows["M9-casual-language"]["verdict"], "FLAG", rows["M9-casual-language"])

    def test_refuse_a33(self) -> None:
        self.assertEqual(main(["--serial", REFUSE_SERIAL]), 3)

    def test_parse_gauntlet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "GAUNTLET.md"
            p.write_text(
                "| id | verdict | evidence |\n"
                "|----|---------|----------|\n"
                "| G7-draft-propose | PASS | typed |\n"
                "| G11-send-stage | FAIL | missing |\n",
                encoding="utf-8",
            )
            g = parse_gauntlet(p)
            self.assertEqual(g["G7-draft-propose"], "PASS")
            self.assertEqual(g["G11-send-stage"], "FAIL")

    def test_exit_zero_when_only_flag(self) -> None:
        self.assertEqual(main([]), 0)


if __name__ == "__main__":
    unittest.main()
