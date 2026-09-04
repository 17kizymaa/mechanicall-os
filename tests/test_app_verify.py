#!/usr/bin/env python3
"""app_verify scorer — never taps Confirm."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from app_verify import BEHAVIOURS, REFUSE_SERIAL, main, score_source  # noqa: E402


class TestAppVerify(unittest.TestCase):
    def test_ten_behaviours(self) -> None:
        rows = score_source()
        ids = [r["id"] for r in rows]
        self.assertEqual(ids, list(BEHAVIOURS))
        self.assertEqual(len(rows), 15)

    def test_last_pass_closes_gaps(self) -> None:
        rows = {r["id"]: r for r in score_source()}
        self.assertTrue(rows["B3-plan-manual-edit"]["ok"], rows["B3-plan-manual-edit"])
        self.assertTrue(rows["B4-draft-is-workshop"]["ok"], rows["B4-draft-is-workshop"])
        self.assertTrue(rows["B7-gate-instrument"]["ok"], rows["B7-gate-instrument"])
        self.assertTrue(rows["B11-crt-isolated"]["ok"], rows["B11-crt-isolated"])
        self.assertTrue(rows["B12-send-overlay"]["ok"], rows["B12-send-overlay"])
        self.assertTrue(rows["B13-draft-workshop-page"]["ok"], rows["B13-draft-workshop-page"])
        self.assertTrue(rows["B15-receipt-honest"]["ok"], rows["B15-receipt-honest"])

    def test_refuse_a33(self) -> None:
        self.assertEqual(main(["--serial", REFUSE_SERIAL]), 3)

    def test_exit_zero_when_all_pass(self) -> None:
        self.assertEqual(main([]), 0)


if __name__ == "__main__":
    unittest.main()
