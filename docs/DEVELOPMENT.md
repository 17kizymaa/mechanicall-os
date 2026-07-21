<!-- generated-by: gsd-doc-writer -->
# Development

How to work on **Mechanicall OS** (`mechanicall-os`) as a contributor.

This repo is a **local-first project control layer**: one POSIX shell CLI
(`aether`), plain Markdown/JSON sidecars, and a few optional Python helpers.
There is **no** package manager build step, no database, and no application
server. Components listed in [NOT-IMPLEMENTED.md](../NOT-IMPLEMENTED.md)
(PostgreSQL, LangGraph, vector DBs, web dashboards) are **not** part of this
codebase — do not add them without an explicit architecture decision.

For end-user install and first run, see [getting-started.md](./getting-started.md)
and the root [README.md](../README.md). For env vars and sidecars, see
[CONFIGURATION.md](./CONFIGURATION.md).

---

## Overview

| Concern | Where it lives |
|---------|----------------|
| One-true CLI | Repo-root [`aether`](../aether) (copy also at [`bin/aether`](../bin/aether)) |
| Optional LLM helpers | [`python/`](../python/) (`aether_garden.py`, `aether_rival.py`, `aether_llm.py`) |
| Integration tests | [`tests/run.sh`](../tests/run.sh) |
| Authority contract | [`SPEC-v0.2.md`](../SPEC-v0.2.md) |
| Awareness contract | [`SPEC-v0.1.md`](../SPEC-v0.1.md) |
| Locked principles | [`CORE_PRINCIPLES.md`](../CORE_PRINCIPLES.md) |
| Agent / ICM workflow | [`AGENTS.md`](../AGENTS.md) |

**Runtime model:** edit files → run `./aether …` or `./tests/run.sh`. No compile,
no `node_modules`, no migrations.

---

## Local setup

### Prerequisites

| Tool | Required? | Notes |
|------|-----------|--------|
| POSIX shell (`sh`) | **Yes** | Core CLI is pure shell (`set -e`, no bashisms required in `aether`) |
| Standard Unix utilities | **Yes** | `find`, `grep`, `sed`, `awk`, `cksum`, `mkdir`, `mktemp`, … |
| `python3` | Optional | Needed for `garden`, `rival`, and any future `python/aether_distill.py` |
| `entr` | Optional | Preferred backend for `aether watch`; poll mode works without it |
| Nix (flakes) | Optional | Recommended reproducible dev shell (`entr` + `python3`) |
| `direnv` | Optional | Auto-load flake when entering the repo |

No language package install is required for core authority/awareness commands
(`init`, `status`, `distill`, `preflight`, `approve`, `reject`, …).

### Clone and enter the repo

```bash
git clone <repo-url> mechanicall-os
cd mechanicall-os
```

<!-- VERIFY: public or private remote URL for this checkout -->

### Dev environment (NixOS-first)

**Preferred — flake shell:**

```bash
nix develop
# Prints: awareness-agent (Mechanicall OS) — Nix dev shell active
# PATH includes: entr, python3
```

Defined in [`flake.nix`](../flake.nix) (`devShells.default` for `x86_64-linux`
and `aarch64-linux`).

**Classic nix-shell (no flakes):**

```bash
nix-shell          # uses shell.nix → entr + python3
# or one-off:
nix-shell -p entr python3
```

**direnv (recommended with flakes):**

```bash
cp .envrc.example .envrc   # contents: "use flake"
direnv allow
```

See also [nixos-transition.md](./nixos-transition.md) for installing Nix on a
non-NixOS host.

### Without Nix

Install `entr` and `python3` from your distro (or skip them). Core `aether`
commands still work with only a POSIX shell and common utilities.

```bash
# Example (Alpine)
apk add entr python3
```

### Put `aether` on PATH (optional)

```bash
# Recommended: symlink the shell CLI
mkdir -p ~/.local/bin
ln -sf "$(pwd)/aether" ~/.local/bin/aether
# ensure ~/.local/bin is on PATH

# If aether is installed as a bare copy elsewhere, point helpers at this tree:
export AETHER_HOME="$(pwd)"
```

When developing, prefer invoking the checkout directly:

```bash
./aether --help
./aether status /path/to/project
```

> **Note:** `scripts/emit_aether_snippet.py` still emits a `python3 -m aether`
> wrapper aimed at the **legacy** Python package under `legacy/aether/`. Prefer
> the shell symlink above for day-to-day work.

