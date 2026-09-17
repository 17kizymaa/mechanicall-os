#!/usr/bin/env python3
"""Lab-only project drop. Bind 127.0.0.1. Not Yes. Not Play Store. Not mesh.

Emulators reach this via 10.0.2.2:8765. One offer slot. Bytes land in
mechanicall-os/inbox (sitters/ + drop/). Accept still lives on the phone
and still skips live CURRENT.md.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
MAX = 8 * 1024 * 1024


def store_dir() -> Path:
    from aether_inbox import inbox_root

    return inbox_root() / "drop"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_drop_progress(direction: str, got: int, total: int) -> None:
    dest = store_dir()
    dest.mkdir(parents=True, exist_ok=True)
    pct = 0 if total <= 0 else min(100, int(100 * got / total))
    (dest / "progress.json").write_text(
        json.dumps(
            {
                "direction": direction,
                "percent": pct,
                "got": got,
                "total": total,
                "updated": _now(),
                "not_yes": True,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def land_sitter_copy(blob: bytes, from_id: str, files: int) -> None:
    """Unpack the offer into inbox/sitters/<id>/. Copy only. Not operator CURRENT."""
    from aether_inbox import _notice, _slug, _unzip_to, inbox_root
    from aether_pocket import PocketError

    try:
        slug = _slug(from_id)
    except PocketError:
        slug = "pocket"
    dest = inbox_root() / "sitters" / slug
    tmp = dest.with_name(dest.name + ".part")
    if tmp.exists():
        shutil.rmtree(tmp)
    try:
        n = _unzip_to(blob, tmp)
        _notice(
            tmp,
            direction="sitter-to-operator",
            sitter=slug,
            files=n or files,
            note="Lab drop into mechanicall-os/inbox. Not operator CURRENT.",
        )
        if dest.exists():
            shutil.rmtree(dest)
        tmp.rename(dest)
    except Exception:
        if tmp.exists():
            shutil.rmtree(tmp)
        raise


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
            self._json(
                200,
                {
                    "ok": True,
                    "service": "mechanicall-drop",
                    "store": str(store_dir()),
                    "not_yes": True,
                },
            )
            return
        if path == "/progress.json":
            prog = store_dir() / "progress.json"
            if not prog.is_file():
                self._json(200, {"ok": True, "percent": 0, "direction": "", "not_yes": True})
                return
            try:
                data = json.loads(prog.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._json(200, {"ok": True, "percent": 0, "direction": "", "not_yes": True})
                return
            if isinstance(data, dict):
                data["ok"] = True
                data["not_yes"] = True
                self._json(200, data)
                return
            self._json(200, {"ok": True, "percent": 0, "direction": "", "not_yes": True})
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
        dest = store_dir()
        dest.mkdir(parents=True, exist_ok=True)
        part = dest / "offer.zip.part"
        got = 0
        write_drop_progress("up", 0, length)
        with part.open("wb") as out:
            while got < length:
                chunk = self.rfile.read(min(65536, length - got))
                if not chunk:
                    break
                out.write(chunk)
                got += len(chunk)
                write_drop_progress("up", got, length)
        if got != length:
            part.unlink(missing_ok=True)
            self._json(400, {"ok": False, "error": "refused: short body"})
            return
        blob = part.read_bytes()
        part.replace(dest / "offer.zip")
        meta = {
            "id": _now().replace(":", "").replace("-", ""),
            "from": (qs.get("from") or ["pocket"])[0],
            "name": (qs.get("name") or ["folder"])[0],
            "files": int((qs.get("files") or ["0"])[0] or "0"),
            "kind": "folder",
            "offered": _now(),
            "status": "offered",
            "note": "Landed in mechanicall-os/inbox. Not Yes.",
            "not_yes": True,
        }
        (dest / "offer.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        try:
            land_sitter_copy(blob, str(meta["from"]), int(meta["files"]))
        except Exception as exc:
            meta["note"] = f"Drop stored. Sitter copy refused ({exc}). Not Yes."
        write_drop_progress("up", length, length)
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
