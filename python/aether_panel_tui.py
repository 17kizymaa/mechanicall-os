#!/usr/bin/env python3
"""Mechanicall seat TUI — PANEL | SHELL pages, Grok padding, sparse inbox.

Grok Build padding (docs/user-guide theming):
  outer_vpad=1  outer_hpad=3  block_pad=3  msg_gap=2  max_thoughts_width=72

Dock (bottom, top→bottom): [actions F3, flush-right] · filled input · status/F3 hints.
Status bar sits at the very bottom (right-biased hints). Actions stay above input.
Chat: bottom-aligned; filled bubbles + emphasis.
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
# chat line: (kind, text)
# kind = pad|you|think|tool|sub|grok|peer|meta|plain
ChatLine = Tuple[str, str]


class GrokPad:
    """Seat chatbox tokens — Grok Build *layout language*, not the real binary."""
    outer_vpad: int = 1
    outer_hpad_left: int = 3
    outer_hpad_right: int = 3
    block_pad_left: int = 3
    block_pad_right: int = 3
    msg_gap: int = 1
    header_rows: int = 2
    menu_rows: int = 0          # closed — no action strip
    menu_rows_open: int = 1     # open — right-packed actions at bottom
    input_rows: int = 2         # status + filled input (input sits above actions)
    # R-09: do not hard-cap answers to a tiny bubble; scroll full transcript
    max_thoughts_width: int = 200
    max_history_turns: int = 12
    max_thinking_chars: int = 12000   # was 220 — that hid the whole think strip
    max_thinking_lines: int = 80
    max_reply_lines: int = 2000       # was hard-coded 8 — root of "finished but gone"
    max_user_lines: int = 40
    max_tool_lines: int = 4
    min_cols: int = 56
    min_rows: int = 16
    bubble_hpad: int = 1        # spaces inside filled bubble
    chat_top_air: int = 0       # unused when bottom-aligning
    page_scroll_step: int = 8   # PgUp/PgDn


PAD = GrokPad()

MAIN_ACTIONS: List[Action] = [
    ("APPROVE", "approve"),
    ("REJECT", "reject"),
    ("REFRESH", "refresh"),
    ("SHELL", "open_shell"),
    ("YANK LAST", "yank_last"),
    ("EXPAND", "expand_last"),
    ("PASTE", "paste_input"),
    ("→ CURRENT", "paste_current"),
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
    ("YANK LAST", "yank_last"),
    ("EXPAND", "expand_last"),
    ("PASTE", "paste_input"),
    ("→ CURRENT", "paste_current"),
    ("PREFLIGHT NEXT", "preflight_next"),
    ("STATUS", "shell_status"),
    ("HELP", "shell_help"),
    ("CLEAR", "shell_clear"),
    ("QUIT", "quit"),
]

PLAYBOOK = """\
AETHER SEAT
F1 PANEL · F2 SHELL · F3 actions (right-packed, below input)
Chatbox = Grok Build transcript mimic: you · ··· think · ▸ tools · grok answer
Scroll: ↑↓ PgUp/PgDn · Ctrl+E expand last · Ctrl+Y yank · Ctrl+V paste · Ctrl+T →CURRENT
Full reply also written to .aether/last-reply.md after each turn
Shell = personal-llm-sft-v4 peer. Panel chat = Grok session (web_search on unless denied).
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


def _safe_hline(win, y: int, x: int, ch: int, n: int, attr: int = 0) -> None:
    try:
        h, w = win.getmaxyx()
        if y < 0 or y >= h or n <= 0:
            return
        n = min(n, max(0, w - x - 1))
        if n <= 0:
            return
        win.attron(attr)
        win.hline(y, x, ch, n)
        win.attroff(attr)
    except curses.error:
        pass


def _fill_row(win, y: int, x: int, width: int, attr: int = 0) -> None:
    """Paint a solid horizontal run (filled bar / bubble body)."""
    if width <= 0:
        return
    try:
        h, w = win.getmaxyx()
        if y < 0 or y >= h or x >= w:
            return
        width = min(width, max(0, w - x - 1))
        if width <= 0:
            return
        win.addnstr(y, x, " " * width, width, attr)
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



def mirror_last_reply(root: Path, reply: str, thinking: str = "", tools=None) -> Path:
    """Write full turn body to .aether/last-reply.md (FS truth; survives truncate bugs)."""
    tools = tools or []
    adir = Path(root) / ".aether"
    try:
        adir.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    path = adir / "last-reply.md"
    parts = ["# last panel/shell reply\n"]
    if tools:
        parts.append("## tools\n")
        for t in tools:
            parts.append(f"- {t}\n")
        parts.append("\n")
    if (thinking or "").strip():
        parts.append("## thinking\n\n")
        parts.append(thinking.strip())
        parts.append("\n\n")
    parts.append("## answer\n\n")
    parts.append((reply or "").strip() or "(empty)")
    parts.append("\n")
    try:
        path.write_text("".join(parts), encoding="utf-8")
    except OSError:
        pass
    return path


def _wl_run(args: list, *, input_bytes: Optional[bytes] = None) -> Optional[bytes]:
    try:
        r = subprocess.run(
            args,
            input=input_bytes,
            capture_output=True,
            timeout=5,
        )
        if r.returncode == 0:
            return r.stdout if input_bytes is None else b""
    except Exception:
        pass
    return None


