#!/usr/bin/env python3
"""Rival Editor v0 — turn-based anti-convergence.

Usage:
  aether rival --track "JRJRJR" --read "VHS grain, dark cold open"
  aether rival --track "JRJRJR" --structure "0-8 cold; hook densest" --read "..."
  echo "my read" | aether rival --track "JRJRJR"

Logs both sides into ./.session.md (state ledger). Prompt is verbatim from
skills/rival-editor/PROMPT.md — do not soften.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aether_llm import chat, describe_backend  # noqa: E402


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_system_prompt() -> str:
    path = package_root() / "skills" / "rival-editor" / "PROMPT.md"
    text = path.read_text()
    # extract first fenced block (verbatim system prompt)
    m = re.search(r"```\n(.*?)```", text, re.DOTALL)
    if not m:
        raise RuntimeError(f"no fenced system prompt in {path}")
    return m.group(1).strip()


def session_path(cwd: Path | None = None) -> Path:
    root = cwd or Path.cwd()
    return root / ".session.md"


def append_session(lines: list[str], cwd: Path | None = None) -> Path:
    path = session_path(cwd)
    if not path.is_file():
        name = path.parent.name
        path.write_text(
            f"# Session ledger — {name}\n\n"
            "Inputs (what was playing) and outputs (what got made).\n"
            "The middle stays unmanaged. Rival turns land here too.\n\n"
        )
    with path.open("a") as f:
        for line in lines:
            f.write(f"- {now_iso()} {line}\n")
    return path


def build_user_msg(track: str, structure: str, read: str, narration: str) -> str:
    parts = [f"Track: {track}"]
    if structure:
        parts.append(f"Structure: {structure}")
    if narration:
        parts.append(f"Listening narration:\n{narration}")
    parts.append(f"Author visual read: {read}")
    parts.append("Return one counter-treatment only.")
    return "\n\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aether rival")
    p.add_argument("--track", "-t", default="", help="track title")
    p.add_argument("--structure", "-s", default="", help="section map / structure notes")
    p.add_argument("--read", "-r", default="", help="your one-line (or short) visual read")
    p.add_argument("--narration", "-n", default="", help="listening-experiment text if any")
    p.add_argument(
        "--no-log",
        action="store_true",
        help="print only; do not append .session.md",
    )
    p.add_argument(
        "read_pos",
        nargs="*",
        help="visual read as positional args (alternative to --read)",
    )
    args = p.parse_args(argv)

    read = args.read.strip() or " ".join(args.read_pos).strip()
    if not read and not sys.stdin.isatty():
        read = sys.stdin.read().strip()
    if not read:
        print(
            "aether rival: need a visual read\n"
            '  aether rival --track "JRJRJR" --read "VHS grain cold open"',
            file=sys.stderr,
        )
        return 2

    track = args.track.strip() or os.environ.get("AETHER_RIVAL_TRACK", "untitled")
    system = load_system_prompt()
    user = build_user_msg(track, args.structure.strip(), read, args.narration.strip())

    print(f"aether rival: backend {describe_backend()}", file=sys.stderr)
    try:
        out = chat(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.9,
        )
    except Exception as e:
        print(f"aether rival: {e}", file=sys.stderr)
        return 1

    # one treatment, under 200 words — soft trim only if wildly long
    words = out.split()
    if len(words) > 220:
        out = " ".join(words[:200]) + "…"

    print(out)

    if not args.no_log:
        condensed = " ".join(out.split())
        if len(condensed) > 280:
            condensed = condensed[:277] + "…"
        path = append_session(
            [
                f"rival-in: track={track} read={read}",
                f"rival: {condensed}",
            ]
        )
        print(f"\nlogged → {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
