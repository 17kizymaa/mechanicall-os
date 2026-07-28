# Session audit — Client-one Desk + house LAN (for phone model review)

**Date:** 2026-07-28  
**Branch:** `session/client-one-delroy-reconfigure`  
**Repo:** mechanicall-os (local path on myarch: `/home/anphuni/mechanicall-os`)  
**Purpose of this file:** Self-contained attachment for analysis on a **phone** — not a substitute for git, but enough context without cloning.  
**ADB phones/devices used this session (distinct roles):**

| ADB id | Model | Role |
|--------|--------|------|
| `RZCW2038KHN` (USB) | **Samsung SM-A336B** | Operator **phone** (this audit target) |
| `192.168.1.235:5555` | eME640 Android-x86 TV box | Client-one **Android box** (Desk WebView shell, Kodi) |

**Not ADB:** LG living-room TV on LAN (usually standby).

---

## 1. What we built (product)

**House Desk** = propose-only chat + **CURRENT.md as the product/authority** (right rail).

| Piece | Location |
|-------|----------|
| Domain / CURRENT | `domains/house-tv-desk/` |
| Terminal desk | `python/aether_desk.py` · `aether desk` |
| Web bridge + UI | `python/aether_desk_api.py` · `aether desk-serve` |
| ADB helpers (optional) | `python/aether_house_adb.py` |
| TV scripts | `scripts/tv/` |
| Stage notes | `dev/11_aether-desk-android-tv/` |
| LG stream research | `research/speculative/LG-TV-STREAM-FROM-MYARCH.md` |

### Doctrine (non-negotiable)

- **Filesystem is truth** — CURRENT.md is human authority.
- **Model proposes only** — never approves; silence ≠ permission.
- **Keys on myarch** (`~/Desktop/.env` OpenRouter) — never in APK/git/TV seed.
- **Chat history** in **browser localStorage** on the client (phone/TV WebView), not in CURRENT.
- **Desk UI is chat + CURRENT rail only** (Kodi/remote action buttons removed after reliability issues).

### UI behaviour

- Maximalist CSS (gradients; no heavy animation engines).
- **Chat left · CURRENT.md right** (stacked on narrow screens).
- **Poll CURRENT** on input focus/type (debounced) and **await re-fetch before Send**.
- First-run **closeable popup**: history stored locally on this browser / protected as non-authority.
- Server: **ThreadingHTTPServer** (fixed stuck POSTs when single-threaded + LLM).

### Run (operator host myarch = 192.168.1.241)

```bash
cd /home/anphuni/mechanicall-os
aether desk-serve --lan --port 8788 domains/house-tv-desk
# Phone / TV browser:
# http://192.168.1.241:8788/
```

Health shape: `{ "ok", "backend", "mode": "chat-only", "ui": "maximalist-current-rail", "store": "2" }`

---

## 2. Architecture under test

```
Human edits CURRENT.md (authority / product)
        │
        ▼
Desk right rail GET /current  ←── polls on chat input + before-send
        │
Chat left ──POST /chat──► myarch desk_turn ──injects CURRENT──► OpenRouter free
        │
        └── reply is proposal only; history → localStorage
```

**Client-one CURRENT** (promo / chat sparks): entertainment preview→accept, grocery-analysis methodology, Outlook/email→files, “explain this to someone.”  
**Next** field (at write time): `pick-a-thread-and-chat` (may drift if re-edited).

---

## 3. LAN inventory (critical: three screens)

| IP | Identity | Role |
|----|----------|------|
| **192.168.1.241** | myarch (Arch desktop) | Operator host · Desk backend · intended **stream origin** |
| **192.168.1.235** | eME640 · Android 8.1 x86 · ~2.8 GB RAM | Client box: Desk in WebView shell, Kodi, seed `/sdcard/Mechanicall/` |
| **192.168.1.179** | MAC `44:27:45:83:54:12` · **LG Innotek** | **Living-room LG TV** (usually standby; WOL did not wake without TV network-standby settings) |
| **192.168.1.189** | Amazon Fire TV Stick “delroy's 2nd FireTVStick” | Alternate sink / DIAL |
| 192.168.1.254 | OpenWrt | Router |
| 192.168.1.81 | TP-LINK | AP |

**Correction made in-session:** Streaming offload research targets the **LG**, not eME640. eME640 is light control/propose; myarch is compute/guide; LG is display sink when awake.

