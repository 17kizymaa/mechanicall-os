"""Tests for Grok-shaped aether shell agent DEFINITION + tools."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from aether_shell_agent import (  # noqa: E402
    build_agent_system,
    execute_tool,
    load_agent_profile,
    load_agents_md,
    parse_tool_call,
    tool_bash,
    tool_read_file,
)


def test_load_dual_profiles():
    grok = load_agent_profile(ROOT / "references" / "aether-shell-agent-grok.md")
    assert grok.name == "aether-shell-grok"
    assert "search_replace" in grok.tools
    assert grok.role == "real-agent"
    peer = load_agent_profile(ROOT / "references" / "aether-shell-agent-peer.md")
    assert peer.name == "aether-shell-peer"
    assert peer.role == "peer-propose"
    assert "search_replace" not in peer.tools
    assert "bash" not in peer.tools
    assert "read_file" in peer.tools
    assert "web_search" in peer.disallowed


def test_parse_tool_call():
    text = 'thinking\n<tool_call>\n{"name":"list_dir","arguments":{"path":"."}}\n</tool_call>\n'
    c = parse_tool_call(text)
    assert c and c["name"] == "list_dir"


def test_tools_under_root(tmp_path: Path):
    (tmp_path / "f.txt").write_text("hello\nworld\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# rules\nBe brief.\n", encoding="utf-8")
    out = tool_read_file(tmp_path, {"path": "f.txt"})
    assert "1|hello" in out
    out = tool_bash(tmp_path, {"command": "cat f.txt"})
    assert "hello" in out
    out = tool_bash(tmp_path, {"command": "rm f.txt"})
    assert "error" in out.lower() or "allow" in out.lower()
    prof = load_agent_profile(ROOT / "references" / "aether-shell-agent-grok.md")
    r = execute_tool(
        tmp_path,
        prof,
        {"name": "search_replace", "arguments": {"path": "f.txt", "old_string": "hello", "new_string": "hi"}},
    )
    assert "ok" in r
    assert "hi" in (tmp_path / "f.txt").read_text(encoding="utf-8")
    sys_txt = build_agent_system(tmp_path, "**Next:** t\n", prof)
    assert "Be brief" in sys_txt or "rules" in sys_txt
    assert "Next" in sys_txt
    assert load_agents_md(tmp_path)


def test_escape_root(tmp_path: Path):
    prof = load_agent_profile(ROOT / "references" / "aether-shell-agent-grok.md")
    r = execute_tool(
        tmp_path,
        prof,
        {"name": "read_file", "arguments": {"path": "../../etc/passwd"}},
    )
    assert "error" in r.lower() or "escape" in r.lower()
