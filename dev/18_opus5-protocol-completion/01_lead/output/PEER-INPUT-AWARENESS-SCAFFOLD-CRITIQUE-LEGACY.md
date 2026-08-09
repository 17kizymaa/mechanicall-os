# Peer input — legacy awareness-scaffold critique (archived)

**Captured:** 2026-08-04  
**Role:** historical peer paste supplied for Opus 5 re-review  
**Authority:** not CURRENT · archival Layer 4 only  
**Note:** This text describes an early v0.1 *awareness-agent* tree. Host already has a claim-by-claim correction at  
`dev/17_client-one-session-three/05_review/output/PEER-CORRECTION-AWARENESS-SCAFFOLD-CRITIQUE.md`.  
Opus 5 must re-adjudicate against **live master after PR #3 merge** (2026-08-04), not re-apply this as truth.

---

## `17kizymaa/mechanicall-os` — what it is

**"Mechanicall OS v0.1"** (repo also calls itself *awareness-agent*) is a single-author, filesystem-native context system: instead of a database or index, every project folder gets tiny "sidecar" files that a small tool keeps fresh so both humans and LLM agents can `cat` a project's current state.

| | |
|---|---|
| Created / last push | 2026-07-10 (both — pushed once, dormant ~1 month) |
| Stars / forks / contributors | 0 / 0 / 1 |
| Languages | Python 57.8%, Shell 38.3%, Nix 3.9% |
| Default branch | `master` |
| License | none present |

**The contract** (from `SPEC-v0.1.md`):

```
project/
├── .context.md        # THE primary artifact — human + machine readable
└── .aether/
    ├── state.json     # tiny cache: last_distill, file_count, tree_hash
    ├── .scope         # one path per line, limits the scan (default ".")
    └── hooks/{on-save,on-distill}
```

The whole runtime is one POSIX `sh` script, `aether`, with six verbs: `init`, `status`, `distill`, `watch [--poll N]`, `repair`, `poke`. `entr` is recommended for watch but never required; zero daemons on the happy path.

There's also a heavy meta layer: `.grok/` (personas like `principles-auditor`, `sidecar-auditor`, a `meta-agent` skill), `references/swarm-agents/`, and `dev/01_…` → `dev/06_…` folders that are essentially archived agent-run transcripts (`CONTEXT.md` + `output/`). The project is visibly built *by* agent swarms as much as *for* them.

---

## Findings

The most interesting thing here is that the repo **already violates its own locked doctrine**, and the docs no longer describe the code.

### 🔴 Doc/code divergence (highest priority)

1. **`README.md` documents software that no longer exists.** Quick Start still says `python3 /home/awareness-agent/aether/cli.py init` — a hardcoded absolute path to a Python package that now lives in `legacy/`. It also advertises `.awareness.json`, which `SPEC-v0.1.md` explicitly demotes to "legacy alias of state.json", and claims Status: *"Initial scaffolding… Next: basic CLI + watcher"* when a working v0.1 shell CLI ships at repo root. The README even contradicts itself mid-file (`aether/cli.py` in Quick Start vs. "`aether` — the core POSIX sh script" under Development).
2. **`CORE_PRINCIPLES.md` is now factually false.** It declares "**Markdown + Python as the only userland** — no other languages" as *non-negotiable*, while the entire v0.1 core is POSIX shell (38% of the repo). `SPEC-v0.1.md` silently amends this to "Markdown + POSIX shell + optional tiny Python". The principles file needs the amendment recorded, or the "locked" framing loses all force.
3. **Stray test artifacts committed.** `CORE_PRINCIPLES.md` ends with a bare `trigger line`; `SPEC-v0.1.md` ends with `---edit---` / `===edit marker===`. Clearly watch-loop test residue.
4. **The "smart" distill path is dead code.** `python_distill()` looks for `$AETHER_ROOT/python/aether_distill.py` — there is no `python/` directory in the tree. Every `distill` silently falls through to `dumb_distill`. The spec's promised ≤80-line optional distiller was never written.

### 🟠 Bugs in `aether`

<details>
<summary><strong>Five concrete defects, with fixes (click to expand)</strong></summary>

