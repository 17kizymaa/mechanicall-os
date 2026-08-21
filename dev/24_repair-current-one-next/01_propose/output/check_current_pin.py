#!/usr/bin/env python3
"""Exit 0 iff CURRENT.md header Next == body Action id. Read-only."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[4]
    path = root / "CURRENT.md"
    text = path.read_text(encoding="utf-8")
    header = re.search(r"^\*\*Next:\*\*\s*(.+)$", text, re.M)
    body = re.search(r"^\*\*Action id:\*\*\s*`?([^`\n]+)`?", text, re.M)
    nxt = header.group(1).strip() if header else ""
    act = body.group(1).strip() if body else ""
    if not nxt or not act:
        print(f"FAIL: missing pin header={nxt!r} action={act!r}", file=sys.stderr)
        return 3
    if nxt != act:
        print(f"FAIL: header Next={nxt!r} != Action id={act!r}", file=sys.stderr)
        return 3
    print(f"OK: Next == Action id == {nxt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
