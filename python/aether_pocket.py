#!/usr/bin/env python3
"""Pocket Domain bridge for the mobile-planning-demo APK (demo only).

Law: bind a folder *outside* the mechanicall-os operator tree.
Apply-PROPOSE then native pocket approve is Yes (stock phone; no POSIX
``bin/aether`` required). Desktop ``aether`` CLI remains for current/validate.

This module is stdlib-only so Chaquopy can import it.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

FIELD_RE = re.compile(
    r"^\*\*(?P<name>[^*]+):?\*\*\s*:?\s*(?P<value>.*)$",
    re.MULTILINE,
)
AUTHORITY_FIELDS = (
    "Objective",
    "Phase",
    "Status",
    "Baseline",
    "Next",
    "Approval",
)
OPERATOR_MARKERS = ("PRODUCT.md", "bin/aether", "CORE_PRINCIPLES.md", "AGENTS.md")
PROPOSE_NAME = "PROPOSE-CURRENT.md"
RECEIPT_NAME = "RECEIPT.md"
CHAT_NAME = "DRAFT-CHAT.jsonl"
WALK_STAGES = ("bind", "plan", "chat", "decide", "receipt")
CHAT_FILES = 24
DEFAULT_DESK_HOSTS = (
    "http://myarch:11434",
    "http://127.0.0.1:11434",
    "http://192.168.0.51:11434",
    "http://100.90.85.68:11434",
)
HUNK_MAX_CHARS = 2048
HUNK_SELECT_REL = Path(".aether") / "hunk-select.json"
TAILNET_REL = Path(".aether") / "tailnet.json"
QUEUE_REL = Path(".aether") / "desk-queue.json"
WAKE_DEFAULT = "http://wol-pi:7077/wake"
JOIN_STATUSES = ("not-on-net", "invited", "connected")
DESK_TRY_TIMEOUT = 8
DESK_STREAM_TIMEOUT = 45
LOAD_TIMEOUT = 60
GATE_STEPS = 16
GATE_REL = ".aether/gate.json"
GATE_STATES = frozenset({"idle", "warm", "gate", "quiet", "load", "queued"})
BUSY_GATE = frozenset({"load", "warm", "gate"})
SHORTCUT_FILES = (
    ("CURRENT.md", "current"),
    (PROPOSE_NAME, "propose"),
    (RECEIPT_NAME, "receipt"),
    ("DECISIONS.md", "decisions"),
    (".aether/events.jsonl", "events"),
)


class PocketError(Exception):
    """Bind or protocol error (never silent)."""


@dataclass
class PocketResult:
    ok: bool
    code: int
    text: str
    extra: dict = field(default_factory=dict)


def _resolve(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def _blank_pocket(pocket: str | Path | None) -> bool:
    """No folder named yet. One project at a time — empty is unbound."""
    if pocket is None:
        return True
    return str(pocket).strip() == ""


def is_operator_tree(path: str | Path) -> bool:
    if _blank_pocket(path):
        return False
    root = _resolve(path)
    return all((root / name).exists() for name in OPERATOR_MARKERS)


def refuse_if_operator(path: str | Path) -> Path:
    if _blank_pocket(path):
        raise PocketError("refused: name one folder first")
    root = _resolve(path)
    if is_operator_tree(root):
        raise PocketError(
            f"refused: {root} is the mechanicall-os operator tree — "
            "bind a client pocket folder outside this repo"
        )
    return root


def find_aether_bin(explicit: str | Path | None = None) -> Path | None:
    if explicit:
        p = Path(explicit)
        if p.is_file() and os.access(p, os.X_OK):
            return p
    env = os.environ.get("AETHER_HOME")
    if env:
        cand = Path(env) / "aether"
        if cand.is_file():
            return cand
        cand = Path(env) / "bin" / "aether"
        if cand.is_file():
            return cand
    which = shutil.which("aether")
    if which:
        return Path(which)
    return None


def run_aether(
    args: list[str],
    pocket: str | Path,
    *,
    aether_bin: str | Path | None = None,
    timeout: int = 60,
) -> PocketResult:
    root = refuse_if_operator(pocket)
    bin_path = find_aether_bin(aether_bin)
    if bin_path is None:
        raise PocketError("aether CLI not found (set AETHER_HOME or ship bin/aether)")
    cmd = [str(bin_path), *args, str(root)]
    env = os.environ.copy()
    # Do not let operator AETHER_HOME steal a pocket bind
    home = bin_path.parent
    if home.name == "bin":
        home = home.parent
    env["AETHER_HOME"] = str(home)
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except FileNotFoundError as exc:
        raise PocketError(f"cannot exec aether: {exc}") from exc
    text = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    return PocketResult(ok=proc.returncode == 0, code=proc.returncode, text=text.strip())


def current(pocket: str | Path, **kw) -> PocketResult:
    return run_aether(["current"], pocket, **kw)


def current_validate(pocket: str | Path, **kw) -> PocketResult:
    return run_aether(["current", "validate"], pocket, **kw)


def brief(pocket: str | Path, **kw) -> PocketResult:
    return run_aether(["brief"], pocket, **kw)


def drift(pocket: str | Path, **kw) -> PocketResult:
    return run_aether(["drift"], pocket, **kw)


def events_tail(pocket: str | Path, n: int = 8) -> PocketResult:
    root = refuse_if_operator(pocket)
    ev = root / ".aether" / "events.jsonl"
    if not ev.is_file():
        return PocketResult(ok=True, code=0, text="(no events)", extra={"lines": []})
    lines = ev.read_text(encoding="utf-8").splitlines()
    tail = lines[-n:]
    return PocketResult(ok=True, code=0, text="\n".join(tail), extra={"lines": tail})


def parse_fields(current_md: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in current_md.splitlines():
        m = FIELD_RE.match(line.strip())
        if not m:
            continue
        name = m.group("name").strip().rstrip(":")
        if name in AUTHORITY_FIELDS and name not in out:
            out[name] = m.group("value").strip()
    return out


def parse_field_alts(text: str) -> dict[str, list[str]]:
    """Every **Field:** value, including duplicates (alternative hunks)."""
    out: dict[str, list[str]] = {name: [] for name in AUTHORITY_FIELDS}
    for line in (text or "").splitlines():
        m = FIELD_RE.match(line.strip())
        if not m:
            continue
        name = m.group("name").strip().rstrip(":")
        if name not in AUTHORITY_FIELDS:
            continue
        val = m.group("value").strip()
        if val and val not in out[name]:
            out[name].append(val)
    return {k: v for k, v in out.items() if v}


def extract_propose_block(propose_md: str) -> str:
    """Prefer the block after 'Proposed CURRENT change'; else first fence; else whole file."""
    prefer = re.search(
        r"Proposed CURRENT change.{0,80}```(?:markdown|md)?\s*\n(.*?)```",
        propose_md,
        re.DOTALL | re.IGNORECASE,
    )
    if prefer:
        return prefer.group(1).strip()
    m = re.search(r"```(?:markdown|md)?\s*\n(.*?)```", propose_md, re.DOTALL)
    if m:
        return m.group(1).strip()
    return propose_md


def parse_field_value_pairs(text: str) -> dict[str, str]:
    """Accept **Field:** Name / **Value:** x dumps from sloppy models."""
    out: dict[str, str] = {}
    name = None
    for line in text.splitlines():
        m = FIELD_RE.match(line.strip())
        if not m:
            continue
        key = m.group("name").strip().rstrip(":")
        val = m.group("value").strip()
        if key.lower() == "field" and val:
            name = val
        elif key.lower() == "value" and name:
            if name in AUTHORITY_FIELDS:
                out[name] = val
            name = None
    return out


def apply_fields_to_current(current_text: str, fields: dict[str, str]) -> str:
    lines = current_text.splitlines()
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        m = FIELD_RE.match(line.strip())
        if m:
            name = m.group("name").strip().rstrip(":")
            if name in fields:
                out.append(f"**{name}:** {fields[name]}")
                seen.add(name)
                continue
        out.append(line)
    missing = [k for k in fields if k not in seen]
    if missing:
        # insert after title
        insert_at = 1 if out and out[0].startswith("#") else 0
        block = [f"**{k}:** {fields[k]}" for k in missing]
        out = out[:insert_at] + [""] + block + out[insert_at:]
    return "\n".join(out) + ("\n" if current_text.endswith("\n") else "")


def apply_propose(pocket: str | Path, only: list[str] | None = None) -> PocketResult:
    """Write proposed **Field:** values into CURRENT.md. Does not approve.

    ``only`` limits which AUTHORITY_FIELDS land. Empty list is a refuse.
    """
    root = refuse_if_operator(pocket)
    cf = root / "CURRENT.md"
    pf = root / PROPOSE_NAME
    if not cf.is_file():
        raise PocketError("no CURRENT.md in pocket")
    if not pf.is_file():
        raise PocketError(f"no {PROPOSE_NAME} in pocket")
    block = extract_propose_block(pf.read_text(encoding="utf-8"))
    fields = parse_fields(block)
    if not fields:
        fields = parse_field_value_pairs(pf.read_text(encoding="utf-8"))
    if not fields:
        raise PocketError("PROPOSE has no **Field:** lines to apply")
    if only is not None:
        allow = [n for n in only if n in AUTHORITY_FIELDS]
        if not allow:
            raise PocketError("refused: no hunks included")
        fields = {k: v for k, v in fields.items() if k in allow}
        if not fields:
            raise PocketError("refused: included hunks have no proposed values")
    new_text = apply_fields_to_current(cf.read_text(encoding="utf-8"), fields)
    cf.write_text(new_text, encoding="utf-8")
    return PocketResult(
        ok=True,
        code=0,
        text="applied fields: " + ", ".join(sorted(fields)),
        extra={"fields": fields},
    )


def write_receipt(
    pocket: str | Path,
    *,
    said: str,
    reason: str = "",
) -> PocketResult:
    """Page they can open tomorrow. Never writes CURRENT.md."""
    root = refuse_if_operator(pocket)
    fields: dict[str, str] = {}
    cf = root / "CURRENT.md"
    if cf.is_file():
        fields = parse_fields(cf.read_text(encoding="utf-8"))
    ev = events_tail(root, n=5)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    nxt = fields.get("Next", "(unset)")
    obj = fields.get("Objective", "")
    approval = fields.get("Approval", "")
    status = fields.get("Status", "")
    said_l = said.strip().lower()
    if said_l in {"yes", "approved"}:
        headline = "You said Yes."
        said_label = "Yes"
    else:
        headline = "You said Not yet. The machine did not pretend you agreed."
        said_label = "Not yet"
    body = (
        f"# Receipt\n\n"
        f"**When:** {now}\n"
        f"**You said:** {said_label}\n"
        f"**Plan (Next):** {nxt}\n"
        f"**Objective:** {obj}\n"
        f"**Status:** {status}\n"
        f"**Approval:** {approval}\n\n"
        f"{headline}\n\n"
        f"Silence is never permission.\n\n"
        f"## What happened\n"
        f"- Reason recorded: {reason or '(none)'}\n\n"
        f"## Trail\n\n"
        f"```\n{ev.text}\n```\n"
    )
    dest = root / RECEIPT_NAME
    dest.write_text(body, encoding="utf-8")
    return PocketResult(ok=True, code=0, text=f"wrote {RECEIPT_NAME}", extra={"path": str(dest)})


def read_receipt(pocket: str | Path) -> str:
    root = refuse_if_operator(pocket)
    rf = root / RECEIPT_NAME
    if not rf.is_file():
        return ""
    return rf.read_text(encoding="utf-8")


def _said_from_receipt(text: str) -> str:
    m = re.search(r"\*\*You said:\*\*\s*(.+)", text)
    return m.group(1).strip() if m else ""


def _empty_face(path: str, message: str, *, refused: bool = False) -> dict:
    return {
        "ok": False,
        "refused": refused,
        "bound": False,
        "path": path,
        "message": message,
        "has_current": False,
        "objective": "",
        "next": "",
        "phase": "",
        "status": "",
        "approval": "",
        "plan_text": "",
        "propose": "",
        "receipt": "",
        "said": "",
        "open_is_yes": False,
        "shortcuts": [],
        "schema": {},
        "schema_draft": {},
        "chat_len": 0,
        "walk": "bind",
        "chat_stage": "",
        "first_sit": False,
    }


def bind_folder(pocket: str | Path) -> dict:
    """Name one folder. Creates it if missing. Not Yes. Not the operator tree."""
    if _blank_pocket(pocket):
        return _empty_face("", "Name your folder. One project at a time.")
    root = _resolve(pocket)
    if is_operator_tree(root):
        return _empty_face(
            str(root),
            "That folder is the operator tree. Bind a different folder.",
            refused=True,
        )
    if root.exists() and not root.is_dir():
        return _empty_face(str(root), "Bind a folder, not a file.")
    if len(root.parts) < 2:
        return _empty_face(str(root), "Name a folder, not the phone root.")
    if not root.exists():
        try:
            root.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            return _empty_face(str(root), f"Could not make this folder. {exc}")
    return face_state(root)


def face_state(pocket: str | Path) -> dict:
    """People-app walk payload for the phone face. Does not approve. Open is not Yes."""
    if _blank_pocket(pocket):
        return _empty_face("", "Name your folder. One project at a time.")
    root = _resolve(pocket)
    if not root.exists():
        return _empty_face(
            str(root),
            "This folder is not on this phone yet. Bind a folder that exists.",
        )
    if not root.is_dir():
        return _empty_face(str(root), "Bind a folder, not a file.")
    if is_operator_tree(root):
        return _empty_face(
            str(root),
            "That folder is the operator tree. Bind a different folder.",
            refused=True,
        )
    cf = root / "CURRENT.md"
    plan_text = cf.read_text(encoding="utf-8") if cf.is_file() else ""
    fields = parse_fields(plan_text) if plan_text else {}
    receipt = ""
    rf = root / RECEIPT_NAME
    if rf.is_file():
        receipt = rf.read_text(encoding="utf-8")
    propose = ""
    pf = root / PROPOSE_NAME
    if pf.is_file():
        propose = pf.read_text(encoding="utf-8")
    if not cf.is_file():
        message = "This folder is bound. No plan file yet."
    else:
        message = "This folder is bound."
    payload = {
        "ok": True,
        "refused": False,
        "bound": True,
        "path": str(root),
        "message": message,
        "has_current": cf.is_file(),
        "objective": fields.get("Objective", ""),
        "next": fields.get("Next", ""),
        "phase": fields.get("Phase", ""),
        "status": fields.get("Status", ""),
        "approval": fields.get("Approval", ""),
        "plan_text": plan_text,
        "propose": propose,
        "receipt": receipt,
        "said": _said_from_receipt(receipt),
        "open_is_yes": False,
        "shortcuts": [s["name"] for s in project_shortcuts(root)],
        "schema": schema_fields(root),
        "schema_draft": read_schema_draft(root),
        "chat_len": 0,
        "walk": "plan",
        "chat_stage": "",
        "first_sit": is_first_sit(root),
    }
    return _apply_walk(payload, root)


def face_state_json(pocket: str | Path) -> str:
    return json.dumps(face_state(pocket), ensure_ascii=False)


def is_first_sit(pocket: str | Path) -> bool:
    """No published Objective or Next. Template stage, not hunk pick."""
    root = refuse_if_operator(pocket)
    cf = root / "CURRENT.md"
    if not cf.is_file():
        return True
    fields = parse_fields(cf.read_text(encoding="utf-8"))
    obj = (fields.get("Objective") or "").strip()
    nxt = (fields.get("Next") or "").strip()
    return not obj and not nxt


def _action_id_from(asked: str) -> str:
    words = re.findall(r"[a-z0-9]+", (asked or "").lower())
    if not words:
        return "name-the-sit"
    return "-".join(words[:4])[:48]


def write_first_sit_template(
    pocket: str | Path,
    asked: str,
    fields: dict[str, str] | None = None,
) -> PocketResult:
    """Full PROPOSE CURRENT template. Never CURRENT. Not Yes."""
    root = refuse_if_operator(pocket)
    asked_s = (asked or "").strip().replace("\n", " ")[:200]
    src = {name: "" for name in AUTHORITY_FIELDS}
    if isinstance(fields, dict):
        for name in AUTHORITY_FIELDS:
            val = str(fields.get(name) or "").strip()
            if val:
                src[name] = val
    src["Objective"] = src["Objective"] or asked_s or "Sit this folder. One Next."
    src["Phase"] = src["Phase"] or "SELECT"
    src["Status"] = src["Status"] or "DRAFT"
    src["Baseline"] = src["Baseline"] or "first-sit"
    src["Next"] = src["Next"] or _action_id_from(asked_s)
    src["Approval"] = src["Approval"] or "PENDING"
    return write_schema_draft(root, src)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _append_event(root: Path, kind: str, **fields: object) -> Path:
    dest = root / ".aether"
    dest.mkdir(parents=True, exist_ok=True)
    ev = dest / "events.jsonl"
    payload = {"ts": _now_iso(), "kind": kind, **fields}
    with ev.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return ev


def _append_decision(root: Path, line: str) -> None:
    path = root / "DECISIONS.md"
    if not path.is_file():
        path.write_text(
            "# DECISIONS\n\nAppend-only human decisions. Authority remains CURRENT.md.\n\n",
            encoding="utf-8",
        )
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line.rstrip() + "\n")


def _require_why(reason: str) -> str:
    why = (reason or "").strip()
    if not why:
        raise PocketError("refused: Why is required")
    return why


def pocket_approve(pocket: str | Path, reason: str) -> PocketResult:
    """Same field/event shape as ``aether approve``. No POSIX aether. Not for agents."""
    root = refuse_if_operator(pocket)
    why = _require_why(reason)
    cf = root / "CURRENT.md"
    if not cf.is_file():
        raise PocketError("no CURRENT.md in pocket")
    fields = parse_fields(cf.read_text(encoding="utf-8"))
    patch = {"Status": "APPROVED", "Approval": "APPROVED"}
    phase = (fields.get("Phase") or "").strip().upper()
    if phase in {"EXECUTE", "REVIEW", "SELECT", "COMMIT"}:
        patch["Phase"] = "APPROVE"
    cf.write_text(apply_fields_to_current(cf.read_text(encoding="utf-8"), patch), encoding="utf-8")
    ev = _append_event(root, "approve", reason=why, by="human")
    _append_decision(root, f"- {_now_iso()} APPROVED: {why}")
    text = f"APPROVED: {why}\n  CURRENT Status/Approval updated. Events: {ev}"
    return PocketResult(ok=True, code=0, text=text, extra={"reason": why})


def pocket_reject(pocket: str | Path, reason: str) -> PocketResult:
    """Same field/event shape as ``aether reject``. No POSIX aether. Not for agents."""
    root = refuse_if_operator(pocket)
    why = _require_why(reason)
    cf = root / "CURRENT.md"
    if not cf.is_file():
        raise PocketError("no CURRENT.md in pocket")
    patch = {"Status": "REJECTED", "Approval": "REJECTED", "Phase": "SELECT"}
    cf.write_text(apply_fields_to_current(cf.read_text(encoding="utf-8"), patch), encoding="utf-8")
    ev = _append_event(root, "reject", reason=why, by="human", phase="SELECT")
    _append_decision(
        root,
        f"- {_now_iso()} REJECTED: {why} (returned to SELECT; no automatic rebuild)",
    )
    text = f"REJECTED: {why}\n  Phase → SELECT. No automatic rebuild. Events: {ev}"
    return PocketResult(ok=True, code=0, text=text, extra={"reason": why})


def yes(
    pocket: str | Path,
    reason: str = "yes from demo sitting",
    included: list[str] | str | None = None,
    **kw,
) -> PocketResult:
    """Human Yes: apply included hunks then native approve. Agent must not call this.

    Does not exec POSIX ``aether``. ``kw`` kept for FaceBridge call sites.
    """
    del kw
    _require_why(reason)
    if included is not None:
        set_hunk_included(pocket, included)
    names = hunk_included(pocket)
    applied = apply_propose(pocket, only=names)
    approved = pocket_approve(pocket, reason)
    rec = write_receipt(pocket, said="Yes", reason=reason)
    text = applied.text + "\n" + approved.text + "\n" + rec.text
    return PocketResult(
        ok=approved.ok,
        code=approved.code,
        text=text.strip(),
        extra={"applied": applied.extra, "approve": approved.text, "receipt": rec.text},
    )


def not_yet(pocket: str | Path, reason: str = "not yet from demo sitting", **kw) -> PocketResult:
    del kw
    rejected = pocket_reject(pocket, reason)
    rec = write_receipt(pocket, said="Not yet", reason=reason)
    text = rejected.text + "\n" + rec.text
    return PocketResult(
        ok=rejected.ok,
        code=rejected.code,
        text=text.strip(),
        extra={"reject": rejected.text, "receipt": rec.text},
    )


def next_action(pocket: str | Path, action_id: str, **kw) -> PocketResult:
    return run_aether(["next", action_id], pocket, **kw)


def read_propose(pocket: str | Path) -> str:
    root = refuse_if_operator(pocket)
    pf = root / PROPOSE_NAME
    if not pf.is_file():
        return ""
    return pf.read_text(encoding="utf-8")


def write_propose(pocket: str | Path, text: str) -> PocketResult:
    """Editor save. Never writes CURRENT.md."""
    root = refuse_if_operator(pocket)
    pf = root / PROPOSE_NAME
    pf.write_text(text, encoding="utf-8")
    return PocketResult(ok=True, code=0, text=f"wrote {pf.name} ({len(text)} bytes)")


def schema_fields(pocket: str | Path) -> dict[str, str]:
    """Live CURRENT AUTHORITY_FIELDS. Never writes. Open is not Yes."""
    root = refuse_if_operator(pocket)
    cf = root / "CURRENT.md"
    found = parse_fields(cf.read_text(encoding="utf-8")) if cf.is_file() else {}
    return {name: found.get(name, "") for name in AUTHORITY_FIELDS}


def read_schema_draft(pocket: str | Path) -> dict[str, str]:
    """Proposed AUTHORITY_FIELDS from PROPOSE-CURRENT.md; else live schema_fields."""
    root = refuse_if_operator(pocket)
    live = schema_fields(root)
    pf = root / PROPOSE_NAME
    if not pf.is_file():
        return dict(live)
    raw = pf.read_text(encoding="utf-8")
    proposed = parse_fields(extract_propose_block(raw))
    if not proposed:
        proposed = parse_field_value_pairs(raw)
    if not proposed:
        return dict(live)
    out = dict(live)
    for name in AUTHORITY_FIELDS:
        if name in proposed:
            out[name] = proposed[name]
    return out


def write_schema_draft(pocket: str | Path, fields: dict) -> PocketResult:
    """Write PROPOSE-CURRENT.md from locked fields. Never writes CURRENT.md."""
    root = refuse_if_operator(pocket)
    clean: dict[str, str] = {}
    if isinstance(fields, dict):
        for name in AUTHORITY_FIELDS:
            if name in fields and fields[name] is not None:
                clean[name] = str(fields[name])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    field_lines = "\n".join(f"**{name}:** {clean[name]}" for name in AUTHORITY_FIELDS if name in clean)
    body = (
        "# Proposed CURRENT update (draft — not authority)\n\n"
        f"**Date:** {now}\n"
        "**Author:** schema editor (propose only)\n\n"
        "## Observations\n\n"
        "- Schema fields edited on the phone seat.\n\n"
        "## Inferences\n\n"
        "- These values are a draft until Decide publishes.\n\n"
        "## Unknowns\n\n"
        "- (none from schema editor)\n\n"
        "## Proposed CURRENT change\n\n"
        "```markdown\n"
        f"{field_lines}\n"
        "```\n\n"
        "## Conflicts with existing authority\n\n"
        "- Draft only. CURRENT.md is unchanged until Yes.\n\n"
        "## Human decision required\n\n"
        "- [ ] Apply proposed fields to CURRENT.md\n"
        "- [ ] Reject and leave CURRENT unchanged\n"
        "- [ ] Revise and re-propose\n\n"
        "**Do not** run `aether approve` from a model or agent.\n"
    )
    result = write_propose(root, body)
    result.extra = {"fields": clean}
    return result


def markdown_hunks(text: str) -> list[dict[str, str]]:
    """Split CURRENT/PROPOSE markdown into heading or AUTHORITY_FIELD hunks."""
    hunks: list[dict[str, str]] = []
    cur_id = "preamble"
    buf: list[str] = []

    def flush() -> None:
        if buf:
            hunks.append({"id": cur_id, "text": "".join(buf)})

    for line in (text or "").splitlines(keepends=True):
        head = re.match(r"^##\s+(.+?)\s*$", line)
        field = re.match(r"^\*\*([^*]+?):\*\*", line)
        name = field.group(1).strip() if field else ""
        if head:
            flush()
            cur_id = head.group(1).strip()
            buf = [line]
        elif name in AUTHORITY_FIELDS:
            flush()
            cur_id = name
            buf = [line]
        else:
            buf.append(line)
    flush()
    return hunks


def _read_live_md(root: Path) -> str:
    cf = root / "CURRENT.md"
    if cf.is_file():
        return cf.read_text(encoding="utf-8")
    return ""


def _hunk_select_path(root: Path) -> Path:
    return root / HUNK_SELECT_REL


def load_hunk_select(pocket: str | Path) -> dict:
    root = refuse_if_operator(pocket)
    path = _hunk_select_path(root)
    empty: dict = {"request": "", "focus": "", "included": None, "alts": {}, "picked": {}}
    if not path.is_file():
        return dict(empty)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(empty)
    if not isinstance(data, dict):
        return dict(empty)
    alts = data.get("alts") if isinstance(data.get("alts"), dict) else {}
    picked = data.get("picked") if isinstance(data.get("picked"), dict) else {}
    included = data.get("included")
    if included is not None and not isinstance(included, list):
        included = None
    return {
        "request": str(data.get("request") or ""),
        "focus": str(data.get("focus") or ""),
        "included": included,
        "alts": alts,
        "picked": picked,
    }


def save_hunk_select(pocket: str | Path, data: dict) -> dict:
    root = refuse_if_operator(pocket)
    path = _hunk_select_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "request": str(data.get("request") or ""),
        "focus": str(data.get("focus") or ""),
        "included": data.get("included"),
        "alts": data.get("alts") if isinstance(data.get("alts"), dict) else {},
        "picked": data.get("picked") if isinstance(data.get("picked"), dict) else {},
        "not_yes": True,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def hunk_included(pocket: str | Path) -> list[str] | None:
    """None = apply every proposed field (legacy). List = Decide's included hunks."""
    inc = load_hunk_select(pocket).get("included")
    if inc is None:
        return None
    return [n for n in inc if n in AUTHORITY_FIELDS]


