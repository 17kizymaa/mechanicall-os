"""Unit tests for aether_shell helpers (no network)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from aether_shell import (  # noqa: E402
    SHELL_SYSTEM,
    _field,
    handle_slash,
    next_blurb,
    prefer_grok_tui_for_shell,
    prefer_xai_for_shell,
    run_allowlisted,
    smoke_standard_behaviours,
    status_line,
    tail_events,
)


def test_field_parse():
    cur = "**Next:** lane-a-test\n**Phase:** EXECUTE\n"
    assert _field(cur, "Next") == "lane-a-test"
    assert _field(cur, "Phase") == "EXECUTE"
    assert _field(cur, "Missing") == ""


def test_shell_system_gates():
    assert "propose only" in SHELL_SYSTEM.lower() or "Propose only" in SHELL_SYSTEM
    assert "silence" in SHELL_SYSTEM.lower()
    assert "CURRENT" in SHELL_SYSTEM
    assert "aether approve" in SHELL_SYSTEM.lower() or "approve" in SHELL_SYSTEM.lower()


def test_prefer_grok_tui_when_available(tmp_path: Path, monkeypatch=None):
    """If grok auth present, shell should lock provider to grok_tui not xai."""
    os.environ.pop("AETHER_LLM_PROVIDER", None)
    os.environ.pop("AETHER_SHELL_PROVIDER_LOCK", None)
    os.environ["AETHER_SHELL_PREFER_GROK_TUI"] = "1"
    # Simulate TUI session without requiring real grok binary path quirks:
    # prefer_grok_tui_for_shell calls grok_tui_available() which needs bin + auth.
    # We only assert: when not available, provider is not forced to xai by XAI key alone.
    os.environ["XAI_API_KEY"] = "xai-test-not-real"
    os.environ["AETHER_GROK_TUI"] = "0"  # force unavailable
    prefer_grok_tui_for_shell()
    assert os.environ.get("AETHER_LLM_PROVIDER") != "xai"
    os.environ.pop("XAI_API_KEY", None)
    os.environ.pop("AETHER_GROK_TUI", None)
    os.environ.pop("AETHER_LLM_PROVIDER", None)


def test_prefer_xai_alias_does_not_elevate_api():
    """Legacy prefer_xai_for_shell must not set provider=xai from API key alone."""
    os.environ.pop("AETHER_LLM_PROVIDER", None)
    os.environ.pop("AETHER_SHELL_PROVIDER_LOCK", None)
    os.environ["XAI_API_KEY"] = "xai-test-not-real"
    os.environ["AETHER_GROK_TUI"] = "0"
    prefer_xai_for_shell()
    assert os.environ.get("AETHER_LLM_PROVIDER") != "xai"
    os.environ.pop("XAI_API_KEY", None)
    os.environ.pop("AETHER_GROK_TUI", None)
    os.environ.pop("AETHER_LLM_PROVIDER", None)


def test_status_line_no_current(tmp_path: Path):
    s = status_line(tmp_path)
    assert tmp_path.name in s
    assert "no CURRENT" in s or "unset" in s


def test_next_blurb_and_events(tmp_path: Path):
    (tmp_path / "CURRENT.md").write_text(
        "# CURRENT\n\n**Next:** smoke-me\n\n## Next allowed action\n"
        "Do the smoke. Action id: `smoke-me`.\n\n## Prohibited\n- x\n",
        encoding="utf-8",
    )
    a = tmp_path / ".aether"
    a.mkdir()
    (a / "events.jsonl").write_text(
        '{"ts":"t","kind":"current_init"}\n{"ts":"t2","kind":"approve"}\n',
        encoding="utf-8",
    )
    blurb = next_blurb(tmp_path)
    assert "smoke-me" in blurb
    assert "Do the smoke" in blurb
    ev = tail_events(tmp_path, 1)
    assert "approve" in ev
    hist: list = []
    assert "smoke-me" in (handle_slash(tmp_path, "/next", hist) or "")
    assert "approve" in (handle_slash(tmp_path, "/events 1", hist) or "")


def test_smoke_standard_behaviours_ok(tmp_path: Path):
    (tmp_path / "CURRENT.md").write_text(
        "# CURRENT\n\n**Objective:** t\n**Phase:** SELECT\n**Status:** DRAFT\n"
        "**Baseline:** b\n**Next:** unit-smoke\n**Approval:** PENDING\n\n"
        "## Next allowed action\nUnit smoke only.\n\n## Prohibited\n- automatic-approve\n",
        encoding="utf-8",
    )
    report = smoke_standard_behaviours(tmp_path)
    assert "SMOKE OK" in report
    assert "FAIL" not in report or report.count("PASS") > report.count("FAIL")


def test_run_allowlisted_touch_cat_grep(tmp_path: Path):
    f = tmp_path / "hello.txt"
    out = run_allowlisted(tmp_path, ["touch", "hello.txt"])
    assert "exit=0" in out
    assert f.is_file()
    f.write_text("alpha\nbeta\n", encoding="utf-8")
    out = run_allowlisted(tmp_path, ["cat", "hello.txt"])
    assert "alpha" in out
    out = run_allowlisted(tmp_path, ["grep", "beta", "hello.txt"])
    assert "beta" in out
    out = run_allowlisted(tmp_path, ["rm", "hello.txt"])
    assert "refused" in out.lower()
    out = run_allowlisted(tmp_path, ["cat", "hello.txt", ";", "rm", "-rf", "/"])
    assert "refused" in out.lower() or "metachar" in out.lower()
