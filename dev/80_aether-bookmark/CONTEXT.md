# 80 — aether bookmark grill

**Layer 1 for this folder only.** Not CURRENT. Not a Yes.

Live Next is still `advanced-local-model`. Bookmark is parked there. This folder grills `aether bookmark` and writes an applyable CURRENT proposal. It does not add the verb. It does not apply.

## Inputs
- Live `CURRENT.md`
- `.aether/proposals/CURRENT-proposal-20261016-1724.md` command spec
- `dev/79_advanced-local-model/output/FRAMEWORK.md`
- `aether` `cmd_apply` backup naming (`.aether/current-before/`)
- One local Ollama call of `personal-llm-sft-v6:latest` (not Onyx)

## Process
1. Grill v6 on the snapshot verb against the live CLI.
2. Write a command spec that uses real verbs and files.
3. Write `.aether/proposals/CURRENT-proposal-*.md` with Next `add-aether-bookmark`.
4. Dry-run apply. Do not apply. Do not implement.

## Outputs
- `output/V6-GRILL.md`
- `output/SPEC.md`
- `output/RECEIPT.md`
- proposal under `.aether/proposals/`

## Halt
Do not add `bookmark` to `AETHER_VERBS`. Do not restore the snapshot onto CURRENT.md. Do not `aether apply`. Do not `aether approve`. Do not spend Onyx.