def _field_value(text: str, name: str) -> str:
    found = parse_fields(text or "")
    if name in found:
        return found[name]
    line = (text or "").strip()
    if line.startswith(f"**{name}:**"):
        return line.split(":", 1)[-1].lstrip("* ").strip()
    return line


def _alt_row(field: str, value: str, source: str, index: int) -> dict:
    val = (value or "").strip()
    text = val if val.startswith(f"**{field}:**") else f"**{field}:** {val}"
    return {"id": f"{field}#{index}", "text": text, "source": source}


def record_hunk_alts(
    pocket: str | Path,
    *,
    request: str = "",
    focus: str = "",
    alts: dict[str, list[str]] | None = None,
) -> dict:
    """Store alternative wordings for one request. Never writes CURRENT."""
    root = refuse_if_operator(pocket)
    live = schema_fields(root)
    asked = (request or "").strip().replace("\n", " ")[:200]
    packed: dict[str, list[dict]] = {}
    included: list[str] = []
    picked: dict[str, str] = {}
    for name in AUTHORITY_FIELDS:
        values = list((alts or {}).get(name) or [])
        rows: list[dict] = []
        for val in values:
            clean = _field_value(val, name)
            if not clean:
                continue
            rows.append(_alt_row(name, clean, "desk", len(rows) + 1))
        if asked and focus == name:
            if asked not in {_field_value(r["text"], name) for r in rows}:
                rows.append(_alt_row(name, asked, "asked", len(rows) + 1))
        live_val = (live.get(name) or "").strip()
        if live_val and live_val not in {_field_value(r["text"], name) for r in rows}:
            rows.append(_alt_row(name, live_val, "live", len(rows) + 1))
        if rows:
            packed[name] = rows
            if any(r.get("source") != "live" for r in rows):
                included.append(name)
                desk = next((r for r in rows if r.get("source") == "desk"), rows[0])
                picked[name] = desk["id"]
    data = {
        "request": asked,
        "focus": focus,
        "included": included,
        "alts": packed,
        "picked": picked,
    }
    return save_hunk_select(root, data)


