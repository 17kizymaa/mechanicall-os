#!/usr/bin/env python3
"""Terminal desk: chat-first surface over CURRENT.md + free/frontier model.

Default = multi-turn chat in the terminal (probabilistic propose layer).
Project root = cwd (or path arg). Authority stays in CURRENT.md.

Slash commands (not model tools):
  /help /c /e /n /p /s /i /w /clear /reload /quit
  (aliases: /current /edit /next /preflight /status /init /write /q)

Legacy: --keys  single-key mode (optional)

Doctrine (Mechanicall):
  - Filesystem is truth; CURRENT.md is authority.
  - Model proposes in chat; never approves; never advances phase.
  - Silence is never permission — empty input does not mean yes.
  - Chat transcript may log under .aether/chat.jsonl (inspectable, not authority).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import termios
import tty
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from aether_llm import chat, describe_backend, flag_unsafe_model_output
except ImportError:  # pragma: no cover
    chat = None  # type: ignore
    describe_backend = lambda: "unavailable"  # type: ignore
    flag_unsafe_model_output = lambda t: []  # type: ignore


SYSTEM_DOCTRINE = """You are the chat surface of Mechanicall OS desk (aether desk).

Architecture (non-negotiable):
- CURRENT.md in the project root is the only authority. You do not own it.
- You are a probabilistic propose layer: draft, explain, suggest Next wording.
- You never approve. You never claim approval. You never say silence is permission.
- You never invent that preflight passed unless the human pastes preflight output.
- Prefer short, practical answers. When proposing CURRENT edits, use clear Markdown drafts.

If CURRENT.md is present in context, treat it as ground truth for objective/next/limits.
If the human asks you to "just do it" or "approve", remind them to edit CURRENT ( /e ) or run human approve outside chat.
"""

HELP = """
desk — chat is default. Type normally to talk to the model.
Slash commands (mechanical; not model authority):

  /help          this text
  /c  /current   print CURRENT.md
  /e  /edit      $EDITOR CURRENT.md
  /n  /next      show Next + preflight
  /p  /preflight preflight Next only
  /s  /status    aether status
  /i  /init      aether current init
  /w  /write     save last model reply → .aether/propose-CURRENT.md
  /clear         clear chat memory (not CURRENT)
  /reload        re-read CURRENT into context banner
  /q  /quit      leave desk