def clipboard_copy(text: str) -> Tuple[bool, str]:
    """Copy text to Wayland clipboard + primary (for highlight parity) + file."""
    text = text or ""
    if not text.strip():
        return False, "nothing to copy"
    data = text.encode("utf-8", errors="replace")
    wl = shutil.which("wl-copy")
    ok_clip = False
    if wl:
        # clipboard
        if _wl_run([wl, "--"], input_bytes=data) is not None:
            ok_clip = True
        # primary — so middle-click / highlight-aware tools see it too
        _wl_run([wl, "--primary", "--"], input_bytes=data)
    if ok_clip:
        # keep file mirror for /tocurrent when WAYLAND flaky
        try:
            clip = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "aether-clip.txt"
            clip.write_text(text, encoding="utf-8")
        except OSError:
            pass
        return True, f"copied {len(text)} chars"
    # OSC 52 — foot may accept into clipboard
    try:
        import base64

        b64 = base64.b64encode(data).decode("ascii")
        if len(b64) < 100_000:
            sys.stdout.write(f"\033]52;c;{b64}\a")
            sys.stdout.flush()
            return True, f"copied {len(text)} chars (osc52)"
    except Exception:
        pass
    try:
        clip = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "aether-clip.txt"
        clip.write_text(text, encoding="utf-8")
        return True, f"copied {len(text)} chars → {clip.name} (file)"
    except OSError as e:
        return False, f"copy failed: {e}"


def clipboard_paste(*, prefer_primary: bool = False) -> Tuple[bool, str]:
    """Paste from Wayland. prefer_primary=True: highlight (primary) first."""
    wl = shutil.which("wl-paste")
    if wl:
        order = (["-p", "-n"], ["-n"]) if prefer_primary else (["-n"], ["-p", "-n"])
        for args in order:
            out = _wl_run([wl, *args])
            if out:
                return True, out.decode("utf-8", errors="replace")
    try:
        clip = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "aether-clip.txt"
        if clip.is_file():
            return True, clip.read_text(encoding="utf-8", errors="replace")
    except OSError:
        pass
    return False, ""


