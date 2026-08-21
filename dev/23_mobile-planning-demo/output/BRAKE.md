# BRAKE — the sitting face

**When:** 2026-08-18  
**Next:** `mobile-planning-demo` (demo only — not Play Store, not Mechanicall-core)  
**Worth:** the first time someone can say “I didn’t say yes” — and the machine has to live with that.

This page is the contract for the **sendable face**. Chrome (URL or APK) must match it. Law stays `bin/aether` in a pocket folder **outside** this repo.

---

## One sentence (say this out loud)

You have not said yes yet. Opening the page is not a yes. Only the green button is.

---

## One screen

```
[ Plan — what is allowed right now          ]
[ Draft — a proposal, not the plan          ]
[ Yes ]     [ Not yet ]
[ Receipt — what you decided last time      ]
```

| Face | Meaning |
|------|---------|
| **Plan** | Their pocket `CURRENT.md` (read-only) |
| **Draft** | `PROPOSE-CURRENT.md` — save does not change the plan |
| **Yes** | Apply the visible draft, then record human Yes |
| **Not yet** | Leave the plan. The machine does not pretend they agreed |
| **Receipt** | `RECEIPT.md` they can open tomorrow without you |

No verb museum. No bubble chat as the face. The word **aether** does not appear on the face.

---

## Law the chrome must not break

- **GET is never Yes.** `GET /yes` is 404. Reload does nothing to the plan.
- **Silence is never Yes.** Closing the tab, waiting, “looks good” in chat — none of these apply.
- The agent may edit the **draft only**.
- Yes is POST (URL) or an explicit tap (APK) that calls the same `yes()` as the tests.
- Refuse if the bind path is the mechanicall-os operator tree.
- No public bind of the model. Face may be LAN or Tailscale. Not `0.0.0.0` as a product.

---

## What they keep tomorrow

`RECEIPT.md` in **their** pocket folder:

- when
- they said Yes or Not yet
- what the Next was
- a short trail

You can forward that file. They should not need this git tree to read it.

---

## How you send it (this week)

1. **URL first** — `sh scripts/send-brake.sh` prints a link. Friend opens it on their phone. You host the face.
2. **APK second** — same table, sideload lab chrome (`android/`). Same engine. Not a store listing.

Phone sync (`adb` / A33) is **off** unless you set `POCKET_SYNC=1`.

---

## Honest limits (say these)

- Demo sitting. Not an app-store product.
- The model on the desk may see the **whole pocket folder**. Put only what they may send.
- Chat dies. Plan + draft + receipt remain.
- If nobody who is not you ever taps, this Next is decoration.

---

## Face copy (use these strings)

- Title: **You have not said yes yet**
- Sub: Opening this page is not a yes. Only **Yes** is.
- Yes button: **Yes**
- Not yet button: **Not yet**
- Confirm Yes: Apply the draft and record that you said yes?
- Footer: GET never Yes. Silence is never permission.
