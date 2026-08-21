"""Chaquopy face → aether_pocket. Demo only."""
from __future__ import annotations

import json
import traceback


def _wrap(fn, *args):
    try:
        from aether_pocket import (
            PocketError,
            agent_edit_propose,
            bind_folder,
            brief,
            chat_history,
            clear_chat,
            current,
            current_validate,
            accept_hunk,
            apply_hunk,
            desk_probe,
            draft_chat,
            join_accept,
            join_status,
            list_hunks,
            reject_hunk,
            wake_desk,
            drift,
            events_tail,
            face_state_json,
            gate_state,
            not_yet,
            project_shortcuts,
            read_propose,
            read_receipt,
            read_shortcut,
            read_schema_draft,
            refuse_if_operator,
            schema_fields,
            write_propose,
            write_schema_draft,
            yes,
        )
    except Exception as exc:  # import error is a face error, not law
        return f"ERROR: import aether_pocket: {exc}"
    try:
        return fn(
            {
                "PocketError": PocketError,
                "agent_edit_propose": agent_edit_propose,
                "bind_folder": bind_folder,
                "brief": brief,
                "chat_history": chat_history,
                "clear_chat": clear_chat,
                "current": current,
                "current_validate": current_validate,
                "accept_hunk": accept_hunk,
                "apply_hunk": apply_hunk,
                "desk_probe": desk_probe,
                "draft_chat": draft_chat,
                "join_accept": join_accept,
                "join_status": join_status,
                "list_hunks": list_hunks,
                "reject_hunk": reject_hunk,
                "wake_desk": wake_desk,
                "drift": drift,
                "events_tail": events_tail,
                "face_state_json": face_state_json,
                "gate_state": gate_state,
                "not_yet": not_yet,
                "project_shortcuts": project_shortcuts,
                "read_propose": read_propose,
                "read_receipt": read_receipt,
                "read_shortcut": read_shortcut,
                "read_schema_draft": read_schema_draft,
                "refuse_if_operator": refuse_if_operator,
                "schema_fields": schema_fields,
                "write_propose": write_propose,
                "write_schema_draft": write_schema_draft,
                "yes": yes,
            },
            *args,
        )
    except Exception as exc:
        return f"ERROR: {exc}\n{traceback.format_exc()}"


def _inbox_wrap(fn, *args):
    try:
        from aether_inbox import (
            accept_pocket_offer,
            decline_pocket_offer,
            offer_status,
            stage_upload,
        )
        from aether_pocket import PocketError
    except Exception as exc:
        return f"ERROR: import aether_inbox: {exc}"
    try:
        return fn(
            {
                "PocketError": PocketError,
                "accept_pocket_offer": accept_pocket_offer,
                "decline_pocket_offer": decline_pocket_offer,
                "offer_status": offer_status,
                "stage_upload": stage_upload,
            },
            *args,
        )
    except Exception as exc:
        return f"ERROR: {exc}\n{traceback.format_exc()}"


def bind_status(path: str) -> str:
    def inner(m, p):
        root = m["refuse_if_operator"](p)
        return f"This folder is bound. {root}"

    return _wrap(inner, path)


def face_state(path: str) -> str:
    return _wrap(lambda m, p: m["face_state_json"](p), path)


def bind_folder(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["bind_folder"](p), ensure_ascii=False), path)


def current_text(path: str) -> str:
    return _wrap(lambda m, p: m["current"](p).text, path)


def plan_text(path: str) -> str:
    def inner(m, p):
        from pathlib import Path

        root = m["refuse_if_operator"](p)
        cf = Path(root) / "CURRENT.md"
        if cf.is_file():
            return cf.read_text(encoding="utf-8")
        return m["current"](p).text

    return _wrap(inner, path)


def validate_text(path: str) -> str:
    return _wrap(lambda m, p: m["current_validate"](p).text, path)


def receipts_text(path: str) -> str:
    def inner(m, p):
        br = m["brief"](p).text
        ev = m["events_tail"](p).text
        dr = m["drift"](p).text
        return f"{br}\n\n--- events ---\n{ev}\n\n--- drift ---\n{dr}"

    return _wrap(inner, path)


def read_propose(path: str) -> str:
    return _wrap(lambda m, p: m["read_propose"](p), path)


def receipt_text(path: str) -> str:
    return _wrap(lambda m, p: m["read_receipt"](p) or "(no receipt yet)", path)


