#!/usr/bin/env python3
"""Draft dest is a whole-file writer. Never Confirm."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from app_verify import score_source  # noqa: E402


JAVA = (
    ROOT
    / "android"
    / "app"
    / "src"
    / "main"
    / "java"
    / "com"
    / "mechanicall"
    / "pocket"
    / "demo"
)


class TestDraftWriter(unittest.TestCase):
    def test_source_is_text_editor(self) -> None:
        rack = (JAVA / "SitRackView.kt").read_text(encoding="utf-8")
        nav = (JAVA / "MainActivity.kt").read_text(encoding="utf-8")
        self.assertIn("editDraftWriter", rack)
        self.assertIn("IME_FLAG_NO_ENTER_ACTION", rack)
        self.assertIn("savePropose", nav)
        self.assertNotIn("drawTerminalDest", rack)
        self.assertNotIn("draftFieldOnGlass", nav)

    def test_law_rows_pass(self) -> None:
        rows = {r["id"]: r for r in score_source()}
        self.assertTrue(rows["B3-plan-manual-edit"]["ok"], rows["B3-plan-manual-edit"])
        self.assertTrue(rows["B4-draft-is-workshop"]["ok"], rows["B4-draft-is-workshop"])
        self.assertTrue(rows["B13-draft-workshop-page"]["ok"], rows["B13-draft-workshop-page"])


if __name__ == "__main__":
    unittest.main()
