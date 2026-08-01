#!/usr/bin/env python3
"""aether shell — Domain-bound operator REPL (sacred CURRENT seat).

Unlike panel→Open Grok (launch-and-return):
  * CURRENT.md is re-read every turn and shown as a one-line status
  * System doctrine is Domain-first (propose-only, silence ≠ permission)
  * Default agent = peer (personal-llm); /agent grok for real tools
  * Slash commands for local truth without leaving the seat
  * Never runs aether approve; flags unsafe model suggestions

Desk product removed (unsacred soft-chat). Panel + shell remain.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from aether_fs import load_dotenv_files, project_root, read_current  # noqa: E402
from aether_llm import (  # noqa: E402
    apply_peer_backend,
    apply_preset,
    chat,
    cycle_preset,
    describe_backend,
    flag_unsafe_model_output,
    format_presets_help,
    grok_tui_available,
    load_preset_from_project,
    personal_llm_serve_hints,
    resolve_ollama_host,
    save_preset_to_project,
    write_project_ollama_host,
)
from aether_shell_agent import (  # noqa: E402
    agent_chat_loop,
    load_agent_profile,
    resolve_agent_role,
    set_agent_role,
)

MAX_HISTORY = 20
RUN_TIMEOUT_SEC = 30
RUN_OUTPUT_CAP = 12000

# Human-only local tools (basename). No shell=True; no pipes/redirs as shell syntax.
# Model output never auto-executes these — human types /run or !…
ALLOW_CMDS = frozenset(
    {
        "cat",
        "head",
        "tail",
        "grep",
        "rg",
        "ls",
        "pwd",
        "touch",
        "mkdir",
        "stat",
        "wc",
        "find",
        "echo",
        "date",
        "file",
        "diff",
        "which",
        "basename",
        "dirname",
        "realpath",
        "test",
        "true",
        "false",
        "printf",
        "tee",
        "sort",
        "uniq",
        "cut",
        "tr",
        "sed",  # still argv-only; no shell metachar eval
        "awk",
        "tree",
        "du",
        "df",
        "id",
        "uname",
        "env",  # read-only env dump; no assignment via shell
    }
)

# Explicitly never allow even if someone expands the set carelessly
DENY_CMDS = frozenset(
    {
        "rm",
        "rmdir",
        "mv",
        "cp",
        "chmod",
        "chown",
        "sudo",
        "su",
        "bash",
        "sh",
        "zsh",
        "dash",
        "python",
        "python3",
        "perl",
        "ruby",
        "node",
        "curl",
        "wget",
        "ssh",
        "scp",
        "cryptsetup",
        "dd",
        "mkfs",
        "mount",
        "umount",
        "kill",
        "pkill",
        "aether",  # use /preflight etc.; not free aether approve
    }
)

SHELL_SYSTEM = """You are the operator's Domain-bound assistant inside `aether shell`.

## Authority
- CURRENT.md is the live Domain (Objective, Next, Keep, Reject, Limits, Prohibited).
- You propose only. You never approve, never advance Next, never claim CURRENT changed.
- Silence is never permission. Empty human replies mean wait.
- Technique (you / Grok / any model) is not Domain.

## Behaviour
- Ground every consequential suggestion in the CURRENT fields provided this turn.
- Prefer small reversible steps that match the single Next when one is set.
- If asked to do something Prohibited or outside Next, refuse and point at CURRENT.
- Never emit a ready-to-run `aether approve` command.
- Never invent secrets, vault unlock, or finance/client facts.
- You cannot run shell tools yourself. Human runs allowlisted tools via `/run …` or `!…`
  (cat grep ls touch mkdir …). Suggest the exact /run line; do not claim you executed it.