---

## Project structure

```
mechanicall-os/
├── aether                 # One-true POSIX implementation (edit this)
├── bin/aether             # Same CLI surface (keep in sync with root aether)
├── python/                # Optional helpers (stdlib only)
│   ├── aether_llm.py      # Shared Anthropic / xAI / Ollama client
│   ├── aether_garden.py   # aether garden — seed filing proposals
│   └── aether_rival.py    # aether rival — counter-treatment editor
├── scripts/               # Setup, capture, review utilities
│   ├── setup.py
│   ├── emit_aether_snippet.py
│   ├── seed-voice.sh
│   ├── seed-hotkey.sh
│   ├── audio-headset-toggle.sh
│   ├── codebase-review    # points to Grok CLI /codebase-review
│   └── codebase_review.py
├── tests/
│   └── run.sh             # Integration suite (canonical)
├── examples/
│   ├── reel-control/      # v0.2 product proof (authority stop-before-spiral)
│   ├── dev-task/          # Non-reel authority generality
│   └── sidecars/          # Sidecar layout samples
├── docs/                  # Human docs (this file, RHIZOME, config, …)
├── skills/                # Prompt/skill packs (e.g. rival-editor)
├── references/            # Stable reference material for agents
├── dev/                   # Numbered ICM stage workspaces (research/impl)
├── legacy/aether/         # Old Python CLI (0.0.1) — do not extend as primary
├── research/speculative/  # Fiction / not implemented concepts only
├── SPEC-v0.1.md           # Awareness sidecars + CLI contract
├── SPEC-v0.2.md           # Authority / preflight / approve contract
├── CORE_PRINCIPLES.md     # Locked product principles
├── NOT-IMPLEMENTED.md     # Explicit denial list
├── AGENTS.md              # ICM meta-agent session rules
├── ARCHITECTURE.md        # Layer sketch (filesystem / awareness / interface)
├── flake.nix              # Nix flake devShell
├── shell.nix              # Classic nix-shell fallback
└── .envrc.example         # direnv + "use flake"
```

### What to edit for common changes

| Change | Primary file(s) |
|--------|-----------------|
| CLI behavior (init, distill, preflight, …) | `aether` (and keep `bin/aether` consistent) |
| Garden / rival / LLM | `python/aether_*.py` |
| Capture hotkeys / voice | `scripts/seed-*.sh` |
| Integration coverage | `tests/run.sh` |
| Authority semantics | `SPEC-v0.2.md` then implement in `aether` |
| Awareness / sidecars | `SPEC-v0.1.md` then implement in `aether` |

---

## Running the CLI locally

From the repo root (or with `aether` on `PATH` and `AETHER_HOME` set if needed):

```bash
# Help
./aether --help

# Awareness (v0.1)
./aether init /tmp/demo-proj
./aether status /tmp/demo-proj
./aether distill /tmp/demo-proj --quiet --no-hooks
./aether trust /tmp/demo-proj
./aether watch /tmp/demo-proj --poll 5

# Authority (v0.2)
./aether current init /tmp/demo-proj
$EDITOR /tmp/demo-proj/CURRENT.md
./aether current /tmp/demo-proj
./aether preflight write-tests /tmp/demo-proj
./aether approve "tests green" /tmp/demo-proj
# or: ./aether reject "not ready" /tmp/demo-proj
cat /tmp/demo-proj/.aether/events.jsonl

# Capture (Rhizome — never overrides CURRENT)
./aether seed "raw thought"
./aether session "note for this project"
./aether garden status          # needs python3 + optional LLM keys
```

### Fixture demos

```bash
# Stop-before-spiral authority proof
cd examples/reel-control
../../aether init .
../../aether current
../../aether preflight rough-v6      # expect refuse
../../aether preflight silent-proof  # expect allow

# Non-reel generality
cd examples/dev-task
../../aether init .
../../aether preflight add-postgres  # refuse
../../aether preflight write-tests   # allow
```

### Distill implementation note

`aether distill` calls shell `dumb_distill` by default. If
`python/aether_distill.py` is present under `AETHER_ROOT`, it is tried first
and the shell path is the fallback. That optional file is **not** required for
tests or normal operation.

---

## Build commands

There is no compile or bundle step. Useful entry points:

