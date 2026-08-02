#!/usr/bin/env python3
"""Mechanicall seat TUI — PANEL | SHELL pages, Grok padding, sparse inbox.

Grok Build padding (docs/user-guide theming):
  outer_vpad=1  outer_hpad=3  block_pad=3  msg_gap=2  max_thoughts_width=72

Actions dock: hidden by default (F3 toggle), right-aligned when open.
Shell default: personal-llm-sft-v4 peer via Ollama. Panel chat: Grok session.
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


class GrokPad:
    outer_vpad: int = 1
    outer_hpad_left: int = 3
    outer_hpad_right: int = 3
    block_pad_left: int = 3
    block_pad_right: int = 3
    msg_gap: int = 2
    header_rows: int = 2
    menu_rows: int = 1          # closed (status only)
    menu_rows_open: int = 2     # open (actions strip + status)
    input_rows: int = 2
    max_thoughts_width: int = 72
    max_history_turns: int = 10
    max_thinking_chars: int = 220
    min_cols: int = 56
    min_rows: int = 16


PAD = GrokPad()

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
    ("Switch project…", "switch_project"),
    ("Open PROPOSE…", "open_propose"),
    ("Events", "events"),
    ("Write PANEL files", "write"),
    ("Create CURRENT", "current_init"),
    ("Playbook", "help"),
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

PLAYBOOK = """\
AETHER SEAT
F1 PANEL · F2 SHELL · F3 actions (toggle, right-aligned when open)
Shell = personal-llm-sft-v4 peer (Ollama). Panel chat = Grok session.
Human APPROVE only. docs/PANEL-GROK-SPLIT.md · docs/AETHER-SHELL.md
"""


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


class PanelApp:
    def __init__(self, root: Path, host_mod) -> None:
        self.root = root
        self.host = host_mod
        self.st = host_mod.load_state(root)
        self.page = "panel"
        self.history: List[dict] = []
        self.shell_lines: List[str] = []
        self.shell_hist: List[dict] = []
        self.focus = "chat"
        self.selected = 0
        self.input_buf = ""
        self.chat_scroll = 0
        self.current_scroll = 0
        self.shell_scroll = 0
        self.status = "F3 actions · F1/F2 pages · type to chat"
        self.advanced = False
        self.show_actions = False
        self._colors = False
        self._inner_h = 10
        self._be_label = _backend_label()
        self._shell_booted = False

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

    def menu(self) -> List[Action]:
        if self.page == "shell":
            return SHELL_ACTIONS
        return ADVANCED_ACTIONS if self.advanced else MAIN_ACTIONS

    def _bot_rows(self) -> int:
        mr = PAD.menu_rows_open if self.show_actions else PAD.menu_rows
        return mr + PAD.input_rows

    def draw_header(self, stdscr, w: int) -> None:
        L = PAD.outer_hpad_left
        line0 = " MECHANICALL SEAT  ·  GOP  ·  F3 actions "
        _safe_add(stdscr, 0, 0, line0.ljust(w)[: max(0, w - 1)], self.c(6) | curses.A_BOLD)
        _safe_add(stdscr, 1, 0, " " * max(0, w - 1), self.c(8))
        p_attr = self.c(9) | curses.A_BOLD if self.page == "panel" else self.c(8) | curses.A_BOLD
        s_attr = self.c(9) | curses.A_BOLD if self.page == "shell" else self.c(8) | curses.A_BOLD
        _safe_add(stdscr, 1, L, " F1 PANEL ", p_attr)
        _safe_add(stdscr, 1, L + 11, " F2 SHELL ", s_attr)
        proj = (self.st.project_label or self.root.name)[:14]
        nxt = (self.st.next_action or "—")[:22]
        meta = f"  {proj}  ·  {nxt}  ·  {self._be_label}"
        _safe_add(stdscr, 1, L + 22, meta[: max(0, w - L - 22 - PAD.outer_hpad_right)], self.c(8))

    def chat_display(self, width: int) -> List[str]:
        w = max(8, min(width, PAD.max_thoughts_width))
        if not self.history:
            return ["", "", "  chat", "", "  type below", "  F3 · actions", ""]
        lines: List[str] = [""]
        gap = [""] * PAD.msg_gap

        def emit(prefix: str, cont: str, body: str, max_lines: int) -> None:
            body = (body or "").strip()
            if not body:
                return
            wrapped = _wrap(body, max(8, w - len(prefix)))
            if len(wrapped) > max_lines:
                wrapped = wrapped[: max_lines - 1] + ["…"]
            for i, wl in enumerate(wrapped):
                lines.append((prefix if i == 0 else cont) + wl)

        for m in self.history[-PAD.max_history_turns :]:
            role = m.get("role") or ""
            content = (m.get("content") or "").strip()
            thinking = (m.get("thinking") or "").strip()
            if role == "user":
                emit("  you    ", "         ", content, 6)
            else:
                if thinking:
                    tshow = thinking[: PAD.max_thinking_chars]
                    if len(thinking) > PAD.max_thinking_chars:
                        tshow += "…"
                    emit("  think  ", "         ", tshow, 3)
                emit("  grok   ", "         ", content or "(empty)", 8)
            lines.extend(gap)
        while lines and lines[-1] == "":
            lines.pop()
        return lines + [""]

    def current_text(self) -> str:
        cf = self.root / "CURRENT.md"
        if not cf.is_file():
            return "(no CURRENT.md)"
        try:
            body = cf.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return f"(read error: {e})"
        # compact pin + body (less dense)
        pin = f"NEXT  {self.st.next_action}\n{self.st.phase} · {self.st.status}\n\n"
        return pin + body

    def draw_panel_page(self, stdscr, h: int, w: int, top: int) -> None:
        L, R = PAD.outer_hpad_left, PAD.outer_hpad_right
        BL, BR = PAD.block_pad_left, PAD.block_pad_right
        bot = self._bot_rows()
        x0 = L
        usable_w = max(20, w - L - R)
        body_h = max(6, h - top - bot - PAD.outer_vpad)
        mid = max(16, int(usable_w * 0.58))  # chat gets more width
        if usable_w - mid < 16:
            mid = max(12, usable_w - 16)
        right_w = usable_w - mid
        frame = self.c(1)
        self._draw_box(stdscr, top, x0, body_h, mid, frame)
        self._draw_box(stdscr, top, x0 + mid, body_h, right_w, frame)
        _safe_add(stdscr, top, x0 + BL, " chat ", self.c(1) | curses.A_BOLD)
        _safe_add(stdscr, top, x0 + mid + BL, " CURRENT ", self.c(3) | curses.A_BOLD)

        inner_h = max(1, body_h - 3)
        inner_w_l = max(8, mid - BL - BR - 2)
        inner_w_r = max(8, right_w - BL - BR - 2)
        self._inner_h = inner_h
        cy = top + 2  # title row + air

        chat_lines = self.chat_display(inner_w_l)
        max_cs = max(0, len(chat_lines) - inner_h)
        self.chat_scroll = max(0, min(self.chat_scroll, max_cs))
        # auto-stick to bottom when near end
        vis = chat_lines[self.chat_scroll : self.chat_scroll + inner_h]
        cx = x0 + 1 + BL
        for i in range(inner_h):
            row = cy + i
            _safe_add(stdscr, row, cx, " " * inner_w_l)
            if i < len(vis):
                line = vis[i][:inner_w_l]
                attr = 0
                if "you" in line[:8]:
                    attr = self.c(2)
                elif "grok" in line[:8] or line.strip().startswith("◆"):
                    attr = self.c(1) | curses.A_BOLD
                elif "think" in line[:10]:
                    attr = self.c(4)
                _safe_add(stdscr, row, cx, line, attr)

        cur_lines = _wrap(self.current_text(), min(inner_w_r, 56))
        max_rs = max(0, len(cur_lines) - inner_h)
        self.current_scroll = max(0, min(self.current_scroll, max_rs))
        vis_r = cur_lines[self.current_scroll : self.current_scroll + inner_h]
        rx = x0 + mid + 1 + BL
        for i in range(inner_h):
            row = cy + i
            _safe_add(stdscr, row, rx, " " * inner_w_r)
            if i < len(vis_r):
                attr = self.c(3) if i < 2 and self.current_scroll == 0 else 0
                _safe_add(stdscr, row, rx, vis_r[i][:inner_w_r], attr)

        self._draw_menu_dock(stdscr, top + body_h, h, w)

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
            set_agent_role("peer")
            peer = apply_peer_backend(self.root, model="personal-llm-sft-v4:latest")
            self.shell_lines = [
                "",
                "  shell  ·  peer sft-v4",
                f"  {status_line(self.root)[:70]}",
                f"  {peer}",
                f"  {describe_backend()}",
                "",
                "  type to chat about CURRENT · drafts only",
                "  F1 panel · F3 actions",
                "",
            ]
        except Exception as e:
            self.shell_lines = ["", f"  shell init: {e}", ""]

    def shell_display(self, width: int) -> List[str]:
        w = max(8, min(width, PAD.max_thoughts_width))
        if not self.shell_lines:
            return ["", "  shell", ""]
        out: List[str] = []
        for line in self.shell_lines[-50:]:
            out.extend(_wrap(line, w))
        return out

    def draw_shell_page(self, stdscr, h: int, w: int, top: int) -> None:
        L, R = PAD.outer_hpad_left, PAD.outer_hpad_right
        BL, BR = PAD.block_pad_left, PAD.block_pad_right
        bot = self._bot_rows()
        x0 = L
        usable_w = max(20, w - L - R)
        body_h = max(6, h - top - bot - PAD.outer_vpad)
        frame = self.c(1)
        self._draw_box(stdscr, top, x0, body_h, usable_w, frame)
        _safe_add(stdscr, top, x0 + BL, " shell ", self.c(1) | curses.A_BOLD)
        inner_h = max(1, body_h - 3)
        inner_w = max(8, usable_w - BL - BR - 2)
        self._inner_h = inner_h
        lines = self.shell_display(inner_w)
        max_ss = max(0, len(lines) - inner_h)
        self.shell_scroll = max(0, min(self.shell_scroll, max_ss))
        vis = lines[self.shell_scroll : self.shell_scroll + inner_h]
        cx = x0 + 1 + BL
        cy = top + 2
        for i in range(inner_h):
            row = cy + i
            _safe_add(stdscr, row, cx, " " * inner_w)
            if i < len(vis):
                line = vis[i][:inner_w]
                attr = self.c(2) if "you" in line[:10] else (self.c(1) if "peer" in line[:10] else 0)
                _safe_add(stdscr, row, cx, line, attr)
        self._draw_menu_dock(stdscr, top + body_h, h, w)

    def _draw_menu_dock(self, stdscr, menu_y: int, h: int, w: int) -> None:
        L, R = PAD.outer_hpad_left, PAD.outer_hpad_right
        usable = max(10, w - L - R)
        if self.page == "panel":
            mode = {"chat": "CHAT", "menu": "MENU", "current": "CURRENT"}.get(
                self.focus, "?"
            )
        else:
            mode = {"input": "SHELL", "menu": "MENU", "log": "LOG"}.get(self.focus, "?")

        if self.show_actions:
            _safe_add(stdscr, menu_y, L, "─" * usable, self.c(1))
            menu = self.menu()
            # build strip then right-align
            parts = []
            for i, (label, _) in enumerate(menu):
                parts.append((f"[{label}]", self.focus == "menu" and i == self.selected))
            total = sum(len(t) + 1 for t, _ in parts) - (1 if parts else 0)
            x = max(L, w - R - max(total, 1))
            y = menu_y + 1
            for text, sel in parts:
                attr = (curses.A_REVERSE | self.c(7)) if sel else self.c(1)
                if x + len(text) < w - R:
                    _safe_add(stdscr, y, x, text, attr)
                x += len(text) + 1
            foot = f" {mode} │ F3 hide actions │ {self.status}"
        else:
            foot = f" {mode} │ F3 show actions │ F1/F2 │ {self.status}"

        _safe_add(stdscr, h - 2, L, foot[:usable].ljust(usable)[:usable], self.c(4))
        prompt = " › " if self.page == "panel" else " shell> "
        lead = " " * (L + PAD.block_pad_left)
        shown = (lead + prompt + self.input_buf)[-(w - R - 1) :]
        bold = self.focus in ("chat", "input")
        attr = (curses.A_BOLD | self.c(2)) if bold else 0
        _safe_add(stdscr, h - 1, 0, shown.ljust(max(0, w - 1))[: max(0, w - 1)], attr)

    def draw(self, stdscr) -> None:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        if h < PAD.min_rows or w < PAD.min_cols:
            _safe_add(stdscr, 0, 0, f"need ≥{PAD.min_rows}×{PAD.min_cols}")
            stdscr.noutrefresh()
            curses.doupdate()
            return
        self.draw_header(stdscr, w)
        top = PAD.header_rows + PAD.outer_vpad
        if self.page == "shell":
            self.ensure_shell_boot()
            self.draw_shell_page(stdscr, h, w, top)
        else:
            self.draw_panel_page(stdscr, h, w, top)
        stdscr.noutrefresh()
        curses.doupdate()

    def goto_panel(self) -> None:
        self.page = "panel"
        self.focus = "chat"
        self.selected = 0
        self.advanced = False
        self.st = self.host.load_state(self.root)
        self._be_label = _backend_label()
        self.status = "panel"

    def goto_shell(self) -> None:
        self.page = "shell"
        self.focus = "input"
        self.selected = 0
        self.ensure_shell_boot()
        self.st = self.host.load_state(self.root)
        self._be_label = _backend_label()
        self.status = "shell · peer sft-v4"

    def panel_chat(self, text: str) -> None:
        try:
            import os as _os
            from aether_fs import load_dotenv_files, read_current
            from aether_llm import chat, last_chat_meta
            from aether_shell import build_messages
            from aether_shell_agent import set_agent_role

            load_dotenv_files()
            # Force Grok session model — never leave peer/ollama model id (setdefault fails after F2)
            _os.environ["AETHER_LLM_PROVIDER"] = "grok_tui"
            _os.environ["AETHER_SHELL_AGENT_ROLE"] = "grok"
            _os.environ["AETHER_MODEL"] = "grok-4.5"
            _os.environ.pop("AETHER_OLLAMA_MODEL", None)
            _os.environ.setdefault("AETHER_REASONING_EFFORT", "high")
            _os.environ.setdefault("AETHER_GROK_OUTPUT_FORMAT", "streaming-json")
            set_agent_role("grok")
        except Exception as e:
            self.status = f"init: {e}"
            return
        self.history.append({"role": "user", "content": text})
        try:
            msgs = build_messages(self.root, self.history[-12:])
            reply = chat(msgs, temperature=0.35)
            meta = {}
            try:
                meta = last_chat_meta() or {}
            except Exception:
                pass
            thinking = (meta.get("thinking") or "").strip()
            self.history.append(
                {"role": "assistant", "content": reply or "", "thinking": thinking}
            )
            self.status = "grok ready"
            self._be_label = _backend_label()
            # stick scroll to end
            self.chat_scroll = 10**9
        except Exception as e:
            self.history.pop()
            self.status = f"grok: {e}"[:50]
        self.st = self.host.load_state(self.root)

    def shell_submit(self, text: str) -> None:
        text = (text or "").strip()
        if not text:
            self.shell_lines.append("")
            self.shell_lines.append("  (waiting)")
            self.shell_lines.append("")
            return
        self.shell_lines.append("")
        self.shell_lines.append(f"  you    {text}")
        self.shell_lines.append("")

        if text.lower() in ("/panel", "/back", "/p", "panel"):
            self.goto_panel()
            return
        if text.lower() in ("bye", "quit", "exit", "q", "/quit", "/exit", "/q"):
            self.goto_panel()
            return

        try:
            from aether_llm import apply_peer_backend, chat
            from aether_shell import append_log, build_messages, handle_slash, run_allowlisted
            from aether_shell_agent import set_agent_role
        except ImportError as e:
            self.shell_lines.append(f"  (import error: {e})")
            return

        if text.startswith("!") and not text.startswith("!="):
            try:
                argv = shlex.split(text[1:].lstrip()) if text[1:].strip() else []
            except ValueError as e:
                self.shell_lines.append(f"  parse: {e}")
                return
            out = run_allowlisted(self.root, argv)
            for ln in (out or "").splitlines():
                self.shell_lines.append(f"  {ln}")
            self.shell_lines.append("")
            self.shell_scroll = 10**9
            return

        if text.startswith("/"):
            out = handle_slash(self.root, text, self.shell_hist)
            if out is None:
                self.goto_panel()
                return
            for ln in (out or "").splitlines():
                self.shell_lines.append(f"  {ln}")
            self.shell_lines.append("")
            self.shell_scroll = 10**9
            self.st = self.host.load_state(self.root)
            return

        self.shell_hist.append({"role": "user", "content": text})
        try:
            append_log(self.root, "user", text)
        except Exception:
            pass
        try:
            set_agent_role("peer")
            # Free chat only — no agent_mode_enabled (lives in aether_shell, not shell_agent)
            peer = apply_peer_backend(self.root, model="personal-llm-sft-v4:latest")
            os.environ["AETHER_LLM_PROVIDER"] = "ollama"
            os.environ["AETHER_OLLAMA_MODEL"] = "personal-llm-sft-v4:latest"
            os.environ["AETHER_MODEL"] = "personal-llm-sft-v4:latest"
            os.environ.setdefault("AETHER_OLLAMA_NUM_CTX", "8192")
            os.environ.setdefault("OLLAMA_HOST", "http://192.168.1.241:11434")
            msgs = build_messages(self.root, self.shell_hist)
            reply = chat(msgs, temperature=0.35)
            self.shell_hist.append({"role": "assistant", "content": reply or ""})
            try:
                append_log(self.root, "assistant", reply or "")
            except Exception:
                pass
            self.shell_lines.append("")
            first = True
            for line in (reply or "(empty)").splitlines() or ["(empty)"]:
                if first:
                    self.shell_lines.append(f"  peer   {line}")
                    first = False
                else:
                    self.shell_lines.append(f"         {line}")
            self.shell_lines.append("")
            self.status = "peer ready"
        except Exception as e:
            if self.shell_hist and self.shell_hist[-1].get("role") == "user":
                self.shell_hist.pop()
            self.shell_lines.append(f"  (llm error: {e})")
            self.shell_lines.append("  tip: myarch ollama up?  OLLAMA_HOST=http://192.168.1.241:11434")
            self.shell_lines.append("")
            self.status = f"err: {e}"[:48]
        self.shell_scroll = 10**9
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

                self.shell_lines.append(f"  {status_line(self.root)}")
            except Exception as e:
                self.shell_lines.append(f"  {e}")
            self.shell_scroll = 10**9
            return False
        if key == "shell_help":
            try:
                from aether_shell import HELP

                for ln in HELP.splitlines()[:30]:
                    self.shell_lines.append(f"  {ln}")
            except Exception:
                self.shell_lines.append("  docs/AETHER-SHELL.md")
            self.shell_scroll = 10**9
            return False
        if key == "shell_clear":
            self.shell_lines = ["", "  (cleared)", ""]
            self.shell_hist = []
            return False
        if key == "advanced":
            self.advanced = True
            self.show_actions = True
            self.selected = 0
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
            nxt = self.st.next_action or ""
            if nxt:
                self.shell_submit(f"/preflight {nxt}")
            return False

        def prompt(p: str) -> Optional[str]:
            return self.host._prompt_line(stdscr, p)

        self.st = self.host._run_action(self.st, key, prompt, stdscr=stdscr)
        self.status = self.st.result or self.status
        self.st = self.host.load_state(self.st.root)
        self.root = self.st.root
        return False

    def loop(self, stdscr) -> None:
        try:
            curses.curs_set(1)
            curses.raw()
        except curses.error:
            pass
        stdscr.keypad(True)
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
                _safe_add(stdscr, h - 1, 0, " any key ")
                stdscr.refresh()
                stdscr.getch()
                self.st.detail = ""
                continue

            self.draw(stdscr)
            ch = stdscr.getch()

            if ch == curses.KEY_F1:
                self.goto_panel()
                continue
            if ch == curses.KEY_F2:
                self.goto_shell()
                continue
            if ch == curses.KEY_F3:
                self.show_actions = not self.show_actions
                if self.show_actions:
                    self.focus = "menu"
                    self.selected = 0
                    self.status = "actions · arrows · Enter · F3 hide"
                else:
                    self.focus = "chat" if self.page == "panel" else "input"
                    self.status = "actions hidden"
                continue

            if ch == 9:  # Tab
                if self.page == "panel":
                    order = (
                        ["chat", "menu", "current"]
                        if self.show_actions
                        else ["chat", "current"]
                    )
                else:
                    order = (
                        ["input", "menu", "log"] if self.show_actions else ["input", "log"]
                    )
                try:
                    i = order.index(self.focus)
                except ValueError:
                    i = 0
                self.focus = order[(i + 1) % len(order)]
                continue

            if ch == 27:
                if self.advanced:
                    self.advanced = False
                elif self.show_actions:
                    self.show_actions = False
                    self.focus = "chat" if self.page == "panel" else "input"
                elif self.page == "shell":
                    self.goto_panel()
                continue

            if self.page == "shell":
                if self.focus == "log":
                    if ch in (curses.KEY_UP,):
                        self.shell_scroll = max(0, self.shell_scroll - 1)
                    elif ch in (curses.KEY_DOWN,):
                        self.shell_scroll += 1
                    continue
                if self.focus == "menu" and self.show_actions:
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
                if ch == curses.KEY_UP:
                    self.shell_scroll = max(0, self.shell_scroll - 1)
                    continue
                if ch == curses.KEY_DOWN:
                    self.shell_scroll += 1
                    continue
                if 32 <= ch < 127:
                    self.input_buf += chr(ch)
                continue

            # panel page
            if self.focus == "current":
                if ch == curses.KEY_UP:
                    self.current_scroll = max(0, self.current_scroll - 1)
                elif ch == curses.KEY_DOWN:
                    self.current_scroll += 1
                continue
            if self.focus == "menu" and self.show_actions:
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
                if text in ("/shell", "/s"):
                    self.goto_shell()
                    continue
                self.status = "…"
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
        sys.stderr.write("needs tmux\n")
        return 1
    grok = os.environ.get("GROK_BIN") or shutil.which("grok") or "grok"
    right = f"watch -n 1 -c cat {shlex.quote(str(root / 'CURRENT.md'))}"
    session = f"mech-panel-{os.getpid()}"
    subprocess.call(["tmux", "new-session", "-d", "-s", session, "-c", str(root), grok])
    subprocess.call(["tmux", "split-window", "-h", "-t", session, right])
    os.execvp("tmux", ["tmux", "attach", "-t", session])
    return 0
