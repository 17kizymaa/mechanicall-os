#!/bin/sh
# Week 7 host rehearsal. Temp pocket only. Never operator CURRENT. Never the host twin.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
export AETHER_HOME="$ROOT"
export PYTHONPATH="$ROOT/python${PYTHONPATH:+:$PYTHONPATH}"

echo "refuse operator bind..."
if sh "$ROOT/scripts/pocket-refuse-root.sh" "$ROOT"; then
  echo "FAIL: operator bind was allowed" >&2
  exit 1
fi
echo "  refused (expected)"

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/pocket-rehearse.XXXXXX")"
trap 'rm -rf "$WORKDIR"' EXIT
"$ROOT/aether" current init "$WORKDIR"
cp "$ROOT/examples/pocket-demo-client/CURRENT.md" "$WORKDIR/CURRENT.md"
python3 - "$WORKDIR" <<'PY'
import sys
from pathlib import Path

from aether_pocket import current, current_validate, not_yet, write_propose, yes  # noqa: E402

pocket = Path(sys.argv[1])
propose = """# Proposed CURRENT update (draft — not authority)

## Proposed CURRENT change

```markdown
**Objective:** Rehearse one Yes on a temp pocket (not a sitting).
**Phase:** APPROVE
**Status:** APPROVED
**Next:** rehearsal-buy-starts
**Approval:** PENDING
```
"""
before = (pocket / "CURRENT.md").read_text(encoding="utf-8")
cur = current(pocket)
assert cur.ok, cur.text
assert "name-the-outcome" in cur.text, cur.text
val = current_validate(pocket)
assert val.ok, val.text
write_propose(pocket, propose)
assert (pocket / "CURRENT.md").read_text(encoding="utf-8") == before
r = yes(pocket, reason="host rehearsal — not a sitting")
assert r.ok, r.text
body = (pocket / "CURRENT.md").read_text(encoding="utf-8")
assert "rehearsal-buy-starts" in body, body
rec = (pocket / "RECEIPT.md").read_text(encoding="utf-8")
assert "You said Yes" in rec, rec
n = not_yet(pocket, reason="rehearsal hold")
assert n.ok, n.text
rec2 = (pocket / "RECEIPT.md").read_text(encoding="utf-8")
assert "You said Not yet" in rec2, rec2
print("REHEARSE: OK")
PY
