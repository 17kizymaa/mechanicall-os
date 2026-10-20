# Inventory — isolation millwork

**Not Yes. Not apex.**

| Surface | Before | After |
|---------|--------|--------|
| GET `/you-decide/t/<id>` | Always `you-decide-ticket.html` (chat-only after 20352fd; before that, desk for **every** room) | `paperTicketIds()` → `you-decide-desk.html`; else chat-only ticket |
| API `getTicket.paper` | Already null unless birthday id | Unchanged |
| POST `/paper/fill` | Already 404 off-allow-list | Unchanged |
| `/paper` `/paper.html` | Global blotter page | 302 → birthday room |
| Home nav Paper | Already stripped 20352fd | Unchanged |
| `public/clients/merseyflush.html` | Cream `--paper` CSS (not stocks) | Untouched |
| GTK twin | Lab | Not relaunched |
| Apex | Stale until human deploy | Not deployed |

Birthday id: `e9b16791a12ac1ef521891b6eac3bf68`.
