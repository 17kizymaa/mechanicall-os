#!/usr/bin/env python3
"""Lab folder send/receive — mechanicall-os/inbox, not Headscale-as-Drive.

Not Yes. Not Decide. Not CURRENT of mechanicall-os.

Steal: AirDrop / Nearby Share / Taildrop / DownloadManager progress —
offer → notify → Accept/Decline. GATE shows upload/download percent.
Upload (sitter → operator) lands under inbox/sitters/<id>/ (gitignored).
Download (operator → sitter) stages under inbox/outbox/<id>/ and is an
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
import stat
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
        return Path(repo).expanduser().resolve() / "inbox"
    return Path(__file__).resolve().parent.parent / "inbox"


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
        note="Staged upload. Operator copies into inbox/sitters/.",
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


def write_pocket_transfer(
    pocket: str | Path,
    direction: str,
    percent: int,
    note: str = "",
) -> dict:
    """Honest GATE percent. Not Yes. Empty pocket is a no-op."""
    payload = {
        "direction": direction if direction in {"up", "down"} else "",
        "percent": max(0, min(100, int(percent))),
        "note": note,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "not_yes": True,
    }
    if not str(pocket).strip():
        return payload
    try:
        root = refuse_if_operator(pocket)
    except PocketError:
        return payload
    dest = root / ".aether"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "transfer.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


class _ProgressReader(io.RawIOBase):
    """File-like zip body that reports GATE percent while POSTing."""

    def __init__(self, data: bytes, on_progress) -> None:
        self._buf = io.BytesIO(data)
        self._total = len(data)
        self._got = 0
        self._on = on_progress

    def readable(self) -> bool:
        return True

    def __len__(self) -> int:
        return self._total

    def read(self, n: int = -1) -> bytes:  # noqa: A003
        chunk = self._buf.read(n)
        self._got += len(chunk)
        if self._total and self._on:
            pct = 40 + int(55 * self._got / self._total)
            self._on(min(95, pct))
        return chunk


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


def _zip_member_unsafe(info: zipfile.ZipInfo) -> bool:
    """True if this member must not be written (zip-slip / special / abs)."""
    raw = info.filename or ""
    if not raw or "\x00" in raw:
        return True
    if raw.startswith(("/", "\\")):
        return True
    if "\\" in raw:
        return True
    if len(raw) >= 2 and raw[1] == ":" and raw[0].isalpha():
        return True
    name = Path(raw)
    if name.is_absolute() or name.anchor:
        return True
    if any(part in {"..", ""} for part in name.parts):
        return True
    if info.create_system == 3:
        mode = (info.external_attr >> 16) & 0xFFFF
        ftype = stat.S_IFMT(mode) if mode else 0
        if ftype and ftype not in {stat.S_IFREG, stat.S_IFDIR}:
            return True
    return False


def _zip_target(dest_res: Path, info: zipfile.ZipInfo) -> Path:
    """Resolved path under dest_res, or PocketError if it would escape."""
    if _zip_member_unsafe(info):
        raise PocketError("refused: zip member escapes offer directory")
    rel = Path(info.filename)
    target = dest_res.joinpath(*rel.parts)
    try:
        resolved = target.resolve()
        resolved.relative_to(dest_res)
    except ValueError as exc:
        raise PocketError("refused: zip member escapes offer directory") from exc
    dest_s = str(dest_res)
    norm = os.path.normpath(str(dest_res.joinpath(*rel.parts)))
    if not (norm == dest_s or norm.startswith(dest_s + os.sep)):
        raise PocketError("refused: zip member escapes offer directory")
    return target


def _unzip_to(blob: bytes, dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    dest_res = dest.resolve()
    n = 0
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        planned: list[tuple[zipfile.ZipInfo, Path]] = []
        for info in zf.infolist():
            if info.is_dir() or str(info.filename).endswith("/"):
                continue
            name = Path(info.filename)
            if name.name in SKIP or name.name == "NOTICE.json":
                continue
            planned.append((info, _zip_target(dest_res, info)))
        for info, target in planned:
            if target.exists() and (target.is_symlink() or not target.is_file()):
                raise PocketError("refused: zip member collides with non-file")
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.parent.resolve() != dest_res:
                try:
                    target.parent.resolve().relative_to(dest_res)
                except ValueError as exc:
                    raise PocketError("refused: zip member escapes offer directory") from exc
            with zf.open(info) as src, target.open("wb") as out:
                out.write(src.read())
            if target.is_symlink():
                target.unlink()
                raise PocketError("refused: zip member resolved as symlink")
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
    write_pocket_transfer(pocket, "up", 5, "staging")
    staged = stage_upload(pocket)
    root = refuse_if_operator(pocket)
    slug = from_id.strip() or root.name or "pocket"
    if not SLUG_RE.match(slug):
        slug = "pocket"
    write_pocket_transfer(pocket, "up", 25, "zip")
    blob = _zip_tree(root)
    write_pocket_transfer(pocket, "up", 40, "post")
    last = "drop quiet"
    for host in drop_hosts():
        url = host.rstrip("/") + "/offer?" + urllib.parse.urlencode(
            {"from": slug, "name": root.name, "files": str(staged.get("files") or 0)}
        )
        try:
            status, body, _hdrs = _drop_request(
                url,
                method="POST",
                data=_ProgressReader(
                    blob,
                    lambda pct: write_pocket_transfer(pocket, "up", pct, "post"),
                ),
                headers={
                    "Content-Type": "application/zip",
                    "Content-Length": str(len(blob)),
                },
                timeout=12,
            )
        except (urllib.error.URLError, TimeoutError, OSError):
            last = "drop quiet"
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
            write_pocket_transfer(pocket, "up", 100, note)
            return staged
        last = "drop quiet"
    staged["note"] = f"Staged locally. {last}."
    staged["drop"] = ""
    staged["from"] = slug
    write_pocket_transfer(pocket, "up", 0, staged["note"])
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
        except (urllib.error.URLError, TimeoutError, OSError):
            last = "drop quiet"
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
        write_pocket_transfer(pocket, "down", 10, "pull")
        try:
            _st, blob, _h = _drop_request(blob_url, timeout=8)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = f"drop blob quiet ({exc})"
            write_pocket_transfer(pocket, "down", 0, last)
            continue
        write_pocket_transfer(pocket, "down", 70, "unpack")
        dest = pocket_offer_dir(root)
        if dest.exists():
            shutil.rmtree(dest)
        try:
            n = _unzip_to(blob, dest)
        except PocketError:
            if dest.exists():
                shutil.rmtree(dest)
            last = "drop zip refused"
            write_pocket_transfer(pocket, "down", 0, last)
            continue
        _notice(
            dest,
            direction="drop-to-sitter",
            kind=str(meta.get("kind") or "folder"),
            files=n,
            sender=str(meta.get("from") or ""),
            id=str(meta.get("id") or ""),
            note="Incoming folder via lab drop.",
        )
        write_pocket_transfer(pocket, "down", 100, "incoming folder")
        return offer_status(root)
    existing["note"] = last
    return existing
