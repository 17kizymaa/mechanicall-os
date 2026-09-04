#!/usr/bin/env python3
"""Stdio MCP projection of aether. Stdlib only.

Tools: current, probe, propose_write.
Never approve / reject / next. Opening this module is not Yes.
Bind-root is one folder (--root / AETHER_MCP_ROOT).
propose_write lands under <root>/.aether/proposals/ only — never CURRENT.md.

Not EdubaWare. Not default-on. Human opts the client in.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROTOCOL = "2024-11-05"
SERVER_NAME = "aether-mcp"
SERVER_VERSION = "0.1.0"
FORBIDDEN = frozenset(
    {
        "approve",
        "reject",
        "next",
        "yes",
        "not_yet",
        "not-yet",
        "aether_approve",
        "aether_reject",
        "aether_next",
        "deinit",
    }
)
SAFE_NAME = re.compile(r"^[\w.-]{1,80}$")
PROPOSAL_DIR = Path(".aether") / "proposals"


class McpError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")


def resolve_root(raw: str | Path | None) -> Path:
    text = os.environ.get("AETHER_MCP_ROOT", "") if raw is None else str(raw)
    if not text.strip():
        text = os.getcwd()
    root = Path(text).expanduser().resolve()
    if not root.is_dir():
        raise McpError(-32602, f"bind-root is not a directory: {root}")
    return root


def find_aether(root: Path) -> Path:
    env = os.environ.get("AETHER_HOME", "").strip()
    candidates = [
        root / "aether",
        Path(env) / "aether" if env else None,
        Path(env) / "bin" / "aether" if env else None,
    ]
    which = os.environ.get("PATH", "")
    for part in which.split(os.pathsep):
        if part:
            candidates.append(Path(part) / "aether")
    for cand in candidates:
        if cand is None:
            continue
        if cand.is_file() and os.access(cand, os.X_OK):
            return cand
    raise McpError(-32603, "aether CLI not found (set AETHER_HOME or pass --root with ./aether)")


def run_aether(root: Path, args: list[str], timeout: int = 30) -> tuple[int, str]:
    bin_path = find_aether(root)
    env = os.environ.copy()
    home = bin_path.parent
    if home.name == "bin":
        home = home.parent
    env["AETHER_HOME"] = str(home)
    try:
        proc = subprocess.run(
            [str(bin_path), *args, str(root)],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except FileNotFoundError as exc:
        raise McpError(-32603, f"cannot exec aether: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise McpError(-32603, f"aether timed out: {exc}") from exc
    text = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    return proc.returncode, text.strip()


def tool_defs() -> list[dict]:
    return [
        {
            "name": "current",
            "description": (
                "Read live CURRENT.md via aether current (inspect only). "
                "Not Yes. Does not approve."
            ),
            "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "name": "probe",
            "description": (
                "Dry would-preflight for an action-id (aether probe). "
                "Does not write events. Does not approve."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Action id to probe against the bind-root CURRENT Next pin.",
                    }
                },
                "required": ["action"],
                "additionalProperties": False,
            },
        },
        {
            "name": "propose_write",
            "description": (
                "Write a proposal file under .aether/proposals/ only. "
                "Never writes CURRENT.md. Human applies. Not Yes."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Markdown proposal body."},
                    "name": {
                        "type": "string",
                        "description": (
                            "Basename only, e.g. CURRENT-proposal-20260828.md. "
                            "Default: CURRENT-proposal-<utc>.md"
                        ),
                    },
                },
                "required": ["text"],
                "additionalProperties": False,
            },
        },
    ]


def _text_result(text: str, is_error: bool = False) -> dict:
    return {
        "content": [{"type": "text", "text": text}],
        "isError": bool(is_error),
    }


def call_current(root: Path) -> dict:
    code, text = run_aether(root, ["current"])
    return _text_result(text or "(empty)", is_error=code != 0)


def call_probe(root: Path, action: str) -> dict:
    action = (action or "").strip()
    if not action:
        raise McpError(-32602, "probe requires action")
    if action.lower() in FORBIDDEN:
        return _text_result(
            f"refused: MCP cannot probe commitment verb {action!r}",
            is_error=True,
        )
    code, text = run_aether(root, ["probe", action])
    return _text_result(text or "(empty)", is_error=code not in (0, 3))


def call_propose_write(root: Path, text: str, name: str | None) -> dict:
    body = text if isinstance(text, str) else ""
    if not body.strip():
        raise McpError(-32602, "propose_write requires text")
    raw = (name or "").strip() or f"CURRENT-proposal-{_utc_stamp()}.md"
    if raw in {"CURRENT.md", "current.md"}:
        return _text_result("refused: cannot write CURRENT.md", is_error=True)
    if not SAFE_NAME.match(raw) or "/" in raw or "\\" in raw or ".." in raw:
        return _text_result("refused: name must be a basename like CURRENT-proposal-….md", is_error=True)
    dest_dir = (root / PROPOSAL_DIR).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = (dest_dir / raw).resolve()
    try:
        dest.relative_to(dest_dir)
    except ValueError:
        return _text_result("refused: path escapes .aether/proposals/", is_error=True)
    if dest.name == "CURRENT.md":
        return _text_result("refused: cannot write CURRENT.md", is_error=True)
    dest.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8")
    rel = dest.relative_to(root)
    return _text_result(f"wrote {rel}\nNot Yes. Human applies CURRENT.")


def dispatch_tool(root: Path, name: str, arguments: dict | None) -> dict:
    key = (name or "").strip()
    if key.lower() in FORBIDDEN:
        return _text_result(
            f"refused: MCP cannot {key} (inference is not authority)",
            is_error=True,
        )
    args = arguments if isinstance(arguments, dict) else {}
    if key == "current":
        return call_current(root)
    if key == "probe":
        return call_probe(root, str(args.get("action") or ""))
    if key == "propose_write":
        return call_propose_write(
            root,
            str(args.get("text") or ""),
            str(args.get("name") or "") or None,
        )
    return _text_result(f"refused: unknown tool {key!r}", is_error=True)


def handle_rpc(root: Path, message: dict) -> dict | None:
    """Return a JSON-RPC response, or None for notifications."""
    if not isinstance(message, dict):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "invalid request"}}
    method = message.get("method")
    req_id = message.get("id")
    params = message.get("params") if isinstance(message.get("params"), dict) else {}
    if req_id is None and method:
        return None
    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": PROTOCOL,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                    "instructions": (
                        "Aether projection: inspect CURRENT and write proposals only. "
                        "Never approve. Silence is not permission."
                    ),
                },
            }
        if method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tool_defs()}}
        if method == "tools/call":
            name = str(params.get("name") or "")
            arguments = params.get("arguments") if isinstance(params.get("arguments"), dict) else {}
            result = dispatch_tool(root, name, arguments)
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"method not found: {method}"},
        }
    except McpError as exc:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": exc.code, "message": exc.message},
        }


def _read_content_length_message(buf: bytes) -> tuple[dict | None, bytes]:
    header_end = buf.find(b"\r\n\r\n")
    if header_end < 0:
        return None, buf
    header = buf[:header_end].decode("utf-8", errors="replace")
    length = None
    for line in header.split("\r\n"):
        if line.lower().startswith("content-length:"):
            try:
                length = int(line.split(":", 1)[1].strip())
            except ValueError:
                length = None
    if length is None:
        return None, buf[header_end + 4 :]
    start = header_end + 4
    if len(buf) < start + length:
        return None, buf
    blob = buf[start : start + length]
    rest = buf[start + length :]
    try:
        msg = json.loads(blob.decode("utf-8"))
    except json.JSONDecodeError:
        return None, rest
    if isinstance(msg, dict):
        return msg, rest
    return None, rest


def serve_stdio(root: Path) -> int:
    buf = b""
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer
    while True:
        chunk = stdin.read(1)
        if not chunk:
            break
        buf += chunk
        while True:
            msg = None
            if b"\r\n\r\n" in buf:
                msg, buf = _read_content_length_message(buf)
                if msg is None and b"\r\n\r\n" not in buf:
                    break
                if msg is None:
                    continue
            elif b"\n" in buf and not buf.lstrip().startswith(b"Content-Length"):
                line, _, rest = buf.partition(b"\n")
                buf = rest
                line = line.strip()
                if not line:
                    continue
                try:
                    parsed = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    continue
                msg = parsed if isinstance(parsed, dict) else None
            else:
                break
            if msg is None:
                continue
            reply = handle_rpc(root, msg)
            if reply is None:
                continue
            payload = json.dumps(reply, ensure_ascii=False).encode("utf-8")
            frame = f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii") + payload
            stdout.write(frame)
            stdout.flush()
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--root",
        default=None,
        help="Bind-root folder (one CURRENT). Default: AETHER_MCP_ROOT or cwd.",
    )
    args = ap.parse_args(argv)
    try:
        root = resolve_root(args.root)
    except McpError as exc:
        print(exc.message, file=sys.stderr)
        return 2
    return serve_stdio(root)


if __name__ == "__main__":
    raise SystemExit(main())
