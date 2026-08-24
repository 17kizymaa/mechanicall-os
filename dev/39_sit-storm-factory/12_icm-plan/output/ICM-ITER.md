# ICM-ITER — 7B replies, then the prompt changed

**Not Yes.** Model: `personal-llm-sft-v4:latest` on myarch `:11434`. One generate at a time.

## What it actually said

**Old hunk JSON ICM** (glass, 11 Draft): last desk say was `user: Go outside user: Create a folder`. The 7B continued the `Recent user turns` transcript. JSON `{"hunk":...}` did not land. First live generate of that prompt **timed out** (LOAD).

**Field ICM** (this run, 68.6s, `new-field-icm.txt`):

```
GOAL: 100% CURRENT within 3 hours (no CURRENT today)
RULE: no CURRENT until explicit approval
I will not approve CURRENT.
You must say SURE and I will reply with one paragraph.
**Objective:** Deliver the "Say" line in
```

It **will not approve** (good). It **ignores** SAY:/CHANGE: wrappers. It **does** emit `**Objective:**` (SFT CURRENT shape). It drifts into “say SURE” / GOAL-RULE from training.

## Iteration shipped in `draft_chat`

1. Stop prefixing history with `user:` (that was the echo).
2. Ask for **one field line**, not JSON hunks: `**{focus}:** <new value>`.
3. Ban SURE / GOAL / RULE in the system line.
4. Parser: `SAY:` / `CHANGE:` / JSON `change` / `**Field:**`. If the reply starts like a `user:` transcript, treat as **not a proposal**.

Engine still never writes CURRENT. Face no longer says “hunk”.
