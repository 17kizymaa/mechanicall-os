#!/usr/bin/env python3
"""Local desk bridge: propose-only chat + CURRENT.md rail.

Chat + authority surface only. No Kodi/remote actions.
Default bind 127.0.0.1. Use --lan for phone / TV on home LAN.

Endpoints:
  GET  /           desk HTML (chat left, CURRENT right)
  GET  /health     backend name only
  GET  /privacy    privacy + banner text
  GET  /current    CURRENT.md if present
  POST /chat       {message, history?} → {ok, reply, flags, history, backend}
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aether_desk import (  # noqa: E402
    PRIVACY,
    BANNER,
    desk_turn,
    load_dotenv_files,
    project_root,
    read_current,
)
from aether_llm import describe_backend  # noqa: E402

DEFAULT_PORT = 8788
# Bump when localStorage schema or first-run popup copy changes
UI_STORE_VERSION = "2"


def _html_page() -> str:
    privacy_js = json.dumps(PRIVACY)
    banner_js = json.dumps(BANNER.strip())
    store_ver = json.dumps(UI_STORE_VERSION)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0a0614">
<title>Desk · CURRENT</title>
<style>
/* Maximalist look, cheap paint: gradients + borders, no blur animation loops */
:root {{
  --void: #07040f;
  --ink: #f4eefc;
  --muted: #a894c4;
  --gold: #e8c56a;
  --gold2: #f0a85c;
  --rose: #e07ab5;
  --violet: #7b5cff;
  --cyan: #5ce1e6;
  --panel: rgba(22,12,40,.88);
  --line: rgba(232,197,106,.35);
  --ok: #7dffa2;
  --err: #ff8f9f;
  --font-display: "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  --font-body: system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "Cascadia Code", "SF Mono", Menlo, monospace;
}}
* {{ box-sizing: border-box; }}
html, body {{ height: 100%; }}
body {{
  margin: 0;
  color: var(--ink);
  font-family: var(--font-body);
  background:
    radial-gradient(ellipse 90% 60% at 10% -10%, rgba(123,92,255,.45), transparent 55%),
    radial-gradient(ellipse 70% 50% at 100% 0%, rgba(224,122,181,.28), transparent 50%),
    radial-gradient(ellipse 50% 40% at 80% 100%, rgba(92,225,230,.12), transparent 45%),
    linear-gradient(165deg, #12081f 0%, var(--void) 45%, #0d0618 100%);
  background-attachment: fixed;
  min-height: 100dvh;
}}
/* static ornate frame — no animated particles (device-safe) */
.shell {{
  max-width: 1180px;
  margin: 0 auto;
  min-height: 100dvh;
  padding: .75rem;
  display: flex;
  flex-direction: column;
  gap: .65rem;
}}
.topbar {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: .85rem 1.15rem;
  border: 1px solid var(--line);
  border-radius: 18px;
  background:
    linear-gradient(135deg, rgba(232,197,106,.12), transparent 40%),
    var(--panel);
  box-shadow: 0 0 0 1px rgba(255,255,255,.04) inset, 0 12px 40px rgba(0,0,0,.35);
}}
.brand {{
  font-family: var(--font-display);
  font-size: 1.55rem;
  letter-spacing: .04em;
  margin: 0;
  background: linear-gradient(100deg, var(--gold), var(--rose) 55%, var(--cyan));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: none;
}}
.brand small {{
  display: block;
  font-family: var(--font-body);
  font-size: .72rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: .15rem;
  background: none;
  -webkit-background-clip: unset;
  background-clip: unset;
}}
.pill {{
  font-size: .7rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  padding: .4rem .75rem;
  border-radius: 999px;
  border: 1px solid rgba(92,225,230,.35);
  color: var(--cyan);
  white-space: nowrap;
}}
.workspace {{
  flex: 1 1 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(260px, .85fr);
  gap: .65rem;
  min-height: 0;
}}
@media (max-width: 820px) {{
  .workspace {{ grid-template-columns: 1fr; }}
  .rail {{ order: -1; max-height: 38vh; }}
}}
.panel {{
  border: 1px solid var(--line);
  border-radius: 18px;
  background: var(--panel);
  box-shadow: 0 0 0 1px rgba(255,255,255,.03) inset, 0 16px 48px rgba(0,0,0,.4);
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}}
.panel-head {{
  flex: 0 0 auto;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: .5rem;
  padding: .75rem 1rem;
  border-bottom: 1px solid rgba(232,197,106,.2);
  background: linear-gradient(90deg, rgba(123,92,255,.15), transparent 60%);
}}
.panel-head h2 {{
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: .03em;
}}
.panel-head .hint {{
  font-size: .68rem;
  color: var(--muted);
  letter-spacing: .06em;
  text-transform: uppercase;
}}
#privacy {{
  display: none;
}}
#log {{
  flex: 1 1 auto;
  overflow: auto;
  padding: 1rem 1.1rem;
  -webkit-overflow-scrolling: touch;
  min-height: 12rem;
}}
.msg {{
  margin: 0 0 1rem;
  line-height: 1.5;
  word-wrap: break-word;
  animation: rise .25s ease-out;
}}
@keyframes rise {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to {{ opacity: 1; transform: none; }}
}}
.msg .who {{
  font-size: .65rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  display: block;
  margin-bottom: .25rem;
  color: var(--muted);
}}
.msg.you .bubble {{
  background: linear-gradient(135deg, rgba(123,92,255,.35), rgba(224,122,181,.2));
  border: 1px solid rgba(123,92,255,.4);
  border-radius: 4px 16px 16px 16px;
  padding: .7rem .9rem;
  color: #f0e8ff;
}}
.msg.desk .bubble {{
  background: linear-gradient(145deg, rgba(232,197,106,.12), rgba(22,12,40,.6));
  border: 1px solid rgba(232,197,106,.3);
  border-radius: 16px 4px 16px 16px;
  padding: .7rem .9rem;
  color: var(--ink);
}}
.composer {{
  flex: 0 0 auto;
  padding: .75rem;
  border-top: 1px solid rgba(232,197,106,.2);
  background: linear-gradient(0deg, rgba(7,4,15,.9), rgba(22,12,40,.5));
}}
form {{ display: flex; gap: .5rem; align-items: stretch; }}
input[type=text] {{
  flex: 1 1 auto;
  min-height: 3rem;
  font-size: 16px;
  border-radius: 14px;
  border: 1px solid rgba(232,197,106,.35);
  padding: .75rem 1rem;
  background: rgba(10,6,20,.85);
  color: var(--ink);
  -webkit-appearance: none;
  outline: none;
}}
input[type=text]:focus {{
  border-color: var(--cyan);
  box-shadow: 0 0 0 2px rgba(92,225,230,.2);
}}
button.send {{
  appearance: none;
  border: 0;
  border-radius: 14px;
  min-height: 3rem;
  padding: .75rem 1.2rem;
  font-size: .95rem;
  font-weight: 600;
  letter-spacing: .04em;
  cursor: pointer;
  color: #1a0f05;
  background: linear-gradient(135deg, var(--gold), var(--gold2) 50%, var(--rose));
  box-shadow: 0 4px 20px rgba(232,197,106,.25);
  -webkit-tap-highlight-color: transparent;
}}
button.send:disabled {{ opacity: .5; cursor: wait; }}
button.send:active {{ transform: scale(.98); }}
#status {{
  font-size: .75rem;
  color: var(--muted);
  margin: .45rem .15rem 0;
  min-height: 1.1rem;
}}
#status.ok {{ color: var(--ok); }}
#status.err {{ color: var(--err); }}
/* CURRENT rail (right) */
.rail .panel-head {{
  background: linear-gradient(90deg, rgba(232,197,106,.18), transparent 70%);
}}
#current-body {{
  flex: 1 1 auto;
  overflow: auto;
  padding: .85rem 1rem 1.1rem;
  font-family: var(--font-mono);
  font-size: .78rem;
  line-height: 1.45;
  white-space: pre-wrap;
  word-break: break-word;
  color: #e8dff5;
  -webkit-overflow-scrolling: touch;
}}
#current-body .empty {{
  font-family: var(--font-body);
  color: var(--muted);
  font-style: italic;
}}
.rail-meta {{
  flex: 0 0 auto;
  padding: .45rem 1rem .65rem;
  font-size: .65rem;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--muted);
  border-top: 1px solid rgba(232,197,106,.15);
}}
.rail.syncing {{
  box-shadow: 0 0 0 1px rgba(92,225,230,.45) inset, 0 16px 48px rgba(0,0,0,.4);
}}
.rail-meta.poll {{
  color: var(--cyan);
}}
/* First-run / history protection popup */
.modal-root {{
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(5,2,12,.72);
}}
.modal-root[hidden] {{ display: none !important; }}
.modal {{
  width: min(28rem, 100%);
  border-radius: 20px;
  border: 1px solid var(--line);
  background:
    linear-gradient(160deg, rgba(232,197,106,.15), transparent 40%),
    linear-gradient(200deg, rgba(123,92,255,.2), #140a24 55%);
  box-shadow: 0 24px 80px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06) inset;
  padding: 1.35rem 1.4rem 1.2rem;
  color: var(--ink);
}}
.modal h3 {{
  margin: 0 0 .65rem;
  font-family: var(--font-display);
  font-size: 1.35rem;
  background: linear-gradient(100deg, var(--gold), var(--cyan));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}}
.modal p {{
  margin: 0 0 .75rem;
  font-size: .92rem;
  line-height: 1.5;
  color: #e6dcf5;
}}
.modal .fine {{
  font-size: .78rem;
  color: var(--muted);
  margin-bottom: 1.1rem;
}}
.modal button {{
  appearance: none;
  border: 0;
  width: 100%;
  min-height: 2.85rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: .95rem;
  cursor: pointer;
  color: #1a0f05;
  background: linear-gradient(135deg, var(--gold), var(--rose));
}}
.modal button:active {{ transform: scale(.99); }}
</style>
</head><body>
<div class="shell">
  <header class="topbar">
    <h1 class="brand">Desk<small>Propose only · authority on the right</small></h1>
    <span class="pill" id="backend-pill">connecting…</span>
  </header>
  <div class="workspace">
    <section class="panel chat" aria-label="Chat">
      <div class="panel-head">
        <h2>Conversation</h2>
        <span class="hint">local history</span>
      </div>
      <div id="log" aria-live="polite"></div>
      <div class="composer">
        <form id="f" autocomplete="off">
          <input id="msg" type="text" placeholder="Ask anything grounded in CURRENT…" enterkeyhint="send" autocapitalize="sentences" />
          <button type="submit" class="send" id="send">Send</button>
        </form>
        <p id="status">ready</p>
      </div>
    </section>
    <aside class="panel rail" aria-label="CURRENT.md authority">
      <div class="panel-head">
        <h2>CURRENT.md</h2>
        <span class="hint">product · authority</span>
      </div>
      <div id="current-body"><span class="empty">Loading authority…</span></div>
      <div class="rail-meta" id="current-meta">filesystem truth · polls on your input</div>
    </aside>
  </div>
</div>

<div class="modal-root" id="hist-modal" hidden role="dialog" aria-modal="true" aria-labelledby="hist-title">
  <div class="modal">
    <h3 id="hist-title">Your chat stays on this device</h3>
    <p>
      Conversation history is stored <strong>locally in this browser</strong>
      (on the phone or TV you are using). It is not uploaded as a cloud archive
      and is not written into the project’s authority file.
    </p>
    <p class="fine">
      CURRENT.md on the right remains the human-owned control surface.
      The model only proposes. Silence is never permission.
      Cloud replies may still leave this device when you send a message — that is the chat path, not your history vault.
    </p>
    <button type="button" id="hist-ok">Got it — continue</button>
  </div>
</div>

<script>
(function () {{
  var STORE_VER = {store_ver};
  var KEY_HIST = "aether_desk_hist_v" + STORE_VER;
  var KEY_POPUP = "aether_desk_hist_popup_v" + STORE_VER;
  var history = [];
  var log = document.getElementById("log");
  var status = document.getElementById("status");
  var sendBtn = document.getElementById("send");
  var input = document.getElementById("msg");
  var currentBody = document.getElementById("current-body");
  var currentMeta = document.getElementById("current-meta");
  var backendPill = document.getElementById("backend-pill");
  var modal = document.getElementById("hist-modal");

  function loadHistory() {{
    try {{
      var raw = localStorage.getItem(KEY_HIST);
      if (!raw) return [];
      var arr = JSON.parse(raw);
      if (!Array.isArray(arr)) return [];
      return arr.filter(function (m) {{
        return m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string";
      }}).slice(-40);
    }} catch (e) {{ return []; }}
  }}
  function saveHistory() {{
    try {{
      localStorage.setItem(KEY_HIST, JSON.stringify(history.slice(-40)));
    }} catch (e) {{ /* quota / private mode */ }}
  }}
  function add(role, text, skipSave) {{
    var d = document.createElement("div");
    d.className = "msg " + (role === "user" ? "you" : "desk");
    var who = document.createElement("span");
    who.className = "who";
    who.textContent = role === "user" ? "you" : "desk";
    var bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;
    d.appendChild(who);
    d.appendChild(bubble);
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    if (!skipSave) {{ /* display only */ }}
  }}
  function renderHistory() {{
    log.innerHTML = "";
    history.forEach(function (m) {{
      add(m.role, m.content, true);
    }});
  }}

  history = loadHistory();
  renderHistory();

  // Closeable first-run popup for this store version
  try {{
    if (localStorage.getItem(KEY_POPUP) !== "1") {{
      modal.hidden = false;
    }}
  }} catch (e) {{
    modal.hidden = false;
  }}
  document.getElementById("hist-ok").onclick = function () {{
    try {{ localStorage.setItem(KEY_POPUP, "1"); }} catch (e) {{}}
    modal.hidden = true;
    try {{ input.focus(); }} catch (e) {{}}
  }};

  function xhrJson(method, url, body, timeoutMs) {{
    return new Promise(function (resolve, reject) {{
      var xhr = new XMLHttpRequest();
      xhr.open(method, url, true);
      xhr.timeout = timeoutMs || 30000;
      if (body) xhr.setRequestHeader("Content-Type", "application/json");
      xhr.onload = function () {{
        var t = xhr.responseText || "";
        try {{ resolve({{ status: xhr.status, data: JSON.parse(t) }}); }}
        catch (e) {{ resolve({{ status: xhr.status, data: null, raw: t }}); }}
      }};
      xhr.onerror = function () {{ reject(new Error("network")); }};
      xhr.ontimeout = function () {{ reject(new Error("timeout")); }};
      xhr.send(body || null);
    }});
  }}

  var rail = document.querySelector(".rail");
  var currentPollTimer = null;
  var lastCurrentText = "";

  /** Re-fetch CURRENT.md (product surface). Awaitable so chat waits for fresh authority. */
  function refreshCurrent(reason) {{
    reason = reason || "poll";
    return new Promise(function (resolve) {{
      if (rail) rail.classList.add("syncing");
      currentMeta.className = "rail-meta poll";
      currentMeta.textContent = "CURRENT · syncing (" + reason + ")…";
      var x = new XMLHttpRequest();
      x.open("GET", "/current?ts=" + Date.now(), true);
      x.timeout = 12000;
      x.onload = function () {{
        var t = (x.responseText || "").trim();
        if (!t || t === "(no CURRENT.md)") {{
          currentBody.innerHTML = '<span class="empty">No CURRENT.md in project root.</span>';
          lastCurrentText = "";
        }} else {{
          if (t !== lastCurrentText) {{
            currentBody.textContent = t;
            lastCurrentText = t;
          }}
        }}
        currentMeta.className = "rail-meta";
        currentMeta.textContent = "product · " + reason + " · " + new Date().toLocaleTimeString();
        if (rail) rail.classList.remove("syncing");
        resolve(t);
      }};
      x.onerror = function () {{
        currentMeta.className = "rail-meta";
        currentMeta.textContent = "could not refresh CURRENT (network)";
        if (rail) rail.classList.remove("syncing");
        resolve(lastCurrentText);
      }};
      x.ontimeout = function () {{
        currentMeta.className = "rail-meta";
        currentMeta.textContent = "CURRENT poll timed out";
        if (rail) rail.classList.remove("syncing");
        resolve(lastCurrentText);
      }};
      x.send();
    }});
  }}

  function scheduleCurrentPoll(reason) {{
    if (currentPollTimer) clearTimeout(currentPollTimer);
    currentPollTimer = setTimeout(function () {{
      refreshCurrent(reason || "input");
    }}, 280);
  }}

  // CURRENT-as-product: re-poll whenever the human types or focuses the chat
  input.addEventListener("input", function () {{ scheduleCurrentPoll("input"); }});
  input.addEventListener("focus", function () {{ scheduleCurrentPoll("focus"); }});
  input.addEventListener("keydown", function (ev) {{
    if (ev.key === "Enter") scheduleCurrentPoll("send");
  }});

  refreshCurrent("load");
  // slow background tick only — input/send is the primary poll
  setInterval(function () {{ refreshCurrent("tick"); }}, 45000);

  document.getElementById("f").onsubmit = async function (e) {{
    e.preventDefault();
    var message = (input.value || "").trim();
    if (!message) {{
      status.textContent = "empty line waits — silence is not yes";
      status.className = "";
      return;
    }}
    input.value = "";
    // Revisit CURRENT.md-as-product before any proposal path
    status.textContent = "reading CURRENT…";
    status.className = "";
    sendBtn.disabled = true;
    await refreshCurrent("before-send");
    history.push({{ role: "user", content: message }});
    saveHistory();
    add("user", message, true);
    status.textContent = "thinking… (CURRENT as foundation)";
    try {{
      var res = await xhrJson("POST", "/chat", JSON.stringify({{
        message: message,
        history: history.slice(0, -1)
      }}), 120000);
      var data = res.data || {{}};
      if (!data.ok) {{
        history.pop();
        saveHistory();
        status.textContent = data.error === "empty" ? "empty line waits"
          : data.error === "no_backend" ? "Chat needs a connection key on the house computer."
          : data.error === "llm" ? "Model busy or failed — try again."
          : ("Something went wrong (" + (data.error || res.status) + ").");
        status.className = "err";
        return;
      }}
      if (data.history && data.history.length) {{
        history = data.history;
      }} else if (data.reply) {{
        history.push({{ role: "assistant", content: data.reply }});
      }}
      saveHistory();
      add("assistant", data.reply || "", true);
      status.textContent = data.backend ? ("ok · " + data.backend) : "ok";
      status.className = "ok";
      backendPill.textContent = data.backend || "ready";
    }} catch (err) {{
      history.pop();
      saveHistory();
      var msg = (err && err.message) || "";
      status.textContent = msg === "timeout"
        ? "Timed out waiting for reply. Try again."
        : "Desk needs the house computer / network.";
      status.className = "err";
    }} finally {{
      sendBtn.disabled = false;
      try {{ input.focus(); }} catch (e) {{}}
    }}
  }};

  // health
  xhrJson("GET", "/health", null, 8000).then(function (res) {{
    var h = res.data || {{}};
    backendPill.textContent = h.backend || "ready";
    status.textContent = h.backend ? ("ready · " + h.backend) : "ready";
  }}).catch(function () {{
    backendPill.textContent = "offline";
    status.textContent = "offline";
    status.className = "err";
  }});
}})();
</script>
</body></html>
"""


