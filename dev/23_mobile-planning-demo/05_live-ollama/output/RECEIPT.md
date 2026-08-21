# Receipt — live Ollama propose-only

**2026-08-16** · `personal-llm-sft-v4:latest` @ `127.0.0.1:11434` (also `100.90.85.68`)

| Check | Result |
|--------|--------|
| CURRENT.md on A33 | **unchanged** 619 bytes, Next `name-the-outcome` |
| PROPOSE-CURRENT.md | pushed after generate + normalize |
| `aether approve` | **not run** |
| Phone curl to Ollama | none (no curl/wget on A33) — generate on myarch, push draft |

sft-v4 first drafts were noisy (fake APK/OpenAI). Parser now also reads `**Field:**` / `**Value:**`. Sitting file on the phone is a **normalized** propose:

- **Objective:** Plant one afternoon of herbs the client can water.
- **Next:** buy-starts

Repeat: `sh scripts/agent-edit-a33.sh`

Human Yes still required to apply.
