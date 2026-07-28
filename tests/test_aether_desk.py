#!/usr/bin/env python3
"""Unit tests for minimal desk (stdlib only)."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_desk import banner, parse_next, project_root, read_current  # noqa: E402
from aether_llm import resolve_backend  # noqa: E402


class TestDesk(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "CURRENT.md").write_text(
            """# CURRENT

**Objective:** Minimal desk
**Phase:** EXECUTE
**Status:** DRAFT
**Next:** run-aether-desk
**Approval:** PENDING
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_parse_next(self) -> None:
        t = read_current(self.root) or ""
        self.assertEqual(parse_next(t), "run-aether-desk")

    def test_banner_contains_objective(self) -> None:
        b = banner(self.root)
        self.assertIn("Minimal desk", b)
        self.assertIn("run-aether-desk", b)

    def test_project_root_cwd(self) -> None:
        self.assertEqual(project_root(self.root), self.root.resolve())


class TestFreeBackendResolve(unittest.TestCase):
    def test_openrouter_preferred(self) -> None:
        env = {
            "OPENROUTER_API_KEY": "sk-or-test",
            "GROQ_API_KEY": "gsk-test",
            "AETHER_LLM_PROVIDER": "",
            "AETHER_MODEL": "",
        }
        with mock.patch.dict(os.environ, env, clear=False):
            # clear force
            os.environ.pop("AETHER_LLM_PROVIDER", None)
            b = resolve_backend()
            self.assertIsNotNone(b)
            assert b is not None
            self.assertEqual(b.name, "openrouter")

    def test_groq_when_no_openrouter(self) -> None:
        env = {
            "OPENROUTER_API_KEY": "",
            "GROQ_API_KEY": "gsk-test",
            "ANTHROPIC_API_KEY": "",
            "XAI_API_KEY": "",
            "AETHER_LLM_PROVIDER": "groq",
            "AETHER_MODEL": "llama-3.3-70b-versatile",
        }
        with mock.patch.dict(os.environ, env, clear=False):
            b = resolve_backend()
            self.assertIsNotNone(b)
            assert b is not None
            self.assertEqual(b.name, "groq")


if __name__ == "__main__":
    unittest.main()
