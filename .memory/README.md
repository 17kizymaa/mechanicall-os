# Session memory — a sidecar, not law

Law: ../CURRENT.md. Human decisions: ../DECISIONS.md. Receipts: ../.aether/events.jsonl.
This folder holds what an agent learned that lives nowhere else.

Capture is sacred; structure is deferred.
- ledger.jsonl  append-only. One JSON object per line. Never rewrite.
- TAIL          last_ts / last_line / seq. Bump after every append.
- topics/       one .md per subject. Deferred filing; reviewed by git diff.
- rollup/       YYYY-MM.md human summaries. Ledger is never truncated.

kind: fact | convention | todo | blocker
No agent or model names. No prompts. No secrets. No restated law.

Start:   read TAIL; tail -100 ledger.jsonl; ls topics/; open what applies.
Turn:    append; bump TAIL. Never block on it.
Fold:    new ledger lines -> topics/<subject>.md, deduped. Propose; human reviews the diff.

Schema: {"ts":"2026-10-08T12:34:56Z","kind":"convention","text":"...","refs":["path:line"]}
