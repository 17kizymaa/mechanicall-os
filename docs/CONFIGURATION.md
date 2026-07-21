<!-- generated-by: gsd-doc-writer -->
# Configuration

Mechanicall OS is configured almost entirely through **environment variables**,
**project sidecars** (plain Markdown/JSON on disk), and **CLI flags** on the
POSIX `aether` script. There is no central config server, database, or
dashboard.

This document covers what you can set, what is required, and what defaults
apply. For authority semantics see [SPEC-v0.2.md](../SPEC-v0.2.md); for capture
paths see [RHIZOME.md](./RHIZOME.md). Components listed in
[NOT-IMPLEMENTED.md](../NOT-IMPLEMENTED.md) (PostgreSQL, LangGraph, vector DBs,
web config UIs) are **not** configuration targets — they do not exist.

---

## Configuration surfaces

| Surface | Where | Purpose |
|---------|-------|---------|
| Environment variables | Shell / direnv / process env | Paths, LLM backends, hook suppression |
| Project sidecars | Project root + `.aether/` | Authority, awareness, trust, events |
| CLI flags | `aether` invocation | Per-run overrides (`--no-hooks`, `--quiet`, …) |
| Nix / direnv | `flake.nix`, `shell.nix`, `.envrc` | Dev tool PATH (`entr`, `python3`) |
| Optional helper scripts | `scripts/seed-*.sh` | Voice/hotkey capture knobs |

Core CLI lives at repo-root [`aether`](../aether) (also `bin/aether`). Optional
Python helpers under [`python/`](../python/) read the same env vars.

---

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AETHER_HOME` | Optional | *(unset)* → if script dir has no `python/`/`docs/`, uses `$AETHER_HOME` when that directory exists; else `$HOME/mechanicall-os` when `$HOME/mechanicall-os/python` or `$HOME/mechanicall-os/aether` exists | Absolute path to the mechanicall-os checkout. Used when `aether` is installed as a bare copy on `PATH` so `python/` helpers can still be found. |
| `AETHER_NO_HOOKS` | Optional | `0` | Set to `1` to skip project hooks for this process (same effect as `--no-hooks`). |
| `AETHER_INBOX` | Optional | `$HOME/inbox.md` | Global seed inbox path (`aether seed`). |
| `AETHER_SPARKS` | Optional | `$HOME/prompts.md` | Spark deck (one oblique line per line / bullet). |
| `AETHER_PROPOSALS` | Optional | `$HOME/inbox-proposals.md` | Gardener proposal file (`aether garden`). |
| `AETHER_INBOX_ARCHIVE` | Optional | `$HOME/inbox-archive.md` | Archive destination when garden applies `trash`. |
| `AETHER_BIN` | Optional | `aether` on `PATH` | Absolute path to the `aether` script for hooks and helper scripts. |
| `AETHER_RIVAL_TRACK` | Optional | `untitled` | Default track title for `aether rival` when `--track` is omitted. |
| `ANTHROPIC_API_KEY` | Optional* | *(unset)*; also read from `~/.config/anthropic/api_key` | Anthropic Messages API key (highest-priority LLM backend). |
| `ANTHROPIC_MODEL` | Optional | *(see `AETHER_MODEL`)* | Anthropic model id / alias when using Anthropic. |
| `XAI_API_KEY` | Optional* | *(unset)* | xAI API key for `https://api.x.ai/v1` (OpenAI-compatible chat). |
| `AETHER_MODEL` | Optional | Anthropic: `claude-sonnet-5`; xAI: `grok-4.5` | Model id or alias for garden/rival LLM calls. |
| `AETHER_OLLAMA_HOST` | Optional | `http://127.0.0.1:11434` | Ollama base URL. |
| `AETHER_OLLAMA_MODEL` | Optional | auto-pick from Ollama tags, else `aetherOS-custom` | Ollama model name. |
| `AETHER_LLM_TIMEOUT` | Optional | `120` | LLM HTTP timeout in seconds. |
| `AETHER_LLM_PROVIDER` | Optional | *(auto)* | Force backend: `anthropic`, `xai`, or `ollama`. |
| `AETHER_VOICE_SECS` | Optional | `8` | Voice seed recording length (seconds). |
| `AETHER_VOICE_MODEL` | Optional | `$HOME/models/ggml-base.en.bin` | Whisper.cpp model path for `scripts/seed-voice.sh`. |
| `AETHER_VOICE_NO_TOGGLE` | Optional | `0` | Set to `1` to skip headset audio toggle in voice capture. |
| `HOME` | System | user home | Used for default inbox/sparks/proposals paths and Anthropic key file. |

