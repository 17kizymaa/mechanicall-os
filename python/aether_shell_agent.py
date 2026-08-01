#!/usr/bin/env python3
"""Grok-shaped agent DEFINITION loader + tool loop for aether shell.

Mirrors Grok TUI structure (from ~/.grok/README.md):
  - Agent profile (.md + YAML frontmatter tools/disallowedTools + body)
  - AGENTS.md / Claude.md project rules appended to system
  - Built-in tool IDs: read_file, grep_search, list_dir, bash, search_replace
  - Multi-turn tool loop until plain reply

Domain: CURRENT injected by caller; never auto aether approve.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

# --- defaults (Grok-shaped subset) -------------------------------------------

DEFAULT_TOOLS = (
    "read_file",
    "grep_search",
    "list_dir",
    "bash",
    "search_replace",
)

DEFAULT_DISALLOWED = (
    "web_search",
    "web_fetch",
    "Agent",
    "task",
    "memory_search",
    "use_tool",
)

AGENTS_NAMES = ("AGENTS.md", "Agents.md", "AGENT.md", "Claude.md", "CLAUDE.md")
AGENTS_CAP = 10_000  # Grok cap per file

TOOL_CALL_RE = re.compile(
    r"<tool_call>\s*(\{.*?\})\s*</tool_call>",
    re.DOTALL | re.IGNORECASE,
)

BASH_ALLOW = frozenset(
    {
        "cat",
        "head",
        "tail",
        "grep",
        "rg",
        "ls",
        "pwd",
        "touch",
        "mkdir",
        "stat",
        "wc",
        "find",
        "echo",
        "date",
        "file",
        "diff",
        "which",
        "basename",
        "dirname",
        "realpath",
        "printf",
        "tee",
        "sort",
        "uniq",
        "cut",
        "tr",
        "sed",
        "awk",
        "tree",
        "du",
        "df",
        "id",
        "uname",
        "true",
        "false",
        "test",
    }
)

BASH_DENY = frozenset(
    {
        "rm",
        "rmdir",
        "mv",
        "cp",
        "sudo",
        "bash",
        "sh",
        "zsh",
        "python",
        "python3",
        "curl",
        "wget",
        "ssh",
        "cryptsetup",
        "aether",
        "chmod",
        "chown",
        "dd",
        "kill",
    }
)


@dataclass
class AgentProfile:
    name: str = "aether-shell"
    description: str = ""
    tools: List[str] = field(default_factory=lambda: list(DEFAULT_TOOLS))
    disallowed: List[str] = field(default_factory=lambda: list(DEFAULT_DISALLOWED))
    body: str = ""
    path: Optional[Path] = None
    role: str = "real-agent"  # real-agent | peer-propose


def _parse_simple_yaml_list(block: str, key: str) -> List[str]:
    """Parse minimal frontmatter list: key:\\n  - a\\n  - b"""
    lines = block.splitlines()
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(rf"^{re.escape(key)}\s*:", line):
            rest = line.split(":", 1)[1].strip()
            if rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
                if inner:
                    out = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
                return out
            i += 1
            while i < len(lines):
                m = re.match(r"^\s*-\s+(.+)$", lines[i])
                if not m:
                    break
                out.append(m.group(1).strip().strip("'\""))
                i += 1
            return out
        i += 1
    return out


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_raw = parts[1]
    body = parts[2].lstrip("\n")
    meta: dict = {}
    for key in ("name", "description", "permissionMode", "role"):
        m = re.search(rf"^{key}\s*:\s*(.+)$", fm_raw, re.M)
        if m:
            val = m.group(1).strip().strip("'\"")
            if val == ">" or val.startswith("|"):
                # folded block — take following indented lines lightly
                continue
            meta[key] = val
    # description may be folded with >
    m = re.search(
        r"^description\s*:\s*>\s*\n((?:[ \t]+.+\n?)+)",
        fm_raw,
        re.M,
    )
    if m:
        meta["description"] = " ".join(
            ln.strip() for ln in m.group(1).splitlines() if ln.strip()
        )
    tools = _parse_simple_yaml_list(fm_raw, "tools")
    dis = _parse_simple_yaml_list(fm_raw, "disallowedTools")
    if tools:
        meta["tools"] = tools
    if dis:
        meta["disallowedTools"] = dis
    return meta, body


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def agent_role_paths() -> dict[str, Path]:
    r = repo_root() / "references"
    return {
        "grok": r / "aether-shell-agent-grok.md",
        "real": r / "aether-shell-agent-grok.md",
        "peer": r / "aether-shell-agent-peer.md",
        "personal": r / "aether-shell-agent-peer.md",
        "pll": r / "aether-shell-agent-peer.md",
        "sft": r / "aether-shell-agent-peer.md",
    }


def resolve_agent_role() -> str:
    """Return 'grok' | 'peer'.

    **Default is peer** (personal-llm proposals/synthesis + remote Ollama path).
    Grok real agent only when explicitly requested (/agent grok or ROLE=grok).
    """
    explicit = os.environ.get("AETHER_SHELL_AGENT_ROLE", "").strip().lower()
    if explicit in ("grok", "real", "agent"):
        return "grok"
    if explicit in ("peer", "personal", "pll", "sft", "personal-llm"):
        return "peer"
    # Path override (only if role not set)
    path_env = os.environ.get("AETHER_SHELL_AGENT", "").strip()
    if path_env:
        low = path_env.lower()
        if "grok" in low and "peer" not in low:
            return "grok"
        return "peer"
    # Default shape: peer (personal-llm + remote path integrated)
    return "peer"


def default_agent_path() -> Path:
    env = os.environ.get("AETHER_SHELL_AGENT", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            return p
    role = resolve_agent_role()
    paths = agent_role_paths()
    p = paths.get(role) or paths["peer"]
    if p.is_file():
        return p
    # legacy single profile
    legacy = repo_root() / "references" / "aether-shell-agent.md"
    return legacy


def load_agent_profile(path: Optional[Path] = None) -> AgentProfile:
    p = path or default_agent_path()
    if not p.is_file():
        return AgentProfile(
            body="(missing agent profile — Domain-only shell)",
            path=p,
            role="peer-propose",
        )
    text = p.read_text(encoding="utf-8", errors="replace")
    meta, body = _parse_frontmatter(text)
    role = str(meta.get("role") or "")
    if not role:
        role = "peer-propose" if "peer" in p.name else "real-agent"
    return AgentProfile(
        name=str(meta.get("name") or "aether-shell"),
        description=str(meta.get("description") or ""),
        tools=list(meta.get("tools") or DEFAULT_TOOLS),
        disallowed=list(meta.get("disallowedTools") or DEFAULT_DISALLOWED),
        body=body.strip(),
        path=p,
        role=role,
    )


def set_agent_role(role: str) -> str:
    """Pin role for this process (and hint for profile path)."""
    r = role.strip().lower()
    if r in ("grok", "real", "agent"):
        os.environ["AETHER_SHELL_AGENT_ROLE"] = "grok"
        os.environ["AETHER_SHELL_AGENT"] = str(agent_role_paths()["grok"])
        return "grok"
    if r in ("peer", "personal", "pll", "sft", "personal-llm"):
        os.environ["AETHER_SHELL_AGENT_ROLE"] = "peer"
        os.environ["AETHER_SHELL_AGENT"] = str(agent_role_paths()["peer"])
        return "peer"
    raise ValueError(f"unknown agent role {role!r} — use grok|peer")


def load_agents_md(root: Path) -> str:
    """Grok-like: walk root→… collect AGENTS.md style files (root only for strip-alpha).

    Full Grok walks every dir from repo root to cwd; we load project root + optional
    parent mechanicall AGENTS if root is a nested Domain.
    """
    chunks: List[str] = []
    candidates = [root]
    # one parent up if nested under mechanicall-os
    if root.parent != root:
        candidates.append(root.parent)
    seen: set[Path] = set()
    for base in candidates:
        try:
            b = base.resolve()
        except OSError:
            b = base
        if b in seen:
            continue
        seen.add(b)
        for name in AGENTS_NAMES:
            f = b / name
            if f.is_file():
                try:
                    t = f.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if len(t) > AGENTS_CAP:
                    t = t[:AGENTS_CAP] + "\n…(truncated)"
                chunks.append(f"## Project rules ({f})\n{t}")
                break  # one file per directory (Grok checks multiple names)
    return "\n\n".join(chunks)


def build_agent_system(
    root: Path,
    current: str,
    profile: Optional[AgentProfile] = None,
) -> str:
    prof = profile or load_agent_profile()
    parts: List[str] = []
    # Peer technique: personal-llm doctrine under Domain
    if prof.role == "peer-propose" or "peer" in (prof.name or ""):
        try:
            from aether_llm import personal_llm_system_text

            parts.append(personal_llm_system_text().strip())
            parts.append("")
        except Exception:
            pass
    parts.extend(
        [
            prof.body or "(empty agent body)",
            "",
            "## CURRENT.md (Domain — re-read this turn; sacred)",
            current
            or "(no CURRENT.md — refuse consequential claims; suggest aether current init)",
        ]
    )
    agents = load_agents_md(root)
    if agents:
        parts.extend(["", agents])
    parts.extend(
        [
            "",
            f"## Agent role: {prof.role} ({prof.name})",
            f"## Active tools: {', '.join(prof.tools) if prof.tools else '(none)'}",
            f"## Disallowed: {', '.join(prof.disallowed)}",
        ]
    )
    return "\n".join(parts)


def _safe_path(root: Path, rel: str) -> Path:
    root = root.resolve()
    raw = (rel or ".").strip() or "."
    p = (root / raw).resolve()
    if p != root and root not in p.parents:
        raise ValueError(f"path escapes project root: {rel}")
    return p


def tool_read_file(root: Path, args: dict) -> str:
    path = _safe_path(root, str(args.get("path") or args.get("target_file") or ""))
    if not path.is_file():
        return f"error: not a file: {path}"
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    offset = int(args.get("offset") or 1)
    limit = args.get("limit")
    if offset < 1:
        offset = 1
    start = offset - 1
    chunk = lines[start:]
    if limit is not None:
        chunk = chunk[: int(limit)]
    out = []
    for i, ln in enumerate(chunk, start=offset):
        out.append(f"{i}|{ln}")
    return "\n".join(out) if out else "(empty)"


def tool_list_dir(root: Path, args: dict) -> str:
    path = _safe_path(root, str(args.get("path") or "."))
    if not path.is_dir():
        return f"error: not a directory: {path}"
    names = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    lines = []
    for p in names[:500]:
        suf = "/" if p.is_dir() else ""
        lines.append(p.name + suf)
    if len(names) > 500:
        lines.append("…")
    return "\n".join(lines) if lines else "(empty)"


def tool_grep_search(root: Path, args: dict) -> str:
    pattern = str(args.get("pattern") or args.get("query") or "")
    if not pattern:
        return "error: pattern required"
    path = _safe_path(root, str(args.get("path") or "."))
    rg = _which("rg")
    if rg:
        cmd = [rg, "-n", "--no-heading", "-m", "50", pattern, str(path)]
    else:
        cmd = ["grep", "-rn", "-m", "50", "--", pattern, str(path)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(root))
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"error: {e}"
    out = (r.stdout or "") + (r.stderr or "")
    if len(out) > 12000:
        out = out[:12000] + "\n…"
    return out.strip() or "(no matches)"


def _which(cmd: str) -> Optional[str]:
    from shutil import which

    return which(cmd)


def tool_bash(root: Path, args: dict) -> str:
    command = str(args.get("command") or args.get("cmd") or "").strip()
    if not command:
        return "error: command required"
    try:
        argv = shlex.split(command)
    except ValueError as e:
        return f"error: parse: {e}"
    if not argv:
        return "error: empty argv"
    name = Path(argv[0]).name
    if name in BASH_DENY or name not in BASH_ALLOW:
        return f"error: `{name}` not allowlisted for bash tool"
    for a in argv:
        if any(c in a for c in ("|", ";", "&", "`", "\n", "$(", "${")):
            return f"error: metacharacters refused ({a!r})"
    bin_path = _which(name)
    if not bin_path:
        return f"error: `{name}` not on PATH"
    try:
        r = subprocess.run(
            [bin_path] + argv[1:],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"error: {e}"
    out = (r.stdout or "") + (r.stderr or "")
    if len(out) > 12000:
        out = out[:12000] + "\n…"
    return f"exit={r.returncode}\n{out}".rstrip()


def tool_search_replace(root: Path, args: dict) -> str:
    path = _safe_path(root, str(args.get("path") or ""))
    old = args.get("old_string")
    new = args.get("new_string")
    if old is None or new is None:
        return "error: old_string and new_string required"
    old_s, new_s = str(old), str(new)
    if not path.is_file():
        return f"error: not a file: {path}"
    text = path.read_text(encoding="utf-8", errors="replace")
    replace_all = bool(args.get("replace_all"))
    count = text.count(old_s)
    if count == 0:
        return "error: old_string not found"
    if count > 1 and not replace_all:
        return f"error: old_string found {count} times; set replace_all true or uniquify"
    path.write_text(
        text.replace(old_s, new_s) if replace_all else text.replace(old_s, new_s, 1),
        encoding="utf-8",
    )
    return f"ok: replaced {count if replace_all else 1} occurrence(s) in {path}"


TOOL_IMPL: Dict[str, Callable[[Path, dict], str]] = {
    "read_file": tool_read_file,
    "grep_search": tool_grep_search,
    "list_dir": tool_list_dir,
    "bash": tool_bash,
    "search_replace": tool_search_replace,
    # aliases
    "grep": tool_grep_search,
    "read": tool_read_file,
}


def parse_tool_call(text: str) -> Optional[dict]:
    m = TOOL_CALL_RE.search(text or "")
    if not m:
        return None
    try:
        obj = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {"error": "invalid JSON in tool_call"}
    if not isinstance(obj, dict):
        return {"error": "tool_call must be object"}
    return obj


def execute_tool(root: Path, profile: AgentProfile, call: dict) -> str:
    if call.get("error"):
        return str(call["error"])
    name = str(call.get("name") or call.get("tool") or "").strip()
    args = call.get("arguments") or call.get("args") or {}
    if not isinstance(args, dict):
        return "error: arguments must be object"
    if name in profile.disallowed or name not in profile.tools:
        # allow alias if canonical in tools
        canon = {"grep": "grep_search", "read": "read_file"}.get(name, name)
        if canon not in profile.tools or canon in profile.disallowed:
            return f"error: tool `{name}` not allowed by agent profile"
        name = canon
    impl = TOOL_IMPL.get(name)
    if not impl:
        return f"error: unknown tool `{name}`"
    try:
        return impl(root, args)
    except ValueError as e:
        return f"error: {e}"
    except OSError as e:
        return f"error: {e}"


def agent_chat_loop(
    root: Path,
    history: List[dict],
    *,
    chat_fn: Callable[..., str],
    profile: Optional[AgentProfile] = None,
    current: str = "",
    max_tool_turns: int = 8,
    temperature: float = 0.35,
) -> str:
    """Multi-turn tool loop (Grok-like). chat_fn(messages, temperature=) → text.

    Peer role: fewer tool turns, read-only tools only (enforced by profile).
    Real/grok role: full allowlisted write tools.
    """
    prof = profile or load_agent_profile()
    if len(current) > 14000:
        current = current[:14000] + "\n…"
    system = build_agent_system(root, current, prof)
    msgs: List[dict] = [{"role": "system", "content": system}]
    for m in history:
        msgs.append({"role": m["role"], "content": m["content"]})

    # Peer: short loop; real agent: more turns
    if prof.role == "peer-propose" or not prof.tools:
        max_tool_turns = min(max_tool_turns, 4)
        temperature = min(temperature, 0.4)
    else:
        max_tool_turns = max(max_tool_turns, 8)

    final = ""
    for _ in range(max_tool_turns):
        reply = chat_fn(msgs, temperature=temperature) or ""
        final = reply
        if not prof.tools:
            break
        call = parse_tool_call(reply)
        if not call:
            break
        result = execute_tool(root, prof, call)
        msgs.append({"role": "assistant", "content": reply})
        msgs.append(
            {
                "role": "user",
                "content": f"<tool_result>\n{result}\n</tool_result>\nContinue. Use another tool_call or finish in plain prose.",
            }
        )
    return final
