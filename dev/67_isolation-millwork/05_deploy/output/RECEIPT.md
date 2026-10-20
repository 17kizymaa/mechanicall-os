# RECEIPT — isolation-millwork apex

**Human authorized deploy.** Not `aether approve`. Action was `isolation-millwork` (preflight ALLOW). Did not probe `deploy` (that token hits Prohibited).

## Git

Repo: `~/sites/anphuni.com-repo` → `https://github.com/17kizymaa/anphuni.com.git`  
Commit: `0204887` `feat(you-decide): isolate Paper to birthday; chat-only elsewhere`  
Pushed: `origin/main` (Render `autoDeploy: true`, `branch: main`)

## Apex checks (after 502 during rebuild)

| URL | Result |
|-----|--------|
| `GET /health` | 200 |
| birthday `e9b16791…` | desk HTML (`paper-reset`, dock) |
| Mum `e745d275…` | `yd-chat`, no `#trader` |
| merseyflush `f4e969e6…` | `yd-chat`, no `#trader` |
| this-works `2b48071d…` | `yd-chat`, no `#trader` |
| `/paper` | 302 |

Did not reset the live birthday book. Did not Send. Did not stamp Yes on a ticket.
