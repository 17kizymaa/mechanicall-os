#!/usr/bin/env python3
"""Fullscreen dual-pane Project Panel TUI (not a CLI menu).

Layout (locked):
  LEFT  — Grok-shaped Domain chat (fullscreen app chrome)
  RIGHT — CURRENT.md always visible

Interaction:
  Tab        cycle focus: chat | menu | current
  Type       chat input (when focus=chat)
  Enter      send chat / run menu action
  ↑↓←→       scroll panes / move menu
  Esc        leave Advanced (if open)
  No letter hotkeys on main.

Preflight is not on the main board — use Domain shell (or Advanced).
"""
from __future__ import annotations

import curses
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Callable, List, Optional, Tuple

# Import host module pieces lazily via injection to avoid circular imports at load.


Action = Tuple[str, str]

MAIN_ACTIONS: List[Action] = [
    ("Refresh", "refresh"),
    ("APPROVE", "approve"),
    ("REJECT", "reject"),
    ("Advanced…", "advanced"),
    ("Domain shell", "open_shell"),
    ("Grok fullscreen", "open_grok"),
    ("Edit CURRENT", "edit_current"),
    ("Quit", "quit"),
]

ADVANCED_ACTIONS: List[Action] = [
    ("Preflight Next (prefer shell)", "preflight_next"),
    ("Preflight step…", "preflight"),
    ("Demo refuse", "demo_refuse"),
    ("Switch project…", "switch_project"),
    ("Open PROPOSE…", "open_propose"),
    ("Record artifact…", "artifact"),
    ("Events", "events"),
    ("Write PANEL files", "write"),
    ("Init .aether", "init"),
    ("Create CURRENT", "current_init"),
    ("LLM preset next", "llm_next"),
    ("LLM preset pick…", "llm_pick"),
    ("Design notes", "help"),
    ("← Back", "advanced_back"),
]


def _wrap(text: str, width: int) -> List[str]:
    width = max(8, width)
    out: List[str] = []
    for para in (text or "").splitlines() or [""]:
        while len(para) > width:
            out.append(para[:width])
            para = para[width:]
        out.append(para)
    return out


def _safe_add(win, y: int, x: int, s: str, attr: int = 0) -> None:
    try:
        h, w = win.getmaxyx()
        if y < 0 or y >= h or x >= w:
            return
        win.addnstr(y, x, s, max(0, w - x - 1), attr)
    except curses.error:
        pass


