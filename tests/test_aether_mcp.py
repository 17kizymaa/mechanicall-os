#!/usr/bin/env python3
"""aether MCP spike — never approve / next; never write CURRENT."""
from __future__ import annotations

import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_mcp import (  # noqa: E402
    FORBIDDEN,
    dispatch_tool,
    handle_rpc,
    resolve_root,
    tool_defs,
)

POCKET_CURRENT = """# CURRENT

**Objective:** Garden bed sitting.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** spike-1
**Next:** name-plants
**Approval:** PENDING

## Keep
- rain barrel

## Reject
- concrete

## Limits
- one afternoon

## Next allowed action
Name the plants.

## Approval condition
Human Yes.

## Prohibited
- automatic-approve
"""


class TestToolSurface(unittest.TestCase):
    def test_only_three_tools(self) -> None:
        names = [t["name"] for t in tool_defs()]
        self.assertEqual(names, ["current", "probe", "propose_write"])

    def test_forbidden_not_listed(self) -> None:
        names = set(t["name"] for t in tool_defs())
        self.assertTrue(FORBIDDEN.isdisjoint(names))


class TestDispatch(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
        aether = ROOT / "aether"
        dest = self.root / "aether"
        dest.write_bytes(aether.read_bytes())
        dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
        self.old_home = os.environ.get("AETHER_HOME")
        os.environ["AETHER_HOME"] = str(ROOT)

    def tearDown(self) -> None:
        if self.old_home is None:
            os.environ.pop("AETHER_HOME", None)
        else:
            os.environ["AETHER_HOME"] = self.old_home
        self.tmp.cleanup()

    def test_refuse_approve_tool(self) -> None:
        out = dispatch_tool(self.root, "approve", {"reason": "nope"})
        self.assertTrue(out["isError"])
        self.assertIn("cannot approve", out["content"][0]["text"])
        self.assertEqual((self.root / "CURRENT.md").read_text(encoding="utf-8"), POCKET_CURRENT)

    def test_refuse_next_tool(self) -> None:
        out = dispatch_tool(self.root, "next", {"action": "name-plants"})
        self.assertTrue(out["isError"])
        self.assertIn("cannot next", out["content"][0]["text"])

    def test_current_reads_pin(self) -> None:
        out = dispatch_tool(self.root, "current", {})
        text = out["content"][0]["text"]
        self.assertIn("name-plants", text)
        self.assertIn("PENDING", text)

    def test_probe_allow_and_refuse(self) -> None:
        allow = dispatch_tool(self.root, "probe", {"action": "name-plants"})
        self.assertIn("ALLOW", allow["content"][0]["text"])
        refuse = dispatch_tool(self.root, "probe", {"action": "concrete-the-yard"})
        self.assertIn("REFUSE", refuse["content"][0]["text"])

    def test_propose_write_not_current(self) -> None:
        out = dispatch_tool(
            self.root,
            "propose_write",
            {"text": "# proposal\n", "name": "CURRENT-proposal-spike.md"},
        )
        self.assertFalse(out["isError"], out)
        dest = self.root / ".aether" / "proposals" / "CURRENT-proposal-spike.md"
        self.assertTrue(dest.is_file())
        self.assertIn("# proposal", dest.read_text(encoding="utf-8"))
        self.assertEqual((self.root / "CURRENT.md").read_text(encoding="utf-8"), POCKET_CURRENT)

    def test_propose_write_refuses_current_name(self) -> None:
        out = dispatch_tool(self.root, "propose_write", {"text": "x", "name": "CURRENT.md"})
        self.assertTrue(out["isError"])
        self.assertFalse((self.root / "CURRENT.md").read_text(encoding="utf-8").startswith("x"))

    def test_propose_write_refuses_path_escape(self) -> None:
        out = dispatch_tool(self.root, "propose_write", {"text": "x", "name": "../CURRENT.md"})
        self.assertTrue(out["isError"])
        self.assertEqual((self.root / "CURRENT.md").read_text(encoding="utf-8"), POCKET_CURRENT)


class TestRpc(unittest.TestCase):
    def test_initialize_and_list(self) -> None:
        root = Path(tempfile.mkdtemp())
        init = handle_rpc(root, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.assertEqual(init["result"]["serverInfo"]["name"], "aether-mcp")
        listed = handle_rpc(root, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = [t["name"] for t in listed["result"]["tools"]]
        self.assertEqual(names, ["current", "probe", "propose_write"])

    def test_tools_call_approve_refused(self) -> None:
        root = Path(tempfile.mkdtemp())
        reply = handle_rpc(
            root,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "approve", "arguments": {}},
            },
        )
        self.assertTrue(reply["result"]["isError"])

    def test_resolve_root_missing(self) -> None:
        from aether_mcp import McpError

        with self.assertRaises(McpError):
            resolve_root("/no/such/mechanicall-mcp-root-test")


if __name__ == "__main__":
    unittest.main()
