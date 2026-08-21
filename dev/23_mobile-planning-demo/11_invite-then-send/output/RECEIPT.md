# Receipt — 11 invite-then-send

**When:** 2026-08-18  
**Human:** picked option 1 (invite their email, then send tailnet URL)  
**Preflight:** `mobile-planning-demo` ALLOW  
**Operator CURRENT:** not rewritten. Next still `mobile-planning-demo`.  
**Invite:** **not sent by this CLI.** Operator must click Invite at https://login.tailscale.com/admin/users using the friend’s **own** email.

## Face (up)

```bash
export POCKET_HOST_TWIN="$HOME/brake-friend-sit"
export POCKET_FACE_HOST=100.90.85.68
export POCKET_FACE_PORT=8765
export POCKET_SYNC=0
sh scripts/send-brake.sh
```

| | |
|--|--|
| Send this URL | `http://100.90.85.68:8765/` |
| Listen | `100.90.85.68:8765` (not `0.0.0.0`, not `127.0.0.1`) |
| Twin | `~/brake-friend-sit` |
| Phone sync | `POCKET_SYNC=0` |

## Checks this turn

| Check | Result |
|-------|--------|
| Twin refuse operator tree | accepted `~/brake-friend-sit` |
| `GET /` | 200, `Cache-Control: no-store`, title **You have not said yes yet** |
| `GET /yes` | **404** |
| `GET 127.0.0.1:8765` | connection refused |
| Twin CURRENT / RECEIPT / PROPOSE sha256 | **unchanged** after GET |
| Friend `RECEIPT.md` | still “No sitting yet.” |
| Funnel / serve HTTPS | not enabled |
| POST `/yes` | **not sent** |

Tailnet peers (wol-pi, mbp-edge, kamilas-tab-s9-fe) answered `tailscale ping`. `tailscale status` still prints this host as `offline` even though `BackendState=Running` — do not treat that line as “friend can already open the page.”

`kamilas-tab-s9-fe` is already on this tailnet as `17kizymaa@`. That is **not** a stranger sitting.

## What you do next (human)

1. Invite **their** email: https://login.tailscale.com/admin/users  
   Do **not** tell them to log in as `17kizymaa@gmail.com`.
2. After they accept, send only: `http://100.90.85.68:8765/`
3. Stay on the host until they tap Yes or Not yet.
4. Opening the page is not a Yes.

## Do not claim

- Invite was sent
- Friend connected
- Friend tapped
- Website hosts the gate
- APK assembled
- Operator CURRENT rewritten