**a) Hooks run twice.**
```sh
run_hook() {
  [ -x "$h" ] && (cd "$root" && "$h") || true
  [ -f "$h" ] && (cd "$root" && sh "$h") || true
}
```
`init` creates hooks with `chmod +x`, so both branches fire — every hook executes twice. Make it `if [ -x "$h" ]; then …; elif [ -f "$h" ]; then …; fi`.

**b) `abspath` mangles `.`** — `aether init .` yields root `/cwd/.`, so `basename` gives `.` and you get a `# Context — .` heading plus `/cwd/./…` paths. Special-case directories: `if [ -d "$1" ]; then (cd "$1" && pwd -P); else …; fi`.

**c) `cmd_distill` computes state *before* distilling, then overwrites the distiller's output.** `cnt`/`hsh`/`ts` are captured, `python_distill` runs (and is allowed to write `.context.md`), then `write_state` + `embed_state_comment` stamp the pre-computed values back over it. Compute after, and let one writer own the file.

**d) `watch` (entr path) snapshots the file list once.** The `find … | entr -d -r` list is built a single time; `entr -d` exits when a new file appears in a watched directory, and nothing wraps it — so `aether watch` just dies instead of re-globbing. Wrap in `while true; do … ; done`.

**e) Unknown subcommands are silently swallowed.** `main`'s fallback is `*) cmd_status "$cmd"`, so a typo like `aether distil` prints the status of a nonexistent path with exit 0 instead of erroring. Only treat the arg as a path if `[ -d "$1" ]`; otherwise `die`.

*Caveat:* my fetch tool strips HTML comments, so I could not fully read the `<!--aether … -->` block-rewriting logic in `embed_state_comment`. Two things are worth auditing there by hand: the `awk` inserts the new block **after** line 1, so if line 1 *is* the old block it gets `next`-ed and the `NR==1` insert never fires (block silently lost); and the strip appears line-oriented while the spec shows a **multi-line** JSON comment — that would leave orphaned `}` and `-->` lines behind.

</details>

### 🟡 Hygiene & design

- **No `.gitignore`, and it shows.** `.aether/state.json` is committed despite the spec saying "Gitignore this", and `legacy/aether/__pycache__/*.pyc` + `scripts/__pycache__/*.pyc` are tracked binary blobs — a direct affront to the project's own motto: *"If you can't `cat` it, `grep` it, or `git diff` it, it shouldn't be the source of truth."*
- **The file-type whitelist is too narrow and duplicated.** `*.md`, `*.py`, `*.txt`, `*.sh` — hardcoded in both `collect_files` and `cmd_watch`. Your own `flake.nix` is invisible to the awareness layer, as would be any Rust/JS/Go project. Move it to `.aether/.include` (one glob per line, defaulted).
- **LOC budget blown ~1.7×.** Spec target for `aether` is ≤220 lines; the file is 10.9 KB (≈380 lines). Since "fits in one screen of `cat aether`" is a stated success criterion, this is a spec violation worth either fixing or renegotiating.
- **`cmd_repair` is a lie** — it's just `cmd_distill "$@"`. The spec promises it can "restore a minimal `.context.md` if it looks mangled"; there is no mangle detection.
- **No tests, no CI, no LICENSE.** Given the whole design is shell-script-plus-filesystem, a ~30-line `tests/smoke.sh` (init in a tmpdir → assert 4 files exist → touch → distill → assert `file_count` changed) would cover most of the surface and would have caught (a) and (b).

---

## If you're picking this back up

The fastest path to coherence, in order:

1. **Rewrite `README.md` around `./aether init`** and delete the `/home/awareness-agent/` paths and `.awareness.json` references. Right now a new reader (or agent) is instructed to run software that isn't there.
2. **Add an "Amendments" section to `CORE_PRINCIPLES.md`** recording the Python→POSIX-sh shift, and strip the `trigger line` / `===edit marker===` artifacts.
3. **Add `.gitignore`** (`__pycache__/`, `*.pyc`, `.aether/state.json`) and `git rm --cached` the tracked caches.
4. **Fix the double-hook and `abspath "."` bugs**, then add the smoke test.
5. **Decide on `python/aether_distill.py`**: write the 80-line version, or delete `python_distill()` and drop the claim from the spec. Dead branches in a 380-line "brutalist minimal" script are the exact rot the doctrine exists to prevent.

Want me to draft any of these — the corrected README, the `.gitignore` + amendment patch, or a `tests/smoke.sh`?
