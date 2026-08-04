# Grok hooks for mechanicall-os

**Trust required:** project hooks need `/hooks-trust` (or `grok --trust`) once per machine.

| File | Event | Behaviour |
|------|--------|-----------|
| `session-start.json` | SessionStart | ICM meta-agent reminder (legacy) |
| `aether-session-start.json` | SessionStart | Runs `aether brief` → stderr + `.aether/last-grok-brief.txt` |
| `aether-prompt-context.json` | UserPromptSubmit | Injects brief as `additionalContext` (model sees Next/gate) |

All hooks are **advisory / non-blocking**. They never deny tools and never rewrite CURRENT.

Script: `scripts/grok-aether-brief.sh`  
Doctrine: `docs/GROK-SEAT.md`