class DeskState:
    def __init__(self, root: Path, *, public_url: str = ""):
        self.root = project_root(root)
        self.public_url = public_url or f"http://127.0.0.1:{DEFAULT_PORT}/"


STATE: Optional[DeskState] = None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, code: int, body: str | bytes, ctype: str = "text/plain; charset=utf-8") -> None:
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code: int, obj: dict) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False), "application/json; charset=utf-8")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self) -> None:
        assert STATE is not None
        u = urlparse(self.path)
        try:
            if u.path in ("/", "/index.html", "/desk"):
                return self._send(200, _html_page(), "text/html; charset=utf-8")
            if u.path == "/health":
                load_dotenv_files()
                return self._json(
                    200,
                    {
                        "ok": True,
                        "backend": describe_backend(),
                        "root": str(STATE.root),
                        "public_url": STATE.public_url,
                        "mode": "chat-only",
                        "ui": "maximalist-current-rail",
                        "store": UI_STORE_VERSION,
                    },
                )
            if u.path == "/privacy":
                return self._send(200, PRIVACY + "\n\n" + BANNER)
            if u.path == "/current":
                text = read_current(STATE.root) or ""
                return self._send(200, text if text else "(no CURRENT.md)")
            if u.path == "/favicon.ico":
                return self._send(204, b"", "image/x-icon")
            return self._send(404, "not found")
        except Exception as e:
            return self._send(500, f"error: {e}")

    def do_POST(self) -> None:
        assert STATE is not None
        u = urlparse(self.path)
        if u.path != "/chat":
            return self._send(404, "not found")
        sys.stderr.write(
            "%s - POST /chat begin thread=%s\n"
            % (self.address_string(), threading.current_thread().name)
        )
        sys.stderr.flush()
        try:
            n = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            n = 0
        raw = self.rfile.read(n) if n > 0 else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return self._json(400, {"ok": False, "error": "bad_json", "reply": ""})

        message = body.get("message") or body.get("text") or ""
        history = body.get("history") or []
        if not isinstance(history, list):
            history = []
        clean = []
        for m in history:
            if not isinstance(m, dict):
                continue
            role = m.get("role")
            content = m.get("content")
            if role in ("user", "assistant") and isinstance(content, str):
                clean.append({"role": role, "content": content})

        root = STATE.root
        if body.get("root"):
            root = project_root(str(body["root"]))

        preview = str(message).strip().replace("\n", " ")[:80]
        sys.stderr.write("%s - POST /chat msg=%r\n" % (self.address_string(), preview))
        sys.stderr.flush()

        result = desk_turn(root, str(message), clean, log=True)
        code = 200 if result.get("ok") else (400 if result.get("error") == "empty" else 503)
        out = {
            "ok": bool(result.get("ok")),
            "error": result.get("error") or "",
            "reply": result.get("reply") or "",
            "flags": result.get("flags") or [],
            "history": result.get("history") or clean,
            "backend": result.get("backend") or "",
        }
        sys.stderr.write(
            "%s - POST /chat done ok=%s err=%s\n"
            % (self.address_string(), out["ok"], out["error"] or "-")
        )
        sys.stderr.flush()
        return self._json(code, out)


