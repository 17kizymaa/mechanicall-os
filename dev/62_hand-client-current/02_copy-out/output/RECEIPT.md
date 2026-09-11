# RECEIPT — 02_copy-out

**Not Yes.** Not a client stamp. Not 03 hand-off.  
**Action id:** `hand-client-current`  
**When:** 2026-09-11T10:55:05Z  
**Preflight:** allowed (`hand-client-current` matches Next; Phase=APPROVE Status=APPROVED)  
**Human Yes (operator tree):** 2026-09-11T10:53:00Z — *I think this plan covers the shape of what I want to do today! A great outline-style contract ensuring that the 3 sprints go in the right direction!*

## What left the git tree

Dest root (outside mechanicall-os): `/home/anphuni/client-offers`

| Alias | Dest | Objective | Next | Approval | CURRENT sha256 |
|-------|------|-----------|------|----------|----------------|
| `happy-birthday` | `/home/anphuni/client-offers/happy-birthday` | A paper-trading site. | `paper-trading-site` | PENDING | `47bb74a6b9d6519c855f319214d9ea97321f7c2feab4d37cf1086100eb7d29e7` |
| `hi-its-mother` | `/home/anphuni/client-offers/hi-its-mother` | An open invitation to collaborate. | `open-invite` | PENDING | `c961057fe24b955a32283196e658308b2b2d393cc0375178095cdc510bd00a4d` |
| `this-works` | `/home/anphuni/client-offers/this-works` | A food-tasting app. | `food-tasting-app` | PENDING | `6ebf6c8e60c6b5162bd894deb9e601776d6e352126a176f85826db21cb133f04` |

Each dest holds `CURRENT.md` + `HOW-TO-ACCEPT.md` only.  
`aether current validate` **PASS** on all three.  
No `.aether/` created in dest. Operator did not `aether approve` there.

## Rewrite after reject (2026-09-11T10:56Z)

Human reject: *OOPS - forgot about the 'app' and 'site' identifications. Let us unidentify them for now.*

Dest CURRENT files for `happy-birthday` and `this-works` were rewritten to drop site/app. Approval still PENDING. **Not handed. Not a new Yes.** Wait for operator `aether approve` before 03.

## What this is not

- Not handed to a person (03).
- Not a zip (carrier later; zip is not the product).
- Not sequential ids.
- Not millwork / Generate.
- Drafts under `.aether/proposals/clients/` remain in-repo factory copies (NOT ACTIVE as law).

## Behaviour

`dev/62_hand-client-current/scripts/copy_out_packs.py`  
Refuses dest inside mechanicall-os git. Refuses if Approval is not PENDING.
