# SETUP — one phase: product-review swarm (approvable)

**When:** 2026-08-19  
**Not law until a human applies the propose and `aether approve`s.**  
Opening this file is not Yes. Running the smoke-check is not Yes.

## What you would be approving (one Next, one phase)

A **factory** that redefines the product by simultaneous Grok reviews, then one human Yes.

Not: four Nexts. Not: another APK walk. Not: models approving.

```text
tests/run.sh                    → deterministic green (already)
.github/workflows/test.yml      → optional remote copy of the same
.grok/workflows/product-review.rhai
        parallel read-only Grok reviewers
        → one REVIEW.md in output/
        → await human
        → propose-current only
Human: aether approve "…"
```

## Files

| Path | Role |
|------|------|
| `.grok/workflows/product-review.rhai` | Swarm: 8 read-only dimensions, one synthesizer |
| `dev/32_phase-close-agent-ci/` | This phase (review + research + setup) |
| `examples/propose-current/PROPOSE-agent-review-ci.md` | CURRENT draft — **you** apply |
| `docs/CI-CONTROL-LAYER.md` | Unchanged local gates |

## How to run (after you Yes the Next, or as a lab run)

```bash
# deterministic — always
sh tests/run.sh
# or
sh scripts/ci-control-layer-gates.sh

# swarm (Grok TUI): /product-review   or
# workflow tool name=product-review
# Watch: /workflows
```

Headless (optional CI cell, **no --yolo**):

```bash
grok -p "$(cat scripts/product-review-prompt.txt)" \
  --tools "read_file,grep,list_dir" \
  --disallowed-tools "Agent,search_replace" \
  --output-format json
```

Do not put API keys in git.

## Caps

- First run: **8** parallel reviewers (the dimensions below) + **1** synthesizer.
- Raise `agent_budget` only after a human sees `/workflows` and the `REVIEW.md`.
- Reviewers: `capability_mode: read-only`. Writers wait for Yes.

## Dimensions (fixed list — not discovered)

1. local-AI structured support  
2. selected directory  
3. chat-app framework  
4. workspace bridge  
5. protocol law (CURRENT / Yes / silence)  
6. ICM factory vs Rooms  
7. distribution honesty (APK / CLI / Play Store)  
8. skeptic (try to refute that a redesign is needed)

## Multi-SDK (optional, not this Next’s identity)

If a human has the binary:

- `codex exec` → `output/codex-review.md`  
- `claude` / GitHub claude-code-action → `output/claude-review.md`  

Same rule: propose only. Never CURRENT. Never merge.

## What this setup refuses

- `--yolo` / `full-auto` pointed at CURRENT  
- Dual Nexts for redesign slices  
- Swarm that `aether approve`s  
- Unbounded spawn in chat with no `output/`  

## Human decision

See `examples/propose-current/PROPOSE-agent-review-ci.md`.

- [ ] Apply propose + **you** `aether approve` with a real reason  
- [ ] Reject; stay SELECT / REJECTED on `people-app-phone-seat`  
- [ ] Revise the workflow, do not approve yet  

Silence is never permission.
