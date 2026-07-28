#!/usr/bin/env python3
"""Minimal hotkey desk over CURRENT.md — product is the file, not the chrome.

Project root = current working directory (or path arg). No nested path ceremony.

Hotkeys (single key, then Enter in simple mode; raw tty when available):
  ?  help
  c  show CURRENT.md
  e  edit CURRENT.md ($EDITOR)
  n  show Next + preflight that action
  p  preflight Next only
  s  aether status summary
  i  aether current init (if missing)
  g  ask free/frontier model (propose only — never approve)
  w  write last model reply to .aether/propose-CURRENT.md
  q  quit

Doctrine: models propose; humans edit CURRENT by hand. Approve is optional and not a hotkey.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import termios
import tty
from pathlib import Path
from typing import Optional

# sibling import
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from aether_llm import chat, describe_backend, flag_unsafe_model_output
except ImportError:  # pragma: no cover
    chat = None  # type: ignore
    describe_backend = lambda: "unavailable"  # type: ignore
    flag_unsafe_model_output = lambda t: []  # type: ignore


HELP = """
  ?  help                 this text
  c  current              print CURRENT.md
  e  edit                 $EDITOR CURRENT.md
  n  next                 show Next + preflight it
  p  preflight            preflight Next only
  s  status               aether status
  i  init current         create CURRENT.md template if missing
  g  ask model            free API propose (does not write authority)
  w  write proposal       save last model reply → .aether/propose-CURRENT.md
  q  quit

  Product = CURRENT.md you edit. Tools are optional.
  Model never approves. Silence is never permission.
"""

_FIELD_RE = re.compile(
    r"^\*\*(?P<name>[^*]+?):?\*\*\s*:?\s*(?P<val>.*)$",
    re.IGNORECASE,
)


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


def banner(root: Path) -> str:
    text = read_current(root)
    lines = [
        f"desk — {root}",
        f"llm  — {describe_backend()}",
        "",
    ]
    if not text:
        lines.append("  (no CURRENT.md — press i to init, or e after creating one)")
        lines.append("  hotkeys: ? c e n p s i g w q")
        return "\n".join(lines)
    fields: dict[str, str] = {}
    for line in text.splitlines():
        m = _FIELD_RE.match(line.strip())
        if m:
            fields[m.group("name").rstrip(":").strip().lower()] = m.group("val").strip()
    lines.append(f"  What we're doing:  {fields.get('objective', '(unset)')}")
    lines.append(f"  Allowed next step: {fields.get('next', '(unset)')}")
    lines.append(f"  Phase / Status:    {fields.get('phase', '?')} / {fields.get('status', '?')}")
    lines.append(f"  Human sign-off:    {fields.get('approval', '?')}")
    lines.append("")
    lines.append("  hotkeys: ? c e n p s i g w q")
    return "\n".join(lines)


def get_key() -> str:
    """Single character; falls back to line mode."""
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
    if ch in ("\x03", "\x04"):  # Ctrl-C / D
        return "q"
    if ch == "\r" or ch == "\n":
        return ""
    return ch.lower()


def edit_current(root: Path) -> None:
    cf = root / "CURRENT.md"
    if not cf.is_file():
        print("no CURRENT.md — press i first", flush=True)
        return
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"
    subprocess.call([*editor.split(), str(cf)])  # noqa: S603 — intentional editor


def ask_model(root: Path, last: list[str]) -> None:
    if chat is None:
        print("aether_llm unavailable", flush=True)
        return
    text = read_current(root) or "(no CURRENT.md yet)"
    print("question (empty = 'What should Next be? propose only'): ", end="", flush=True)
    try:
        q = sys.stdin.readline()
    except KeyboardInterrupt:
        print()
        return
    if q is None:
        return
    q = q.strip() or (
        "Given CURRENT.md below, propose at most one clear Next action and "
        "any Keep/Reject edits. Do not claim approval. Propose Markdown only."
    )
    system = (
        "You help edit a Mechanicall CURRENT.md authority file. "
        "Propose only. Never instruct the human to treat silence as permission. "
        "Never claim you approved anything. Keep answers short."
    )
    try:
        os.environ.setdefault("AETHER_PERSONAL_LLM_SYSTEM", "1")
        reply = chat(
            [
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": f"CURRENT.md:\n\n{text}\n\nUser:\n{q}",
                },
            ],
            temperature=0.4,
        )
    except Exception as e:
        print(f"model error: {e}", flush=True)
        print("Set OPENROUTER_API_KEY or GROQ_API_KEY — see docs/FREE-API.md", flush=True)
        return
    flags = flag_unsafe_model_output(reply)
    if flags:
        print(f"[flags: {', '.join(flags)}]", flush=True)
    print("\n--- proposal (not authority) ---\n", flush=True)
    print(reply, flush=True)
    print("\n--- end — edit CURRENT yourself (e) or save with w ---\n", flush=True)
    last.clear()
    last.append(reply)


def write_proposal(root: Path, last: list[str]) -> None:
    if not last:
        print("no proposal in memory — press g first", flush=True)
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


def run_desk(root: Path) -> int:
    root = project_root(root)
    last: list[str] = []
    print(banner(root), flush=True)
    while True:
        print("\nkey> ", end="", flush=True)
        k = get_key()
        if not k:
            continue
        # echo key when raw mode hides it
        if sys.stdin.isatty():
            print(k, flush=True)
        if k in ("q", "x"):
            print("bye", flush=True)
            return 0
        if k in ("?", "h"):
            print(HELP, flush=True)
            continue
        if k == "c":
            t = read_current(root)
            print(t if t else "(no CURRENT.md)", flush=True)
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
            print(banner(root), flush=True)
            continue
        if k in ("n", "p"):
            t = read_current(root)
            if not t:
                print("no CURRENT.md", flush=True)
                continue
            nxt = parse_next(t)
            if not nxt or nxt.lower() in ("unset", "(unset)"):
                print("Next is unset — edit CURRENT (e)", flush=True)
                continue
            if k == "n":
                print(f"Next: {nxt}", flush=True)
            code, out = run_aether(["preflight", nxt, str(root)], root)
            print(out or f"(exit {code})", flush=True)
            continue
        if k == "g":
            ask_model(root, last)
            continue
        if k == "w":
            write_proposal(root, last)
            continue
        print(f"unknown key {k!r} — press ?", flush=True)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Minimal CURRENT.md hotkey desk")
    ap.add_argument(
        "path",
        nargs="?",
        default=".",
        help="project root (default: cwd)",
    )
    ap.add_argument(
        "--once",
        metavar="KEY",
        help="run one hotkey action and exit (for scripts/tests)",
    )
    args = ap.parse_args(argv)
    root = project_root(args.path)
    if args.once:
        # non-interactive single shot
        os.chdir(root)
        if args.once == "c":
            t = read_current(root)
            sys.stdout.write((t or "(no CURRENT.md)") + "\n")
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
    return run_desk(root)


if __name__ == "__main__":
    sys.exit(main())
