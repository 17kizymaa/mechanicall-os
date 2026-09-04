#!/usr/bin/env python3
"""wol-wake-listen: tailnet doorbell. Not Yes. No public bind."""
from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "wol_wake_listen", ROOT / "scripts" / "wol-wake-listen.py"
)
assert SPEC and SPEC.loader
wol = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wol)


class WolWakeTests(unittest.TestCase):
    def test_refuses_public_bind(self) -> None:
        for host in ("0.0.0.0", "::", "[::]"):
            with mock.patch.dict(os.environ, {"WOL_BIND": host}, clear=False):
                with self.assertRaises(SystemExit) as ctx:
                    wol._bind()
                self.assertEqual(ctx.exception.code, 2)

    def test_default_bind_is_localhost(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "WOL_BIND"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(wol._bind(), "127.0.0.1")

    def test_magic_packet_length(self) -> None:
        mac = bytes.fromhex("aabbccddeeff")
        pkt = wol._magic(mac)
        self.assertEqual(len(pkt), 6 + 16 * 6)
        self.assertTrue(pkt.startswith(b"\xff" * 6))

    def test_mac_required(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "WOL_MAC"}
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(SystemExit) as ctx:
                wol._mac()
            self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
