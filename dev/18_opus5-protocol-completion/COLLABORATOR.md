# Collaborator — Claude Opus 5

| Field | Value |
|-------|--------|
| Model | `anthropic/claude-opus-5` via OpenRouter |
| Role | Sprint **lead** — plans waves, prioritizes, reviews; host agent implements |
| Host agent | Grok Build TUI (this session) — tools + filesystem |
| Human | Anphuni — sole `aether approve`; ACCEPTED this collaboration |
| Key | `OPENROUTER_API_KEY` from Desktop/.env (`sk-or-…`); never commit |

## Invocation

```bash
# Host agent runs (never log full key):
export OPENROUTER_API_KEY=…   # from Desktop/.env first sk-or- line
python3 dev/18_opus5-protocol-completion/scripts/opus_lead.py \
  --brief path/to/brief.md \
  --out dev/18_opus5-protocol-completion/01_lead/output/WAVE-N.md
```

## Recent session decisions (must honour)

1. Product = **local authority protocol** (CURRENT + preflight + human yes) — PRODUCT.md boundary map.  
2. Peer GPT-5.6 CONDITIONAL absorbed: docs wording, Session ≠ “not multi-user,” privacy split, AGENTS CURRENT-first.  
3. Client One: no sustained Session use; email-draft transfer **scrapped**; Outlook = research only.  
4. Hosted Session: ≤5 seats lab; not core.  
5. `aether current validate` shipped; protocol-first APPROVED with comments.  
6. Operator uses **Grok Build TUI** as primary seat — Protocol Lab must include Grok interference/observability, not browser-only.  
7. CURRENT overload: **no new CURRENT schema** until peer says so; prefer thin gate.  
8. Stale critique (`python3 …/cli.py`) is wrong baseline — one-true CLI is POSIX `./aether`.  
9. Silence is never permission; models never approve.

## Done criteria (sprint)

- Protocol demo: refuse + allow + human approve path documented and scripted.  
- Thin CURRENT hygiene after APPROVE lifecycle.  
- Grok-aware “you are outside auto-preflight” observability (SessionStart or doc + optional hook).  
- Protocol Lab design merged for Grok + optional web literacy page.  
- Public-facing docs consistent with PRODUCT boundary.  
- Receipts in `02_execute/output/`.