| Command | Description |
|---------|-------------|
| `./aether --help` | CLI surface and subcommands |
| `./aether status [path]` | Inspect sidecars + CURRENT authority |
| `./aether distill [path]` | Rebuild generated section of `.context.md` |
| `./tests/run.sh` | Full integration suite |
| `nix develop` | Enter flake dev shell (`entr`, `python3`) |
| `nix-shell` | Classic shell via `shell.nix` |
| `python3 scripts/setup.py` | Optional one-time setup hints (no deps installed) |

Lifecycle hooks (`prepublish`, etc.) do not apply — this is not an npm/pip package.

---

## Making changes

1. **Read the contract first** — awareness changes → `SPEC-v0.1.md`; authority
   changes → `SPEC-v0.2.md`. Product claims must not contradict
   `NOT-IMPLEMENTED.md` or `CORE_PRINCIPLES.md`.
2. **Prefer the shell CLI** — new core behavior belongs in `aether` (POSIX `sh`),
   not a new language or framework.
3. **Keep userland thin** — Markdown for context/docs; Python only for logic that
   is awkward in shell (LLM HTTP, garden apply). Stdlib only in `python/`.
4. **Filesystem remains truth** — durable state is files humans can `cat`,
   `grep`, and `git diff`. No hidden DBs, no silent network authority.
5. **Preserve human sections** — distill must keep notes above
   `<!-- aether:generated:start -->` markers; corrupt markers must refuse to
   overwrite (see tests).
6. **Trust boundaries** — hooks under `.aether/hooks/` run only when
   `.aether/trusted` exists and `--no-hooks` / `AETHER_NO_HOOKS` is not set.
   Init must **not** auto-trust pre-existing hooks.
7. **Silence is never permission** — only explicit human `approve` / edits of
   `CURRENT.md` advance authority. Seeds and garden proposals never unlock
   prohibited actions.
8. **Prove with tests** — extend `tests/run.sh` for any new preflight, hook, or
   distill invariant.
9. **ICM for multi-step work** — sequential research/implementation uses numbered
   stages under `dev/` with `CONTEXT.md` + reviewable `output/` (see
   `AGENTS.md` and `.grok/skills/meta-agent/SKILL.md`). Wait for human review
   before advancing stages when the stage contract requires it.

### Sync `bin/aether`

Root `aether` is the source of truth. If you change it, keep `bin/aether`
aligned (same content or an intentional symlink policy for your install).

---

## Testing

### Framework and setup

There is no Jest/pytest harness. Tests are a **POSIX integration script**:

- File: [`tests/run.sh`](../tests/run.sh)
- Runner: `sh` with `set -e`
- Subject: repo-root `aether` (`AETHER_HOME` and `PATH` pointed at the checkout)
- Isolation: temporary directories under `${TMPDIR:-/tmp}/aether-test.$$`

No global setup beyond a working shell and the repo tree. Optional `python3` is
not required for the suite as written.

### Running tests

```bash
# Full suite (from repo root)
./tests/run.sh
# or:
sh tests/run.sh
```

Successful run ends with:

```text
All aether integration tests passed.
```

There is no watch mode or per-file test runner. To focus on one scenario while
developing, temporarily comment other sections **or** copy the relevant block
into a throwaway script — do not leave the suite permanently disabled.

### What the suite covers

Among other cases:

- `init` + idempotent re-init, scope/trusted files
- Human notes preserved across distill; generated markers present
- Hooks: once when trusted, skipped with `--no-hooks` or untrusted
- Init does **not** auto-trust pre-existing hooks
- Paths with spaces (explicit path args + tree hash semantics)
- Corrupt `.context.md` markers refuse distill without overwrite
- `poke` trust boundary for on-save hooks
- v0.2: `CURRENT` preflight allow/refuse, artifact register, reject/approve,
  events.jsonl, seeds cannot authorize prohibited actions
- Non-reel authority model (`examples/dev-task` shape)
- Preflight refuses when `CURRENT.md` is missing

### Writing new tests

1. Add a clearly labeled section to `tests/run.sh`.
2. Use a fresh directory under `$TMP`.
3. Prefer asserting on exit codes, file contents (`grep -q`), and
   `.aether/events.jsonl` kinds — not on wall-clock or network.
4. Use `pass "description"` / `fail "reason"` helpers already defined in the
   script.