def set_hunk_included(pocket: str | Path, names: list[str] | str | None) -> dict:
    root = refuse_if_operator(pocket)
    sel = load_hunk_select(root)
    if isinstance(names, str):
        items = [n.strip() for n in names.split(",") if n.strip()]
    elif names is None:
        items = []
    else:
        items = [str(n).strip() for n in names if str(n).strip()]
    sel["included"] = [n for n in items if n in AUTHORITY_FIELDS]
    return save_hunk_select(root, sel)


def pick_hunk_alt(pocket: str | Path, field: str, alt_id: str) -> dict:
    """Write the chosen wording onto PROPOSE. Not Yes."""
    root = refuse_if_operator(pocket)
    hid = (field or "").strip()
    if hid not in AUTHORITY_FIELDS:
        raise PocketError("hunk pick needs an authority field")
    sel = load_hunk_select(root)
    alts = sel.get("alts", {}).get(hid) or []
    chosen = None
    for row in alts:
        if str(row.get("id")) == str(alt_id):
            chosen = row
            break
    if chosen is None and alts:
        raise PocketError("refused: unknown hunk alt")
    text = str((chosen or {}).get("text") or "")
    if not text:
        raise PocketError("refused: empty hunk alt")
    apply_hunk(root, hid, text if text.endswith("\n") else text + "\n")
    sel["picked"][hid] = str(alt_id)
    if hid not in (sel.get("included") or []):
        inc = list(sel.get("included") or [])
        inc.append(hid)
        sel["included"] = inc
    save_hunk_select(root, sel)
    return {"ok": True, "field": hid, "picked": str(alt_id), "not_yes": True}