def clipboard_read_highlight() -> Tuple[bool, str]:
    """Read foot/Wayland *highlighted* text (primary selection only)."""
    wl = shutil.which("wl-paste")
    if not wl:
        return False, ""
    out = _wl_run([wl, "-p", "-n"])
    if out and out.strip():
        return True, out.decode("utf-8", errors="replace")
    return False, ""


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
        self._last_reply = ""  # last peer/grok text for yank

    def _init_colors(self) -> None:
        """GrokNight-class editorial palette (256-color preferred)."""
        if not curses.has_colors():
            return
        try:
            curses.start_color()
            curses.use_default_colors()
            if curses.COLORS >= 256:
                # Neutrals + mauve accent (professional, not rainbow terminal)
                curses.init_pair(1, 240, -1)        # border dim
                curses.init_pair(2, 114, -1)        # success
                curses.init_pair(3, 252, -1)        # primary text
                curses.init_pair(4, 179, -1)        # warm warn / next
                curses.init_pair(5, 203, -1)        # danger
                curses.init_pair(6, 255, 176)       # brand / accent inverse
                curses.init_pair(7, 236, 245)       # secondary chip (CURRENT label)
                curses.init_pair(8, 250, 236)       # header bar fill
                curses.init_pair(9, 232, 114)       # active page chip
                curses.init_pair(10, 232, 187)      # you bubble (soft gold)
                curses.init_pair(11, 255, 60)       # agent bubble (deep mauve/blue-ish)
                curses.init_pair(12, 245, 238)      # think strip
                curses.init_pair(13, 245, -1)       # meta muted
                curses.init_pair(14, 250, 235)      # dock track
                curses.init_pair(15, 255, 238)      # input field
                curses.init_pair(16, 236, 179)      # action chip idle
                curses.init_pair(17, 252, 239)      # tool
                curses.init_pair(18, 176, 236)      # subagent / dim accent
                curses.init_pair(19, 176, -1)       # accent fg
                curses.init_pair(20, 111, -1)       # cool CURRENT accent
            else:
                curses.init_pair(1, curses.COLOR_WHITE, -1)
                curses.init_pair(2, curses.COLOR_GREEN, -1)
                curses.init_pair(3, curses.COLOR_WHITE, -1)
                curses.init_pair(4, curses.COLOR_YELLOW, -1)
                curses.init_pair(5, curses.COLOR_RED, -1)
                curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
                curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
                curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
                curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)
                curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_YELLOW)
                curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
                curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
                curses.init_pair(13, curses.COLOR_WHITE, -1)
                curses.init_pair(14, curses.COLOR_WHITE, curses.COLOR_BLACK)
                curses.init_pair(15, curses.COLOR_BLACK, curses.COLOR_WHITE)
                curses.init_pair(16, curses.COLOR_BLACK, curses.COLOR_YELLOW)
                curses.init_pair(17, curses.COLOR_CYAN, curses.COLOR_BLACK)
                curses.init_pair(18, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
                curses.init_pair(19, curses.COLOR_MAGENTA, -1)
                curses.init_pair(20, curses.COLOR_CYAN, -1)
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
        """status + input, plus action strip when open (input above actions)."""
        mr = PAD.menu_rows_open if self.show_actions else PAD.menu_rows
        return mr + PAD.input_rows

    def draw_header(self, stdscr, w: int) -> None:
        L = PAD.outer_hpad_left
        # Row 0 — brand (unmistakable redesign marker)
        brand = " MECHANICALL "
        _fill_row(stdscr, 0, 0, max(0, w - 1), self.c(6) | curses.A_BOLD)
        _safe_add(stdscr, 0, 0, brand, self.c(6) | curses.A_BOLD)
        rest = f" seat  ·  design v3  ·  {self.st.project_label or self.root.name}"
        _safe_add(
            stdscr,
            0,
            len(brand),
            rest[: max(0, w - 1 - len(brand))],
            self.c(6),
        )
        # Row 1 — page chips + authority chips
        _fill_row(stdscr, 1, 0, max(0, w - 1), self.c(8))
        p_on = self.page == "panel"
        s_on = self.page == "shell"
        p_attr = (self.c(9) | curses.A_BOLD) if p_on else (self.c(8) | curses.A_BOLD)
        s_attr = (self.c(9) | curses.A_BOLD) if s_on else (self.c(8) | curses.A_BOLD)
        _safe_add(stdscr, 1, L, "  PANEL  ", p_attr)
        _safe_add(stdscr, 1, L + 10, "  SHELL  ", s_attr)
        # Domain chips (right side of header)
        nxt = (self.st.next_action or "—")[:20]
        phase = (self.st.phase or "—")[:12]
        appr = (self.st.approval or "—")[:10]
        chips = f"  NEXT {nxt}   PHASE {phase}   {appr}  "
        cx = max(L + 24, w - len(chips) - PAD.outer_hpad_right - 1)
        if cx + len(chips) < w - 1:
            _safe_add(stdscr, 1, cx, chips[: max(0, w - 1 - cx)], self.c(4) | curses.A_BOLD)
        else:
            meta = f"  {nxt}  ·  {self._be_label}"
            _safe_add(stdscr, 1, L + 22, meta[: max(0, w - L - 22 - PAD.outer_hpad_right)], self.c(8))

    def _bubble_attrs(self, kind: str) -> Tuple[int, int]:
        """Return (fill_attr, text_attr) for a chat line kind."""
        dim = curses.A_DIM if hasattr(curses, "A_DIM") else 0
        if kind == "you":
            fill = self.c(10)
            return fill, fill | curses.A_BOLD
        if kind == "grok" or kind == "peer":
            fill = self.c(11)
            return fill, fill | curses.A_BOLD
        if kind == "think":
            fill = self.c(12)
            return fill, fill | dim
        if kind == "tool":
            fill = self.c(17)
            return fill, fill | curses.A_BOLD
        if kind == "sub":
            fill = self.c(18)
            return fill, fill | curses.A_BOLD
        if kind == "meta":
            return 0, self.c(13) | dim
        return 0, self.c(3)

    def chat_lines_typed(self, width: int) -> List[ChatLine]:
        """Grok Build–style transcript: you → think → tools → answer (scroll full).

        R-09: never hard-cap assistant to 8 lines. Viewport + ↑↓/Pg scroll.
        """
        # Use full pane width (soft max only for pathological widths)
        w = max(8, min(width, PAD.max_thoughts_width))
        bp = PAD.bubble_hpad
        text_w = max(8, w - 2 * bp)

        if not self.history:
            return [
                ("meta", ""),
                ("meta", "  Conversation"),
                ("meta", "  ─────────────────────────"),
                ("meta", "  One seat. Law on the right."),
                ("meta", "  You approve — models never do."),
                ("meta", ""),
                ("meta", "  Type below to begin."),
                ("meta", "  Tab focus · F3 actions · F1/F2 pages"),
            ]

        out: List[ChatLine] = []

        def emit(kind: str, label: str, body: str, max_lines: int) -> None:
            body = (body or "").rstrip()
            if not (body or "").strip():
                return
            tag = f"{label} "
            body_w = max(6, text_w - len(tag))
            wrapped = _wrap(body, body_w)
            if max_lines > 0 and len(wrapped) > max_lines:
                more = len(wrapped) - (max_lines - 1)
                wrapped = wrapped[: max_lines - 1] + [f"… +{more} lines · Ctrl+E expand · Ctrl+Y yank"]
            for i, wl in enumerate(wrapped):
                if i == 0:
                    out.append((kind, tag + wl))
                else:
                    out.append((kind, (" " * len(tag)) + wl))

        for m in self.history[-PAD.max_history_turns :]:
            role = m.get("role") or ""
            content = (m.get("content") or "").strip()
            thinking = (m.get("thinking") or "").strip()
            tools = m.get("tools") or []
            tool_trace = m.get("tool_trace") or []
            if role == "user":
                emit("you", "you", content, PAD.max_user_lines)
            else:
                # 1) thinking strip (Grok Build thought stream)
                if thinking:
                    tshow = thinking
                    if len(thinking) > PAD.max_thinking_chars:
                        tshow = thinking[: PAD.max_thinking_chars] + "…"
                    emit("think", "···", tshow, PAD.max_thinking_lines)
                # 2) tool / subagent activity rows (icons in ASCII)
                if tool_trace:
                    for tr in tool_trace[:24]:
                        if isinstance(tr, dict):
                            name = str(tr.get("name") or tr.get("title") or "tool")
                            phase = str(tr.get("phase") or tr.get("kind") or "")
                            detail = str(tr.get("detail") or tr.get("message") or "")[:120]
                            if phase in ("subagent", "agent", "sub"):
                                label, kind = "◆", "sub"
                            else:
                                label, kind = "▸", "tool"
                            body = name if not detail else f"{name}  {detail}"
                            if phase and phase not in ("call", "tool_call", ""):
                                body = f"{phase} · {body}"
                            emit(kind, label, body, PAD.max_tool_lines)
                        else:
                            emit("tool", "▸", str(tr), PAD.max_tool_lines)
                elif tools:
                    # compact one-line tool list if only names
                    for tname in tools[:16]:
                        emit("tool", "▸", str(tname), 1)
                # 3) final answer — full scrollable body (R-09)
                emit("grok", "grok", content or "(empty)", PAD.max_reply_lines)
            for _ in range(PAD.msg_gap):
                out.append(("pad", ""))
        while out and out[-1][0] == "pad":
            out.pop()
        return out

    def shell_lines_typed(self, width: int) -> List[ChatLine]:
        w = max(8, min(width, PAD.max_thoughts_width))
        if not self.shell_lines:
            return [("meta", "shell")]
        out: List[ChatLine] = []
        for raw in self.shell_lines[-50:]:
            s = raw or ""
            stripped = s.lstrip()
            if stripped.startswith("you"):
                kind = "you"
            elif stripped.startswith("peer"):
                kind = "peer"
            elif stripped.startswith("shell") or stripped.startswith("tip:") or stripped.startswith("("):
                kind = "meta"
            elif not stripped:
                kind = "pad"
            else:
                kind = "plain"
            for wl in _wrap(s, w) or [""]:
                out.append((kind, wl))
        return out

    def _bottom_align(
        self, lines: List[ChatLine], viewport_h: int, scroll: int
    ) -> Tuple[List[ChatLine], int]:
        """Pad top so content sits low; clamp scroll. Returns (visible, max_scroll)."""
        n = len(lines)
        max_scroll = max(0, n - viewport_h)
        scroll = max(0, min(scroll, max_scroll))
        # when content shorter than viewport, pad top (bottom-align)
        if n <= viewport_h:
            pad_n = viewport_h - n
            vis: List[ChatLine] = [("pad", "")] * pad_n + list(lines)
            return vis, 0
        slice_ = lines[scroll : scroll + viewport_h]
        return slice_, max_scroll

    def _draw_chat_viewport(
        self,
        stdscr,
        lines: List[ChatLine],
        y0: int,
        x0: int,
        inner_h: int,
        inner_w: int,
        scroll: int,
    ) -> int:
        """Draw bottom-aligned filled bubbles. Returns clamped scroll."""
        vis, max_sc = self._bottom_align(lines, inner_h, scroll)
        # clear pane interior
        for i in range(inner_h):
            _fill_row(stdscr, y0 + i, x0, inner_w, 0)

        bp = PAD.bubble_hpad
        for i, (kind, text) in enumerate(vis):
            row = y0 + i
            if kind == "pad" or not text:
                continue
            fill, tattr = self._bubble_attrs(kind)
            # filled text box: full inner width for message kinds
            if kind in ("you", "grok", "peer", "think", "tool", "sub"):
                # fill bubble to text; for long assistant lines use full inner width
                if kind in ("grok", "peer", "think") and len(text) + 2 * bp >= inner_w - 2:
                    bubble_w = inner_w
                else:
                    bubble_w = min(inner_w, max(len(text) + 2 * bp, 12))
                if kind == "you":
                    bx = x0 + max(0, inner_w - bubble_w)
                else:
                    bx = x0
                _fill_row(stdscr, row, bx, bubble_w, fill)
                _safe_add(stdscr, row, bx + bp, text[: max(0, bubble_w - 2 * bp)], tattr)
            else:
                _safe_add(stdscr, row, x0, text[:inner_w], self._bubble_attrs(kind)[1])
        return max(0, min(scroll, max_sc))

    def current_text(self) -> str:
        """Plain CURRENT.md as on disk (+ short pin). No reformatting of body."""
        cf = self.root / "CURRENT.md"
        if not cf.is_file():
            return "(no CURRENT.md)"
        try:
            body = cf.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return f"(read error: {e})"
        pin = f"NEXT  {self.st.next_action}\n{self.st.phase} · {self.st.status}\n\n"
        return pin + body

    def draw_panel_page(self, stdscr, h: int, w: int, top: int) -> None:
        L, R = PAD.outer_hpad_left, PAD.outer_hpad_right
        bot = self._bot_rows()
        x0 = L
        usable_w = max(20, w - L - R)
        body_h = max(6, h - top - bot)
        mid = max(16, int(usable_w * 0.58))
        if usable_w - mid < 16:
            mid = max(12, usable_w - 16)
        right_w = usable_w - mid
        # Accent frame (not cyan toy border)
        frame = self.c(19) | curses.A_BOLD if self._colors else self.c(1)
        self._draw_box(stdscr, top, x0, body_h, mid, frame)
        self._draw_box(stdscr, top, x0 + mid, body_h, right_w, frame)
        # Pane titles — filled title chips on the top edge
        _safe_add(stdscr, top, x0 + 2, " CONVERSATION ", self.c(6) | curses.A_BOLD)
        _safe_add(stdscr, top, x0 + mid + 2, " DOMAIN · CURRENT ", self.c(7) | curses.A_BOLD)

        inner_h = max(1, body_h - 2)
        inner_w_l = max(8, mid - 2)
        inner_w_r = max(8, right_w - 2)
        self._inner_h = inner_h
        cy = top + 1
        cx = x0 + 1

        chat = self.chat_lines_typed(max(8, inner_w_l - 2 * PAD.bubble_hpad))
        if self.chat_scroll >= max(0, len(chat) - inner_h - 1):
            self.chat_scroll = 10**9
        self.chat_scroll = self._draw_chat_viewport(
            stdscr, chat, cy, cx, inner_h, inner_w_l, self.chat_scroll
        )

        # CURRENT: authority strip first, then raw file
        pin = [
            f"NEXT     {self.st.next_action}",
            f"PHASE    {self.st.phase}  ·  {self.st.status}",
            f"APPROVAL {self.st.approval}",
            "─" * min(inner_w_r, 28),
        ]
        body = self.current_text()
        # drop duplicate pin if current_text already starts with NEXT
        cur_lines = pin + _wrap(body, inner_w_r)
        max_rs = max(0, len(cur_lines) - inner_h)
        self.current_scroll = max(0, min(self.current_scroll, max_rs))
        vis_r = cur_lines[self.current_scroll : self.current_scroll + inner_h]
        rx = x0 + mid + 1
        for i in range(inner_h):
            row = cy + i
            _fill_row(stdscr, row, rx, inner_w_r, 0)
            if i >= len(vis_r) or not vis_r[i]:
                continue
            line = vis_r[i][:inner_w_r]
            # first authority lines pop; body is muted
            if self.current_scroll == 0 and i < 3:
                attr = self.c(4) | curses.A_BOLD if i == 0 else self.c(20) | curses.A_BOLD
                _safe_add(stdscr, row, rx, line, attr)
            elif line.startswith("─"):
                _safe_add(stdscr, row, rx, line, self.c(1))
            else:
                _safe_add(stdscr, row, rx, line, self.c(13))

        self._draw_dock(stdscr, h, w)

    def ensure_shell_boot(self) -> None:
        if self._shell_booted:
            return
        self._shell_booted = True
        try:
            from aether_fs import load_dotenv_files
            from aether_llm import apply_peer_backend, describe_backend, peer_down_recovery
            from aether_shell import status_line
            from aether_shell_agent import set_agent_role

            load_dotenv_files()
            set_agent_role("peer")

            peer = apply_peer_backend(self.root, model="personal-llm-sft-v4:latest")
            down = peer.endswith("(DOWN)")
            self.shell_lines = [
                "",
                "  shell  ·  peer sft-v4",
                f"  {status_line(self.root)[:70]}",
                f"  {peer}",
                f"  {describe_backend()}",
                "",
            ]
            if down:
                for ln in peer_down_recovery(self.root).splitlines():
                    self.shell_lines.append(f"  {ln}")
                self.shell_lines.append("")
            self.shell_lines.extend(
                [
                    "  type to chat about CURRENT · drafts only",
                    "  highlight text → Ctrl+Y /yank  (uses selection; else last reply)",
                    "  paste input: Ctrl+V /paste  ·  →CURRENT: Ctrl+T /tocurrent",
                    "  foot: mouse-select also fills primary; Ctrl+Shift+C/V works too",
                    "  F1 panel · F3 actions",
                    "",
                ]
            )
        except Exception as e:
            self.shell_lines = ["", f"  shell init: {e}", ""]

    def draw_shell_page(self, stdscr, h: int, w: int, top: int) -> None:
        L, R = PAD.outer_hpad_left, PAD.outer_hpad_right
        bot = self._bot_rows()
        x0 = L
        usable_w = max(20, w - L - R)
        body_h = max(6, h - top - bot)
        frame = self.c(1)
        self._draw_box(stdscr, top, x0, body_h, usable_w, frame)
        _safe_add(stdscr, top, x0 + 1, " shell ", self.c(6) | curses.A_BOLD)
        inner_h = max(1, body_h - 2)
        inner_w = max(8, usable_w - 2)
        self._inner_h = inner_h
        lines = self.shell_lines_typed(max(8, inner_w - 2 * PAD.bubble_hpad))
        if self.shell_scroll >= max(0, len(lines) - inner_h - 1):
            self.shell_scroll = 10**9
        self.shell_scroll = self._draw_chat_viewport(
            stdscr, lines, top + 1, x0 + 1, inner_h, inner_w, self.shell_scroll
        )
        self._draw_dock(stdscr, h, w)

    def _draw_actions_right(self, stdscr, y: int, x0: int, width: int) -> None:
        """Action chips packed flush-right (above input — not the bottom bar)."""
        if width < 8:
            return
        menu = self.menu()
        chips: List[Tuple[str, bool]] = []
        for i, (label, _) in enumerate(menu):
            chips.append((f" {label} ", self.focus == "menu" and i == self.selected))

        gap = 1
        total = sum(len(t) for t, _ in chips) + gap * max(0, len(chips) - 1)
        while total > width and chips:
            chips.pop(0)
            total = sum(len(t) for t, _ in chips) + gap * max(0, len(chips) - 1)

        _fill_row(stdscr, y, x0, width, self.c(14))
        try:
            hz = curses.ACS_HLINE
        except Exception:
            hz = ord("-")
        _safe_hline(stdscr, y, x0, hz, width, self.c(1))

        right_edge = x0 + width
        x = max(x0, right_edge - total)
        for text, sel in chips:
            attr = (
                (self.c(7) | curses.A_BOLD | curses.A_REVERSE)
                if sel
                else (self.c(16) | curses.A_BOLD)
            )
            _fill_row(stdscr, y, x, len(text), attr)
            _safe_add(stdscr, y, x, text, attr)
            x += len(text) + gap

    def _draw_status_bar(self, stdscr, y: int, x0: int, width: int, mode: str) -> None:
        """Bottom bar: mode/F3/status — full-width fill, hints packed flush-right."""
        if width < 8:
            return
        _fill_row(stdscr, y, x0, width, self.c(14))
        try:
            hz = curses.ACS_HLINE
        except Exception:
            hz = ord("-")
        _safe_hline(stdscr, y, x0, hz, width, self.c(1))

        # left: compact mode chip
        left = f" {mode} "
        _fill_row(stdscr, y, x0, len(left), self.c(6) | curses.A_BOLD)
        _safe_add(stdscr, y, x0, left, self.c(6) | curses.A_BOLD)

        # right-packed: F3 hint + live status (same treatment actions used to get)
        if self.show_actions:
            f3 = " F3 hide "
        else:
            f3 = " F3 actions "
        st = f" {self.status} " if self.status else ""
        # prefer status then F3 on the right
        parts = [p for p in (st, f3) if p.strip()]
        gap = 1
        total = sum(len(p) for p in parts) + gap * max(0, len(parts) - 1)
        # truncate status if overflow
        while total > width - len(left) - 2 and parts:
            if len(parts[0]) > 12 and parts[0] is st:
                parts[0] = parts[0][: max(8, width // 3)] + "… "
                total = sum(len(p) for p in parts) + gap * max(0, len(parts) - 1)
            else:
                break
        x = max(x0 + len(left) + 1, x0 + width - total)
        for i, p in enumerate(parts):
            # status yellow-ish, F3 chip yellow fill
            if "F3" in p:
                attr = self.c(16) | curses.A_BOLD
            else:
                attr = self.c(4) | curses.A_BOLD
            _fill_row(stdscr, y, x, len(p), attr)
            _safe_add(stdscr, y, x, p[: max(0, x0 + width - x)], attr)
            x += len(p) + gap

    def _draw_dock(self, stdscr, h: int, w: int) -> None:
        """Dock top→bottom: [actions right] · input · status/F3 bar (bottom)."""
        L, R = PAD.outer_hpad_left, PAD.outer_hpad_right
        usable = max(10, w - L - R)
        right_edge = w - R
        if self.page == "panel":
            mode = {"chat": "CHAT", "menu": "MENU", "current": "CURRENT"}.get(
                self.focus, "?"
            )
        else:
            mode = {"input": "SHELL", "menu": "MENU", "log": "LOG"}.get(self.focus, "?")

        if self.show_actions:
            # actions above input; status/F3 bar at very bottom
            action_y, input_y, status_y = h - 3, h - 2, h - 1
        else:
            action_y, input_y, status_y = None, h - 2, h - 1

        if action_y is not None:
            self._draw_actions_right(stdscr, action_y, L, usable)

        # input above status bar — filled field, clear prompt
        prompt = "  →  " if self.page == "panel" else "  $  "
        _fill_row(stdscr, input_y, L, usable, self.c(15))
        body = prompt + self.input_buf
        shown = body[-(usable - 2) :] if len(body) > usable - 2 else body
        focus_in = self.focus in ("chat", "input")
        attr = self.c(15) | (curses.A_BOLD if focus_in else 0)
        _safe_add(stdscr, input_y, L + 1, shown[: usable - 2], attr)
        if focus_in:
            _safe_add(stdscr, input_y, right_edge - 1, "█", self.c(6) | curses.A_BOLD)

        self._draw_status_bar(stdscr, status_y, L, usable, mode)

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

    def build_panel_messages(self, history: List[dict]) -> List[dict]:
        """Native Grok Build agent context — NOT shell XML tool_call protocol.

        Root cause of broken panel chat: `build_messages()` injects aether-shell-agent-grok
        (XML <tool_call> for Python loop) while we invoke the real Grok CLI with native tools.
        Those two protocols fight; agent burns turns / returns empty finals.
        """
        try:
            from aether_fs import read_current

            cur = (read_current(self.root) or "").strip()
        except Exception:
            cur = ""
        if len(cur) > 14000:
            cur = cur[:14000] + "\n…(CURRENT truncated for seat)"

        system = f"""You are **Grok Build** on the Mechanicall seat PANEL.
You run on the same Grok CLI session stack as interactive Grok TUI (thinking + tools + answer).

## Behaviour (steal real Grok agent logic)
- Think, then answer. Use **native Grok tools** when useful: read_file, grep, list_dir.
- Do **not** emit fake XML `<tool_call>` blocks — those are for a different shell loop.
- Prefer tools over guessing repo contents. Parallelize independent reads when helpful.
- Always leave a clear **final answer** the operator can read in chat (not only tools/thinking).

## Domain (sacred)
- CURRENT.md below is Domain law.
- Never approve Domain changes; never claim `aether approve`.
- Propose CURRENT edits only as markdown drafts for the human.

## Project root
{self.root}

## CURRENT.md
{cur or "(no CURRENT.md)"}
"""
        msgs: List[dict] = [{"role": "system", "content": system}]
        for m in history[-16:]:
            role = m.get("role") or ""
            if role not in ("user", "assistant"):
                continue
            content = (m.get("content") or "").strip()
            if content:
                msgs.append({"role": role, "content": content})
        return msgs

    def panel_chat(self, text: str) -> None:
        try:
            import os as _os
            from aether_fs import load_dotenv_files
            from aether_llm import chat, last_chat_meta

            load_dotenv_files()
            # Native Grok Build agent (headless) — research tools, auto-approve, no Domain writes
            _os.environ["AETHER_LLM_PROVIDER"] = "grok_tui"
            _os.environ["AETHER_MODEL"] = "grok-4.5"
            _os.environ.pop("AETHER_OLLAMA_MODEL", None)
            _os.environ.pop("AETHER_GROK_NO_TOOLS", None)
            _os.environ["AETHER_REASONING_EFFORT"] = "high"
            _os.environ["AETHER_GROK_OUTPUT_FORMAT"] = "streaming-json"
            _os.environ["AETHER_GROK_MAX_TURNS"] = "24"
            _os.environ["AETHER_GROK_ALWAYS_APPROVE"] = "1"
            _os.environ["AETHER_GROK_PERMISSION_MODE"] = "auto"
            # Allow read/search only — blocks runaway coding sessions (run_terminal, edit, todos)
            _os.environ["AETHER_GROK_TOOLS"] = (
                "read_file,grep,list_dir,web_search,web_fetch"
            )
            _os.environ["AETHER_GROK_DENY_TOOLS"] = (
                "search_replace,Write,Edit,write,run_terminal_command,"
                "run_terminal_cmd,todo_write,Bash,bash,spawn_subagent,task"
            )
            _os.environ["AETHER_GROK_CWD"] = str(self.root)
            _os.environ["MECH_PROJECT"] = str(self.root)
            # explore = read-only Grok agent (not general-purpose implementer)
            explore = Path.home() / ".grok" / "bundled" / "agents" / "explore.md"
            if explore.is_file():
                _os.environ["AETHER_GROK_AGENT"] = str(explore)
            else:
                _os.environ.pop("AETHER_GROK_AGENT", None)
        except Exception as e:
            self.status = f"init: {e}"
            return
        self.history.append({"role": "user", "content": text})
        try:
            msgs = self.build_panel_messages(self.history)
            reply = chat(msgs, temperature=0.35)
            meta = {}
            try:
                meta = last_chat_meta() or {}
            except Exception:
                pass
            thinking = (meta.get("thinking") or "").strip()
            tools = meta.get("tools") or []
            tool_trace = meta.get("tool_trace") or []
            self.history.append(
                {
                    "role": "assistant",
                    "content": reply or "",
                    "thinking": thinking,
                    "tools": tools,
                    "tool_trace": tool_trace,
                    "provider": meta.get("provider") or "grok_tui",
                }
            )
            self._last_reply = reply or ""
            try:
                mirror_last_reply(self.root, reply or "", thinking, tools)
            except Exception:
                pass
            n = len(reply or "")
            tbits = []
            if tools:
                tbits.append(f"tools={','.join(str(t) for t in tools[:5])}")
            if thinking:
                tbits.append(f"think {len(thinking)}c")
            tbits.append(f"{n}c")
            tbits.append("Ctrl+E expand · Ctrl+Y yank")
            self.status = "grok · " + " · ".join(tbits)
            self._be_label = _backend_label()
            self.chat_scroll = 10**9
        except Exception as e:
            self.history.pop()
            self.status = f"grok: {e}"[:60]
        self.st = self.host.load_state(self.root)

    def yank_last(self) -> None:
        """Yank highlighted text (primary) first; else last peer/grok reply."""
        src = ""
        text = ""
        ok_h, hi = clipboard_read_highlight()
        if ok_h and hi.strip():
            text = hi
            src = "selection"
        else:
            text = (self._last_reply or "").strip()
            src = "last reply"
            if not text:
                for m in reversed(
                    self.history if self.page == "panel" else self.shell_hist
                ):
                    if m.get("role") == "assistant" and (m.get("content") or "").strip():
                        text = m["content"].strip()
                        src = "last reply"
                        break
        if not text.strip():
            self.status = "nothing to yank — highlight text or wait for a reply"
            if self.page == "shell":
                self.shell_lines.append("  (yank: no selection, no last reply)")
                self.shell_scroll = 10**9
            return
        ok, msg = clipboard_copy(text)
        # msg like "copied N chars" — annotate source
        if ok:
            self.status = f"yanked {src}: {len(text)} chars"
            note = f"  (yanked {src}: {len(text)} chars)"
        else:
            self.status = msg
            note = f"  ({msg})"
        if self.page == "shell":
            self.shell_lines.append(note)
            self.shell_scroll = 10**9


    def expand_last(self, stdscr=None) -> None:
        """Fullscreen pager for last reply (+ thinking) — Grok Build full-text escape hatch."""
        text = (self._last_reply or "").strip()
        thinking = ""
        tools: list = []
        hist = self.history if self.page == "panel" else self.shell_hist
        for m in reversed(hist):
            if m.get("role") == "assistant":
                if not text:
                    text = (m.get("content") or "").strip()
                thinking = (m.get("thinking") or "").strip()
                tools = m.get("tools") or []
                break
        if not text and not thinking:
            # fall back to on-disk mirror
            p = self.root / ".aether" / "last-reply.md"
            if p.is_file():
                try:
                    text = p.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    text = ""
        if not text and not thinking:
            self.status = "nothing to expand — send a chat first"
            return
        parts = []
        if tools:
            parts.append("▸ tools: " + ", ".join(str(t) for t in tools))
            parts.append("")
        if thinking:
            parts.append("··· thinking")
            parts.append(thinking)
            parts.append("")
            parts.append("─" * 40)
            parts.append("")
        parts.append(text or "(empty answer)")
        blob = "\n".join(parts)
        if stdscr is None:
            self.status = f"expand: {len(blob)} chars (no TTY) — see .aether/last-reply.md"
            return
        lines = blob.splitlines() or [""]
        top = 0
        while True:
            h, w = stdscr.getmaxyx()
            stdscr.erase()
            title = f" EXPAND last · {len(blob)}c · ↑↓ Pg · q/Esc "
            _safe_add(stdscr, 0, 0, title.ljust(max(0, w - 1))[: max(0, w - 1)], self.c(6) | curses.A_BOLD)
            view = max(1, h - 2)
            top = max(0, min(top, max(0, len(lines) - view)))
            for i in range(view):
                if top + i >= len(lines):
                    break
                _safe_add(stdscr, 1 + i, 0, lines[top + i][: max(0, w - 1)], self.c(3))
            foot = f" lines {top + 1}-{min(len(lines), top + view)}/{len(lines)} · q close · y yank "
            _safe_add(stdscr, h - 1, 0, foot.ljust(max(0, w - 1))[: max(0, w - 1)], self.c(4))
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (27, ord("q"), ord("Q")):
                break
            if ch in (curses.KEY_UP, ord("k")):
                top = max(0, top - 1)
            elif ch in (curses.KEY_DOWN, ord("j")):
                top += 1
            elif ch in (curses.KEY_PPAGE,):
                top = max(0, top - view)
            elif ch in (curses.KEY_NPAGE,):
                top += view
            elif ch in (ord("y"), ord("Y"), 25):
                ok, msg = clipboard_copy(text or blob)
                self.status = msg if not ok else f"yanked expand: {len(text or blob)} chars"
        self.status = self.status if self.status.startswith("yanked") else f"expand closed · {len(text or '')}c in last reply"

    def paste_to_input(self) -> None:
        # prefer highlighted primary, then clipboard
        ok, text = clipboard_paste(prefer_primary=True)
        if not ok or not text:
            self.status = "clipboard empty — highlight+/yank or Ctrl+Shift+C"
            if self.page == "shell":
                self.shell_lines.append("  (clipboard empty)")
            return
        # single-line into input; multi-line: first line to input, rest note
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        self.input_buf += lines[0]
        extra = len(lines) - 1
        self.status = f"pasted {len(lines[0])} chars" + (
            f" (+{extra} more lines — use /tocurrent for full clip)" if extra > 0 else ""
        )
        if self.page == "shell" and extra > 0:
            self.shell_lines.append(
                f"  (pasted line 1 to input; {extra} more lines still in clipboard)"
            )

    def paste_to_current(self) -> None:
        """Append highlight/clipboard (or last reply) into CURRENT.md."""
        ok, text = clipboard_paste(prefer_primary=True)
        if not ok or not text.strip():
            text = (self._last_reply or "").strip()
        if not text.strip():
            self.status = "nothing to paste into CURRENT"
            if self.page == "shell":
                self.shell_lines.append("  (empty clip + no last reply)")
            return
        cf = self.root / "CURRENT.md"
        try:
            if not cf.is_file():
                cf.write_text("# CURRENT\n\n", encoding="utf-8")
            prev = cf.read_text(encoding="utf-8", errors="replace")
            block = (
                "\n\n## seat paste\n\n"
                + text.rstrip()
                + "\n"
            )
            cf.write_text(prev.rstrip() + block, encoding="utf-8")
            self.status = f"appended {len(text)} chars → CURRENT.md"
            if self.page == "shell":
                self.shell_lines.append(f"  (appended {len(text)} chars → CURRENT.md)")
                self.shell_scroll = 10**9
            self.st = self.host.load_state(self.root)
        except OSError as e:
            self.status = f"CURRENT write: {e}"
            if self.page == "shell":
                self.shell_lines.append(f"  (CURRENT write: {e})")

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

        # clipboard helpers (before generic slash)
        low = text.lower().split()
        cmd0 = low[0] if low else ""
        if cmd0 in ("/yank", "/y", "/copy"):
            self.yank_last()
            return
        if cmd0 in ("/paste", "/v"):
            self.paste_to_input()
            return
        if cmd0 in ("/tocurrent", "/clip-current", "/current+", "/tocur"):
            self.paste_to_current()
            return
        if cmd0 in ("/cliphelp", "/clipboard"):
            for ln in (
                "  clipboard:",
                "  1) mouse-highlight text in foot",
                "  2) Ctrl+Y /yank  — copies *selection* (primary) to clipboard",
                "     (if nothing highlighted → last peer/grok reply)",
                "  Ctrl+V /paste    — paste into input (primary then clipboard)",
                "  Ctrl+T /tocurrent — append selection/clip to CURRENT.md",
                "  foot: Ctrl+Shift+C / Ctrl+Shift+V also work",
            ):
                self.shell_lines.append(ln)
            self.shell_scroll = 10**9
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
            from aether_llm import peer_down_recovery

            peer = apply_peer_backend(self.root, model="personal-llm-sft-v4:latest")
            os.environ["AETHER_LLM_PROVIDER"] = "ollama"
            os.environ["AETHER_OLLAMA_MODEL"] = "personal-llm-sft-v4:latest"
            os.environ["AETHER_MODEL"] = "personal-llm-sft-v4:latest"
            os.environ.setdefault("AETHER_OLLAMA_NUM_CTX", "8192")
            os.environ.setdefault("OLLAMA_HOST", "http://192.168.1.241:11434")
            # R-08: fail-fast when Ollama DOWN — do not hang chat timeout (120s)
            if peer.endswith("(DOWN)"):
                if self.shell_hist and self.shell_hist[-1].get("role") == "user":
                    self.shell_hist.pop()
                self.shell_lines.append(f"  ({peer})")
                for ln in peer_down_recovery(self.root).splitlines():
                    self.shell_lines.append(f"  {ln}")
                self.shell_lines.append("")
                self.status = "peer DOWN · start ollama on myarch"
                self.shell_scroll = 10**9
                self._be_label = _backend_label()
                return
            msgs = build_messages(self.root, self.shell_hist)
            reply = chat(msgs, temperature=0.35)
            self.shell_hist.append({"role": "assistant", "content": reply or ""})
            self._last_reply = reply or ""
            try:
                append_log(self.root, "assistant", reply or "")
            except Exception:
                pass
            try:
                mirror_last_reply(self.root, reply or "", "", [])
            except Exception:
                pass
            self.shell_lines.append("")
            first = True
            # R-09: show full peer reply (no silent drop) — scroll shell log
            for line in (reply or "(empty)").splitlines() or ["(empty)"]:
                if first:
                    self.shell_lines.append(f"  peer   {line}")
                    first = False
                else:
                    self.shell_lines.append(f"         {line}")
            self.shell_lines.append("")
            self.status = f"peer ready · {len(reply or '')}c · Ctrl+Y yank · /tocurrent"
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
        if key == "yank_last":
            self.yank_last()
            return False
        if key == "expand_last":
            self.expand_last(stdscr)
            return False
        if key == "paste_input":
            self.paste_to_input()
            return False
        if key == "paste_current":
            self.paste_to_current()
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

            # clipboard: Ctrl+Y yank, Ctrl+V paste, Ctrl+T → CURRENT, Ctrl+E expand
            if ch == 25:  # Ctrl+Y
                self.yank_last()
                continue
            if ch == 22:  # Ctrl+V
                self.paste_to_input()
                continue
            if ch == 20:  # Ctrl+T — append clip/last reply to CURRENT
                self.paste_to_current()
                continue
            if ch == 5:  # Ctrl+E expand last full reply
                self.expand_last(stdscr)
                continue
            # page scroll in chat/shell/current
            if ch == curses.KEY_PPAGE:
                step = PAD.page_scroll_step
                if self.page == "shell" or self.focus == "log":
                    self.shell_scroll = max(0, self.shell_scroll - step)
                elif self.focus == "current":
                    self.current_scroll = max(0, self.current_scroll - step)
                else:
                    self.chat_scroll = max(0, self.chat_scroll - step)
                continue
            if ch == curses.KEY_NPAGE:
                step = PAD.page_scroll_step
                if self.page == "shell" or self.focus == "log":
                    self.shell_scroll += step
                elif self.focus == "current":
                    self.current_scroll += step
                else:
                    self.chat_scroll += step
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
                self.status = "grok agent · running (blocking)…"
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