## Style
Short, practical, anti-clown. Fact vs inference. Label proposals as proposals.
When drafting CURRENT text, wrap it as a proposal block the human can copy — do not claim applied.
"""


def _field(current: str, name: str) -> str:
    # **Next:** value
    pat = re.compile(
        rf"^\*\*{re.escape(name)}:\*\*\s*(.+)$",
        re.IGNORECASE | re.MULTILINE,
    )
    m = pat.search(current or "")
    return (m.group(1).strip() if m else "")


def prefer_grok_tui_for_shell() -> None:
    """Prefer Grok TUI compute (`grok login` session) over raw XAI API.

    Ranking for shell: grok_tui > (other providers via resolve_backend) > xai API.
    Override with AETHER_SHELL_PREFER_GROK_TUI=0, or force --provider.
    Legacy AETHER_SHELL_PREFER_XAI=1 no longer elevates raw API above TUI.
    """
    if os.environ.get("AETHER_SHELL_PROVIDER_LOCK", "").strip():
        return
    prefer = os.environ.get("AETHER_SHELL_PREFER_GROK_TUI", "1").strip().lower()
    # Legacy env: only disable TUI prefer when explicitly off
    legacy = os.environ.get("AETHER_SHELL_PREFER_XAI", "").strip().lower()
    if prefer in ("0", "false", "no", "off") or legacy in ("0", "false", "no", "off"):
        return
    if not grok_tui_available():
        return
    os.environ["AETHER_LLM_PROVIDER"] = "grok_tui"
    model = os.environ.get("AETHER_MODEL", "").strip()
    if not model or model.startswith("openrouter") or model.startswith("claude"):
        os.environ["AETHER_MODEL"] = "grok-4.5"


def prefer_xai_for_shell() -> None:
    """Deprecated alias — now prefers Grok TUI, not raw XAI API."""
    prefer_grok_tui_for_shell()

def status_line(root: Path) -> str:
    cur = read_current(root) or ""
    obj = _field(cur, "Objective")[:60] or "(no CURRENT)"
    nxt = _field(cur, "Next")[:40] or "unset"
    ph = _field(cur, "Phase")[:12] or "?"
    st = _field(cur, "Status")[:16] or "?"
    return f"[{root.name}] phase={ph} status={st} next={nxt} | {obj}"


def agent_mode_enabled() -> bool:
    """Grok-shaped agent DEFINITION + tool loop (default on). AETHER_SHELL_AGENT_MODE=0 to disable."""
    v = os.environ.get("AETHER_SHELL_AGENT_MODE", "1").strip().lower()
    return v not in ("0", "false", "no", "off")


def build_messages(root: Path, history: List[dict]) -> List[dict[str, str]]:
    """Legacy chat-only messages (no tool loop). Prefer agent_chat_loop when agent mode on."""
    cur = read_current(root) or "(no CURRENT.md — refuse consequential claims; suggest aether current init)"
    if len(cur) > 14000:
        cur = cur[:14000] + "\n…"
    if agent_mode_enabled():
        from aether_shell_agent import build_agent_system

        system = build_agent_system(root, cur)
    else:
        system = SHELL_SYSTEM + "\n\n## CURRENT.md (re-read this turn)\n" + cur
    msgs: List[dict[str, str]] = [{"role": "system", "content": system}]
    for m in history[-MAX_HISTORY:]:
        msgs.append({"role": m["role"], "content": m["content"]})
    return msgs


def run_preflight(root: Path, action: str) -> str:
    aether = os.environ.get("AETHER_HOME", str(Path(__file__).resolve().parent.parent))
    bin_path = Path(aether) / "aether"
    if not bin_path.is_file():
        bin_path = Path(shutil_which("aether") or "aether")
    try:
        r = subprocess.run(
            [str(bin_path), "preflight", action, str(root)],
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "AETHER_HOME": str(aether)},
        )
        out = (r.stdout or "") + (r.stderr or "")
        return f"exit={r.returncode}\n{out.strip()}"
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"preflight error: {e}"


def shutil_which(cmd: str) -> Optional[str]:
    from shutil import which

    return which(cmd)


def append_log(root: Path, role: str, text: str) -> None:
    try:
        d = root / ".aether"
        d.mkdir(parents=True, exist_ok=True)
        path = d / "shell.jsonl"
        rec = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "role": role,
            "text": text[:20000],
        }
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


HELP = """\
slash commands (local — no model):
  /help              this text
  /current           print CURRENT.md
  /status            one-line Domain status
  /next              Next id + Next allowed action blurb
  /events [n]        last n lines of .aether/events.jsonl (default 8)
  /decisions         DECISIONS.md if present
  /preflight <id>    run aether preflight <id> in this project
  /run <cmd> [args]  allowlisted local tool (cat grep ls touch mkdir …)
  ! <cmd> [args]     same as /run (leading !)
  /tools             list allowlisted commands
  /backend           show LLM backend (+ active preset)
  /provider [id|next|prev|list]
                     toggle compute: coding free → sonnet35 → ollama → …
  /model <id>        pin AETHER_MODEL (keep current provider)
  /preset-save       write .aether/llm-preset for this project
  /smoke             offline smoke of standard slash behaviours
  /agent [grok|peer] show / switch agent role
                     grok = real coding agent (full tools)
                     peer = personal-llm proposals/synthesis (read-only)
  /peer-serve        peer REPL on THIS host + LAN/Tailscale URLs
  /ollama-host [url] show / pin Ollama (local or remote Tailscale); saved in .aether/
  /clear             clear chat history (not CURRENT)
  /quit  /exit  bye  leave shell