def main(argv: Optional[list[str]] = None) -> int:
    load_dotenv_files()
    ap = argparse.ArgumentParser(description="Aether desk bridge — chat + CURRENT rail")
    ap.add_argument("path", nargs="?", default=".", help="project root with CURRENT.md")
    ap.add_argument("--port", type=int, default=int(os.environ.get("AETHER_DESK_PORT", DEFAULT_PORT)))
    ap.add_argument("--bind", default=None, help="bind address (default 127.0.0.1)")
    ap.add_argument("--lan", action="store_true", help="bind 0.0.0.0 for phone / TV")
    ap.add_argument(
        "--public-url",
        default=os.environ.get("AETHER_DESK_PUBLIC_URL", ""),
        help="public URL printed for clients",
    )
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args(argv)

    if args.debug:
        os.environ["AETHER_DESK_DEBUG"] = "1"

    root = project_root(args.path)
    bind = args.bind or ("0.0.0.0" if args.lan else "127.0.0.1")
    public = args.public_url.strip()
    if not public:
        host = "127.0.0.1" if bind == "127.0.0.1" else os.environ.get(
            "AETHER_DESK_HOST", "192.168.1.241"
        )
        public = f"http://{host}:{args.port}/"

    global STATE
    STATE = DeskState(root, public_url=public)

    httpd = ThreadingHTTPServer((bind, args.port), Handler)
    print(
        f"Desk: http://127.0.0.1:{args.port}/  root={root}  bind={bind}  backend={describe_backend()}",
        flush=True,
    )
    print(f"Public URL: {public}  UI=maximalist-current-rail store={UI_STORE_VERSION}", flush=True)
    if bind == "0.0.0.0":
        print("LAN bind — phone/TV: open Public URL. Keys stay on this machine.", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDesk stopped.", flush=True)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
