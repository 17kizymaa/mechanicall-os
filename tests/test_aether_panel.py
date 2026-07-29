#!/usr/bin/env python3
"""Unit tests for Project Panel projection (stdlib only)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_panel import (  # noqa: E402
    discover_proposes,
    known_projects,
    load_state,
    render_html,
    render_md,
    render_text,
    write_projections,
)


class TestPanelProjection(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".aether").mkdir()
        (self.root / "CURRENT.md").write_text(
            """# CURRENT

**Objective:** Ship the panel without drama.
**Phase:** EXECUTE
**Status:** READY-FOR-REVIEW
**Baseline:** alpha
**Next:** write-tests
**Approval:** PENDING

## Prohibited
- deploy-production
- add-postgres
""",
            encoding="utf-8",
        )
        (self.root / ".aether" / "events.jsonl").write_text(
            '{"ts":"t","kind":"preflight","action":"deploy-production","result":"refused"}\n',
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_load_fields(self) -> None:
        st = load_state(self.root)
        self.assertTrue(st.has_current)
        self.assertEqual(st.next_action, "write-tests")
        self.assertEqual(st.objective, "Ship the panel without drama.")
        self.assertIn("deploy-production", st.prohibited)
        self.assertEqual(len(st.recent_events), 1)

    def test_render_text_contains_next(self) -> None:
        text = render_text(load_state(self.root))
        self.assertIn("write-tests", text)
        self.assertIn("deploy-production", text)
        self.assertIn("NEXT", text)
        self.assertIn("PROHIBITED", text)
        self.assertIn("Operator Board", text)
        self.assertIn("Human only", text)

    def test_write_md_html(self) -> None:
        st = load_state(self.root)
        md_p, html_p = write_projections(st)
        self.assertTrue(md_p.is_file())
        self.assertTrue(html_p.is_file())
        md = md_p.read_text(encoding="utf-8")
        self.assertIn("write-tests", md)
        self.assertIn("Operator Board", md)
        ht = html_p.read_text(encoding="utf-8")
        self.assertIn("write-tests", ht)
        self.assertIn("<!DOCTYPE html>", ht)

    def test_render_md_html_helpers(self) -> None:
        st = load_state(self.root)
        self.assertIn("**Next**", render_md(st))
        self.assertIn("class=\"next\"", render_html(st))

    def test_discover_proposes(self) -> None:
        art = self.root / "artifacts"
        art.mkdir()
        (art / "PROPOSE-TEST.md").write_text("# propose\n", encoding="utf-8")
        (art / "PRESPIKE-X.md").write_text("# spike\n", encoding="utf-8")
        found = discover_proposes(self.root)
        names = {p.name for p in found}
        self.assertIn("PROPOSE-TEST.md", names)
        self.assertIn("PRESPIKE-X.md", names)
        st = load_state(self.root)
        self.assertTrue(any(p.name == "PROPOSE-TEST.md" for p in st.proposes))
        text = render_text(st)
        self.assertIn("PROPOSE-TEST.md", text)

    def test_known_projects_nonempty(self) -> None:
        # Host may or may not have all four; function must not crash.
        _ = known_projects()


if __name__ == "__main__":
    unittest.main()
