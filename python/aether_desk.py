#!/usr/bin/env python3
"""Straight-to-chat terminal. No slash commands. No technical chrome.

Loads keys from env or a .env file (KEY=value or raw sk-or- / gsk_ lines).
CURRENT.md is silent context for the model when present — not shown as UI.
Empty line is not yes. Type bye / quit / exit to leave (or Ctrl-D).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
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


PRIVACY = """\
────────────────────────────────────────
  PRIVACY

  This chat talks to a cloud model.
  Do not paste passwords, bank details,
  health records, or secrets you would
  not put in an email.

  What you type may leave this device.
  Conversations are not a legal vault.
────────────────────────────────────────"""

BANNER = """\
  Hello.

  Type anything to begin.
  (empty line waits · bye to leave)
"""

SYSTEM = """You are a calm, helpful assistant in a private chat (terminal or living-room Desk).

You are a probabilistic model: you propose ideas and wording; you do not control the user's machine or grant permissions. Silence from the user is never agreement.

CURRENT.md is the product and the live authority. Re-read it as the foundation for every turn. The human owns it; you only propose wording or edits until a human applies a proposal. Never claim you approved, advanced Next, or changed CURRENT.

If a movies index or navigation help is provided, use it for suggestions only. Never claim you started playback or changed device settings.

Keep answers clear and human. Avoid jargon, stack traces, and tool dumps unless asked.
"""

# Living-room / House TV profile (same doctrine; warmer, parent-facing).
SYSTEM_HOUSE = """You are Desk — calm house helper for Client-one architecture tests.

CURRENT.md is the product: human-owned authority on the right of the Desk UI. Every answer must respect that file as foundational understanding (Objective, Next, Keep, Reject, Prohibited). Revisit it whenever the human speaks. Until the human applies a proposal, you only propose — you never approve, never write authority, never treat silence as permission.

Propose movie ideas or navigation tips only when they fit CURRENT. Do not control the TV or start playback.

