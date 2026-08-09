# Mechanicall OS — alpha release notes

**STATUS: DRAFT — not published**  
**Do not tag or announce until human says so.**  
**Superseded for packaging path by:** [RELEASE-NOTES-ALPHA-2.md](./RELEASE-NOTES-ALPHA-2.md) (package-alpha-2).

## What alpha *is*

- **Local-first authority protocol** for human–agent work  
- One live plan file: `CURRENT.md` (SPEC-v0.2)  
- Deterministic **cooperative** preflight (`aether preflight`) when consulted  
- Human-only `aether approve` / `reject` / `next`  
- Inspectable ledger: `.aether/events.jsonl`  
- One-command literacy: `aether demo` (temp sandbox)  
- Schema check: `aether current validate`  
- External-TUI awareness: `aether brief`, `aether drift`  

## What alpha is *not*

- Multi-tenant SaaS or open registration  
- A sandbox that forces every editor/agent to preflight  
- anphuni.com Session as core product (it is a **capped hosted lab**, max 5 seats)  
- Live Outlook / Graph OAuth / host SMTP  
- Club-cortex / multi-LoRA host platform  

## One-command demo

```bash
./aether demo
# expect: DEMO OK
```

## Honesty language

| Surface | Say |
|---------|-----|
| Mechanicall core | local authority protocol |
| anphuni Session | capped hosted alpha lab (≤5 seats) |
| Club-cortex | research only |

Never say Session is “not multi-user” — it is multi-seat hosted, capped, not open SaaS.
