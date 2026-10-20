# RECEIPT — 77_session-memory

**Action id:** `session-memory`
**When:** 2026-10-08T15:25Z
**Preflight:** allowed (Phase=APPROVE Status=APPROVED, Next=session-memory; approve event 2026-10-08T15:05:34Z)
**Not a Yes for the agent-tool doc rewrite. Not a commit. Not a CURRENT edit.**

## Done

1. `.memory/` sidecar exists: `README.md` (contract), `TAIL`, `ledger.jsonl`, `topics/.keep`, `rollup/.keep`. `principles-reminder.md` untouched and now named in the contract.
2. Folded the sidecar into the documentation where `.memory/` was already described under its old meaning:
   - `ARCHITECTURE.md:15` — sidecar bullet rewritten (ledger / TAIL / topics / rollup; not authority)
   - `README.md:184` — sidecar table row rewritten
   - `docs/DOC-AUTHORITY.md` — `.memory/README.md` row added, NON-NORMATIVE
   - `docs/AGENT-AGNOSTIC-COLD-START.md` — orphan row at the file tail removed; `.memory/` row placed in the step-2 read table
   - `CORE_PRINCIPLES.md:20` already lists `.memory/` — no edit needed
3. Dogfooded the contract: 4 ledger entries (2 fact, 1 convention, 1 todo), `TAIL` bumped to `last_line=4 seq=1`. JSONL validates.

## Found, not changed (for the skills / docs-merge discussion)

- `.grok/skills/meta-agent/SKILL.md:66-77` startup ritual has no CURRENT-first, preflight, or never-approve step. `AGENTS.md:54` still names it the mandatory multi-step entry.
- `.grok/personas/*.toml` (4 files, 2026-07-10): no CURRENT / preflight / never-approve.
- `.grok/hooks/session-start.json` is labelled legacy in the hooks README but still present beside the aether hooks.
- `.claude/` is an empty directory. Claude Code gets only `AGENTS.md`.
- Untracked: `opencode.json`, `docs/OPENCODE-SEAT.md`, `.grok/skills/site-play/`. `docs/DOC-AUTHORITY.md` has an uncommitted human row pointing at the untracked seat doc.
- `.grok/skills/meta-agent/SKILL.md:116` cites `scripts/do-the-thing.py` (does not exist).
- No `mechanicall-domain` skill exists under `.grok/skills/` or `skills/`.

## Environment notes

- `/home/anphuni/mechanicall-os` is no longer a symlink; it is an empty directory (created 2026-10-08 ~16:06). The repo is at `/mnt/kingston-nixos-sync/opt/mechanicall-os`. All work this halt was done at the `/mnt` path.
- Scaffold commit `94a50f8` was made before the select (out of order; noted in the previous receipt). This halt's doc edits are uncommitted.

## Not done

- No commit. No push.
- No write to `CURRENT.md`, `DECISIONS.md`, `.aether/`.
- No script or aether subcommand (framework-before-three-repeats).
- No edit to any `.grok/` skill, persona, or hook.

## Sit

`git diff ARCHITECTURE.md README.md docs/DOC-AUTHORITY.md docs/AGENT-AGNOSTIC-COLD-START.md .memory/` then `cat .memory/ledger.jsonl`.
