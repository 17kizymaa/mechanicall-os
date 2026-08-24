# ICM for Chat — decision framework (0.6.0-icm)

Chat is not a dump of CURRENT + PROPOSE + the whole transcript into `personal-llm-sft-v4`.

## Stages (one turn, one stage)

| Stage | When | Desk sees | Desk may write |
|-------|------|-----------|----------------|
| **show-plan** | default / questions | schema fields + last 3 user turns (280 chars each) | nothing (CURRENT/PROPOSE untouched) |
| **propose** | “change next”, draft, rewrite… | same slim pack | PROPOSE only, via fields |
| **gate** | yes / approve / reject / not yet | **no Ollama call** | nothing — “Use Decide” |

One-way: gate never proposes. Chat never Yes.

## Caps (so the local model is not overwhelmed)

- No full `CURRENT.md` in the prompt  
- No full `PROPOSE-CURRENT.md` in the prompt  
- No full `DRAFT-CHAT.jsonl`  
- Last **3** user turns only  
- Bubble **≤ 240** characters (full draft lives in Plan)  
- JSON `{say, stage, fields}` not a markdown novel  

## Face

Composer only. Desk URL is Support/default, not a form on the thread. `imePadding`. Open is not Yes.
