#!/usr/bin/env python3
"""Pocket demo engine — never touches the operator CURRENT."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_pocket import (  # noqa: E402
    PocketError,
    accept_hunk,
    apply_hunk,
    apply_propose,
    bind_folder,
    chat_history,
    current,
    current_validate,
    chat_stage,
    clear_chat,
    draft_chat,
    events_tail,
    walk_stage,
    read_shortcut,
    desk_probe,
    enqueue_desk,
    gate_state,
    list_desk_queue,
    tsnet_up,
    write_gate,
    face_state,
    is_operator_tree,
    join_accept,
    join_status,
    list_hunks,
    not_yet,
    parse_fields,
    project_shortcuts,
    projection,
    read_propose,
    read_schema_draft,
    refuse_if_operator,
    reject_hunk,
    schema_fields,
    wake_desk,
    write_propose,
    write_schema_draft,
    yes,
    read_receipt,
)

POCKET_CURRENT = """# CURRENT

**Objective:** Plan a small garden bed with the client.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** sitting-1
**Next:** name-plants
**Approval:** PENDING

## Keep
- rain barrel

## Reject
- concrete the yard

## Limits
- one afternoon

## Next allowed action
Name the plants.

## Approval condition
Human Yes on the phone.

## Prohibited
- automatic-approve
- model-auto-approve
"""

POCKET_PROPOSE = """# Proposed CURRENT update (draft — not authority)

## Observations
- Client wants herbs.

## Inferences
- Next should be buy-starts.

## Unknowns
- Sun hours.

## Proposed CURRENT change

```markdown
**Objective:** Plant a herb bed the client can water from the rain barrel.
**Phase:** APPROVE
**Status:** APPROVED
**Next:** buy-starts
**Approval:** PENDING
```

## Conflicts with existing authority
- Next is currently name-plants.