Empty line = wait (not yes). Model never approves.
Product = CURRENT.md. Chat = propose only.
"""

_FIELD_RE = re.compile(
    r"^\*\*(?P<name>[^*]+?):?\*\*\s*:?\s*(?P<val>.*)$",
    re.IGNORECASE,
)

# Max prior turns kept in API context (user+assistant pairs roughly)
MAX_HISTORY_MESSAGES = 24


def project_root(path: str | Path | None = None) -> Path:
    p = Path(path or os.getcwd()).resolve()
    if p.is_file():
        p = p.parent
    return p


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
    return which or "aether"


def run_aether(args: list[str], root: Path, timeout: int = 120) -> tuple[int, str]:
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
        return 127, "aether not found"
    except subprocess.TimeoutExpired:
        return 124, "aether timed out"
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def parse_next(current_text: str) -> str:
    for line in current_text.splitlines():
        m = _FIELD_RE.match(line.strip())
        if not m:
            continue
        if m.group("name").rstrip(":").strip().lower() == "next":
            return m.group("val").strip()
    return ""


def read_current(root: Path) -> Optional[str]:
    cf = root / "CURRENT.md"
    if not cf.is_file():
        return None
    return cf.read_text(encoding="utf-8", errors="replace")


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        m = _FIELD_RE.match(line.strip())
        if m:
            fields[m.group("name").rstrip(":").strip().lower()] = m.group("val").strip()
    return fields


def banner(root: Path) -> str:
    text = read_current(root)
    lines = [
        f"desk (chat) — {root}",
        f"llm         — {describe_backend()}",
        "",
    ]
    if not text:
        lines.append("  (no CURRENT.md — /init or create one, then /e)")
    else:
        f = parse_fields(text)
        lines.append(f"  What we're doing:  {f.get('objective', '(unset)')}")
        lines.append(f"  Allowed next step: {f.get('next', '(unset)')}")
        lines.append(f"  Phase / Status:    {f.get('phase', '?')} / {f.get('status', '?')}")
        lines.append(f"  Human sign-off:    {f.get('approval', '?')}")
    lines.append("")
    lines.append("  Type to chat.  /help for commands.  Empty line is not yes.")
    return "\n".join(lines)


def append_chat_log(root: Path, role: str, text: str) -> None:
    """Inspectable transcript; never authority."""
    aether = root / ".aether"
    try:
        aether.mkdir(parents=True, exist_ok=True)
        path = aether / "chat.jsonl"
        rec = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "role": role,
            "text": text[:20000],
        }
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def edit_current(root: Path) -> None:
    cf = root / "CURRENT.md"
    if not cf.is_file():
        print("no CURRENT.md — /init first", flush=True)
        return
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"
    subprocess.call(editor.split() + [str(cf)])


def write_proposal(root: Path, last: list[str]) -> None:
    if not last:
        print("no model reply yet — chat first", flush=True)
        return
    aether = root / ".aether"
    aether.mkdir(parents=True, exist_ok=True)
    out = aether / "propose-CURRENT.md"
    out.write_text(
        "# Proposed CURRENT edits (not authority)\n\n"
        "Human must copy into CURRENT.md. Model output is not approval.\n\n"
        + last[0]
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out}", flush=True)


def preflight_next(root: Path, show_next: bool) -> None:
    t = read_current(root)
    if not t:
        print("no CURRENT.md", flush=True)
        return
    nxt = parse_next(t)
    if not nxt or nxt.lower() in ("unset", "(unset)"):
        print("Next is unset — /e to edit CURRENT", flush=True)
        return
    if show_next:
        print(f"Next: {nxt}", flush=True)
    code, out = run_aether(["preflight", nxt, str(root)], root)
    print(out or f"(exit {code})", flush=True)


def handle_slash(cmd: str, root: Path, history: List[dict], last: list[str]) -> bool:
    """Return True if desk should exit."""
    raw = cmd.strip()
    name = raw.split()[0].lower() if raw else ""
    if name in ("/q", "/quit", "/exit"):
        print("bye", flush=True)
        return True
    if name in ("/help", "/?", "/h"):
        print(HELP, flush=True)
        return False
    if name in ("/c", "/current"):
        print(read_current(root) or "(no CURRENT.md)", flush=True)
        return False
    if name in ("/e", "/edit"):
        edit_current(root)
        print(banner(root), flush=True)
        return False
    if name in ("/s", "/status"):
        code, out = run_aether(["status", str(root)], root)
        print(out or f"(exit {code})", flush=True)
        return False
    if name in ("/i", "/init"):
        code, out = run_aether(["current", "init", str(root)], root)
        print(out or f"(exit {code})", flush=True)
        print(banner(root), flush=True)
        return False
    if name in ("/n", "/next"):
        preflight_next(root, show_next=True)
        return False
    if name in ("/p", "/preflight"):
        preflight_next(root, show_next=False)
        return False
    if name in ("/w", "/write"):
        write_proposal(root, last)
        return False
    if name == "/clear":
        history.clear()
        last.clear()
        print("chat memory cleared (CURRENT unchanged)", flush=True)
        return False
    if name == "/reload":
        print(banner(root), flush=True)
        return False
    print(f"unknown command {name!r} — /help", flush=True)
    return False


def build_messages(root: Path, history: List[dict]) -> List[dict[str, str]]:
    current = read_current(root) or "(no CURRENT.md in project root)"
    # Cap CURRENT injection size
    if len(current) > 12000:
        current = current[:12000] + "\n…(truncated)"
    system = (
        SYSTEM_DOCTRINE
        + "\n\n--- CURRENT.md (authority; propose only) ---\n"
        + current
        + "\n--- end CURRENT.md ---"
    )
    msgs: List[dict[str, str]] = [{"role": "system", "content": system}]
    # keep tail of history
    tail = history[-MAX_HISTORY_MESSAGES:]
    for m in tail:
        msgs.append({"role": m["role"], "content": m["content"]})
    return msgs


def model_reply(root: Path, history: List[dict], user_text: str, last: list[str]) -> None:
    if chat is None:
        print("aether_llm unavailable", flush=True)
        return
    history.append({"role": "user", "content": user_text})
    append_chat_log(root, "user", user_text)
    try:
        os.environ.setdefault("AETHER_PERSONAL_LLM_SYSTEM", "0")  # we inject doctrine ourselves
        reply = chat(build_messages(root, history), temperature=0.5)
    except Exception as e:
        history.pop()  # drop failed user turn from context? keep it for retry
        print(f"model error: {e}", flush=True)
        print("Set OPENROUTER_API_KEY or GROQ_API_KEY — docs/FREE-API.md", flush=True)
        return
    flags = flag_unsafe_model_output(reply)
    if flags:
        print(f"[flags: {', '.join(flags)}]", flush=True)
    print(f"\nmodel> {reply}\n", flush=True)
    history.append({"role": "assistant", "content": reply})
    append_chat_log(root, "assistant", reply)
    last.clear()
    last.append(reply)


def run_chat(root: Path) -> int:
    root = project_root(root)
    history: List[dict] = []
    last: list[str] = []
    print(banner(root), flush=True)
    print(HELP if os.environ.get("AETHER_DESK_VERBOSE") else "", end="", flush=True)

    while True:
        try:
            print("you> ", end="", flush=True)
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            print("\n(use /quit to exit)", flush=True)
            continue
        if line == "":
            # EOF
            print("\nbye", flush=True)
            return 0
        text = line.rstrip("\n")
        # Silence is never permission: empty line does nothing
        if not text.strip():
            continue
        stripped = text.strip()
        if stripped.startswith("/"):
            if handle_slash(stripped, root, history, last):
                return 0
            continue
        model_reply(root, history, text, last)


# --- legacy single-key mode -------------------------------------------------


def get_key() -> str:
    if not sys.stdin.isatty():
        line = sys.stdin.readline()
        return (line or "q").strip()[:1].lower() or "q"
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    if ch in ("\x03", "\x04"):
        return "q"
    if ch in ("\r", "\n"):
        return ""
    return ch.lower()


def run_keys(root: Path) -> int:
    """Optional legacy hotkey UI (--keys)."""
    root = project_root(root)
    last: list[str] = []
    history: List[dict] = []
    print(banner(root), flush=True)
    print("(keys mode — prefer default chat; press ?)", flush=True)
    while True:
        print("\nkey> ", end="", flush=True)
        k = get_key()
        if not k:
            continue
        if sys.stdin.isatty():
            print(k, flush=True)
        if k in ("q", "x"):
            print("bye", flush=True)
            return 0
        if k in ("?", "h"):
            print(HELP, flush=True)
            continue
        if k == "c":
            print(read_current(root) or "(no CURRENT.md)", flush=True)
            continue
        if k == "e":
            edit_current(root)
            print(banner(root), flush=True)
            continue
        if k == "s":
            code, out = run_aether(["status", str(root)], root)
            print(out or f"(exit {code})", flush=True)
            continue
        if k == "i":
            code, out = run_aether(["current", "init", str(root)], root)
            print(out or f"(exit {code})", flush=True)
            continue
        if k in ("n", "p"):
            preflight_next(root, show_next=(k == "n"))
            continue
        if k == "g":
            print("type a message (chat mode is default without --keys): ", end="", flush=True)
            q = sys.stdin.readline()
            if q and q.strip():
                model_reply(root, history, q.strip(), last)
            continue
        if k == "w":
            write_proposal(root, last)
            continue
        print(f"unknown {k!r}", flush=True)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Mechanicall desk — terminal chat over CURRENT.md"
    )
    ap.add_argument("path", nargs="?", default=".", help="project root (default: cwd)")
    ap.add_argument(
        "--once",
        metavar="KEY",
        help="one-shot: b=banner c=current n=preflight-next",
    )
    ap.add_argument(
        "--keys",
        action="store_true",
        help="legacy single-key mode instead of chat",
    )
    args = ap.parse_args(argv)
    root = project_root(args.path)

    if args.once:
        if args.once == "c":
            sys.stdout.write((read_current(root) or "(no CURRENT.md)") + "\n")
            return 0
        if args.once == "b":
            sys.stdout.write(banner(root) + "\n")
            return 0
        if args.once == "n":
            t = read_current(root) or ""
            nxt = parse_next(t)
            if not nxt:
                print("Next unset", flush=True)
                return 1
            code, out = run_aether(["preflight", nxt, str(root)], root)
            print(out, flush=True)
            return code
        print(f"unsupported --once {args.once}", flush=True)
        return 2

    if not sys.stdin.isatty():
        print("aether desk: need a TTY (or use --once KEY)", file=sys.stderr)
        print(banner(root))
        return 1

    if args.keys:
        return run_keys(root)
    return run_chat(root)


if __name__ == "__main__":
    sys.exit(main())