\* LLM keys are **not** required for core authority/awareness (`init`, `status`,
`distill`, `preflight`, `approve`, …). They are only needed for optional
`garden` / `rival` (and other callers of `python/aether_llm.py`).

### LLM backend resolution

Shared plumbing in [`python/aether_llm.py`](../python/aether_llm.py):

1. If `AETHER_LLM_PROVIDER` is set → only that backend is tried.
2. Else, first available in order: **Anthropic** → **xAI** → **Ollama**.
3. If none are available, garden/rival fall back to heuristics or error with a
   clear message — they never invent a database connection.

Anthropic model aliases (via `AETHER_MODEL` / `ANTHROPIC_MODEL`): `haiku`,
`sonnet`, `sonnet-5`, `sonnet-4.6`, and related forms map to API model ids
defined in `MODEL_ALIASES` inside `aether_llm.py`.

<!-- VERIFY: production Anthropic / xAI account dashboards and billing URLs -->

---

## Sidecar and project files

Configuration for a given project is the project directory itself. After
`aether init` / `aether current init`:

```
project/
├── CURRENT.md                 # AUTHORITATIVE operating state (v0.2)
├── DECISIONS.md               # Optional durable decision log (created by approve/reject)
├── .context.md                # Descriptive inventory + human notes (not authority)
├── .session.md                # Chronological activity ledger (Rhizome)
├── .aether/
│   ├── .scope                 # Paths distill/watch scan (default: ".")
│   ├── state.json             # Distill cache (safe to delete; gitignored)
│   ├── trusted                # Local hook-approval marker (gitignored)
│   ├── events.jsonl           # Append-only transition log
│   ├── artifacts/             # Registered artifact metadata (JSON)
│   ├── hooks/
│   │   ├── on-save
│   │   └── on-distill
│   └── .poke                  # Touch file from `aether poke`
└── artifacts/                 # Optional project-owned outputs
```

### `CURRENT.md` (authority)

Human-owned Markdown. Parsed fields (bold labels):

| Field | Meaning | Typical values |
|-------|---------|----------------|
| `**Objective:**` | One-sentence goal | free text |
| `**Phase:**` | Lifecycle stage | `CAPTURE` \| `SELECT` \| `COMMIT` \| `EXECUTE` \| `REVIEW` \| `APPROVE` |
| `**Status:**` | Operating status | `DRAFT` \| `READY-FOR-REVIEW` \| `APPROVED` \| `REJECTED` \| `BLOCKED` \| `BLOCKED-PENDING-HUMAN` |
| `**Baseline:**` | Label or path | free text |
| `**Next:**` | Machine-facing next action id | e.g. `silent-proof`; `unset` means no pin |
| `**Approval:**` | Approval gate | `PENDING` \| `APPROVED` \| `REJECTED` |

Sections (prose / lists):

- `## Keep`, `## Reject`, `## Limits` — human guidance
- `## Next allowed action` — prose for the authorized step
- `## Approval condition` — what the human must do to approve
- `## Prohibited` — bullet list of forbidden action tokens (gates `preflight`)

Create a template with:

```bash
aether current init
```

Authority rules (silence is never permission): seeds, `.context.md`, and
`.session.md` **never** override `CURRENT.md`. See SPEC-v0.2.

### `.aether/.scope`

One path per line (relative to project root or absolute). Default after init:

```
.
```

Edit to limit distill/watch to subtrees (avoids huge trees). Lines starting with
`#` and blank lines are ignored.

### `.aether/trusted`

Created by `aether trust` (or by `aether init` only when **all** default hooks
are newly created — pre-existing hooks after clone stay untrusted). Presence of
this file allows `.aether/hooks/*` to run. Remove the file to revoke trust.

### `.aether/hooks/`

Executable scripts or plain shell files. Known hook names:

| Hook | When |
|------|------|
| `on-distill` | After a successful `aether distill` |
| `on-save` | After `aether poke` / watch change path |

Hooks resolve `aether` via `$AETHER_BIN`, `PATH`, or a sibling script path.
Untrusted projects skip hooks and print a warning unless `--no-hooks` /
`AETHER_NO_HOOKS=1`.

### `.aether/state.json`

Distill cache (timestamps, file count, tree hash). Safe to delete; regenerated
on next distill. Listed in [`.gitignore`](../.gitignore).

### `.aether/events.jsonl`

Append-only JSON Lines log of preflight / approve / reject / artifact / note
events. Inspect with `cat` / `grep`.

### Global capture files (user home)

| File | Env override | Role |
|------|--------------|------|
| `~/inbox.md` | `AETHER_INBOX` | Raw seeds |
| `~/prompts.md` | `AETHER_SPARKS` | Spark deck |
| `~/inbox-proposals.md` | `AETHER_PROPOSALS` | Garden proposals (`[ ]` / `[x]`) |
| `~/inbox-archive.md` | `AETHER_INBOX_ARCHIVE` | Trashed seeds |

These are **capture only** — they do not grant authority.

---

## CLI flags

Global (accepted before the subcommand):

| Flag | Effect |
|------|--------|
| `--no-hooks` | Sets `AETHER_NO_HOOKS=1` for this invocation |
| `-h` / `--help` / `help` | Print usage |

Per-command flags:

| Command | Flags | Notes |
|---------|-------|-------|
| `aether distill [path]` | `--quiet`, `--no-hooks` | Quiet suppresses success print |
| `aether watch [path]` | `--poll N`, `--no-hooks` | Poll interval seconds (default `5` if `--poll` given without value handling via `${2:-5}`); without `--poll`, requires `entr` |
| `aether artifact <file>` | `--action A`, `--status S`, `--project DIR` | Default status `produced` |
| `aether rival` | `--track` / `-t`, `--structure` / `-s`, `--read` / `-r`, `--narration` / `-n`, `--no-log` | See `python/aether_rival.py` |
| `aether garden` | `apply`, `status` (subcommands) | Default: propose only |

Most commands take an optional `[path]` project root (default: current working
directory). `approve` / `reject` use cwd unless a single existing directory
argument is passed.

---

## Required vs optional settings

### Required for core use

Nothing beyond a writable project directory and a POSIX shell. Typical first
run:

```bash
aether init                 # creates .aether/ + .context.md
aether current init         # creates CURRENT.md for authority gates
```

Without `CURRENT.md`, `aether preflight` **refuses** all consequential actions
(exit 1). That is intentional fail-closed behaviour, not a missing env var.

### Required only for optional features

| Feature | Needs |
|---------|-------|
| `aether watch` (entr mode) | `entr` on `PATH` |
| `aether watch --poll N` | Sleep-based loop only (no entr) |
| `aether garden` / `aether rival` (LLM mode) | `ANTHROPIC_API_KEY` and/or `XAI_API_KEY` and/or running Ollama |
| `python/` helpers when `aether` is not in the repo tree | `AETHER_HOME` pointing at the checkout |
| Voice seed (`scripts/seed-voice.sh`) | `ffmpeg` or `arecord`, plus whisper binary/model |

### Failures that block distill

Corrupt `.context.md` generated markers (not exactly one
`<!-- aether:generated:start -->` before one end marker) cause distill to
**refuse** until fixed by hand (`aether repair` diagnoses).