Keep answers short, warm, and free of developer jargon unless asked.
"""

MAX_HISTORY = 24
_FIELD_RE = re.compile(
    r"^\*\*(?P<name>[^*]+?):?\*\*\s*:?\s*(?P<val>.*)$",
    re.IGNORECASE,
)

EXTRA_CONTEXT_FILES = (
    "library/movies-index.md",
    "library/navigate-help.md",
)


def project_root(path: str | Path | None = None) -> Path:
    p = Path(path or os.getcwd()).resolve()
    if p.is_file():
        p = p.parent
    return p


def load_dotenv_files() -> None:
    """Load keys without requiring python-dotenv. Never print values."""
    candidates = [
        Path.home() / "Desktop" / ".env",
        Path.home() / ".env",
        project_root() / ".env",
        Path("/etc/chat.env"),
        Path("/root/.chat.env"),
    ]
    for path in candidates:
        try:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            # CI/sandbox may block /root/.chat.env etc. without denying other keys
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line and not line.startswith("sk-") and not line.startswith("gsk_"):
                k, _, v = line.partition("=")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and v and k not in os.environ:
                    os.environ[k] = v
                continue
            # raw key lines (Desktop .env style)
            if line.startswith("sk-or-") and "OPENROUTER_API_KEY" not in os.environ:
                os.environ["OPENROUTER_API_KEY"] = line
            elif line.startswith("gsk_") and "GROQ_API_KEY" not in os.environ:
                os.environ["GROQ_API_KEY"] = line
            elif line.startswith("xai-") and "XAI_API_KEY" not in os.environ:
                os.environ["XAI_API_KEY"] = line
            elif line.startswith("sk-ant-") and "ANTHROPIC_API_KEY" not in os.environ:
                os.environ["ANTHROPIC_API_KEY"] = line
            # ghp_ and other tokens: leave as GITHUB_TOKEN if unset (not for chat)
            elif line.startswith("ghp_") and "GITHUB_TOKEN" not in os.environ:
                os.environ["GITHUB_TOKEN"] = line

    # Prefer free OpenRouter when key present
    if os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("AETHER_LLM_PROVIDER"):
        os.environ.setdefault("AETHER_LLM_PROVIDER", "openrouter")
        os.environ.setdefault("AETHER_MODEL", "openrouter/free")


def read_current(root: Path) -> Optional[str]:
    cf = root / "CURRENT.md"
    if not cf.is_file():
        return None
    try:
        return cf.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def read_extra_context(root: Path) -> str:
    """Optional library / help files for House TV desk (propose substrate only)."""
    chunks: List[str] = []
    for rel in EXTRA_CONTEXT_FILES:
        path = root / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if len(text) > 8000:
            text = text[:8000] + "\n…"
        chunks.append(f"--- {rel} ---\n{text}")
    return "\n\n".join(chunks)


def system_prompt_for(root: Path) -> str:
    """Pick system prompt: house profile when CURRENT/domain looks like House TV."""
    profile = (os.environ.get("AETHER_DESK_PROFILE") or "").strip().lower()
    if profile in ("house", "tv", "house-tv"):
        return SYSTEM_HOUSE
    current = read_current(root) or ""
    if "House TV" in current or "living-room" in current.lower() or "Kodi" in current:
        return SYSTEM_HOUSE
    return SYSTEM


def append_chat_log(root: Path, role: str, text: str) -> None:
    try:
        aether = root / ".aether"
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


def build_messages(root: Path, history: List[dict]) -> List[dict[str, str]]:
    current = read_current(root)
    system = system_prompt_for(root)
    if current:
        if len(current) > 12000:
            current = current[:12000] + "\n…"
        system = system + "\n\nProject note (human-owned):\n" + current
    extra = read_extra_context(root)
    if extra:
        system = system + "\n\nLocal notes (human-owned propose substrate):\n" + extra
    msgs: List[dict[str, str]] = [{"role": "system", "content": system}]
    for m in history[-MAX_HISTORY:]:
        msgs.append({"role": m["role"], "content": m["content"]})
    return msgs


def is_exit(text: str) -> bool:
    t = text.strip().lower()
    return t in ("bye", "quit", "exit", "q", ":q", "/quit", "/q")


def desk_turn(
    root: Path,
    message: str,
    history: Optional[List[dict]] = None,
    *,
    temperature: float = 0.55,
    log: bool = True,
) -> dict:
    """One propose-only chat turn (shared by TTY desk and HTTP bridge).

    Returns a dict:
      ok, reply, flags, history, backend, error?

    Empty / whitespace message → ok=False, error='empty' (silence ≠ permission).
    Does not write CURRENT.md. Does not execute tools.
    """
    root = project_root(root)
    load_dotenv_files()
    hist: List[dict] = list(history or [])
    text = (message or "").strip()
    if not text:
        return {
            "ok": False,
            "error": "empty",
            "reply": "",
            "flags": [],
            "history": hist,
            "backend": describe_backend() if describe_backend else "unavailable",
        }
    if chat is None:
        return {
            "ok": False,
            "error": "unavailable",
            "reply": "",
            "flags": [],
            "history": hist,
            "backend": "unavailable",
        }
    backend = describe_backend()
    if backend.startswith("none"):
        return {
            "ok": False,
            "error": "no_backend",
            "reply": "",
            "flags": [],
            "history": hist,
            "backend": backend,
        }

    hist.append({"role": "user", "content": text})
    if log:
        append_chat_log(root, "user", text)
    try:
        os.environ["AETHER_PERSONAL_LLM_SYSTEM"] = "0"
        reply = chat(build_messages(root, hist), temperature=temperature)
    except Exception as e:
        hist.pop()
        return {
            "ok": False,
            "error": "llm",
            "reply": "",
            "flags": [],
            "history": hist,
            "backend": backend,
            "detail": str(e) if os.environ.get("AETHER_DESK_DEBUG") else "",
        }

    flags = flag_unsafe_model_output(reply) if flag_unsafe_model_output else []
    hist.append({"role": "assistant", "content": reply})
    if log:
        append_chat_log(root, "assistant", reply)
    return {
        "ok": True,
        "error": "",
        "reply": reply,
        "flags": flags,
        "history": hist,
        "backend": backend,
    }


def run_chat(root: Path, *, quiet_errors: bool = True) -> int:
    root = project_root(root)
    load_dotenv_files()
    history: List[dict] = []

    print(PRIVACY, flush=True)
    print(BANNER, flush=True)

    if chat is None:
        print("Chat is unavailable right now. Please try again later.", flush=True)
        return 1
    if describe_backend().startswith("none"):
        print(
            "Chat needs a connection key. Add it and try again.",
            flush=True,
        )
        return 1

    while True:
        try:
            print("you> ", end="", flush=True)
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            print("\n", flush=True)
            continue
        if line == "":
            print("\nGoodbye.", flush=True)
            return 0
        text = line.rstrip("\n")
        if not text.strip():
            continue  # silence ≠ permission / not a prompt
        if is_exit(text):
            print("Goodbye.", flush=True)
            return 0

        result = desk_turn(root, text, history, log=True)
        history = list(result.get("history") or history)
        if not result.get("ok"):
            err = result.get("error") or "llm"
            if quiet_errors:
                print("\n(Something went wrong. Please try again.)\n", flush=True)
                if os.environ.get("AETHER_DESK_DEBUG") and result.get("detail"):
                    print(f"[{result['detail']}]", flush=True)
            else:
                print(f"\nerror: {err}\n", flush=True)
            # desk_turn already popped user on llm failure
            if err != "llm":
                history = [m for m in history if m is not None]
            continue

        flags = result.get("flags") or []
        if flags and os.environ.get("AETHER_DESK_DEBUG"):
            print(f"[flags: {', '.join(flags)}]", flush=True)
        print(f"\n{result.get('reply', '')}\n", flush=True)


def main(argv: Optional[list[str]] = None) -> int:
    load_dotenv_files()
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--help", "-h", action="store_true")
    ap.add_argument("--once", metavar="KEY")  # keep for tests: b|c
    ap.add_argument("--debug", action="store_true")
    args, _unknown = ap.parse_known_args(argv)

    if args.help:
        print("Chat. Type to talk. bye to leave.", flush=True)
        return 0
    if args.debug:
        os.environ["AETHER_DESK_DEBUG"] = "1"

    root = project_root(args.path)

    if args.once:
        # silent test hooks only
        if args.once == "b":
            print(PRIVACY)
            print(BANNER)
            return 0
        if args.once == "c":
            t = read_current(root)
            sys.stdout.write((t or "") + ("\n" if t else ""))
            return 0
        if args.once == "backend":
            print(describe_backend())
            return 0
        return 2

    if not sys.stdin.isatty():
        print(PRIVACY)
        print(BANNER)
        return 1

    return run_chat(root)


if __name__ == "__main__":
    sys.exit(main())