class PanelApp:
    def __init__(self, root: Path, host_mod) -> None:
        self.root = root
        self.host = host_mod
        self.st = host_mod.load_state(root)
        self.history: List[dict] = []
        self.focus = "chat"  # chat | menu | current
        self.selected = 0
        self.input_buf = ""
        self.chat_scroll = 0
        self.current_scroll = 0
        self.status = "Tab focus · type to chat · Enter send · menu for Approve/shell"
        self.advanced = False
        self._colors = False
        # Geometry cache for scroll clamps (set each draw)
        self._inner_h = 10
        self._chat_line_count = 0
        self._cur_line_count = 0

    def _init_colors(self) -> None:
        if not curses.has_colors():
            return
        try:
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_MAGENTA, -1)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
            curses.init_pair(5, curses.COLOR_RED, -1)
            curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
            self._colors = True
        except curses.error:
            self._colors = False

    def c(self, n: int) -> int:
        if not self._colors:
            return 0
        try:
            return curses.color_pair(n)
        except curses.error:
            return 0

    def menu(self) -> List[Action]:
        return ADVANCED_ACTIONS if self.advanced else MAIN_ACTIONS

    def chat_display(self, width: int) -> List[str]:
        if not self.history:
            return _wrap(
                "Domain chat — Grok-shaped left pane\n"
                "CURRENT is always on the right.\n\n"
                "Type below and press Enter.\n"
                "Tab → menu (Approve / shell / Grok full).\n"
                "Preflight lives in Domain shell.",
                width,
            )
        lines: List[str] = []
        for m in self.history[-50:]:
            role = m.get("role") or ""
            content = (m.get("content") or "").strip()
            prefix = "you  " if role == "user" else "◆   "
            for i, wl in enumerate(_wrap(content, max(8, width - 5))):
                lines.append((prefix if i == 0 else "    ") + wl)
            lines.append("")
        return lines

    def current_text(self) -> str:
        cf = self.root / "CURRENT.md"
        if not cf.is_file():
            return "(no CURRENT.md)\n\nUse menu → Advanced → Create CURRENT"
        try:
            body = cf.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return f"(read error: {e})"
        pin = (
            f"NEXT {self.st.next_action}\n"
            f"{self.st.phase} · {self.st.status} · {self.st.approval}\n"
            f"{'─' * 40}\n"
        )
        return pin + body

    def _draw_box(self, stdscr, y0: int, x0: int, h: int, w: int, attr: int = 0) -> None:
        """Draw a box on stdscr (no child windows — avoids flicker/z-order bugs)."""
        if h < 2 or w < 2:
            return
        # corners + edges (ASCII-safe for odd locales; ACS when available)
        try:
            tl, tr = curses.ACS_ULCORNER, curses.ACS_URCORNER
            bl, br = curses.ACS_LLCORNER, curses.ACS_LRCORNER
            hz, vt = curses.ACS_HLINE, curses.ACS_VLINE
        except Exception:
            tl = tr = bl = br = ord("+")
            hz, vt = ord("-"), ord("|")
        try:
            stdscr.attron(attr)
            stdscr.addch(y0, x0, tl)
            stdscr.addch(y0, x0 + w - 1, tr)
            stdscr.addch(y0 + h - 1, x0, bl)
            stdscr.addch(y0 + h - 1, x0 + w - 1, br)
            for x in range(1, w - 1):
                stdscr.addch(y0, x0 + x, hz)
                stdscr.addch(y0 + h - 1, x0 + x, hz)
            for y in range(1, h - 1):
                stdscr.addch(y0 + y, x0, vt)
                stdscr.addch(y0 + y, x0 + w - 1, vt)
            stdscr.attroff(attr)
        except curses.error:
            pass

    def draw(self, stdscr) -> None:
        """Single-buffer draw on stdscr only.

        Bugfix: creating newwin() every frame + stdscr.refresh() after
        noutrefresh() painted blank erase over the panes (invisible + flicker).
        """
        h, w = stdscr.getmaxyx()
        # erase once; draw everything onto stdscr; one refresh at end
        stdscr.erase()
        if h < 14 or w < 48:
            _safe_add(stdscr, 0, 0, "Resize terminal (≥14 rows × 48 cols)")
            stdscr.noutrefresh()
            curses.doupdate()
            return

        top = 1
        bot_menu = 3
        bot_input = 2
        body_h = max(4, h - top - bot_menu - bot_input)
        mid = max(18, int(w * 0.56))
        if w - mid < 20:
            mid = max(12, w - 20)
        right_w = w - mid

        # Title bar
        title = (
            f" MECHANICALL PANEL  │  {self.st.project_label or self.root.name}  │  "
            f"Grok-left · CURRENT-right "
        )
        _safe_add(stdscr, 0, 0, title.ljust(w)[: max(0, w - 1)], self.c(6) | curses.A_BOLD)

        # Pane frames on stdscr
        self._draw_box(stdscr, top, 0, body_h, mid, self.c(1))
        self._draw_box(stdscr, top, mid, body_h, right_w, self.c(3))

        lh = "● CHAT" if self.focus == "chat" else " CHAT"
        rh = "● CURRENT" if self.focus == "current" else " CURRENT"
        _safe_add(stdscr, top, 2, f" {lh} ", self.c(1) | curses.A_BOLD)
        _safe_add(stdscr, top, mid + 2, f" {rh} ", self.c(3) | curses.A_BOLD)

        # Scrollable interiors (clip inside boxes)
        inner_h = max(1, body_h - 2)
        inner_w_l = max(8, mid - 4)
        inner_w_r = max(8, right_w - 4)
        self._inner_h = inner_h

        chat_lines = self.chat_display(inner_w_l)
        self._chat_line_count = len(chat_lines)
        max_cs = max(0, len(chat_lines) - inner_h)
        self.chat_scroll = max(0, min(self.chat_scroll, max_cs))
        vis = chat_lines[self.chat_scroll : self.chat_scroll + inner_h]
        for i in range(inner_h):
            row = top + 1 + i
            # clear interior cell line first for clean scroll (no ghost glyphs)
            _safe_add(stdscr, row, 2, " " * inner_w_l)
            if i < len(vis):
                line = vis[i][:inner_w_l]
                attr = (
                    self.c(2)
                    if line.startswith("you")
                    else (self.c(1) if line.startswith("◆") else 0)
                )
                _safe_add(stdscr, row, 2, line, attr)
        # scroll indicator left
        if max_cs > 0:
            ind = f" {self.chat_scroll + 1}-{min(self.chat_scroll + inner_h, len(chat_lines))}/{len(chat_lines)} "
            _safe_add(stdscr, top + body_h - 1, max(2, mid - len(ind) - 2), ind, self.c(4))

        cur_lines = _wrap(self.current_text(), inner_w_r)
        self._cur_line_count = len(cur_lines)
        max_rs = max(0, len(cur_lines) - inner_h)
        self.current_scroll = max(0, min(self.current_scroll, max_rs))
        vis_r = cur_lines[self.current_scroll : self.current_scroll + inner_h]
        for i in range(inner_h):
            row = top + 1 + i
            _safe_add(stdscr, row, mid + 2, " " * inner_w_r)
            if i < len(vis_r):
                line = vis_r[i][:inner_w_r]
                attr = self.c(3) | curses.A_BOLD if i < 3 and self.current_scroll == 0 else 0
                _safe_add(stdscr, row, mid + 2, line, attr)
        if max_rs > 0:
            ind = f" {self.current_scroll + 1}-{min(self.current_scroll + inner_h, len(cur_lines))}/{len(cur_lines)} "
            _safe_add(
                stdscr,
                top + body_h - 1,
                min(w - len(ind) - 2, mid + right_w - len(ind) - 2),
                ind,
                self.c(4),
            )

        # Menu dock
        menu_y = top + body_h
        _safe_add(
            stdscr,
            menu_y,
            0,
            "─" * max(0, w - 1),
            self.c(7) if self.focus == "menu" else self.c(1),
        )
        menu = self.menu()
        x = 1
        y = menu_y + 1
        for i, (label, _k) in enumerate(menu):
            pill = f" {label} "
            if x + len(pill) >= w - 2:
                y += 1
                x = 1
                if y >= h - bot_input:
                    break
            sel = self.focus == "menu" and i == self.selected
            attr = curses.A_REVERSE | self.c(6) if sel else self.c(1)
            _safe_add(stdscr, y, x, pill, attr)
            x += len(pill) + 1

        # Input dock
        mode = {
            "chat": "CHAT  type + Enter to send",
            "menu": "MENU  ←→ select · Enter run",
            "current": "CURRENT  ↑↓ scroll",
        }[self.focus]
        _safe_add(
            stdscr,
            h - 2,
            0,
            f" {mode}  ·  Tab focus  ·  {self.status}"[: max(0, w - 1)],
            self.c(4),
        )
        prompt = " › "
        shown = (prompt + self.input_buf)[-max(10, w - 3) :]
        attr = curses.A_BOLD | self.c(2) if self.focus == "chat" else 0
        _safe_add(stdscr, h - 1, 0, shown.ljust(max(0, w - 1))[: max(0, w - 1)], attr)

        # Single update — never stdscr.refresh() after partial child updates
        stdscr.noutrefresh()
        curses.doupdate()

    def panel_chat(self, text: str) -> None:
        try:
            from aether_fs import read_current
            from aether_llm import apply_peer_backend, chat
            from aether_shell_agent import agent_chat_loop, resolve_agent_role, set_agent_role
        except ImportError as e:
            self.status = f"chat import error: {e}"
            return
        try:
            if resolve_agent_role() != "grok":
                set_agent_role("peer")
                apply_peer_backend(self.root)
        except Exception:
            pass
        self.history.append({"role": "user", "content": text})
        try:
            cur = read_current(self.root) or ""
            reply = agent_chat_loop(
                self.root,
                self.history[-16:],
                chat_fn=chat,
                current=cur,
                temperature=0.35,
            )
            self.history.append({"role": "assistant", "content": reply or ""})
            self.status = "ready"
        except Exception as e:
            self.history.pop()
            self.status = f"llm: {e}"
        self.st = self.host.load_state(self.root)

    def run_menu_action(self, stdscr, key: str) -> bool:
        """Return True if should quit app."""
        if key == "advanced":
            self.advanced = True
            self.selected = 0
            self.status = "Advanced — preflight also in Domain shell"
            return False
        if key == "advanced_back":
            self.advanced = False
            self.selected = 0
            return False
        if key == "quit":
            return True
        if key == "help":
            self.st.detail = (
                "docs/PANEL-GROK-SPLIT.md\n\n"
                "LEFT  = Grok-shaped Domain chat (fullscreen TUI)\n"
                "RIGHT = CURRENT always\n"
                "Main has no letter hotkeys and no preflight.\n"
                "Preflight → Domain shell agent (or Advanced).\n"
            )
            return False

        def prompt(p: str) -> Optional[str]:
            return self.host._prompt_line(stdscr, p)

        self.st = self.host._run_action(self.st, key, prompt, stdscr=stdscr)
        self.status = self.st.result or self.status
        if self.st.detail:
            # show overlay in loop
            pass
        self.st = self.host.load_state(self.st.root)
        self.root = self.st.root
        return False

    def loop(self, stdscr) -> None:
        try:
            curses.curs_set(1)
        except curses.error:
            pass
        try:
            curses.raw()
        except curses.error:
            pass
        stdscr.keypad(True)
        if hasattr(stdscr, "meta"):
            try:
                stdscr.meta(True)
            except curses.error:
                pass
        try:
            curses.mousemask(0)  # keyboard-first; can enable later
        except curses.error:
            pass
        # Force full redraw / alt screen already via wrapper
        try:
            stdscr.clear()
            stdscr.refresh()
        except curses.error:
            pass
        self._init_colors()

        while True:
            # detail overlay
            if self.st.detail:
                h, w = stdscr.getmaxyx()
                stdscr.erase()
                for i, line in enumerate(self.st.detail.splitlines()[: h - 2]):
                    _safe_add(stdscr, i, 0, line)
                _safe_add(stdscr, h - 1, 0, " any key → back ")
                stdscr.refresh()
                stdscr.getch()
                self.st.detail = ""
                continue

            self.draw(stdscr)
            ch = stdscr.getch()

            if ch == 9:  # Tab
                order = ["chat", "menu", "current"]
                self.focus = order[(order.index(self.focus) + 1) % 3]
                try:
                    curses.curs_set(1 if self.focus == "chat" else 0)
                except curses.error:
                    pass
                continue

            if ch == 27:  # Esc
                if self.advanced:
                    self.advanced = False
                    self.selected = 0
                continue

            menu = self.menu()
            if self.selected >= len(menu):
                self.selected = 0

            if self.focus == "current":
                max_rs = max(0, self._cur_line_count - self._inner_h)
                if ch in (curses.KEY_UP,):
                    self.current_scroll = max(0, self.current_scroll - 1)
                elif ch in (curses.KEY_DOWN,):
                    self.current_scroll = min(max_rs, self.current_scroll + 1)
                elif ch == curses.KEY_PPAGE:
                    self.current_scroll = max(0, self.current_scroll - self._inner_h)
                elif ch == curses.KEY_NPAGE:
                    self.current_scroll = min(max_rs, self.current_scroll + self._inner_h)
                elif ch == curses.KEY_HOME:
                    self.current_scroll = 0
                elif ch == curses.KEY_END:
                    self.current_scroll = max_rs
                continue

            if self.focus == "menu":
                if ch in (curses.KEY_LEFT, curses.KEY_UP):
                    self.selected = (self.selected - 1) % len(menu)
                elif ch in (curses.KEY_RIGHT, curses.KEY_DOWN):
                    self.selected = (self.selected + 1) % len(menu)
                elif ch in (curses.KEY_ENTER, 10, 13):
                    if self.run_menu_action(stdscr, menu[self.selected][1]):
                        return
                continue

            # chat focus
            max_cs = max(0, self._chat_line_count - self._inner_h)
            if ch == curses.KEY_UP:
                self.chat_scroll = max(0, self.chat_scroll - 1)
            elif ch == curses.KEY_DOWN:
                self.chat_scroll = min(max_cs, self.chat_scroll + 1)
            elif ch == curses.KEY_PPAGE:
                self.chat_scroll = max(0, self.chat_scroll - self._inner_h)
            elif ch == curses.KEY_NPAGE:
                self.chat_scroll = min(max_cs, self.chat_scroll + self._inner_h)
            elif ch in (curses.KEY_BACKSPACE, 127, 8):
                self.input_buf = self.input_buf[:-1]
            elif ch in (curses.KEY_ENTER, 10, 13):
                text = self.input_buf.strip()
                self.input_buf = ""
                if text:
                    self.status = "…"
                    self.draw(stdscr)
                    self.panel_chat(text)
                    # stick to bottom of chat after reply
                    self.chat_scroll = max(0, self._chat_line_count - self._inner_h)
            elif 32 <= ch < 127:
                self.input_buf += chr(ch)