---

## Defaults

| Setting | Default | Set by |
|---------|---------|--------|
| Project root | `pwd -P` | CLI path arg |
| Distill scope | `.` | `.aether/.scope` |
| Seed inbox | `$HOME/inbox.md` | `AETHER_INBOX` |
| Spark deck | `$HOME/prompts.md` | `AETHER_SPARKS` |
| Proposals file | `$HOME/inbox-proposals.md` | `AETHER_PROPOSALS` |
| Inbox archive | `$HOME/inbox-archive.md` | `AETHER_INBOX_ARCHIVE` |
| Hooks | enabled only if `.aether/trusted` exists and `AETHER_NO_HOOKS` ≠ `1` | trust file + env/flag |
| Poll interval | `5` seconds when `--poll` is used | `--poll N` |
| Artifact status | `produced` | `--status` |
| Rival track | `untitled` | `AETHER_RIVAL_TRACK` / `--track` |
| LLM timeout | `120` s | `AETHER_LLM_TIMEOUT` |
| Ollama host | `http://127.0.0.1:11434` | `AETHER_OLLAMA_HOST` |
| CURRENT template Phase/Status/Next | `SELECT` / `DRAFT` / `unset` | `aether current init` |
| CURRENT template Prohibited | `rough-v6`, `full-reel-export`, `automatic-rebuild` | template (edit freely) |

---

## Per-environment overrides

Mechanicall OS does not ship separate staging/production config files. Use
ordinary shell environment composition:

### Local development (this repo)

```bash
# Flake-based shell (entr + python3)
nix develop

# Or classic
nix-shell

# Or direnv — copy example then allow
cp .envrc.example .envrc   # contents: "use flake"
direnv allow
```

[`.envrc.example`](../.envrc.example) only enables the Nix flake; optional
exports can be added there. Do not commit secrets.

### Project-specific authority

Each project carries its own `CURRENT.md` and `.aether/`. Clone a repo → hooks
are **untrusted** until `aether trust` (pre-existing hooks never auto-trust).

### Global capture vs project work

```bash
export AETHER_INBOX="$HOME/capture/inbox.md"
export AETHER_SPARKS="$HOME/capture/prompts.md"
# optional LLM
export XAI_API_KEY=…          # or ANTHROPIC_API_KEY, or start Ollama
export AETHER_LLM_PROVIDER=xai   # force one backend
```

### Installed CLI without living in the repo

```bash
ln -sf /path/to/mechanicall-os/aether ~/.local/bin/aether
export AETHER_HOME=/path/to/mechanicall-os
export AETHER_BIN=/path/to/mechanicall-os/aether
```

If `AETHER_HOME` is unset, `aether` also tries `$HOME/mechanicall-os` when the
script location has no `python/` or `docs/` sibling.

### CI / tests

[`tests/run.sh`](../tests/run.sh) sets `AETHER_HOME` to the repo root and uses
temporary `AETHER_INBOX` paths so tests do not touch the operator’s real inbox.

### What is intentionally not configured

- No database connection strings
- No LangGraph / agent-pool YAML
- No vector store endpoints
- No multi-tenant or cloud workspace settings

Those appear only in speculative material under `research/speculative/` and are
denied by [NOT-IMPLEMENTED.md](../NOT-IMPLEMENTED.md).

---

## Quick reference: inspect live config

```bash
# Authority + sidecars for cwd
aether status
aether current
cat CURRENT.md
cat .aether/.scope
cat .aether/events.jsonl
ls -la .aether/trusted .aether/hooks/

# Capture destinations
echo "inbox=${AETHER_INBOX:-$HOME/inbox.md}"
echo "sparks=${AETHER_SPARKS:-$HOME/prompts.md}"

# LLM backend (garden/rival)
python3 -c 'from pathlib import Path; import sys; sys.path.insert(0,"python"); from aether_llm import describe_backend; print(describe_backend())'
```

All durable truth remains files you can `cat`, `grep`, and `git diff`.
