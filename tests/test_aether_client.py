#!/usr/bin/env python3
"""Aether client — never approve / reject / next; never write CURRENT."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_client import CLIENT_ALLOW, CLIENT_DENY, client_run  # noqa: E402
from aether_pocket import PocketError, is_operator_tree  # noqa: E402

POCKET_CURRENT = """# CURRENT

**Objective:** Plan a small garden bed with the client.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** sitting-1
**Next:** name-plants
**Approval:** PENDING

## Keep
- rain barrel

## Reject
- concrete the yard

## Limits
- one afternoon

## Next allowed action
Name the plants.

## Approval condition
Human Yes on the phone.

## Prohibited
- automatic-approve
- model-auto-approve
"""


class TestClientAllowDeny(unittest.TestCase):
    def test_allow_has_client_room_verbs(self) -> None:
        for verb in ("current", "brief", "validate", "events", "drift", "verbs", "help", "status"):
            self.assertIn(verb, CLIENT_ALLOW)
        for verb in ("approve", "reject", "next", "deinit", "init", "onboard"):
            self.assertIn(verb, CLIENT_DENY)
            self.assertNotIn(verb, CLIENT_ALLOW)


class TestClientRunPocket(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pocket = Path(self.tmp.name)
        (self.pocket / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
        os.environ["AETHER_HOME"] = str(ROOT)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _current_text(self) -> str:
        return (self.pocket / "CURRENT.md").read_text(encoding="utf-8")

    def test_approve_refused_current_unchanged(self) -> None:
        before = self._current_text()
        result = client_run(self.pocket, "approve")
        self.assertFalse(result["ok"])
        self.assertEqual(result["verb"], "approve")
        self.assertIn("refused", result["text"].lower())
        self.assertIn("cannot", result["text"].lower())
        self.assertEqual(self._current_text(), before)

    def test_reject_refused(self) -> None:
        before = self._current_text()
        result = client_run(self.pocket, "reject")
        self.assertFalse(result["ok"])
        self.assertIn("refused", result["text"].lower())
        self.assertEqual(self._current_text(), before)

    def test_next_refused(self) -> None:
        before = self._current_text()
        result = client_run(self.pocket, "next")
        self.assertFalse(result["ok"])
        self.assertIn("refused", result["text"].lower())
        self.assertEqual(self._current_text(), before)

    def test_deinit_init_onboard_refused(self) -> None:
        before = self._current_text()
        for verb in ("deinit", "init", "onboard", "yes", "Approve", "NEXT"):
            result = client_run(self.pocket, verb)
            self.assertFalse(result["ok"], verb)
            self.assertIn("refused", result["text"].lower(), verb)
        self.assertEqual(self._current_text(), before)

    def test_current_ok_contains_next_and_objective(self) -> None:
        result = client_run(self.pocket, "current")
        self.assertTrue(result["ok"], result["text"])
        self.assertEqual(result["verb"], "current")
        self.assertIn("Next", result["text"])
        self.assertIn("Objective", result["text"])
        self.assertIn("name-plants", result["text"])
        self.assertIn("garden bed", result["text"])

    def test_client_run_does_not_write_current(self) -> None:
        before = self._current_text()
        for verb in CLIENT_ALLOW:
            result = client_run(self.pocket, verb)
            self.assertIn("ok", result)
            self.assertEqual(self._current_text(), before, f"CURRENT mutated by {verb}")
        self.assertEqual(self._current_text(), before)

    def test_validate_ok(self) -> None:
        result = client_run(self.pocket, "validate")
        self.assertTrue(result["ok"], result["text"])
        self.assertIn("VALIDATE", result["text"])

    def test_brief_ok(self) -> None:
        result = client_run(self.pocket, "brief")
        self.assertTrue(result["ok"], result["text"])
        self.assertIn("name-plants", result["text"])


class TestClientOperatorTree(unittest.TestCase):
    def test_operator_tree_detected(self) -> None:
        self.assertTrue(is_operator_tree(ROOT))

    def test_operator_tree_refused_and_current_untouched(self) -> None:
        before = (ROOT / "CURRENT.md").read_text(encoding="utf-8")
        try:
            result = client_run(ROOT, "current")
        except PocketError as exc:
            self.assertIn("operator", str(exc).lower())
            self.assertEqual((ROOT / "CURRENT.md").read_text(encoding="utf-8"), before)
            return
        self.assertFalse(result["ok"])
        self.assertIn("operator", result["text"].lower())
        self.assertEqual((ROOT / "CURRENT.md").read_text(encoding="utf-8"), before)

    def test_operator_tree_approve_does_not_write(self) -> None:
        before = (ROOT / "CURRENT.md").read_text(encoding="utf-8")
        try:
            result = client_run(ROOT, "approve")
        except PocketError:
            self.assertEqual((ROOT / "CURRENT.md").read_text(encoding="utf-8"), before)
            return
        self.assertFalse(result["ok"])
        self.assertEqual((ROOT / "CURRENT.md").read_text(encoding="utf-8"), before)


class TestClientFallback(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pocket = Path(self.tmp.name)
        (self.pocket / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
        (self.pocket / ".aether").mkdir()
        (self.pocket / ".aether" / "events.jsonl").write_text(
            '{"t":"note","msg":"hello from events"}\n',
            encoding="utf-8",
        )
        os.environ["AETHER_HOME"] = str(ROOT)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_fallback_current_and_no_write(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        with patch("aether_client.find_aether_bin", return_value=None):
            result = client_run(self.pocket, "current")
            self.assertTrue(result["ok"], result["text"])
            self.assertIn("**Next:**", result["text"])
            self.assertIn("**Objective:**", result["text"])
            denied = client_run(self.pocket, "approve")
            self.assertFalse(denied["ok"])
            self.assertIn("refused", denied["text"].lower())
            events = client_run(self.pocket, "events")
            self.assertTrue(events["ok"], events["text"])
            self.assertIn("hello from events", events["text"])
            validate = client_run(self.pocket, "validate")
            self.assertTrue(validate["ok"], validate["text"])
            self.assertIn("VALIDATE: OK", validate["text"])
        after = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
