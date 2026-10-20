# RECEIPT — apex verify publish-pilot-page (2026-09-09)

**Not Yes.** Generate discuss ignored. Human: commit/push, verify on actual website, receive the offer.

## Ship

- Commit `6b2e77f` on `anphuni.com` `main`
- Push `390e8fd..6b2e77f` → origin
- Render: `/you-decide` 404 → 502 → **200** (~80s)

## Operate (https://anphuni.com)

| Step | Result |
|------|--------|
| GET `/you-decide` | 200 |
| POST `/api/you-decide/mint` | `/you-decide/t/a7d0de04b897dfe3b30ff5d9530a4a63` `not_yes` |
| GET ticket before drop | `drop: null`, zip empty |
| POST drop `offer.txt` (24 B) | `not_yes`, name offer.txt |
| GET ticket after drop | **received:** `drop: offer.txt (24 B)` |
| GET zip | 409 empty until later Yes |
| `/session` `/protocol` `/privacy` | 200 |

Ticket: https://anphuni.com/you-decide/t/a7d0de04b897dfe3b30ff5d9530a4a63

Stills: `apex-you-decide.png`, `apex-ticket.png` (shows **drop: offer.txt (24 B)**).

## Receive where

Health: `you_decide.inbox` = `/opt/render/project/src/data/you-decide` (Render app disk). **Not** Kingston `inbox/tickets`. `YOU_DECIDE_INBOX` in `render.yaml` may not have bound this deploy. Redeploys can wipe ephemeral `src/data`. Durable path needs Render env/disk as yaml (`/var/data/seats/you-decide`).

## Not done

- Operator zip (`out.zip`) — later Yes
- Generate / CURRENT.md talk — parked
- `aether next` / approve — not this receipt
- Live mechanicall-os CURRENT still **REJECTED**