def run_fullscreen_tui(root: Path, host_mod) -> int:
    """Real alt-screen TUI. Never falls back to numbered CLI silently."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        sys.stderr.write(
            "aether panel: need a real TTY for the TUI.\n"
            "  Open a terminal and run:  aether panel .\n"
            "  Or: aether panel --dump   (text only)\n"
        )
        return 1

    app = PanelApp(root, host_mod)

    def _main(stdscr) -> None:
        app.loop(stdscr)

    try:
        curses.wrapper(_main)
        return 0
    except Exception:
        sys.stderr.write("aether panel TUI crashed:\n")
        sys.stderr.write(traceback.format_exc())
        sys.stderr.write("\nTry: aether panel --simple   (CLI menu fallback)\n")
        return 2


def run_tmux_grok_split(root: Path) -> int:
    """Steal real Grok TUI on the left; CURRENT watcher on the right (tmux).

    Requires: tmux, and preferably `grok` on PATH.
    """
    if not shutil.which("tmux"):
        sys.stderr.write("aether panel --grok-split needs tmux installed\n")
        return 1
    root = root.resolve()
    session = f"aether-panel-{abs(hash(str(root))) % 10**8}"
    # kill old session same name
    subprocess.call(["tmux", "kill-session", "-t", session], stderr=subprocess.DEVNULL)
    grok_bin = os.environ.get("GROK_BIN", "").strip() or shutil.which("grok")
    # Right pane: live CURRENT
    viewer = (
        f"while true; do clear; "
        f"printf '\\033[1;35m══ CURRENT.md ══\\033[0m %s\\n\\n' {shlex_quote(str(root))}; "
        f"test -f {shlex_quote(str(root / 'CURRENT.md'))} "
        f"&& cat {shlex_quote(str(root / 'CURRENT.md'))} || echo '(no CURRENT)'; "
        f"sleep 2; done"
    )
    # Left: real Grok TUI if present, else Domain shell (Grok-shaped agent)
    aether_home = os.environ.get("AETHER_HOME") or str(Path(__file__).resolve().parent.parent)
    if grok_bin:
        left = f"cd {shlex_quote(str(root))} && exec {shlex_quote(grok_bin)}"
    else:
        left = (
            f"cd {shlex_quote(str(root))} && "
            f"AETHER_HOME={shlex_quote(aether_home)} "
            f"exec {shlex_quote(sys.executable)} "
            f"{shlex_quote(str(Path(aether_home) / 'python' / 'aether_shell.py'))} ."
        )
    # Create session with left command, split right
    subprocess.check_call(["tmux", "new-session", "-d", "-s", session, "-c", str(root), left])
    subprocess.check_call(["tmux", "split-window", "-h", "-t", session, viewer])
    # Prefer left slightly wider
    subprocess.call(["tmux", "resize-pane", "-t", f"{session}:0.0", "-x", "58%"])
    os.execvp("tmux", ["tmux", "attach-session", "-t", session])
    return 0  # unreachable


def shlex_quote(s: str) -> str:
    import shlex

    return shlex.quote(s)
