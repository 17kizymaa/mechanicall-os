#!/usr/bin/env python3
"""STORM factory — never the A33. Never Yes."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_storm import (  # noqa: E402
    CAP,
    REFUSE_SERIAL,
    StormError,
    create_avd,
    list_avds,
    main,
    probe,
    refuse_serial,
    status,
)


class TestStorm(unittest.TestCase):
    def setUp(self) -> None:
        self._home = os.environ.get("MECHANICALL_STORM_HOME")

    def tearDown(self) -> None:
        if self._home is None:
            os.environ.pop("MECHANICALL_STORM_HOME", None)
        else:
            os.environ["MECHANICALL_STORM_HOME"] = self._home

    def test_refuse_a33(self) -> None:
        with self.assertRaises(StormError):
            refuse_serial(REFUSE_SERIAL)
        self.assertEqual(main(["status", "--serial", REFUSE_SERIAL]), 3)

    def test_cap_two(self) -> None:
        self.assertEqual(CAP, 2)
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["MECHANICALL_STORM_HOME"] = tmp
            with self.assertRaises(StormError):
                create_avd("storm-2")

    def test_name_must_be_storm(self) -> None:
        with self.assertRaises(StormError):
            create_avd("emulator-5554")

    def test_probe_and_status_do_not_write_current(self) -> None:
        st = probe()
        self.assertIn("sdk", st)
        self.assertEqual(st["refuse"], REFUSE_SERIAL)
        out = status()
        self.assertIn("avds", out)
        live = (ROOT / "CURRENT.md").read_text(encoding="utf-8")
        self.assertTrue(live)

    def test_isolated_home_lists_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["MECHANICALL_STORM_HOME"] = tmp
            self.assertEqual(list_avds(), [])


if __name__ == "__main__":
    unittest.main()