See: `research/speculative/LG-TV-STREAM-FROM-MYARCH.md`  
Recommended path: **Jellyfin/DLNA on myarch → LG apps**; optional webOS SSAP after human accept; no heavy encode on eME640.

---

## 4. ADB results (session)

### 4.1 Devices present (end of session)

```
RZCW2038KHN            device usb  product:a33xnseea model:SM_A336B   ← PHONE
192.168.1.235:5555     device      model:eME640__________            ← Android box
```

### 4.2 eME640 (Android box) — verified earlier

- Android 8.1 · abi **x86** · MemTotal ~2.8 GB  
- Packages of note: `org.xbmc.kodi`, `org.chromium.webview_shell`  
- Movies on device: Big Buck Bunny full + sample under `/sdcard/Movies/`  
- Seed pushed: `/sdcard/Mechanicall/{CURRENT.md,library/,bridge.url,open-desk.sh,…}`  
- Device can `wget` `http://192.168.1.241:8788/health`  
- Desk opened via:  
  `am start -a VIEW -d http://192.168.1.241:8788/ -n org.chromium.webview_shell/.WebViewBrowserActivity`  
- Live chat from host returned titles like **Big Buck Bunny** and CURRENT Next correctly.

### 4.3 Samsung phone (SM-A336B) — for this handoff

- Serial **RZCW2038KHN** attached USB at audit time.  
- This audit file is intended to be **pushed/shared to this phone** for offline model review.  
- Phone can also open Desk in browser on same Wi‑Fi: `http://192.168.1.241:8788/` (myarch must run desk-serve).

### 4.4 Reliability bug found + fixed

- Symptom: user message on device “never got a reply.”  
- Logs: TV often never completed `POST /chat`; TCP **Recv-Q** stuck; single-threaded server blocked during LLM.  
- Fix: threaded server + XHR client + chat-only UI.

---

## 5. Stages completed (ICM `dev/11_aether-desk-android-tv`)

| Stage | Outcome |
|-------|---------|
| 01–04 | Domain, desk_turn, desk-serve, HTML surface |
| 05 | house-remote Desk links (later chat-only strip for Desk itself) |
| 06–08 | Smoke + device UAT (eME640) |
| 09 | WebView path live; custom APK scaffold only (no SDK) |
| 10 | HTML home row existed; Desk later simplified to chat+CURRENT |
| Promo CURRENT | Operator-approved promotional CURRENT for chat inspiration |
| LG research | Separate display target documented |

---

## 6. What is *not* done / open questions

- Custom Leanback **APK binary** not built (no Android SDK on host).  
- **LG** not fully woken/paired (SSAP :3000 not open while standby).  
- Jellyfin/DLNA **not deployed** yet — design only.  
- Model must never auto-play; preview→accept still human.  
- Fire Stick is a fallback sink, not primary guide host.

---

## 7. Key file paths (attach-friendly checklist)

```
domains/house-tv-desk/CURRENT.md
domains/house-tv-desk/README.md
python/aether_desk.py
python/aether_desk_api.py
scripts/tv/README.md
scripts/tv/desk-smoke.sh
scripts/tv/install-desk-on-device.sh
dev/11_aether-desk-android-tv/CONTEXT.md
dev/11_aether-desk-android-tv/08_device-uat/output/VERIFICATION.md
research/speculative/LG-TV-STREAM-FROM-MYARCH.md
docs/FREE-API.md
```

Sibling tree (not always in this git commit): `~/one-off-TV-box-OS/` (Kodi, house-remote, CLIENT-ONE-DEMO).

---

## 8. Review prompts for the phone model

1. Does CURRENT-as-product + poll-on-input correctly separate **authority** from **chat history**?  
2. Is LG vs eME640 vs Fire Stick role split sound for a family living room?  
3. Rank next engineering: Jellyfin on myarch, webOS SSAP, or Desk propose-play UX only?  
4. Any doctrine violations (model approve, secrets, heavy on-device LLM)?  
5. How should “preview→accept entertainment proposal” be represented in CURRENT without giving the model playback tools?

---

## 9. One-paragraph pitch

Mechanicall Client-one Desk is a propose-only web chat on the operator desktop that treats a human-owned CURRENT.md file as the live product surface (shown and re-polled while chatting). The weak eMachine Android box and the operator’s phone only render that UI; API keys and LLM calls stay on myarch. A separate LG TV on the LAN is the intended living-room display for future offloaded streaming from myarch—not the eME640. History stays in the browser; authority stays in files; silence is never permission.

---

*End of audit. Prefer this file + branch name over chat transcript for cross-model review.*
