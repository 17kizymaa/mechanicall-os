#!/usr/bin/env python3
"""Operator Board (Project Panel v0) — hardcore TUI over aether authority.

Doctrine:
  - Filesystem is sole durable truth (CURRENT.md, events.jsonl, …).
  - This module only *projects* state and shells out to `aether` for mutations.
  - Models never approve. Panel is optional Interface Layer, not a second control plane.
  - Same projection powers TUI now; .md / .html scaffolds for later GUI-friendly surfaces.

Operator board v0 (pre-spike P0/P1):
  - Always-on CURRENT summary · Next · Prohibited · events · Approve/Reject
  - Project switcher (known SOT roots)
  - Split view: status | open PROPOSE-*/SPIKE*/PRESPIKE* artifacts
  - Keyboard-first; `--simple` kept for broken TTY

Usage:
  python3 python/aether_panel.py [path]
  python3 python/aether_panel.py [path] --write
  python3 python/aether_panel.py [path] --dump
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
ACTIONS: List[Action] = [
    ("Refresh board", "refresh", "r"),
    ("Preflight Next (allowed step)", "preflight_next", "p"),
    (">>> APPROVE (human only)", "approve", "a"),
    (">>> REJECT (human only)", "reject", "x"),
    ("Switch project…", "switch_project", "s"),
    ("List / open PROPOSE…", "open_propose", "l"),
    ("Check a specific step…", "preflight", "f"),
    ("Show blocked-step demo", "demo_refuse", "d"),
    ("Record finished file…", "artifact", "t"),
    ("Show CURRENT.md", "show_current", "c"),
    ("Show event history", "events", "e"),
    ("Edit CURRENT.md", "edit_current", "o"),
    ("Write PANEL.md + html", "write", "w"),
    ("Init .aether", "init", "i"),
    ("Create CURRENT template", "current_init", "n"),
    ("Open Grok here", "open_grok", "g"),
    ("Help", "help", "?"),
    ("Quit", "quit", "q"),
]

ACTION_HELP: dict[str, str] = {
    "refresh": "Reload CURRENT.md + events + proposes from disk.",
    "preflight_next": "aether preflight <Next> — allow/refuse only.",
    "approve": "Human only: aether approve. Models must never do this.",
    "reject": "Human only: aether reject.",
    "switch_project": "Jump among mechanicall-os, personal-llm, rag, house-tv-desk.",
    "open_propose": "List recent PROPOSE-/SPIKE-/PRESPIKE- files; open one in $EDITOR.",
    "preflight": "Check any action id you type.",
    "demo_refuse": "Show a refused preflight using first Prohibited item.",
    "artifact": "Register a finished file via aether artifact.",
    "show_current": "Full CURRENT.md overlay.",
    "events": "Tail of .aether/events.jsonl.",
    "edit_current": "Open CURRENT in $EDITOR then return.",
    "write": "Write .aether/PANEL.md + panel.html.",
    "init": "aether init",
    "current_init": "aether current init",
    "open_grok": "Suspend board, run grok, return.",
    "help": "This list.",
    "quit": "Leave the board.",
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


def _draw_curses(stdscr, st: ProjectState, selected: int) -> None:
    """P0/P1: split-ish board — left authority, right proposes, actions bottom."""
    import curses

    if not hasattr(_draw_curses, "_color"):
        _draw_curses._color = False  # type: ignore[attr-defined]
        try:
            if curses.has_colors():
                curses.start_color()
                curses.use_default_colors()
                curses.init_pair(1, curses.COLOR_GREEN, -1)
                curses.init_pair(2, curses.COLOR_RED, -1)
                curses.init_pair(3, curses.COLOR_YELLOW, -1)
                curses.init_pair(4, curses.COLOR_CYAN, -1)
                curses.init_pair(5, curses.COLOR_MAGENTA, -1)
                _draw_curses._color = True  # type: ignore[attr-defined]
        except curses.error:
            pass

    stdscr.erase()
    h, w = stdscr.getmaxyx()
    split = max(28, int(w * 0.58)) if w >= 72 else w
    right_w = max(0, w - split - 1)

    # --- left column: authority ---
    left_lines = [
        f"OPERATOR BOARD v0 · {st.project_label}",
        str(st.root)[: split - 1],
        "",
        f"OBJECTIVE  {st.objective}"[: split - 1],
        f"PHASE {st.phase}  STATUS {st.status}"[: split - 1],
        f"APPROVAL  {st.approval}"[: split - 1],
        f">>> NEXT  {st.next_action}"[: split - 1],
        "",
        "PROHIBITED",
    ]
    if st.prohibited:
        for p in st.prohibited[:8]:
            left_lines.append(f"  ✗ {p}"[: split - 1])
    else:
        left_lines.append("  (none)")
    left_lines.append("")
    left_lines.append("EVENTS")
    for ev in st.recent_events[-6:]:
        left_lines.append(f"  {ev}"[: split - 1])

    y = 0
    max_left_h = max(6, h - len(ACTIONS) - 5)
    for line in left_lines:
        if y >= max_left_h:
            break
        attr = curses.A_NORMAL
        if _draw_curses._color:  # type: ignore[attr-defined]
            if line.startswith(">>> NEXT"):
                attr = curses.color_pair(1) | curses.A_BOLD
            elif line.startswith("  ✗"):
                attr = curses.color_pair(2)
            elif line.startswith("OPERATOR"):
                attr = curses.color_pair(4) | curses.A_BOLD
            elif line.startswith("APPROVAL"):
                attr = curses.color_pair(3)
        try:
            stdscr.addnstr(y, 0, line[: max(0, split - 1)], max(0, split - 1), attr)
        except curses.error:
            pass
        y += 1

    # --- right column: proposes ---
    if right_w > 12:
        ry = 0
        rtitle = "PROPOSE / SPIKE"
        try:
            attr = curses.color_pair(5) | curses.A_BOLD if _draw_curses._color else curses.A_BOLD  # type: ignore[attr-defined]
            stdscr.addnstr(ry, split + 1, rtitle[: right_w - 1], right_w - 1, attr)
        except curses.error:
            pass
        ry = 1
        if st.proposes:
            for i, p in enumerate(st.proposes[: max(1, max_left_h - 2)], 1):
                try:
                    rel = str(p.relative_to(st.root))
                except ValueError:
                    rel = p.name
                line = f"{i}. {rel}"
                try:
                    stdscr.addnstr(ry, split + 1, line[: right_w - 1], right_w - 1)
                except curses.error:
                    pass
                ry += 1
                if ry >= max_left_h:
                    break
        else:
            try:
                stdscr.addnstr(ry, split + 1, "(none)"[: right_w - 1], right_w - 1)
            except curses.error:
                pass

    # --- actions ---
    y = min(max_left_h + 1, h - len(ACTIONS) - 3)
    help_line = "↑↓/jk · Enter · [s] project · [l] propose · [p] preflight · [a]/[x] human · [?] · q"
    try:
        attr = curses.color_pair(4) if _draw_curses._color else curses.A_DIM  # type: ignore[attr-defined]
        stdscr.addnstr(y, 0, help_line[: w - 1], w - 1, attr)
    except curses.error:
        pass
    y += 1

    for i, (label, key, hot) in enumerate(ACTIONS):
        if y + i >= h - 1:
            break
        marker = "▶ " if i == selected else "  "
        hot_s = f"[{hot}] " if hot else "    "
        text = f"{marker}{hot_s}{label}"
        attr = curses.A_REVERSE if i == selected else curses.A_NORMAL
        if _draw_curses._color and not (i == selected):  # type: ignore[attr-defined]
            if key == "approve":
                attr = curses.color_pair(1) | curses.A_BOLD
            elif key == "reject":
                attr = curses.color_pair(2) | curses.A_BOLD
        try:
            stdscr.addnstr(y + i, 0, text[: w - 1], w - 1, attr)
        except curses.error:
            pass

    if st.result:
        row = h - 1
        attr = curses.A_BOLD
        if _draw_curses._color:  # type: ignore[attr-defined]
            low = st.result.lower()
            if low.startswith("refused") or "refused:" in low:
                attr = curses.color_pair(2) | curses.A_BOLD
            elif low.startswith("allowed") or "allowed:" in low:
                attr = curses.color_pair(1) | curses.A_BOLD
            else:
                attr = curses.color_pair(3) | curses.A_BOLD
        try:
            stdscr.move(row, 0)
            stdscr.clrtoeol()
            stdscr.addnstr(row, 0, st.result[: w - 1], w - 1, attr)
        except curses.error:
            pass

    stdscr.refresh()


def _run_action(
    st: ProjectState,
    key: str,
    prompt_fn: Callable[[str], Optional[str]],
    *,
    stdscr: Any = None,
) -> ProjectState:
    root = st.root
    prev_result = st.result

    def done(new: ProjectState, result: str = "", detail: str = "", write: bool = False) -> ProjectState:
        new.result = result
        new.detail = detail
        if write:
            _quiet_write(new)
        return new

    if key == "refresh":
        st = load_state(root)
        return done(st, "refreshed")
    if key == "quit":
        return done(st, "quit")
    if key == "write":
        st = load_state(root)
        md_p, html_p = write_projections(st)
        return done(st, f"wrote {md_p.name} + {html_p.name}")
    if key == "init":
        code, out = run_aether(["init", str(root)], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "current_init":
        code, out = run_aether(["current", "init", str(root)], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "help":
        lines = [
            "Operator Board v0 — action help",
            "(Board = Domain viewport. Grok = AI chat. Human only for approve.)",
            "",
        ]
        for label, akey, hot in ACTIONS:
            if akey == "help":
                continue
            tip = ACTION_HELP.get(akey, "")
            hot_s = f"[{hot}] " if hot else ""
            lines.append(f"{hot_s}{label}")
            if tip:
                lines.append(f"    {tip}")
        lines.append("")
        lines.append("Known projects for [s]:")
        for i, (pid, label, path) in enumerate(known_projects(), 1):
            lines.append(f"  {i}) {pid:5} {label}  {path}")
        return done(st, "help", "\n".join(lines))
    if key == "switch_project":
        projects = known_projects()
        if not projects:
            return done(st, "no known projects on disk")
        lines = ["Switch project — enter number:", ""]
        for i, (pid, label, path) in enumerate(projects, 1):
            mark = " *" if path.resolve() == root.resolve() else ""
            lines.append(f"  {i}) [{pid}] {label}{mark}")
            lines.append(f"      {path}")
        # if we can use prompt, do interactive pick; else show list
        choice = prompt_fn("Project number (empty=cancel): ")
        if not choice:
            return done(st, "switch cancelled", "\n".join(lines))
        if not choice.isdigit() or not (1 <= int(choice) <= len(projects)):
            return done(st, "invalid project number", "\n".join(lines))
        _pid, label, path = projects[int(choice) - 1]
        st = load_state(path)
        return done(st, f"switched → {label}", write=True)
    if key == "open_propose":
        st = load_state(root)
        if not st.proposes:
            return done(st, "no PROPOSE/SPIKE files found")
        lines = ["Open PROPOSE/SPIKE — enter number:", ""]
        for i, p in enumerate(st.proposes, 1):
            lines.append(f"  {i}) {_rel(root, p)}")
        choice = prompt_fn("Propose # (empty=list only): ")
        if not choice:
            return done(st, f"{len(st.proposes)} propose/spike file(s)", "\n".join(lines))
        if not choice.isdigit() or not (1 <= int(choice) <= len(st.proposes)):
            return done(st, "invalid number", "\n".join(lines))
        target = st.proposes[int(choice) - 1]
        editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"
        cmd = shlex.split(editor) + [str(target)]
        suspended = False
        if stdscr is not None:
            import curses

            try:
                curses.def_prog_mode()
                curses.endwin()
                suspended = True
            except curses.error:
                suspended = False
        try:
            code = subprocess.call(cmd)
        except OSError as e:
            return done(st, f"editor failed: {e}")
        finally:
            if suspended and stdscr is not None:
                import curses

                try:
                    curses.reset_prog_mode()
                    stdscr.clear()
                    stdscr.refresh()
                except curses.error:
                    pass
        st = load_state(root)
        return done(st, f"opened {target.name} (exit {code})")
    if key == "show_current":
        cf = root / "CURRENT.md"
        if not cf.is_file():
            return done(st, "no CURRENT.md — use Create CURRENT [n]")
        return done(st, "showing CURRENT.md", cf.read_text(encoding="utf-8", errors="replace")[:6000])
    if key == "events":
        ef = root / ".aether" / "events.jsonl"
        if not ef.is_file():
            return done(st, "no history yet")
        lines = ef.read_text(encoding="utf-8", errors="replace").splitlines()[-24:]
        return done(st, f"{len(lines)} recent events", "\n".join(lines))
    if key == "open_grok":
        grok = shutil.which("grok") or os.environ.get("GROK_BIN", "grok")
        cmd = [grok]
        suspended = False
        if stdscr is not None:
            import curses

            try:
                curses.def_prog_mode()
                curses.endwin()
                suspended = True
            except curses.error:
                suspended = False
        try:
            code = subprocess.call(cmd, cwd=str(root))
        except OSError as e:
            return done(st, f"could not start Grok: {e}")
        finally:
            if suspended and stdscr is not None:
                import curses

                try:
                    curses.reset_prog_mode()
                    stdscr.clear()
                    stdscr.refresh()
                except curses.error:
                    pass
        st = load_state(root)
        return done(st, f"Back from Grok (exit {code})")
    if key == "edit_current":
        cf = root / "CURRENT.md"
        if not cf.is_file():
            return done(st, "no CURRENT.md — use Create CURRENT [n]")
        editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"
        cmd = shlex.split(editor) + [str(cf)]
        suspended = False
        if stdscr is not None:
            import curses

            try:
                curses.def_prog_mode()
                curses.endwin()
                suspended = True
            except curses.error:
                suspended = False
        try:
            code = subprocess.call(cmd)
        except OSError as e:
            return done(st, f"editor failed: {e} ({editor!r})")
        finally:
            if suspended and stdscr is not None:
                import curses

                try:
                    curses.reset_prog_mode()
                    stdscr.clear()
                    stdscr.refresh()
                except curses.error:
                    pass
        st = load_state(root)
        if code != 0:
            return done(st, f"editor exit {code} ({editor})", write=True)
        return done(st, f"edited via {editor}", write=True)
    if key == "preflight_next":
        action = st.next_action
        if not action or action in ("(unset)", "unset", ""):
            return done(st, "Next empty — Edit CURRENT [o] or Check step [f]")
        code, out = run_aether(["preflight", action, str(root)], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "demo_refuse":
        action = st.prohibited[0] if st.prohibited else "deploy-production"
        code, out = run_aether(["preflight", action, str(root)], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "preflight":
        action = prompt_fn("Step name to check: ")
        if not action:
            st.result = prev_result
            return done(st, "check cancelled")
        code, out = run_aether(["preflight", action, str(root)], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "approve":
        reason = prompt_fn("Approve reason (human only): ")
        if reason is None:
            return done(st, "approve cancelled")
        if reason == "":
            reason = "approved from operator board"
        code, out = run_aether(["approve", reason], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "reject":
        reason = prompt_fn("Reject reason (human only): ")
        if reason is None:
            return done(st, "reject cancelled")
        if reason == "":
            reason = "rejected from operator board"
        code, out = run_aether(["reject", reason], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "artifact":
        path = prompt_fn("Path of finished file: ")
        if not path:
            return done(st, "record cancelled")
        action = prompt_fn("Step name (empty = Next): ")
        if action is None:
            return done(st, "record cancelled")
        if not action:
            action = st.next_action if st.next_action not in ("(unset)", "unset") else "manual"
        code, out = run_aether(
            ["artifact", path, "--action", action, "--status", "produced", "--project", str(root)],
            root,
        )
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    return done(st, f"unknown action {key}")


def run_tui_curses(root: Path) -> int:
    import curses

    st = load_state(root)
    selected = 0
    for i, (_, key, _) in enumerate(ACTIONS):
        if key == "preflight_next":
            selected = i
            break

    def main(stdscr) -> None:
        nonlocal st, selected
        curses.curs_set(0)
        stdscr.keypad(True)
        while True:
            if st.detail:
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

            _draw_curses(stdscr, st, selected)
            ch = stdscr.getch()
            if ch in (27,):
                break
            if ch in (curses.KEY_UP, ord("k")):
                selected = (selected - 1) % len(ACTIONS)
                continue
            if ch in (curses.KEY_DOWN, ord("j")):
                selected = (selected + 1) % len(ACTIONS)
                continue

            if ord("1") <= ch <= ord("9"):
                idx = ch - ord("1")
                if idx < len(ACTIONS):
                    selected = idx
                    ch = curses.KEY_ENTER
                else:
                    continue

            run_key: Optional[str] = None
            if ch in (curses.KEY_ENTER, 10, 13):
                run_key = ACTIONS[selected][1]
            else:
                try:
                    ch_s = chr(ch).lower()
                except ValueError:
                    ch_s = ""
                for i, (_, key, hot) in enumerate(ACTIONS):
                    if hot and ch_s == hot:
                        selected = i
                        run_key = key
                        break

            if run_key is None:
                continue
            if run_key == "quit":
                break

            def prompt(p: str) -> Optional[str]:
                return _prompt_line(stdscr, p)

            st = _run_action(st, run_key, prompt, stdscr=stdscr)
            if run_key == "quit":
                break

    curses.wrapper(main)
    return 0


def run_tui_simple(root: Path) -> int:
    st = load_state(root)
    while True:
        sys.stdout.write("\n" + "=" * 64 + "\n")
        sys.stdout.write(render_text(st))
        sys.stdout.write("\nActions:\n")
        for i, (label, _, hot) in enumerate(ACTIONS, 1):
            hot_s = f" [{hot}]" if hot else ""
            sys.stdout.write(f"  {i}){hot_s} {label}\n")
        sys.stdout.write("Choice [number / hotkey / q]: ")
        sys.stdout.flush()
        try:
            choice = sys.stdin.readline()
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            return 0
        if not choice:
            return 0
        choice = choice.strip().lower()
        if choice in ("q", "quit"):
            return 0

        key: Optional[str] = None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(ACTIONS):
                key = ACTIONS[idx][1]
        else:
            for _, k, hot in ACTIONS:
                if hot and choice == hot:
                    key = k
                    break

        if key is None:
            st.result = "enter a number, hotkey, or q"
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
    return 0


def run_tui(root: Path) -> int:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        sys.stderr.write(
            "aether panel: not a TTY — use --dump or --write, or run in a terminal\n"
        )
        st = load_state(root)
        sys.stdout.write(render_text(st))
        return 1
    try:
        import curses  # noqa: F401

        return run_tui_curses(root)
    except Exception as e:
        sys.stderr.write(f"aether panel: curses unavailable ({e}); simple menu\n")
        return run_tui_simple(root)


# --- main --------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Mechanicall Operator Board / Project Panel v0")
    ap.add_argument("path", nargs="?", default=".", help="project root")
    ap.add_argument("--write", action="store_true", help="write .aether/PANEL.md and panel.html")
    ap.add_argument("--dump", action="store_true", help="print text projection and exit")
    ap.add_argument("--simple", action="store_true", help="force numbered menu (no curses)")
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
    if args.simple:
        return run_tui_simple(root)
    return run_tui(root)


if __name__ == "__main__":
    sys.exit(main())
