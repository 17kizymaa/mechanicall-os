#!/usr/bin/env python3
"""Copy client CURRENT packs out of mechanicall-os git. Leave Approval PENDING.

Usage:
  python3 copy_out_packs.py <src-clients-dir> <dest-root>
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

ALIASES = ("happy-birthday", "hi-its-mother", "this-works")
FILES = ("CURRENT.md", "HOW-TO-ACCEPT.md")


def approval_line(text: str) -> str:
    for line in text.splitlines():
        low = line.lower().lstrip()
        if low.startswith("**approval:**") or low.startswith("**approval**:"):
            return line.split(":", 1)[1].replace("*", "").strip()
    return ""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: copy_out_packs.py <src-clients-dir> <dest-root>", file=sys.stderr)
        return 2
    src_root = Path(sys.argv[1]).resolve()
    dest_root = Path(sys.argv[2]).resolve()
    git_top = Path("/mnt/kingston-nixos-sync/opt/mechanicall-os").resolve()
    try:
        dest_root.relative_to(git_top)
    except ValueError:
        pass
    else:
        print(f"refuse: dest is inside mechanicall-os git: {dest_root}", file=sys.stderr)
        return 3

    dest_root.mkdir(parents=True, exist_ok=True)
    for alias in ALIASES:
        src = src_root / alias
        dest = dest_root / alias
        if not src.is_dir():
            print(f"missing source {src}", file=sys.stderr)
            return 1
        dest.mkdir(parents=True, exist_ok=True)
        for name in FILES:
            s = src / name
            if not s.is_file():
                print(f"missing {s}", file=sys.stderr)
                return 1
            shutil.copy2(s, dest / name)
        current = dest / "CURRENT.md"
        appr = approval_line(current.read_text())
        if appr.upper() != "PENDING":
            print(f"refuse: {alias} Approval is {appr!r} (need PENDING)", file=sys.stderr)
            return 3
        print(f"{alias}\t{dest}\t{sha256(current)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
