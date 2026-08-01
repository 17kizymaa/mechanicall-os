#!/usr/bin/env python3
"""Unit tests for grok_tui backend ranking (no network)."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_llm import (  # noqa: E402
    describe_backend,
    grok_tui_available,
    resolve_backend,
)


class TestGrokTuiBackend(unittest.TestCase):
    def setUp(self) -> None:
        self._saved = {
            k: os.environ.get(k)
            for k in (
                "AETHER_LLM_PROVIDER",
                "AETHER_GROK_TUI",
                "XAI_API_KEY",
                "OPENROUTER_API_KEY",
                "GROQ_API_KEY",
                "ANTHROPIC_API_KEY",
                "AETHER_OPENAI_BASE_URL",
                "GROK_BIN",
                "GROK_HOME",
                "AETHER_MODEL",
            )
        }
        for k in self._saved:
            os.environ.pop(k, None)

    def tearDown(self) -> None:
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_api_key_alone_is_not_grok_tui(self) -> None:
        os.environ["XAI_API_KEY"] = "xai-fake"
        os.environ["AETHER_GROK_TUI"] = "0"
        # Force xai so a host Anthropic key file cannot steal resolution
        os.environ["AETHER_LLM_PROVIDER"] = "xai"
        self.assertFalse(grok_tui_available())
        b = resolve_backend()
        self.assertIsNotNone(b)
        assert b is not None
        self.assertEqual(b.name, "xai")
        # Without force, disabled TUI must not report as grok_tui
        os.environ.pop("AETHER_LLM_PROVIDER", None)
        b2 = resolve_backend()
        if b2 is not None:
            self.assertNotEqual(b2.name, "grok_tui")

    def test_grok_tui_outranks_xai_api(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            token = "x" * 40
            (home / "auth.json").write_text(
                f'{{"access_token":"{token}"}}', encoding="utf-8"
            )
            fake_bin = home / "grok"
            fake_bin.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            fake_bin.chmod(0o755)
            os.environ["GROK_HOME"] = str(home)
            os.environ["GROK_BIN"] = str(fake_bin)
            os.environ["XAI_API_KEY"] = "xai-fake"
            os.environ["AETHER_GROK_TUI"] = "1"
            # clear other free keys that might win if TUI detection failed
            os.environ.pop("OPENROUTER_API_KEY", None)
            os.environ.pop("GROQ_API_KEY", None)
            self.assertTrue(grok_tui_available())
            b = resolve_backend()
            self.assertIsNotNone(b)
            assert b is not None
            self.assertEqual(b.name, "grok_tui")
            desc = describe_backend()
            self.assertIn("grok_tui", desc)
            self.assertIn("preferred", desc.lower())

    def test_force_xai_still_works(self) -> None:
        os.environ["AETHER_LLM_PROVIDER"] = "xai"
        os.environ["XAI_API_KEY"] = "xai-fake"
        b = resolve_backend()
        self.assertIsNotNone(b)
        assert b is not None
        self.assertEqual(b.name, "xai")


if __name__ == "__main__":
    unittest.main()
