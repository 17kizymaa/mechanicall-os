#!/usr/bin/env python3
"""alias-links.py — read-only LINKS table from projects/*/POINTER.md.

    scripts/alias-links.py [--root DIR] [--base URL] [--out FILE] [--json]

Columns: alias · room URL · status · has-opener · has-intake

  room URL    <base>/you-decide/t/<32-hex id> from the POINTER "Room id" row;
              "unminted" when no id is present
  status      the POINTER "| Status |" row if present, else the first bold
              phrase in the header line, else "-"
  has-opener  PROPOSALS/OPENER.md exists (kit) or POINTER mentions an opener
  has-intake  INTAKE.md exists and has at least one non-empty quoted answer

Never writes into --root. Prints Markdown to stdout unless --out is given
(--out may live anywhere; the operator decides). Never mints. Never shares.
Paper/stocks flag is informational only and comes from the fixed allow-list.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"\b([0-9a-f]{32})\b")
ROOM_ROW_RE = re.compile(r"^\|\s*Room(?: id)?\s*\|\s*(.*?)\s*\|\s*$", re.I | re.M)
STATUS_ROW_RE = re.compile(r"^\|\s*Status\s*\|\s*(.*?)\s*\|\s*$", re.I | re.M)
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
QUOTE_ANSWER_RE = re.compile(r"^>\s*\S", re.M)

# The only room allowed the Paper dock. Kit is generic otherwise; this is the
# one alias name CURRENT.md permits to be hard-coded.
PAPER_ALLOW = {"e9b16791a12ac1ef521891b6eac3bf68": "happy-birthday"}


def strip_md(s: str) -> str:
    s = s.replace("`", "")
    s = BOLD_RE.sub(r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def scan(alias_dir: Path, base: str) -> dict:
    alias = alias_dir.name
    pointer = read(alias_dir / "POINTER.md")

    room_id = None
    m = ROOM_ROW_RE.search(pointer)
    if m:
        idm = ID_RE.search(m.group(1))
        if idm:
            room_id = idm.group(1)
    if room_id is None:
        idm = ID_RE.search(pointer)
        if idm:
            room_id = idm.group(1)

    url = f"{base.rstrip('/')}/you-decide/t/{room_id}" if room_id else "unminted"

    status = "-"
    sm = STATUS_ROW_RE.search(pointer)
    if sm:
        status = strip_md(sm.group(1))
    else:
        head = pointer.splitlines()[0] if pointer else ""
        hm = re.search(r"\((.*?)\)", head)
        if hm:
            status = strip_md(hm.group(1))

    opener_file = alias_dir / "PROPOSALS" / "OPENER.md"
    has_opener = opener_file.is_file() and bool(read(opener_file).strip())
    if not has_opener and re.search(r"\bopener\b", pointer, re.I):
        has_opener = "pointer-only"

    intake_file = alias_dir / "INTAKE.md"
    intake = read(intake_file)
    if not intake_file.is_file():
        has_intake = False
    elif QUOTE_ANSWER_RE.search(intake):
        has_intake = True
    else:
        has_intake = "empty"

    return {
        "alias": alias,
        "room_id": room_id,
        "url": url,
        "status": status,
        "has_pointer": bool(pointer),
        "has_opener": has_opener,
        "has_intake": has_intake,
        "paper": PAPER_ALLOW.get(room_id or "", None),
        "client_current": (alias_dir / "CURRENT.md").exists(),
    }


def yn(v) -> str:
    if v is True:
        return "yes"
    if v is False:
        return "no"
    return str(v)


def render_md(rows: list[dict], root: Path, base: str) -> str:
    out = []
    out.append("# LINKS — operator only")
    out.append("")
    out.append("**Not waitlist. Not Yes. Send is hello.** You share, or not.")
    out.append("")
    out.append(f"Root: `{root}` · Base: `{base}` · Rooms: {sum(1 for r in rows if r['room_id'])}/{len(rows)} minted")
    paper = [r for r in rows if r["paper"]]
    out.append(
        "Paper stays on "
        + (", ".join(f"`{r['alias']}`" for r in paper) if paper else "**nobody**")
        + " only. `DEFAULT_PAPER_TICKETS` untouched."
    )
    out.append("")
    out.append("| Alias | Room | Status | Opener | Intake |")
    out.append("|-------|------|--------|--------|--------|")
    for r in rows:
        room = r["url"] if r["room_id"] else "**unminted**"
        st = r["status"]
        if r["paper"]:
            st += " · Paper owner"
        out.append(f"| `{r['alias']}` | {room} | {st} | {yn(r['has_opener'])} | {yn(r['has_intake'])} |")
    flags = []
    for r in rows:
        if not r["has_pointer"]:
            flags.append(f"`{r['alias']}`: no POINTER.md")
        if r["client_current"]:
            flags.append(f"`{r['alias']}`: client CURRENT.md present — CURRENT forbids nested/client CURRENT")
        if r["has_opener"] is False:
            flags.append(f"`{r['alias']}`: no PROPOSALS/OPENER.md — run alias-scaffold.sh")
    if flags:
        out.append("")
        out.append("## FLAGS")
        out.append("")
        out.extend(f"- {f}" for f in flags)
    out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.environ.get("ANPHUNI_ROOT", os.path.expanduser("~/anphuni-project")))
    ap.add_argument("--base", default="https://anphuni.com", help="room base URL (local sit: http://127.0.0.1:8788)")
    ap.add_argument("--out", help="write Markdown here instead of stdout (never inside --root/projects)")
    ap.add_argument("--json", action="store_true", help="emit JSON rows instead of Markdown")
    a = ap.parse_args(argv)

    root = Path(a.root).expanduser().resolve()
    projects = root / "projects"
    if not projects.is_dir():
        print(f"no projects/ under {root}", file=sys.stderr)
        return 2

    rows = [scan(d, a.base) for d in sorted(projects.iterdir()) if d.is_dir() and not d.name.startswith(".")]

    if a.json:
        text = json.dumps(rows, indent=2) + "\n"
    else:
        text = render_md(rows, root, a.base)

    if a.out:
        outp = Path(a.out).expanduser().resolve()
        if projects in outp.parents:
            print("refuse: --out must not be inside projects/ (read-only tree)", file=sys.stderr)
            return 3
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(text, encoding="utf-8")
        print(f"wrote {outp}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