## Human decision required
- [ ] Apply
"""


def _tags_ok():
    from unittest.mock import MagicMock

    resp = MagicMock()
    resp.status = 200
    resp.read.return_value = b'{"models":[]}'
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    return resp


def _stream_ok(payload: str):
    import json
    from unittest.mock import MagicMock

    lines = [
        (json.dumps({"response": payload, "done": False}) + "\n").encode(),
        (json.dumps({"response": "", "done": True}) + "\n").encode(),
        b"",
    ]
    resp = MagicMock()
    resp.status = 200
    resp.readline.side_effect = lines
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    return resp


def _fake_desk(payload: str, down_hosts: tuple[str, ...] = ()):
    import urllib.error

    def fake_urlopen(req, timeout=0):  # noqa: ARG001
        url = getattr(req, "full_url", "") or ""
        if any(h in url for h in down_hosts):
            raise urllib.error.URLError("refused")
        if "/api/tags" in url:
            return _tags_ok()
        return _stream_ok(payload)

    return fake_urlopen


class TestRefuseOperator(unittest.TestCase):
    def test_operator_tree_detected(self) -> None:
        self.assertTrue(is_operator_tree(ROOT))

    def test_refuse_operator_bind(self) -> None:
        with self.assertRaises(PocketError) as ctx:
            refuse_if_operator(ROOT)
        self.assertIn("operator tree", str(ctx.exception))

    def test_plain_folder_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            self.assertFalse(is_operator_tree(p))
            self.assertEqual(refuse_if_operator(p), p.resolve())


class TestPocketAether(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pocket = Path(self.tmp.name)
        (self.pocket / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
        write_propose(self.pocket, POCKET_PROPOSE)
        os.environ["AETHER_HOME"] = str(ROOT)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_current_and_validate(self) -> None:
        cur = current(self.pocket)
        self.assertTrue(cur.ok, cur.text)
        self.assertIn("name-plants", cur.text)
        val = current_validate(self.pocket)
        self.assertTrue(val.ok, val.text)
        self.assertIn("VALIDATE: OK", val.text)

    def test_projection_payload(self) -> None:
        payload = projection(self.pocket)
        self.assertEqual(payload["fields"]["Next"], "name-plants")
        self.assertIn("buy-starts", payload["propose"])
        self.assertTrue(payload["validate_ok"])

    def test_editor_save_does_not_touch_current(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        write_propose(self.pocket, POCKET_PROPOSE + "\n\n# note\n")
        after = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertIn("# note", read_propose(self.pocket))

    def test_apply_propose_fields_only(self) -> None:
        r = apply_propose(self.pocket)
        self.assertTrue(r.ok)
        fields = parse_fields((self.pocket / "CURRENT.md").read_text(encoding="utf-8"))
        self.assertEqual(fields["Next"], "buy-starts")
        self.assertIn("herb bed", fields["Objective"])
        # sections from original CURRENT remain
        body = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("## Keep", body)
        self.assertIn("rain barrel", body)

    def test_yes_approve_matches_cli_shape(self) -> None:
        r = yes(self.pocket, reason="client said yes")
        self.assertTrue(r.ok, r.text)
        self.assertIn("APPROVED", r.text)
        ev = events_tail(self.pocket, n=20)
        self.assertIn("approve", ev.text)
        self.assertIn("client said yes", ev.text)
        fields = parse_fields((self.pocket / "CURRENT.md").read_text(encoding="utf-8"))
        self.assertEqual(fields["Approval"], "APPROVED")
        self.assertEqual(fields["Status"], "APPROVED")
        self.assertEqual(fields["Next"], "buy-starts")
        decisions = (self.pocket / "DECISIONS.md").read_text(encoding="utf-8")
        self.assertIn("APPROVED: client said yes", decisions)
        rec = read_receipt(self.pocket)
        self.assertIn("You said Yes", rec)
        self.assertIn("buy-starts", rec)

    def test_not_yet_select(self) -> None:
        r = not_yet(self.pocket, reason="hold")
        self.assertTrue(r.ok, r.text)
        fields = parse_fields((self.pocket / "CURRENT.md").read_text(encoding="utf-8"))
        self.assertEqual(fields["Phase"], "SELECT")
        self.assertEqual(fields["Status"], "REJECTED")
        # Next unchanged on reject
        self.assertEqual(fields["Next"], "name-plants")
        rec = read_receipt(self.pocket)
        self.assertIn("You said Not yet", rec)
        self.assertIn("did not pretend you agreed", rec)

    def test_yes_refuses_operator(self) -> None:
        with self.assertRaises(PocketError):
            yes(ROOT, reason="no")

    def test_face_state_fields_open_is_not_yes(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        st = face_state(self.pocket)
        after = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertTrue(st["ok"])
        self.assertTrue(st["bound"])
        self.assertFalse(st["refused"])
        self.assertFalse(st["open_is_yes"])
        self.assertTrue(st["has_current"])
        self.assertEqual(st["next"], "name-plants")
        self.assertIn("garden bed", st["objective"])
        self.assertIn("buy-starts", st["propose"])
        self.assertEqual(st["said"], "")

    def test_face_state_said_from_receipt(self) -> None:
        not_yet(self.pocket, reason="hold")
        st = face_state(self.pocket)
        self.assertEqual(st["said"], "Not yet")
        self.assertIn("You said Not yet", st["receipt"])


class TestFaceStateBind(unittest.TestCase):
    def test_face_state_refuses_operator_without_raising(self) -> None:
        st = face_state(ROOT)
        self.assertTrue(st["refused"])
        self.assertFalse(st["bound"])
        self.assertFalse(st["ok"])
        self.assertFalse(st["open_is_yes"])
        self.assertIn("operator tree", st["message"])
        self.assertEqual(st["plan_text"], "")
        self.assertEqual(st["next"], "")

    def test_face_state_missing_folder(self) -> None:
        missing = Path("/tmp/mechanicall-pocket-does-not-exist-29")
        if missing.exists():
            self.skipTest("path unexpectedly exists")
        st = face_state(missing)
        self.assertFalse(st["bound"])
        self.assertFalse(st["refused"])
        self.assertFalse(st["open_is_yes"])
        self.assertIn("not on this phone", st["message"])

    def test_face_state_bound_without_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            st = face_state(tmp)
            self.assertTrue(st["bound"])
            self.assertFalse(st["has_current"])
            self.assertFalse(st["open_is_yes"])
            self.assertIn("No plan file yet", st["message"])

    def test_blank_pocket_is_bind_first(self) -> None:
        st = face_state("")
        self.assertFalse(st["bound"])
        self.assertFalse(st["refused"])
        self.assertEqual(st["walk"], "bind")
        self.assertIn("Name your folder", st["message"])
        self.assertEqual(walk_stage(""), "bind")
        self.assertEqual(gate_state("")["state"], "idle")

    def test_bind_folder_one_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            named = Path(tmp) / "afternoon"
            self.assertFalse(named.exists())
            st = bind_folder(named)
            self.assertTrue(named.is_dir())
            self.assertTrue(st["bound"])
            self.assertFalse(st["refused"])
            self.assertEqual(st["walk"], "plan")
        refused = bind_folder(ROOT)
        self.assertTrue(refused["refused"])
        self.assertFalse(refused["bound"])
        blank = bind_folder("")
        self.assertFalse(blank["bound"])
        self.assertIn("Name your folder", blank["message"])

    def test_desk_probe_blank_does_not_raise(self) -> None:
        from unittest.mock import patch

        with patch("aether_pocket._desk_alive", return_value=False):
            out = desk_probe("", "http://127.0.0.1:11434")
        self.assertFalse(out["ok"])
        self.assertEqual(out["state"], "quiet")


class TestSchemaDraftChat(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pocket = Path(self.tmp.name)
        (self.pocket / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
        write_propose(self.pocket, POCKET_PROPOSE)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_write_schema_draft_does_not_change_current(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        r = write_schema_draft(
            self.pocket,
            {
                "Next": "buy-soil",
                "Objective": "Plant herbs this weekend.",
                "bogus": "should-not-appear",
            },
        )
        self.assertTrue(r.ok, r.text)
        after = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        propose = read_propose(self.pocket)
        self.assertIn("**Next:** buy-soil", propose)
        self.assertIn("Proposed CURRENT change", propose)
        self.assertNotIn("should-not-appear", propose)
        draft = read_schema_draft(self.pocket)
        self.assertEqual(draft["Next"], "buy-soil")

    def test_face_state_open_is_yes_false(self) -> None:
        st = face_state(self.pocket)
        self.assertFalse(st["open_is_yes"])
        self.assertIn("CURRENT.md", st["shortcuts"])
        self.assertEqual(st["schema"]["Next"], "name-plants")
        self.assertEqual(st["schema_draft"]["Next"], "buy-starts")
        self.assertEqual(st["chat_len"], 0)

    def test_operator_tree_refused(self) -> None:
        with self.assertRaises(PocketError) as ctx:
            write_schema_draft(ROOT, {"Next": "no"})
        self.assertIn("operator tree", str(ctx.exception))
        with self.assertRaises(PocketError):
            schema_fields(ROOT)
        with self.assertRaises(PocketError):
            draft_chat(ROOT, "http://127.0.0.1:11434", "hello")
        with self.assertRaises(PocketError):
            project_shortcuts(ROOT)

    def test_project_shortcuts_lists_current(self) -> None:
        sc = project_shortcuts(self.pocket)
        names = [row["name"] for row in sc]
        self.assertIn("CURRENT.md", names)
        current_row = next(row for row in sc if row["name"] == "CURRENT.md")
        self.assertEqual(current_row["kind"], "current")
        self.assertTrue(Path(current_row["path"]).is_file())
        self.assertIn("PROPOSE-CURRENT.md", names)

    def test_draft_chat_public_bind_fails_without_writing_current(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        propose_before = read_propose(self.pocket)
        with self.assertRaises(PocketError) as ctx:
            draft_chat(self.pocket, "http://0.0.0.0:11434", "please rewrite next")
        self.assertIn("0.0.0.0", str(ctx.exception))
        after = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertEqual(read_propose(self.pocket), propose_before)
        self.assertEqual(chat_history(self.pocket), [])

    def test_draft_chat_writes_propose_not_current(self) -> None:
        from unittest.mock import patch

        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        fake = (
            "# Proposed CURRENT update (draft — not authority)\n\n"
            "## Proposed CURRENT change\n\n"
            "```markdown\n"
            "**Next:** mock-next\n"
            "```\n"
        )
        with patch("aether_pocket.urllib.request.urlopen", side_effect=_fake_desk(fake)):
            out = draft_chat(self.pocket, "http://127.0.0.1:11434", "change next")
        self.assertTrue(out["ok"], out["reply"])
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        self.assertIn("mock-next", read_propose(self.pocket))
        self.assertEqual(out.get("fields", {}).get("Next") or "mock-next", "mock-next")
        hist = chat_history(self.pocket)
        self.assertEqual(hist[0]["role"], "user")
        self.assertEqual(hist[0]["text"], "change next")
        self.assertEqual(hist[-1]["role"], "assistant")
        self.assertLess(len(hist[-1]["text"]), 300)
        self.assertNotIn("# Proposed CURRENT", hist[-1]["text"])

        with patch("aether_pocket.urllib.request.urlopen", side_effect=_fake_desk("x", down_hosts=("127.0.0.1", "192.168.0.51", "100.90.85.68", "myarch"))):
            failed = draft_chat(self.pocket, "http://127.0.0.1:11434", "hello again")
        self.assertFalse(failed["ok"])
        self.assertIn("Desk quiet", failed["reply"])
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        roles_texts = [(row["role"], row["text"]) for row in chat_history(self.pocket)]
        self.assertIn(("user", "hello again"), roles_texts)
        self.assertTrue(
            any(role == "assistant" and "Desk quiet" in text for role, text in roles_texts)
        )

    def test_chat_stage_decision_framework(self) -> None:
        self.assertEqual(chat_stage("yes"), "gate")
        self.assertEqual(chat_stage("please approve this"), "gate")
        self.assertEqual(chat_stage("change next"), "propose")
        self.assertEqual(chat_stage("what is the next step?"), "show-plan")

    def test_show_plan_cannot_write_propose(self) -> None:
        from unittest.mock import patch

        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        propose_before = read_propose(self.pocket)
        fake = (
            '{"say":"Next is name-plants.","stage":"propose",'
            '"fields":{"Next":"stolen-next"}}\n'
        )
        with patch("aether_pocket.urllib.request.urlopen", side_effect=_fake_desk(fake)):
            out = draft_chat(self.pocket, "http://127.0.0.1:11434", "what is next?")
        self.assertEqual(out["stage"], "show-plan")
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        self.assertEqual(read_propose(self.pocket), propose_before)
        self.assertEqual(out.get("fields") or {}, {})

    def test_gate_does_not_call_desk(self) -> None:
        from unittest.mock import patch

        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        with patch("aether_pocket.urllib.request.urlopen") as opener:
            out = draft_chat(self.pocket, "http://127.0.0.1:11434", "please approve this")
        opener.assert_not_called()
        self.assertEqual(out["stage"], "gate")
        self.assertIn("Decide", out["reply"])
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)

    def test_chat_prompt_is_slim(self) -> None:
        from unittest.mock import MagicMock, patch

        captured: list[bytes] = []

        def fake_urlopen(req, timeout=0):  # noqa: ARG001
            captured.append(req.data or b"")
            url = getattr(req, "full_url", "") or ""
            if "/api/tags" in url:
                return _tags_ok()
            payload = __import__("json").dumps(
                {
                    "say": "Next is name-plants. Not Yes.",
                    "stage": "show-plan",
                    "fields": {},
                }
            )
            return _stream_ok(payload)

        with patch("aether_pocket.urllib.request.urlopen", side_effect=fake_urlopen):
            out = draft_chat(self.pocket, "http://127.0.0.1:11434", "what is next?")
        self.assertTrue(out["ok"], out["reply"])
        blob = b"".join(captured)
        self.assertNotIn(b"Live CURRENT.md", blob)
        self.assertNotIn(b"Existing PROPOSE-CURRENT.md", blob)
        self.assertIn(b"Plan (fields only", blob)
        self.assertIn(b"name-plants", blob)
        self.assertEqual(out["reply"], "Next is name-plants. Not Yes.")
        self.assertNotIn(b"rain barrel", blob)
        self.assertIn(b"Folder files (names only", blob)
        self.assertIn(b"CURRENT.md", blob)
        self.assertIn(b"Plugin pages", blob)

    def test_walk_stage_and_clear_chat(self) -> None:
        self.assertEqual(walk_stage(self.pocket), "chat")
        st = face_state(self.pocket)
        self.assertEqual(st["walk"], "chat")
        self.assertEqual(st["chat_stage"], "")
        out = draft_chat(self.pocket, "http://127.0.0.1:11434", "please approve this")
        self.assertEqual(out["stage"], "gate")
        hist = chat_history(self.pocket)
        self.assertEqual(hist[-1]["stage"], "gate")
        self.assertEqual(walk_stage(self.pocket), "decide")
        cleared = clear_chat(self.pocket)
        self.assertTrue(cleared["ok"])
        self.assertEqual(chat_history(self.pocket), [])
        self.assertTrue((self.pocket / "CURRENT.md").is_file())
        missing = Path("/tmp/mechanicall-pocket-does-not-exist-33-core")
        if missing.exists():
            self.skipTest("path unexpectedly exists")
        self.assertEqual(walk_stage(missing), "bind")
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(walk_stage(tmp), "plan")

    def test_read_shortcut_stays_in_pocket(self) -> None:
        (self.pocket / "notes.txt").write_text("herb list\n", encoding="utf-8")
        self.assertEqual(read_shortcut(self.pocket, "notes.txt"), "herb list\n")
        names = [row["name"] for row in project_shortcuts(self.pocket)]
        self.assertIn("notes.txt", names)
        with self.assertRaises(PocketError):
            read_shortcut(self.pocket, "../secret")

    def test_desk_tries_next_host(self) -> None:
        from unittest.mock import patch

        payload = __import__("json").dumps(
            {"say": "Next is name-plants.", "stage": "show-plan", "fields": {}}
        )
        with patch(
            "aether_pocket.urllib.request.urlopen",
            side_effect=_fake_desk(payload, down_hosts=("127.0.0.1",)),
        ):
            out = draft_chat(self.pocket, "http://127.0.0.1:11434", "what is next?")
        self.assertTrue(out["ok"], out["reply"])
        self.assertEqual(out["reply"], "Next is name-plants.")
        self.assertIn("myarch", out.get("host", ""))
        g = gate_state(self.pocket)
        self.assertEqual(g["state"], "quiet")
        self.assertGreater(g["step"], 0)

    def test_desk_probe_and_gate_write(self) -> None:
        from unittest.mock import patch

        with patch(
            "aether_pocket.urllib.request.urlopen",
            side_effect=_fake_desk("{}", down_hosts=("127.0.0.1",)),
        ):
            probe = desk_probe(self.pocket)
        self.assertTrue(probe["ok"])
        self.assertIn("myarch", probe["host"])
        g = write_gate(self.pocket, state="gate", step=7, desk="http://127.0.0.1:11434")
        self.assertEqual(g["step"], 7)
        self.assertEqual(gate_state(self.pocket)["state"], "gate")


class TestHunkJoinWake(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pocket = Path(self.tmp.name)
        (self.pocket / "CURRENT.md").write_text(POCKET_CURRENT, encoding="utf-8")
        write_propose(self.pocket, POCKET_PROPOSE)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_apply_hunk_does_not_change_current(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        r = apply_hunk(self.pocket, "Objective", "**Objective:** Plant herbs.\n")
        self.assertTrue(r.ok, r.text)
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        self.assertIn("Plant herbs", read_propose(self.pocket))
        ids = [row["id"] for row in list_hunks(self.pocket)]
        self.assertIn("Objective", ids)

    def test_reject_hunk_restores_live_into_propose(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        apply_hunk(self.pocket, "Keep", "## Keep\n- stolen\n")
        reject_hunk(self.pocket, "Keep")
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        self.assertIn("rain barrel", read_propose(self.pocket))

    def test_join_accept_does_not_store_secret(self) -> None:
        from unittest.mock import patch

        secret = "tskey-auth-NOT-FOR-GIT-ABCDEF123456"
        with patch("aether_pocket._desk_alive", return_value=False):
            st = join_accept(self.pocket, secret)
        self.assertEqual(st["status"], "invited")
        self.assertTrue(st["fp"].startswith("sha256:"))
        blob = (self.pocket / ".aether" / "tailnet.json").read_text(encoding="utf-8")
        self.assertNotIn(secret, blob)
        self.assertNotIn("NOT-FOR-GIT", blob)
        self.assertEqual(join_status(self.pocket)["status"], "invited")

    def test_join_refuses_operator_email(self) -> None:
        with self.assertRaises(PocketError):
            join_accept(self.pocket, "https://login.tailscale.com/invite/17kizymaa")

    def test_wake_refuses_public_url(self) -> None:
        with self.assertRaises(PocketError):
            wake_desk(self.pocket, "http://0.0.0.0:7077/wake")

    def test_draft_chat_focus_writes_hunk_not_current(self) -> None:
        from unittest.mock import patch

        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        fake = '{"say":"Drafted Next.","hunk":"**Next:** buy-soil\\n","schema":{"Next":"buy-soil"}}'
        with patch("aether_pocket.urllib.request.urlopen", side_effect=_fake_desk(fake)):
            out = draft_chat(
                self.pocket,
                "http://127.0.0.1:11434",
                "change this hunk",
                focus="Next",
            )
        self.assertTrue(out["ok"], out["reply"])
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        self.assertIn("buy-soil", read_propose(self.pocket))
        self.assertEqual(out.get("focus"), "Next")

    def test_accept_hunk_is_not_yes(self) -> None:
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        apply_hunk(self.pocket, "Next", "**Next:** later\n")
        accept_hunk(self.pocket, "Next")
        self.assertEqual((self.pocket / "CURRENT.md").read_text(encoding="utf-8"), before)
        fields = parse_fields(before)
        self.assertEqual(fields["Next"], "name-plants")

    def test_join_desk_alive_is_not_connected(self) -> None:
        from unittest.mock import patch

        secret = "hskey-auth-NOT-FOR-GIT-ABCDEF1234567890"
        with patch("aether_pocket._desk_alive", return_value=True):
            st = join_accept(self.pocket, secret)
        self.assertEqual(st["status"], "invited")
        self.assertFalse(st["userspace"])
        blob = (self.pocket / ".aether" / "tailnet.json").read_text(encoding="utf-8")
        self.assertNotIn(secret, blob)

    def test_join_userspace_marker_connects(self) -> None:
        marker = self.pocket / "tsnet-up.json"
        marker.write_text('{"up": true}\n', encoding="utf-8")
        os.environ["MECHANICALL_TSNET_MARKER"] = str(marker)
        os.environ.pop("MECHANICALL_TSNET_UP", None)
        try:
            self.assertTrue(tsnet_up())
            st = join_accept(self.pocket, "hskey-auth-FAKESECRET-marker-aaaaaaaa")
            self.assertEqual(st["status"], "connected")
            self.assertTrue(st["userspace"])
            blob = (self.pocket / ".aether" / "tailnet.json").read_text(encoding="utf-8")
            self.assertNotIn("FAKESECRET", blob)
        finally:
            os.environ.pop("MECHANICALL_TSNET_MARKER", None)

    def test_join_refuses_tailscale_invite(self) -> None:
        with self.assertRaises(PocketError):
            join_accept(self.pocket, "https://login.tailscale.com/invite/someone-else")

    def test_write_gate_load_and_queue(self) -> None:
        g = write_gate(self.pocket, state="load", step=4, desk="http://myarch:11434")
        self.assertEqual(g["state"], "load")
        self.assertEqual(gate_state(self.pocket)["state"], "load")
        write_gate(self.pocket, state="gate", step=3)
        queued = enqueue_desk(self.pocket, "second send", focus="Next")
        self.assertTrue(queued["queued"])
        self.assertEqual(queued["queue"], 1)
        self.assertEqual(len(list_desk_queue(self.pocket)), 1)

    def test_draft_chat_queues_when_busy(self) -> None:
        write_gate(self.pocket, state="gate", step=2, desk="http://myarch:11434")
        out = draft_chat(self.pocket, "http://127.0.0.1:11434", "change this hunk", focus="Next")
        self.assertTrue(out["ok"], out["reply"])
        self.assertTrue(out.get("queued"))
        self.assertIn("Queued", out["reply"])
        before = (self.pocket / "CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("name-plants", before)


if __name__ == "__main__":
    unittest.main()
