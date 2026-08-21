#!/usr/bin/env python3
"""Mum-class LAN face for the A33 pocket demo. Yes is a POST, never GET.

Binds a pocket *outside* mechanicall-os. Optional pull/push via env:
  POCKET_EDGE  POCKET_SERIAL  POCKET_PHONE_PATH
"""
from __future__ import annotations

import html
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from aether_pocket import (
    PocketError,
    agent_edit_propose,
    not_yet,
    projection,
    refuse_if_operator,
    write_propose,
    yes,
)

EDGE = os.environ.get("POCKET_EDGE", "anphuni@100.70.86.90")
SERIAL = os.environ.get("POCKET_SERIAL", "RZCW2038KHN")
PHONE = os.environ.get("POCKET_PHONE_PATH", "/sdcard/mechanicall-pocket")
OLLAMA = os.environ.get("POCKET_OLLAMA", "http://127.0.0.1:11434")
MODEL = os.environ.get("POCKET_MODEL", "personal-llm-sft-v4:latest")


def sync_wanted() -> bool:
    return os.environ.get("POCKET_SYNC", "").strip().lower() in ("1", "yes", "true")


def _ssh(cmd: str) -> None:
    subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", EDGE, cmd],
        check=True,
        capture_output=True,
        text=True,
    )


def pull_phone(twin: Path) -> str:
    twin.mkdir(parents=True, exist_ok=True)
    _ssh(
        f"adb -s {SERIAL} pull {PHONE}/CURRENT.md /tmp/a33-CURRENT.md; "
        f"adb -s {SERIAL} pull {PHONE}/PROPOSE-CURRENT.md /tmp/a33-PROPOSE.md"
    )
    subprocess.run(["scp", "-o", "BatchMode=yes", "-q", f"{EDGE}:/tmp/a33-CURRENT.md", str(twin / "CURRENT.md")], check=True)
    subprocess.run(["scp", "-o", "BatchMode=yes", "-q", f"{EDGE}:/tmp/a33-PROPOSE.md", str(twin / "PROPOSE-CURRENT.md")], check=True)
    return "pulled CURRENT + PROPOSE from A33"


def push_phone(twin: Path, *names: str) -> str:
    sent = []
    for name in names:
        src = twin / name
        if not src.exists():
            continue
        subprocess.run(["scp", "-o", "BatchMode=yes", "-q", str(src), f"{EDGE}:/tmp/a33-{name}"], check=True)
        _ssh(f"adb -s {SERIAL} push /tmp/a33-{name} {PHONE}/{name}")
        sent.append(name)
    aether = twin / ".aether"
    if aether.is_dir() and "CURRENT.md" in names:
        # events + decisions if yes/not-yet
        ev = aether / "events.jsonl"
        if ev.is_file():
            subprocess.run(["scp", "-o", "BatchMode=yes", "-q", str(ev), f"{EDGE}:/tmp/a33-events.jsonl"], check=True)
            _ssh(f"adb -s {SERIAL} shell mkdir -p {PHONE}/.aether")
            _ssh(f"adb -s {SERIAL} push /tmp/a33-events.jsonl {PHONE}/.aether/events.jsonl")
            sent.append(".aether/events.jsonl")
        dec = twin / "DECISIONS.md"
        if dec.is_file():
            subprocess.run(["scp", "-o", "BatchMode=yes", "-q", str(dec), f"{EDGE}:/tmp/a33-DECISIONS.md"], check=True)
            _ssh(f"adb -s {SERIAL} push /tmp/a33-DECISIONS.md {PHONE}/DECISIONS.md")
            sent.append("DECISIONS.md")
    return "pushed " + ", ".join(sent) if sent else "nothing to push"


def page(twin: Path, flash: str = "") -> bytes:
    refuse_if_operator(twin)
    try:
        proj = projection(twin)
        cf = twin / "CURRENT.md"
        cur = cf.read_text(encoding="utf-8") if cf.is_file() else proj["current"]
        propose = proj["propose"]
        fields = proj["fields"]
        receipt = proj.get("receipt") or "(no receipt yet)"
        nxt = fields.get("Next", "(unset)")
    except PocketError as exc:
        cur, propose, receipt, nxt = str(exc), "", "(none)", "?"
    flash_h = f"<p class='flash'>{html.escape(flash)}</p>" if flash else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>You have not said yes yet</title>
