#!/usr/bin/env python3
"""Project Panel — Grok-left chat · CURRENT-right (sacred).

Doctrine:
  - Filesystem is sole durable truth (CURRENT.md, events.jsonl, …).
  - Left pane steals Grok TUI *chat UX* (Domain agent); right pane is always CURRENT.
  - Main board: no letter hotkeys, no preflight (preflight → Domain shell agent).
  - Advanced… keeps the full power action list (including preflight for emergencies).
  - Models never approve. Panel projects + human gates only.

See docs/PANEL-GROK-SPLIT.md.

Usage:
  aether panel [path] [--write] [--dump] [--simple]
"""
from __future__ import annotations

import argparse
import html
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List, Optional, Sequence, Tuple


# --- known operator projects (P1 switcher) -----------------------------------

# (short id, display name, candidate paths in preference order)
_KNOWN_PROJECT_SPECS: List[Tuple[str, str, Tuple[str, ...]]] = [
    ("mech", "mechanicall-os", ("~/mechanicall-os",)),
    ("pll", "personal-llm", ("~/MODEL+RAG/personal-llm,", "~/MODEL+RAG/personal-llm")),
    ("rag", "rag-archive-manager", ("~/MODEL+RAG/rag-archive-manager,", "~/MODEL+RAG/rag-archive-manager")),
    ("desk", "house-tv-desk", ("~/mechanicall-os/domains/house-tv-desk",)),
]


def known_projects() -> List[Tuple[str, str, Path]]:
    """Return (id, label, resolved path) for roots that exist on disk."""
    out: List[Tuple[str, str, Path]] = []
    for pid, label, cands in _KNOWN_PROJECT_SPECS:
        for c in cands:
            p = Path(os.path.expanduser(c)).resolve()
            if not p.is_dir():
                continue
            # Prefer trees with CURRENT or .aether (real Domain projects)
            if (p / "CURRENT.md").is_file() or (p / ".aether").is_dir():
                out.append((pid, label, p))
                break
    return out


def discover_proposes(root: Path, limit: int = 12) -> List[Path]:
    """Recent PROPOSE / SPIKE / PRESPIKE markdown under root and artifacts/."""
    root = project_root(root)
    patterns = (
        "PROPOSE*.md",
        "SPIKE*.md",
        "PRESPIKE*.md",
        "*SPIKE*.md",
        "*PROPOSE*.md",
    )
    found: List[Path] = []
    search_dirs = [root, root / "artifacts", root / "dev"]
    for d in search_dirs:
        if not d.is_dir():
            continue
        for pat in patterns:
            try:
                found.extend(d.glob(pat))
            except OSError:
                pass
    # unique, newest mtime first
    uniq: dict[str, Path] = {}
    for p in found:
        if not p.is_file():
            continue
        key = str(p.resolve())
        uniq[key] = p
    paths = list(uniq.values())

    def mtime(p: Path) -> float:
        try:
            return p.stat().st_mtime
        except OSError:
            return 0.0

    paths.sort(key=mtime, reverse=True)
    return paths[:limit]


# --- projection (shared by TUI / md / html) ---------------------------------


@dataclass
class ProjectState:
    root: Path
    has_aether: bool = False
    has_current: bool = False
    objective: str = "(unset)"
    phase: str = "(unset)"
    status: str = "(unset)"
    baseline: str = "(unset)"
    next_action: str = "(unset)"
    approval: str = "(unset)"
    prohibited: List[str] = field(default_factory=list)
    recent_events: List[str] = field(default_factory=list)
    proposes: List[Path] = field(default_factory=list)
    app_name: Optional[str] = None
    project_label: str = ""
    result: str = ""  # one-line outcome under the board
    detail: str = ""  # multi-line overlay (CURRENT / events)


_FIELD_RE = re.compile(
    r"^\*\*(?P<name>[^*]+?):?\*\*\s*:?\s*(?P<val>.*)$",
    re.IGNORECASE,
)


def project_root(path: str | Path | None = None) -> Path:
    p = Path(path or os.getcwd()).resolve()
    if p.is_file():
        p = p.parent
    return p


