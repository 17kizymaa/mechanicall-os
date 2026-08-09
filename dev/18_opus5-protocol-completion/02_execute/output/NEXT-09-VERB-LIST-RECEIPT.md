# Receipt — next-09-verb-list

**Date:** 2026-08-04  
**Action:** `next-09-verb-list` · APPROVED  
**Peer:** Opus 5 🟡-2 / 🟡-3 / 🟡-6 / NEXT-09  

## Deliverable

| Item | Detail |
|------|--------|
| `AETHER_VERSION` | `"0.2"` — `version` / `--version` / `-V` |
| `AETHER_VERBS` | Space-separated list; `aether verbs`; help footer |
| `aether_is_verb` | Internal consistency check if list/dispatch drift |
| Completion | `scripts/aether-completion.bash` |

## Tests

`ok: version + verb list (next-09)` — every verb must not print `unknown command`

## Human gate

```bash
aether next next-10-lab-status
# or park-protocol-alpha
```
