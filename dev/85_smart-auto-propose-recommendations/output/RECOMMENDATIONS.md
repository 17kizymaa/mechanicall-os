# Pre-proposal recommendations

**Not a Yes.** No hook. Apply and approve stay human slash commands.

## When a stage is named

Write one file under `.aether/proposals/` in that same stretch of work. The file waits. The human applies it or does not. Nothing in the repo applies it, approves it, or writes `CURRENT.md` by itself.

One file, one Next. The next named stage gets its own file. It is not applied in the same turn as the file that is already live.

## Session, then spent

A pre-proposal belongs to the agent session that was visible when it was written. The CLI looks only at `AGENT_SESSION`. If that variable is unset or empty, the client has hidden the session. Do not file the proposal under a session, and do not archive it. The feature stays off.

While the session is visible, the proposal lives under that session:

`.aether/proposals/sessions/<AGENT_SESSION>/`

That directory is the session. It is not a flat pile of every proposal ever written.

When that session's suggestion is dead (not applied, or applied and then rejected), archive it under spent inside the same session:

`.aether/proposals/sessions/<AGENT_SESSION>/spent/`

`spent` is the archive of one session. It is not a top-level bucket. A later session does not drop its files into another session's spent directory.

The move into `spent/` is a human hand. This file does not move or delete proposals. A turn may list the paths that are still in the session directory. It does not invent a session id, and it does not read a vendor's private session store.

## What this is not

No git hook. No daemon. No watcher. No auto-apply. No auto-approve. A recommendation is not a Yes.