def list_hunks(pocket: str | Path) -> list[dict]:
    """Live vs proposed hunks. Never writes CURRENT."""
    root = refuse_if_operator(pocket)
    live = markdown_hunks(_read_live_md(root))
    proposed = markdown_hunks(read_propose(root) or "")
    by_live = {row["id"]: row["text"] for row in live}
    by_prop = {row["id"]: row["text"] for row in proposed}
    ids: list[str] = []
    for row in live + proposed:
        if row["id"] not in ids:
            ids.append(row["id"])
    sel = load_hunk_select(root)
    for name in AUTHORITY_FIELDS:
        if name not in ids and name in (sel.get("alts") or {}):
            ids.append(name)
    included = sel.get("included")
    picked_map = sel.get("picked") or {}
    alts_map = sel.get("alts") or {}
    out: list[dict] = []
    for hid in ids:
        lt = by_live.get(hid, "")
        pt = by_prop.get(hid, "")
        differs = bool(pt) and pt != lt
        alts = alts_map.get(hid) if isinstance(alts_map.get(hid), list) else []
        if included is None:
            is_in = differs
        else:
            is_in = hid in included
        out.append(
            {
                "id": hid,
                "live": lt,
                "propose": pt,
                "differs": differs,
                "included": bool(is_in),
                "picked": str(picked_map.get(hid) or ""),
                "alts": alts,
                "request": sel.get("request") or "",
            }
        )
    return out


def _replace_hunk(doc: str, heading: str, replacement: str) -> str:
    hunks = markdown_hunks(doc)
    found = False
    parts: list[str] = []
    for row in hunks:
        if row["id"] == heading:
            parts.append(replacement if replacement.endswith("\n") or not replacement else replacement + "\n")
            found = True
        else:
            parts.append(row["text"])
    if not found:
        extra = replacement if replacement.endswith("\n") or not replacement else replacement + "\n"
        parts.append(extra)
    return "".join(parts)


def apply_hunk(pocket: str | Path, heading: str, replacement: str) -> PocketResult:
    """Write one hunk into PROPOSE-CURRENT.md. Never CURRENT.md."""
    root = refuse_if_operator(pocket)
    hid = (heading or "").strip()
    if not hid:
        raise PocketError("hunk needs a focus heading")
    body = (replacement or "")[:HUNK_MAX_CHARS]
    live = _read_live_md(root)
    current_propose = read_propose(root)
    base = current_propose if current_propose.strip() else live
    nxt = _replace_hunk(base, hid, body)
    before_live = live
    result = write_propose(root, nxt)
    after_live = _read_live_md(root)
    if after_live != before_live:
        raise PocketError("refused: hunk write touched CURRENT")
    result.extra = {"heading": hid, "propose": nxt}
    return result


def reject_hunk(pocket: str | Path, heading: str) -> PocketResult:
    """Restore one hunk in PROPOSE from live CURRENT. Never writes CURRENT."""
    root = refuse_if_operator(pocket)
    hid = (heading or "").strip()
    live_map = {row["id"]: row["text"] for row in markdown_hunks(_read_live_md(root))}
    live_text = live_map.get(hid, "")
    return apply_hunk(root, hid, live_text)


