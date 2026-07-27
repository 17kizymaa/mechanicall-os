# Alpha limitations — Mechanicall OS v0.2

This file is part of the public alpha contract. If a README claim contradicts
it, **this file wins**.

## Supported environment

- **OS:** Linux (primary). macOS best-effort. Windows only via WSL.
- **Shell:** POSIX `sh` + common Unix tools (`grep`, `sed`, `awk`, `date`, `mkdir`).
- **Core:** no database, daemon, cloud account, or package install required.
- **Optional:** `python3` (garden / rival / personal-llm helpers), `entr` (watch),
  local Ollama (propose drafts only).

## What preflight can and cannot enforce

**Can:**

- Deterministically parse `CURRENT.md`.
- Allow (exit 0) or refuse (exit 1) a named action when a workflow calls
  `aether preflight <action>`.
- Append an evidence line to `.aether/events.jsonl`.

**Cannot:**

- Sandbox the shell or block processes that never call preflight.
- Stop an agent that edits `CURRENT.md` or runs `aether approve` without a human.
- Provide authenticated human identity for `approve` / `reject` in this alpha.
- Prevent any process with filesystem access from rewriting project files.

Honest product claim:

> Mechanicall gives humans and AI agents an inspectable authority contract and
> a deterministic preflight gate for project actions.

Do **not** claim that Mechanicall guarantees agents cannot perform unapproved
actions.

## Not included in the alpha

- Hosted service or multi-tenant SaaS
- Web dashboard as product UI
- Personal model weights / training data
- Club-cortex membership, train queues, multi-user isolation
- Authenticated operator identity
- Production security assurances for sensitive corpora

See [NOT-IMPLEMENTED.md](../NOT-IMPLEMENTED.md).

## Project Panel (optional TUI)

`aether panel` is a **local projection** with action buttons (preflight, approve,
reject, …). It does not add a product web dashboard or sandbox.

- Requires a terminal (TTY); use `--dump` / `--write` non-interactively
- `--write` emits `.aether/PANEL.md` and `.aether/panel.html` (safe to delete)
- Still cooperative preflight — see enforcement section above

## Reversibility

- **CLI symlink:** `scripts/uninstall-aether.sh` or `rm ~/.local/bin/aether`
- **One project:** `aether deinit` removes `.aether/` only (never deletes
  `CURRENT.md` or human notes unless you pass an explicit flag)
- **Hooks:** `aether --no-hooks …` or delete `.aether/trusted`

## Alpha cohort (operator)

- 1 technical self-serve user
- Up to 3 non-technical users with operator support (local clients)

Stars are not the main signal. A real refusal is.