def _parse_current_fields(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = _FIELD_RE.match(line.strip())
        if not m:
            continue
        name = m.group("name").rstrip(":").strip().lower()
        out[name] = m.group("val").strip()
    return out


def _parse_prohibited(text: str) -> List[str]:
    items: List[str] = []
    in_sec = False
    for line in text.splitlines():
        if re.match(r"^##\s+Prohibited", line, re.I):
            in_sec = True
            continue
        if in_sec and re.match(r"^##\s+", line):
            break
        if in_sec:
            m = re.match(r"^\s*[-*]\s+(.+)$", line)
            if m:
                items.append(m.group(1).strip())
    return items


def _tail_events(events_path: Path, n: int = 10) -> List[str]:
    if not events_path.is_file():
        return []
    try:
        lines = events_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return lines[-n:]


def _label_for_root(root: Path) -> str:
    root = root.resolve()
    for _pid, label, path in known_projects():
        try:
            if path.resolve() == root:
                return label
        except OSError:
            continue
    return root.name


def load_state(root: Path) -> ProjectState:
    root = project_root(root)
    st = ProjectState(root=root)
    st.project_label = _label_for_root(root)
    st.has_aether = (root / ".aether").is_dir()
    cf = root / "CURRENT.md"
    st.has_current = cf.is_file()
    if st.has_current:
        try:
            text = cf.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            st.result = f"read CURRENT.md failed: {e}"
            return st
        fields = _parse_current_fields(text)
        st.objective = fields.get("objective", st.objective)
        st.phase = fields.get("phase", st.phase)
        st.status = fields.get("status", st.status)
        st.baseline = fields.get("baseline", st.baseline)
        st.next_action = fields.get("next", st.next_action)
        st.approval = fields.get("approval", st.approval)
        st.prohibited = _parse_prohibited(text)
    st.recent_events = _tail_events(root / ".aether" / "events.jsonl", n=10)
    st.proposes = discover_proposes(root)
    appf = root / ".aether" / "app.json"
    if appf.is_file():
        try:
            raw = appf.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'"name"\s*:\s*"([^"]*)"', raw)
            if m:
                st.app_name = m.group(1)
        except OSError:
            pass
    return st


def render_text(st: ProjectState) -> str:
    """Operator board text projection (also --dump)."""
    lines = [
        f"Operator Board (panel v0) — {st.project_label or st.root.name}",
        f"  {st.root}",
        "",
        f"  OBJECTIVE  {st.objective}",
        f"  PHASE      {st.phase}    STATUS  {st.status}",
        f"  BASELINE   {st.baseline}",
        f"  >>> NEXT   {st.next_action}",
        f"  APPROVAL   {st.approval}",
    ]
    if st.app_name:
        lines.append(f"  APP        {st.app_name}")
    lines.append("")
    lines.append("  PROHIBITED")
    if st.prohibited:
        for p in st.prohibited:
            lines.append(f"    ✗ {p}")
    else:
        lines.append("    (none listed)" if st.has_current else "    (no CURRENT.md yet)")
    lines.append("")
    lines.append("  EVENTS (tail)")
    if st.recent_events:
        for ev in st.recent_events[-8:]:
            lines.append(f"    {ev[:110]}")
    else:
        lines.append("    (none)")
    lines.append("")
    lines.append("  OPEN PROPOSE / SPIKE")
    if st.proposes:
        for i, p in enumerate(st.proposes[:8], 1):
            try:
                rel = p.relative_to(st.root)
            except ValueError:
                rel = p
            lines.append(f"    {i}. {rel}")
    else:
        lines.append("    (none found under ./ or artifacts/)")
    if st.result:
        lines.append("")
        lines.append(f"  LAST  {st.result}")
    lines.append("")
    lines.append("  Human only: Approve / Reject. Models never approve.")
    lines.append("  [s] switch project  [l] list proposes  [p] preflight Next  [a]/[x] human")
    return "\n".join(lines) + "\n"


def render_md(st: ProjectState) -> str:
    """Scaffold for editor / future GUI-friendly surface."""
    prol = (
        "\n".join(f"- `{p}`" for p in st.prohibited)
        if st.prohibited
        else "- *(none)*"
    )
    event_block = (
        "\n".join(f"    {e}" for e in st.recent_events)
        if st.recent_events
        else "    (none)"
    )
    prop_block = (
        "\n".join(f"- `{_rel(st.root, p)}`" for p in st.proposes)
        if st.proposes
        else "- *(none)*"
    )
    next_cmd = (
        st.next_action
        if st.next_action not in ("(unset)", "unset", "")
        else "<action>"
    )
    return f"""# Operator Board (panel v0)

Generated by `aether panel --write`. Safe to delete; regenerate anytime.

**Root:** `{st.root}`  
**Label:** {st.project_label}

| Field | Value |
|-------|-------|
| Objective | {st.objective} |
| Phase | {st.phase} |
| Status | {st.status} |
| Baseline | {st.baseline} |
| **Next** | `{st.next_action}` |
| Approval | {st.approval} |
| App | {st.app_name or "—"} |

## Prohibited

{prol}

## Recent events

```
{event_block}
```

## Open PROPOSE / SPIKE

{prop_block}

## Actions

```bash
aether panel
aether preflight {next_cmd}
aether approve "…"   # human only
aether reject "…"    # human only
aether current
```

> Operator board projects Domain files. Grok = AI chat. Human only for approve.
"""