def accept_hunk(pocket: str | Path, heading: str) -> PocketResult:
    """Keep the proposed hunk (already on PROPOSE). Not Yes."""
    root = refuse_if_operator(pocket)
    hid = (heading or "").strip()
    prop = {row["id"]: row["text"] for row in markdown_hunks(read_propose(root))}
    live = {row["id"]: row["text"] for row in markdown_hunks(_read_live_md(root))}
    text = prop.get(hid) or live.get(hid, "")
    return apply_hunk(root, hid, text)


def _tailnet_path(root: Path) -> Path:
    return root / TAILNET_REL


def _load_tailnet(root: Path) -> dict:
    p = _tailnet_path(root)
    empty = {
        "status": "not-on-net",
        "kind": "",
        "fp": "",
        "desk": "",
        "login_server": "",
        "userspace": False,
    }
    if not p.is_file():
        return dict(empty)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(empty)
    if not isinstance(data, dict):
        return dict(empty)
    status = str(data.get("status") or "not-on-net")
    if status not in JOIN_STATUSES:
        status = "not-on-net"
    return {
        "status": status,
        "kind": str(data.get("kind") or ""),
        "fp": str(data.get("fp") or ""),
        "desk": str(data.get("desk") or ""),
        "login_server": str(data.get("login_server") or ""),
        "userspace": bool(data.get("userspace")),
    }


def _save_tailnet(root: Path, data: dict) -> None:
    path = _tailnet_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = {
        "status": data.get("status") or "not-on-net",
        "kind": data.get("kind") or "",
        "fp": data.get("fp") or "",
        "desk": data.get("desk") or "",
        "login_server": data.get("login_server") or "",
        "userspace": bool(data.get("userspace")),
    }
    path.write_text(json.dumps(clean, indent=2) + "\n", encoding="utf-8")


def join_status(pocket: str | Path) -> dict:
    """not-on-net / invited / connected. JOIN is not Yes."""
    if _blank_pocket(pocket):
        return {
            "status": "not-on-net",
            "kind": "",
            "fp": "",
            "desk": "",
            "login_server": "",
            "userspace": False,
            "ok": True,
        }
    root = refuse_if_operator(pocket)
    st = _load_tailnet(root)
    st["ok"] = True
    return st


def tsnet_up() -> bool:
    """True only when native userspace (or a test marker) reports Up. Not LAN Ollama."""
    flag = os.environ.get("MECHANICALL_TSNET_UP", "").strip().lower()
    if flag in {"1", "yes", "true"}:
        return True
    marker = os.environ.get("MECHANICALL_TSNET_MARKER", "").strip()
    if not marker:
        return False
    path = Path(marker)
    if not path.is_file():
        return False
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return bool(isinstance(obj, dict) and obj.get("up"))


def _join_provision(root: Path) -> str:
    """Desk-side key. Never a face well. Never git. Never CURRENT."""
    env_key = os.environ.get("MECHANICALL_JOIN_KEY", "").strip()
    env_ls = os.environ.get("MECHANICALL_LOGIN_SERVER", "").strip()
    if env_key:
        return f"{env_ls} {env_key}".strip()
    path = root / ".aether" / "join-provision"
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def join_accept(pocket: str | Path, pasted: str = "") -> dict:
    """JOIN from desk provision (env or ``.aether/join-provision``). Never stores the
    secret in tailnet.json. Never CURRENT. Not Yes. Empty paste is allowed.

    ``connected`` only if userspace tsnet is Up. A live ``myarch:11434`` is not JOIN.
    """
    root = refuse_if_operator(pocket)
    raw = pasted if isinstance(pasted, str) else str(pasted)
    text = raw.strip() or _join_provision(root)
    if not text:
        userspace = tsnet_up()
        st = {
            "status": "connected" if userspace else "not-on-net",
            "kind": "",
            "fp": "",
            "desk": "",
            "login_server": "",
            "userspace": userspace,
            "ok": True,
            "note": (
                "Connected (userspace)."
                if userspace
                else "JOIN waits on desk provision."
            ),
        }
        _save_tailnet(root, st)
        return st
    low = text.lower()
    if "17kizymaa" in low:
        raise PocketError("refused: Tailscale-as-me is not a send path")
    if "login.tailscale.com/invite" in low:
        raise PocketError("refused: Tailscale.com invite; paste a Headscale preauth key")
    login_server = ""
    key_part = text
    for token in text.replace(",", " ").split():
        if token.startswith("https://"):
            login_server = token.rstrip("/")
        elif "tskey-" in token.lower() or "hskey-" in token.lower() or len(token) > 24:
            key_part = token
    if "tskey-" in low or "hskey-" in low or (len(key_part) > 24 and "://" not in key_part):
        kind = "authkey"
    elif text.startswith("http"):
        kind = "invite-url"
    else:
        kind = "paste"
    fp = "sha256:" + hashlib.sha256(key_part.encode("utf-8")).hexdigest()[:16]
    userspace = tsnet_up()
    st = {
        "status": "connected" if userspace else "invited",
        "kind": kind,
        "fp": fp,
        "desk": "",
        "login_server": login_server,
        "userspace": userspace,
        "ok": True,
        "note": (
            "Connected (userspace)."
            if userspace
            else "Secret not stored. Userspace not linked — not connected."
        ),
    }
    _save_tailnet(root, st)
    saved = _load_tailnet(root)
    blob = json.dumps(saved)
    if len(key_part) >= 8 and key_part in blob:
        raise PocketError("refused: join state stored a secret")
    if login_server and login_server in blob:
        pass
    return st


def wake_desk(pocket: str | Path, url: str = "") -> dict:
    """POST wol-pi wake. Tailnet only. Not Yes. No public bind."""
    if not _blank_pocket(pocket):
        refuse_if_operator(pocket)
    target = (url or os.environ.get("WOL_WAKE_URL") or WAKE_DEFAULT).strip()
    _refuse_public_ollama(target)
    if target.startswith("http://0.0.0.0") or "://0.0.0.0" in target:
        raise PocketError("refused: public wake URL")
    req = urllib.request.Request(target, data=b"{}", method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            code = getattr(resp, "status", 200)
            return {
                "ok": 200 <= code < 300,
                "status": "waking" if 200 <= code < 300 else "sleeping",
                "url_host": urllib.parse.urlparse(target).hostname or "",
                "note": "",
            }
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            "ok": False,
            "status": "sleeping",
            "url_host": urllib.parse.urlparse(target).hostname or "",
            "note": str(exc),
        }


def project_shortcuts(pocket: str | Path) -> list[dict[str, str]]:
    """Named pocket files that exist. Read view only."""
    root = refuse_if_operator(pocket)
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for rel, kind in SHORTCUT_FILES:
        p = root / rel
        if p.is_file():
            out.append({"name": rel, "path": str(p), "kind": kind})
            seen.add(rel)
    for rel in list_pocket_tree(root, limit=40):
        if rel in seen or rel == CHAT_NAME:
            continue
        out.append({"name": rel, "path": str(root / rel), "kind": "file"})
        seen.add(rel)
    return out


def read_shortcut(pocket: str | Path, name: str) -> str:
    """Read one pocket file. Never CURRENT write. Path must stay inside the pocket."""
    root = refuse_if_operator(pocket)
    raw = (name or "").strip()
    if not raw:
        return ""
    candidate = Path(raw)
    target = candidate.resolve() if candidate.is_absolute() else (root / raw).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise PocketError("refused: path outside pocket") from exc
    if not target.is_file():
        return ""
    try:
        return target.read_text(encoding="utf-8")[:12_000]
    except (UnicodeDecodeError, OSError):
        return ""


def chat_history(pocket: str | Path) -> list[dict[str, str]]:
    """DRAFT-CHAT.jsonl rows {role, text}. Empty list if missing."""
    root = refuse_if_operator(pocket)
    dest = root / CHAT_NAME
    if not dest.is_file():
        return []
    rows: list[dict[str, str]] = []
    for line in dest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "role" in obj and "text" in obj:
            row = {"role": str(obj["role"]), "text": str(obj["text"])}
            if obj.get("stage"):
                row["stage"] = str(obj["stage"])
            rows.append(row)
    return rows


def _append_chat(root: Path, role: str, text: str, stage: str = "") -> None:
    dest = root / CHAT_NAME
    rec: dict[str, str] = {"role": role, "text": text}
    if stage:
        rec["stage"] = stage
    with dest.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def clear_chat(pocket: str | Path) -> dict:
    """Wipe DRAFT-CHAT.jsonl. Never writes CURRENT. Not Yes."""
    root = refuse_if_operator(pocket)
    dest = root / CHAT_NAME
    if dest.is_file():
        dest.unlink()
    return {"ok": True, "history": [], "cleared": True}


