# awareness-agent

**Mechanicall OS v0** — a minimal, filesystem-native awareness and context system.

Core idea: make every project self-aware through small, living sidecar files that a simple Python agent keeps fresh.

## Locked Core Principles

See [CORE_PRINCIPLES.md](./CORE_PRINCIPLES.md) for the non-negotiable rules:

- Filesystem = single source of truth (no hidden databases)
- Markdown + Python = only userland
- Active, observable context sidecars
- Extremely low overhead + maximum inspectability

## Quick Start (canonical: POSIX `aether` shell CLI)

Contract: **[SPEC-v0.1.md](./SPEC-v0.1.md)**. Implementation: repo-root `./aether` (also `bin/aether`).

```bash
# Optional: install on PATH
ln -sf "$(pwd)/aether" ~/.local/bin/aether

# 1. Bootstrap sidecars in a project folder
cd /path/to/your/project
aether init

# 2. See what's there
aether status
cat .context.md          # human notes ABOVE generated markers survive distill
cat .aether/state.json   # cache (gitignored)

# 3. Manually refresh generated inventory (does not wipe human notes)
aether distill
aether distill --no-hooks   # skip project hooks

# 4. Allow hooks for this project (required after clone; init trusts by default)
aether trust

# 5. Watch (foreground; change-driven poll or entr)
aether watch --poll 5
# aether watch   # needs entr
```

**Trust:** hooks under `.aether/hooks/` run only for trusted projects (`aether trust`) unless disabled with `--no-hooks`. Do not run `aether distill` in untrusted checkouts without reading hooks.

## Architecture

Three layers — see [ARCHITECTURE.md](./ARCHITECTURE.md) and SPEC-v0.1 (shell + `.aether/state.json` is current; legacy Python/` .awareness.json` paths are historical):

1. **Filesystem Substrate** — normal folders + sidecars (`.context.md`, `.aether/`)
2. **Awareness Layer** — `aether` shell CLI (optional Python for garden/rival)
3. **Interface Layer** — plain Markdown and scripts

## Sidecar Conventions (v0.1)

| File / Dir           | Purpose                              | Format     | Managed by      |
|----------------------|--------------------------------------|------------|-----------------|
| `.context.md`        | Human notes + generated inventory between markers | Markdown | human + distill |
| `.aether/state.json` | Freshness cache (safe to delete)     | JSON       | aether          |
| `.aether/trusted`    | Local approval for hooks             | text       | `aether trust`  |
| `.aether/hooks/`     | on-save / on-distill scripts         | shell      | project         |
| `.aether/.scope`     | Paths to inventory                   | text lines | human           |
| `.memory/`           | Optional recall fragments            | .md files  | user + scripts  |

Everything is deliberately small and directly usable.

## Development / Hacking

All code is in this repo:

- `aether` — the core POSIX sh script (the one-true implementation)
- `scripts/` — helper scripts (shell integration, etc.)
- `docs/` — additional guidance
- Examples live as real sidecars in this repo itself when bootstrapped

Run everything with plain POSIX sh + optional python3. No virtualenvs or build steps required.

**NixOS-first development environment** (recommended):

```bash
nix develop
```

See [docs/getting-started.md](./docs/getting-started.md) and `flake.nix` / `shell.nix`.

## Philosophy

> If you can't `cat` it, `grep` it, or `git diff` it, it shouldn't be the source of truth.

The agent exists only to keep useful sidecars alive and accurate. You remain in control.

## Status

Initial scaffolding. Principles and architecture are locked.

Next: basic CLI + watcher + distillation that respects the rules.