def save_propose(path: str, text: str) -> str:
    return _wrap(lambda m, p, t: m["write_propose"](p, t).text, path, text)


def yes(path: str, reason: str) -> str:
    return _wrap(lambda m, p, r: m["yes"](p, r).text, path, reason)


def not_yet(path: str, reason: str) -> str:
    return _wrap(lambda m, p, r: m["not_yet"](p, r).text, path, reason)


def agent_edit(path: str, host: str) -> str:
    return _wrap(
        lambda m, p, h: m["agent_edit_propose"](p, ollama_host=h).text,
        path,
        host,
    )


def schema_fields(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["schema_fields"](p), ensure_ascii=False), path)


def read_schema_draft(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["read_schema_draft"](p), ensure_ascii=False), path)


def write_schema_draft(path: str, fields_json: str) -> str:
    def inner(m, p, fj):
        fields = json.loads(fj) if fj else {}
        r = m["write_schema_draft"](p, fields)
        return json.dumps(
            {"ok": r.ok, "code": r.code, "text": r.text, "extra": r.extra},
            ensure_ascii=False,
        )

    return _wrap(inner, path, fields_json)


def project_shortcuts(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["project_shortcuts"](p), ensure_ascii=False), path)


def chat_history(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["chat_history"](p), ensure_ascii=False), path)


def draft_chat(path: str, host: str, message: str, focus: str = "") -> str:
    return _wrap(
        lambda m, p, h, msg, f: json.dumps(
            m["draft_chat"](p, h, msg, focus=f),
            ensure_ascii=False,
        ),
        path,
        host,
        message,
        focus,
    )


def list_hunks(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["list_hunks"](p), ensure_ascii=False), path)


def apply_hunk(path: str, heading: str, replacement: str) -> str:
    def inner(m, p, h, r):
        out = m["apply_hunk"](p, h, r)
        return json.dumps({"ok": out.ok, "text": out.text}, ensure_ascii=False)

    return _wrap(inner, path, heading, replacement)


def reject_hunk(path: str, heading: str) -> str:
    def inner(m, p, h):
        out = m["reject_hunk"](p, h)
        return json.dumps({"ok": out.ok, "text": out.text}, ensure_ascii=False)

    return _wrap(inner, path, heading)


def accept_hunk(path: str, heading: str) -> str:
    def inner(m, p, h):
        out = m["accept_hunk"](p, h)
        return json.dumps({"ok": out.ok, "text": out.text}, ensure_ascii=False)

    return _wrap(inner, path, heading)


def join_status(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["join_status"](p), ensure_ascii=False), path)


def join_accept(path: str, pasted: str) -> str:
    return _wrap(
        lambda m, p, t: json.dumps(m["join_accept"](p, t), ensure_ascii=False),
        path,
        pasted,
    )


def wake_desk(path: str, url: str = "") -> str:
    return _wrap(
        lambda m, p, u: json.dumps(m["wake_desk"](p, u), ensure_ascii=False),
        path,
        url,
    )


def clear_chat(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["clear_chat"](p), ensure_ascii=False), path)


def events_text(path: str) -> str:
    return _wrap(lambda m, p: m["events_tail"](p).text, path)


def read_shortcut(path: str, name: str) -> str:
    return _wrap(lambda m, p, n: m["read_shortcut"](p, n) or "", path, name)


def gate_state(path: str) -> str:
    return _wrap(lambda m, p: json.dumps(m["gate_state"](p), ensure_ascii=False), path)


def desk_probe(path: str, host: str = "") -> str:
    return _wrap(
        lambda m, p, h: json.dumps(m["desk_probe"](p, h), ensure_ascii=False),
        path,
        host,
    )


def offer_status(path: str) -> str:
    return _inbox_wrap(lambda m, p: json.dumps(m["offer_status"](p), ensure_ascii=False), path)


def accept_offer(path: str) -> str:
    return _inbox_wrap(
        lambda m, p: json.dumps(m["accept_pocket_offer"](p), ensure_ascii=False), path
    )


def decline_offer(path: str) -> str:
    return _inbox_wrap(
        lambda m, p: json.dumps(m["decline_pocket_offer"](p), ensure_ascii=False), path
    )


def stage_upload(path: str) -> str:
    return _inbox_wrap(lambda m, p: json.dumps(m["stage_upload"](p), ensure_ascii=False), path)