def walk_stage(pocket: str | Path) -> str:
    """Which ICM walk step this pocket is on. Open is not Yes."""
    return str(face_state(pocket).get("walk") or "bind")


def _apply_walk(face: dict, root: Path) -> dict:
    if face.get("refused") or not face.get("bound"):
        face["walk"] = "bind"
        face["chat_stage"] = ""
        return face
    hist = chat_history(root)
    last_stage = ""
    for row in reversed(hist):
        st = str(row.get("stage") or "").strip().lower()
        if row.get("role") == "assistant" and st:
            last_stage = st
            break
    face["chat_stage"] = last_stage
    face["chat_len"] = len(hist)
    said = str(face.get("said") or "").strip().lower()
    if said in {"yes", "not yet"}:
        face["walk"] = "receipt"
        return face
    if not face.get("has_current"):
        face["walk"] = "plan"
        return face
    if last_stage == "gate":
        face["walk"] = "decide"
        return face
    if hist or str(face.get("propose") or "").strip():
        face["walk"] = "chat"
        return face
    face["walk"] = "plan"
    return face


def _refuse_public_ollama(host: str) -> None:
    if "0.0.0.0" in (host or ""):
        raise PocketError(
            "refused: public bind 0.0.0.0 — use Tailscale or a private host"
        )


def _desk_hosts(host: str) -> list[str]:
    """Passed hosts first, then MagicDNS myarch, USB, LAN, last-known 100.x. Never 0.0.0.0."""
    out: list[str] = []
    for item in [h.strip().rstrip("/") for h in (host or "").split(",") if h.strip()]:
        _refuse_public_ollama(item)
        if item not in out:
            out.append(item)
    for item in DEFAULT_DESK_HOSTS:
        if item not in out:
            out.append(item)
    return out


def _ollama_generate(host: str, prompt: str, model: str, timeout: int) -> str:
    """Non-stream fallback. Prefer _ollama_stream for GATE."""
    return _ollama_stream(host, prompt, model, timeout, on_chunk=None)


def _desk_alive(host: str, timeout: int = 2) -> bool:
    _refuse_public_ollama(host)
    url = host.rstrip("/") + "/api/tags"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= getattr(resp, "status", 200) < 300
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def desk_probe(pocket: str | Path, host: str = "") -> dict:
    """Which private desk URL answers. Never 0.0.0.0. Not Decide.

    Unbound still probes (GATE can light before a folder exists). write_gate
    only runs once one project folder is bound.
    """
    tried: list[dict] = []
    found = ""
    for item in _desk_hosts(host):
        ok = _desk_alive(item)
        tried.append({"host": item, "ok": ok})
        if ok:
            found = item
            break
    if _blank_pocket(pocket):
        return {
            "ok": bool(found),
            "host": found,
            "state": "idle" if found else "quiet",
            "tried": tried,
        }
    root = refuse_if_operator(pocket)
    if found:
        write_gate(root, state="idle", step=0, desk=found)
        return {"ok": True, "host": found, "state": "idle", "tried": tried}
    write_gate(root, state="quiet", step=0, desk="")
    return {"ok": False, "host": "", "state": "quiet", "tried": tried}


def write_gate(
    pocket: str | Path,
    *,
    state: str,
    step: int = 0,
    desk: str = "",
    queue: int | None = None,
) -> dict:
    """Debug instrument. Not a chat ellipsis. Not Decide.

    States: idle / load / warm / gate (STREAM on the face) / queued / quiet.
    """
    root = refuse_if_operator(pocket)
    dest = root / ".aether"
    dest.mkdir(parents=True, exist_ok=True)
    st = state if state in GATE_STATES else "idle"
    q = 0 if queue is None else max(0, int(queue))
    if queue is None:
        try:
            prev = json.loads((dest / "gate.json").read_text(encoding="utf-8"))
            q = int(prev.get("queue") or 0) if isinstance(prev, dict) else 0
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            q = 0
    payload = {
        "state": st,
        "step": max(0, min(GATE_STEPS, int(step))),
        "steps": GATE_STEPS,
        "desk": desk or "",
        "queue": q,
    }
    (dest / "gate.json").write_text(json.dumps(payload), encoding="utf-8")
    return payload


def gate_state(pocket: str | Path) -> dict:
    empty = {"state": "idle", "step": 0, "steps": GATE_STEPS, "desk": "", "queue": 0}
    if _blank_pocket(pocket):
        return empty
    try:
        root = refuse_if_operator(pocket)
    except PocketError:
        return empty
    path = root / GATE_REL
    if not path.is_file():
        return empty
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return empty
    if not isinstance(obj, dict):
        return empty
    st = str(obj.get("state") or "idle")
    if st not in GATE_STATES:
        st = "idle"
    try:
        step = int(obj.get("step") or 0)
    except (TypeError, ValueError):
        step = 0
    try:
        qn = int(obj.get("queue") or 0)
    except (TypeError, ValueError):
        qn = 0
    return {
        "state": st,
        "step": max(0, min(GATE_STEPS, step)),
        "steps": GATE_STEPS,
        "desk": str(obj.get("desk") or ""),
        "queue": max(0, qn),
    }


def _queue_path(root: Path) -> Path:
    return root / QUEUE_REL


def list_desk_queue(pocket: str | Path) -> list[dict]:
    root = refuse_if_operator(pocket)
    path = _queue_path(root)
    if not path.is_file():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for row in raw:
        if not isinstance(row, dict):
            continue
        msg = str(row.get("message") or "").strip()
        if not msg:
            continue
        out.append(
            {
                "message": msg[:CHAT_MSG_CHARS],
                "focus": str(row.get("focus") or ""),
            }
        )
    return out


def enqueue_desk(pocket: str | Path, message: str, focus: str = "") -> dict:
    """Queue an extra Send. Never CURRENT. Not Yes."""
    root = refuse_if_operator(pocket)
    rows = list_desk_queue(root)
    rows.append(
        {
            "message": (message if isinstance(message, str) else str(message)).strip()[:CHAT_MSG_CHARS],
            "focus": (focus or "").strip(),
        }
    )
    path = _queue_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows), encoding="utf-8")
    g = gate_state(root)
    write_gate(
        root,
        state=g["state"] if g["state"] in BUSY_GATE else "queued",
        step=g["step"],
        desk=g.get("desk") or "",
        queue=len(rows),
    )
    return {"ok": True, "queued": True, "queue": len(rows), "note": "Queued."}


def pop_desk_queue(pocket: str | Path) -> dict | None:
    root = refuse_if_operator(pocket)
    rows = list_desk_queue(root)
    if not rows:
        path = _queue_path(root)
        if path.is_file():
            path.write_text("[]", encoding="utf-8")
        return None
    first, rest = rows[0], rows[1:]
    path = _queue_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rest), encoding="utf-8")
    return first


def _drain_one_send(
    root: Path,
    host: str,
    model: str,
    timeout: int,
) -> None:
    nxt = pop_desk_queue(root)
    if not nxt:
        return
    draft_chat(
        root,
        host,
        nxt["message"],
        model=model,
        timeout=timeout,
        focus=nxt.get("focus") or "",
    )


def _ollama_stream(
    host: str,
    prompt: str,
    model: str,
    timeout: int,
    on_chunk=None,
) -> str:
    _refuse_public_ollama(host)
    url = host.rstrip("/") + "/api/generate"
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0.1},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    chunks: list[str] = []
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        while True:
            line = resp.readline()
            if not line:
                break
            raw_line = line.decode("utf-8", "replace").strip()
            if not raw_line:
                continue
            try:
                obj = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            piece = str(obj.get("response") or "")
            if piece:
                chunks.append(piece)
                if on_chunk is not None:
                    on_chunk(len(chunks), piece)
            if obj.get("done"):
                break
    text = "".join(chunks).strip()
    if not text:
        raise PocketError("ollama returned empty proposal")
    return text


def list_pocket_tree(pocket: str | Path, limit: int = 80) -> list[str]:
    root = refuse_if_operator(pocket)
    skip = {".git", "__pycache__", ".pytest_cache"}
    files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in filenames:
            p = Path(dirpath) / name
            rel = p.relative_to(root)
            files.append(str(rel))
            if len(files) >= limit:
                return files
    return files


