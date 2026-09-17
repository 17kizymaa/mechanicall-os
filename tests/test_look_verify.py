#!/usr/bin/env python3
"""look_verify — launcher is FAIL; IsolatedDark dest is FLAG. Never Confirm."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from look_verify import L_ROWS, REFUSE_SERIAL, main, score  # noqa: E402


class TestLookVerify(unittest.TestCase):
    def test_ids(self) -> None:
        rows = score(None)
        self.assertEqual([r["id"] for r in rows], list(L_ROWS))

    def test_refuse_a33(self) -> None:
        self.assertEqual(main(["--serial", REFUSE_SERIAL]), 3)

    def test_launcher_png_fails_l0(self) -> None:
        d = ROOT / "dev" / "55_sit-dest-preview" / "01_look" / "output"
        if not (d / "look-after-send.png").is_file():
            self.skipTest("no dest-preview launcher PNG")
        rows = {r["id"]: r for r in score(d)}
        self.assertEqual(rows["L0-frame"]["verdict"], "FAIL", rows["L0-frame"])

    def test_first_sit_look_dests_flag(self) -> None:
        d = ROOT / "dev" / "57_first-sit-look" / "02_still" / "output"
        if not (d / "dest-crt.png").is_file():
            self.skipTest("no first-sit-look dest stills")
        rows = {r["id"]: r for r in score(d)}
        self.assertNotEqual(rows["L0-frame"]["verdict"], "FAIL", rows["L0-frame"])
        self.assertEqual(rows["L2-crt-dest"]["verdict"], "FLAG", rows["L2-crt-dest"])
        self.assertIn(rows["L3-draft-dest"]["verdict"], ("FLAG", "PASS"), rows["L3-draft-dest"])


if __name__ == "__main__":
    unittest.main()
