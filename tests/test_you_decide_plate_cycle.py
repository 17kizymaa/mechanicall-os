#!/usr/bin/env python3
"""you_decide_plate_cycle — FLAG is iterate; other-row FLAG is not this plate."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from look_verify import REFUSE_SERIAL  # noqa: E402
from you_decide_plate_cycle import (  # noqa: E402
    EXIT_BUDGET,
    EXIT_ENV,
    EXIT_ITERATE,
    EXIT_PASS,
    EXIT_REFUSE,
    budget_stop,
    decide,
    main,
    normalize_plate,
)


def _look(lid: str, verdict: str) -> dict:
    return {"id": lid, "verdict": verdict, "ok": verdict == "PASS", "evidence": lid}


def _law(ok: bool = True) -> list[dict]:
    return [{"id": "B1-bind-first", "verdict": "PASS" if ok else "FAIL", "ok": ok, "evidence": "t"}]


class TestPlateCycle(unittest.TestCase):
    def test_normalize(self) -> None:
        self.assertEqual(normalize_plate("L2"), "L2-crt-dest")
        self.assertEqual(normalize_plate("L3-draft-dest"), "L3-draft-dest")
        with self.assertRaises(ValueError):
            normalize_plate("L9")

    def test_this_plate_pass_ignores_other_flag(self) -> None:
        look = [
            _look("L0-frame", "PASS"),
            _look("L2-crt-dest", "FLAG"),
            _look("L3-draft-dest", "PASS"),
            _look("L6-decide-well", "FLAG"),
        ]
        d = decide("L3-draft-dest", look, _law(True))
        self.assertEqual(d["name"], "PASS")
        self.assertEqual(d["exit"], EXIT_PASS)

    def test_this_plate_flag_is_iterate(self) -> None:
        look = [_look("L0-frame", "PASS"), _look("L2-crt-dest", "FLAG")]
        d = decide("L2-crt-dest", look, _law(True))
        self.assertEqual(d["name"], "FLAG")
        self.assertEqual(d["exit"], EXIT_ITERATE)

    def test_l0_fail_fail_closes(self) -> None:
        look = [_look("L0-frame", "FAIL"), _look("L2-crt-dest", "PASS")]
        d = decide("L2-crt-dest", look, _law(True))
        self.assertEqual(d["name"], "FAIL")
        self.assertEqual(d["exit"], EXIT_ITERATE)

    def test_law_fail_fail_closes(self) -> None:
        look = [_look("L0-frame", "PASS"), _look("L2-crt-dest", "PASS")]
        d = decide("L2-crt-dest", look, _law(False))
        self.assertEqual(d["name"], "FAIL")
        self.assertEqual(d["exit"], EXIT_ITERATE)

    def test_budget_stop_after_n(self) -> None:
        d = {"name": "FLAG", "exit": EXIT_ITERATE, "reason": "IsolatedDark"}
        stopped = budget_stop(d, 5, 5)
        self.assertEqual(stopped["exit"], EXIT_BUDGET)
        self.assertEqual(stopped["name"], "STOP")
        self.assertEqual(budget_stop(d, 1, 5)["exit"], EXIT_ITERATE)

    def test_refuse_a33(self) -> None:
        self.assertEqual(main(["--plate", "L2", "--serial", REFUSE_SERIAL, "--score-only"]), EXIT_REFUSE)

    def test_unknown_plate(self) -> None:
        self.assertEqual(main(["--plate", "nope", "--score-only"]), EXIT_ENV)

    def test_score_only_l2_iterate_on_post_l3_stills(self) -> None:
        stills = ROOT / "dev" / "57_first-sit-look" / "02_still" / "output"
        if not (stills / "dest-crt.png").is_file():
            self.skipTest("no post-L3 dest stills")
        with tempfile.TemporaryDirectory() as tmp:
            code = main(
                [
                    "--plate",
                    "L2",
                    "--score-only",
                    "--stills-dir",
                    str(stills),
                    "--out",
                    tmp,
                    "--iter",
                    "1",
                    "--max",
                    "5",
                ]
            )
            self.assertEqual(code, EXIT_ITERATE, Path(tmp, "VERDICT.md").read_text())
            verdict = Path(tmp, "VERDICT.md").read_text(encoding="utf-8")
            self.assertIn("ITERATE", verdict)
            self.assertIn("L2-crt-dest", verdict)

    def test_score_only_l3_pass_on_post_l3_stills(self) -> None:
        stills = ROOT / "dev" / "57_first-sit-look" / "04_one_plate" / "output" / "stills"
        if not (stills / "dest-draft.png").is_file():
            self.skipTest("no post-L3 dest stills")
        with tempfile.TemporaryDirectory() as tmp:
            code = main(
                [
                    "--plate",
                    "L3",
                    "--score-only",
                    "--stills-dir",
                    str(stills),
                    "--out",
                    tmp,
                ]
            )
            self.assertEqual(code, EXIT_PASS, Path(tmp, "VERDICT.md").read_text())

    def test_loop_score_only_budget_on_l2(self) -> None:
        stills = ROOT / "dev" / "57_first-sit-look" / "02_still" / "output"
        if not (stills / "dest-crt.png").is_file():
            self.skipTest("no post-L3 dest stills")
        with tempfile.TemporaryDirectory() as tmp:
            code = main(
                [
                    "--plate",
                    "L2",
                    "--score-only",
                    "--loop",
                    "--max",
                    "1",
                    "--stills-dir",
                    str(stills),
                    "--out",
                    tmp,
                ]
            )
            self.assertEqual(code, EXIT_BUDGET, Path(tmp, "VERDICT.md").read_text())


if __name__ == "__main__":
    unittest.main()
