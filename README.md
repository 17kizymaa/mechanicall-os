# awareness-agent

**Mechanicall OS v0** — a minimal, filesystem-native awareness and context system.

Core idea: make every project self-aware through small, living sidecar files that a simple Python agent keeps fresh.

## Locked Core Principles

See [CORE_PRINCIPLES.md](./CORE_PRINCIPLES.md) for the non-negotiable rules:

- Filesystem = single source of truth (no hidden databases)
- Markdown + Python = only userland
- Active, observable context sidecars
- Extremely low overhead + maximum inspectability

## Quick Start

```bash
# 1. Bootstrap sidecars in a project folder
cd /path/to/your/project
python3 /home/awareness-agent/aether/cli.py init

# 2. See what's there
ls -a
cat .context.md
cat .awareness.json

# 3. Manually refresh awareness
python3 /home/awareness-agent/aether/cli.py update

# 4. Start watching (daemon-like)
python3 /home/awareness-agent/aether/cli.py watch
```

Later a proper `aether` executable will be provided via shell integration (see `scripts/`).

## Architecture

Three clean layers — see [ARCHITECTURE.md](./ARCHITECTURE.md):

1. **Filesystem Substrate** — normal folders + tiny sidecars (`.context.md`, `.awareness.json`, `.memory/`)
2. **Awareness Layer** — `aether` Python watcher + CLI that observes, distills, updates
3. **Interface Layer** — plain Markdown and Python scripts (edit files, run commands)

## Sidecar Conventions (v0)

| File / Dir           | Purpose                              | Format     | Managed by      |
|----------------------|--------------------------------------|------------|-----------------|
| `.context.md`        | Human + agent readable project understanding | Markdown   | aether distill  |
| `.awareness.json`    | Freshness, stats, lightweight facts  | JSON       | aether          |
| `.memory/`           | Small recall fragments, notes        | .md files  | user + scripts  |
| `.aether/`           | Internal but still plain-text cache / logs (optional) | various | aether (minimal) |

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
