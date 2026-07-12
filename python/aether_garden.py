#!/usr/bin/env python3
"""RHIZOME layer 6 — gardener.

Proposes destinations for inbox seeds; never moves without [x] + apply.

  aether garden              # propose → ~/inbox-proposals.md
  aether garden apply        # move only checked lines
  aether garden status       # show pending proposals / backend

Destinations (apply understands):
  spark              → bullet on ~/prompts.md ($AETHER_SPARKS)
  trash              → ~/inbox-archive.md, drop from inbox
  note:/abs/or/rel   → append timestamped line to that .md (create ok)
  hold               → leave in inbox (explicit no-op on apply)
  project:/path      → append to /path/garden-seeds.md

Doctrine: capture stays sacred; structure is deferred to coffee-approval.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# package-local import when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aether_llm import chat, describe_backend  # noqa: E402


# Timestamp may include fractional seconds (…S.mmmZ) so rapid seeds stay unique.
SEED_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}T[^\s]+Z) (.+)$")
PROP_RE = re.compile(
    r"^- \[([ xX])\] `([^`]+)`\s*→\s*(.+)$"
)


def home() -> Path:
    return Path(os.environ.get("HOME", str(Path.home())))


def inbox_path() -> Path:
    return Path(os.environ.get("AETHER_INBOX", str(home() / "inbox.md")))


def proposals_path() -> Path:
    return Path(os.environ.get("AETHER_PROPOSALS", str(home() / "inbox-proposals.md")))


def sparks_path() -> Path:
    return Path(os.environ.get("AETHER_SPARKS", str(home() / "prompts.md")))


def archive_path() -> Path:
    return Path(os.environ.get("AETHER_INBOX_ARCHIVE", str(home() / "inbox-archive.md")))


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_seeds(text: str) -> list[tuple[str, str]]:
    """Return list of (iso, body) for seed lines."""
    out = []
    for line in text.splitlines():
        m = SEED_RE.match(line.strip())
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def heuristic_dest(body: str) -> str:
    b = body.strip()
    low = b.lower()
    if len(b) < 90 and not any(c in b for c in "?!."):
        # short oblique → spark deck
        if len(b.split()) <= 16:
            return "spark"
    if any(w in low for w in ("junk", "ignore", "trash", "nvm", "nevermind")):
        return "trash"
    if "reel" in low or "cut " in low or "resolve" in low:
        return f"note:{home() / 'reel' / 'notes' / 'seeds.md'}"
    return "hold"


def llm_propose(seeds: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """Return list of (iso, body, dest). Identity is full (iso, body) — timestamps may collide."""
    listing = "\n".join(f"{i+1}. {iso} {body}" for i, (iso, body) in enumerate(seeds))
    system = (
        "You are the RHIZOME gardener for a filesystem-first creative OS. "
        "Seeds must NOT be filed by the human at capture; you propose only. "
        "For each numbered seed pick exactly one destination:\n"
        "  spark — oblique creative prompt line for the spark deck\n"
        "  trash — noise, accidental, or empty\n"
        "  hold — leave in inbox for later\n"
        f"  note:{home() / 'reel' / 'notes' / 'seeds.md'} — edit/music thoughts\n"
        "  project:/absolute/dir — append to that dir's garden-seeds.md\n"
        "Prefer hold when unsure. Prefer spark for short oblique one-liners. "
        "Use real absolute paths under the user's home, never /home/user. "
        "Reply with ONLY lines of the form:\n"
        "N | destination\n"
        "where N is the seed number. No commentary."
    )
    user = f"Seeds:\n{listing}\n\nDestinations:"
    try:
        raw = chat(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
        )
    except Exception as e:
        print(f"aether garden: LLM unavailable ({e}); using heuristic", file=sys.stderr)
        return [(iso, body, heuristic_dest(body)) for iso, body in seeds]

    results: list[tuple[str, str, str] | None] = [None] * len(seeds)
    for line in raw.splitlines():
        line = line.strip().lstrip("-").strip()
        if "|" not in line:
            continue
        left, right = line.split("|", 1)
        num_s = left.strip().split()[0].rstrip(".")
        dest = right.strip().split()[0] if right.strip() else "hold"
        try:
            idx = int(num_s) - 1
        except ValueError:
            continue
        if 0 <= idx < len(seeds) and results[idx] is None:
            iso, body = seeds[idx]
            results[idx] = (iso, body, _clean_dest(dest))
    out: list[tuple[str, str, str]] = []
    for i, row in enumerate(results):
        if row is None:
            iso, body = seeds[i]
            out.append((iso, body, heuristic_dest(body)))
        else:
            out.append(row)
    return out


def _clean_dest(dest: str) -> str:
    dest = dest.strip().strip("`").rstrip(".,;")
    # models sometimes invent /home/user — rewrite to real $HOME
    fake = "/home/user"
    real = str(home())
    if fake in dest:
        dest = dest.replace(fake, real)
    if dest.startswith("~/"):
        dest = str(home() / dest[2:])
        if not dest.startswith("note:") and dest.endswith(".md"):
            dest = f"note:{dest}"
    if dest in ("spark", "trash", "hold"):
        return dest
    if dest.startswith("note:") or dest.startswith("project:"):
        kind, _, rest = dest.partition(":")
        rest = rest.strip().replace(fake, real)
        if rest.startswith("~/"):
            rest = str(home() / rest[2:])
        return f"{kind}:{rest}"
    if dest.endswith(".md"):
        p = dest.replace(fake, real)
        if p.startswith("~/"):
            p = str(home() / p[2:])
        return f"note:{p}"
    return "hold"


def write_proposals(rows: list[tuple[str, str, str]], backend: str) -> Path:
    path = proposals_path()
    lines = [
        f"# Inbox proposals — {now_iso()}",
        "",
        "Approve with coffee: change `[ ]` to `[x]`, then run `aether garden apply`.",
        "Nothing moves without a check. Unchecked / rejected seeds stay in the inbox.",
        "",
        f"_backend: {backend}_",
        "",
    ]
    for iso, body, dest in rows:
        # escape backticks in body
        safe = body.replace("`", "'")
        lines.append(f"- [ ] `{iso} {safe}` → {dest}")
    lines.append("")
    path.write_text("\n".join(lines) + "\n")
    return path


def cmd_propose() -> int:
    inbox = inbox_path()
    if not inbox.is_file():
        print(f"aether garden: no inbox at {inbox}", file=sys.stderr)
        return 1
    seeds = parse_seeds(inbox.read_text())
    if not seeds:
        print(f"aether garden: inbox empty of seeds ({inbox})")
        return 0
    backend = describe_backend()
    print(f"aether garden: {len(seeds)} seed(s), backend {backend}")
    rows = llm_propose(seeds)
    path = write_proposals(rows, backend)
    print(f"proposals → {path}")
    print("edit checks, then: aether garden apply")
    return 0


def parse_proposals(text: str) -> list[tuple[bool, str, str]]:
    """(checked, seed_key, dest) where seed_key is 'iso body'."""
    out = []
    for line in text.splitlines():
        m = PROP_RE.match(line.strip())
        if not m:
            continue
        checked = m.group(1).lower() == "x"
        key = m.group(2).strip()
        dest = m.group(3).strip()
        out.append((checked, key, dest))
    return out


def remove_seed_from_inbox(iso: str, body_prefix: str) -> bool:
    """Remove one seed matching iso + body prefix (first match only)."""
    inbox = inbox_path()
    if not inbox.is_file():
        return False
    lines = inbox.read_text().splitlines(True)
    kept = []
    removed = False
    for line in lines:
        m = SEED_RE.match(line.strip())
        if (
            not removed
            and m
            and m.group(1) == iso
            and (
                m.group(2) == body_prefix
                or m.group(2).startswith(body_prefix[:40])
                or body_prefix.startswith(m.group(2)[:40])
            )
        ):
            removed = True
            continue
        kept.append(line)
    if removed:
        inbox.write_text("".join(kept))
    return removed


def apply_dest(iso: str, body: str, dest: str) -> str:
    dest = dest.strip()
    if dest == "hold":
        return "hold (left in inbox)"
    if dest == "spark":
        sp = sparks_path()
        if not sp.is_file():
            sp.write_text(
                "# Spark deck\n#\n# Only `- ` / `* ` lines are dealt by `aether spark`.\n\n"
            )
        with sp.open("a") as f:
            f.write(f"- {body}\n")
        remove_seed_from_inbox(iso, body)
        return f"spark → {sp}"
    if dest == "trash":
        ar = archive_path()
        if not ar.is_file():
            ar.write_text("# Inbox archive — trashed seeds\n\n")
        with ar.open("a") as f:
            f.write(f"- {iso} {body}\n")
        remove_seed_from_inbox(iso, body)
        return f"trash → {ar}"
    if dest.startswith("note:"):
        target = Path(dest[5:].strip()).expanduser()
        if not target.is_absolute():
            target = home() / target
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.is_file():
            target.write_text(f"# {target.name}\n\nGarden deposits.\n\n")
        with target.open("a") as f:
            f.write(f"- {iso} {body}\n")
        remove_seed_from_inbox(iso, body)
        return f"note → {target}"
    if dest.startswith("project:"):
        root = Path(dest[8:].strip()).expanduser()
        if not root.is_absolute():
            root = home() / root
        root.mkdir(parents=True, exist_ok=True)
        target = root / "garden-seeds.md"
        if not target.is_file():
            target.write_text(f"# Garden seeds — {root.name}\n\n")
        with target.open("a") as f:
            f.write(f"- {iso} {body}\n")
        remove_seed_from_inbox(iso, body)
        return f"project → {target}"
    return f"unknown dest {dest!r} (skipped)"


def cmd_apply() -> int:
    path = proposals_path()
    if not path.is_file():
        print(f"aether garden: no proposals at {path} — run aether garden first", file=sys.stderr)
        return 1
    props = parse_proposals(path.read_text())
    checked = [(k, d) for c, k, d in props if c]
    if not checked:
        print("aether garden: no [x] approvals — nothing moved")
        return 0
    n = 0
    for key, dest in checked:
        parts = key.split(" ", 1)
        if len(parts) != 2:
            print(f"  skip malformed: {key!r}")
            continue
        iso, body = parts[0], parts[1]
        msg = apply_dest(iso, body, dest)
        print(f"  {iso}: {msg}")
        n += 1
    # rewrite proposals: drop applied checks, keep open ones
    remaining = [line for line in path.read_text().splitlines() if not _is_checked_prop(line)]
    # ensure header exists
    if remaining and remaining[0].startswith("#"):
        path.write_text("\n".join(remaining) + "\n")
    else:
        path.write_text(
            f"# Inbox proposals — residual {now_iso()}\n\n"
            + "\n".join(remaining)
            + "\n"
        )
    print(f"applied {n} approval(s)")
    return 0


def _is_checked_prop(line: str) -> bool:
    m = PROP_RE.match(line.strip())
    return bool(m and m.group(1).lower() == "x")


def cmd_status() -> int:
    print(f"backend:   {describe_backend()}")
    print(f"inbox:     {inbox_path()} ({'yes' if inbox_path().is_file() else 'missing'})")
    if inbox_path().is_file():
        print(f"  seeds:   {len(parse_seeds(inbox_path().read_text()))}")
    print(f"proposals: {proposals_path()} ({'yes' if proposals_path().is_file() else 'missing'})")
    if proposals_path().is_file():
        props = parse_proposals(proposals_path().read_text())
        open_n = sum(1 for c, _, _ in props if not c)
        done_n = sum(1 for c, _, _ in props if c)
        print(f"  open: {open_n}  checked: {done_n}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aether garden")
    p.add_argument(
        "action",
        nargs="?",
        default="propose",
        choices=["propose", "apply", "status"],
        help="propose (default) | apply | status",
    )
    args = p.parse_args(argv)
    if args.action == "propose":
        return cmd_propose()
    if args.action == "apply":
        return cmd_apply()
    return cmd_status()


if __name__ == "__main__":
    sys.exit(main())
