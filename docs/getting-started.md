# Getting Started with aether

## Install / Activate (no installation needed)

The entire system is the files in this directory.

```bash
# From the mechanicall-os checkout (one-true CLI is the POSIX shell script):
./aether --help

# Recommended: add to your shell once
python3 scripts/emit_aether_snippet.py >> ~/.bashrc
source ~/.bashrc

aether --help
```

## Recommended: Develop on NixOS

This repository targets NixOS for contributor and agent development environments (reproducible toolchains, zero hidden state).

**Full transition instructions** (including quick "just install Nix" path and full OS install): see [docs/nixos-transition.md](./nixos-transition.md).

From the repo root:

```bash
nix develop
# Now entr + python3 are in PATH for aether watch / distill.

./aether status
./aether init   # in another folder you are making self-aware
```

With direnv (highly recommended on NixOS):

```bash
echo 'use flake' > .envrc
direnv allow
```

A classic `shell.nix` is also present for `nix-shell` users.

No other dependencies. The core `aether` script is pure POSIX sh.

## Bootstrap a new project

```bash
cd ~/my-cool-project
aether init
aether distill
cat .context.md
```

## Keep it fresh

```bash
# One-shot
aether distill

# Continuous
aether watch   # uses simple polling in v0
```

Edit `.context.md` or `.memory/*` yourself anytime — aether treats them as the source of truth.

## Inspect everything

```bash
ls -a
cat .context.md
cat .aether/state.json
tree .memory || ls .memory
grep -r "TODO" .context.md .memory
```

No black boxes.

## Prerequisites

Core **aether** is a single POSIX shell script (`aether` at the repo root, also
`bin/aether`). There is no package install, database, or cloud account required
for awareness or authority.

| Requirement | Notes |
|-------------|--------|
| POSIX shell + common Unix tools | `sh`, `grep`, `sed`, `awk`, `date`, `mkdir`, `chmod` — present on any normal Linux |
| `python3` | Optional — only for garden / rival LLM helpers under `python/` |
| `entr` | Optional — preferred by `aether watch`; without it, watch falls back to poll mode |
| Nix (optional) | `nix develop` or `nix-shell` for a reproducible contributor shell (`flake.nix` / `shell.nix`) |

Recommended path setup (current truth for v0.2):

```bash
# From a mechanicall-os checkout:
ln -sf "$(pwd)/aether" ~/.local/bin/aether
export AETHER_HOME="$(pwd)"   # so python/ helpers resolve when aether is on PATH
aether --help
```

LLM keys (`XAI_API_KEY`, `ANTHROPIC_API_KEY`, or local Ollama) are **not**
required for `init`, `status`, `distill`, `preflight`, `approve`, or `reject`.
See [CONFIGURATION.md](./CONFIGURATION.md).

## Authority control (v0.2)

v0.2 adds a human-owned authority file so agents cannot treat every idea as an
instruction. Contract: [SPEC-v0.2.md](../SPEC-v0.2.md).

**Silence is never permission.** Only an explicit `aether approve` (or a human
edit of `CURRENT.md`) advances authority.

### Bootstrap authority in a project

```bash
cd /path/to/your/project
aether init              # .context.md + .aether/ sidecars
aether current init      # CURRENT.md template (if missing)
$EDITOR CURRENT.md       # set Objective, Phase, Next, Prohibited
aether current           # show parsed authority summary
aether status            # sidecars + CURRENT together
```

### Gate an action

```bash
aether preflight <action-id>     # exit 0 = allowed, exit 1 = refused
# examples:
aether preflight silent-proof    # allowed when it matches **Next:**
aether preflight rough-v6        # refused when listed under ## Prohibited
```

Preflight refuses when:

1. `CURRENT.md` is missing
2. The action matches a `## Prohibited` entry
3. `**Next:**` is set and the action does not match it
4. Status is `BLOCKED` / `BLOCKED-PENDING-HUMAN` and the action is not Next
5. Status is `REJECTED` (return to SELECT; human re-selects)

Every preflight writes a line to `.aether/events.jsonl`.

### Produce evidence, then human decide

```bash
# Register what was produced (does not approve anything)
aether artifact artifacts/proof-01.txt --action silent-proof --status produced

# Human only — workers must never approve their own work
aether approve "KEEP"
# or:
aether reject "arrival on plate 4 fails"

cat CURRENT.md
cat .aether/events.jsonl
```

### Walkthrough fixtures

```bash
# Reel-control proof (stop before spiral)
cd examples/reel-control
../../aether current
../../aether preflight rough-v6      # Refused
../../aether preflight silent-proof  # Allowed
# full sequence: examples/reel-control/README.md

# Non-reel generality
cd examples/dev-task
../../aether preflight add-postgres  # Refused
../../aether preflight write-tests   # Allowed
```

