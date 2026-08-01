#!/usr/bin/env python3
"""Filesystem helpers for aether panel / shell (shared).

Extracted from former aether_desk — desk product removed as unsacred.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def project_root(path: str | Path | None = None) -> Path:
    p = Path(path or os.getcwd()).resolve()
    if p.is_file():
        p = p.parent
    return p


def load_dotenv_files() -> None:
    """Load keys without requiring python-dotenv. Never print values."""
    candidates = [
        Path.home() / "Desktop" / ".env",
        Path.home() / ".env",
        project_root() / ".env",
        Path("/etc/chat.env"),
        Path("/root/.chat.env"),
    ]
    for path in candidates:
        try:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line and not line.startswith("sk-") and not line.startswith("gsk_"):
                k, _, v = line.partition("=")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and v and k not in os.environ:
                    os.environ[k] = v
                continue
            if line.startswith("sk-or-") and "OPENROUTER_API_KEY" not in os.environ:
                os.environ["OPENROUTER_API_KEY"] = line
            elif line.startswith("gsk_") and "GROQ_API_KEY" not in os.environ:
                os.environ["GROQ_API_KEY"] = line
            elif line.startswith("xai-") and "XAI_API_KEY" not in os.environ:
                os.environ["XAI_API_KEY"] = line
            elif line.startswith("sk-ant-") and "ANTHROPIC_API_KEY" not in os.environ:
                os.environ["ANTHROPIC_API_KEY"] = line
            elif line.startswith("ghp_") and "GITHUB_TOKEN" not in os.environ:
                os.environ["GITHUB_TOKEN"] = line

    if os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("AETHER_LLM_PROVIDER"):
        os.environ.setdefault("AETHER_LLM_PROVIDER", "openrouter")
        os.environ.setdefault("AETHER_MODEL", "openrouter/free")


def read_current(root: Path) -> Optional[str]:
    cf = root / "CURRENT.md"
    if not cf.is_file():
        return None
    try:
        return cf.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
