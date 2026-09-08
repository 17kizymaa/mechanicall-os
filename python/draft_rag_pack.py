#!/usr/bin/env python3
"""Pack a Draft RAG blob: bound papers + curated CURRENT examples.

No chroma. No network. Never writes CURRENT.md. Propose/taste only.
USB ≠ LTE. Confirm not tapped.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = ROOT / "examples" / "propose-current"
AUTHORITY = ("CURRENT.md", "PROPOSE-CURRENT.md", "RECEIPT.md")
SKIP_NAMES = {".env", "adbkey", "id_rsa"}
MAX_FILE = 8_000
DEFAULT_CAP = 24_000


def _read(path: Path, cap: int = MAX_FILE) -> str:
    if not path.is_file() or path.name in SKIP_NAMES:
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if len(text) > cap:
        return text[: cap] + "\n…[truncated]\n"
    return text


def pack(
    pocket: Path,
    *,
    corpus: Path = DEFAULT_CORPUS,
    max_bytes: int = DEFAULT_CAP,
    shots: int = 4,
) -> str:
    """Folder-walk RAG for prose→PROPOSE. Retrieved text is evidence, not law."""
    parts: list[str] = []
    used = 0

    def add(title: str, body: str) -> bool:
        nonlocal used
        if not body.strip():
            return True
        chunk = f"\n--- {title} ---\n{body.strip()}\n"
        if used + len(chunk) > max_bytes:
            parts.append(f"\n--- {title} --- [cap]\n")
            return False
        parts.append(chunk)
        used += len(chunk)
        return True

    pocket = pocket.resolve()
    add("BOUND CURRENT.md (law — do not write)", _read(pocket / "CURRENT.md"))
    add("BOUND PROPOSE-CURRENT.md (edit this only)", _read(pocket / "PROPOSE-CURRENT.md"))
    rec = pocket / "RECEIPT.md"
    if rec.is_file():
        add("BOUND RECEIPT.md (what happened)", _read(rec, cap=2_000))

    shots_dir = corpus if corpus.is_dir() else DEFAULT_CORPUS
    prefer = (
        "CURRENT-you-decide-ritual.md",
        "CURRENT-sit-bound-draft.md",
        "CURRENT-you-decide-casual.md",
        "PROPOSE-TEMPLATE.md",
    )
    names = [n for n in prefer if (shots_dir / n).is_file()]
    extra = sorted(p.name for p in shots_dir.glob("CURRENT-*.md") if p.name not in names)
    for name in (names + extra)[:shots]:
        if not add(f"FEW-SHOT {name}", _read(shots_dir / name, cap=4_000)):
            break

    header = (
        "Draft RAG pack. Evidence only. Never approve. Never write CURRENT.md.\n"
        "Output belongs in PROPOSE-CURRENT.md. Mark NOT ACTIVE. Schema merge; prose stays.\n"
    )
    return header + "".join(parts)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pocket", type=Path, help="bound folder (not this operator tree)")
    ap.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    ap.add_argument("--max-bytes", type=int, default=DEFAULT_CAP)
    ap.add_argument("--shots", type=int, default=4)
    args = ap.parse_args(argv)
    if not args.pocket.is_dir():
        print(f"missing pocket: {args.pocket}", file=sys.stderr)
        return 2
    blob = pack(args.pocket, corpus=args.corpus, max_bytes=args.max_bytes, shots=args.shots)
    print(blob)
    print(f"\n# bytes={len(blob)} files_hint=CURRENT+PROPOSE+RECEIPT+shots", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