## Capture / Rhizome

Capture is sacred; structure is deferred. Seeds never override `CURRENT.md`.
Design: [RHIZOME.md](./RHIZOME.md).

```bash
aether seed "thought"              # append to $AETHER_INBOX (default ~/inbox.md)
echo "piped thought" | aether seed
aether session "listening: track"  # project .session.md (no arg: show tail)
aether spark                       # one random line from $AETHER_SPARKS (~/prompts.md)
aether graph                       # [[wiki-link]] network as Mermaid
aether garden                      # propose seed destinations (optional LLM)
# edit [ ] → [x] on accepted proposals, then:
aether garden apply
```

Optional capture helpers (not required for core CLI):

| Helper | Purpose |
|--------|---------|
| `scripts/seed-hotkey.sh` | Global hotkey → `aether seed` |
| `scripts/seed-voice.sh` | Short voice note → seed (Whisper / whisper.cpp) |

Daily loop card: [PHONE-RHIZOME-CARD.md](./PHONE-RHIZOME-CARD.md).

## Common workflows

### Awareness only (v0.1 surface)

```bash
aether init
aether distill           # rebuild generated section of .context.md
aether status
aether watch --poll 5    # live updates (entr or poll)
aether trust             # allow .aether/hooks after clone
aether repair            # diagnose sidecars, then distill safely
```

### Authority-gated task (v0.2)

1. Human writes `CURRENT.md` (`Objective`, `Phase`, `Next`, `Prohibited`).
2. Agent or script runs `aether preflight <action>` before any consequential step.
3. On allow: do that **one** action; register proof with `aether artifact`.
4. Stop. Human runs `aether approve` or `aether reject`.
5. Inspect `.aether/events.jsonl` — complete transition history, plain text.

### Integration test smoke

```bash
# from mechanicall-os checkout
./tests/run.sh
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `command not found: aether` | Script not on `PATH` | `ln -sf /path/to/mechanicall-os/aether ~/.local/bin/aether` or run `./aether` from the checkout |
| `PYTHONPATH=… python3 -m aether` fails | Legacy Python package path; one-true CLI is the shell script | Use repo-root `./aether` or the symlink above — not `python -m aether` |
| `no CURRENT.md — refuse all…` | Authority not initialized | `aether current init` then edit `CURRENT.md` |
| Preflight always refuses | Action not equal to `**Next:**`, or listed under `## Prohibited` | Read `aether current`; fix `CURRENT.md` as a human |
| Hooks never run after clone | Project untrusted | `aether trust` (creates `.aether/trusted`) |
| Hooks skipped with warning | Same as untrusted, or `AETHER_NO_HOOKS=1` / `--no-hooks` | Trust the project, or unset the env flag |
| `garden missing: … (is AETHER_HOME set?)` | Bare `aether` on PATH cannot find `python/` | `export AETHER_HOME=/path/to/mechanicall-os` |
| `no spark deck at …` | `~/prompts.md` missing | Create it: one oblique prompt per line |
| `aether update` not recognized | There is no `update` subcommand in v0.2 | Use `aether distill` (one-shot) or `aether watch` (continuous) |
| Corrupt distill markers | Broken `aether:generated:start/end` pair in `.context.md` | Fix markers by hand, then `aether distill` or `aether repair` |

## Next steps

| Doc | Why read it |
|-----|-------------|
| [../README.md](../README.md) | Product overview and quick-start contract |
| [../SPEC-v0.2.md](../SPEC-v0.2.md) | Authority, preflight, approve/reject semantics |
| [../SPEC-v0.1.md](../SPEC-v0.1.md) | Awareness sidecars (context, distill, watch) |
| [./CONFIGURATION.md](./CONFIGURATION.md) | Env vars, sidecars, defaults |
| [./RHIZOME.md](./RHIZOME.md) | Capture layer design |
| [../ARCHITECTURE.md](../ARCHITECTURE.md) | Three-layer architecture sketch |
| [../NOT-IMPLEMENTED.md](../NOT-IMPLEMENTED.md) | Explicit non-goals (no DB, no Cortex, …) |
| [../examples/reel-control/](../examples/reel-control/) | End-to-end v0.2 stop-before-spiral demo |
| [../examples/dev-task/](../examples/dev-task/) | Non-reel authority example |
| [./nixos-transition.md](./nixos-transition.md) | Nix / NixOS contributor environment |

Verify the binary yourself anytime:

```bash
aether --help
cat CURRENT.md
grep -r . .aether/events.jsonl
```
