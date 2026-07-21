# Mechanicall OS v0.1 — Brutalist Minimal Spec

**Goal**: Make the infrastructure disappear. The folders should just feel alive.

## Non-negotiable Principles (still locked)

1. Filesystem is the single source of truth. No hidden databases.
2. Markdown + POSIX shell + (optional tiny Python) as userland.
3. Active, directly observable sidecars only. `cat`, `grep`, `sed`, `git diff` must be sufficient.
4. Default happy path has **zero running daemons**. Watch is opt-in and foreground.

## Target Runtime Characteristics

- A project folder + a single `aether` shell script is enough.
- `entr` (static ~30KB) recommended for watch, but never required.
- Python3 only used for "smart" distillation when present and desired.
- Total "core" under ~500 LOC across everything that ships in the repo for v0.1.
- Container image target: `FROM scratch` + busybox symlinks + entr + aether + (optional python) < 8MB.

## Official Sidecar Layout (strict + dumb)

Every project that has been touched by aether contains:

```
project/
├── .context.md                 # THE primary artifact. Human + machine.
├── .aether/
│   ├── state.json              # Tiny. Regenerated on every distill. Gitignore this.
│   ├── hooks/                  # Executable fragments or sh scripts. No schema.
│   │   ├── on-save
│   │   └── on-distill
│   └── .scope                  # Optional. One path per line. Limits scope. Default = "."
└── (optional userland)
    └── .memory/                # Freeform fragments. Pure convention.
```

### .context.md rules

- Starts with a title or just free Markdown.
- May contain optional YAML frontmatter at the very top.
- May contain machine data as a single HTML comment block anywhere:

```markdown
<!--aether
{
  "last_distill": "2026-06-21T20:12:00Z",
  "file_count": 47,
  "scope_sha": "..."
}
-->
```

Scripts prefer `.aether/state.json` when present. They fall back to parsing the `<!--aether ... -->` block with `sed`/`awk` if `jq` is missing.

Users can delete `.aether/state.json` any time. It is cache.

### .aether/state.json (example)

```json
{
  "last_distill": "2026-06-21T20:12:00Z",
  "file_count": 13,
  "source_sha": "a1b2c3..."
}
```

Tiny. Always safe to delete. Never hand-edit long term.

### .aether/hooks/

Just files. If executable and in PATH or relative, aether will run them at appropriate times.

`aether distill` runs `on-distill` hooks after updating sidecars (if present).

File change flows (via entr or manual) run `on-save`.

No plugin system. Just `sh -c` or direct exec.

## The `aether` Command (single POSIX sh script)

Must work with `/bin/sh`.

Core subcommands (keep the surface tiny):

- `aether init [path]`
- `aether status [path]`
- `aether distill [path]`
- `aether watch [path]`
- `aether repair [path]`
- `aether poke` (light touch: touch a file to trigger hooks)

`aether` with no args → `status`.

### watch behavior (the important one)

```sh
# Recommended usage
aether watch

# What it actually does when entr exists:
# Scope dirs come from .aether/.scope via internal scope_dirs() — there is no `aether scope` subcommand.
while IFS= read -r d; do
  [ -d "$d" ] && find "$d" -type f \( -name "*.md" -o -name "*.py" -o -name "*.txt" \)
done < .aether/.scope \
  | entr -d -r sh -c 'aether distill --quiet && .aether/hooks/on-save 2>/dev/null || true'
```

If entr is missing:

- Print clear message: "install entr for live watch (static binary ~30k)"
- Offer pure polling fallback only if user passes `--poll`.

Zero Python in the watch hot loop.

## Distillation

`aether distill` is allowed to be "smart".

Implementation options (in priority):

1. If `python3` and optional `python/aether_distill.py` exist → call it. (Not shipped in v0.1; only `aether_garden.py`, `aether_llm.py`, `aether_rival.py` under `python/`. Default is shell `dumb_distill`.)
2. Else: dumb shell version (`dumb_distill`) that just lists files + appends README excerpt + updates timestamps.

The Python distill should be **one small file**, not a package. Optional / not shipped.

## Scope

`aether init` creates:

```
.aether/.scope
.
```

User can edit `.scope` to contain:

```
.
src/
docs/
```

`aether` commands and watch respect `.scope`.

Prevents death on giant trees (node_modules, .git history, etc.).

## Repair & Integrity

Every distill writes a `source_sha` (simple tree hash via `find | sort | xargs sha1sum | sha1sum` or `cksum`).

`aether repair`:
- Rebuilds state.json
- Can restore a minimal .context.md if it looks mangled
- Is fully deterministic from the filesystem + .scope

## Cross-project (later / opt-in)

`~/.aether/index/` or `$AETHER_HOME/index/`

Scanned only by explicit `aether sync` or `aether global-status`.

Per-project sidecars never talk to each other.

## Installation / "Disappearing" model

Two blessed ways:

**A. Bring the script with the project (maximum portability)**

Just copy `aether` (the sh script) into the project or put it on PATH from the awareness-agent checkout.

**B. System-wide**

Put the `aether` shell script + optional `python/aether_distill.py` (not shipped; shell `dumb_distill` is default) somewhere.

`entr` is a separate static binary the user provides (or the distro does).

NixOS is the recommended development environment for working on this repo (reproducible, declarative, matches the filesystem-as-truth philosophy). Use the provided flake:

```sh
nix develop
# or with direnv + .envrc:  use flake
```

Classic one-off (flakes or not):

```sh
nix-shell -p entr python3
```

Other distros (example shown for Alpine):

```sh
apk add entr
# or statically compile entr yourself (~30k)
```

## One True Test

The canonical experience:

```sh
echo 'aether distill' > .aether/hooks/on-save
find . -name '*.md' | entr -d -n sh -c 'echo "changed" && .aether/hooks/on-save'
```

If `aether` is not in your $PATH (common when you just cloned this repo), prefix with the local dir:

```sh
echo 'aether distill' > .aether/hooks/on-save
PATH="$(pwd):$PATH" find . -name '*.md' | entr -d -n sh -c 'echo "changed" && .aether/hooks/on-save'
```

Or use the built-in:

```sh
aether watch
```

After `aether init`, the generated hooks contain a robust resolver for `$AETHER_BIN`, PATH, or sibling `aether` script. You can also just put the one-liner directly in the hook file.

If this feels good and understandable in 5 seconds, we won.

## LOC Budget (v0.1)

- `aether` (POSIX sh) target: ≤ 220 lines
- Optional `python/aether_distill.py` (not shipped; shell `dumb_distill` only): ≤ 80 lines if added
- Supporting scripts + examples: as few as possible
- **Everything the user must understand to be productive**: fits in one screen of `cat aether`

## What we are deleting / not carrying forward

- The 400+ line Python package as the primary thing
- Always-on Python watcher
- .awareness.json as the *required* machine file (demoted to legacy alias of state.json)
- Any implicit daemon
- Complex class hierarchies

We keep .memory/ as a user-friendly convention but it is not part of the official sidecar contract.

This is the version where the OS starts to vanish.
---edit---
===edit marker===
