# PROMPT-CONTRACT — 7B + active LoRA, hunk-scoped ICM

**Not CURRENT.** Desk model: `personal-llm-sft-v4:latest` (7B + LoRA). LoRA = propose/taste only (ARCHITECTURE). Local stage owns writes.

## Hard refuses (engine, not the model)
Python must refuse before Ollama if:
- Prompt would include the **whole** `CURRENT.md` or whole `PROPOSE-CURRENT.md`
- Stage is not `propose` (show-plan / gate do not write)
- Host is public (`0.0.0.0` / Funnel) — existing `_refuse_public_ollama`

Keep existing caps as a ceiling: `CHAT_USER_TURNS=3`, `CHAT_MSG_CHARS=280`, `CHAT_SAY_CHARS=240`. Hunk body may exceed 280 **only for the focused section**, still truncated (suggest 1–2 KB max section, not the file).

## Prompt shape (every Send from Draft)
```
sys: Mechanicall peer. Propose only. Output one hunk patch. Do not rewrite CURRENT. Do not approve.
stage: propose
focus: <heading or field name>
LIVE (this hunk only):
<live bytes>
PROPOSED (this hunk only, may be empty):
<propose bytes>
schema fields (names + short values, not prose dump):
Objective / Next / … (AUTHORITY_FIELDS)
user turns (≤3, trimmed):
…
```

## Model output
1. `say:` ≤240 chars, one line, not a chat essay.
2. `hunk:` unified diff **or** replacement text for **focus only**.
3. Optional `schema:` JSON/map of AUTHORITY_FIELDS to complete from the hunks (S11). Applied as **more PROPOSE suggestions**, never CURRENT.

If the model emits a full CURRENT or a `stage: gate` self-promotion: drop fields (existing `parsed_stage` cannot promote).

## Apply
- `hunk` → patch `PROPOSE-CURRENT.md` at that heading.
- `schema` → merge into proposed AUTHORITY_FIELDS in the same file.
- CURRENT.md bytes unchanged.
- GATE: idle → warm → gate (stream chunks) → quiet. Not `…` on SEND.

## Tests to add (03_verify)
- Dump-file prompt path returns refuse, no HTTP.
- Hunk apply does not touch CURRENT.md.
- Schema auto-complete does not touch CURRENT.md.
- Empty Why still cannot Confirm.
