## Inputs
- Layer 1: ../CONTEXT.md
- Layer 0: ../../CURRENT.md · ../../AGENTS.md · ../../decision-tree.md (S13, T1–T8b, G-series)
- Layer 3: ../../examples/propose-current/CURRENT-sit-vst-headscale.md
- Layer 3: ../../dev/37_sit-join-workshop/02_implement/output/RECEIPT.md
- Layer 3: ../../docs/AGENT-AGNOSTIC-COLD-START.md (header Next vs body Action id)
- Layer 4: `git status` / `aether current` / `aether preflight sit-vst-headscale`

## Process
You are the **git-tree analyser**. You inform an **executor** agent. You do not execute the PR.

1. Pin live law (`aether current`, header **Next:**). Preflight the Next. Stop on refuse.
2. Map the dirty tree into S13 groups. Never include live `CURRENT.md`, `.aether/events.jsonl`, secrets, `android/app/build`, `local.properties`, `*.apk`.
3. Slice **3–4 PRs** that a reviewer can actually read (this repo’s PRs #1–#6 were small). Historical pattern: one feature branch, sequential PRs after review.
4. Prepare to ingest `/sdcard/mechanicall/` as a **read-only review inbox** between PRs (existing sessions tree — do **not** bind; see `examples/pocket-demo-client/README.md`).
5. Write a brief the executor can follow without this chat.
6. Halt. Do not `git add` / `commit` / `gh pr create`. Do not rewrite CURRENT.

Use `behaviours/print-pr-groups.py` to print the file lists (mechanical).

## Outputs
- EXECUTOR-BRIEF.md -> output/
- PR-MANIFEST.md -> output/
- summary.md -> output/
