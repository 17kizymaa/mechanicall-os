#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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

from aether_pocket import write_propose, yes  # noqa: E402
from aether_pocket_serve import Handler, page  # noqa: E402
from test_aether_pocket import POCKET_CURRENT, POCKET_PROPOSE  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestFace(unittest.TestCase):
    def test_page_is_post_yes_and_escapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "CURRENT.md").write_text(
                "# CURRENT\n\n**Objective:** x\n**Phase:** SELECT\n"
                "**Status:** DRAFT\n**Next:** n\n**Approval:** PENDING\n\n"
                "## Keep\n- a\n\n## Reject\n- b\n\n## Limits\n- c\n\n"
                "## Next allowed action\nHi.\n\n## Approval condition\nYes.\n\n"
                "## Prohibited\n- automatic-approve\n",
                encoding="utf-8",
            )
            (p / "PROPOSE-CURRENT.md").write_text("<script>alert(1)</script>", encoding="utf-8")
            os.environ["AETHER_HOME"] = str(ROOT)
            html = page(p).decode("utf-8")
        self.assertIn('method="post" action="/yes"', html)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("GET never Yes", html)
        self.assertIn("You have not said yes yet", html)
        self.assertNotIn("aether", html.lower())

    def test_refuse_operator_page(self) -> None:
        from aether_pocket import PocketError, refuse_if_operator

        with self.assertRaises(PocketError):
            refuse_if_operator(ROOT)


class TestFaceHttp(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["AETHER_HOME"] = str(ROOT)
        os.environ["POCKET_SYNC"] = "0"
        self.tmp = tempfile.TemporaryDirectory()
        self.pocket = Path(self.tmp.name)
        (self.pocket / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
        write_propose(self.pocket, POCKET_PROPOSE)
        Handler.twin = self.pocket
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def _url(self, path: str) -> str:
        return f"http://127.0.0.1:{self.port}{path}"

    def test_get_is_not_yes(self) -> None:
        before = _sha(self.pocket / "CURRENT.md")
        with urlopen(self._url("/")) as resp:
            body = resp.read().decode("utf-8")
            self.assertEqual(resp.status, 200)
        self.assertIn("You have not said yes yet", body)
        self.assertEqual(_sha(self.pocket / "CURRENT.md"), before)
        with self.assertRaises(HTTPError) as ctx:
            urlopen(self._url("/yes"))
        self.assertEqual(ctx.exception.code, 404)
        self.assertEqual(_sha(self.pocket / "CURRENT.md"), before)

    def test_post_yes_writes_receipt(self) -> None:
        req = Request(self._url("/yes"), data=b"", method="POST")
        with urlopen(req) as resp:
            # 303 follow may land on GET /
            self.assertIn(resp.status, (200, 303))
        rec = (self.pocket / "RECEIPT.md").read_text(encoding="utf-8")
        self.assertIn("You said Yes", rec)
        self.assertIn("buy-starts", rec)
        fields = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("**Approval:** APPROVED", fields)

    def test_post_not_yet_receipt(self) -> None:
        req = Request(self._url("/not-yet"), data=b"", method="POST")
        with urlopen(req) as resp:
            self.assertIn(resp.status, (200, 303))
        rec = (self.pocket / "RECEIPT.md").read_text(encoding="utf-8")
        self.assertIn("You said Not yet", rec)
        self.assertIn("name-plants", rec)
        self.assertIn("**Status:** REJECTED", (self.pocket / "CURRENT.md").read_text(encoding="utf-8"))


class TestYesHelperStillReceipts(unittest.TestCase):
    def test_direct_yes_receipt(self) -> None:
        os.environ["AETHER_HOME"] = str(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
            write_propose(p, POCKET_PROPOSE)
            r = yes(p, reason="direct")
            self.assertTrue(r.ok, r.text)
            self.assertTrue((p / "RECEIPT.md").is_file())


if __name__ == "__main__":
    unittest.main()