def pack_tree_context(pocket: str | Path, max_bytes: int = 80_000) -> str:
    """D9=3 demo shortcut: whole pocket tree into one prompt blob."""
    root = refuse_if_operator(pocket)
    skip = {".git", "__pycache__", ".pytest_cache"}
    parts: list[str] = []
    used = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in sorted(filenames):
            p = Path(dirpath) / name
            rel = p.relative_to(root)
            try:
                data = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            chunk = f"\n--- {rel} ---\n{data}"
            if used + len(chunk) > max_bytes:
                parts.append(f"\n--- {rel} --- [truncated: context full]\n")
                return "".join(parts)
            parts.append(chunk)
            used += len(chunk)
    return "".join(parts)


_AGENT_SYSTEM = """You are a Mechanicall peer (propose only).
Edit PROPOSE-CURRENT.md for this pocket Domain.
Never write CURRENT.md. Never approve. Never claim silence is permission.
Output the FULL new PROPOSE-CURRENT.md document only — no fence, no preamble.
Use the propose-current shape: Observations, Inferences, Unknowns,
a fenced Proposed CURRENT change with **Field:** lines, Conflicts, Human decision.
"""

# ICM chat: do not dump CURRENT/PROPOSE/full transcript at the local model.
CHAT_USER_TURNS = 3
CHAT_MSG_CHARS = 280
CHAT_SAY_CHARS = 240
_CHAT_SYS = """You propose. You never approve. You never write CURRENT.
Reply with exactly:
SAY: <one short line>
CHANGE:
**Field:** <new value>
"""
_CHAT_SYS_CHANGE = """Never approve. Never write CURRENT.
The person asked for one change. Give THREE alternative values for that one field.
Do not say SURE. Do not give a GOAL or RULE. Do not continue a transcript.
Exactly:
SAY: <one short line>
CHANGE:
**{focus}:** <wording 1>
**{focus}:** <wording 2>
**{focus}:** <wording 3>
"""
_CHAT_SYS_TEMPLATE = """Never approve. Never write CURRENT.
They have no plan yet. Write a complete CURRENT template from what they said.
Do not say SURE. Do not give a GOAL or RULE. Do not continue a transcript.
Exactly:
SAY: <one short line>
CHANGE:
**Objective:** <one sentence>
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** first-sit
**Next:** <one-action-id>
**Approval:** PENDING
"""


def chat_stage(message: str) -> str:
    """Decision framework: which ICM stage this turn is. No extra model call."""
    m = (message or "").strip().lower()
    if not m:
        return "show-plan"
    gate = (
        "approve",
        "approved",
        "reject",
        "not yet",
        "notyet",
        " i say yes",
        "say yes",
        "tap yes",
    )
    if m in {"yes", "no"} or any(g in m for g in gate):
        return "gate"
    propose = (
        "propose",
        "change next",
        "set next",
        "update plan",
        "draft",
        "rewrite",
        "change the plan",
        "**next:**",
    )
    if any(p in m for p in propose):
        return "propose"
    template = (
        "start a plan",
        "new project",
        "make a template",
        "first sit",
    )
    if any(t in m for t in template):
        return "template"
    return "show-plan"


def _trim(text: str, n: int) -> str:
    t = (text or "").strip()
    if len(t) <= n:
        return t
    return t[: n - 1] + "…"


def _schema_lines(pocket: str | Path) -> str:
    fields = schema_fields(pocket)
    lines = [f"**{k}:** {fields.get(k, '')}" for k in AUTHORITY_FIELDS]
    return "\n".join(lines)


def _folder_names(pocket: str | Path, limit: int = CHAT_FILES) -> str:
    names = list_pocket_tree(pocket, limit=limit)
    if not names:
        return "(empty folder)"
    return "\n".join(names)


def _slim_user_turns(history: list[dict[str, str]]) -> str:
    users = [row for row in history if row.get("role") == "user"][-CHAT_USER_TURNS:]
    if not users:
        return "(none)"
    # Do not prefix "user:" — the 7B continues that transcript as the desk say.
    return "\n".join(
        f"- {_trim(row.get('text', ''), CHAT_MSG_CHARS)}" for row in users
    )


def _prompt_contains_whole_file(prompt: str, root: Path) -> bool:
    live = _read_live_md(root)
    if len(live) < 400:
        return False
    return live in (prompt or "")


def _parse_chat_model(raw: str) -> tuple[str, dict[str, str], str, str]:
    """Return say, fields, stage, change-text. Never treat a user-echo as the bubble."""
    text = (raw or "").strip()
    say = ""
    fields: dict[str, str] = {}
    stage = "show-plan"
    hunk = ""
    say_m = re.search(r"(?im)^SAY:\s*(.+)$", text)
    if say_m:
        say = say_m.group(1).strip()
    change_m = re.search(r"(?im)^CHANGE:\s*(.*)$", text, re.DOTALL)
    if change_m:
        hunk = change_m.group(1).strip()
    blob = text
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        blob = fence.group(1)
    else:
        brace = re.search(r"\{.*\}", text, re.DOTALL)
        if brace:
            blob = brace.group(0)
    try:
        obj = json.loads(blob)
    except json.JSONDecodeError:
        obj = None
    if isinstance(obj, dict):
        say = say or str(obj.get("say") or "").strip()
        st = str(obj.get("stage") or "").strip().lower()
        if st in {"show-plan", "propose", "gate"}:
            stage = st
        raw_fields = obj.get("fields") or {}
        if isinstance(raw_fields, dict):
            for key in AUTHORITY_FIELDS:
                val = raw_fields.get(key) or raw_fields.get(key.lower())
                if val:
                    fields[key] = str(val).strip()
        schema = obj.get("schema") or {}
        if isinstance(schema, dict):
            for key in AUTHORITY_FIELDS:
                val = schema.get(key) or schema.get(key.lower())
                if val and key not in fields:
                    fields[key] = str(val).strip()
        hunk = hunk or str(obj.get("change") or obj.get("hunk") or "").strip()
    if not fields:
        extracted = parse_fields(hunk or text)
        if not extracted:
            extracted = parse_fields(extract_propose_block(text))
        fields = {k: v for k, v in extracted.items() if k in AUTHORITY_FIELDS and v}
        if fields:
            stage = "propose"
    echo = text.lower().lstrip().startswith("user:") or text.lower().count("\nuser:") >= 1
    if echo and not fields and not hunk:
        say = "Desk did not propose. Try again."
        return _trim(say, CHAT_SAY_CHARS), {}, "show-plan", ""
    if not say:
        if fields or hunk:
            say = "Change drafted."
        else:
            say = _trim(re.sub(r"\s+", " ", text), CHAT_SAY_CHARS) or (
                "The desk answered."
            )
    return _trim(say, CHAT_SAY_CHARS), fields, stage, hunk[:HUNK_MAX_CHARS]


