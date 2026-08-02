#!/usr/bin/env python3
"""Mechanicall seat TUI — one app, two pages (PANEL | SHELL), shared GOP header.

Pages share the same header chrome (like bootloader tabs):
  F1 PANEL  — dual-pane Domain chat + CURRENT + human gates
  F2 SHELL  — Domain shell transcript + slash/tools (same window)

No process replace. No compositor kill. /panel on shell page = F1.
"""
from __future__ import annotations

import curses
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

Action = Tuple[str, str]

MAIN_ACTIONS: List[Action] = [
    ("APPROVE", "approve"),
    ("REJECT", "reject"),
    ("REFRESH", "refresh"),
    ("SHELL", "open_shell"),
    ("ADVANCED", "advanced"),
    ("EDIT CURRENT", "edit_current"),
    ("QUIT", "quit"),
]

ADVANCED_ACTIONS: List[Action] = [
    ("Preflight Next", "preflight_next"),
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
    ("Grok fullscreen", "open_grok"),
    ("Playbook / design", "help"),
    ("← Back", "advanced_back"),
]

SHELL_ACTIONS: List[Action] = [
    ("PANEL", "goto_panel"),
    ("PREFLIGHT NEXT", "preflight_next"),
    ("STATUS", "shell_status"),
    ("HELP", "shell_help"),
    ("CLEAR", "shell_clear"),
    ("QUIT", "quit"),
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


def _backend_label() -> str:
    try:
        from aether_llm import resolve_backend

        b = resolve_backend()
        if not b:
            return "backend: none"
        return f"backend: {getattr(b, 'name', '?')}/{getattr(b, 'model', '?')}"
    except Exception as e:
        return f"backend: ? ({e.__class__.__name__})"


PLAYBOOK = """\
AETHER SEAT · PANEL + SHELL (same app / same TTY)
=================================================
docs/PANEL-GROK-SPLIT.md  ·  docs/AETHER-SHELL.md

F1 PANEL  Domain chat + CURRENT + APPROVE/REJECT
F2 SHELL  slash tools + Domain agent (same header)
  In shell: /panel or F1 returns to PANEL page
  Preflight: shell> /preflight <id>  or  menu PREFLIGHT NEXT

Human only approves. Models never approve.
"""


class PanelApp:
    def __init__(self, root: Path, host_mod) -> None:
        self.root = root
        self.host = host_mod
        self.st = host_mod.load_state(root)
        # page: panel | shell  (tabs under shared header)
        self.page = "panel"
        self.history: List[dict] = []
        self.shell_lines: List[str] = []
        self.shell_hist: List[dict] = []
        self.focus = "chat"  # panel: chat|menu|current · shell: input|menu|log
        self.selected = 0
        self.input_buf = ""
        self.chat_scroll = 0
        self.current_scroll = 0
        self.shell_scroll = 0
        self.status = "F1 panel · F2 shell · same header · Tab focus"
        self.advanced = False
        self._colors = False
        self._inner_h = 10
        self._be_label = _backend_label()
        self._shell_booted = False

    # --- colors / chrome -------------------------------------------------

    def _init_colors(self) -> None:
        if not curses.has_colors():
            return
        try:
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_WHITE, -1)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
            curses.init_pair(5, curses.COLOR_RED, -1)
            curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)
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

    def _draw_box(self, stdscr, y0: int, x0: int, h: int, w: int, attr: int = 0) -> None:
        if h < 2 or w < 2:
            return
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

    def draw_header(self, stdscr, w: int) -> None:
        """Shared GOP header — same on every page."""
        line0 = " MECHANICALL SEAT  ·  EFI/GOP chrome  ·  one app · two pages "
        _safe_add(stdscr, 0, 0, line0.ljust(w)[: max(0, w - 1)], self.c(6) | curses.A_BOLD)

        _safe_add(stdscr, 1, 0, " " * max(0, w - 1), self.c(8))
        # Tabs: active page highlighted green
        p_attr = self.c(9) | curses.A_BOLD if self.page == "panel" else self.c(8) | curses.A_BOLD
        s_attr = self.c(9) | curses.A_BOLD if self.page == "shell" else self.c(8) | curses.A_BOLD
        _safe_add(stdscr, 1, 1, " F1 PANEL ", p_attr)
        _safe_add(stdscr, 1, 12, " F2 SHELL ", s_attr)
        proj = (self.st.project_label or self.root.name)[:16]
        nxt = (self.st.next_action or "—")[:24]
        meta = f"  {proj}  ·  Next: {nxt}  ·  {self._be_label}"
        _safe_add(stdscr, 1, 24, meta[: max(0, w - 25)], self.c(8))

    def menu(self) -> List[Action]:
        if self.page == "shell":
            return SHELL_ACTIONS
        return ADVANCED_ACTIONS if self.advanced else MAIN_ACTIONS

    # --- panel page content ----------------------------------------------

    def chat_display(self, width: int) -> List[str]:
        if not self.history:
            return _wrap(
                "GROK CHAT (session compute)\n"
                "──────────────────────────\n"
                "Same stack as Grok Build TUI:\n"
                "  thinking → answer (streaming-json)\n"
                "CURRENT always on the right.\n"
                "F2 SHELL · Enter send · Tab focus",
                width,
            )
        lines: List[str] = []
        for m in self.history[-50:]:
            role = m.get("role") or ""
            content = (m.get("content") or "").strip()
            thinking = (m.get("thinking") or "").strip()
            if role == "user":
                prefix = "YOU │ "
                for i, wl in enumerate(_wrap(content, max(8, width - len(prefix)))):
                    lines.append((prefix if i == 0 else "    │ ") + wl)
            else:
                if thinking:
                    tprefix = "💭  │ "
                    # collapse whitespace-heavy thought streams a bit for display
                    tshow = thinking
                    if len(tshow) > 1200:
                        tshow = tshow[:600] + " … " + tshow[-400:]
                    for i, wl in enumerate(_wrap(tshow, max(8, width - len(tprefix)))):
                        lines.append((tprefix if i == 0 else "    │ ") + wl)
                    lines.append("────┼" + "─" * max(4, width - 5))
                prefix = "GROK│ "
                for i, wl in enumerate(_wrap(content or "(empty)", max(8, width - len(prefix)))):
                    lines.append((prefix if i == 0 else "    │ ") + wl)
            lines.append("")
        return lines

    def current_text(self) -> str:
        cf = self.root / "CURRENT.md"
        if not cf.is_file():
            return "(no CURRENT.md)\n\nAdvanced → Create CURRENT"
        try:
            body = cf.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return f"(read error: {e})"
        pin = (
            f"NEXT  {self.st.next_action}\n"
            f"PHASE {self.st.phase}  ·  {self.st.status}  ·  {self.st.approval}\n"
            f"{'─' * 40}\n"
        )
        return pin + body

    def draw_panel_page(self, stdscr, h: int, w: int, top: int) -> None:
        bot_menu, bot_input = 2, 2
        body_h = max(5, h - top - bot_menu - bot_input)
        mid = max(20, int(w * 0.55))
        if w - mid < 22:
            mid = max(14, w - 22)
        right_w = w - mid
        frame = self.c(1)
        self._draw_box(stdscr, top, 0, body_h, mid, frame)
        self._draw_box(stdscr, top, mid, body_h, right_w, frame)

        lh = "▌ CHAT" if self.focus == "chat" else "  CHAT"
        rh = "▌ CURRENT" if self.focus == "current" else "  CURRENT"
        _safe_add(stdscr, top, 2, f" {lh} ", self.c(1) | curses.A_BOLD)
        _safe_add(stdscr, top, mid + 2, f" {rh} ", self.c(3) | curses.A_BOLD)

        inner_h = max(1, body_h - 2)
        inner_w_l = max(8, mid - 4)
        inner_w_r = max(8, right_w - 4)
        self._inner_h = inner_h

        chat_lines = self.chat_display(inner_w_l)
        max_cs = max(0, len(chat_lines) - inner_h)
        self.chat_scroll = max(0, min(self.chat_scroll, max_cs))
        vis = chat_lines[self.chat_scroll : self.chat_scroll + inner_h]
        for i in range(inner_h):
            row = top + 1 + i
            _safe_add(stdscr, row, 2, " " * inner_w_l)
            if i < len(vis):
                line = vis[i][:inner_w_l]
                attr = 0
                if line.startswith("YOU"):
                    attr = self.c(2)
                elif line.startswith("GROK") or line.startswith("◆"):
                    attr = self.c(1) | curses.A_BOLD
                elif line.startswith("💭") or line.startswith("────"):
                    attr = self.c(4)  # thinking = amber

                _safe_add(stdscr, row, 2, line, attr)

        cur_lines = _wrap(self.current_text(), inner_w_r)
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

        self._draw_menu_dock(stdscr, top + body_h, h, w)

    # --- shell page content ----------------------------------------------

    def ensure_shell_boot(self) -> None:
        if self._shell_booted:
            return
        self._shell_booted = True
        try:
            from aether_fs import load_dotenv_files
            from aether_llm import apply_peer_backend, describe_backend
            from aether_shell import status_line
            from aether_shell_agent import set_agent_role

            load_dotenv_files()
            lines = [
                "aether shell page — Domain-bound · YOUR model (sft-v4 peer)",
                status_line(self.root),
            ]
            set_agent_role("peer")
            lines.append(apply_peer_backend(self.root, model="personal-llm-sft-v4") or "peer backend")
            try:
                lines.append(f"backend: {describe_backend()}")
            except Exception:
                lines.append(f"backend: {_backend_label()}")
            lines.append("slash: /help /preflight /run /panel  ·  F1 → PANEL page")
            lines.append("─" * 48)
        except Exception as e:
            lines = [f"(shell init: {e})", "type /help · F1 panel"]
        self.shell_lines.extend(lines)

    def shell_display(self, width: int) -> List[str]:
        if not self.shell_lines:
            return _wrap("SHELL page — F1 returns to PANEL", width)
        out: List[str] = []
        for line in self.shell_lines[-200:]:
            out.extend(_wrap(line, width))
        return out

    def draw_shell_page(self, stdscr, h: int, w: int, top: int) -> None:
        bot_menu, bot_input = 2, 2
        body_h = max(5, h - top - bot_menu - bot_input)
        frame = self.c(1)
        self._draw_box(stdscr, top, 0, body_h, w, frame)
        title = "▌ SHELL" if self.focus in ("input", "log") else "  SHELL"
        _safe_add(stdscr, top, 2, f" {title} · Domain REPL ", self.c(1) | curses.A_BOLD)

        inner_h = max(1, body_h - 2)
        inner_w = max(8, w - 4)
        self._inner_h = inner_h
        lines = self.shell_display(inner_w)
        max_ss = max(0, len(lines) - inner_h)
        self.shell_scroll = max(0, min(self.shell_scroll, max_ss))
        vis = lines[self.shell_scroll : self.shell_scroll + inner_h]
        for i in range(inner_h):
            row = top + 1 + i
            _safe_add(stdscr, row, 2, " " * inner_w)
            if i < len(vis):
                line = vis[i][:inner_w]
                attr = 0
                if line.startswith("shell>") or line.startswith("YOU"):
                    attr = self.c(2)
                elif line.startswith("◆") or line.startswith("agent"):
                    attr = self.c(1)
                _safe_add(stdscr, row, 2, line, attr)

        self._draw_menu_dock(stdscr, top + body_h, h, w)

    def _draw_menu_dock(self, stdscr, menu_y: int, h: int, w: int) -> None:
        _safe_add(stdscr, menu_y, 0, "═" * max(0, w - 1), self.c(1))
        menu = self.menu()
        x = 1
        y = menu_y + 1
        for i, (label, _k) in enumerate(menu):
            pill = f"[{label}]"
            if x + len(pill) >= w - 2:
                break
            sel = self.focus == "menu" and i == self.selected
            attr = curses.A_REVERSE | self.c(7) if sel else self.c(1)
            _safe_add(stdscr, y, x, pill, attr)
            x += len(pill) + 1

        if self.page == "panel":
            mode = {"chat": "CHAT", "menu": "MENU", "current": "CURRENT"}.get(
                self.focus, self.focus.upper()
            )
        else:
            mode = {"input": "SHELL", "menu": "MENU", "log": "LOG"}.get(
                self.focus, self.focus.upper()
            )
        foot = f" {mode} │ F1 PANEL · F2 SHELL │ {self.status}"
        _safe_add(
            stdscr,
            h - 2,
            0,
            foot[: max(0, w - 1)].ljust(max(0, w - 1))[: max(0, w - 1)],
            self.c(4),
        )
        prompt = " › " if self.page == "panel" else " shell> "
        shown = (prompt + self.input_buf)[-max(10, w - 3) :]
        bold = self.focus in ("chat", "input")
        attr = (curses.A_BOLD | self.c(2)) if bold else 0
        _safe_add(stdscr, h - 1, 0, shown.ljust(max(0, w - 1))[: max(0, w - 1)], attr)

    def draw(self, stdscr) -> None:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        if h < 16 or w < 56:
            _safe_add(stdscr, 0, 0, "Seat needs ≥16×56 terminal")
            stdscr.noutrefresh()
            curses.doupdate()
            return
        self.draw_header(stdscr, w)
        top = 2
        if self.page == "shell":
            self.ensure_shell_boot()
            self.draw_shell_page(stdscr, h, w, top)
        else:
            self.draw_panel_page(stdscr, h, w, top)
        stdscr.noutrefresh()
        curses.doupdate()

    # --- page switch -----------------------------------------------------

    def goto_panel(self) -> None:
        self.page = "panel"
        self.focus = "chat"
        self.selected = 0
        self.advanced = False
        self.st = self.host.load_state(self.root)
        self._be_label = _backend_label()
        self.status = "page: PANEL"

    def goto_shell(self) -> None:
        self.page = "shell"
        self.focus = "input"
        self.selected = 0
        self.ensure_shell_boot()
        self.st = self.host.load_state(self.root)
        self._be_label = _backend_label()
        self.status = "page: SHELL · /panel or F1 back"

    # --- chat / shell input ----------------------------------------------

    def panel_chat(self, text: str) -> None:
        try:
            from aether_fs import load_dotenv_files, read_current
            from aether_llm import apply_peer_backend, chat
            from aether_shell_agent import agent_chat_loop, resolve_agent_role, set_agent_role
        except ImportError as e:
            self.status = f"chat import error: {e}"
            return
        try:
            load_dotenv_files()
        except Exception:
            pass
        # Chatter = Grok session (TUI compute + thinking), not peer/ollama
        try:
            import os as _os
            _os.environ["AETHER_SHELL_AGENT_ROLE"] = "grok"
            _os.environ["AETHER_LLM_PROVIDER"] = "grok_tui"
            _os.environ.setdefault("AETHER_MODEL", "grok-4.5")
            _os.environ.setdefault("AETHER_REASONING_EFFORT", "high")
            set_agent_role("grok")
        except Exception:
            pass
        self.history.append({"role": "user", "content": text})
        try:
            from aether_llm import last_chat_meta
            cur = read_current(self.root) or ""
            # Prefer direct Grok chat (session + thoughts) over multi-tool peer loop
            from aether_shell import build_messages
            msgs = build_messages(self.root, self.history[-16:])
            # Domain injection: CURRENT always in system via build_messages
            reply = chat(msgs, temperature=0.35)
            meta = {}
            try:
                meta = last_chat_meta() or {}
            except Exception:
                meta = {}
            thinking = (meta.get("thinking") or "").strip()
            self.history.append(
                {
                    "role": "assistant",
                    "content": reply or "",
                    "thinking": thinking,
                    "provider": meta.get("provider") or "grok_tui",
                }
            )
            tools = meta.get("tools") or []
            self.status = "grok ready" + (f" · tools={','.join(tools[:3])}" if tools else "")
            self._be_label = _backend_label()
        except Exception as e:
            self.history.pop()
            self.status = f"grok: {e}"
        self.st = self.host.load_state(self.root)

    def shell_submit(self, text: str) -> None:
        """Process one shell line (slash / tool / agent chat)."""
        text = (text or "").strip()
        if not text:
            self.shell_lines.append("(waiting — silence is not permission)")
            return
        self.shell_lines.append(f"shell> {text}")

        # return to panel page
        if text.lower() in ("/panel", "/back", "/p", "panel"):
            self.goto_panel()
            return
        if text.lower() in ("bye", "quit", "exit", "q", "/quit", "/exit", "/q"):
            # stay in seat — go panel rather than kill app
            self.shell_lines.append("(use F1 / /panel for board · menu QUIT leaves seat)")
            self.goto_panel()
            return

        try:
            from aether_fs import read_current
            from aether_llm import chat
            from aether_shell import append_log, handle_slash, run_allowlisted
            from aether_shell_agent import agent_chat_loop, agent_mode_enabled
        except ImportError as e:
            self.shell_lines.append(f"(import error: {e})")
            return

        # bang tools
        if text.startswith("!") and not text.startswith("!="):
            body = text[1:].lstrip()
            try:
                argv = shlex.split(body) if body else []
            except ValueError as e:
                self.shell_lines.append(f"parse error: {e}")
                return
            out = run_allowlisted(self.root, argv)
            self.shell_lines.extend((out or "").splitlines() or [""])
            self.shell_scroll = 10**9
            return

        if text.startswith("/"):
            out = handle_slash(self.root, text, self.shell_hist)
            if out is None:
                # /quit family in handle_slash — treat as panel return
                self.goto_panel()
                return
            self.shell_lines.extend((out or "").splitlines() or [""])
            self.shell_scroll = 10**9
            self.st = self.host.load_state(self.root)
            self._be_label = _backend_label()
            return

        # Domain agent chat — default: personal-llm-sft-v4 (peer / Ollama on myarch)
        self.shell_hist.append({"role": "user", "content": text})
        try:
            append_log(self.root, "user", text)
        except Exception:
            pass
        try:
            import os as _os
            from aether_llm import apply_peer_backend, last_chat_meta
            from aether_shell import build_messages
            from aether_shell_agent import set_agent_role, agent_mode_enabled, agent_chat_loop

            # Shell page = YOUR model (PEER). Panel page keeps Grok session chatter.
            set_agent_role("peer")
            peer_line = apply_peer_backend(self.root, model="personal-llm-sft-v4")
            _os.environ["AETHER_OLLAMA_MODEL"] = "personal-llm-sft-v4"
            _os.environ["AETHER_MODEL"] = "personal-llm-sft-v4"
            if peer_line and not any(peer_line in ln for ln in self.shell_lines[-5:]):
                self.shell_lines.append(peer_line)

            cur = read_current(self.root) or ""
            if agent_mode_enabled():
                reply = agent_chat_loop(
                    self.root,
                    self.shell_hist[-16:],
                    chat_fn=chat,
                    current=cur,
                    temperature=0.35,
                )
            else:
                msgs = build_messages(self.root, self.shell_hist)
                reply = chat(msgs, temperature=0.45)
            thinking = ""
            try:
                thinking = (last_chat_meta() or {}).get("thinking") or ""
            except Exception:
                pass
            if thinking:
                tshow = thinking if len(thinking) <= 600 else thinking[:300] + " … "
                self.shell_lines.append("💭 " + tshow.replace("\n", " ")[:500])
            self.shell_hist.append(
                {"role": "assistant", "content": reply or "", "thinking": thinking}
            )
            try:
                append_log(self.root, "assistant", reply or "")
            except Exception:
                pass
            first = True
            for line in (reply or "(empty)").splitlines() or ["(empty)"]:
                if first:
                    self.shell_lines.append("◆ " + line)
                    first = False
                else:
                    self.shell_lines.append("  " + line)
        except Exception as e:
            self.shell_hist.pop()
            self.shell_lines.append(f"(llm error: {e})")
        self.shell_scroll = 10**9
        self.status = "shell ready"
        self._be_label = _backend_label()

    def run_menu_action(self, stdscr, key: str) -> bool:
        if key == "goto_panel":
            self.goto_panel()
            return False
        if key == "open_shell":
            self.goto_shell()
            return False
        if key == "shell_status":
            try:
                from aether_shell import status_line

                self.shell_lines.append(status_line(self.root))
            except Exception as e:
                self.shell_lines.append(str(e))
            self.shell_scroll = 10**9
            return False
        if key == "shell_help":
            try:
                from aether_shell import HELP

                self.shell_lines.extend(HELP.splitlines())
            except Exception:
                self.shell_lines.append("see docs/AETHER-SHELL.md")
            self.shell_scroll = 10**9
            return False
        if key == "shell_clear":
            self.shell_lines = ["(cleared)"]
            self.shell_hist = []
            self.shell_scroll = 0
            return False
        if key == "advanced":
            self.advanced = True
            self.selected = 0
            self.status = "Advanced"
            return False
        if key == "advanced_back":
            self.advanced = False
            self.selected = 0
            return False
        if key == "quit":
            return True
        if key == "help":
            self.st.detail = PLAYBOOK
            return False
        if key == "preflight_next" and self.page == "shell":
            # run into shell transcript
            nxt = self.st.next_action or ""
            if nxt:
                self.shell_submit(f"/preflight {nxt}")
            else:
                self.shell_lines.append("(no Next in CURRENT)")
            return False

        def prompt(p: str) -> Optional[str]:
            return self.host._prompt_line(stdscr, p)

        self.st = self.host._run_action(self.st, key, prompt, stdscr=stdscr)
        self.status = self.st.result or self.status
        self.st = self.host.load_state(self.st.root)
        self.root = self.st.root
        return False

    # --- main loop -------------------------------------------------------

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
            stdscr.clear()
            stdscr.refresh()
        except curses.error:
            pass
        self._init_colors()
        self._be_label = _backend_label()

        while True:
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

            # Global page tabs (work even while typing — F-keys only; digits only on menu)
            if ch == curses.KEY_F1:
                self.goto_panel()
                continue
            if ch == curses.KEY_F2:
                self.goto_shell()
                continue

            # Tab focus
            if ch == 9:
                if self.page == "panel":
                    order = ["chat", "menu", "current"]
                else:
                    order = ["input", "menu", "log"]
                try:
                    i = order.index(self.focus)
                except ValueError:
                    i = 0
                self.focus = order[(i + 1) % len(order)]
                try:
                    curses.curs_set(1 if self.focus in ("chat", "input") else 0)
                except curses.error:
                    pass
                continue

            if ch == 27:  # Esc
                if self.advanced:
                    self.advanced = False
                    self.selected = 0
                elif self.page == "shell":
                    self.goto_panel()
                continue

            # --- shell page keys ---
            if self.page == "shell":
                if self.focus == "log":
                    if ch in (curses.KEY_UP, ord("k")):
                        self.shell_scroll = max(0, self.shell_scroll - 1)
                    elif ch in (curses.KEY_DOWN, ord("j")):
                        self.shell_scroll += 1
                    elif ch == curses.KEY_PPAGE:
                        self.shell_scroll = max(0, self.shell_scroll - 10)
                    elif ch == curses.KEY_NPAGE:
                        self.shell_scroll += 10
                    continue
                if self.focus == "menu":
                    menu = self.menu()
                    if ch in (curses.KEY_LEFT, curses.KEY_UP):
                        self.selected = (self.selected - 1) % len(menu)
                        continue
                    if ch in (curses.KEY_RIGHT, curses.KEY_DOWN):
                        self.selected = (self.selected + 1) % len(menu)
                        continue
                    if ch in (curses.KEY_ENTER, 10, 13):
                        if self.run_menu_action(stdscr, menu[self.selected][1]):
                            return
                    continue
                # input focus
                if ch == curses.KEY_UP:
                    self.shell_scroll = max(0, self.shell_scroll - 1)
                    continue
                if ch == curses.KEY_DOWN:
                    self.shell_scroll += 1
                    continue
                if ch in (curses.KEY_BACKSPACE, 127, 8):
                    self.input_buf = self.input_buf[:-1]
                    continue
                if ch in (curses.KEY_ENTER, 10, 13):
                    text = self.input_buf
                    self.input_buf = ""
                    self.status = "…"
                    self.draw(stdscr)
                    self.shell_submit(text)
                    continue
                if 32 <= ch < 127:
                    self.input_buf += chr(ch)
                continue

            # --- panel page keys ---
            if self.focus == "current":
                if ch in (curses.KEY_UP, ord("k")):
                    self.current_scroll = max(0, self.current_scroll - 1)
                elif ch in (curses.KEY_DOWN, ord("j")):
                    self.current_scroll += 1
                elif ch == curses.KEY_PPAGE:
                    self.current_scroll = max(0, self.current_scroll - 10)
                elif ch == curses.KEY_NPAGE:
                    self.current_scroll += 10
                continue

            if self.focus == "menu":
                menu = self.menu()
                if ch in (curses.KEY_LEFT, curses.KEY_UP):
                    self.selected = (self.selected - 1) % len(menu)
                    continue
                if ch in (curses.KEY_RIGHT, curses.KEY_DOWN):
                    self.selected = (self.selected + 1) % len(menu)
                    continue
                if ch in (curses.KEY_ENTER, 10, 13):
                    if self.run_menu_action(stdscr, menu[self.selected][1]):
                        return
                # digit 1/2 as page switch only on menu focus
                if ch == ord("1"):
                    self.goto_panel()
                elif ch == ord("2"):
                    self.goto_shell()
                continue

            # chat focus
            if ch == curses.KEY_UP:
                self.chat_scroll = max(0, self.chat_scroll - 1)
                continue
            if ch == curses.KEY_DOWN:
                self.chat_scroll += 1
                continue
            if ch in (curses.KEY_BACKSPACE, 127, 8):
                self.input_buf = self.input_buf[:-1]
                continue
            if ch in (curses.KEY_ENTER, 10, 13):
                text = self.input_buf.strip()
                self.input_buf = ""
                if not text:
                    continue
                if text in ("/shell", ":shell", "/s"):
                    self.goto_shell()
                    continue
                if text in ("/playbook", "/help", "?"):
                    self.st.detail = PLAYBOOK
                    continue
                self.status = "thinking…"
                self.draw(stdscr)
                self.panel_chat(text)
                continue
            if 32 <= ch < 127:
                self.input_buf += chr(ch)


def run_fullscreen_tui(root: Path, host_mod) -> int:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        sys.stderr.write("aether panel: need interactive TTY\n")
        return 1
    app = PanelApp(root, host_mod)

    def _main(stdscr) -> None:
        app.loop(stdscr)

    try:
        curses.wrapper(_main)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        sys.stderr.write(f"aether panel TUI error: {e}\n")
        return 2
    return 0


def run_tmux_grok_split(root: Path) -> int:
    import shlex

    if not shutil.which("tmux"):
        sys.stderr.write("aether panel --grok-split needs tmux\n")
        return 1
    grok = os.environ.get("GROK_BIN") or shutil.which("grok") or "grok"
    right = f"watch -n 1 -c cat {shlex.quote(str(root / 'CURRENT.md'))}"
    session = f"mech-panel-{os.getpid()}"
    subprocess.call(["tmux", "new-session", "-d", "-s", session, "-c", str(root), grok])
    subprocess.call(["tmux", "split-window", "-h", "-t", session, right])
    subprocess.call(["tmux", "select-pane", "-t", f"{session}.0"])
    os.execvp("tmux", ["tmux", "attach", "-t", session])
    return 0