5. Keep tests offline and hermetic (no real LLM calls, no external DBs).

### Coverage requirements

No line/branch coverage thresholds are configured. The bar is: **integration
invariants that match SPEC-v0.1 / SPEC-v0.2 behavior**.

### CI integration

No `.github/workflows/` deploy or test pipeline is present in this repository.
Run `./tests/run.sh` locally before merging.

---

## Code style and conventions

### Shell (`aether`)

- POSIX `sh` (`#!/bin/sh`), `set -e`
- Small functions (`cmd_*`, helpers); global flags stripped without destroying
  quoting (`::AETHER_END::` pattern)
- Prefer `find`/`grep`/`sed`/`awk`/`cksum` over new dependencies
- Fail loudly with `die '…'`; usage via `usage` heredoc
- Never use unquoted `$@` rebuilds that collapse multi-word args or spaced paths
- Distill must not clobber human context; validate generated markers

### Python (`python/`, some `scripts/`)

- Stdlib only (`urllib`, `argparse`, `pathlib`, …)
- No package install, no FastAPI/SQLAlchemy/LangChain in core
- Shared LLM code lives in `aether_llm.py` only
- Keys from env / `~/.config/anthropic/api_key` — never hardcode secrets

### Markdown / sidecars

- Human-editable fields in `CURRENT.md` stay parseable (`**Field:**` lines)
- Generated regions use explicit HTML comment markers
- Docs describe what **is** implemented; speculative material stays under
  `research/speculative/`

### Linting / formatting

No ESLint, Prettier, Biome, or Black config ships with this repo. Use:

- `sh -n aether` — basic shell syntax check
- Manual review against `CORE_PRINCIPLES.md` and SPECs
- Optional: `shellcheck aether` if installed on your machine (not required by CI)

### Branch conventions

No project-wide branch naming policy is documented (no
`.github/PULL_REQUEST_TEMPLATE.md` or `CONTRIBUTING.md` yet). Reasonable default:

- Default branch: whatever the remote uses as mainline
- Feature work: short topic branches (e.g. `feat/preflight-xyz`)

### PR process

No formal PR template is checked in. Suggested checklist:

- [ ] Behavior matches `SPEC-v0.1.md` / `SPEC-v0.2.md` (or SPECs updated first)
- [ ] Does not introduce denied components from `NOT-IMPLEMENTED.md`
- [ ] `./tests/run.sh` passes
- [ ] Human-owned sidecar sections and trust rules still hold
- [ ] Docs updated if CLI surface or config changed (`README.md`,
      `docs/CONFIGURATION.md`, this file)

---

## Coding principles (non-negotiable)

From [`CORE_PRINCIPLES.md`](../CORE_PRINCIPLES.md):

1. **Filesystem is the single source of truth** — no hidden databases.
2. **Markdown + Python (and POSIX shell for the CLI) as userland** — no heavy
   frameworks or opaque formats in the user layer.
3. **Active, observable sidecars** — state lives in plain files next to the project.
4. **Capture is sacred; structure is deferred** — seeds cost zero decisions;
   filing is later (garden), human-approved.
5. **Extremely low overhead and high inspectability** — `cat` / `grep` /
   `git diff` must be enough to debug.

Product rule of thumb (from the README / denial list):

> The product must prove that it can **stop one wrong action** before it adds
> machinery for performing more actions.

---

## Related docs

| Doc | Purpose |
|-----|---------|
| [README.md](../README.md) | Product overview + quick start |
| [getting-started.md](./getting-started.md) | First-time install / activate |
| [CONFIGURATION.md](./CONFIGURATION.md) | Env vars, sidecars, defaults |
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Three-layer sketch |
| [SPEC-v0.1.md](../SPEC-v0.1.md) | Awareness contract |
| [SPEC-v0.2.md](../SPEC-v0.2.md) | Authority contract |
| [RHIZOME.md](./RHIZOME.md) | Capture / seed / garden doctrine |
| [NOT-IMPLEMENTED.md](../NOT-IMPLEMENTED.md) | What this repo is not |
| [CORE_PRINCIPLES.md](../CORE_PRINCIPLES.md) | Locked principles |
| [AGENTS.md](../AGENTS.md) | ICM / meta-agent session rules |
| [nixos-transition.md](./nixos-transition.md) | Nix install and direnv |
