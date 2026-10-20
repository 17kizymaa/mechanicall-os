# opencode seat + Mechanicall protocol

**Doc status:** **NON-NORMATIVE** — ops contract for the opencode CLI (permission gate, not a new authority store).
**Map:** `docs/DOC-AUTHORITY.md`
**Status:** native permission gate · enforced by opencode itself, not by this repo
**Audience:** operator who runs `opencode` in this project

## Truth

opencode is **agentic** (it has its own `edit` and `bash` tools) — unlike the Grok seat
(`docs/GROK-SEAT.md`), which is purely observational, this seat actually gates opencode's
mutating actions, using opencode's own native permission system. This is not "fighting the
TUI" the way a PreToolUse deny would be (see GROK-SEAT.md's warning against that) — it's
opencode's own first-class, documented mechanism for exactly this: `opencode.json`'s
`permission` block, honored by opencode's own approval-prompt UX.

**Verified, not assumed:** a bare `opencode` install (no config file anywhere — confirmed via
`opencode debug config`, and `opencode agent list`) auto-**allows** `edit` and `bash` with
**zero confirmation** for the default `build` agent. This is opencode's factory default, not
a misconfiguration. Left unconfigured, opencode would edit files and run shell commands with
no Yes-gate at all — worse than aider (which needs an explicit `/add` first) and a direct
violation of this repo's `automatic-approve` prohibition. `opencode.json` (below) is what
closes that gap; it is not optional polish.

Also verified against opencode's own docs: `AGENTS.md` is **not** auto-loaded natively —
it must be listed explicitly via `instructions`, same as `CURRENT.md`.

## `opencode.json` (repo root)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "CURRENT.md"],
  "permission": {
    "edit": "ask",
    "bash": "ask"
  }
}
```

- `instructions`: loaded into every opencode session automatically — the model always sees
  `AGENTS.md` ("CURRENT-first; models never approve") and the live `CURRENT.md` (Objective /
  Next / Prohibited) without anyone pasting a brief. No wrapper script needed: unlike aider,
  opencode's model can just run `aether current` / `aether brief` / `aether preflight <id>`
  itself via its own `bash` tool whenever it needs a fresher read — that's the cold-start
  checklist in `docs/AGENT-AGNOSTIC-COLD-START.md`, executable by the agent directly.
- `permission.edit` / `permission.bash` = `"ask"`: every file edit and every shell command
  requires an explicit human Yes in the moment, matching CURRENT.md's "Explicit confirmation
  for destructive or external actions" almost verbatim. `read` / `glob` / `grep` / `list` /
  `webfetch` / `websearch` are left at their defaults (non-mutating, no ceremony needed —
  matches "ordinary personal edits/reads" being ceremony-free too).

## Never `--auto`

`opencode run`/`opencode`'s `--auto` flag is documented by opencode itself as "auto-approve
permissions that are not explicitly denied **(dangerous!)**." Never pass it in this project —
it would silently undo the `permission: ask` gate above and recreate exactly the
`automatic-approve` pattern `CURRENT.md` prohibits. There is no scenario in this Domain where
that flag is appropriate.

## Humans actualise — agent never approves

Same rule as every other seat: the opencode agent may propose file edits (which the human
approves one at a time via the `ask` prompt) but must never run `aether approve` / `reject` /
`next` / `apply` itself. Those stay human-only, via `/mechanicall-domain:approve` etc. or direct shell
use by the human. `apply` copies a proposal's fenced body onto CURRENT.md and is still not a Yes. **Silence is never permission.**

## Invoke

```bash
cd /path/to/mechanicall-os   # or your Domain project
opencode
```

No wrapper script, no `--read` flags to remember — the project config in `opencode.json` is
picked up automatically by any `opencode` invocation from repo root. This is simpler than the
Grok/aider seats precisely because opencode has a native project-config surface those tools
don't.

## Disable / adjust

- Loosen: edit `opencode.json`'s `permission` block (e.g. `"edit": "allow"` for a single
  low-stakes session) — but remember the verified default (above) is dangerously permissive,
  so don't delete the file entirely expecting a safe fallback.
- Opt out entirely: delete `opencode.json`. opencode will fall back to its default `build`
  agent behavior (unrestricted edit/bash) — only do this for throwaway scratch work outside
  this Domain.
- Never use a `permission: deny` on `edit`/`bash` as a substitute for `aether preflight` —
  that's a lockout, not a gate; the point is a human Yes in the moment, not a hard refusal.

## Related

- `docs/GROK-SEAT.md` — the advisory-only precedent this seat's doc mirrors in structure.
- `docs/AGENT-AGNOSTIC-COLD-START.md` — the tool-agnostic checklist opencode's agent can run
  itself via its `bash` tool.
- `docs/DOC-AUTHORITY.md` — this doc's catalog entry and conflict-resolution order.