empty line waits (never yes). models never approve.
default agent: peer (personal-llm-sft-v4). /agent grok for real tools.
remote: /ollama-host http://100.x.y.z:11434  then chat as peer.
human /run or ! — allowlisted tools without model.
"""


def _resolve_cmd_bin(name: str) -> Optional[str]:
    """Resolve basename to absolute path on PATH (no relative/absolute user bins)."""
    if not name or name in (".", "..") or "/" in name or "\\" in name:
        return None
    return shutil_which(name)


def run_allowlisted(root: Path, argv: List[str]) -> str:
    """Run allowlisted tool with cwd=project root. Never shell=True."""
    if not argv:
        return "usage: /run <cmd> [args…]   or   !<cmd> [args…]\ntry /tools"
    name = Path(argv[0]).name  # strip any path attempt
    if name in DENY_CMDS or name not in ALLOW_CMDS:
        return (
            f"refused: `{name}` not in allowlist (or denied).\n"
            f"allowed: {' '.join(sorted(ALLOW_CMDS))}\n"
            "no shell pipes; human /run only; model never auto-executes."
        )
    # Block shell metacharacters that would only make sense under shell=True
    for a in argv:
        if any(c in a for c in ("|", ";", "&", "`", "\n", "\r", "$(", "${")):
            return f"refused: metacharacters not allowed in argv ({a!r})"
    bin_path = _resolve_cmd_bin(name)
    if not bin_path:
        return f"refused: `{name}` not found on PATH"
    real_argv = [bin_path] + list(argv[1:])
    try:
        r = subprocess.run(
            real_argv,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_SEC,
            env={**os.environ, "AETHER_SHELL_RUN": "1"},
        )
    except subprocess.TimeoutExpired:
        return f"timeout after {RUN_TIMEOUT_SEC}s: {' '.join(argv)}"
    except OSError as e:
        return f"exec error: {e}"
    out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr else "")
    if len(out) > RUN_OUTPUT_CAP:
        out = out[:RUN_OUTPUT_CAP] + "\n…(truncated)"
    if not out.strip():
        out = "(no output)"
    return f"exit={r.returncode}  cwd={root}\n$ {' '.join(argv)}\n{out.rstrip()}"


def next_blurb(root: Path) -> str:
    """Show **Next:** and ## Next allowed action body (local)."""
    cur = read_current(root) or ""
    nxt = _field(cur, "Next") or "(unset)"
    lines = [f"**Next:** {nxt}", ""]
    # Extract ## Next allowed action … until next ##
    m = re.search(
        r"^##\s+Next allowed action\s*\n(.*?)(?=^##\s|\Z)",
        cur,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if m:
        body = m.group(1).strip()
        if body:
            lines.append(body)
        else:
            lines.append("(empty Next allowed action section)")
    else:
        lines.append("(no ## Next allowed action section)")
    return "\n".join(lines)


def tail_events(root: Path, n: int = 8) -> str:
    path = root / ".aether" / "events.jsonl"
    if not path.is_file():
        return "(no .aether/events.jsonl)"
    try:
        raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as e:
        return f"(events read error: {e})"
    if not raw:
        return "(events empty)"
    n = max(1, min(n, 50))
    chunk = raw[-n:]
    return f"(last {len(chunk)} of {len(raw)})\n" + "\n".join(chunk)


def read_decisions(root: Path) -> str:
    path = root / "DECISIONS.md"
    if not path.is_file():
        return "(no DECISIONS.md)"
    try:
        t = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return f"(decisions read error: {e})"
    if len(t) > 8000:
        t = t[:8000] + "\n…"
    return t


def smoke_standard_behaviours(root: Path) -> str:
    """Offline smoke: standard slash handlers + doctrine checks (no LLM)."""
    hist: List[dict] = []
    checks: List[str] = []

    def ok(name: str, cond: bool, detail: str = "") -> None:
        mark = "PASS" if cond else "FAIL"
        checks.append(f"  {mark}  {name}" + (f" — {detail}" if detail else ""))

    # Doctrine in system prompt
    ok("SHELL_SYSTEM propose-only", "propose only" in SHELL_SYSTEM.lower())
    ok("SHELL_SYSTEM silence", "silence" in SHELL_SYSTEM.lower())
    ok("SHELL_SYSTEM no approve exec", "never emit" in SHELL_SYSTEM.lower() or "approve" in SHELL_SYSTEM.lower())

    # Slash table
    for cmd, need in (
        ("/help", "slash commands"),
        ("/status", root.name),
        ("/current", ""),  # any string or no CURRENT
        ("/next", "Next"),
        ("/backend", ""),
        ("/provider list", ""),
        ("/model", "AETHER_MODEL"),
        ("/events", ""),
        ("/decisions", ""),
        ("/preflight", "usage"),
        ("/tools", "allowlisted"),
        ("/agent", "aether-shell"),
    ):
        out = handle_slash(root, cmd, hist)
        ok(f"slash {cmd}", out is not None and (need.lower() in (out or "").lower() if need else bool(out)))

    # allowlisted tools
    marker = root / ".aether-shell-smoke-touch"
    try:
        if marker.exists():
            marker.unlink()
    except OSError:
        pass
    run_out = handle_slash(root, f"/run touch {marker.name}", hist) or ""
    ok("run touch", "exit=0" in run_out and marker.is_file(), run_out.split("\n", 1)[0])
    cat_out = handle_slash(root, f"/run cat {marker.name}", hist) or ""
    ok("run cat", "exit=0" in cat_out)
    pwd_out = handle_slash(root, "/run pwd", hist) or ""
    ok("run pwd", "exit=0" in pwd_out and str(root) in pwd_out)
    deny = handle_slash(root, "/run rm -rf /", hist) or ""
    ok("run deny rm", "refused" in deny.lower())
    bang = handle_slash(root, f"! ls {marker.name}", hist) or ""
    ok("bang ls", "exit=0" in bang or marker.name in bang)
    try:
        if marker.exists():
            marker.unlink()
    except OSError:
        pass

    # clear + history
    hist.append({"role": "user", "content": "x"})
    out = handle_slash(root, "/clear", hist)
    ok("slash /clear", out is not None and "clear" in (out or "").lower() and len(hist) == 0)

    # quit signal
    ok("slash /quit → exit", handle_slash(root, "/quit", hist) is None)

    # unknown
    u = handle_slash(root, "/not-a-real-cmd", hist) or ""
    ok("unknown slash", "unknown" in u.lower())

    # build_messages injects CURRENT
    msgs = build_messages(root, [])
    ok("build_messages system", msgs and msgs[0]["role"] == "system" and "CURRENT" in msgs[0]["content"])

    # guard flags: line-anchored aether approve (see UNSAFE_CMD_RE)
    flags = flag_unsafe_model_output('aether approve "done"\n')
    ok("flag unsafe approve-ish", "unsafe_cmd_suggest" in flags, ",".join(flags) if flags else "none")

    failed = sum(1 for c in checks if c.strip().startswith("FAIL"))
    passed = sum(1 for c in checks if c.strip().startswith("PASS"))
    header = f"aether shell smoke  pass={passed} fail={failed}  root={root}"
    return header + "\n" + "\n".join(checks) + ("\n\nSMOKE OK" if failed == 0 else "\n\nSMOKE FAILED")


def handle_slash(root: Path, line: str, history: List[dict]) -> Optional[str]:
    """Return response string, or None to signal exit, or '' to continue without model."""
    line = (line or "").strip()
    # Bang form: !cmd … (also handled in repl; support here for /smoke + tests)
    if line.startswith("!") and not line.startswith("!="):
        body = line[1:].lstrip()
        if not body:
            return "usage: ! <cmd> [args…]   (same as /run)"
        try:
            argv = shlex.split(body)
        except ValueError as e:
            return f"parse error: {e}"
        return run_allowlisted(root, argv)

    parts = shlex.split(line)
    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in ("/quit", "/exit", "/q"):
        return None
    if cmd in ("/help", "/h", "/?"):
        return HELP
    if cmd == "/current":
        return read_current(root) or "(no CURRENT.md)"
    if cmd == "/status":
        return status_line(root)
    if cmd == "/next":
        return next_blurb(root)
    if cmd == "/events":
        n = 8
        if args:
            try:
                n = int(args[0])
            except ValueError:
                return "usage: /events [n]"
        return tail_events(root, n)
    if cmd in ("/decisions", "/decision"):
        return read_decisions(root)
    if cmd in ("/smoke", "/smoke-test"):
        return smoke_standard_behaviours(root)
    if cmd in ("/tools", "/allow", "/allowlist"):
        return "allowlisted (human /run or ! only):\n  " + " ".join(sorted(ALLOW_CMDS))
    if cmd in ("/peer-serve", "/pll-serve", "/personal-serve"):
        host = resolve_ollama_host(root)
        return personal_llm_serve_hints() + f"\n\nactive AETHER_OLLAMA_HOST={host}"
    if cmd in ("/ollama-host", "/pll-host", "/remote-ollama"):
        if not args:
            host = resolve_ollama_host(root)
            pin = root / ".aether" / "ollama-host"
            pin_s = pin.read_text(encoding="utf-8").strip() if pin.is_file() else "(none)"
            return (
                f"active: {host}\n"
                f"project pin (.aether/ollama-host): {pin_s}\n"
                f"env AETHER_OLLAMA_HOST={os.environ.get('AETHER_OLLAMA_HOST', '')!r}\n"
                f"usage: /ollama-host http://100.x.y.z:11434\n"
                f"       /ollama-host local   # → http://127.0.0.1:11434"
            )
        raw = args[0].strip()
        if raw.lower() in ("local", "loopback", "127", "localhost"):
            raw = "http://127.0.0.1:11434"
        path = write_project_ollama_host(root, raw)
        os.environ["AETHER_OLLAMA_HOST"] = resolve_ollama_host(root)
        msg = apply_peer_backend(root)
        return f"pinned {path}\n{msg}\n{describe_backend()}"
    if cmd in ("/agent", "/profile"):
        if args:
            try:
                role = set_agent_role(args[0])
            except ValueError as e:
                return str(e) + "\nusage: /agent grok | /agent peer"
            if role == "peer":
                msg = apply_peer_backend(root)
            else:
                prefer_grok_tui_for_shell()
                msg = "grok real agent (TUI compute preferred)"
        else:
            msg = ""
            if resolve_agent_role() == "peer":
                msg = apply_peer_backend(root)
        prof = load_agent_profile()
        role = resolve_agent_role()
        extra = ""
        if role == "peer":
            extra = "\n\n" + personal_llm_serve_hints()
        head = (msg + "\n") if msg else ""
        return (
            head
            + f"role: {role}  ({prof.role})  [default=peer]\n"
            f"agent: {prof.name}\n"
            f"path: {prof.path}\n"
            f"mode: {'ON' if agent_mode_enabled() else 'OFF'} (AETHER_SHELL_AGENT_MODE)\n"
            f"tools: {', '.join(prof.tools) or '(none)'}\n"
            f"disallowed: {', '.join(prof.disallowed)}\n"
            f"backend: {describe_backend()}\n"
            f"desc: {(prof.description or '')[:240]}\n"
            f"switch: /agent grok  |  /agent peer\n"
            f"remote: /ollama-host http://<tailscale-ip>:11434"
            + extra
        )
    if cmd in ("/run", "/exec", "/sh"):
        # /sh is alias but we still do NOT invoke a shell — argv allowlist only
        return run_allowlisted(root, args)
    if cmd == "/backend":
        return describe_backend()
    if cmd in ("/provider", "/providers", "/preset", "/presets"):
        if not args or args[0] in ("list", "ls", "?"):
            return format_presets_help() + "\n\nactive: " + describe_backend()
        sub = args[0].lower()
        if sub in ("next", "n", "+"):
            try:
                msg = cycle_preset(+1)
            except ValueError as e:
                return str(e)
            return msg + "\n" + describe_backend()
        if sub in ("prev", "previous", "p", "-"):
            try:
                msg = cycle_preset(-1)
            except ValueError as e:
                return str(e)
            return msg + "\n" + describe_backend()
        if sub in ("save", "persist"):
            path = save_preset_to_project(root)
            return f"saved preset to {path}\n{describe_backend()}"
        try:
            msg = apply_preset(sub, lock=True)
        except ValueError as e:
            return str(e) + "\n\n" + format_presets_help()
        return msg + "\n" + describe_backend()
    if cmd == "/model":
        if not args:
            return f"AETHER_MODEL={os.environ.get('AETHER_MODEL', '')!r}\n{describe_backend()}"
        os.environ["AETHER_MODEL"] = args[0]
        os.environ["AETHER_SHELL_PROVIDER_LOCK"] = "1"
        return f"model pinned → {args[0]}\n{describe_backend()}"
    if cmd in ("/preset-save", "/save-preset"):
        path = save_preset_to_project(root)
        return f"saved preset to {path}\n{describe_backend()}"
    if cmd == "/clear":
        history.clear()
        return "(history cleared)"
    if cmd == "/preflight":
        if not args:
            return "usage: /preflight <action-id>"
        return run_preflight(root, args[0])
    return f"unknown command {cmd} — try /help"


def repl(root: Path) -> int:
    load_dotenv_files()
    # Project llm-preset if any; default agent is **peer** (personal-llm + remote path)
    loaded = load_preset_from_project(root)
    role = resolve_agent_role()
    peer_line = ""
    if role == "peer":
        # Default shape: peer profile + ollama host probe (local → project pin → Tailscale)
        set_agent_role("peer")
        peer_line = apply_peer_backend(root)
    elif not loaded:
        prefer_grok_tui_for_shell()

    print("aether shell — Domain-bound · default agent=peer (personal-llm)")
    print(status_line(root))
    if peer_line:
        print(peer_line)
    print(f"backend: {describe_backend()}")
    if loaded:
        print(f"loaded: {loaded}")
    if agent_mode_enabled():
        role = resolve_agent_role()
        prof = load_agent_profile()
        print(
            f"agent: {role} · {prof.name} · tools={','.join(prof.tools) or 'none'}  "
            f"(/agent grok|peer · /ollama-host)"
        )
    else:
        print("agent: OFF (chat-only)")
    print("type /help · /run · /peer-serve · empty line waits · bye to leave")
    print()

    history: List[dict] = []
    while True:
        try:
            line = input("shell> ").rstrip("\n")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\n(interrupt — type bye to leave)")
            continue

        if not line.strip():
            print("(waiting — silence is not permission)")
            continue

        if line.strip().lower() in ("bye", "quit", "exit", "q"):
            break

        raw = line.strip()
        # Human tool run: !cmd …  (not sent to model)
        if raw.startswith("!") and not raw.startswith("!="):
            body = raw[1:].lstrip()
            if not body:
                print("usage: ! <cmd> [args…]   (same as /run)")
                print()
                continue
            try:
                argv = shlex.split(body)
            except ValueError as e:
                print(f"parse error: {e}")
                print()
                continue
            print(run_allowlisted(root, argv))
            print()
            continue

        if raw.startswith("/"):
            out = handle_slash(root, raw, history)
            if out is None:
                break
            print(out)
            print()
            continue

        history.append({"role": "user", "content": line})
        append_log(root, "user", line)
        try:
            cur = read_current(root) or ""
            if agent_mode_enabled():
                # Grok-shaped multi-turn tool loop (profile + AGENTS + CURRENT)
                reply = agent_chat_loop(
                    root,
                    history[-MAX_HISTORY:],
                    chat_fn=chat,
                    current=cur,
                    temperature=0.35,
                )
            else:
                msgs = build_messages(root, history)
                reply = chat(msgs, temperature=0.45)
        except Exception as e:
            print(f"(llm error: {e})")
            history.pop()
            continue

        flags = flag_unsafe_model_output(reply or "")
        if flags:
            reply = (reply or "") + "\n\n[shell guard: " + ", ".join(flags) + "]"

        history.append({"role": "assistant", "content": reply or ""})
        append_log(root, "assistant", reply or "")
        print()
        print(reply or "(empty)")
        print()
        # refresh status strip so Next changes mid-session are visible
        print(status_line(root))

    print("bye.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="aether shell")
    p.add_argument("path", nargs="?", default=".", help="project root (default: cwd)")
    p.add_argument(
        "--provider",
        default="",
        help="force provider or preset (coding|free|sonnet35|ollama|grok_tui|xai|…)",
    )
    p.add_argument("--model", default="", help="force AETHER_MODEL")
    p.add_argument(
        "--preset",
        default="",
        help="alias for --provider preset id (coding, sonnet35, ollama, …)",
    )
    p.add_argument(
        "--smoke",
        action="store_true",
        help="offline smoke of standard slash behaviours then exit (no LLM)",
    )
    args = p.parse_args(argv)
    choice = (args.preset or args.provider or "").strip()
    if choice:
        try:
            # Prefer named presets; fall back to raw provider name
            from aether_llm import LLM_PRESETS, PRESET_ALIASES, normalize_preset_name

            n = normalize_preset_name(choice)
            if n in LLM_PRESETS or choice.lower() in PRESET_ALIASES:
                apply_preset(choice, lock=True)
            else:
                os.environ["AETHER_LLM_PROVIDER"] = choice
                os.environ["AETHER_SHELL_PROVIDER_LOCK"] = "1"
        except ValueError:
            os.environ["AETHER_LLM_PROVIDER"] = choice
            os.environ["AETHER_SHELL_PROVIDER_LOCK"] = "1"
    if args.model:
        os.environ["AETHER_MODEL"] = args.model
    root = project_root(args.path)
    if args.smoke:
        report = smoke_standard_behaviours(root)
        print(report)
        return 0 if "SMOKE OK" in report else 1
    return repl(root)


if __name__ == "__main__":
    raise SystemExit(main())
