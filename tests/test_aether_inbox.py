#!/usr/bin/env python3
"""Inbox offers are not Yes and do not write operator CURRENT."""
from __future__ import annotations

import io
import json
import os
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_inbox import (  # noqa: E402
    _unzip_to,
    accept_offer,
    accept_pocket_offer,
    decline_offer,
    inbox_root,
    offer_outbound,
    offer_status,
    poll_incoming,
    project_preview,
    send_project,
    stage_upload,
    upload_sitter,
    write_pocket_transfer,
)
from aether_pocket import PocketError, gate_state  # noqa: E402


def _zip_bytes(entries: dict[str, bytes], *, symlink: str | None = None) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
        if symlink is not None:
            info = zipfile.ZipInfo(symlink)
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            zf.writestr(info, "/tmp/outside")
    return buf.getvalue()


class TestInbox(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        os.environ["MECHANICALL_INBOX_ROOT"] = str(self.home / "inbox")
        self.pocket = self.home / "pocket"
        self.pocket.mkdir()
        (self.pocket / "CURRENT.md").write_text("# CURRENT\n**Next:** keep-me\n", encoding="utf-8")
        (self.pocket / "notes.md").write_text("hello\n", encoding="utf-8")

    def tearDown(self) -> None:
        os.environ.pop("MECHANICALL_INBOX_ROOT", None)
        self.tmp.cleanup()

    def test_upload_does_not_change_operator_current(self) -> None:
        before = (ROOT / "CURRENT.md").read_text(encoding="utf-8")
        out = upload_sitter(self.pocket, "storm-0", repo=self.home)
        self.assertTrue(out["not_yes"])
        self.assertTrue((self.home / "inbox" / "sitters" / "storm-0" / "NOTICE.json").is_file())
        self.assertEqual((ROOT / "CURRENT.md").read_text(encoding="utf-8"), before)

    def test_refuse_operator_tree_upload(self) -> None:
        with self.assertRaises(PocketError):
            upload_sitter(ROOT, "nope")

    def test_accept_skips_live_current(self) -> None:
        payload = self.home / "payload"
        payload.mkdir()
        (payload / "app.txt").write_text("new application bits\n", encoding="utf-8")
        (payload / "CURRENT.md").write_text("# CURRENT\n**Next:** hijack\n", encoding="utf-8")
        offer_outbound(payload, "storm-0", kind="application")
        dest = self.home / "sitter"
        dest.mkdir()
        (dest / "CURRENT.md").write_text("# CURRENT\n**Next:** keep-me\n", encoding="utf-8")
        offer = self.home / "inbox" / "outbox" / "storm-0"
        r = accept_offer(offer, dest)
        self.assertTrue(r["current_untouched"])
        self.assertEqual((dest / "CURRENT.md").read_text(encoding="utf-8"), "# CURRENT\n**Next:** keep-me\n")
        self.assertIn("new application", (dest / "app.txt").read_text(encoding="utf-8"))

    def test_decline(self) -> None:
        payload = self.home / "payload2"
        payload.mkdir()
        (payload / "x.txt").write_text("x\n", encoding="utf-8")
        offer_outbound(payload, "storm-0")
        offer = self.home / "inbox" / "outbox" / "storm-0"
        r = decline_offer(offer)
        self.assertEqual(r["status"], "declined")
        notice = json.loads((offer / "NOTICE.json").read_text(encoding="utf-8"))
        self.assertEqual(notice["status"], "declined")

    def test_pocket_offer_accept_skips_current(self) -> None:
        offer = self.pocket / ".aether" / "offer"
        offer.mkdir(parents=True)
        (offer / "app.txt").write_text("apk bits\n", encoding="utf-8")
        (offer / "CURRENT.md").write_text("# CURRENT\n**Next:** hijack\n", encoding="utf-8")
        (offer / "NOTICE.json").write_text(
            '{"status":"offered","notify":true,"kind":"application","note":"offer"}\n',
            encoding="utf-8",
        )
        st = offer_status(self.pocket)
        self.assertTrue(st["notify"])
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        r = accept_pocket_offer(self.pocket)
        self.assertTrue(r["current_untouched"])
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        self.assertIn("apk bits", (self.pocket / "app.txt").read_text(encoding="utf-8"))

    def test_stage_upload_is_not_yes(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        r = stage_upload(self.pocket)
        self.assertTrue(r["not_yes"])
        self.assertTrue((self.pocket / ".aether" / "upload-stage" / "NOTICE.json").is_file())
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)

    def test_preview_is_not_yes(self) -> None:
        p = project_preview(self.pocket)
        self.assertTrue(p["not_yes"])
        self.assertGreaterEqual(p["files"], 1)
        self.assertTrue((self.pocket / "CURRENT.md").is_file())

    def test_lab_drop_send_and_receive_skips_current(self) -> None:
        import threading
        from aether_drop import DropHandler, ThreadingHTTPServer

        os.environ["MECHANICALL_INBOX_ROOT"] = str(self.home / "inbox")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), DropHandler)
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        os.environ["MECHANICALL_DROP"] = f"http://127.0.0.1:{port}"
        sender = self.home / "alice"
        sender.mkdir()
        (sender / "CURRENT.md").write_text("# CURRENT\n**Next:** alice-live\n", encoding="utf-8")
        (sender / "brief.md").write_text("alice notes\n", encoding="utf-8")
        receiver = self.home / "bob"
        receiver.mkdir()
        (receiver / "CURRENT.md").write_text("# CURRENT\n**Next:** bob-live\n", encoding="utf-8")
        try:
            sent = send_project(sender, from_id="alice")
            self.assertTrue(sent["not_yes"])
            self.assertTrue(sent.get("drop"))
            got = poll_incoming(receiver, for_id="bob")
            self.assertTrue(got["notify"], got)
            before = (receiver / "CURRENT.md").read_text(encoding="utf-8")
            acc = accept_pocket_offer(receiver)
            self.assertTrue(acc["current_untouched"])
            self.assertEqual((receiver / "CURRENT.md").read_text(encoding="utf-8"), before)
            self.assertIn("alice notes", (receiver / "brief.md").read_text(encoding="utf-8"))
            again = poll_incoming(receiver, for_id="bob")
            self.assertEqual(again.get("status"), "accepted")
            self.assertFalse(again.get("notify"))
            self.assertEqual((receiver / "CURRENT.md").read_text(encoding="utf-8"), before)
        finally:
            httpd.shutdown()
            os.environ.pop("MECHANICALL_DROP", None)

    def test_unzip_nested_file_stays_inside(self) -> None:
        dest = self.home / "safe-offer"
        n = _unzip_to(_zip_bytes({"docs/note.md": b"ok\n", "CURRENT.md": b"# CURRENT\n"}), dest)
        self.assertGreaterEqual(n, 1)
        self.assertTrue((dest / "docs" / "note.md").is_file())
        self.assertIn("ok", (dest / "docs" / "note.md").read_text(encoding="utf-8"))

    def test_unzip_refuses_dotdot(self) -> None:
        dest = self.home / "slip-dotdot"
        outside = self.home / "pwned.txt"
        with self.assertRaises(PocketError):
            _unzip_to(_zip_bytes({"../pwned.txt": b"no\n"}), dest)
        self.assertFalse(outside.exists())

    def test_unzip_refuses_absolute_unix(self) -> None:
        dest = self.home / "slip-abs"
        marker = self.home / "abs-pwned.txt"
        with self.assertRaises(PocketError):
            _unzip_to(_zip_bytes({str(marker): b"no\n"}), dest)
        self.assertFalse(marker.exists())
        with self.assertRaises(PocketError):
            _unzip_to(_zip_bytes({"/etc/mechanicall-pwned": b"no\n"}), dest)

    def test_unzip_refuses_backslash_and_drive(self) -> None:
        dest = self.home / "slip-win"
        with self.assertRaises(PocketError):
            _unzip_to(_zip_bytes({"..\\pwned.txt": b"no\n"}), dest)
        with self.assertRaises(PocketError):
            _unzip_to(_zip_bytes({"C:/Windows/mechanicall-pwned.txt": b"no\n"}), dest)
        self.assertFalse(self.home.joinpath("pwned.txt").exists())

    def test_unzip_refuses_symlink_member(self) -> None:
        dest = self.home / "slip-link"
        with self.assertRaises(PocketError):
            _unzip_to(_zip_bytes({"ok.md": b"x\n"}, symlink="escape"), dest)
        self.assertFalse((dest / "escape").exists())

    def test_poll_malicious_zip_does_not_stage(self) -> None:
        import threading
        from aether_drop import DropHandler, ThreadingHTTPServer

        os.environ["MECHANICALL_INBOX_ROOT"] = str(self.home / "inbox")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), DropHandler)
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        os.environ["MECHANICALL_DROP"] = f"http://127.0.0.1:{port}"
        drop_root = self.home / "inbox" / "drop"
        drop_root.mkdir(parents=True, exist_ok=True)
        evil = _zip_bytes({"../pwned-poll.txt": b"no\n", "brief.md": b"hi\n"})
        (drop_root / "offer.zip").write_bytes(evil)
        (drop_root / "offer.json").write_text(
            json.dumps(
                {
                    "id": "evil",
                    "from": "mallory",
                    "name": "mallory",
                    "present": True,
                    "files": 2,
                    "kind": "folder",
                    "status": "offered",
                    "not_yes": True,
                }
            ),
            encoding="utf-8",
        )
        receiver = self.home / "victim"
        receiver.mkdir()
        (receiver / "CURRENT.md").write_text("# CURRENT\n**Next:** keep\n", encoding="utf-8")
        try:
            got = poll_incoming(receiver, for_id="victim")
            self.assertFalse(got.get("notify"), got)
            self.assertFalse((self.home / "pwned-poll.txt").exists())
            self.assertFalse((receiver / ".aether" / "offer").exists())
            self.assertEqual(
                (receiver / "CURRENT.md").read_text(encoding="utf-8"),
                "# CURRENT\n**Next:** keep\n",
            )
        finally:
            httpd.shutdown()
            os.environ.pop("MECHANICALL_DROP", None)

    def test_inbox_root_defaults_to_repo_inbox(self) -> None:
        os.environ.pop("MECHANICALL_INBOX_ROOT", None)
        self.assertEqual(inbox_root(), ROOT / "inbox")
        self.assertEqual(inbox_root(self.home), self.home / "inbox")
        os.environ["MECHANICALL_INBOX_ROOT"] = str(self.home / "inbox")

    def test_gate_state_shows_transfer_percent(self) -> None:
        write_pocket_transfer(self.pocket, "up", 47, "post")
        g = gate_state(self.pocket)
        self.assertEqual(g["direction"], "up")
        self.assertEqual(g["percent"], 47)
        self.assertEqual(g["state"], "idle")

    def test_lab_drop_lands_in_inbox_sitters(self) -> None:
        import threading
        from aether_drop import DropHandler, ThreadingHTTPServer

        os.environ["MECHANICALL_INBOX_ROOT"] = str(self.home / "inbox")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), DropHandler)
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        os.environ["MECHANICALL_DROP"] = f"http://127.0.0.1:{port}"
        sender = self.home / "carol"
        sender.mkdir()
        (sender / "CURRENT.md").write_text("# CURRENT\n**Next:** carol-live\n", encoding="utf-8")
        (sender / "brief.md").write_text("carol notes\n", encoding="utf-8")
        before = (ROOT / "CURRENT.md").read_text(encoding="utf-8")
        try:
            sent = send_project(sender, from_id="carol")
            self.assertTrue(sent["not_yes"])
            self.assertTrue(sent.get("drop"))
            landed = self.home / "inbox" / "sitters" / "carol" / "brief.md"
            self.assertTrue(landed.is_file(), landed)
            self.assertIn("carol notes", landed.read_text(encoding="utf-8"))
            notice = self.home / "inbox" / "sitters" / "carol" / "NOTICE.json"
            self.assertTrue(notice.is_file())
            prog = self.home / "inbox" / "drop" / "progress.json"
            self.assertTrue(prog.is_file())
            data = json.loads(prog.read_text(encoding="utf-8"))
            self.assertEqual(data.get("percent"), 100)
            self.assertEqual((ROOT / "CURRENT.md").read_text(encoding="utf-8"), before)
            g = gate_state(sender)
            self.assertEqual(g["direction"], "up")
            self.assertEqual(g["percent"], 100)
        finally:
            httpd.shutdown()
            os.environ.pop("MECHANICALL_DROP", None)


if __name__ == "__main__":
    unittest.main()
