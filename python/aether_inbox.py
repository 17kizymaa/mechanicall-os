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

import io
import json
import os
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from aether_pocket import PocketError, is_operator_tree, refuse_if_operator

DROP_DEFAULTS = (
    "http://10.0.2.2:8765",
    "http://127.0.0.1:8765",
    "http://192.168.0.51:8765",
)
DROP_MAX = 8 * 1024 * 1024

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
        note="Inbox copy. Not operator CURRENT.",
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
        note="Offer only. User Accept copies files. Does not write CURRENT.",
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
        "note": str(data.get("note") or "Incoming folder."),
        "id": str(data.get("id") or data.get("offered") or ""),
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
        note="Staged upload. Operator copies into .inbox/sitters/.",
    )
    return {
        "ok": True,
        "dest": str(dest),
        "files": count,
        "notify": True,
        "not_yes": True,
        "note": "Staged. JOIN/mesh may carry later.",
    }


def project_preview(pocket: str | Path) -> dict:
    """What SEND FOLDER would offer. Not Yes. Does not copy."""
    root = refuse_if_operator(pocket)
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        rel = Path(dirpath).relative_to(root)
        if rel.parts[:1] in {(".aether",), (".inbox",)}:
            continue
        n += len(filenames)
    return {
        "ok": True,
        "name": root.name,
        "path": str(root),
        "files": n,
        "not_yes": True,
        "note": "Project in the works.",
    }


def drop_hosts() -> list[str]:
    env = (os.environ.get("MECHANICALL_DROP") or "").strip()
    if env:
        return [p.strip().rstrip("/") for p in env.split(",") if p.strip()]
    return list(DROP_DEFAULTS)


def _zip_tree(src: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(src):
            dirnames[:] = [d for d in dirnames if d not in SKIP]
            for name in filenames:
                if name in SKIP:
                    continue
                path = Path(dirpath) / name
                rel = path.relative_to(src)
                if rel.parts[:1] == (".aether",) and rel.parts[1:2] in {("upload-stage",), ("offer",)}:
                    continue
                zf.write(path, str(rel))
    data = buf.getvalue()
    if len(data) > DROP_MAX:
        raise PocketError("refused: project too large for demo drop")
    return data


def _unzip_to(blob: bytes, dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = Path(info.filename)
            if name.name in SKIP or name.name == "NOTICE.json":
                continue
            if ".." in name.parts:
                continue
            target = dest / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, target.open("wb") as out:
                out.write(src.read())
            n += 1
    return n


def _drop_request(
    url: str,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict | None = None,
    timeout: float = 3,
):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read(), dict(resp.headers)


def send_project(pocket: str | Path, from_id: str = "") -> dict:
    """Stage + post to the lab drop. Local stage still happens if drop is quiet. Not Yes."""
    staged = stage_upload(pocket)
    root = refuse_if_operator(pocket)
    slug = from_id.strip() or root.name or "pocket"
    if not SLUG_RE.match(slug):
        slug = "pocket"
    blob = _zip_tree(root)
    last = "drop quiet"
    for host in drop_hosts():
        url = host.rstrip("/") + "/offer?" + urllib.parse.urlencode(
            {"from": slug, "name": root.name, "files": str(staged.get("files") or 0)}
        )
        try:
            status, body, _hdrs = _drop_request(
                url,
                method="POST",
                data=blob,
                headers={"Content-Type": "application/zip"},
                timeout=6,
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = f"drop quiet ({exc})"
            continue
        if status and status < 300:
            note = "In the works. Other seat can receive."
            try:
                payload = json.loads(body.decode("utf-8"))
                note = str(payload.get("note") or note)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
            staged["note"] = note
            staged["drop"] = host
            staged["from"] = slug
            return staged
        last = f"drop refused HTTP {status}"
    staged["note"] = f"Staged locally. {last}."
    staged["drop"] = ""
    staged["from"] = slug
    return staged


def poll_incoming(pocket: str | Path, for_id: str = "") -> dict:
    """Pull a lab-drop offer into .aether/offer. Does not Accept. Not Yes."""
    existing = offer_status(pocket)
    if existing.get("status") == "offered":
        return existing
    root = refuse_if_operator(pocket)
    slug = for_id.strip() or root.name or "pocket"
    last = "drop quiet"
    for host in drop_hosts()[:1]:
        meta_url = host.rstrip("/") + "/offer.json?" + urllib.parse.urlencode({"not": slug})
        try:
            status, body, _hdrs = _drop_request(meta_url, timeout=1.2)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = f"drop quiet ({exc})"
            continue
        if status == 204 or not body:
            last = "no offer"
            continue
        try:
            meta = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            last = "drop garbled"
            continue
        if not meta.get("present"):
            last = "no offer"
            continue
        if str(meta.get("from") or "") == slug:
            last = "own offer"
            continue
        meta_id = str(meta.get("id") or "")
        stored_id = str(existing.get("id") or "")
        if existing.get("status") in {"accepted", "declined"}:
            if not stored_id or stored_id == meta_id:
                return existing
        blob_url = host.rstrip("/") + "/offer.zip"
        try:
            _st, blob, _h = _drop_request(blob_url, timeout=4)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = f"drop blob quiet ({exc})"
            continue
        dest = pocket_offer_dir(root)
        if dest.exists():
            shutil.rmtree(dest)
        n = _unzip_to(blob, dest)
        _notice(
            dest,
            direction="drop-to-sitter",
            kind=str(meta.get("kind") or "folder"),
            files=n,
            sender=str(meta.get("from") or ""),
            id=str(meta.get("id") or ""),
            note="Incoming folder via lab drop.",
        )
        return offer_status(root)
    existing["note"] = last
    return existing
