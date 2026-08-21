# APP-CORE — Mechanicall phone seat

**Not CURRENT. Not Yes.** Opening this file is not Yes.

## Pitch (one breath)

You bind **your** folder. You read the plan. The desk drafts in chat. **You** Decide. Tomorrow you can open the receipt.

## The walk (the product)

| # | Stage | What it is | What it is not |
|---|-------|------------|----------------|
| 01 | **Bind** | Name a folder that is not mechanicall-os. Default `mechanicall-pocket`. Picker is support. | Yes. Operator tree. |
| 02 | **Plan** | CAPITALISED CURRENT fields. Detailed markdown is a dropdown. | A sermon. A dump into the model. |
| 03 | **Chat** | Thread + composer. Desk sees schema + last 3 user turns + **file names**. Stage chip on glass. | Yes. CURRENT file. Full jsonl. Client verbs. |
| 04 | **Decide** | Two-tap + required Why. Only human Yes. | Chat saying “approve”. Silence. |
| 05 | **Receipt** | You said / RECEIPT.md / last events. | A second CLI. |

One-way in spirit: Bind before Plan, Plan before Chat, Chat drafts, Decide actualises, Receipt remains. The rail lets them jump; it does not make later stages required.

## Chat ICM (so the local model is not overwhelmed)

Turn classifier (no extra model call): `show-plan` | `propose` | `gate`.

| Stage | Desk sees | Desk may write |
|-------|-----------|----------------|
| show-plan | schema + 3 user turns + file **names** | nothing |
| propose | same | PROPOSE only |
| gate | **no Ollama** | nothing — “Use Decide” |

Caps: no full CURRENT, no full PROPOSE, no full jsonl, say ≤ 240 chars, last 3 user turns ≤ 280 chars.

## Not core

- Client verb dump (current/brief/validate chips)
- Six independent Sit rooms with no walk
- Play Store / Funnel / public Ollama
- Model `aether approve` / `next` / rewrite CURRENT
- `pack_tree_context` stuffed into Chat Send

## Chrome

- Splash logo, then **land on the derived walk stage**
- Bottom rail: `01 Bind · 02 Plan · 03 Chat · 04 Decide · 05 Receipt`
- Hamburger: **PROJECT files only** (read; opening is not Yes)
- Chat: stage on bubbles; Clear thread; gate offers Open Decide

## Law

Open / Bind / Send / GET ≠ Yes. Silence ≠ Yes. Gate never proposes.

## Version this contract ships as

`0.7.0-core` (lab sideload).
