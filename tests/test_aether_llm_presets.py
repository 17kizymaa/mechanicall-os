#!/usr/bin/env python3
"""Unit tests for toggleable LLM presets (no network)."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_llm import (  # noqa: E402
    LLM_PRESETS,
    PRESET_CYCLE,
    apply_preset,
    cycle_preset,
    current_preset_name,
    format_presets_help,
    list_presets,
    load_preset_from_project,
    normalize_preset_name,
    save_preset_to_project,
)


class TestPresets(unittest.TestCase):
    def setUp(self) -> None:
        self._keys = [
            "AETHER_LLM_PRESET",
            "AETHER_LLM_PROVIDER",
            "AETHER_MODEL",
            "AETHER_OLLAMA_MODEL",
            "AETHER_SHELL_PROVIDER_LOCK",
            "OPENROUTER_API_KEY",
            "ANTHROPIC_API_KEY",
            "XAI_API_KEY",
            "GROQ_API_KEY",
            "AETHER_GROK_TUI",
        ]
        self._saved = {k: os.environ.get(k) for k in self._keys}
        for k in self._keys:
            os.environ.pop(k, None)
        os.environ["AETHER_GROK_TUI"] = "0"

    def tearDown(self) -> None:
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_cycle_order_starts_with_coding(self) -> None:
        self.assertEqual(PRESET_CYCLE[0], "coding")
        self.assertIn("sonnet35", PRESET_CYCLE)
        self.assertIn("ollama", PRESET_CYCLE)

    def test_normalize_aliases(self) -> None:
        self.assertEqual(normalize_preset_name("code"), "coding")
        self.assertEqual(normalize_preset_name("sonnet-3.5"), "sonnet35")
        self.assertEqual(normalize_preset_name("local"), "ollama")
        self.assertEqual(normalize_preset_name("tui"), "grok_tui")

    def test_apply_coding(self) -> None:
        os.environ["OPENROUTER_API_KEY"] = "sk-or-test"
        msg = apply_preset("coding")
        self.assertIn("coding", msg)
        self.assertEqual(os.environ.get("AETHER_LLM_PROVIDER"), "openrouter")
        self.assertIn("coder", os.environ.get("AETHER_MODEL", "").lower())
        self.assertEqual(current_preset_name(), "coding")

    def test_apply_sonnet35(self) -> None:
        apply_preset("sonnet35")
        self.assertEqual(os.environ.get("AETHER_LLM_PROVIDER"), "openrouter")
        self.assertIn("3.5", os.environ.get("AETHER_MODEL", ""))

    def test_apply_ollama(self) -> None:
        apply_preset("ollama")
        self.assertEqual(os.environ.get("AETHER_LLM_PROVIDER"), "ollama")
        self.assertEqual(current_preset_name(), "ollama")

    def test_cycle_next(self) -> None:
        apply_preset("coding")
        cycle_preset(+1)
        self.assertEqual(current_preset_name(), "coding_alt")

    def test_list_and_help(self) -> None:
        rows = list_presets()
        ids = [r[0] for r in rows]
        self.assertIn("coding", ids)
        self.assertIn("sonnet35", ids)
        self.assertIn("ollama", ids)
        help_txt = format_presets_help("coding")
        self.assertIn("coding", help_txt)
        self.assertIn("▶", help_txt)

    def test_project_persist(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            apply_preset("sonnet35")
            path = save_preset_to_project(root)
            self.assertTrue(path.is_file())
            self.assertEqual(path.read_text().strip(), "sonnet35")
            os.environ.pop("AETHER_LLM_PRESET", None)
            os.environ.pop("AETHER_LLM_PROVIDER", None)
            os.environ.pop("AETHER_MODEL", None)
            msg = load_preset_from_project(root)
            self.assertIsNotNone(msg)
            self.assertEqual(current_preset_name(), "sonnet35")

    def test_all_presets_defined(self) -> None:
        for pid in PRESET_CYCLE:
            self.assertIn(pid, LLM_PRESETS)


if __name__ == "__main__":
    unittest.main()
