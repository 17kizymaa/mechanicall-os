#!/usr/bin/env python3
"""Lab-only project drop. Bind 127.0.0.1. Not Yes. Not Play Store. Not mesh.

Emulators reach this via 10.0.2.2:8765. One offer slot. Accept still lives
on the phone and still skips live CURRENT.md.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
MAX = 8 * 1024 * 1024


def store_dir() -> Path:
    env = os.environ.get("MECHANICALL_INBOX_ROOT")
    if env:
        return Path(env).expanduser().resolve() / "drop"
    return ROOT / ".inbox" / "drop"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class DropHandler(BaseHTTPRequestHandler):
    server_version = "MechanicallDrop/0.1"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        sys.stderr.write("[drop] " + (fmt % args) + "\n")

    def _send(self, code: int, body: bytes, ctype: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _json(self, code: int, payload: dict) -> None:
        blob = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
        self._send(code, blob)

    def _meta_path(self) -> Path:
        return store_dir() / "offer.json"

    def _zip_path(self) -> Path:
        return store_dir() / "offer.zip"

    def _read_meta(self) -> dict | None:
        path = self._meta_path()
        if not path.is_file() or not self._zip_path().is_file():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
        if not isinstance(data, dict):
            return None
        return data

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)
        if path in {"/", "/health"}:
            self._json(200, {"ok": True, "service": "mechanicall-drop", "not_yes": True})
            return
        meta = self._read_meta()
        if path == "/offer.json":
            if not meta:
                self._json(200, {"ok": True, "present": False, "not_yes": True})
                return
            skip = (qs.get("not") or [""])[0]
            if skip and skip == str(meta.get("from") or ""):
                self._json(200, {"ok": True, "present": False, "not_yes": True, "note": "own offer"})
                return
            self._json(200, {**meta, "ok": True, "present": True, "not_yes": True})
            return
        if path == "/offer.zip":
            if not meta:
                self.send_error(404, "no offer")
                return
            blob = self._zip_path().read_bytes()
            self._send(200, blob, "application/zip")
            return
        self.send_error(404, "not a drop path")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)
        if path != "/offer":
            self.send_error(404, "POST /offer")
            return
        length = int(self.headers.get("Content-Length") or "0")
        if length <= 0 or length > MAX:
            self._json(400, {"ok": False, "error": "refused: empty or too large"})
            return
        blob = self.rfile.read(length)
        dest = store_dir()
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "offer.zip").write_bytes(blob)
        meta = {
            "id": _now().replace(":", "").replace("-", ""),
            "from": (qs.get("from") or ["pocket"])[0],
            "name": (qs.get("name") or ["folder"])[0],
            "files": int((qs.get("files") or ["0"])[0] or "0"),
            "kind": "folder",
            "offered": _now(),
            "status": "offered",
            "note": "In the works.",
            "not_yes": True,
        }
        (dest / "offer.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        self._json(200, {**meta, "ok": True, "present": True})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mechanicall lab drop (127.0.0.1 only)")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    if args.bind in {"0.0.0.0", "::"}:
        print("refused: public bind", file=sys.stderr)
        return 3
    dest = store_dir()
    dest.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((args.bind, args.port), DropHandler)
    print(f"drop listening {args.bind}:{args.port} store={dest} (not Yes)", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("drop stop", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
