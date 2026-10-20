# RECEIPT — publish-pilot-page (2026-09-09)

**Not a client job. Not Yes.** Human APPROVED `Go — capability ticket door`. Preflight ALLOW.

## What shipped

Site: `/home/anphuni/sites/anphuni.com-repo/`

| Path | Job |
|------|-----|
| `public/you-decide.html` | Door: offer + limits; mint (not Yes) |
| `public/you-decide-ticket.html` + `assets/you-decide-ticket.js` | Ticket: paper NOT ACTIVE, drop 8 MiB, zip slot |
| `lib/you-decide.mjs` | Mint 32-hex capability id; store; drop; zip |
| `serve.mjs` | `/api/you-decide/*` · GET `/you-decide/t/<id>` |
| `inbox/tickets/<id>/` | NOTICE.json, propose.md, `in/`, `out.zip` (empty until later Yes) |

Did **not** clobber `/session` `/protocol` `/privacy` (still 200). Did **not** bind `aether_drop.py` 127.0.0.1 as the public drop. Server is existing `serve.mjs` on **:8787**.

## Look (chromium)

- `look-you-decide.png` — door
- `look-ticket.png` — ticket with drop hello.txt, zip button disabled

## Checks

- POST mint → `/you-decide/t/<32 hex>`
- GET zip empty → 409 `{ empty: true, not_yes: true }`
- POST drop → `inbox/tickets/<id>/in/`
- PUT propose without `NOT ACTIVE` → 400
- Sequential `T-1` → 404

## Halt

Chromium look done on `http://127.0.0.1:8787/you-decide`. Public **anphuni.com** still needs host deploy (Render/nginx) — that is the same `serve.mjs`, not lab drop.py. Set `YOU_DECIDE_INBOX` to this repo's `inbox/tickets`.

Operator zip after a later Yes: copy `out.zip` into `inbox/tickets/<id>/`.
