#!/usr/bin/env python3
"""Allowlisted aether client for the Client room. Stdlib-only (Chaquopy).

Never approve / reject / next / deinit. Opening this module is not Yes.
Prefer the real ``aether`` CLI via aether_pocket; else read-only file fallbacks.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from aether_pocket import (
    AUTHORITY_FIELDS,
    PocketError,
    PocketResult,
    brief,
    current,
    current_validate,
    drift,
    events_tail,
    find_aether_bin,
    parse_fields,
    refuse_if_operator,
    run_aether,
)

CLIENT_ALLOW = (
    "current",
    "brief",
    "validate",
    "events",
    "drift",
    "verbs",
    "help",
    "status",
)

CLIENT_DENY = (
    "approve",
    "reject",
    "next",
    "deinit",
    "init",
    "onboard",
    "preflight",
    "demo",
    "try",
    "panel",
    "shell",
    "app",
    "distill",
    "watch",
    "repair",
    "poke",
    "trust",
    "event",
    "artifact",
    "seed",
    "spark",
    "session",
    "graph",
    "garden",
    "rival",
    "yes",
    "not_yet",
    "not-yet",
)

_VALIDATE_FIELDS = tuple(n for n in AUTHORITY_FIELDS if n != "Baseline")
_ALLOW_SET = frozenset(CLIENT_ALLOW)
_DENY_SET = frozenset(CLIENT_DENY)


def _payload(ok: bool, verb: str, text: str) -> dict:
    return {"ok": bool(ok), "verb": verb, "text": text or ""}


def _refused(verb: str) -> dict:
    return _payload(False, verb, f"refused: client cannot {verb}")


def _from_cli(verb: str, result: PocketResult) -> dict:
    return _payload(result.ok, verb, result.text)


def _norm_verb(verb) -> str:
    if verb is None:
        return ""
    return " ".join(str(verb).strip().lower().split())


def client_run(pocket: str | Path, verb: str) -> dict:
    """Run one allowlisted read verb. Always returns {ok, verb, text}.

    Operator tree is refused. Approve / reject / next are never dispatched.
    """
    key = _norm_verb(verb)
    try:
        refuse_if_operator(pocket)
    except PocketError as exc:
        return _payload(False, key or str(verb or ""), str(exc))
    if not key or key not in _ALLOW_SET or key in _DENY_SET:
        return _refused(key or str(verb or "(empty)"))
    if find_aether_bin() is not None:
        try:
            return _cli(pocket, key)
        except PocketError:
            return _fallback(pocket, key)
    return _fallback(pocket, key)


def _cli(pocket: str | Path, verb: str) -> dict:
    if verb == "current":
        return _from_cli(verb, current(pocket))
    if verb == "brief":
        return _from_cli(verb, brief(pocket))
    if verb == "validate":
        return _from_cli(verb, current_validate(pocket))
    if verb == "events":
        return _from_cli(verb, events_tail(pocket))
    if verb == "drift":
        return _from_cli(verb, drift(pocket))
    if verb == "verbs":
        result = run_aether(["verbs"], pocket)
        text = result.text.strip() if result.ok and result.text.strip() else " ".join(CLIENT_ALLOW)
        return _payload(True, verb, text)
    if verb == "help":
        return _from_cli(verb, run_aether(["help"], pocket))
    if verb == "status":
        result = run_aether(["status"], pocket)
        if result.ok or (result.text and "unknown command" not in result.text.lower()):
            return _from_cli(verb, result)
        return _from_cli(verb, brief(pocket))
    return _refused(verb)


def _fallback(pocket: str | Path, verb: str) -> dict:
    """Read-only file projection. Never writes. Never approve / reject / next."""
    root = refuse_if_operator(pocket)
    current_path = root / "CURRENT.md"
    if verb == "current":
        if not current_path.is_file():
            return _payload(False, verb, "CURRENT.md: MISSING (no authority file)")
        return _payload(True, verb, current_path.read_text(encoding="utf-8"))
    if verb == "brief":
        return _payload(True, verb, _fallback_brief(root, current_path))
    if verb == "validate":
        return _fallback_validate(root, current_path)
    if verb == "events":
        return _from_cli(verb, events_tail(root))
    if verb == "drift":
        return _payload(True, verb, _fallback_drift(root))
    if verb == "verbs":
        return _payload(True, verb, " ".join(CLIENT_ALLOW))
    if verb == "help":
        return _payload(
            True,
            verb,
            "aether client (read-only)\n"
            "  " + ", ".join(CLIENT_ALLOW) + "\n"
            "never: approve, reject, next, deinit",
        )
    if verb == "status":
        return _payload(True, verb, _fallback_brief(root, current_path))
    return _refused(verb)


def _fallback_brief(root: Path, current_path: Path) -> str:
    if not current_path.is_file():
        return f"=== aether brief ===\nroot: {root}\nCURRENT: MISSING\n==================="
    fields = parse_fields(current_path.read_text(encoding="utf-8"))
    nxt = fields.get("Next") or "(unset)"
    phase = fields.get("Phase") or "(unset)"
    status = fields.get("Status") or "(unset)"
    approval = fields.get("Approval") or "(unset)"
    objective = fields.get("Objective") or "(unset)"
    return (
        "=== aether brief ===\n"
        f"root: {root}\n"
        f"Next: {nxt}\n"
        f"Objective: {objective}\n"
        f"Phase/Status/Approval: {phase} / {status} / {approval}\n"
        "note: client fallback; aether CLI not found; human is the gate\n"
        "==================="
    )


def _fallback_validate(root: Path, current_path: Path) -> dict:
    if not current_path.is_file():
        return _payload(
            False,
            "validate",
            f"VALIDATE FAIL: CURRENT.md missing at {current_path}",
        )
    text = current_path.read_text(encoding="utf-8")
    fields = parse_fields(text)
    fails: list[str] = []
    first = text.splitlines()[0].strip() if text.splitlines() else ""
    if not re.match(r"^#\s*CURRENT\b", first):
        fails.append('FAIL: missing title line "# CURRENT"')
    for name in _VALIDATE_FIELDS:
        if not (fields.get(name) or "").strip():
            fails.append(f"FAIL: missing or empty **{name}:**")
    if fails:
        body = "\n".join(fails) + f"\n\nVALIDATE: FAIL ({current_path})"
        return _payload(False, "validate", body)
    nxt = fields.get("Next") or "unset"
    return _payload(
        True,
        "validate",
        f"VALIDATE: OK\n  root: {root}\n  Next: {nxt}",
    )


def _fallback_drift(root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "drift: n/a (aether CLI not found)"
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        if "not a git" in err.lower() or proc.returncode == 128:
            return f"drift: not a git work tree ({root})"
        return "drift: n/a (aether CLI not found)"
    lines = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
    if not lines:
        return "drift: clean"
    return "\n".join(f"DRIFT: {ln[3:] if len(ln) > 3 else ln} edited outside protocol" for ln in lines)
