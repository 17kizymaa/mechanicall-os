#!/usr/bin/env python3
"""Tailnet-only Wake-on-LAN listener for wol-pi. Not Decide. No secrets in git.

Bind 127.0.0.1 by default. Set WOL_BIND to a tailnet IP to listen on the net.
MAC from WOL_MAC. Refuses 0.0.0.0.

  WOL_MAC=aa:bb:cc:dd:ee:ff WOL_BIND=127.0.0.1 python3 scripts/wol-wake-listen.py
"""
from __future__ import annotations

import os
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


def _mac() -> bytes:
    raw = os.environ.get("WOL_MAC", "").strip()
    if not raw:
        print("WOL_MAC is required (not in git)", file=sys.stderr)
        sys.exit(2)
    parts = raw.replace("-", ":").split(":")
    if len(parts) != 6:
        print("WOL_MAC must be six octets", file=sys.stderr)
        sys.exit(2)
    return bytes(int(p, 16) for p in parts)


def _bind() -> str:
    host = os.environ.get("WOL_BIND", "127.0.0.1").strip() or "127.0.0.1"
    if host in {"0.0.0.0", "::", "[::]"}:
        print("refused: public wake bind", file=sys.stderr)
        sys.exit(2)
    return host


def _magic(mac: bytes) -> bytes:
    return b"\xff" * 6 + mac * 16


class WakeHandler(BaseHTTPRequestHandler):
    mac = b""

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        sys.stderr.write("wake: " + (fmt % args) + "\n")

    def do_GET(self) -> None:  # noqa: N802
        self._wake()

    def do_POST(self) -> None:  # noqa: N802
        self._wake()

    def _wake(self) -> None:
        if self.path.rstrip("/") != "/wake":
            self.send_error(404)
            return
        pkt = _magic(self.mac)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(pkt, ("255.255.255.255", 9))
        finally:
            sock.close()
        body = b'{"ok":true,"note":"WAKE is not Yes."}\n'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    mac = _mac()
    host = _bind()
    port = int(os.environ.get("WOL_PORT", "7077"))
    WakeHandler.mac = mac
    httpd = HTTPServer((host, port), WakeHandler)
    print(f"wol-wake-listen {host}:{port} (not Yes)", file=sys.stderr)
    httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
