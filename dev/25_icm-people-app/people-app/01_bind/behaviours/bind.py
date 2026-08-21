#!/usr/bin/env python3
"""Bind a project folder. Refuse the mechanicall-os operator tree."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Prefer shipped pocket refuse (same markers). Fall back to local check.
MARKERS = ("PRODUCT.md", "bin/aether", "CORE_PRINCIPLES.md", "AGENTS.md")


def _operator_home() -> Path | None:
    env = os.environ.get("AETHER_HOME")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for p in here.parents:
        if all((p / n).exists() for n in MARKERS):
            return p
    return None


def refuse_if_operator(path: Path) -> Path:
    root = path.expanduser().resolve()
    py = _operator_home()
    if py is not None:
        sys.path.insert(0, str(py / "python"))
        try:
            from aether_pocket import PocketError, refuse_if_operator as _ref

            return _ref(root)
        except ImportError:
            pass
    if all((root / n).exists() for n in MARKERS):
        raise SystemExit(
            f"refused: {root} is the mechanicall-os operator tree — "
            "bind a folder outside this repo"
        )
    return root


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: bind.py <project-folder>", file=sys.stderr)
        return 2
    try:
        root = refuse_if_operator(Path(sys.argv[1]))
    except Exception as exc:
        print(exc, file=sys.stderr)
        return 3
    root.mkdir(parents=True, exist_ok=True)
    out = Path(__file__).resolve().parents[1] / "output" / "BIND.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"# BIND\n\n"
        f"- path: `{root}`\n"
        f"- refuse-operator: passed (this is not the operator tree)\n"
        f"- CURRENT.md: {'present' if (root / 'CURRENT.md').is_file() else 'missing'}\n"
        f"- open-is-not-yes: true\n"
    )
    print(out)
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
