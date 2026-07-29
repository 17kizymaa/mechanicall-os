# Desk privacy & history (alpha)

**Product:** `aether desk-serve` / House Desk UI.

## What is true

| Layer | What happens |
|-------|----------------|
| **Browser** | Transcript in `localStorage` (store versioned keys) |
| **On Send** | Recent history is POSTed to myarch and used as model context |
| **Model provider** | Sees user/assistant text for that turn (OpenRouter free or Ollama) |
| **House computer** | By default **does not** write message bodies to `.aether/chat.jsonl` unless `AETHER_DESK_LOG_TRANSCRIPT=1` |

## Exact user-facing copy (preferred)

> Your transcript is persisted in this browser. When you send a message, recent conversation is transmitted to the house computer and model provider as context. Desk does not save message bodies on the house computer unless transcript logging is explicitly enabled.

## Operator flag

```bash
export AETHER_DESK_LOG_TRANSCRIPT=1   # optional server-side chat.jsonl bodies
aether desk-serve --lan domains/house-tv-desk
```

## Not a vault

Conversations are not a legal vault. Do not paste passwords, bank secrets, or health records you would not put in email.
