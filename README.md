# Mechanicall OS

**Local-first project control layer for human–agent work.**

Repo: `mechanicall-os` · Product name: **Mechanicall OS**

Core idea: keep AI-assisted projects aligned with the **latest human decision**,
and **block unapproved execution** — using only plain files you can `cat`,
`grep`, and `git diff`.

## What it is (v0.2)

Aether answers five questions reliably:

1. What is the current objective?
2. What decision is presently authoritative?
3. What is the next allowed action?
4. What is prohibited or needs approval?
5. What happened, and which artifact proves it?

It builds on filesystem sidecars + a single POSIX shell CLI. Optional tiny
Python helpers exist for garden/rival LLM workflows. There is **no** required
database, daemon, or cloud service.

## What it is not

See **[NOT-IMPLEMENTED.md](./NOT-IMPLEMENTED.md)**. In particular: no PostgreSQL,
no pgvector, no LangGraph “Cortex,” no sandboxed multi-agent studio, no
industrial autonomous OS claim. Speculative fiction lives under
`research/speculative/` only.

## Locked Core Principles

See [CORE_PRINCIPLES.md](./CORE_PRINCIPLES.md):

- Filesystem = single source of truth (no hidden databases)
- Markdown + Python/shell = only userland
- Active, observable context sidecars
- Capture is sacred; structure is deferred
- Extremely low overhead + maximum inspectability

## Quick Start

Contract: **[SPEC-v0.1.md](./SPEC-v0.1.md)** (sidecars) + **[SPEC-v0.2.md](./SPEC-v0.2.md)** (authority).  
Implementation: repo-root `./aether` (also `bin/aether`).

```bash
# Optional: install on PATH
ln -sf "$(pwd)/aether" ~/.local/bin/aether

cd /path/to/your/project
aether init

# Awareness (v0.1)
aether status
aether distill
aether trust          # allow hooks after clone
aether watch --poll 5

# Authority (v0.2)
aether current init   # create CURRENT.md template
$EDITOR CURRENT.md    # set Objective, Phase, Next, Prohibited
aether current        # show parsed authority
aether preflight rough-v6          # refuse if prohibited
aether preflight silent-proof      # allow if it is Next
aether artifact artifacts/proof.mp4 --action silent-proof --status produced
aether approve "KEEP"              # human only
# or: aether reject "plate 4 fails"
cat .aether/events.jsonl
```

**Trust:** hooks under `.aether/hooks/` run only for trusted projects
(`aether trust`) unless disabled with `--no-hooks`.

**Silence is never permission.** Only `aether approve` (or an explicit human
edit of CURRENT) advances authority.

## Architecture

Three layers — see [ARCHITECTURE.md](./ARCHITECTURE.md):

1. **Filesystem Substrate** — normal folders + sidecars
2. **Awareness / Control Layer** — `aether` shell CLI
3. **Interface Layer** — plain Markdown and scripts  
   - Optional **personal LLM propose layer** (local Ollama): drafts only, never approves — see [docs/PERSONAL-LLM-LAYER.md](./docs/PERSONAL-LLM-LAYER.md)

```bash
# Prefer local personal model for garden/rival when installed
export AETHER_LLM_PROVIDER=ollama
export AETHER_OLLAMA_MODEL=personal-llm-full:v1   # or personal-llm-sft-v2 when available
export AETHER_PERSONAL_LLM_SYSTEM=1               # inject Mechanicall doctrine SYSTEM
aether garden status
```

### Sidecars

| File / Dir | Purpose | Authority? |
|------------|---------|------------|
| `CURRENT.md` | Present objective, phase, next/prohibited actions | **Yes** |
| `.context.md` | Human notes + generated inventory | No (descriptive) |
| `.session.md` | Chronological activity ledger | No |
| `.aether/events.jsonl` | Append-only transition log | Evidence |
| `.aether/state.json` | Distill cache (safe to delete) | No |
| `.aether/trusted` | Local hook approval | Safety |
| `.aether/artifacts/` | Registered artifact metadata | Evidence |
| `.aether/hooks/` | on-save / on-distill scripts | Must be trusted |
| `.memory/` | Optional recall fragments | No |

## Capture (Rhizome)

```bash
aether seed "thought"     # global inbox — zero decisions
aether session "note"     # project .session.md
aether garden             # optional LLM filing proposals
```

See [docs/RHIZOME.md](./docs/RHIZOME.md). Seeds never override `CURRENT.md`.

## Development

```bash
nix develop          # optional NixOS-first env
./tests/run.sh       # integration tests
```

Code that matters:

- `aether` — one-true POSIX implementation
- `python/` — optional garden / rival / LLM plumbing
- `examples/reel-control/` — v0.2 stop-before-spiral demo
- `examples/dev-task/` — non-reel authority example
- `SPEC-v0.2.md` — authority contract

## Philosophy

> If you can't `cat` it, `grep` it, or `git diff` it, it shouldn't be the source of truth.

> The product must prove that it can **stop one wrong action** before it adds
> machinery for performing more actions.

## Status

- **v0.1** — awareness sidecars, distill, trust, capture (shipped)
- **v0.2** — CURRENT authority, preflight, approve/reject, event/artifact ledger
