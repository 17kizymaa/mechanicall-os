#!/usr/bin/env python3
"""Read-twin is GET-only. Never Yes. Never the operator tree."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_pocket import PocketError, write_propose  # noqa: E402
from aether_twin import FILES, TwinHandler, bind_host  # noqa: E402


class TestTwin(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pocket = Path(self.tmp.name)
        (self.pocket / "CURRENT.md").write_text("# CURRENT\n**Next:** twin-test\n", encoding="utf-8")
        write_propose(self.pocket, "# propose\n")
        os.environ["TWIN_POCKET"] = str(self.pocket)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), TwinHandler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.tmp.cleanup()

    def _get(self, path: str) -> tuple[int, str]:
        url = f"http://127.0.0.1:{self.port}{path}"
        try:
            with urlopen(url, timeout=2) as resp:
                return getattr(resp, "status", 200), resp.read().decode("utf-8")
        except HTTPError as exc:
            return exc.code, exc.read().decode("utf-8")

    def test_get_current(self) -> None:
        code, body = self._get("/current")
        self.assertEqual(code, 200)
        self.assertIn("twin-test", body)

    def test_post_refused(self) -> None:
        req = Request(f"http://127.0.0.1:{self.port}/current", data=b"yes", method="POST")
        with self.assertRaises(HTTPError) as ctx:
            urlopen(req, timeout=2)
        self.assertEqual(ctx.exception.code, 405)

    def test_routes_cover_law_files(self) -> None:
        names = {rel for _, rel in FILES}
        self.assertIn("CURRENT.md", names)
        self.assertIn("PROPOSE-CURRENT.md", names)
        self.assertIn(".aether/events.jsonl", names)

    def test_refuse_public_bind(self) -> None:
        with self.assertRaises(PocketError):
            bind_host("0.0.0.0")

    def test_refuse_operator_pocket(self) -> None:
        os.environ["TWIN_POCKET"] = str(ROOT)
        code, body = self._get("/current")
        self.assertEqual(code, 403)
        self.assertIn("operator", body.lower())


if __name__ == "__main__":
    unittest.main()
