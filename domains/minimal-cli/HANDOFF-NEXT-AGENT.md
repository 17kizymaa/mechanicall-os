# Handoff — next agent (desk / operator host)

**Fork name:** product desk on operator host  
**Date:** 2026-07-28 (session fork after multi-hour hardware detour)  
**Branch:** `session/client-one-delroy-reconfigure`  
**Project root for desk:** `domains/minimal-cli/` (or any dir with this CURRENT + HANDOFF)

---

## Read first (in order)

1. This file  
2. `CURRENT.md` (same directory) — **authority**  
3. Optional: `README.md`  
4. Do **not** load or continue eME640 GRUB/USB/eth recovery unless CURRENT Next says so  

---

## Where this conversation forked

**In scope (continue):**

- Mechanicall product: **CURRENT.md is the product**
- Operator machine **myarch** is the work host  
- **`aether desk`**: quiet terminal chat only (privacy banner → hello → type)  
- Free frontier API: **OpenRouter** (key in `~/Desktop/.env` as raw `sk-or-…` line)  
- Human edits CURRENT by hand; model **proposes only**; empty line ≠ yes; model never approves  

**Out of scope (parked — do not reopen casually):**

- eME640 “jet engine” laptop: GRUB loops, Alpine USB remakes, InsydeH20, eth `10.99.0.x`, quiet-chat-on-device  
- Multi-hour boot recovery; Android boot fix via live USB; partition migration  
- Treat as backlog label only: `eme640-boot-and-chat` (separate session, single success criterion if ever resumed)

---

## Code / files that matter

| Path | Role |
|------|------|
| `python/aether_desk.py` | Quiet chat UI; loads Desktop `.env`; no slash commands |
| `python/aether_llm.py` | OpenRouter / Groq / paid backends; prefer free OpenRouter when key present |
| `aether` → `desk` | CLI entry: `aether desk [path]` |
| `docs/FREE-API.md` | How to set keys |
| `domains/minimal-cli/CURRENT.md` | Authority for this domain |
| `~/Desktop/.env` | Secrets (not in git); OpenRouter `sk-or-…`, optional `ghp_…` as GITHUB_TOKEN only |

**Launch:**

```bash
cd /home/anphuni/mechanicall-os/domains/minimal-cli
aether desk
# keys auto-load from ~/Desktop/.env
```

---

## Product doctrine (non-negotiable)

1. Filesystem is truth; **CURRENT.md** is live authority.  
2. Desk chat = probabilistic **propose** layer, not a second control plane.  
3. Silence is never permission.  
4. Do not nag for `aether approve` when the human has already rejected ceremony (see session log: emotional-involuntary approve aversion).  
5. Prefer small reversible steps; no new frameworks for chat.  

---

## Suggested Next for the next agent

Unless human overrides CURRENT:

| Priority | Action |
|----------|--------|
| P0 | Help human use `aether desk` for real work; fix only real pain (errors, missing key, bad banner) |
| P1 | Help hand-edit CURRENT for a **named domain goal** (not hardware) |
| P2 | Only if human says so: open a **new** CURRENT for `eme640-boot-and-chat` with one goal: cold boot → Android |

**Do not:**

- Restart USB/GRUB/Insyde debugging without explicit human request  
- Put heavy local LLM on eME640 (thermal — “sounds like a jet engine”)  
- Expand desk back into slash-command / panel / multi-tool surface without ask  

---

## Hardware truth (for later, not now)

If a future session must touch the TV box laptop:

- Host: eME640, Android-x86 8.1 32-bit, install dir `android-2019-06-11` on **sda5 / ATVSYS / (hd0,msdos5)**  
- When on LAN often **192.168.1.235:5555** (ADB); root via `adb root` when online  
- Working cmdline once up:  
  `root=/dev/ram0 androidboot.hardware=android_x86 SRC=/android-2019-06-11 DATA=data androidboot.selinux=permissive`  
- Source of partition map: `~/one-off-TV-box-OS/` (not firestick-sideloading)  
- Problem was bootloader/default boot, not “Android missing”  

---

## One-sentence pitch for the next agent

You are on the **operator host**, running a **minimal propose-only chat desk** over **CURRENT.md**; finish product/UX here and leave the eME640 hardware saga parked until the human reopens it with a single explicit goal.