def _rel(root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def render_html(st: ProjectState) -> str:
    """Scaffold for browser view later; same data as TUI."""
    prol = (
        "".join(f"<li><code>{html.escape(p)}</code></li>" for p in st.prohibited)
        or "<li><em>none</em></li>"
    )
    events = (
        "".join(f"<li><code>{html.escape(e[:200])}</code></li>" for e in st.recent_events)
        or "<li><em>none</em></li>"
    )
    props = (
        "".join(f"<li><code>{html.escape(_rel(st.root, p))}</code></li>" for p in st.proposes)
        or "<li><em>none</em></li>"
    )
    next_esc = html.escape(st.next_action)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Operator Board — {html.escape(st.project_label or str(st.root.name))}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 48rem; margin: 2rem auto; padding: 0 1rem;
         background: #0b0f14; color: #e7ecf1; }}
  h1 {{ font-size: 1.15rem; letter-spacing: 0.04em; text-transform: uppercase; color: #8b9aab; }}
  .grid {{ display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 1rem; }}
  @media (max-width: 720px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  .card {{ border: 1px solid #2a3540; border-radius: 8px; padding: 1rem 1.25rem;
           background: #141b24; }}
  .next {{ font-size: 1.5rem; font-weight: 800; color: #5eead4; margin: 0.5rem 0; }}
  .muted {{ color: #8b9aab; font-size: 0.85rem; }}
  code {{ background: #0b0f14; padding: 0.1em 0.35em; border-radius: 3px; }}
  ul {{ padding-left: 1.2rem; }}
  .human {{ border: 2px solid #fbbf24; color: #fde68a; padding: 0.75rem; border-radius: 6px; }}
  .warn {{ border-left: 3px solid #e6b84d; padding-left: 0.75rem; color: #d4c4a0; }}
</style>
</head>
<body>
  <h1>Operator Board · panel v0</h1>
  <p class="muted">{html.escape(st.project_label)} · {html.escape(str(st.root))}</p>
  <div class="grid">
    <div class="card">
      <div><strong>Objective</strong><br/>{html.escape(st.objective)}</div>
      <div class="muted">{html.escape(st.phase)} · {html.escape(st.status)} · sign-off {html.escape(st.approval)}</div>
      <p class="next">NEXT → {next_esc}</p>
      <div class="human"><strong>Human only</strong> — Approve / Reject (models never approve)</div>
      <p><strong>Prohibited</strong></p>
      <ul>{prol}</ul>
      <p><strong>Events</strong></p>
      <ul>{events}</ul>
    </div>
    <div class="card">
      <strong>PROPOSE / SPIKE</strong>
      <ul>{props}</ul>
    </div>
  </div>
  <p class="warn">Read-only scaffold. Mutations: <code>aether panel</code> / CLI. AI chat: host IDE / grok.</p>
</body>
</html>
"""


def write_projections(st: ProjectState) -> Tuple[Path, Path]:
    aether_dir = st.root / ".aether"
    aether_dir.mkdir(parents=True, exist_ok=True)
    md_path = aether_dir / "PANEL.md"
    html_path = aether_dir / "panel.html"
    md_path.write_text(render_md(st), encoding="utf-8")
    html_path.write_text(render_html(st), encoding="utf-8")
    return md_path, html_path


def _quiet_write(st: ProjectState) -> None:
    try:
        write_projections(st)
    except OSError:
        pass


# --- aether subprocess -------------------------------------------------------


def find_aether() -> str:
    env = os.environ.get("AETHER_BIN")
    if env and Path(env).is_file():
        return env
    home = os.environ.get("AETHER_HOME")
    if home:
        cand = Path(home) / "aether"
        if cand.is_file():
            return str(cand)
    here = Path(__file__).resolve().parent.parent / "aether"
    if here.is_file():
        return str(here)
    which = shutil.which("aether")
    if which:
        return which
    return "aether"


def run_aether(args: Sequence[str], root: Path, timeout: int = 120) -> Tuple[int, str]:
    cmd = [find_aether(), *args]
    aether_bin = find_aether()
    home = os.environ.get("AETHER_HOME")
    if not home:
        try:
            home = str(Path(aether_bin).resolve().parent)
        except OSError:
            home = str(Path(__file__).resolve().parent.parent)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "AETHER_HOME": home},
        )
    except FileNotFoundError:
        return 127, "aether executable not found"
    except subprocess.TimeoutExpired:
        return 124, "aether timed out"
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


# --- TUI ---------------------------------------------------------------------

Action = Tuple[str, str, str]

# Operator-first ordering: human gates + Next preflight + switcher up front

# --- TUI: Grok-left · CURRENT-right (no main hotkeys; preflight → shell / Advanced) ---

Action = Tuple[str, str, str]  # label, key, hotkey (hotkey unused on main)

# Main board: sexy dual-pane. No preflight. No letter hotkeys.
MAIN_ACTIONS: List[Action] = [
    ("Refresh", "refresh", ""),
    (">>> APPROVE (human only)", "approve", ""),
    (">>> REJECT (human only)", "reject", ""),
    ("Advanced…", "advanced", ""),
    ("Fullscreen Domain shell", "open_shell", ""),
    ("Fullscreen Grok TUI", "open_grok", ""),
    ("Edit CURRENT", "edit_current", ""),
    ("Quit", "quit", ""),
]

# Power list (was full board). Includes preflight — prefer shell agent for daily use.
ADVANCED_ACTIONS: List[Action] = [
    ("Preflight Next (prefer shell)", "preflight_next", ""),
    ("Check a specific step…", "preflight", ""),
    ("Show blocked-step demo", "demo_refuse", ""),
    ("Switch project…", "switch_project", ""),
    ("List / open PROPOSE…", "open_propose", ""),
    ("Record finished file…", "artifact", ""),
    ("Show event history", "events", ""),
    ("Write PANEL.md + html", "write", ""),
    ("Init .aether", "init", ""),
    ("Create CURRENT template", "current_init", ""),
    ("Toggle LLM preset (next)", "llm_next", ""),
    ("Pick LLM preset…", "llm_pick", ""),
    ("Help / design notes", "help", ""),
    ("Back", "advanced_back", ""),
]

# Back-compat alias used by tests / dump helpers
ACTIONS: List[Action] = list(MAIN_ACTIONS) + [
    a for a in ADVANCED_ACTIONS if a[1] not in ("advanced_back",)
]

ACTION_HELP: dict[str, str] = {
    "refresh": "Reload CURRENT.md + events from disk.",
    "approve": "Human only: aether approve.",
    "reject": "Human only: aether reject.",
    "advanced": "Power actions (preflight, switch project, presets, …).",
    "open_shell": "Fullscreen Domain shell — preflight + agents live here.",
    "open_grok": "Fullscreen raw Grok TUI (not Domain-bound).",
    "edit_current": "Open CURRENT in $EDITOR.",
    "quit": "Leave the board.",
    "preflight_next": "aether preflight <Next> — prefer shell agent day-to-day.",
    "preflight": "Check any action id.",
    "demo_refuse": "Demo a refused preflight.",
    "switch_project": "Jump among known Domain roots.",
    "open_propose": "List/open PROPOSE/SPIKE files.",
    "artifact": "Register finished file.",
    "events": "Tail events.jsonl.",
    "write": "Write PANEL.md + panel.html.",
    "init": "aether init",
    "current_init": "aether current init",
    "llm_next": "Cycle LLM preset.",
    "llm_pick": "Pick LLM preset by id.",
    "help": "Design: Grok-left chat, CURRENT-right; preflight in shell.",
    "advanced_back": "Leave Advanced menu.",
}


def _summarize_result(code: int, out: str) -> str:
    low = out.lower()
    if "refused" in low:
        tag = "REFUSED"
    elif "allowed" in low:
        tag = "ALLOWED"
    elif code == 0:
        tag = "OK"
    else:
        tag = f"exit {code}"
    one = out.replace("\n", " | ")
    if len(one) > 140:
        one = one[:137] + "…"
    return f"{tag}: {one}" if one else tag


def _prompt_line(stdscr, prompt: str) -> Optional[str]:
    import curses

    h, w = stdscr.getmaxyx()
    curses.echo()
    curses.curs_set(1)
    row = h - 1
    try:
        stdscr.move(row, 0)
        stdscr.clrtoeol()
        p = prompt[: max(1, w - 8)]
        stdscr.addstr(row, 0, p)
        stdscr.refresh()
        raw = stdscr.getstr(row, len(p), max(1, w - len(p) - 1))
    except curses.error:
        raw = b""
    curses.noecho()
    curses.curs_set(0)
    if raw is None:
        return None
    try:
        return raw.decode("utf-8", errors="replace").strip()
    except Exception:
        return str(raw).strip()


def _panel_chat(root: Path, history: List[dict], user_text: str) -> tuple[str, List[dict]]:
    """Left-pane chat: Domain agent (peer default) — Grok-shaped, CURRENT injected."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from aether_fs import read_current
        from aether_llm import chat, apply_peer_backend
        from aether_shell_agent import agent_chat_loop, set_agent_role, resolve_agent_role
    except ImportError as e:
        return f"(chat unavailable: {e})", history

    try:
        if resolve_agent_role() != "grok":
            set_agent_role("peer")
            apply_peer_backend(root)
    except Exception:
        pass

    history = list(history)
    history.append({"role": "user", "content": user_text})
    try:
        cur = read_current(root) or ""
        reply = agent_chat_loop(
            root,
            history[-16:],
            chat_fn=chat,
            current=cur,
            temperature=0.35,
        )
    except Exception as e:
        history.pop()
        return f"(llm error: {e})", history
    history.append({"role": "assistant", "content": reply or ""})
    return reply or "(empty)", history


def _wrap(text: str, width: int) -> List[str]:
    if width < 8:
        width = 8
    lines: List[str] = []
    for para in (text or "").splitlines() or [""]:
        while len(para) > width:
            lines.append(para[:width])
            para = para[width:]
        lines.append(para)
    return lines


def _draw_split(
    stdscr,
    st: ProjectState,
    *,
    chat_lines: List[str],
    chat_scroll: int,
    current_scroll: int,
    menu: List[Action],
    selected: int,
    focus: str,
    input_buf: str,
    status: str,
) -> None:
    """Sexy dual pane: left chat (Grok-like), right CURRENT always."""
    import curses

    if not hasattr(_draw_split, "_color"):
        _draw_split._color = False  # type: ignore[attr-defined]
        try:
            if curses.has_colors():
                curses.start_color()
                curses.use_default_colors()
                curses.init_pair(1, curses.COLOR_CYAN, -1)
                curses.init_pair(2, curses.COLOR_GREEN, -1)
                curses.init_pair(3, curses.COLOR_MAGENTA, -1)
                curses.init_pair(4, curses.COLOR_YELLOW, -1)
                curses.init_pair(5, curses.COLOR_RED, -1)
                curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
                curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
                _draw_split._color = True  # type: ignore[attr-defined]
        except curses.error:
            pass

    def c(n: int) -> int:
        if not getattr(_draw_split, "_color", False):
            return 0
        try:
            return curses.color_pair(n)
        except curses.error:
            return 0

    h, w = stdscr.getmaxyx()
    stdscr.erase()
    if h < 12 or w < 40:
        try:
            stdscr.addstr(0, 0, "resize terminal (min ~12x40)")
        except curses.error:
            pass
        stdscr.refresh()
        return

    # geometry: left chat ~58%, right CURRENT ~42%, bottom menu+input
    menu_h = 3
    input_h = 2
    top_h = 1
    body_h = h - menu_h - input_h - top_h - 1
    if body_h < 4:
        body_h = 4
    left_w = max(20, int(w * 0.58))
    right_w = w - left_w - 1
    if right_w < 16:
        right_w = 16
        left_w = w - right_w - 1

    # top bar
    title = f"  MECHANICALL  ·  Grok-left  ·  CURRENT-right  ·  {st.project_label or st.root.name}"
    try:
        stdscr.attron(c(6) | curses.A_BOLD)
        stdscr.addnstr(0, 0, title.ljust(w)[: w - 1], w - 1)
        stdscr.attroff(c(6) | curses.A_BOLD)
    except curses.error:
        pass

    # headers
    try:
        lf = "▌ CHAT" if focus == "chat" else "  CHAT"
        rf = "▌ CURRENT" if focus == "current" else "  CURRENT"
        stdscr.attron(c(1) | (curses.A_BOLD if focus == "chat" else 0))
        stdscr.addnstr(1, 0, lf.ljust(left_w)[:left_w], left_w)
        stdscr.attroff(c(1) | curses.A_BOLD)
        stdscr.addnstr(1, left_w, "│", 1)
        stdscr.attron(c(3) | (curses.A_BOLD if focus == "current" else 0))
        stdscr.addnstr(1, left_w + 1, rf.ljust(right_w)[:right_w], right_w)
        stdscr.attroff(c(3) | curses.A_BOLD)
    except curses.error:
        pass

    # left chat body
    view_h = body_h - 1
    vis = chat_lines[chat_scroll : chat_scroll + view_h]
    for i in range(view_h):
        row = 2 + i
        try:
            if i < len(vis):
                line = vis[i][: left_w - 1]
                attr = c(2) if line.startswith("you ") or line.startswith("you│") else 0
                if line.startswith("agent") or line.startswith("◆"):
                    attr = c(1)
                stdscr.addnstr(row, 0, line.ljust(left_w - 1)[: left_w - 1], left_w - 1, attr)
            else:
                stdscr.addnstr(row, 0, " " * (left_w - 1), left_w - 1)
            stdscr.addnstr(row, left_w, "│", 1, c(1))
        except curses.error:
            pass

    # right CURRENT body
    cur_text = ""
    cf = st.root / "CURRENT.md"
    if cf.is_file():
        try:
            cur_text = cf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            cur_text = "(unreadable CURRENT.md)"
    else:
        cur_text = "(no CURRENT.md — Advanced → Create CURRENT)"
    # pin strip
    pin = f"Next: {st.next_action}  ·  {st.phase}/{st.status}"
    cur_lines = _wrap(pin + "\n" + "─" * max(8, right_w - 2) + "\n" + cur_text, right_w - 2)
    vis_c = cur_lines[current_scroll : current_scroll + view_h]
    for i in range(view_h):
        row = 2 + i
        try:
            if i < len(vis_c):
                stdscr.addnstr(
                    row,
                    left_w + 1,
                    vis_c[i].ljust(right_w - 1)[: right_w - 1],
                    right_w - 1,
                    c(3) if i == 0 else 0,
                )
            else:
                stdscr.addnstr(row, left_w + 1, " " * (right_w - 1), right_w - 1)
        except curses.error:
            pass

    # menu bar
    menu_row = 2 + view_h
    try:
        stdscr.attron(c(7) if focus == "menu" else c(1))
        stdscr.addnstr(menu_row, 0, " ACTIONS ".center(w - 1, "─")[: w - 1], w - 1)
        stdscr.attroff(c(7) if focus == "menu" else c(1))
    except curses.error:
        pass
    # menu items as pills on one/two lines
    x = 1
    row = menu_row + 1
    for i, (label, _k, _h) in enumerate(menu):
        pill = f" {label} "
        if x + len(pill) >= w - 1:
            row += 1
            x = 1
            if row >= h - input_h:
                break
        attr = curses.A_REVERSE | c(6) if (focus == "menu" and i == selected) else c(1)
        try:
            stdscr.addnstr(row, x, pill[: w - x - 1], w - x - 1, attr)
        except curses.error:
            pass
        x += len(pill) + 1

    # input
    in_row = h - 2
    try:
        hint = {
            "chat": "type · Enter send · Tab focus",
            "menu": "←→/↑↓ select · Enter run · Tab",
            "current": "↑↓ scroll CURRENT · Tab",
        }.get(focus, "")
        bar = f" {focus.upper()} │ {hint}"
        stdscr.attron(c(4))
        stdscr.addnstr(in_row, 0, bar.ljust(w - 1)[: w - 1], w - 1)
        stdscr.attroff(c(4))
        prompt = "› "
        shown = (prompt + input_buf)[: w - 2]
        if focus == "chat":
            stdscr.attron(curses.A_BOLD)
        stdscr.addnstr(h - 1, 0, shown.ljust(w - 1)[: w - 1], w - 1)
        if focus == "chat":
            stdscr.attroff(curses.A_BOLD)
    except curses.error:
        pass

    # status flash
    if status:
        try:
            stdscr.addnstr(h - 3, 0, status[: w - 1].ljust(w - 1)[: w - 1], w - 1, c(4))
        except curses.error:
            pass

    stdscr.refresh()


def _build_chat_display(history: List[dict], width: int) -> List[str]:
    lines: List[str] = []
    if not history:
        lines.extend(
            _wrap(
                "◆ Domain chat (Grok-shaped left pane)\n"
                "CURRENT always on the right.\n"
                "Preflight lives in Domain shell — Advanced if you must.\n"
                "Tab cycles focus · type to talk.",
                width,
            )
        )
        return lines
    for m in history[-40:]:
        role = m.get("role") or ""
        content = (m.get("content") or "").strip()
        if role == "user":
            prefix = "you │ "
        else:
            prefix = "◆   │ "
        for i, wl in enumerate(_wrap(content, max(8, width - len(prefix)))):
            lines.append((prefix if i == 0 else "    │ ") + wl)
        lines.append("")
    return lines


def run_tui_curses(root: Path) -> int:
    import curses

    st = load_state(root)
    history: List[dict] = []
    focus = "chat"  # chat | menu | current
    selected = 0
    input_buf = ""
    chat_scroll = 0
    current_scroll = 0
    status = f"Next={st.next_action}  ·  preflight → shell  ·  docs/PANEL-GROK-SPLIT.md"
    advanced_mode = False

    def main(stdscr) -> None:
        nonlocal st, history, focus, selected, input_buf, chat_scroll, current_scroll, status, advanced_mode
        curses.curs_set(1)
        stdscr.keypad(True)
        stdscr.meta(True)

        while True:
            if st.detail and not advanced_mode:
                # one-shot overlay
                h, w = stdscr.getmaxyx()
                stdscr.erase()
                for i, line in enumerate(st.detail.splitlines()[: h - 2]):
                    try:
                        stdscr.addnstr(i, 0, line[: w - 1], w - 1)
                    except curses.error:
                        pass
                try:
                    stdscr.addnstr(h - 1, 0, "[any key → board]"[: w - 1], w - 1)
                except curses.error:
                    pass
                stdscr.refresh()
                stdscr.getch()
                st.detail = ""
                continue

            menu = ADVANCED_ACTIONS if advanced_mode else MAIN_ACTIONS
            if selected >= len(menu):
                selected = max(0, len(menu) - 1)

            h, w = stdscr.getmaxyx()
            left_w = max(20, int(w * 0.58))
            chat_lines = _build_chat_display(history, left_w - 4)
            max_chat_scroll = max(0, len(chat_lines) - max(1, h - 10))
            if chat_scroll > max_chat_scroll:
                chat_scroll = max_chat_scroll

            _draw_split(
                stdscr,
                st,
                chat_lines=chat_lines,
                chat_scroll=chat_scroll,
                current_scroll=current_scroll,
                menu=menu,
                selected=selected,
                focus=focus,
                input_buf=input_buf,
                status=status,
            )

            ch = stdscr.getch()

            # Tab cycles focus
            if ch in (9,):
                order = ["chat", "menu", "current"]
                focus = order[(order.index(focus) + 1) % 3]
                curses.curs_set(1 if focus == "chat" else 0)
                continue

            if ch in (27,):  # Esc: leave advanced or quit confirm via menu
                if advanced_mode:
                    advanced_mode = False
                    selected = 0
                    status = "left Advanced"
                    continue
                # ignore esc on main (use Quit)
                continue

            if focus == "current":
                if ch in (curses.KEY_UP, ord("k")):
                    current_scroll = max(0, current_scroll - 1)
                elif ch in (curses.KEY_DOWN, ord("j")):
                    current_scroll += 1
                elif ch in (curses.KEY_PPAGE,):
                    current_scroll = max(0, current_scroll - 10)
                elif ch in (curses.KEY_NPAGE,):
                    current_scroll += 10
                continue

            if focus == "menu":
                if ch in (curses.KEY_LEFT, curses.KEY_UP):
                    selected = (selected - 1) % len(menu)
                    continue
                if ch in (curses.KEY_RIGHT, curses.KEY_DOWN):
                    selected = (selected + 1) % len(menu)
                    continue
                if ch in (curses.KEY_ENTER, 10, 13):
                    key = menu[selected][1]
                    if key == "advanced":
                        advanced_mode = True
                        selected = 0
                        status = "Advanced — preflight & power tools (prefer shell for daily preflight)"
                        continue
                    if key == "advanced_back":
                        advanced_mode = False
                        selected = 0
                        continue
                    if key == "quit":
                        return
                    if key == "help":
                        st.detail = (
                            "Panel design (docs/PANEL-GROK-SPLIT.md)\n\n"
                            "LEFT  = Grok-shaped Domain chat (peer agent default)\n"
                            "RIGHT = CURRENT.md always\n"
                            "Preflight = Domain shell agent (or Advanced)\n"
                            "No letter hotkeys on main — Tab / arrows / Enter / type\n"
                        )
                        continue

                    def prompt(p: str) -> Optional[str]:
                        return _prompt_line(stdscr, p)

                    st = _run_action(st, key, prompt, stdscr=stdscr)
                    status = st.result or status
                    st = load_state(st.root)
                    continue
                continue

            # focus == chat
            if ch in (curses.KEY_UP,):
                chat_scroll = max(0, chat_scroll - 1)
                continue
            if ch in (curses.KEY_DOWN,):
                chat_scroll += 1
                continue
            if ch in (curses.KEY_BACKSPACE, 127, 8):
                input_buf = input_buf[:-1]
                continue
            if ch in (curses.KEY_ENTER, 10, 13):
                text = input_buf.strip()
                input_buf = ""
                if not text:
                    continue
                status = "thinking…"
                _draw_split(
                    stdscr,
                    st,
                    chat_lines=_build_chat_display(history, left_w - 4),
                    chat_scroll=chat_scroll,
                    current_scroll=current_scroll,
                    menu=menu,
                    selected=selected,
                    focus=focus,
                    input_buf="",
                    status=status,
                )
                reply, history = _panel_chat(st.root, history, text)
                status = "ready"
                # auto-scroll chat to end
                chat_lines = _build_chat_display(history, left_w - 4)
                chat_scroll = max(0, len(chat_lines) - max(1, h - 10))
                st = load_state(st.root)
                continue
            # printable
            if 32 <= ch < 127:
                input_buf += chr(ch)

    curses.wrapper(main)
    return 0


def run_tui_simple(root: Path) -> int:
    """Fallback menu — still no letter hotkeys; numbers only. Preflight in Advanced."""
    st = load_state(root)
    history: List[dict] = []
    advanced = False
    while True:
        sys.stdout.write("\n" + "═" * 64 + "\n")
        sys.stdout.write("MECHANICALL panel · Grok-left chat · CURRENT-right\n")
        sys.stdout.write(f"Next: {st.next_action}  ·  preflight → shell\n")
        sys.stdout.write("─" * 64 + "\n")
        cf = root / "CURRENT.md"
        if cf.is_file():
            sys.stdout.write(cf.read_text(encoding="utf-8", errors="replace")[:1200])
            sys.stdout.write("\n")
        sys.stdout.write("─" * 64 + "\n")
        menu = ADVANCED_ACTIONS if advanced else MAIN_ACTIONS
        sys.stdout.write("Actions (number + Enter — no hotkeys):\n")
        for i, (label, _, _) in enumerate(menu, 1):
            sys.stdout.write(f"  {i}) {label}\n")
        sys.stdout.write("  t) type a chat line to Domain peer agent\n")
        sys.stdout.write("Choice: ")
        sys.stdout.flush()
        try:
            choice = sys.stdin.readline()
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            return 0
        if not choice:
            return 0
        choice = choice.strip()
        if choice.lower() in ("q", "quit"):
            return 0
        if choice.lower() == "t":
            sys.stdout.write("you › ")
            sys.stdout.flush()
            line = sys.stdin.readline()
            if line and line.strip():
                reply, history = _panel_chat(root, history, line.strip())
                sys.stdout.write(f"\n◆ {reply}\n")
            st = load_state(root)
            continue
        if not choice.isdigit():
            st.result = "enter a number, t for chat, or q"
            continue
        idx = int(choice) - 1
        if not (0 <= idx < len(menu)):
            continue
        key = menu[idx][1]
        if key == "advanced":
            advanced = True
            continue
        if key == "advanced_back":
            advanced = False
            continue
        if key == "quit":
            return 0

        def prompt(p: str) -> Optional[str]:
            sys.stdout.write(p)
            sys.stdout.flush()
            line = sys.stdin.readline()
            if line == "":
                return None
            return line.strip()

        st = _run_action(st, key, prompt, stdscr=None)
        if st.detail:
            sys.stdout.write("\n" + st.detail + "\n")
            sys.stdout.write("[Enter] ")
            sys.stdout.flush()
            sys.stdin.readline()
            st.detail = ""
        st = load_state(st.root)
    return 0


def run_tui(root: Path) -> int:
    """Fullscreen dual-pane TUI (not a CLI menu)."""
    # Prefer dedicated TUI module (real alt-screen app)
    try:
        import aether_panel_tui as tui

        return tui.run_fullscreen_tui(root, sys.modules[__name__])
    except Exception as e:
        sys.stderr.write(f"aether panel: TUI module failed ({e}); trying legacy curses\n")
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        sys.stderr.write(
            "aether panel: need a real interactive terminal for the TUI.\n"
            "  Run inside a terminal (not a pipe):\n"
            "    aether panel .\n"
            "  Text dump: aether panel --dump\n"
            "  Real Grok left + CURRENT right (tmux):\n"
            "    aether panel --grok-split .\n"
        )
        return 1
    try:
        import curses  # noqa: F401

        return run_tui_curses(root)
    except Exception as e:
        sys.stderr.write(
            f"aether panel: fullscreen TUI failed ({e})\n"
            "  Retry in a larger terminal, or: aether panel --simple\n"
            "  Or steal real Grok: aether panel --grok-split\n"
        )
        return 2


# --- main --------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Mechanicall Panel TUI — Grok-left chat · CURRENT-right"
    )
    ap.add_argument("path", nargs="?", default=".", help="project root")
    ap.add_argument("--write", action="store_true", help="write .aether/PANEL.md and panel.html")
    ap.add_argument("--dump", action="store_true", help="print text projection and exit")
    ap.add_argument(
        "--simple",
        action="store_true",
        help="legacy numbered CLI menu (not the TUI)",
    )
    ap.add_argument(
        "--grok-split",
        action="store_true",
        help="tmux: real Grok TUI left + live CURRENT right (steal Grok layout)",
    )
    ap.add_argument(
        "--list-projects",
        action="store_true",
        help="list known switcher projects and exit",
    )
    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.list_projects:
        for i, (pid, label, path) in enumerate(known_projects(), 1):
            sys.stdout.write(f"{i}) [{pid}] {label}\n    {path}\n")
        return 0

    root = project_root(args.path)
    if args.dump:
        sys.stdout.write(render_text(load_state(root)))
        return 0
    if args.write:
        st = load_state(root)
        md_p, html_p = write_projections(st)
        sys.stdout.write(f"wrote {md_p}\nwrote {html_p}\n")
        return 0
    if args.grok_split:
        import aether_panel_tui as tui

        return tui.run_tmux_grok_split(root)
    if args.simple:
        sys.stderr.write("aether panel: --simple is legacy CLI menu (not TUI)\n")
        return run_tui_simple(root)
    return run_tui(root)


if __name__ == "__main__":
    sys.exit(main())
