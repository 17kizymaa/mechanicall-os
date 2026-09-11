# RECEIPT — you-decide-os-cycle (2026-09-09)

**Not Yes.** Drop / download / pull / put-zip / this receipt are not Mechanicall Yes.  
Live CURRENT stays SELECT / REJECTED. Models did not `aether approve` / `aether next`. CURRENT.md bytes were not rewritten this stage.

## Preflight

`aether preflight you-decide-os-cycle` → ALLOW (Phase=SELECT Status=REJECTED). Probe ALLOW. Validate OK.

Last human event before this work: reject 14:35 — *Need to validate that the website can handle around 10 requests in a day. Does the website even have a logical backend for this?*

## Door (apex)

- Commit `7ca0d13` on `anphuni.com` `main` (push `6b2e77f..7ca0d13`)
- Health inbox **before:** `/opt/render/project/src/data/you-decide` (ephemeral)
- Deploy: 200 → 502 → **200**
- Health inbox **after:** `/var/data/seats/you-decide` (seats disk)

| Path | Code |
|------|------|
| `/you-decide` | 200 |
| `/session` `/protocol` `/privacy` | 200 |
| GET zip before drop | 409 empty, not Yes |

## Operate + receive (this tree)

Ticket: `4ee13598c7855f0f84f56efbf2627d68`  
https://anphuni.com/you-decide/t/4ee13598c7855f0f84f56efbf2627d68

| Step | Result |
|------|--------|
| POST mint | path `/you-decide/t/4ee13598…`, `not_yes` |
| POST drop `offer.txt` | 24 B, `os-cycle-offer-20260909` |
| `you_decide_os.py pull` | `inbox/tickets/4ee13598…/NOTICE.json` + `in/offer.txt` |
| `cat` / `grep` in this tree | offer line present |
| put-zip 251 B | site `zip.ready`, local `out.zip` |
| GET `/zip` | 200, 251 B, bytes match, download ≠ Yes |
| ticket propose.md | still **NOT ACTIVE** |

Prior apex ticket `a7d0de04…` is **404** after the inbox moved off ephemeral `src/data`. Expected.

## 10 / day

Mint limiter on the door is **10 tickets / 10 minutes / client**. Ten requests in a day sit inside that cap. This halt did **one** full cycle, not a synthetic 10-mint burst.

Logical backend for the operator: mechanicall-os `inbox/tickets/<id>/` (gitignored blobs). Apex holds the live door on the seats disk; pull/put copies by capability URL. No accounts. No sequential public ids. Lab `127.0.0.1` was not bound. Local `:8787` was not restarted.

## Stills

- `apex-you-decide.png` — door
- `apex-ticket.png` — drop `offer.txt (24 B)` · zip ready (251 B)

## Following (NOT ACTIVE)

`.aether/proposals/CURRENT-proposal-20260909-os-cycle-following.md` — parked. CURRENT unchanged.

## Halt

Human stamps CURRENT. Models do not `aether next`. Generate stays parked.
