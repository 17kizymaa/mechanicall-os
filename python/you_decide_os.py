#!/usr/bin/env python3
"""Pull/put You Decide tickets between anphuni.com and mechanicall-os inbox.

Not Yes. Public drop stays HTTPS. Lab 127.0.0.1 is not the public bind.
Capability id is the key. CURRENT.md is never written.

  python3 python/you_decide_os.py pull <id-or-url>
  python3 python/you_decide_os.py put-zip <id-or-url> <zip-path>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ID_RE = re.compile(r"([a-f0-9]{32})")
DROP_MAX = 8 * 1024 * 1024
ORIGIN_DEFAULT = "https://anphuni.com"


def inbox_tickets() -> Path:
    from aether_inbox import inbox_root

    return inbox_root() / "tickets"


def origin() -> str:
    import os

    return (os.environ.get("YOU_DECIDE_ORIGIN") or ORIGIN_DEFAULT).rstrip("/")


def parse_id(raw: str) -> str:
    m = ID_RE.search(raw.strip())
    if not m:
        raise SystemExit("need a 32-hex capability id or ticket URL")
    return m.group(1)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get(url: str, timeout: int = 60) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.headers.get("Content-Disposition") or ""
    except urllib.error.HTTPError as e:
        return e.code, e.read(), ""


def _put(url: str, body: bytes, content_type: str, timeout: int = 60) -> tuple[int, bytes]:
    req = urllib.request.Request(
        url,
        data=body,
        method="PUT",
        headers={"Content-Type": content_type, "Content-Length": str(len(body))},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def pull(id_or_url: str) -> dict:
    tid = parse_id(id_or_url)
    base = f"{origin()}/api/you-decide/t/{tid}"
    code, raw, _ = _get(base)
    if code != 200:
        raise SystemExit(f"ticket GET {code}: {raw[:400]!r}")
    meta = json.loads(raw.decode("utf-8"))
    dest = inbox_tickets() / tid
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "in").mkdir(exist_ok=True)
    notice = {
        "id": tid,
        "created": meta.get("created"),
        "pulled": _now(),
        "origin": origin(),
        "not_yes": True,
        "drop": meta.get("drop"),
        "zip": meta.get("zip") or {"ready": False},
        "note": "Pulled from the public door. Not CURRENT. Drop/download ≠ Yes.",
    }
    (dest / "NOTICE.json").write_text(json.dumps(notice, indent=2) + "\n", encoding="utf-8")
    propose = meta.get("propose") or "# Proposed CURRENT update (draft — not authority)\n\nNOT ACTIVE. Not the plan.\n"
    (dest / "propose.md").write_text(propose, encoding="utf-8")
    drop = meta.get("drop")
    landed = None
    if drop and drop.get("name"):
        dcode, dbytes, _ = _get(f"{base}/drop")
        if dcode != 200:
            raise SystemExit(f"drop GET {dcode}: {dbytes[:400]!r}")
        if len(dbytes) > DROP_MAX:
            raise SystemExit("drop over 8 MiB")
        name = Path(str(drop["name"])).name.replace("/", "_") or "upload"
        (dest / "in" / name).write_bytes(dbytes)
        landed = {"name": name, "bytes": len(dbytes)}
    return {
        "ok": True,
        "not_yes": True,
        "id": tid,
        "dest": str(dest),
        "drop": landed,
        "current_untouched": True,
    }


def put_zip(id_or_url: str, zip_path: str) -> dict:
    tid = parse_id(id_or_url)
    src = Path(zip_path).expanduser().resolve()
    if not src.is_file():
        raise SystemExit(f"no zip at {src}")
    blob = src.read_bytes()
    if not blob:
        raise SystemExit("empty zip")
    if len(blob) > DROP_MAX:
        raise SystemExit("zip over 8 MiB")
    base = f"{origin()}/api/you-decide/t/{tid}"
    code, raw = _put(f"{base}/zip", blob, "application/zip")
    if code != 200:
        raise SystemExit(f"zip PUT {code}: {raw[:400]!r}")
    dest = inbox_tickets() / tid
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "out.zip").write_bytes(blob)
    notice_path = dest / "NOTICE.json"
    notice = {}
    if notice_path.is_file():
        notice = json.loads(notice_path.read_text(encoding="utf-8"))
    notice.update(
        {
            "id": tid,
            "not_yes": True,
            "zip": {"ready": True, "bytes": len(blob), "at": _now()},
            "note": "Zip placed by operator. Download is not Yes.",
        }
    )
    notice_path.write_text(json.dumps(notice, indent=2) + "\n", encoding="utf-8")
    body = json.loads(raw.decode("utf-8"))
    return {
        "ok": True,
        "not_yes": True,
        "id": tid,
        "bytes": len(blob),
        "site": body,
        "local": str(dest / "out.zip"),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="You Decide os-cycle: pull drop / put zip. Not Yes.")
    sub = p.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("pull", help="copy a live ticket into inbox/tickets/<id>/")
    p1.add_argument("id")
    p2 = sub.add_parser("put-zip", help="place out.zip on the same ticket (download ≠ Yes)")
    p2.add_argument("id")
    p2.add_argument("zip")
    args = p.parse_args(argv)
    if args.cmd == "pull":
        print(json.dumps(pull(args.id), indent=2))
        return 0
    print(json.dumps(put_zip(args.id, args.zip), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
