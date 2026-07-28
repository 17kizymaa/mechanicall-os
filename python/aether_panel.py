#!/usr/bin/env python3
"""Project Panel — low-overhead TUI + file projections over aether authority.

Doctrine:
  - Filesystem is sole durable truth (CURRENT.md, events.jsonl, …).
  - This module only *projects* state and shells out to `aether` for mutations.
  - Models never approve. Panel is optional Interface Layer, not a second control plane.
  - Same projection powers TUI now; .md / .html scaffolds for later GUI-friendly surfaces.

Usage:
  python3 python/aether_panel.py [path]              # interactive TUI
  python3 python/aether_panel.py [path] --write      # write .aether/PANEL.md + panel.html
  python3 python/aether_panel.py [path] --dump       # print text projection to stdout
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
    app_name: Optional[str] = None
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


def _tail_events(events_path: Path, n: int = 8) -> List[str]:
    if not events_path.is_file():
        return []
    try:
        lines = events_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return lines[-n:]


def load_state(root: Path) -> ProjectState:
    root = project_root(root)
    st = ProjectState(root=root)
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
    st.recent_events = _tail_events(root / ".aether" / "events.jsonl")
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
    """Human-facing board. Plain labels; values still from CURRENT.md."""
    lines = [
        f"Project Panel — {st.root}",
        "",
        f"  What we're doing:  {st.objective}",
        f"  Phase:             {st.phase}",
        f"  Status:            {st.status}",
        f"  Baseline:          {st.baseline}",
        f"  Allowed next step: {st.next_action}",
        f"  Human sign-off:    {st.approval}",
    ]
    if st.app_name:
        lines.append(f"  App:               {st.app_name}")
    lines.append("")
    lines.append("  Do not do:")
    if st.prohibited:
        for p in st.prohibited:
            lines.append(f"    - {p}")
    else:
        lines.append("    (none listed)" if st.has_current else "    (no plan file yet)")
    lines.append("")
    lines.append("  Recent history:")
    if st.recent_events:
        for ev in st.recent_events:
            lines.append(f"    {ev[:120]}")
    else:
        lines.append("    (none)")
    if st.result:
        lines.append("")
        lines.append(f"  Last: {st.result}")
    lines.append("")
    lines.append(
        "  Note: This screen shows the plan file. It does not control the AI."
    )
    lines.append(
        "        Use Grok to talk to the AI. Human only for approve / reject."
    )
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
    next_cmd = (
        st.next_action
        if st.next_action not in ("(unset)", "unset", "")
        else "<action>"
    )
    return f"""# Project Panel

Generated by `aether panel --write`. Safe to delete; regenerate anytime.

**Root:** `{st.root}`

| Field | Value |
|-------|-------|
| What we're doing | {st.objective} |
| Phase | {st.phase} |
| Status | {st.status} |
| Baseline | {st.baseline} |
| **Next** (allowed next step) | `{st.next_action}` |
| Human sign-off | {st.approval} |
| App | {st.app_name or "—"} |

## Do not do (Prohibited)

{prol}

## Recent history

```
{event_block}
```

## Actions (CLI — or use `aether panel` TUI)

```bash
aether panel
aether preflight {next_cmd}
aether approve "…"   # human only
aether reject "…"    # human only
aether current
```

