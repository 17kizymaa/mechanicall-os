# Handoff — tailnet invite in the app, then Wake myarch

**When:** 2026-08-19  
**For:** next agent / operator, after Mechanicall `0.2.0-seat` is on the A33  
**Not law.** Operator CURRENT is still SELECT / **REJECTED** / Next `people-app-phone-seat`. This file does not `aether approve`. Opening the app is not Yes. Invite is not Yes. Wake is not Yes.

---

## What you asked for (in one chain)

The phone is the **seat**. **myarch** is the **backend** (Ollama / host). myarch **sleeps**. **wol-pi** is already on the tailnet and can send Wake-on-LAN.

A sitting away from the desk only works if:

1. The person on the phone is **on your tailnet as themselves** (invite — **not** `17kizymaa@gmail.com`).
2. They can reach **wol-pi** (`100.91.173.127` last seen).
3. A button in Mechanicall tells wol-pi: **wake myarch**.
4. When myarch is up (`100.90.85.68`), the app’s “Agent edit draft” can talk to Ollama on Tailscale. Public `:11434` stays refused. Funnel stays refused.

That is why invite is **in the app**, not a homework assignment at `login.tailscale.com/admin/users`. 18 August already proved: admin-click invite + “don’t log in as me” still failed as a send path because the friend never got through the door. The APK is on the A33 now; the door is still missing.

```
  Mechanicall on A33
        │  (1) Invite — their email / their Tailscale identity
        ▼
  Tailnet (same one as myarch, wol-pi, mbp-edge)
        │  (2) Button: Wake myarch
        ▼
  wol-pi  ──magic packet──►  myarch NIC
        │  (3) Backend up
        ▼
  myarch:11434  (Tailscale only)
        │  (4) Agent edits DRAFT only
        ▼
  Plan / Yes / Not yet  (still their tap; still not GET)
```

---

## What is already true

| Piece | State |
|-------|--------|
| A33 app | Sideloaded **Mechanicall** `0.2.0-seat` (`com.mechanicall.pocket.demo`). Plan · Draft · Yes (two-tap) · Not yet · Receipt. |
| Pocket | `/sdcard/mechanicall-pocket/CURRENT.md` exists (16 Aug). Opening/Load is not Yes. |
| myarch | Backend host. CURRENT **Host:** myarch. Ollama on Tailscale `100.90.85.68`. |
| wol-pi | Tailnet peer; the always-on box that can WoL when myarch is asleep. |
| mbp-edge | USB ADB for sideload only. Not the backend. |
| Law | Their identity, not operator email. No Funnel. No public Ollama. Models never approve. |
| Invite (old) | Human at Tailscale admin. CLI **cannot** invite. Friend receipt: no sitting. `kamilas-tab-s9-fe` on the tailnet **as you** is not a stranger. |

---

## What this is **not**

- **Not** “install Tailscale and log in as `17kizymaa@`.” That is Tailscale-as-me. Already failed. Stay failed.
- **Not** Funnel / `0.0.0.0:11434` / a public wake URL. The whole point of invite is to stay **on the tailnet**.
- **Not** Yes. Invite does not apply CURRENT. Wake does not apply CURRENT. Agent still writes **draft only**.
- **Not** a second Next. Dual-concurrent-next is prohibited. This is the phone seat **becoming usable when the desk is asleep** — still `people-app-phone-seat` until you re-SELECT.
- **Not** Play Store. Not rewriting pocket CURRENT from this tree. Not `aether approve` from the model.

---

## The honest gap (so the next build does not lie)

Tailscale does not let a random APK invite people with no operator secret. Today the invite is an **admin click**. To put invite **in Mechanicall** you still need one always-on, already-on-tailnet box (wol-pi) holding a **Tailscale API token** (not in git) that:

1. Accepts **their** email from the app (or opens an invite link the box minted).
2. Creates a tailnet invite / auth path for **that** identity.
3. Never uses the operator Google/Apple account as the sitter.

Until that token + a tiny service exist on wol-pi, a button labelled Invite is decoration. Same as an APK with no `aether` on the pocket.

WoL button is the same shape: Mechanicall → (tailnet) → wol-pi → magic packet to myarch’s MAC. wol-pi must already be up. The phone cannot WoL myarch from LTE without first being on the tailnet. **Invite is the first mile; Wake is the second.**

---

## Face (when you implement — not this file)

Keep the seat. Do not become a verb museum. Two extra controls, not the main story:

- **Join network** — invite as them. Status: not on tailnet / invited / connected. Not Yes.
- **Wake desk** — only enabled when on tailnet. Talks to wol-pi. Status: sleeping / waking / myarch up. Not Yes.

Plan / Draft / Yes / Not yet / Receipt stay the product. Wake is so “Agent edit draft” has a host. Invite is so Wake can be reached from a pocket that is not on the LAN.

---

## What I will not do until you say so

- Implement Invite or Wake in the APK this turn.
- Put Tailscale API secrets in git.
- Funnel.
- Approve CURRENT.
- Tap Yes on the A33.

You still own `aether approve`. This handoff is so the next turn (or you) can extend the **same** phone app instead of inventing a second product.

Silence is never permission.