def agent_edit_propose(
    pocket: str | Path,
    *,
    ollama_host: str,
    model: str = "personal-llm-sft-v4:latest",
    instruction: str = "Update the proposal from the pocket files.",
    timeout: int = 180,
) -> PocketResult:
    """Call remote Ollama; write only PROPOSE-CURRENT.md."""
    root = refuse_if_operator(pocket)
    tree = pack_tree_context(root)
    existing = read_propose(root)
    prompt = (
        f"{_AGENT_SYSTEM}\n\nInstruction:\n{instruction}\n\n"
        f"Existing PROPOSE-CURRENT.md:\n{existing or '(empty)'}\n\n"
        f"Pocket tree (demo whole-folder context):\n{tree}\n"
    )
    url = ollama_host.rstrip("/") + "/api/generate"
    body = json.dumps(
        {"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}}
    ).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise PocketError(f"ollama failed: {exc}") from exc
    text = (raw.get("response") or "").strip()
    if not text:
        raise PocketError("ollama returned empty proposal")
    # Refuse if the model tried to look like a live CURRENT-only dump without propose framing
    write_propose(root, text)
    return PocketResult(
        ok=True,
        code=0,
        text=f"agent wrote {PROPOSE_NAME} ({len(text)} bytes)",
        extra={"model": model, "host": ollama_host},
    )


def draft_chat(
    pocket: str | Path,
    host: str,
    message: str,
    model: str = "personal-llm-sft-v4:latest",
    timeout: int = 25,
    focus: str = "",
) -> dict:
    """ICM chat turn. Slim context. Short bubble. PROPOSE only on propose stage. Never CURRENT."""
    root = refuse_if_operator(pocket)
    _refuse_public_ollama(host)
    user_text = message if isinstance(message, str) else str(message)
    focus_id = (focus or "").strip()
    stage = chat_stage(user_text)
    if is_first_sit(root) and stage not in {"gate"}:
        stage = "template"
        focus_id = ""
    elif focus_id and stage == "show-plan":
        stage = "propose"
    existing = read_propose(root)
    if stage == "gate":
        say = "Use Decide."
        write_gate(root, state="quiet", step=0)
        _append_chat(root, "user", user_text, stage="gate")
        _append_chat(root, "assistant", say, stage="gate")
        return {
            "ok": True,
            "reply": say,
            "propose": existing,
            "stage": "gate",
            "history": chat_history(root),
            "fields": {},
            "schema_draft": read_schema_draft(root),
            "hunk": "",
            "focus": focus_id,
        }
    gnow = gate_state(root)
    if gnow["state"] in BUSY_GATE:
        queued = enqueue_desk(root, user_text, focus_id)
        say = queued["note"]
        _append_chat(root, "user", user_text, stage=stage)
        _append_chat(root, "assistant", say, stage=stage)
        return {
            "ok": True,
            "reply": say,
            "propose": existing,
            "stage": stage,
            "history": chat_history(root),
            "fields": {},
            "schema_draft": read_schema_draft(root),
            "hunk": "",
            "focus": focus_id,
            "queued": True,
            "queue": queued["queue"],
        }
    _append_chat(root, "user", user_text, stage=stage)
    history_before = chat_history(root)
    schema = _schema_lines(root)
    slim = _slim_user_turns(history_before)
    names = _folder_names(root)
    if stage == "template":
        prompt = (
            f"{_CHAT_SYS_TEMPLATE}\n"
            f"They said:\n{slim}\n"
        )
    elif focus_id:
        hunks = {row["id"]: row for row in list_hunks(root)}
        focused = hunks.get(focus_id) or {"live": "", "propose": ""}
        live_h = _trim(str(focused.get("live") or ""), HUNK_MAX_CHARS)
        prop_h = _trim(str(focused.get("propose") or ""), HUNK_MAX_CHARS)
        prompt = (
            f"{_CHAT_SYS_CHANGE.format(focus=focus_id)}\n"
            f"Focus field: {focus_id}\n"
            f"Live:\n{live_h or '(empty)'}\n"
            f"Already proposed (may be empty):\n{prop_h or '(empty)'}\n"
            f"They said:\n{slim}\n"
        )
    else:
        prompt = (
            f"{_CHAT_SYS}\n"
            f"Turn stage: {stage}\n"
            f"Plan (fields only; not the whole file):\n{schema}\n\n"
            f"Folder files (names only; not contents):\n{names}\n\n"
            f"Recent user turns (capped):\n{slim}\n"
        )
    if _prompt_contains_whole_file(prompt, root):
        write_gate(root, state="quiet", step=0, desk="")
        err = "refused: whole CURRENT in prompt"
        _append_chat(root, "assistant", err, stage=stage)
        return {
            "ok": False,
            "reply": err,
            "propose": existing,
            "stage": stage,
            "history": chat_history(root),
            "fields": {},
            "schema_draft": read_schema_draft(root),
            "hunk": "",
            "focus": focus_id,
        }
    write_gate(root, state="load", step=0, desk="")
    live = ""
    for candidate in _desk_hosts(host):
        if _desk_alive(candidate, timeout=2):
            live = candidate
            break
    if not live:
        write_gate(root, state="quiet", step=0, desk="")
        if stage == "template":
            write_first_sit_template(root, user_text)
            say = "Desk quiet. Template drafted from what you said. Not Yes."
            _append_chat(root, "assistant", say, stage="template")
            return {
                "ok": True,
                "reply": say,
                "propose": read_propose(root),
                "stage": "template",
                "history": chat_history(root),
                "fields": {},
                "schema_draft": read_schema_draft(root),
                "hunk": "",
                "focus": "",
                "fallback": "static",
            }
        err = "Desk quiet."
        _append_chat(root, "assistant", err, stage=stage)
        return {
            "ok": False,
            "reply": err,
            "propose": existing,
            "stage": stage,
            "history": chat_history(root),
            "fields": {},
            "schema_draft": read_schema_draft(root),
            "hunk": "",
            "focus": focus_id,
        }
    write_gate(root, state="load", step=max(1, GATE_STEPS // 4), desk=live)
    text = ""
    last_exc: Exception | None = None
    streaming = {"on": False}

    def _on_chunk(n: int, _piece: str) -> None:
        streaming["on"] = True
        write_gate(
            root,
            state="gate",
            step=min(GATE_STEPS, 1 + n // 2),
            desk=live,
        )

    stream_timeout = DESK_STREAM_TIMEOUT if timeout <= 0 else max(int(timeout), DESK_TRY_TIMEOUT)
    try:
        text = _ollama_stream(live, prompt, model, stream_timeout, on_chunk=_on_chunk)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, PocketError, OSError) as exc:
        last_exc = exc
    if not text:
        write_gate(root, state="quiet", step=0, desk=live)
        if stage == "template":
            write_first_sit_template(root, user_text)
            say = "Desk quiet. Template drafted from what you said. Not Yes."
            _append_chat(root, "assistant", say, stage="template")
            _drain_one_send(root, host, model, timeout)
            return {
                "ok": True,
                "reply": say,
                "propose": read_propose(root),
                "stage": "template",
                "history": chat_history(root),
                "host": live,
                "fields": {},
                "schema_draft": read_schema_draft(root),
                "hunk": "",
                "focus": "",
                "fallback": "static",
            }
        err = f"Desk quiet. ({last_exc})"
        _append_chat(root, "assistant", err, stage=stage)
        _drain_one_send(root, host, model, timeout)
        return {
            "ok": False,
            "reply": err,
            "propose": existing,
            "stage": stage,
            "history": chat_history(root),
            "host": live,
            "fields": {},
            "schema_draft": read_schema_draft(root),
            "hunk": "",
            "focus": focus_id,
        }
    write_gate(root, state="quiet", step=GATE_STEPS, desk=live, queue=len(list_desk_queue(root)))
    used_host = live
    say, fields, parsed_stage, hunk = _parse_chat_model(text)
    alts = parse_field_alts(text)
    if hunk:
        extra = parse_field_alts(hunk)
        for name, vals in extra.items():
            have = alts.setdefault(name, [])
            for val in vals:
                if val not in have:
                    have.append(val)
    out_stage = stage
    if stage == "template":
        write_first_sit_template(root, user_text, fields)
        say = say or "Template on PROPOSE. Use Decide to publish."
        out_stage = "template"
    elif stage == "propose":
        if not alts and fields:
            alts = {k: [v] for k, v in fields.items() if v}
        if not alts and focus_id and hunk:
            first = parse_fields(hunk) or parse_fields(f"**{focus_id}:** {hunk}")
            alts = {k: [v] for k, v in first.items() if v}
        if alts:
            for name, vals in alts.items():
                apply_hunk(root, name, f"**{name}:** {vals[0]}\n")
        elif focus_id and hunk:
            apply_hunk(root, focus_id, hunk)
        elif fields and not focus_id:
            write_schema_draft(root, {**schema_fields(root), **fields})
        elif (not focus_id) and text and parse_fields(text):
            write_propose(root, text)
        if alts or focus_id:
            record_hunk_alts(root, request=user_text, focus=focus_id, alts=alts)
        say = say or "Draft updated."
        out_stage = "propose"
    elif parsed_stage == "propose":
        # Local stage owns the turn. The desk cannot promote a question into a write.
        fields = {}
        hunk = ""
    _append_chat(root, "assistant", say, stage=out_stage)
    _drain_one_send(root, host, model, timeout)
    return {
        "ok": True,
        "reply": say,
        "propose": read_propose(root),
        "stage": out_stage,
        "history": chat_history(root),
        "host": used_host,
        "fields": fields,
        "schema_draft": read_schema_draft(root),
        "hunk": hunk,
        "focus": focus_id,
        "alts": alts,
    }


def projection(pocket: str | Path, **kw) -> dict:
    """Week 2 face payload: current + validate + brief + events + drift + propose."""
    root = refuse_if_operator(pocket)
    cur = current(root, **kw)
    val = current_validate(root, **kw)
    br = brief(root, **kw)
    dr = drift(root, **kw)
    ev = events_tail(root)
    return {
        "root": str(root),
        "demo": True,
        "current": cur.text,
        "validate": val.text,
        "validate_ok": val.ok,
        "brief": br.text,
        "drift": dr.text,
        "events": ev.text,
        "propose": read_propose(root),
        "receipt": read_receipt(root),
        "fields": parse_fields((root / "CURRENT.md").read_text(encoding="utf-8"))
        if (root / "CURRENT.md").is_file()
        else {},
    }
