# Mechanicall OS

**Doc status:** **NON-NORMATIVE** — entry narrative. Defer conflicts to SPEC-v0.2, PRODUCT, NOT-IMPLEMENTED.  
**Map:** [docs/DOC-AUTHORITY.md](./docs/DOC-AUTHORITY.md)

**Local-first project control layer for human–agent work.**

### Product shape (casual)

**Custom distribution · one application only** (seat UX — incomplete).  
Not “learn the CLI to manage files.” See **[docs/SINGLE-APP-DISTRIBUTION.md](./docs/SINGLE-APP-DISTRIBUTION.md)** · **[START-HERE.md](./START-HERE.md)**.

Service/dev sample Domain folder: `sh scripts/try.sh` (not the casual front door).


Repo: `mechanicall-os` · Product name: **Mechanicall OS**

Core idea: keep AI-assisted projects aligned with the **latest human decision**,
and give agents a **deterministic preflight/refusal gate** — using only plain
files you can `cat`, `grep`, and `git diff`.

**Honest alpha claim:** Mechanicall gives humans and AI agents an inspectable
authority contract and a deterministic preflight gate for project actions. It
does **not** sandbox arbitrary shell access. See
[docs/ALPHA-LIMITATIONS.md](./docs/ALPHA-LIMITATIONS.md).

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

**License:** [Apache License 2.0](./LICENSE) — copyright 2026 anphuni / Mechanicall OS contributors.  
Core protocol and in-tree tools may be vendored under Apache-2.0. **anphuni.com Session** is a separate hosted lab (use terms / privacy on the site); it is not a multi-tenant “open SaaS” license. Boundary map: [PRODUCT.md](./PRODUCT.md#license).
## What it is not

See **[NOT-IMPLEMENTED.md](./NOT-IMPLEMENTED.md)** (scoped to **Mechanicall core**).
In particular: no PostgreSQL, no LangGraph “Cortex,” no sandbox that forces every
agent, no industrial autonomous OS claim, no open multi-tenant SaaS **as core**.

**Boundary map:** **[PRODUCT.md](./PRODUCT.md)** — core protocol vs optional
interfaces vs adjacent hosted Session lab vs research.

## Research directions (not shipped)

Speculative material (club-cortex, multi-LoRA scale, etc.) lives only under
[`research/speculative/`](./research/speculative/). Do not read those as product claims.

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
# Optional: install on PATH (reversible)
sh scripts/install-aether.sh
# or: ln -sf "$(pwd)/aether" ~/.local/bin/aether
#     export AETHER_HOME="$(pwd)"

cd /path/to/your/project

# First-run setup (init + CURRENT + short preflight demo)
aether onboard --yes
# or step-by-step:
#   aether init
#   aether current init
#   $EDITOR CURRENT.md

# Project Panel — TUI with action buttons (not ritual CLI)
aether panel
# aether panel --write   # also emit .aether/PANEL.md + panel.html scaffolds

# Register this folder as a development application (optional)
aether app register my-project

# Awareness (v0.1)
aether status
aether distill
aether trust          # allow hooks after clone — inspect hooks first
aether watch --poll 5

# Authority (v0.2) — this is the product
aether current                 # show parsed authority
aether current validate        # SPEC schema check
aether preflight rough-v6      # refuse if prohibited
aether preflight silent-proof  # allow if it is Next
aether artifact artifacts/proof.mp4 --action silent-proof --status produced
aether approve "KEEP"              # human only
aether next other-action           # after APPROVED: re-SELECT
aether demo                        # refuse→allow→approve→next in temp root
aether brief                       # paste for Grok/external TUI
aether probe other-action          # read-only would-preflight?
# or: aether reject "plate 4 fails"
cat .aether/events.jsonl
```

**Five-minute demo:** `sh scripts/alpha-demo.sh` — see [examples/alpha-demo/](./examples/alpha-demo/).

**Agent integration:** [docs/INTEGRATION-AGENTS.md](./docs/INTEGRATION-AGENTS.md).

**Trust:** hooks under `.aether/hooks/` run only for trusted projects
(`aether trust`) unless disabled with `--no-hooks`. Inspect hooks with
`cat .aether/hooks/*` before trusting.

**Silence is never permission.** Only `aether approve` (or an explicit human
edit of CURRENT) advances authority.

### What preflight can and cannot enforce

| Can | Cannot |
|-----|--------|
| Parse `CURRENT.md` deterministically | Sandbox arbitrary shell / skip-preflight agents |
| Allow or refuse a named action when called | Authenticate that `approve` was a specific human |
| Log allow/refuse to `.aether/events.jsonl` | Stop edits to project files by any FS-capable process |

Compatible agents must call `aether preflight <action>` and stop on nonzero exit.

### Install / uninstall

```bash
sh scripts/install-aether.sh     # symlink into ~/.local/bin
sh scripts/uninstall-aether.sh   # remove symlink only
aether deinit                    # remove .aether/ from one project (keeps CURRENT.md)
```

Details: [docs/getting-started.md](./docs/getting-started.md) · limitations: [docs/ALPHA-LIMITATIONS.md](./docs/ALPHA-LIMITATIONS.md).

## Architecture

Three layers — see [ARCHITECTURE.md](./ARCHITECTURE.md):

1. **Filesystem Substrate** — normal folders + sidecars
2. **Awareness / Control Layer** — `aether` shell CLI
3. **Interface Layer** — plain Markdown and scripts  
   - Optional first-run setup: `aether onboard`, `aether app register`  
   - Optional **Project Panel** TUI: `aether panel` (buttons for preflight/approve/…; same projection can write `.aether/PANEL.md` + `panel.html`)  
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
- **v0.2 alpha distribution** — Apache-2.0 license, CI, install/uninstall helpers,
  first-run `onboard` / `app register`, **Project Panel TUI** (`aether panel`),
  agent recipe, alpha demo
- **Limitations:** [docs/ALPHA-LIMITATIONS.md](./docs/ALPHA-LIMITATIONS.md) · [NOT-IMPLEMENTED.md](./NOT-IMPLEMENTED.md)
