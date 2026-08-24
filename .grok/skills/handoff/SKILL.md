---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use when the user says /handoff, wants work to travel to a new session/harness, or names a next-session focus.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
metadata:
  author: mattpocock/skills (installed into Grok TUI)
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

In **this** repo, also write a short pointer at `.continue-here.md` that names the temp path (filesystem is truth; the skill still forbids dumping the whole handoff into the worktree as a second copy of specs).

Include a "suggested skills" section in the document, naming which skills the next agent should load.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs, CURRENT.md, decision-tree.md). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, keystore material, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

Never `aether approve` / `next`. Never rewrite live CURRENT as the model's decision.
