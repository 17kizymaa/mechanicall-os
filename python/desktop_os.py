#!/usr/bin/env python3
"""Mechanicall desktop: two apps on one local glass.

Trader = paper book (watchlist, last, ticket, P&L).
Serve = servant (Mum). this-works stays parked.

Bind 127.0.0.1. Not Yes. Not live money. Not IBKR-named.
Never writes CURRENT.md.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PY = Path(__file__).resolve().parent
if str(PY) not in sys.path:
    sys.path.insert(0, str(PY))

from paper_book import (  # noqa: E402
    DISCLAIMER,
    add_symbol,
    cancel,
    flatten,
    load,
    place,
    save,
    snapshot,
    tick,
)

STATIC = ROOT / "desktop" / "static"
HOST = "127.0.0.1"
PORT = int(os.environ.get("MECHANICALL_DESKTOP_PORT") or 8766)


def _var() -> Path:
    return Path(os.environ.get("MECHANICALL_DESKTOP_VAR") or (ROOT / "desktop" / "var"))


def _book_path() -> Path:
    return _var() / "paper-book.json"


def _serve_path() -> Path:
    return _var() / "serve.json"

APPS = (
    {
        "id": "trader",
        "title": "Trader",
        "room": "happy-birthday",
        "note": "Paper trader. Simulated last. They need not stamp.",
    },
    {
        "id": "serve",
        "title": "Serve",
        "room": "hi-its-mother",
        "note": "Servant. Chat is hello. Send is not Yes.",
    },
)

_lock = threading.Lock()
_book = None
_serve = None


def _hello_serve() -> dict:
    return {
        "not_yes": True,
        "messages": [
            {
                "from": "me",
                "text": "I'm here. What do you need?",
                "at": "",
            }
        ],
    }


def _ensure() -> None:
    global _book, _serve
    if _book is None:
        _book = load(_book_path())
    if _serve is None:
        _serve = _load_serve()


def _load_serve() -> dict:
    path = _serve_path()
    if not path.is_file():
        return _hello_serve()
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return _hello_serve()
    if isinstance(obj, dict) and isinstance(obj.get("messages"), list):
        obj["not_yes"] = True
        return obj
    return _hello_serve()


def _save_serve(data: dict) -> None:
    path = _serve_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def reset_paths() -> None:
    """Tests only: drop in-memory book so env VAR is reread."""
    global _book, _serve
    _book = None
    _serve = None


def _state() -> dict:
    with _lock:
        _ensure()
        save(_book_path(), _book)
        return {
            "ok": True,
            "not_yes": True,
            "not_live": True,
            "not_ibkr": True,
            "disclaimer": DISCLAIMER,
            "apps": list(APPS),
            "book": snapshot(_book),
            "serve": _serve,
        }


def _json_body(handler: BaseHTTPRequestHandler) -> dict:
    n = int(handler.headers.get("Content-Length") or 0)
    if n <= 0 or n > 1_000_000:
        return {}
    raw = handler.rfile.read(n)
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
    return obj if isinstance(obj, dict) else {}


class DeskHandler(BaseHTTPRequestHandler):
    server_version = "MechanicallDesktop/0.1"

    def log_message(self, fmt: str, *args) -> None:
        line = fmt % args
        if "/api/state" in line:
            return
        sys.stderr.write("desk " + line + "\n")

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj: dict) -> None:
        blob = json.dumps(obj).encode("utf-8")
        self._send(code, blob, "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            html = (STATIC / "index.html").read_bytes()
            self._send(200, html, "text/html; charset=utf-8")
            return
        if path.startswith("/static/"):
            name = Path(path).name
            fp = STATIC / name
            if not fp.is_file() or fp.resolve().parent != STATIC.resolve():
                self._json(404, {"ok": False, "error": "missing"})
                return
            ctype = {
                ".css": "text/css; charset=utf-8",
                ".js": "text/javascript; charset=utf-8",
                ".html": "text/html; charset=utf-8",
                ".svg": "image/svg+xml",
            }.get(fp.suffix, "application/octet-stream")
            self._send(200, fp.read_bytes(), ctype)
            return
        if path == "/api/state":
            self._json(200, _state())
            return
        self._json(404, {"ok": False, "error": "missing"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        body = _json_body(self)
        try:
            if path == "/api/tick":
                with _lock:
                    _ensure()
                    tick(_book)
                    save(_book_path(), _book)
                self._json(200, _state())
                return
            if path == "/api/order":
                with _lock:
                    _ensure()
                    place(
                        _book,
                        symbol=str(body.get("symbol") or ""),
                        side=str(body.get("side") or ""),
                        qty=float(body.get("qty") or 0),
                        order_type=str(body.get("type") or "MARKET"),
                        limit=(
                            float(body["limit"])
                            if body.get("limit") not in (None, "")
                            else None
                        ),
                    )
                    save(_book_path(), _book)
                self._json(200, _state())
                return
            if path == "/api/cancel":
                with _lock:
                    _ensure()
                    cancel(_book, str(body.get("id") or ""))
                    save(_book_path(), _book)
                self._json(200, _state())
                return
            if path == "/api/flatten":
                with _lock:
                    _ensure()
                    flatten(_book, str(body.get("symbol") or ""))
                    save(_book_path(), _book)
                self._json(200, _state())
                return
            if path == "/api/watch":
                with _lock:
                    _ensure()
                    add_symbol(
                        _book,
                        str(body.get("symbol") or ""),
                        name=str(body.get("name") or ""),
                    )
                    save(_book_path(), _book)
                self._json(200, _state())
                return
            if path == "/api/serve":
                text = str(body.get("text") or "").strip()
                if not text:
                    raise ValueError("empty")
                if len(text) > 4000:
                    raise ValueError("too long")
                with _lock:
                    _ensure()
                    _serve.setdefault("messages", []).append(
                        {"from": "them", "text": text, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                    )
                    _serve["messages"].append(
                        {
                            "from": "me",
                            "text": "I'll take that. You don't need to stamp.",
                            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        }
                    )
                    _serve["messages"] = _serve["messages"][-80:]
                    _serve["not_yes"] = True
                    _save_serve(_serve)
                self._json(200, _state())
                return
        except (ValueError, TypeError, KeyError) as exc:
            self._json(400, {"ok": False, "error": str(exc), "not_yes": True})
            return
        self._json(404, {"ok": False, "error": "missing"})


def ticker(stop: threading.Event) -> None:
    while not stop.wait(0.45):
        with _lock:
            _ensure()
            tick(_book)
            save(_book_path(), _book)


def serve(port: int = PORT) -> ThreadingHTTPServer:
    STATIC.mkdir(parents=True, exist_ok=True)
    _var().mkdir(parents=True, exist_ok=True)
    with _lock:
        _ensure()
    httpd = ThreadingHTTPServer((HOST, port), DeskHandler)
    stop = threading.Event()
    threading.Thread(target=ticker, args=(stop,), daemon=True).start()
    httpd._desk_stop = stop  # type: ignore[attr-defined]
    return httpd


def origin(port: int = PORT) -> str:
    return f"http://{HOST}:{port}/"


def open_window(url: str) -> int:
    os.environ.setdefault("WEBKIT_DISABLE_DMABUF_RENDERER", "1")
    os.environ.setdefault("WEBKIT_DISABLE_COMPOSITING_MODE", "1")
    try:
        import gi

        gi.require_version("Gtk", "3.0")
        gi.require_version("WebKit2", "4.1")
        from gi.repository import Gtk, WebKit2
    except (ImportError, ValueError):
        webbrowser.open(url)
        return 0

    win = Gtk.Window(title="Mechanicall")
    win.set_default_size(1440, 900)
    win.connect("destroy", Gtk.main_quit)
    web = WebKit2.WebView()
    web.load_uri(url)
    win.add(web)
    win.show_all()
    Gtk.main()
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cmd", nargs="?", default="open", choices=("open", "serve", "url"))
    p.add_argument("--port", type=int, default=PORT)
    args = p.parse_args(argv)
    if args.cmd == "url":
        print(origin(args.port))
        return 0
    httpd = serve(args.port)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    url = origin(args.port)
    print(url, flush=True)
    if args.cmd == "serve":
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        httpd.shutdown()
        return 0
    try:
        return open_window(url)
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
