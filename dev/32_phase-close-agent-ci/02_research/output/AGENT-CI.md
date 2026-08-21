# Research — CI with agents (multiple SDKs)

**When:** 2026-08-19  
**Not CURRENT.** Not an approve.  
**Question:** What setup lets Grok subagents run **massive simultaneous reviews** to redefine the product, without inventing multiple Nexts, and without models approving?

## Layers (do not collapse)

| Layer | Job | Authority? |
|-------|-----|------------|
| **A. Deterministic gates** | `sh tests/run.sh` · `sh scripts/ci-control-layer-gates.sh` | Proof of protocol, not product taste |
| **B. Optional GitHub Actions** | `.github/workflows/test.yml` already runs A on push/PR | Remote copy of A. Not product. |
| **C. Agent review swarm** | Parallel Grok reviewers → one synthesized `REVIEW.md` | Taste / redefinition. **Propose only.** |
| **D. Human** | `aether approve` / `reject` / apply CURRENT | **Only actualisation** |

Docs already say: CI runners are not product infrastructure; local scripts are the source of truth (`docs/CI-CONTROL-LAYER.md`). `docs/TESTING.md` is stale when it claims there is no `.github/workflows/` — there is.

`--yolo` / `bypassPermissions` / model `aether approve` are **prohibited** here (`automatic-approve`).

## What the 2026 SDKs actually do

### Grok Build (this seat)

- **Interactive:** `spawn_subagent` — own context, types `general-purpose` / `explore` / `plan`, `capability_mode`, `isolation=worktree|none`. Parent live-child cap is host-configured (workflow docs: 32 live; budget 128 default, 1024 max).
- **Orchestrated:** `workflow` Rhai — `parallel([...])` is the only concurrency; barrier; atomic admit against `agent_budget`. Reviewers should be `capability_mode: "read-only"` and write via the script’s scratch / `output/` after synthesis.
- **Headless CI:** `grok -p "…" --output-format json --tools "read_file,grep,list_dir"` (deny `Agent` if you do not want nested swarms inside a matrix cell). `--yolo` exists; **do not use it** in this repo’s product CI.
- **Fit:** local-first, already how this TUI works, matches ICM (folders + one synthesizer). Best primary swarm.

Public claim (xAI, May 2026): parallel subagents + worktrees + `-p` for scripts. Parallelism is the product bet vs Claude’s depth vs Codex’s cloud sandboxes (third-party 2026 roundups). Treat “8 parallel” marketing as a *default taste*, not a hard cap — this host’s workflow budget is the real cap.

### OpenAI Codex

- `codex exec` for non-interactive; official **Codex Action** (`openai/codex-action`) for GitHub with sandbox controls.
- Strong at long terminal runs and cloud worktrees. Approval-mode `full-auto` is their CI pattern — **incompatible** with Mechanicall’s human Yes if pointed at CURRENT.
- Use as an **optional second panel** that writes `output/codex-review.md` only.

### Claude Code

- CLI + GitHub Action (`anthropics/claude-code-action` lineage) + subagents / Agent Teams (2026).
- Best as a **skeptic panel** on a PR diff, read-only, artifact to `output/`.
- Must not `gh` merge or rewrite CURRENT.

### Cursor / Copilot CLI / others

- Fine as extra SDKs if a human installs them. Not required. Do not make the product depend on them.

## Patterns that work (and that failed here)

**Work:** Plan → **parallel fan-out of read-only reviewers** → adversarial verify → **one** synthesized document → **human** Yes. Grok’s bundled `review-changes` workflow is this shape. Sequential A33 walkers (31) were correct for *one phone*; they are the wrong shape for *redefining the product*.

**Fail:** One Next per room (logo, picker, chat, decide). Operator already forbade that. Dual-concurrent-next is prohibited. A swarm that writes CURRENT is a jailbreak.

**Fail:** Unbounded `spawn_subagent` in a chat session without a budget. The session dies, reviews do not land as files, and nobody can `cat` the product definition.

## Caps (so “massive” is a number)

| Knob | This seat (Grok) | Meaning |
|------|------------------|---------|
| Live children | ~32 (host) | Concurrent subagents in one parent |
| `agent_budget` | 128 default, max 1024 | Logical agent() + parallel() items per workflow run |
| Isolation | `worktree` for writers; `none` + read-only for reviewers | Reviewers must not fight over files |
| GitHub matrix | N jobs × `grok -p` | Extra fan-out; needs secrets **not in git** |

A first product-redefinition run should be **one workflow**: ~8–16 read-only Grok reviewers in one `parallel()`, then one synthesizer, then `await_user`. That is massive relative to sequential walks. It is not infinite.

## Recommendation (one sentence)

**Approve a Grok workflow factory** that fans out read-only reviews into `output/`, synthesizes one `REVIEW.md`, and never touches CURRENT; keep `tests/run.sh` as the only green gate; optional Codex/Claude jobs are extra panels, not Nexts.
