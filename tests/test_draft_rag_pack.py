#!/usr/bin/env python3
"""draft_rag_pack — no network. Never writes CURRENT."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from draft_rag_pack import pack  # noqa: E402


class TestDraftRagPack(unittest.TestCase):
    def test_bound_plus_shots_no_current_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "CURRENT.md").write_text("**Next:** keep-me\n", encoding="utf-8")
            (p / "PROPOSE-CURRENT.md").write_text("NOT ACTIVE draft\n", encoding="utf-8")
            before = (p / "CURRENT.md").read_text(encoding="utf-8")
            blob = pack(p, corpus=ROOT / "examples" / "propose-current", max_bytes=12_000, shots=2)
            after = (p / "CURRENT.md").read_text(encoding="utf-8")
            self.assertEqual(before, after)
            self.assertIn("keep-me", blob)
            self.assertIn("NOT ACTIVE", blob)
            self.assertIn("Never write CURRENT.md", blob)
            self.assertIn("FEW-SHOT", blob)
            self.assertNotIn("--- BOUND .env", blob)

    def test_cap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "CURRENT.md").write_text("x" * 50_000, encoding="utf-8")
            blob = pack(p, corpus=ROOT / "examples" / "propose-current", max_bytes=3_000, shots=1)
            self.assertLessEqual(len(blob), 4_000)


if __name__ == "__main__":
    unittest.main()
