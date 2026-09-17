#!/usr/bin/env python3
"""Send dest stages. Not Yes. Never Confirm."""
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


class TestSendFolder(unittest.TestCase):
    def test_source_stages_on_plaque(self) -> None:
        nav = (JAVA / "MainActivity.kt").read_text(encoding="utf-8")
        rack = (JAVA / "SitRackView.kt").read_text(encoding="utf-8")
        crects = (JAVA / "SitCRects.kt").read_text(encoding="utf-8")
        self.assertIn("stageSendFolder", nav)
        self.assertIn("sendFolder", nav)
        self.assertIn("folderSend", crects)
        self.assertIn("folderOem", crects)
        send_block = nav.split("SitHit.Send")[-1].split("SitHit.")[0]
        self.assertNotIn("FaceBridge.yes", send_block)
        self.assertIn("folderSend.contains", rack)

    def test_law_rows_pass(self) -> None:
        rows = {r["id"]: r for r in score_source()}
        self.assertTrue(rows["B12-send-overlay"]["ok"], rows["B12-send-overlay"])
        self.assertTrue(rows["B14-send-folder-smoke"]["ok"], rows["B14-send-folder-smoke"])


if __name__ == "__main__":
    unittest.main()
