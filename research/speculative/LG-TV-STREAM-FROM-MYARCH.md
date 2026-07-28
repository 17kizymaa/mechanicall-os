# LG living-room TV ← myarch backend stream (not eME640)

**Date:** 2026-07-28  
**Correction:** Entertainment **display** target is the **LG** on the LAN (usually standby), **not** Client-one eME640 (`192.168.1.235`).

---

## Devices on this LAN (facts)

| Host | MAC / vendor | Role |
|------|----------------|------|
| **192.168.1.179** | `44:27:45:83:54:12` · **LG Innotek** | **Likely living-room LG webOS TV** — ping timeout when standby (normal) |
| 192.168.1.235 | eMachine eME640 | Client-one **Android box** (Desk, Kodi, light local) — **not** the big TV |
| 192.168.1.189 | Amazon · “delroy's 2nd FireTVStick” | Fire TV Stick (DIAL/UPnP) |
| 192.168.1.241 | myarch | Operator desktop · stream **backend** |
| 192.168.1.81 | TP-LINK | AP / wifi gear |
| 192.168.1.254 | OpenWrt | Router |

eME640 can stay a **control surface** (Desk chat / propose). The **LG** is the **lean-back screen** we stream *to*.

---

## Goal

When someone **proposes** “browse / play something,” **decode / guide / heavy UI** run on **myarch** (NVIDIA 1660 Super · ffmpeg · docker · plenty of RAM). The LG only **receives** a stream or a cast session — not a full media server.

---

## Architecture options (ranked for this house)

### A. **Recommended v1 — myarch media server + LG native apps (DLNA / network share)**

```text
myarch
  Jellyfin or simple DLNA (minidlna / jellyfin)
  library on host disk
       │  DLNA / HTTP
       ▼
LG webOS  →  built-in Photo & Video / Jellyfin app / browser
```

| Pros | Cons |
|------|------|
| No VM required | Need LG awake + app pairing |
| Uses TV apps designed for this | Library scan is host-side (good) |
| Offloads transcoding to myarch (Jellyfin + NVENC) | First-time LG network standby / LG Connect Apps setup |

**Fit:** Best “TV guide + on-demand” without inventing a protocol.

### B. **Cast / control plane — webOS SSAP + URL open**

LG webOS (when on): SSAP on **:3000** / **:3001** (after pairing).  
myarch: `aiopylgtv` / `lgwebos` style client → power on (if supported), open app, pass **http://192.168.1.241:…/item.m3u8**.

| Pros | Cons |
|------|------|
| Desk can *propose* “play X on LG” then human accepts → script | Pairing key UX once |
| Thin TV role | WOL unreliable unless “network standby” enabled on TV |

### C. **HDMI out from myarch (virtualised “living room PC”)**

```text
myarch KVM/container GPU → HDMI capture or second GPU output → LG HDMI
```

or simpler: **myarch HDMI → LG** when cables allow (no network).

| Pros | Cons |
|------|------|
| Full desktop / browser / any app | Cable topology; not “anywhere on LAN” |
| Zero TV apps | Occupies GPU / display |

Only if HDMI is already in the room path. Prefer network for “standby LG wake → stream.”

### D. **Heavy VM “streamer” container (optional later)**

Docker/KVM on myarch runs Jellyfin + ffmpeg only (not a full desktop).  
TV remains a **client**. Do **not** put the media brain on eME640 (~2.8 G RAM, old CPU).

```text
❌ eME640 as stream origin
✅ myarch as origin
✅ LG as sink
✅ eME640 optional Desk remote / secondary
```

### E. **Fire Stick as middle sink**

Already on LAN (`delroy's 2nd FireTVStick`). Can cast/DLNA to Stick while LG is on HDMI input for Stick.  
Useful **fallback** if webOS pairing is painful; still not “compute on eME640.”

---

## “Complete TV guide” shape (product)

| Layer | Where | Job |
|-------|--------|-----|
| Library + metadata + poster wall | **myarch** Jellyfin (or Kodi-on-desktop headless) | Guide |
| Transcode / bitrate ladder | **myarch** ffmpeg / NVENC | Offload |
| Authority / propose | Desk + CURRENT.md | “Play Bunny?” → proposal |
| Accept | Human (phone Desk / remote) | silence ≠ yes |
| Render | **LG** | Decode HLS/DLNA only |

Desk never auto-plays; it proposes a title + “accept to wake LG and start stream.”

---

## Standby / discovery notes

- LG **Innotek** MAC seen in ARP as **STALE**; ICMP fails → classic **sleep**.
- Wake-on-LAN may need TV setting: *Mobile TV On* / *Network Standby* / *LG Connect Apps*.
- After wake: re-probe `192.168.1.179:3000` (SSAP) and SSDP MediaRenderer.
- Prefer **DHCP reservation** on OpenWrt for `.179` so guide URLs stay stable.

---

## Immediate operator checklist

1. **Confirm model** on the LG sticker (webOS year helps for SSAP).  
2. On LG (once on): enable network standby + LG Connect Apps; note IP stays `.179`.  
3. From myarch: `ping 192.168.1.179` → open `http://192.168.1.179:3000` behaviour.  
4. Pick **A (Jellyfin/DLNA)** for guide+stream; add **B (SSAP)** for one-tap after human accept.  
5. Keep eME640 out of the encode path; Desk may still **propose** from Client-one chat.

---

## Explicit non-goals (for this note)

- Replacing HDMI for all cases  
- Running Jellyfin on eME640  
- Model-auto power-on / play without human accept  
- Confusing LG with Fire Stick or eME640 in CURRENT docs  

---

## One-sentence architecture

**myarch is the streaming PC and TV guide; the LG is a dumb beautiful decoder (when awake); eME640 is optional control/propose, not the media brain.**