<style>
 body {{ font-family: system-ui, sans-serif; margin: 12px; background:#111; color:#eee; }}
 pre, textarea {{ width:100%; background:#1b1b1b; color:#ddd; border:1px solid #333; padding:8px; box-sizing:border-box; }}
 textarea {{ min-height: 220px; font-family: ui-monospace, monospace; font-size: 14px; }}
 .yes {{ background:#2e7d32; color:#fff; font-size:1.2rem; padding:12px 20px; border:0; }}
 .no {{ background:#555; color:#fff; padding:12px 16px; border:0; }}
 .flash {{ background:#333; padding:8px; }}
 h1 {{ font-size:1.3rem; }}
 .muted {{ color:#888; font-size:.85rem; }}
</style></head><body>
<h1>You have not said yes yet</h1>
<p>Opening this page is not a yes. Only <strong>Yes</strong> is.</p>
<p class="muted">Plan Next: <strong>{html.escape(nxt)}</strong> · demo sitting · not a store app</p>
{flash_h}
<h2>Plan</h2>
<pre>{html.escape(cur)}</pre>
<form method="post" action="/yes" onsubmit="return confirm('Apply the draft and record that you said yes?');">
  <button class="yes" type="submit">Yes</button>
</form>
<form method="post" action="/not-yet" style="margin-top:8px">
  <button class="no" type="submit">Not yet</button>
</form>
<h2>Draft</h2>
<form method="post" action="/save">
<textarea name="propose">{html.escape(propose)}</textarea>
<p><button type="submit">Save draft</button> <span class="muted">save does not change the plan</span></p>
</form>
<form method="post" action="/agent">
  <button type="submit">Agent edit draft</button>
  <span class="muted">draft only</span>
</form>
<h2>Receipt</h2>
<pre>{html.escape(receipt)}</pre>
<p class="muted">GET never Yes. Silence is never permission.</p>
</body></html>""".encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    twin: Path

    def log_message(self, fmt: str, *args) -> None:
        print("[pocket-face]", fmt % args)

    def _html(self, body: bytes, code: int = 200) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _redir(self, loc: str) -> None:
        self.send_response(303)
        self.send_header("Location", loc)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] not in ("/", "/index.html"):
            self.send_error(404)
            return
        flash = ""
        if "?" in self.path:
            q = parse_qs(self.path.split("?", 1)[1])
            flash = (q.get("m") or [""])[0]
        if sync_wanted():
            try:
                pull_phone(self.twin)
            except Exception as exc:
                flash = (flash + " | pull: " + str(exc)).strip(" |")
        self._html(page(self.twin, flash))

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        form = parse_qs(raw)
        path = self.path.split("?", 1)[0]
        msg = "ok"
        try:
            refuse_if_operator(self.twin)
            if path == "/yes":
                if sync_wanted():
                    pull_phone(self.twin)
                r = yes(self.twin, reason="yes from brake face")
                if sync_wanted():
                    push_phone(self.twin, "CURRENT.md", "DECISIONS.md", "PROPOSE-CURRENT.md", "RECEIPT.md")
                msg = r.text[:300]
            elif path == "/not-yet":
                if sync_wanted():
                    pull_phone(self.twin)
                r = not_yet(self.twin, reason="not yet from brake face")
                if sync_wanted():
                    push_phone(self.twin, "CURRENT.md", "DECISIONS.md", "RECEIPT.md")
                msg = r.text[:300]
            elif path == "/save":
                write_propose(self.twin, (form.get("propose") or [""])[0])
                if sync_wanted():
                    push_phone(self.twin, "PROPOSE-CURRENT.md")
                msg = "saved draft"
            elif path == "/agent":
                if sync_wanted():
                    pull_phone(self.twin)
                r = agent_edit_propose(self.twin, ollama_host=OLLAMA, model=MODEL)
                if sync_wanted():
                    push_phone(self.twin, "PROPOSE-CURRENT.md")
                msg = r.text
            else:
                self.send_error(404)
                return
        except (PocketError, subprocess.CalledProcessError, OSError) as exc:
            msg = f"ERROR: {exc}"
        from urllib.parse import quote
        self._redir("/?m=" + quote(msg[:200]))


def main() -> None:
    twin = refuse_if_operator(os.environ.get("POCKET_HOST_TWIN", str(Path.home() / "mechanicall-pocket")))
    host = os.environ.get("POCKET_FACE_HOST", "192.168.0.51")
    port = int(os.environ.get("POCKET_FACE_PORT", "8765"))
    Handler.twin = Path(twin)
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"pocket face http://{host}:{port}/  twin={twin}  GET is not Yes")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
