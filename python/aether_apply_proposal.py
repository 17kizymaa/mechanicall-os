#!/usr/bin/env python3
"""Extract a CURRENT body from a proposal file. Does not write CURRENT.md.

The shell verb `aether apply` is the writer. This script only extracts.

A proposal wrapper (preamble, APPLY banner, fidelity notes) must not become
CURRENT.md. That was the proposal-wrapper-as-CURRENT miss. The body is either:

- the file itself, when its first content line is exactly `# CURRENT`, or
- the fenced block after the last "Proposed CURRENT" heading, when that
  fence's first content line is exactly `# CURRENT`.

Exit 0 writes the body to --out.
Exit 2 is usage.
Exit 3 is a protocol refuse (message on stderr, nothing written to --out).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FENCE_RE = re.compile(
    r"```(?:markdown|md)?[ \t]*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)
HEADING_RE = re.compile(
    r"^#{1,3}[ \t]+Proposed CURRENT\b.*$",
    re.MULTILINE | re.IGNORECASE,
)


def refuse(message: str) -> int:
    print(f"refuse: {message}", file=sys.stderr)
    return 3


def first_content_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def is_current_title(line: str) -> bool:
    return bool(re.match(r"^# CURRENT\s*$", line))


def normalize(text: str) -> str:
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) + "\n"


def field_tokens(body: str, label: str) -> list[str]:
    pat = re.compile(
        rf"^\*\*{re.escape(label)}:\*\*\s*(.*?)\s*$",
        re.MULTILINE | re.IGNORECASE,
    )
    out: list[str] = []
    for match in pat.finditer(body):
        raw = match.group(1).strip().strip("`").strip()
        if not raw:
            continue
        token = raw.split()[0].strip("`")
        if token:
            out.append(token)
    return out


def extract_body(text: str) -> str | int:
    """Return the CURRENT body, or an exit code (int) on refuse."""
    if is_current_title(first_content_line(text)):
        body = normalize(text)
    else:
        headings = list(HEADING_RE.finditer(text))
        if not headings:
            return refuse(
                "proposal has no '# CURRENT' body and no 'Proposed CURRENT' heading"
                " — will not copy the wrapper"
            )
        start = headings[-1].end()
        chosen = ""
        for fence in FENCE_RE.finditer(text, start):
            block = fence.group(1)
            if is_current_title(first_content_line(block)):
                chosen = block
                break
        if not chosen:
            return refuse(
                "no fenced '# CURRENT' body after 'Proposed CURRENT'"
                " — will not copy the wrapper"
            )
        body = normalize(chosen)

    if not is_current_title(first_content_line(body)):
        return refuse("extracted text is not a CURRENT body")

    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("APPLY:") or stripped.startswith("**APPLY:"):
            return refuse("extracted body still has the proposal APPLY banner")
        if stripped.lower().startswith("# current proposal"):
            return refuse("extracted body is still a proposal wrapper")

    nexts = field_tokens(body, "Next")
    if len(nexts) != 1:
        return refuse(f"proposal body has {len(nexts)} **Next:** lines; want one")
    actions = field_tokens(body, "Action id")
    mismatched = [item for item in actions if item.casefold() != nexts[0].casefold()]
    if mismatched:
        return refuse(
            f"header Next ({nexts[0]}) does not match Action id ({mismatched[0]})"
        )
    return body


def main(argv: list[str]) -> int:
    out_path: str | None = None
    proposal: str | None = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--out":
            if i + 1 >= len(argv):
                print("usage: aether_apply_proposal.py --out FILE PROPOSAL", file=sys.stderr)
                return 2
            out_path = argv[i + 1]
            i += 2
            continue
        if arg.startswith("-"):
            print("usage: aether_apply_proposal.py --out FILE PROPOSAL", file=sys.stderr)
            return 2
        if proposal is None:
            proposal = arg
            i += 1
            continue
        print("usage: aether_apply_proposal.py --out FILE PROPOSAL", file=sys.stderr)
        return 2
    if not out_path or not proposal:
        print("usage: aether_apply_proposal.py --out FILE PROPOSAL", file=sys.stderr)
        return 2

    path = Path(proposal)
    if not path.is_file():
        print(f"aether: no proposal file: {proposal}", file=sys.stderr)
        return 1
    extracted = extract_body(path.read_text(encoding="utf-8"))
    if isinstance(extracted, int):
        return extracted
    dest = Path(out_path)
    dest.write_text(extracted, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
