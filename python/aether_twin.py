#!/usr/bin/env python3
"""Operator read-twin: GET the bound pocket. Not Yes. Not Decide.

Watches CURRENT / PROPOSE / receipts / events / gate / tailnet.
Never writes. Never approve. Bind is not mechanicall-os.
Default listen 127.0.0.1:7078 — not 0.0.0.0.
"""
from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from aether_pocket import PocketError, refuse_if_operator

HOST_DEFAULT = "127.0.0.1"
PORT_DEFAULT = 7078
FILES = (
    ("/current", "CURRENT.md"),
    ("/propose", "PROPOSE-CURRENT.md"),
    ("/receipt", "RECEIPT.md"),
    ("/events", ".aether/events.jsonl"),
    ("/gate", ".aether/gate.json"),
    ("/tailnet", ".aether/tailnet.json"),
)


def _root() -> Path:
    raw = os.environ.get("TWIN_POCKET", "").strip()
    if not raw:
        raise PocketError("TWIN_POCKET is required (their folder, not mechanicall-os)")
    return refuse_if_operator(raw)


def _read(rel: str) -> tuple[int, bytes, str]:
    root = _root()
    path = root / rel
    if not path.is_file():
        return 404, b"(missing)\n", "text/plain; charset=utf-8"
    data = path.read_bytes()
    ctype = "application/json" if rel.endswith(".json") or rel.endswith(".jsonl") else "text/plain; charset=utf-8"
    return 200, data, ctype


def _index() -> bytes:
    lines = [
        "mechanicall read-twin",
        "GET is not Yes. Twin does not write CURRENT.",
        "",
        "  GET /current  CURRENT.md",
        "  GET /propose  PROPOSE-CURRENT.md",
        "  GET /receipt  RECEIPT.md",
        "  GET /events   .aether/events.jsonl",
        "  GET /gate     .aether/gate.json",
        "  GET /tailnet  fingerprint/status only",
        "",
    ]
    return ("\n".join(lines)).encode("utf-8")


class TwinHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        return

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Mechanicall-Twin", "read-only")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path.rstrip("/") or "/"
        try:
            if path in {"/", ""}:
                self._send(200, _index(), "text/plain; charset=utf-8")
                return
            for route, rel in FILES:
                if path == route:
                    code, body, ctype = _read(rel)
                    if rel.endswith("tailnet.json") and code == 200:
                        try:
                            obj = json.loads(body.decode("utf-8"))
                            obj.pop("authkey", None)
                            obj.pop("secret", None)
                            body = (json.dumps(obj, indent=2) + "\n").encode("utf-8")
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            pass
                    self._send(code, body, ctype)
                    return
            self._send(404, b"not a twin route\n", "text/plain; charset=utf-8")
        except PocketError as exc:
            self._send(403, (str(exc) + "\n").encode("utf-8"), "text/plain; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802
        self._send(405, b"refused: twin is GET-only. POST is not Yes.\n", "text/plain; charset=utf-8")

    def do_PUT(self) -> None:  # noqa: N802
        self.do_POST()

    def do_DELETE(self) -> None:  # noqa: N802
        self.do_POST()


def bind_host(host: str) -> str:
    h = (host or HOST_DEFAULT).strip() or HOST_DEFAULT
    if h in {"0.0.0.0", "::", "[::]"}:
        raise PocketError("refused: twin will not bind a public address")
    return h


def serve(host: str = HOST_DEFAULT, port: int = PORT_DEFAULT) -> None:
    bind_host(host)
    _root()
    httpd = ThreadingHTTPServer((host, int(port)), TwinHandler)
    print(f"twin GET http://{host}:{port}/  pocket={os.environ.get('TWIN_POCKET')}  GET is not Yes")
    httpd.serve_forever()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default=os.environ.get("TWIN_HOST", HOST_DEFAULT))
    ap.add_argument("--port", type=int, default=int(os.environ.get("TWIN_PORT", str(PORT_DEFAULT))))
    args = ap.parse_args(argv)
    try:
        serve(args.host, args.port)
    except PocketError as exc:
        print(f"refused: {exc}", flush=True)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