> This screen shows the plan file. Grok is the AI chat. Human only for approve.
"""


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
    next_esc = html.escape(st.next_action)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Project Panel — {html.escape(str(st.root.name))}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; padding: 0 1rem;
         background: #0f1419; color: #e7ecf1; }}
  h1 {{ font-size: 1.25rem; }}
  .card {{ border: 1px solid #2a3540; border-radius: 8px; padding: 1rem 1.25rem; margin: 1rem 0;
           background: #1a222c; }}
  .next {{ font-size: 1.4rem; font-weight: 700; color: #7dd3a7; }}
  .muted {{ color: #8b9aab; font-size: 0.9rem; }}
  code {{ background: #0f1419; padding: 0.1em 0.35em; border-radius: 3px; }}
  ul {{ padding-left: 1.2rem; }}
  .warn {{ border-left: 3px solid #e6b84d; padding-left: 0.75rem; color: #d4c4a0; }}
</style>
</head>
<body>
  <h1>Project Panel</h1>
  <p class="muted">{html.escape(str(st.root))}</p>
  <div class="card">
    <div><strong>What we're doing</strong> {html.escape(st.objective)}</div>
    <div><strong>Phase</strong> {html.escape(st.phase)} · <strong>Status</strong> {html.escape(st.status)}</div>
    <div><strong>Human sign-off</strong> {html.escape(st.approval)}</div>
    <p class="next">Allowed next step: {next_esc}</p>
  </div>
  <div class="card">
    <strong>Do not do</strong>
    <ul>{prol}</ul>
  </div>
  <div class="card">
    <strong>Recent history</strong>
    <ul>{events}</ul>
  </div>
  <p class="warn">Read-only scaffold. Plan + human yes/no: <code>aether panel</code>.
  AI chat: <code>grok</code>. Human only for approve.</p>
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

# (label, action_key, hotkey_char or "")
Action = Tuple[str, str, str]

# Client-facing labels; keys stay stable for code paths and hotkeys.
ACTIONS: List[Action] = [
    ("Refresh", "refresh", "r"),
    ("Check if next step is allowed", "preflight_next", "p"),
    ("Check a specific step…", "preflight", "f"),
    ("Show a blocked step (demo)", "demo_refuse", "d"),
    ("I approve (human only)", "approve", "a"),
    ("Send back / reject (human only)", "reject", "x"),
    ("Record a finished file…", "artifact", "t"),
    ("Show the plan on file", "show_current", "c"),
    ("Show recent history", "events", "e"),
    ("Edit the plan", "edit_current", "o"),
    ("Save a snapshot of this screen", "write", "w"),
    ("Start project awareness files", "init", "i"),
    ("Create the plan file", "current_init", "n"),
    ("Open Grok in this folder", "open_grok", "g"),
    ("Help (what do these mean?)", "help", "?"),
    ("Quit", "quit", "q"),
]

# One sentence each — shown by Help [?]. Not a second control plane.
ACTION_HELP: dict[str, str] = {
    "refresh": "Reload the plan file from disk.",
    "preflight_next": "Ask: is the allowed next step OK to run? (yes/no check only)",
    "preflight": "Check any step name you type — does not run the step.",
    "demo_refuse": "Practice: show what a blocked step looks like.",
    "approve": "Human only: mark the work accepted. The AI cannot do this.",
    "reject": "Human only: send the work back. The AI cannot do this.",
    "artifact": "Note a finished file path in the project record.",
    "show_current": "Read the plan file (CURRENT.md) on screen.",
    "events": "Show recent allow/refuse/approve history.",
    "edit_current": "Open the plan in your editor, then return here.",
    "write": "Write a copy of this board to PANEL.md / panel.html.",
    "init": "Create small awareness files for this folder.",
    "current_init": "Create an empty plan file (CURRENT.md) if missing.",
    "open_grok": "Leave this menu, open Grok (AI chat) here, then return. Two tools, one terminal.",
    "help": "This list.",
    "quit": "Leave the panel.",
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
    """Simple echo prompt at bottom of curses screen."""
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
                _draw_curses._color = True  # type: ignore[attr-defined]
        except curses.error:
            pass

    stdscr.erase()
    h, w = stdscr.getmaxyx()
    header = render_text(st).splitlines()
    # drop trailing note from header to save space; show in footer help instead
    header = [ln for ln in header if not ln.strip().startswith("Note:")]

    y = 0
    max_header = max(4, h - len(ACTIONS) - 6)
    for line in header:
        if y >= max_header:
            break
        attr = curses.A_NORMAL
        if _draw_curses._color:  # type: ignore[attr-defined]
            if "Allowed next step:" in line or "Next:" in line:
                attr = curses.color_pair(1) | curses.A_BOLD
            elif line.strip().startswith("- ") and "Do not do" not in line:
                attr = curses.color_pair(2)
        try:
            stdscr.addnstr(y, 0, line[: w - 1], w - 1, attr)
        except curses.error:
            pass
        y += 1

    y = min(y + 1, h - len(ACTIONS) - 4)
    help_line = "↑↓/jk · Enter · [?] help · [g] Grok · r refresh · q quit"
    try:
        attr = curses.color_pair(4) if _draw_curses._color else curses.A_DIM  # type: ignore[attr-defined]
        stdscr.addnstr(y, 0, help_line[: w - 1], w - 1, attr)
    except curses.error:
        pass
    y += 1

    for i, (label, _, hot) in enumerate(ACTIONS):
        marker = "▶ " if i == selected else "  "
        hot_s = f"[{hot}] " if hot else "    "
        text = f"{marker}{hot_s}{label}"
        attr = curses.A_REVERSE if i == selected else curses.A_NORMAL
        try:
            stdscr.addnstr(y + i, 0, text[: w - 1], w - 1, attr)
        except curses.error:
            pass

    # result footer
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
            "What these actions mean",
            "(Panel = plan + human yes/no. Grok = AI chat. Not one fused product.)",
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
        return done(st, "help", "\n".join(lines))
    if key == "show_current":
        cf = root / "CURRENT.md"
        if not cf.is_file():
            return done(st, "no plan file yet — use Create the plan file [n]")
        return done(st, "showing plan file", cf.read_text(encoding="utf-8", errors="replace")[:4000])
    if key == "events":
        ef = root / ".aether" / "events.jsonl"
        if not ef.is_file():
            return done(st, "no history yet")
        lines = ef.read_text(encoding="utf-8", errors="replace").splitlines()[-20:]
        return done(st, f"{len(lines)} recent history lines", "\n".join(lines))
    if key == "open_grok":
        # Ops convenience: same TTY, leave panel, run Grok, return. Not a product merge.
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
            return done(
                st,
                f"could not start Grok: {e}. Install first, or run: grok",
            )
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
            return done(st, f"Grok finished (exit {code}). Back at the plan.")
        return done(st, "Back from Grok. Plan reloaded.")
    if key == "edit_current":
        # Curses must release the tty before $EDITOR; otherwise the action no-ops / corrupts UI.
        cf = root / "CURRENT.md"
        if not cf.is_file():
            return done(st, "no plan file yet — use Create the plan file [n]")
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
            return done(st, "Allowed next step is empty — Edit the plan [o] or Check a step [f]")
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
        reason = prompt_fn("Why are you approving? ")
        if reason is None:
            return done(st, "approve cancelled")
        if reason == "":
            reason = "approved from panel"
        code, out = run_aether(["approve", reason], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "reject":
        reason = prompt_fn("Why send it back? ")
        if reason is None:
            return done(st, "reject cancelled")
        if reason == "":
            reason = "rejected from panel"
        code, out = run_aether(["reject", reason], root)
        st = load_state(root)
        return done(st, _summarize_result(code, out), write=True)
    if key == "artifact":
        path = prompt_fn("Path of the finished file: ")
        if not path:
            return done(st, "record cancelled")
        action = prompt_fn("Step name (empty = allowed next step): ")
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
    # default highlight on Preflight Next
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
                    stdscr.addnstr(h - 1, 0, "[any key to return to panel]"[: w - 1], w - 1)
                except curses.error:
                    pass
                stdscr.refresh()
                stdscr.getch()
                st.detail = ""
                continue

            _draw_curses(stdscr, st, selected)
            ch = stdscr.getch()
            if ch in (27,):  # Esc
                break
            if ch in (curses.KEY_UP, ord("k")):
                selected = (selected - 1) % len(ACTIONS)
                continue
            if ch in (curses.KEY_DOWN, ord("j")):
                selected = (selected + 1) % len(ACTIONS)
                continue

            # number keys 1-9 select and run (1-based into ACTIONS)
            if ord("1") <= ch <= ord("9"):
                idx = ch - ord("1")
                if idx < len(ACTIONS):
                    selected = idx
                    ch = curses.KEY_ENTER  # fall through to run
                else:
                    continue

            # letter hotkeys
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
    """Numbered menu fallback when curses is unavailable."""
    st = load_state(root)
    while True:
        sys.stdout.write("\n" + "=" * 60 + "\n")
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
    ap = argparse.ArgumentParser(description="Mechanicall Project Panel (TUI + projections)")
    ap.add_argument("path", nargs="?", default=".", help="project root")
    ap.add_argument("--write", action="store_true", help="write .aether/PANEL.md and panel.html")
    ap.add_argument("--dump", action="store_true", help="print text projection and exit")
    ap.add_argument("--simple", action="store_true", help="force numbered menu (no curses)")
    args = ap.parse_args(list(argv) if argv is not None else None)

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
