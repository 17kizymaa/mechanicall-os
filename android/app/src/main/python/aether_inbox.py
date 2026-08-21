#!/usr/bin/env python3
"""Depreciated folder send/receive — local inbox, not Headscale-as-Drive.

Not Yes. Not Decide. Not CURRENT of mechanicall-os.

Steal: AirDrop / Nearby Share / Taildrop — offer → notify → Accept/Decline.
Upload (sitter → operator) lands under .inbox/sitters/<id>/ (gitignored).
Download (operator → sitter) stages under .inbox/outbox/<id>/ and is an
*offer* on the phone until they Accept. Accept copies files; it never
writes live CURRENT.md. A folder of a new application is still an offer.

Headscale only carries the bytes (mesh). It does not store the folder.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from aether_pocket import PocketError, is_operator_tree, refuse_if_operator

SLUG_RE = re.compile(r"^[a-zA-Z0-9._-]{1,64}$")
SKIP = {".git", "__pycache__", ".pytest_cache", "tsnet"}


def inbox_root(repo: str | Path | None = None) -> Path:
    env = os.environ.get("MECHANICALL_INBOX_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    if repo:
        return Path(repo).expanduser().resolve() / ".inbox"
    return Path(__file__).resolve().parent.parent / ".inbox"


def _slug(name: str) -> str:
    s = (name or "").strip()
    if not SLUG_RE.match(s):
        raise PocketError("refused: inbox id must be a short hostname-like name")
    return s


def _copy_tree(src: Path, dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    dest_res = dest.resolve()
    n = 0
    for dirpath, dirnames, filenames in os.walk(src):
        here = Path(dirpath).resolve()
        try:
            here.relative_to(dest_res)
            dirnames[:] = []
            continue
        except ValueError:
            pass
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        rel = Path(dirpath).relative_to(src)
        (dest / rel).mkdir(parents=True, exist_ok=True)
        for name in filenames:
            if name in SKIP:
                continue
            shutil.copy2(Path(dirpath) / name, dest / rel / name)
            n += 1
    return n


def _notice(dest: Path, **fields: object) -> None:
    payload = {
        "offered": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "offered",
        "notify": True,
        "not_yes": True,
        **fields,
    }
    (dest / "NOTICE.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def upload_sitter(src: str | Path, sitter_id: str, repo: str | Path | None = None) -> dict:
    """Depreciated: sitter opts in to copy their pocket into this tree's gitignored inbox.

    Source must not be the operator tree. Destination is never live CURRENT.
    """
    root = Path(src).expanduser().resolve()
    if is_operator_tree(root):
        raise PocketError("refused: do not upload the mechanicall-os operator tree")
    slug = _slug(sitter_id)
    dest = inbox_root(repo) / "sitters" / slug
    if dest.exists():
        shutil.rmtree(dest)
    count = _copy_tree(root, dest)
    _notice(
        dest,
        direction="sitter-to-operator",
        sitter=slug,
        files=count,
        note="Inbox copy. Not operator CURRENT. Not Yes.",
    )
    return {"ok": True, "dest": str(dest), "files": count, "notify": True, "not_yes": True}


def offer_outbound(src: str | Path, sitter_id: str, repo: str | Path | None = None, kind: str = "folder") -> dict:
    """Operator stages a folder for the sitter. Phone must Accept. Not Yes."""
    root = Path(src).expanduser().resolve()
    if not root.exists():
        raise PocketError("refused: nothing to offer")
    slug = _slug(sitter_id)
    dest = inbox_root(repo) / "outbox" / slug
    if dest.exists():
        shutil.rmtree(dest)
    count = _copy_tree(root, dest)
    _notice(
        dest,
        direction="operator-to-sitter",
        sitter=slug,
        kind=kind,
        files=count,
        note="Offer only. User Accept copies files. Does not write CURRENT. Not Yes.",
    )
    return {"ok": True, "dest": str(dest), "files": count, "notify": True, "not_yes": True}


def accept_offer(offer: str | Path, dest_pocket: str | Path) -> dict:
    """Sitter Accept. Copies into their bound folder except live CURRENT.md."""
    src = Path(offer).expanduser().resolve()
    dest = refuse_if_operator(dest_pocket)
    notice = src / "NOTICE.json"
    if not notice.is_file():
        raise PocketError("refused: not an inbox offer")
    n = 0
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        rel = Path(dirpath).relative_to(src)
        for name in filenames:
            if name in {"NOTICE.json", "CURRENT.md"}:
                continue
            target = dest / rel / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(Path(dirpath) / name, target)
            n += 1
    data = json.loads(notice.read_text(encoding="utf-8"))
    data["status"] = "accepted"
    notice.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "files": n, "not_yes": True, "current_untouched": True}


def decline_offer(offer: str | Path) -> dict:
    src = Path(offer).expanduser().resolve()
    notice = src / "NOTICE.json"
    if not notice.is_file():
        raise PocketError("refused: not an inbox offer")
    data = json.loads(notice.read_text(encoding="utf-8"))
    data["status"] = "declined"
    notice.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "status": "declined", "not_yes": True}


OFFER_REL = Path(".aether") / "offer"
UPLOAD_REL = Path(".aether") / "upload-stage"


def pocket_offer_dir(pocket: str | Path) -> Path:
    return refuse_if_operator(pocket) / OFFER_REL


def offer_status(pocket: str | Path) -> dict:
    """Incoming offer on the bound pocket. Empty is honest. Not Yes."""
    empty = {
        "status": "none",
        "notify": False,
        "kind": "",
        "note": "",
        "ok": True,
        "not_yes": True,
    }
    if not str(pocket).strip():
        return empty
    root = refuse_if_operator(pocket)
    notice = (root / OFFER_REL / "NOTICE.json")
    if not notice.is_file():
        return empty
    try:
        data = json.loads(notice.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return empty
    st = str(data.get("status") or "offered")
    return {
        "status": st,
        "notify": bool(data.get("notify")) and st == "offered",
        "kind": str(data.get("kind") or "folder"),
        "note": str(data.get("note") or "Incoming folder. Accept is not Yes."),
        "ok": True,
        "not_yes": True,
    }


def accept_pocket_offer(pocket: str | Path) -> dict:
    root = refuse_if_operator(pocket)
    return accept_offer(root / OFFER_REL, root)


def decline_pocket_offer(pocket: str | Path) -> dict:
    root = refuse_if_operator(pocket)
    return decline_offer(root / OFFER_REL)


def stage_upload(pocket: str | Path) -> dict:
    """Depreciated opt-in: stage a copy of the pocket for the operator. Not Yes."""
    root = refuse_if_operator(pocket)
    dest = root / UPLOAD_REL
    if dest.exists():
        shutil.rmtree(dest)
    count = _copy_tree(root, dest)
    notice = dest / "NOTICE.json"
    # copy_tree may have copied CURRENT into the stage; that is a *copy* for the operator inbox
    _notice(
        dest,
        direction="sitter-to-operator",
        files=count,
        note="Staged upload. Operator copies into .inbox/sitters/. Not Yes.",
    )
    return {
        "ok": True,
        "dest": str(dest),
        "files": count,
        "notify": True,
        "not_yes": True,
        "note": "Staged. JOIN/mesh may carry later. Not Yes.",
    }
