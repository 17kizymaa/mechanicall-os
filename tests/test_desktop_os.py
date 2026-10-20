#!/usr/bin/env python3
"""Desktop OS: two apps, paper ticket, CURRENT untouched."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))


class TestDesktopOs(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["MECHANICALL_DESKTOP_VAR"] = self.tmp.name
        import desktop_os as desk

        desk.reset_paths()
        self.desk = desk
        self.current = ROOT / "CURRENT.md"
        self.before = self.current.read_text(encoding="utf-8")
        self.httpd = desk.serve(0)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.assertEqual(self.current.read_text(encoding="utf-8"), self.before)
        self.tmp.cleanup()

    def _get(self, path: str) -> tuple[int, bytes]:
        url = f"http://127.0.0.1:{self.port}{path}"
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def _post(self, path: str, obj: dict) -> dict:
        url = f"http://127.0.0.1:{self.port}{path}"
        req = urllib.request.Request(
            url,
            data=json.dumps(obj).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as r:
            return json.loads(r.read().decode("utf-8"))

    def test_face_is_two_apps_not_ibkr(self) -> None:
        code, raw = self._get("/")
        self.assertEqual(code, 200)
        html = raw.decode("utf-8")
        self.assertIn("Trader", html)
        self.assertIn("Serve", html)
        self.assertNotIn("this-works", html.lower())
        self.assertNotIn("Interactive Brokers", html)
        self.assertIn("not live money", html.lower())

    def test_market_order_via_api(self) -> None:
        st = self._post("/api/order", {"symbol": "BOLT", "side": "BUY", "qty": 4, "type": "MARKET"})
        self.assertTrue(st["not_live"])
        self.assertTrue(st["not_ibkr"])
        self.assertEqual(st["book"]["positions"][0]["qty"], 4)
        self.assertEqual(len(st["apps"]), 2)
        self.assertEqual(st["apps"][0]["id"], "trader")
        self.assertEqual(st["apps"][1]["id"], "serve")

    def test_serve_is_not_yes(self) -> None:
        st = self._post("/api/serve", {"text": "Need milk"})
        texts = " ".join(m["text"] for m in st["serve"]["messages"])
        self.assertIn("Need milk", texts)
        self.assertIn("don't need to stamp", texts)
        self.assertTrue(st["serve"]["not_yes"])
        self.assertNotIn("aether approve", texts.lower())


if __name__ == "__main__":
    unittest.main()
