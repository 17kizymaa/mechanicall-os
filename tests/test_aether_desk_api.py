#!/usr/bin/env python3
"""Unit tests for desk_turn + desk API helpers (no live LLM required)."""
from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
from http.client import HTTPConnection
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_desk import (  # noqa: E402
    SYSTEM_HOUSE,
    build_messages,
    desk_turn,
    read_extra_context,
    system_prompt_for,
)
import aether_desk_api as api  # noqa: E402


class TestDeskTurn(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "CURRENT.md").write_text(
            "**Objective:** House TV living-room Desk\n**Next:** talk\n",
            encoding="utf-8",
        )
        lib = self.root / "library"
        lib.mkdir()
        (lib / "movies-index.md").write_text(
            "# Movies\n\n- Big Buck Bunny (2008)\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_empty_message(self) -> None:
        r = desk_turn(self.root, "   ", [], log=False)
        self.assertFalse(r["ok"])
        self.assertEqual(r["error"], "empty")

    def test_house_system_from_current(self) -> None:
        self.assertEqual(system_prompt_for(self.root), SYSTEM_HOUSE)

    def test_extra_context_injected(self) -> None:
        msgs = build_messages(self.root, [{"role": "user", "content": "hi"}])
        self.assertIn("Big Buck Bunny", msgs[0]["content"])
        self.assertIn("movies-index", msgs[0]["content"])

    def test_read_extra(self) -> None:
        text = read_extra_context(self.root)
        self.assertIn("Big Buck Bunny", text)

    def test_desk_turn_calls_chat(self) -> None:
        with mock.patch("aether_desk.chat", return_value="Try Big Buck Bunny.") as mchat:
            with mock.patch("aether_desk.describe_backend", return_value="openrouter:free"):
                with mock.patch("aether_desk.flag_unsafe_model_output", return_value=[]):
                    r = desk_turn(self.root, "something funny", [], log=True)
        self.assertTrue(r["ok"])
        self.assertIn("Bunny", r["reply"])
        mchat.assert_called_once()
        log = self.root / ".aether" / "chat.jsonl"
        self.assertTrue(log.is_file())
        lines = log.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(lines), 2)


class TestDeskApiHttp(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "CURRENT.md").write_text(
            "**Objective:** Quiet bridge test\n",
            encoding="utf-8",
        )
        api.STATE = api.DeskState(self.root, public_url="http://127.0.0.1:9/")
        self.httpd = api.ThreadingHTTPServer(("127.0.0.1", 0), api.Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def test_health_and_empty_chat(self) -> None:
        c = HTTPConnection("127.0.0.1", self.port, timeout=5)
        c.request("GET", "/health")
        resp = c.getresponse()
        body = json.loads(resp.read().decode())
        self.assertEqual(resp.status, 200)
        self.assertTrue(body.get("ok"))
        self.assertEqual(body.get("mode"), "chat-only")
        self.assertIn("project", body)
        self.assertNotIn("root", body)  # no absolute path leak
        self.assertFalse(body.get("transcript_log"))

        c.request(
            "POST",
            "/chat",
            body=json.dumps({"message": "  "}),
            headers={"Content-Type": "application/json"},
        )
        resp = c.getresponse()
        body = json.loads(resp.read().decode())
        self.assertEqual(resp.status, 400)
        self.assertEqual(body.get("error"), "empty")
        c.close()

    def test_html_chat_only(self) -> None:
        c = HTTPConnection("127.0.0.1", self.port, timeout=5)
        c.request("GET", "/")
        resp = c.getresponse()
        html = resp.read().decode()
        self.assertEqual(resp.status, 200)
        self.assertIn("CURRENT.md", html)
        self.assertIn("localStorage", html)
        self.assertIn("hist-modal", html)
        self.assertIn("Conversation", html)
        self.assertNotIn("Open Kodi", html)
        self.assertNotIn("House Remote", html)
        self.assertNotIn("/kodi", html)
        c.close()

    def test_no_action_routes(self) -> None:
        c = HTTPConnection("127.0.0.1", self.port, timeout=5)
        c.request("GET", "/kodi")
        self.assertEqual(c.getresponse().status, 404)
        c.request("GET", "/home")
        self.assertEqual(c.getresponse().status, 404)
        c.request("GET", "/open-on-tv")
        self.assertEqual(c.getresponse().status, 404)
        c.close()

    def test_client_root_ignored(self) -> None:
        """P0: JSON root must not switch Domain."""
        other = Path(self.tmp.name) / "other"
        other.mkdir()
        (other / "CURRENT.md").write_text("**Objective:** LEAKED\n", encoding="utf-8")
        with mock.patch("aether_desk_api.desk_turn") as mturn:
            mturn.return_value = {
                "ok": True,
                "error": "",
                "reply": "hi",
                "flags": [],
                "history": [],
                "backend": "test",
            }
            c = HTTPConnection("127.0.0.1", self.port, timeout=5)
            c.request(
                "POST",
                "/chat",
                body=json.dumps({"message": "hi", "root": str(other)}),
                headers={"Content-Type": "application/json"},
            )
            resp = c.getresponse()
            self.assertEqual(resp.status, 200)
            resp.read()
            c.close()
            args, kwargs = mturn.call_args
            used_root = Path(args[0]).resolve()
            self.assertEqual(used_root, self.root.resolve())
            self.assertNotEqual(used_root, other.resolve())

    def test_body_too_large(self) -> None:
        c = HTTPConnection("127.0.0.1", self.port, timeout=5)
        big = "x" * (300 * 1024)
        payload = json.dumps({"message": big})
        c.request(
            "POST",
            "/chat",
            body=payload,
            headers={
                "Content-Type": "application/json",
                "Content-Length": str(len(payload)),
            },
        )
        resp = c.getresponse()
        body = json.loads(resp.read().decode())
        self.assertEqual(resp.status, 413)
        self.assertEqual(body.get("error"), "body_too_large")
        c.close()


if __name__ == "__main__":
    unittest.main()
